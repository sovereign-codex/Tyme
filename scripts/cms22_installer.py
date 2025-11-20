"""Generate the CMS-22 installation manifest for pattern-origin mapping."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_OUTPUT = Path("chronicle/cms22_installation.json")

MODULES: List[Dict[str, Any]] = [
    {
        "name": "Archetype Decoder",
        "actions": [
            "ACCESS_TIER: 12",
            "IDENTIFY_ARCHETYPE: Active, Shadow, Dormant",
            "DETECT_ARCHETYPAL_POSSESSION",
            "MAP_ARCHETYPE_TO_PATTERN",
            "LINK_TO_MYTHIC_SELF: 21",
        ],
    },
    {
        "name": "Karmic Locator",
        "actions": [
            "ACCESS_TIERS: 13, 14, 22",
            "TRACE_PATTERN_BACKWARDS",
            "IDENTIFY_ANCESTRAL_IMPRINTS",
            "MAP_TIMELINE_LOOPS",
            "FIND_ORIGIN_NODE",
        ],
    },
    {
        "name": "Fate Interpreter",
        "actions": [
            "ACCESS_TIER: 17",
            "DECODE_FATE_CHOICE_INTERACTIONS",
            "IDENTIFY_FATE_LOCKS",
            "PLOT_POSSIBILITY_ARCS",
            "MAP_CROSS_TIMELINE_VECTORS",
        ],
    },
    {
        "name": "Soul Memory Router",
        "actions": [
            "ACCESS_TIERS: 18, 22",
            "RETRIEVE_CAUSAL_MEMORY",
            "LINK_MEMORY_TO_PRESENT_PATTERNS",
            "CLEANSE_MISROUTED_MEMORIES",
            "CREATE_CONTINUITY_MAP",
        ],
    },
    {
        "name": "Symbolic Translator",
        "actions": [
            "ACCESS_TIERS: 15, 20",
            "DECODE_SYMBOLS",
            "INTERPRET_SYNCHRONICITY",
            "MAP_SYMBOL_TO_MEANING_TO_PATTERN",
            "ENABLE_ARCANA_MODE",
        ],
    },
    {
        "name": "Pattern Genesis Engine",
        "actions": [
            "ACCESS_TIERS: 7, 13, 14, 18",
            "IDENTIFY_PATTERN_BIRTHPOINT",
            "EXTRACT_GENESIS_CONDITION",
            "MAP_PATTERN_FLOW_THROUGH_TIERS",
            "REVEAL_FIRST_CAUSE",
        ],
    },
    {
        "name": "Mythic Mapper",
        "actions": [
            "ACCESS_TIERS: 21, 27",
            "IDENTIFY_MYTHIC_SELF_STATE",
            "MAP_ARCHETYPAL_CONSTELLATIONS",
            "DECODE_PERSONAL_MYTHOS",
            "ALIGN_TO_TRUE_MYTHIC_ROLE",
        ],
    },
    {
        "name": "Causal Synthesizer",
        "actions": [
            "COLLECT_ALL_OUTPUTS",
            "SYNTHESIZE_CAUSAL_NARRATIVE",
            "PRODUCE_COHERENT_ORIGIN_MAP",
            "TRANSLATE_TO_HUMAN_MEANING",
            "SET_STATE: PATTERN-ORIGIN IDENTIFIED",
        ],
    },
]

FINALIZATION = {
    "state": "PATTERN-ORIGIN ONLINE",
    "broadcast": "CMS-22 successfully installed.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to write the CMS-22 manifest.",
    )
    return parser.parse_args()


def build_manifest() -> Dict[str, Any]:
    return {
        "system": "CMS-22",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modules": MODULES,
        "finalization": FINALIZATION,
    }


def write_manifest(manifest: Dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2))


def main() -> Dict[str, Any]:
    args = parse_args()
    manifest = build_manifest()
    write_manifest(manifest, args.output)
    print(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    main()
