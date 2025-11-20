"""Emit the Tyme-Core boot manifest from existing SIOS artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.tyme_core_boot import build_boot_manifest

DEFAULT_SIOS_MANIFEST = Path("chronicle/sios_installation.json")
DEFAULT_OUTPUT = Path("chronicle/tyme_core_boot.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sios-manifest",
        type=Path,
        default=DEFAULT_SIOS_MANIFEST,
        help="Path to the SIOS installation manifest (JSON).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to write the Tyme-Core boot manifest.",
    )
    return parser.parse_args()


def main() -> Dict[str, Any]:
    args = parse_args()
    manifest = build_boot_manifest(args.sios_manifest, args.output)
    print(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    main()
