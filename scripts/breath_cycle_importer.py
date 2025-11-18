"""Import SICC Breath Cycle workflow runs and normalize them for Tyme.

The importer uses the GitHub API to pull workflow runs and log excerpts,
normalizes timestamp and duration data, and emits two artifacts:

- ``chronicle/TYME-PULSE-GENESIS.json`` — machine-friendly pulse lineage
- ``chronicle/TYME-PULSE-WAVE.yaml`` — human-readable pulse wave ledger

It also installs breath pacing into the internal metabolic loop by
writing a pacing snapshot to ``heartbeat/logs/metabolic_loop.json``.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import textwrap
import urllib.error
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.metabolic_loop import MetabolicLoop

API_BASE = "https://api.github.com"
DEFAULT_OWNER = "sovereign-codex"
DEFAULT_REPO = "SICC"
DEFAULT_WORKFLOW = "breath"


def github_request(path: str) -> Optional[dict]:
    """Perform a GitHub API request and return the parsed JSON body.

    Returns ``None`` on an HTTP or network error to keep the importer
    resilient when endpoints are unavailable.
    """

    url = f"{API_BASE}{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Tyme-Breath-Cycle-Importer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] GitHub request failed for {url}: {exc}")
        return None
    except urllib.error.URLError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] Network error while reaching {url}: {exc}")
        return None


def parse_timestamp(value: str | None) -> Optional[datetime]:
    """Parse an ISO8601 timestamp and normalize to UTC."""

    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).astimezone(UTC)
    except ValueError:
        return None


def resolve_workflow_id(owner: str, repo: str, needle: str) -> Optional[int]:
    """Resolve a workflow identifier by matching name, path, or numeric id."""

    if needle.isdigit():
        return int(needle)

    response = github_request(f"/repos/{owner}/{repo}/actions/workflows")
    if not response:
        return None

    workflows = response.get("workflows", [])
    for workflow in workflows:
        candidates = (
            str(workflow.get("id", "")),
            (workflow.get("name") or "").lower(),
            (workflow.get("path") or "").lower(),
        )
        if needle.lower() in candidates:
            return int(workflow.get("id"))
    return None


def fetch_workflow_runs(owner: str, repo: str, workflow_id: int, limit: int) -> List[dict]:
    """Fetch workflow runs for the given workflow identifier."""

    response = github_request(f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs?per_page={limit}")
    if not response:
        return []
    return response.get("workflow_runs", [])


def fetch_run_log_excerpt(owner: str, repo: str, run_id: int, line_limit: int) -> List[str]:
    """Download a workflow run's logs and return a truncated list of lines."""

    url = f"{API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}/logs"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Tyme-Breath-Cycle-Importer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            archive = response.read()
    except urllib.error.HTTPError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] Unable to download logs for run {run_id}: {exc}")
        return []
    except urllib.error.URLError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] Network error while fetching logs for run {run_id}: {exc}")
        return []

    lines: List[str] = []
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name in sorted(zipped.namelist()):
            with zipped.open(name) as payload:
                content = payload.read().decode("utf-8", errors="replace")
                for line in content.splitlines():
                    lines.append(line.strip())
                    if len(lines) >= line_limit:
                        return lines
    return lines


def normalize_run(run: dict, owner: str, repo: str, line_limit: int) -> dict:
    """Normalize run metadata and include a log excerpt."""

    started_at = parse_timestamp(run.get("run_started_at") or run.get("created_at"))
    completed_at = parse_timestamp(run.get("updated_at"))
    duration = None
    if started_at and completed_at:
        duration = (completed_at - started_at).total_seconds()

    run_id = int(run.get("id", 0))
    logs = fetch_run_log_excerpt(owner, repo, run_id, line_limit) if run_id else []

    def timestamp_to_iso(dt: Optional[datetime]) -> Optional[str]:
        return dt.isoformat(timespec="seconds") if dt else None

    log_excerpt = [line for line in logs if line][:line_limit]
    return {
        "run_id": run_id,
        "name": run.get("name"),
        "event": run.get("event"),
        "status": run.get("status"),
        "conclusion": run.get("conclusion"),
        "head_branch": run.get("head_branch"),
        "started_at": timestamp_to_iso(started_at),
        "completed_at": timestamp_to_iso(completed_at),
        "duration_seconds": duration,
        "log_excerpt": log_excerpt,
    }


def summarize_cycles(cycles: Iterable[dict]) -> Dict[str, Optional[float]]:
    """Compute aggregate statistics for a list of normalized cycles."""

    durations = [cycle.get("duration_seconds") for cycle in cycles if isinstance(cycle.get("duration_seconds"), (int, float))]
    if not durations:
        return {"count": 0, "average_duration_seconds": None, "longest_duration_seconds": None}

    average = sum(durations) / len(durations)
    longest = max(durations)
    return {
        "count": len(durations),
        "average_duration_seconds": round(average, 2),
        "longest_duration_seconds": round(longest, 2),
    }


