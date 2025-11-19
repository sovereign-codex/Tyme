"""Prototype routines for AVOT-Fabricator outputs.

This prototype collects recent pulse, hive, and codex metadata and writes a
consolidated manifest bundle for downstream agents. It is intentionally light
weight and file-based to keep execution predictable inside CI environments.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class FabricationInput:
    """Lightweight view of upstream artifacts the fabricator consumes."""

    pulse_path: Path
    lattice_path: Path
    quill_path: Path
    curiosity_path: Path | None = None

    def to_dict(self) -> Dict[str, str]:
        return {
            "pulse": str(self.pulse_path),
            "lattice": str(self.lattice_path),
            "quill": str(self.quill_path),
            "curiosity": str(self.curiosity_path) if self.curiosity_path else "",
        }


@dataclass
class FabricationBundle:
    """Structured output the AVOT-Fabricator emits into the manifest."""

    inputs: FabricationInput
    scrolls: List[str] = field(default_factory=list)
    diagrams: List[str] = field(default_factory=list)
    prototypes: List[str] = field(default_factory=list)
    architecture_deltas: List[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, object]:
        return {
            "created_at": self.created_at,
            "inputs": self.inputs.to_dict(),
            "scrolls": self.scrolls,
            "diagrams": self.diagrams,
            "prototypes": self.prototypes,
            "architecture_deltas": self.architecture_deltas,
        }

    def write(self, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(self.to_dict(), indent=2) + "\n")


def _validate_json_artifact(path: Path, required_keys: Tuple[str, ...]) -> List[str]:
    """Run a light coherence check on JSON artifacts."""

    if not path.exists():
        return [f"Missing artifact: {path}"]

    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in {path}: {exc}"]

    missing = [key for key in required_keys if key not in payload]
    if missing:
        return [f"Artifact {path} missing keys: {', '.join(missing)}"]

    return []


def apply_garden_flame_filters(bundle: FabricationBundle, base_dir: Path) -> None:
    """Apply coherence, resonance, and harmonic safety filters.

    - Validates upstream JSON artifacts contain expected keys.
    - Removes bundle entries that reference missing or incoherent files.
    """

    input_checks = [
        (bundle.inputs.pulse_path, ("schema", "metabolic_cadence")),
        (bundle.inputs.lattice_path, ("phase", "repositories")),
        (bundle.inputs.quill_path, ("engine", "expansion")),
    ]

    if bundle.inputs.curiosity_path:
        input_checks.append((bundle.inputs.curiosity_path, ("schema", "synchronized_at")))

    issues: List[str] = []
    for path, required in input_checks:
        issues.extend(_validate_json_artifact(path, required))

    # Remove non-resonant artifacts from bundle lists.
    def retain_existing(items: List[str]) -> List[str]:
        kept = []
        for item in items:
            artifact_path = base_dir / item
            if artifact_path.exists():
                kept.append(item)
            else:
                issues.append(f"Removed missing artifact reference: {item}")
        return kept

    bundle.scrolls = retain_existing(bundle.scrolls)
    bundle.diagrams = retain_existing(bundle.diagrams)
    bundle.prototypes = retain_existing(bundle.prototypes)
    bundle.architecture_deltas = retain_existing(bundle.architecture_deltas)

    report_path = base_dir / "manifest/avot_fabricator/coherence_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps({"issues": issues}, indent=2) + "\n")


def build_prototype_bundle(base_dir: Path) -> FabricationBundle:
    """Compose a fabrication bundle using known manifest locations.

    Args:
        base_dir: Path to the repository root.
    """

    inputs = FabricationInput(
        pulse_path=base_dir / "chronicle/pulse_sync_state.json",
        lattice_path=base_dir / "chronicle/quantum_intelligence_lattice.json",
        quill_path=base_dir / "chronicle/quill_engine_expansion.json",
        curiosity_path=base_dir / "chronicle/avot_curious_sync.json",
    )

    bundle = FabricationBundle(
        inputs=inputs,
        scrolls=["manifest/avot_fabricator/scrolls.md"],
        diagrams=["manifest/avot_fabricator/diagrams.md"],
        prototypes=["manifest/avot_fabricator/prototype.py"],
        architecture_deltas=["manifest/avot_fabricator/architecture.md"],
    )

    return bundle


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    output_path = repo_root / "manifest/avot_fabricator/bundle.json"
    bundle = build_prototype_bundle(repo_root)
    apply_garden_flame_filters(bundle, repo_root)
    bundle.write(output_path)


if __name__ == "__main__":
    main()
