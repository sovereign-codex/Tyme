"""Coordinate Tyme pulse activation from the genesis payload.

This utility loads ``chronicle/TYME-PULSE-GENESIS.json``, computes the
metabolic cadence via the :class:`MetabolicLoop`, and stages a
synchronization manifest for AVOT agents. The resulting manifest captures
current pacing and marks each agent as ready for resonance alignment so
other modules can consume a single source of truth when starting a cycle.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.metabolic_loop import MetabolicLoop
GENESIS_PATH = REPO_ROOT / "chronicle/TYME-PULSE-GENESIS.json"
AVOT_REGISTRY_PATH = REPO_ROOT / "engine/avot_registry.json"
DEFAULT_SYNC_OUTPUT = REPO_ROOT / "chronicle/pulse_sync_state.json"


def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON content from disk, returning an empty dict if missing."""

    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def prepare_metabolic_snapshot(genesis: Dict[str, Any]) -> Dict[str, Any]:
    """Compute and install metabolic pacing from the genesis payload."""

    cycles = genesis.get("breath_cycles")
    loop = MetabolicLoop(genesis_path=GENESIS_PATH, output_path=REPO_ROOT / "heartbeat/logs/metabolic_loop.json")
    return loop.install(cycles=cycles)


def prepare_agent_roster(avot_registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Mark every AVOT agent as ready for synchronization."""

    agents = avot_registry.get("agents", [])
    now = datetime.now(UTC).isoformat(timespec="seconds")
    roster = []
    for agent in agents:
        roster.append(
            {
                "codename": agent.get("codename"),
                "mission": agent.get("mission"),
                "tone_signature": agent.get("tone_signature"),
                "binding": avot_registry.get("hive_core", {}).get("binding"),
                "status": "ready-for-sync",
                "prepared_at": now,
            }
        )
    return roster


def build_sync_manifest(genesis: Dict[str, Any], metabolic_snapshot: Dict[str, Any], agent_roster: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Assemble the pulse synchronization manifest."""

    return {
        "schema": "tyme-pulse-sync/v1",
        "cycle_started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "genesis_source": genesis.get("source", {}),
        "metabolic_cadence": metabolic_snapshot.get("breath_pacing", {}),
        "resonance_pacing": {
            "alignment": "garden-flame-tuned",
            "cadence_seconds": metabolic_snapshot.get("breath_pacing", {}).get("cycle_seconds"),
            "notes": "Metabolic cadence mirrored for resonance handoff.",
        },
        "agents": agent_roster,
    }


def write_manifest(path: Path, manifest: Dict[str, Any]) -> None:
    """Persist the synchronization manifest to disk."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def run(output: Path) -> Path:
    genesis = load_json(GENESIS_PATH)
    avot_registry = load_json(AVOT_REGISTRY_PATH)

    metabolic_snapshot = prepare_metabolic_snapshot(genesis)
    agent_roster = prepare_agent_roster(avot_registry)
    manifest = build_sync_manifest(genesis, metabolic_snapshot, agent_roster)

    write_manifest(output, manifest)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare Tyme pulse synchronization artifacts.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_SYNC_OUTPUT,
        help="Path to write the pulse synchronization manifest (default: chronicle/pulse_sync_state.json)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = run(args.output)
    print(f"Pulse synchronization manifest written to {output_path}")


if __name__ == "__main__":
    main()