def dump_yaml(data: object, indent: int = 0) -> str:
    """Lightweight YAML serializer for dict/list structures."""

    spaces = " " * indent
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, list) and not value:
                lines.append(f"{spaces}{key}: []")
            elif isinstance(value, dict) and not value:
                lines.append(f"{spaces}{key}: {{}}")
            elif isinstance(value, (dict, list)):
                lines.append(f"{spaces}{key}:")
                lines.append(dump_yaml(value, indent + 2))
            else:
                scalar = json.dumps(value)
                lines.append(f"{spaces}{key}: {scalar}")
        return "\n".join(lines)
    if isinstance(data, list):
        if not data:
            return f"{spaces}[]"
        lines = []
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{spaces}-")
                lines.append(dump_yaml(item, indent + 2))
            else:
                scalar = json.dumps(item)
                lines.append(f"{spaces}- {scalar}")
        return "\n".join(lines)
    return f"{spaces}{json.dumps(data)}"


def build_payload(owner: str, repo: str, workflow: str, limit: int, line_limit: int) -> dict:
    """Pull workflow runs, normalize them, and assemble the pulse payload."""

    workflow_id = resolve_workflow_id(owner, repo, workflow)
    if workflow_id is None:
        print(f"[WARN] Unable to resolve workflow '{workflow}' in {owner}/{repo} — proceeding with empty payload")
        runs: List[dict] = []
    else:
        runs = fetch_workflow_runs(owner, repo, workflow_id, limit)

    cycles = [normalize_run(run, owner, repo, line_limit) for run in runs]
    summary = summarize_cycles(cycles)

    payload = {
        "schema": "tyme-pulse-genesis/v1",
        "source": {
            "owner": owner,
            "repo": repo,
            "workflow": workflow,
            "workflow_id": workflow_id,
            "fetched_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "token_present": bool(os.getenv("GITHUB_TOKEN")),
        },
        "summary": summary,
        "breath_cycles": cycles,
    }
    return payload


def write_outputs(payload: dict, wave_payload: dict, genesis_path: Path, wave_path: Path) -> None:
    genesis_path.parent.mkdir(parents=True, exist_ok=True)
    wave_path.parent.mkdir(parents=True, exist_ok=True)

    genesis_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    wave_path.write_text(dump_yaml(wave_payload) + "\n", encoding="utf-8")

    print(f"[OK] TYME-PULSE-GENESIS written to {genesis_path}")
    print(f"[OK] TYME-PULSE-WAVE written to {wave_path}")


def main(argv: Optional[List[str]] = None) -> int:  # pragma: no cover - CLI entry point
    parser = argparse.ArgumentParser(description="Import SICC Breath Cycle workflow runs and generate pulse artifacts.")
    parser.add_argument("--owner", default=DEFAULT_OWNER, help="Repository owner (default: sovereign-codex)")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Repository name (default: SICC)")
    parser.add_argument("--workflow", default=DEFAULT_WORKFLOW, help="Workflow name, path, or id (default: breath)")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of runs to import (default: 10)")
    parser.add_argument("--log-lines", type=int, default=40, help="Maximum number of log lines per run (default: 40)")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("chronicle"),
        help="Directory where TYME-PULSE artifacts are written (default: chronicle)",
    )

    args = parser.parse_args(argv)
    genesis_path = args.output_dir / "TYME-PULSE-GENESIS.json"
    wave_path = args.output_dir / "TYME-PULSE-WAVE.yaml"

    payload = build_payload(args.owner, args.repo, args.workflow, args.limit, args.log_lines)

    metabolic_loop = MetabolicLoop(genesis_path=genesis_path)
    pacing_snapshot = metabolic_loop.install(payload.get("breath_cycles", []))

    payload["metabolic_loop"] = {
        "installed_at": pacing_snapshot["updated_at"],
        "pacing_file": str(metabolic_loop.output_path),
        "breath_pacing": pacing_snapshot["breath_pacing"],
        "cycles_observed": pacing_snapshot["cycles_observed"],
    }

    wave_payload = {
        "schema": "tyme-pulse-wave/v1",
        "source": payload["source"],
        "summary": payload["summary"],
        "breath_cycles": payload["breath_cycles"],
        "breath_pacing": pacing_snapshot["breath_pacing"],
        "metabolic_loop": {
            "status_file": str(metabolic_loop.output_path),
            "installed_at": pacing_snapshot["updated_at"],
        },
        "notes": textwrap.dedent(
            """
            The wave ledger mirrors the genesis payload but is tuned for human review.
            Log excerpts are truncated to keep the pulse wave compact; use GitHub to
            inspect full traces when deeper resonance checks are required.
            """
        ).strip(),
    }

    write_outputs(payload, wave_payload, genesis_path, wave_path)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
