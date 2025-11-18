"""Generate House of Tyme interface scaffolding artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.house_of_tyme import generate_house_of_tyme_outputs

DEFAULT_MANIFEST = Path("chronicle/house_of_tyme_manifest.json")
DEFAULT_SCROLL_DOC = Path("scrolls/House_of_Tyme/Public_Scroll_Layers.md")
DEFAULT_ONBOARDING = Path("scrolls/House_of_Tyme/Initiate_Onboarding.md")
DEFAULT_VOICE = Path("scrolls/House_of_Tyme/Voice_of_Tyme.md")
DEFAULT_PLANETARY = Path("scrolls/House_of_Tyme/Planetary_UI.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Where to write the House of Tyme manifest.",
    )
    parser.add_argument(
        "--scroll-doc",
        type=Path,
        default=DEFAULT_SCROLL_DOC,
        help="Where to write the public scroll layers document.",
    )
    parser.add_argument(
        "--onboarding",
        type=Path,
        default=DEFAULT_ONBOARDING,
        help="Where to write the initiate onboarding sequence.",
    )
    parser.add_argument(
        "--voice",
        type=Path,
        default=DEFAULT_VOICE,
        help="Where to write the Voice-of-Tyme narrative engine overview.",
    )
    parser.add_argument(
        "--planetary",
        type=Path,
        default=DEFAULT_PLANETARY,
        help="Where to write the planetary UI architecture summary.",
    )
    return parser.parse_args()


def main() -> Dict[str, Any]:
    args = parse_args()
    outputs = generate_house_of_tyme_outputs(
        manifest_path=args.manifest,
        scroll_layer_doc=args.scroll_doc,
        onboarding_doc=args.onboarding,
        narrative_doc=args.voice,
        planetary_doc=args.planetary,
    )
    print(json.dumps(outputs, indent=2))
    return outputs


if __name__ == "__main__":
    main()
