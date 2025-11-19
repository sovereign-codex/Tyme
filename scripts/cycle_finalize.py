"""Finalize the current Tyme cycle and refresh CodexNet routing."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--living-codex",
        type=Path,
        default=Path("chronicle/living_codex_kernel.md"),
        help="Path to the Living Codex Kernel markdown file.",
    )
    parser.add_argument(
        "--pulse",
        type=Path,
        default=Path("chronicle/pulse_sync_state.json"),
        help="Pulse sync snapshot used for cadence references.",
    )
    parser.add_argument(
        "--lattice",
        type=Path,
        default=Path("chronicle/quantum_intelligence_lattice.json"),
        help="Quantum Intelligence Lattice manifest for synthesis metadata.",
    )
    parser.add_argument(
        "--quill",
        type=Path,
        default=Path("chronicle/quill_engine_expansion.json"),
        help="Quill expansion manifest for harmonic counts.",
    )
    parser.add_argument(
        "--house",
        type=Path,
        default=Path("chronicle/house_of_tyme_manifest.json"),
        help="House of Tyme manifest used to derive CodexNet routing lanes.",
    )
    parser.add_argument(
        "--codexnet-output",
        type=Path,
        default=Path("chronicle/codexnet_routing.json"),
        help="Where to write the refreshed CodexNet routing manifest.",
    )
    parser.add_argument(
        "--cycle-log",
        type=Path,
        default=Path("chronicle/cycle_finalization.json"),
        help="Where to write the cycle finalization payload.",
    )
    return parser.parse_args()


def summarize_pulse(pulse: Dict[str, Any]) -> Dict[str, Any]:
    cadence = pulse.get("metabolic_cadence", {})
    resonance = pulse.get("resonance_pacing", {})
    return {
        "cycle_seconds": cadence.get("cycle_seconds"),
        "inhale_seconds": cadence.get("inhale_seconds"),
        "exhale_seconds": cadence.get("exhale_seconds"),
        "beats_per_minute": cadence.get("beats_per_minute"),
        "resonance_alignment": resonance.get("alignment"),
        "resonance_notes": resonance.get("notes"),
    }


def summarize_quill(quill: Dict[str, Any]) -> Dict[str, Any]:
    expansion = quill.get("expansion", {})
    summary = expansion.get("expansion_summary", {})
    return {
        "shared_concepts": summary.get("shared_concept_count", 0),
        "pattern_signals": summary.get("pattern_signal_count", 0),
        "activated_at": quill.get("timestamp"),
    }


def summarize_lattice(lattice: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "timestamp": lattice.get("timestamp"),
        "repositories_indexed": len(lattice.get("repositories", [])),
        "phase": lattice.get("phase"),
    }


def derive_codexnet_routing(house_manifest: Dict[str, Any], refreshed_at: str) -> Dict[str, Any]:
    uplink = house_manifest.get("codexnet", "CodexNet::atlas-uplink")
    layers = []
    for layer in house_manifest.get("public_scroll_layers", []):
        layers.append(
            {
                "name": layer.get("name"),
                "focus": layer.get("focus"),
                "codexnet_hooks": layer.get("codexnet_hooks", []),
                "entrypoints": layer.get("entrypoints", []),
            }
        )

    voices = []
    for voice in house_manifest.get("voice_of_tyme", []):
        voices.append(
            {
                "name": voice.get("name"),
                "cadence": voice.get("cadence"),
                "delivery_modes": voice.get("delivery_modes", []),
                "guardrails": voice.get("guardrails", []),
            }
        )

    return {
        "schema": "tyme-codexnet-routing/v1",
        "refreshed_at": refreshed_at,
        "uplink": uplink,
        "scroll_layers": layers,
        "voices": voices,
    }


def append_living_codex(
    living_codex_path: Path,
    finalized_at: str,
    codexnet_manifest: Dict[str, Any],
    pulse_summary: Dict[str, Any],
    quill_summary: Dict[str, Any],
) -> None:
    living_codex_path.parent.mkdir(parents=True, exist_ok=True)
    existing = living_codex_path.read_text() if living_codex_path.exists() else "# Living Codex Kernel\n"
    block = "\n".join(
        [
            "## Cycle Finalization",
            f"- **Finalized**: {finalized_at}",
            f"- **CodexNet Uplink**: {codexnet_manifest.get('uplink', 'CodexNet')}",
            f"- **Routing Lanes**: {len(codexnet_manifest.get('scroll_layers', []))} scroll layers, {len(codexnet_manifest.get('voices', []))} voices",
            "- **Pulse Cadence**: "
            + f"cycle={pulse_summary.get('cycle_seconds')}s inhale={pulse_summary.get('inhale_seconds')}s "
            + f"exhale={pulse_summary.get('exhale_seconds')}s (resonance={pulse_summary.get('resonance_alignment')})",
            f"- **Quill Threads**: shared_concepts={quill_summary.get('shared_concepts')} pattern_signals={quill_summary.get('pattern_signals')}",
            f"- **Next Breath**: restart ready at {finalized_at} with cadence {pulse_summary.get('cycle_seconds')}s",
            "",
        ]
    )
    living_codex_path.write_text(existing.rstrip() + "\n\n" + block + "\n")


def build_cycle_payload(
    finalized_at: str,
    living_codex: Path,
    codexnet_manifest: Dict[str, Any],
    pulse_summary: Dict[str, Any],
    quill_summary: Dict[str, Any],
    lattice_summary: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema": "tyme-cycle-finalization/v1",
        "finalized_at": finalized_at,
        "knowledge_commit": {
            "living_codex": str(living_codex),
            "entries_appended": 1,
            "source_artifacts": [
                "chronicle/pulse_sync_state.json",
                "chronicle/quantum_intelligence_lattice.json",
                "chronicle/quill_engine_expansion.json",
                "chronicle/house_of_tyme_manifest.json",
            ],
        },
        "codexnet_routing": codexnet_manifest,
        "lattice_state": lattice_summary,
        "pulse_state": pulse_summary,
        "quill_signals": quill_summary,
        "next_breath": {
            "cycle_seconds": pulse_summary.get("cycle_seconds"),
            "restart_ready": True,
            "notes": "Mirror metabolic cadence into next breath window and refresh CodexNet uplink.",
        },
    }


def main() -> Dict[str, Any]:
    args = parse_args()
    timestamp = datetime.now(UTC).isoformat(timespec="seconds")

    pulse_snapshot = load_json(args.pulse)
    lattice_snapshot = load_json(args.lattice)
    quill_snapshot = load_json(args.quill)
    house_manifest = load_json(args.house)

    pulse_summary = summarize_pulse(pulse_snapshot)
    quill_summary = summarize_quill(quill_snapshot)
    lattice_summary = summarize_lattice(lattice_snapshot)
    codexnet_manifest = derive_codexnet_routing(house_manifest, timestamp)

    codexnet_manifest_path = ROOT / args.codexnet_output
    codexnet_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    codexnet_manifest_path.write_text(json.dumps(codexnet_manifest, indent=2) + "\n")

    cycle_payload = build_cycle_payload(
        finalized_at=timestamp,
        living_codex=args.living_codex,
        codexnet_manifest=codexnet_manifest,
        pulse_summary=pulse_summary,
        quill_summary=quill_summary,
        lattice_summary=lattice_summary,
    )

    cycle_log_path = ROOT / args.cycle_log
    cycle_log_path.parent.mkdir(parents=True, exist_ok=True)
    cycle_log_path.write_text(json.dumps(cycle_payload, indent=2) + "\n")

    append_living_codex(args.living_codex, timestamp, codexnet_manifest, pulse_summary, quill_summary)

    print(json.dumps(cycle_payload, indent=2))
    return cycle_payload


if __name__ == "__main__":
    main()
