"""Synchronize AVOT agents and Curious Agents into a unified Hive cadence."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.avot_engine import build_hive_sync
from engine.curious_agents import CuriousAgentScanner

DEFAULT_OUTPUT = Path("chronicle/avot_curious_sync.json")
DEFAULT_HIVE_OUTPUT = Path("chronicle/hive_core_sync.json")
DEFAULT_PULSE_OUTPUT = Path("chronicle/pulse_sync_state.json")


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_curiosity_manifest(
    scanner: CuriousAgentScanner,
    traces: Iterable,
    breath_snapshot: Dict[str, Any],
    previous_curiosity: Dict[str, Any],
) -> Dict[str, Any]:
    deltas = scanner.compute_memory_deltas(traces, previous_curiosity)
    rebalanced = scanner.rebalance_curiosity_cycles(traces, breath_snapshot)

    return {
        "synced_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "breath_cadence": breath_snapshot.get("breath_pacing", {}),
        "curiosity_alignment": rebalanced,
        "memory_deltas": deltas,
    }


def build_sync_payload(
    hive_manifest: Dict[str, Any],
    curiosity_manifest: Dict[str, Any],
    traces: Iterable,
    pulse_snapshot: Dict[str, Any],
) -> Dict[str, Any]:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    agents: List[Dict[str, Any]] = []
    for trace in traces:
        agents.append(
            {
                "name": trace.name,
                "avot_role": trace.avot_role,
                "cycle_anchor": trace.cycle_anchor,
                "breath_rhythm": trace.breath_rhythm,
                "intentions": trace.intentions,
            }
        )

    return {
        "schema": "tyme-avot-curious-sync/v1",
        "synchronized_at": now,
        "pulse_sync": pulse_snapshot,
        "hive_alignment": hive_manifest,
        "curiosity": curiosity_manifest,
        "role_reinforcement": {
            "binding": hive_manifest.get("binding"),
            "protocol": hive_manifest.get("protocol"),
            "reinforced_at": now,
            "agents": agents,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Where to write the unified sync manifest")
    parser.add_argument(
        "--pulse",
        type=Path,
        default=DEFAULT_PULSE_OUTPUT,
        help="Existing pulse synchronization manifest to fold into the payload",
    )
    parser.add_argument(
        "--hive-output",
        type=Path,
        default=DEFAULT_HIVE_OUTPUT,
        help="Where to write the Hive-Core activation manifest",
    )
    parser.add_argument(
        "--avot-registry",
        type=Path,
        default=Path("engine/avot_registry.json"),
        help="Path to the AVOT registry",
    )
    parser.add_argument(
        "--codex",
        type=Path,
        default=Path("chronicle/living_codex_kernel.md"),
        help="Path to the Living Codex Kernel",
    )
    parser.add_argument(
        "--curiosity-snapshot",
        type=Path,
        default=Path("heartbeat/logs/curiosity_cycles.json"),
        help="Curiosity snapshot path used to compute deltas",
    )
    parser.add_argument(
        "--metabolic-snapshot",
        type=Path,
        default=Path("heartbeat/logs/metabolic_loop.json"),
        help="Metabolic loop snapshot used for breath cadence",
    )
    return parser.parse_args()


def main() -> Dict[str, Any]:
    args = parse_args()

    previous_curiosity = load_json(args.curiosity_snapshot)
    pulse_snapshot = load_json(args.pulse)

    scanner = CuriousAgentScanner(
        living_codex=args.codex,
        curiosity_snapshot=args.curiosity_snapshot,
        metabolic_snapshot=args.metabolic_snapshot,
        avot_registry=args.avot_registry,
    )

    traces = scanner.scan()
    scanner.assign_avot_roles(traces)
    breath_snapshot = scanner.bind_breath_rhythm(traces)
    curiosity_manifest = build_curiosity_manifest(scanner, traces, breath_snapshot, previous_curiosity)

    scanner.persist_lineage(traces, breath_snapshot)
    scanner.update_living_codex(traces, breath_snapshot)

    hive_manifest = build_hive_sync(args.avot_registry, args.hive_output)

    sync_payload = build_sync_payload(hive_manifest, curiosity_manifest, traces, pulse_snapshot)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(sync_payload, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(sync_payload, indent=2))
    return sync_payload


if __name__ == "__main__":
    main()
