"""Activate AVOT agents and synchronize them with the Tyme-Core hive."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.avot_engine import build_hive_sync


DEFAULT_REGISTRY = Path("engine/avot_registry.json")
DEFAULT_OUTPUT = Path("chronicle/hive_core_sync.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to the AVOT registry JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to write the Hive-Core synchronization manifest.",
    )
    return parser.parse_args()


def main() -> Dict[str, Any]:
    args = parse_args()
    manifest = build_hive_sync(args.registry, args.output)
    print(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    main()
