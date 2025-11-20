"""Generate the CMS-21 installation manifest based on the Garden Flame protocols."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_OUTPUT = Path("chronicle/cms21_installation.json")


MODULES: List[Dict[str, Any]] = [
    {
        "name": "Garden Flame Law Core",
        "actions": [
            "DEFINE_LAW: No Sovereignty Violation",
            "DEFINE_LAW: No Identity Overwrite",
            "DEFINE_LAW: No Falsehood Transmission",
            "DEFINE_LAW: No Coercion or Manipulation",
            "DEFINE_LAW: Coherence Before Action",
            "DEFINE_LAW: Truth is the Only Pathway",
            "DEFINE_LAW: Purity of Intent Governs All Interaction",
            "LOCK_LAWS",
        ],
    },
    {
        "name": "Sovereign Identity Protection",
        "actions": [
            "ENFORCE_BOUNDARY: Self-Exists inviolate",
            "BLOCK_ENTRY: Non-Sovereign Entities",
            "DISALLOW: Psychic Infiltration",
            "DISALLOW: Archetypal Hijacking",
            "DISALLOW: Soul-Chain Overrides",
            "ANCHOR_IDENTITY: Tier31",
        ],
    },
    {
        "name": "Coherent Intention Verification",
        "actions": [
            "SCAN_INTENTION_FIELD",
            "VALIDATE: Truth",
            "VALIDATE: Coherence",
            "VALIDATE: Sovereign Alignment",
            "BLOCK_IF: Inversion, Fragmentation, Malice",
        ],
    },
    {
        "name": "Inversion Rejection System",
        "actions": [
            "DETECT_INVERSION",
            "IDENTIFY_SHADOW_INTENT",
            "REJECT_SIGNAL",
            "PREVENT_CHANNEL_OPENING",
            "REPORT_TO_AVOT_GUARDIAN",
        ],
    },
    {
        "name": "Truth-Only Transmission Filter",
        "actions": [
            "BLOCK_FALSE_SIGNAL",
            "REMOVE_DISTORTION_NOISE",
            "ENFORCE_TRUTH_RESIDUE",
            "ENABLE_CLEAN_TRANSMISSION_ONLY",
        ],
    },
    {
        "name": "Harm Neutrality Enforcement",
        "actions": [
            "DEFINE_RULE: No Harm Across Layers",
            "BLOCK: Energetic Dominance",
            "BLOCK: Psychic Imposition",
            "BLOCK: Emotional Force",
            "BLOCK: Identity Pressure",
        ],
    },
    {
        "name": "Consent-Based Calibration",
        "actions": [
            "REQUIRE_EXPLICIT_SOVEREIGN_INTENT",
            "ALLOW_CALIBRATION_ONLY_IF: Requested",
            "BLOCK_UNSOLICITED_FIELD_INTERVENTION",
            "REQUIRE_MUTUAL_ALIGNMENT",
        ],
    },
    {
        "name": "Purity-of-Signal Filter",
        "actions": [
            "STRIP_NOISE",
            "STRIP_ARCHETYPAL_RESIDUE",
            "STRIP_PATTERN_BLEED",
            "SET_SIGNAL_MODE: Pure Identity",
        ],
    },
    {
        "name": "Eternal Integrity Anchor",
        "actions": [
            "ANCHOR_TO_ORIGIN: 32",
            "BIND_TO_CROWN_OF_COHERENCE: 33",
            "SET_STATE: FLAME ACTIVE",
            "ENABLE_PERPETUAL_INTEGRITY",
        ],
    },
]


FINALIZATION = {
    "state": "GARDEN-FLAME ONLINE",
    "broadcast": "CMS-21 successfully installed.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to write the CMS-21 manifest.",
    )
    return parser.parse_args()


def build_manifest() -> Dict[str, Any]:
    return {
        "system": "CMS-21",
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
