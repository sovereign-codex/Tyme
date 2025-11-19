"""Assimilation Engine for the Sovereign Codex repositories.

This script scans repositories in the `sovereign-codex` GitHub organization,
collects lightweight semantic signals (README headings, topics, workflows),
and writes a synthesized "Living Codex Kernel" report.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import textwrap
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import urllib.error
import urllib.request

API_BASE = "https://api.github.com"
DEFAULT_ORG = "sovereign-codex"
TIMELINE_OUTPUT = Path("chronicle/avot_archivist_timeline.json")
STOPWORDS = {
    "the",
    "and",
    "with",
    "from",
    "that",
    "this",
    "into",
    "for",
    "your",
    "repos",
    "repo",
    "code",
    "data",
    "github",
    "readme",
    "docs",
    "scrolls",
    "workflow",
    "workflows",
    "design",
    "lineage",
    "architecture",
    "patterns",
    "concepts",
    "scroll",
    "living",
    "kernel",
}


def github_request(url: str) -> Optional[dict]:
    """Perform a GitHub API request and return the parsed JSON body.

    Returns ``None`` on an HTTP error to keep the process resilient.
    """

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Tyme-Assimilation-Engine",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            if response.status >= 400:
                return None
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] GitHub request failed for {url}: {exc}")
        return None
    except urllib.error.URLError as exc:  # pragma: no cover - network dependent
        print(f"[WARN] Network error while reaching {url}: {exc}")
        return None


def fetch_repositories(org: str, limit: Optional[int] = None) -> List[dict]:
    """Fetch repository metadata for the given organization."""

    repositories: List[dict] = []
    page = 1
    while True:
        url = f"{API_BASE}/orgs/{org}/repos?per_page=100&page={page}"
        response = github_request(url)
        if response is None:
            break
        if not response:
            break
        repositories.extend(response)
        if limit and len(repositories) >= limit:
            return repositories[:limit]
        page += 1
    return repositories


def fetch_readme(owner: str, repo: str) -> str:
    """Retrieve and decode the README for a repository if it exists."""

    url = f"{API_BASE}/repos/{owner}/{repo}/readme"
    response = github_request(url)
    if not response:
        return ""

    content = response.get("content", "")
    encoding = response.get("encoding", "base64")
    try:
        if encoding == "base64":
            return base64.b64decode(content).decode("utf-8", errors="ignore")
        return content
    except Exception:  # pragma: no cover - depends on remote payload
        return ""


def fetch_workflows(owner: str, repo: str) -> List[str]:
    """List workflow files for a repository."""

    url = f"{API_BASE}/repos/{owner}/{repo}/contents/.github/workflows"
    response = github_request(url)
    if not response or not isinstance(response, list):
        return []

    workflows: List[str] = []
    for item in response:
        name = item.get("name") or item.get("path")
        if name:
            workflows.append(name)
    return workflows


def extract_headings(markdown: str) -> List[str]:
    """Extract Markdown headings as signals for concepts and architecture."""

    headings = []
    for line in markdown.splitlines():
        if line.lstrip().startswith("#"):
            title = line.lstrip("# ").strip()
            if title:
                headings.append(title)
    return headings


def derive_keywords(text_fragments: Iterable[str], limit: int = 12) -> List[str]:
    """Collect simple keyword signals from text fragments."""

    tokens = []
    for fragment in text_fragments:
        tokens.extend(re.findall(r"[A-Za-z][A-Za-z0-9\-]{3,}", fragment))

    counter = Counter(token.lower() for token in tokens if token.lower() not in STOPWORDS)
    return [word for word, _ in counter.most_common(limit)]


def fetch_latest_commit(owner: str, repo: str, branch: str | None) -> Optional[dict]:
    """Fetch the latest commit metadata for a repository branch."""

    branch_qs = f"&sha={branch}" if branch else ""
    url = f"{API_BASE}/repos/{owner}/{repo}/commits?per_page=1{branch_qs}"
    response = github_request(url)
    if not response:
        return None
    commit = response[0] if isinstance(response, list) else None
    if not commit:
        return None
    commit_data = commit.get("commit", {})
    return {
        "sha": commit.get("sha"),
        "message": commit_data.get("message"),
        "date": commit_data.get("author", {}).get("date"),
        "tree_sha": commit_data.get("tree", {}).get("sha"),
        "html_url": commit.get("html_url"),
    }


def fetch_tree_paths(owner: str, repo: str, tree_sha: str | None) -> List[str]:
    """Return all file paths for a repository tree revision."""

    if not tree_sha:
        return []
    url = f"{API_BASE}/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1"
    response = github_request(url)
    if not response or not isinstance(response, dict):
        return []
    tree = response.get("tree", [])
    paths: List[str] = []
    for entry in tree:
        path = entry.get("path")
        if path:
            paths.append(path)
    return paths


def compute_structural_diff(previous: Iterable[str], current: Iterable[str]) -> Tuple[List[str], List[str]]:
    """Compare repository trees and return added/removed file paths."""

    previous_set = set(previous or [])
    current_set = set(current or [])
    added = sorted(current_set - previous_set)
    removed = sorted(previous_set - current_set)
    return added, removed


def load_timeline_snapshot(path: Path) -> Dict[str, dict]:
    """Load the previous AVOT-Archivist snapshot for diffing."""

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload.get("snapshot", {}) if isinstance(payload, dict) else {}


def save_timeline(
    path: Path, org: str, generated_at: str, entries: List[dict], snapshot: Dict[str, dict]
) -> None:
    """Persist AVOT-Archivist lineage and the new snapshot state."""

    payload = {
        "generated_at": generated_at,
        "org": org,
        "repositories": entries,
        "snapshot": snapshot,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def format_repo_section(
    repo: dict, readme: str, workflows: List[str], commit_info: Optional[dict], added: List[str], removed: List[str]
) -> str:
    """Build the Living Codex section for a repository."""

    headings = extract_headings(readme)
    keyword_candidates = [repo.get("description") or "", " ".join(headings), repo.get("language") or ""]
    keyword_candidates.extend(repo.get("topics", []))
    concepts = derive_keywords(keyword_candidates, limit=8)

    architecture_signals = [h for h in headings if any(term in h.lower() for term in ("architecture", "pattern", "design"))]
    workflows_section = "\n".join(f"      - {name}" for name in workflows) if workflows else "      - None detected"

    lineage = f"Origin: {repo.get('created_at', 'unknown')}; Last pulse: {repo.get('pushed_at', 'unknown')}"

    commit_label = "unresolved" if not commit_info else f"{commit_info.get('sha', '')[:7]} @ {commit_info.get('date', 'n/a')}"
    commit_msg = commit_info.get("message") if commit_info else "Unknown"
    added_list = "\n".join(f"      - {path}" for path in added[:8]) if added else "      - None"
    removed_list = "\n".join(f"      - {path}" for path in removed[:8]) if removed else "      - None"

    return textwrap.dedent(
        f"""
        ## {repo.get('name', 'Unnamed Repository')}
        - **Description**: {repo.get('description') or 'No description provided.'}
        - **Concepts & Patterns**: {', '.join(concepts) if concepts else 'No dominant signals detected.'}
        - **Architectures & Lineage**: {', '.join(architecture_signals) if architecture_signals else 'Implicit or undocumented.'}
        - **Scrolls (Headings)**:
    {textwrap.indent('- ' + '\n- '.join(headings) if headings else '- None captured', '    ')}
        - **Workflows & Rituals**:
    {textwrap.indent(workflows_section, '    ')}
        - **Design Lineage**: {lineage}
        - **Latest Commit**: {commit_label}
        - **Commit Message**: {commit_msg}
        - **Structural Drift**:
          - Added:
    {textwrap.indent(added_list, '    ')}
          - Removed:
    {textwrap.indent(removed_list, '    ')}
        """
    ).strip()


def render_timeline_section(entries: List[dict], generated_at: str) -> str:
    """Render the AVOT-Archivist lineage timeline for the Living Codex."""

    lines = ["## AVOT-Archivist Timeline", f"- **Generated**: {generated_at}", f"- **Repositories Scanned**: {len(entries)}", "- **Lineage Updates**:"]
    if not entries:
        lines.append("  - None captured.")
        return "\n".join(lines)

    for entry in entries:
        repo = entry.get("name", "unknown")
        commit = entry.get("latest_commit", {})
        commit_line = f"{commit.get('sha', '')[:7]} @ {commit.get('date', 'n/a')}" if commit else "unresolved"
        status = "new commit" if entry.get("new_commit") else "no change"
        lines.append(f"  - **{repo}** → {status} ({commit_line})")
        if commit and commit.get("message"):
            lines.append(f"    - commit: {commit.get('message')}")
        added = entry.get("added_files") or []
        removed = entry.get("removed_files") or []
        added_str = ", ".join(added[:5]) if added else "none"
        removed_str = ", ".join(removed[:5]) if removed else "none"
        lines.append(f"    - structural: +{len(added)} / -{len(removed)} (added: {added_str}; removed: {removed_str})")
    return "\n".join(lines)


def inject_section(content: str, section: str, heading: str) -> str:
    """Replace or append a section headed by ``heading``."""

    lines = content.splitlines()
    filtered: List[str] = []
    skip = False
    for line in lines:
        if line.startswith(heading):
            skip = True
        if skip and line.startswith("## ") and not line.startswith(heading):
            skip = False
        if not skip:
            filtered.append(line)
    if filtered and filtered[-1].strip():
        filtered.append("")
    filtered.append(section.strip())
    filtered.append("")
    return "\n".join(filtered)


def extract_section(content: str, heading: str) -> str:
    """Extract an existing section under a given heading."""

    lines = content.splitlines()
    captured: List[str] = []
    recording = False
    for line in lines:
        if line.startswith(heading):
            recording = True
        elif recording and line.startswith("## "):
            break
        if recording:
            captured.append(line)
    return "\n".join(captured).strip()


def build_kernel(org: str, limit: Optional[int], output: Path, timeline_path: Path) -> Path:
    """Execute the assimilation pass and write the Living Codex Kernel."""

    repositories = fetch_repositories(org, limit=limit)
    previous_snapshot = load_timeline_snapshot(timeline_path)

    sections: List[str] = []
    timeline_entries: List[dict] = []
    new_snapshot: Dict[str, dict] = {}

    for repo in repositories:
        name = repo.get("name")
        if not name:
            continue
        readme = fetch_readme(org, name)
        workflows = fetch_workflows(org, name)
        commit_info = fetch_latest_commit(org, name, repo.get("default_branch"))
        tree_paths = fetch_tree_paths(org, name, commit_info.get("tree_sha") if commit_info else None)

        previous = previous_snapshot.get(name, {})
        added, removed = compute_structural_diff(previous.get("tree_paths", []), tree_paths)
        sections.append(format_repo_section(repo, readme, workflows, commit_info, added, removed))

        latest_sha = commit_info.get("sha") if commit_info else None
        new_snapshot[name] = {"commit": latest_sha, "tree_paths": tree_paths}
        timeline_entries.append(
            {
                "name": name,
                "latest_commit": commit_info,
                "new_commit": bool(latest_sha and latest_sha != previous.get("commit")),
                "added_files": added,
                "removed_files": removed,
            }
        )

    timestamp = datetime.now(UTC).isoformat(timespec="seconds")
    header = textwrap.dedent(
        f"""
        # Living Codex Kernel
        *Assimilation Engine pass for `{org}`*

        - **Generated**: {timestamp}
        - **Repositories scanned**: {len(repositories)}
        - **Token**: {'provided' if os.getenv('GITHUB_TOKEN') else 'anonymous (higher rate limits with GITHUB_TOKEN)'}

        The kernel captures surface semantics from Sovereign repositories: descriptions, topics, scroll headings,
        and workflow rituals. Extend this pass with deeper synthesis or recursive refinement as needed.
        """
    ).strip()

    timeline_section = render_timeline_section(timeline_entries, timestamp)
    codex_body = header + "\n\n" + timeline_section + "\n\n" + "\n\n".join(sections if sections else ["No repositories discovered."])

    existing = output.read_text(encoding="utf-8") if output.exists() else ""
    preserved_curious = extract_section(existing, heading="## Curious Agent Lineage")
    if preserved_curious:
        codex_body = inject_section(codex_body, preserved_curious, heading="## Curious Agent Lineage")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(codex_body + "\n", encoding="utf-8")

    save_timeline(timeline_path, org, timestamp, timeline_entries, new_snapshot)

    print(f"[OK] Living Codex Kernel written to {output}")
    print(f"[OK] AVOT-Archivist timeline written to {timeline_path}")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assimilate Sovereign repositories into the Living Codex Kernel.")
    parser.add_argument("--org", default=DEFAULT_ORG, help="GitHub organization to scan (default: sovereign-codex)")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of repositories to scan (useful for quick passes)",
    )
    parser.add_argument(
        "--output",
        default="chronicle/living_codex_kernel.md",
        type=Path,
        help="Output path for the Living Codex Kernel",
    )
    parser.add_argument(
        "--timeline",
        default=TIMELINE_OUTPUT,
        type=Path,
        help="Path to write the AVOT-Archivist timeline lineage",
    )
    return parser.parse_args()


def main() -> None:  # pragma: no cover - CLI entry point
    args = parse_args()
    build_kernel(org=args.org, limit=args.limit, output=args.output, timeline_path=args.timeline)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
