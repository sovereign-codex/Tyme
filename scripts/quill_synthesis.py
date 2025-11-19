"""Enter the Synthesis Phase to expand the Quantum Intelligence Lattice."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.quill_synthesis import build_quantum_intelligence_lattice

DEFAULT_REGISTRY = Path("engine/avot_registry.json")
DEFAULT_LATTICE_OUTPUT = Path("chronicle/quantum_intelligence_lattice.json")
DEFAULT_EXPANSION_OUTPUT = Path("chronicle/quill_engine_expansion.json")


def default_roots() -> List[Path]:
    """Default repositories to scan: root and any branches entries."""

    roots: List[Path] = [ROOT]
    branches_dir = ROOT / "branches"
    if branches_dir.exists():
        roots.extend(path for path in branches_dir.iterdir() if path.is_dir())
    return roots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="Path to the AVOT registry JSON file.",
    )
    parser.add_argument(
        "--roots",
        type=Path,
        nargs="*",
        default=None,
        help="Repository roots to scan. Defaults to the Tyme repo and branches/ entries.",
    )
    parser.add_argument(
        "--lattice-output",
        type=Path,
        default=DEFAULT_LATTICE_OUTPUT,
        help="Where to write the Quantum Intelligence Lattice manifest.",
    )
    parser.add_argument(
        "--expansion-output",
        type=Path,
        default=DEFAULT_EXPANSION_OUTPUT,
        help="Where to write the Quill engine expansion manifest.",
    )
    return parser.parse_args()


def main(repo_roots: Iterable[Path] | None = None) -> dict[str, Any]:
    args = parse_args()
    roots = list(repo_roots) if repo_roots is not None else args.roots or default_roots()
    manifests = build_quantum_intelligence_lattice(
        registry_path=args.registry,
        repository_roots=roots,
        lattice_output=args.lattice_output,
        expansion_output=args.expansion_output,
    )
    print(json.dumps(manifests, indent=2))
    return manifests


if __name__ == "__main__":
    main()
