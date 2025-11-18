"""Install the Garden Flame Kodex as the primary ethical layer for Tyme."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.avot_engine import load_registry
from engine.garden_flame_kodex import GardenFlameKodex

DEFAULT_REGISTRY = Path("engine/avot_registry.json")
DEFAULT_OUTPUT = Path("chronicle/garden_flame_kodex.json")

DEFAULT_REASONING_LOOPS = [
    "Assimilation Engine",
    "Breath Engine Loop",
    "AVOT Hive-Core Synchronization",
    "Crownflow Engine",
]
DEFAULT_SYSTEM_ACTIONS = [
    "Manifest generation",
    "Artifact emission",
    "Workflow orchestration",
    "Prototype deployment",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to the AVOT registry JSON file for deriving agent outputs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to write the Garden Flame Kodex manifest.",
    )
    parser.add_argument(
        "--reasoning-loop",
        action="append",
        dest="reasoning_loops",
        help="Optional additional reasoning loop to bind (can be repeated).",
    )
    parser.add_argument(
        "--system-action",
        action="append",
        dest="system_actions",
        help="Optional additional system action to guard (can be repeated).",
    )
    return parser.parse_args()


def _collect_agent_outputs(registry_path: Path) -> List[str]:
    registry = load_registry(registry_path)
    return [agent.codename for agent in registry.get("agents", [])]


def main() -> Dict[str, Any]:
    args = parse_args()

    reasoning_loops = DEFAULT_REASONING_LOOPS.copy()
    if args.reasoning_loops:
        reasoning_loops.extend(args.reasoning_loops)

    system_actions = DEFAULT_SYSTEM_ACTIONS.copy()
    if args.system_actions:
        system_actions.extend(args.system_actions)

    agent_outputs = _collect_agent_outputs(args.registry)

    kodex = GardenFlameKodex()
    manifest = kodex.activate_layer(
        reasoning_loops=reasoning_loops,
        agent_outputs=agent_outputs,
        system_actions=system_actions,
        output_path=args.output,
    )

    print(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    main()
