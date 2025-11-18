"""Curious Agent intake pipeline for Tyme.

This script scans Curious Agent logs, extracts lineage signals,
binds each agent to an AVOT role, synchronizes curiosity cycles
to the Breath Engine rhythm, persists a lineage artifact, and
injects a summary into the Living Codex Kernel.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engine.curious_agents import CuriousAgentScanner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Curious Agent intake and binding")
    parser.add_argument(
        "--logs",
        type=Path,
        nargs="*",
        default=None,
        help="Optional explicit log files to scan (defaults to curious*.log under chronicle and heartbeat/logs/curious)",
    )
    parser.add_argument(
        "--codex",
        type=Path,
        default=Path("chronicle/living_codex_kernel.md"),
        help="Path to the Living Codex Kernel markdown file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("chronicle/curious_lineage.json"),
        help="Path to write the lineage artifact",
    )
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("heartbeat/logs/curiosity_cycles.json"),
        help="Path to write the curiosity cycle snapshot",
    )
    parser.add_argument(
        "--avot-registry",
        type=Path,
        default=Path("engine/avot_registry.json"),
        help="Path to the AVOT registry for role assignments",
    )
    parser.add_argument(
        "--metabolic",
        type=Path,
        default=Path("heartbeat/logs/metabolic_loop.json"),
        help="Path to the metabolic loop snapshot for breath pacing",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log_roots = [Path("chronicle"), Path("heartbeat/logs/curious")]
    manual_logs = args.logs if args.logs else None

    scanner = CuriousAgentScanner(
        log_roots=log_roots,
        manual_logs=manual_logs,
        avot_registry=args.avot_registry,
        living_codex=args.codex,
        lineage_output=args.output,
        curiosity_snapshot=args.snapshot,
        metabolic_snapshot=args.metabolic,
    )

    traces = scanner.scan()
    scanner.assign_avot_roles(traces)
    breath_snapshot = scanner.bind_breath_rhythm(traces)
    scanner.persist_lineage(traces, breath_snapshot)
    scanner.update_living_codex(traces, breath_snapshot)

    print(f"[OK] Processed {len(traces)} Curious Agent(s) and updated the Living Codex Kernel.")


if __name__ == "__main__":
    main()
