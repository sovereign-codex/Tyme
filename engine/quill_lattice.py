"""Quill-core lattice bootstrap utilities for the Quantum Intelligence Lattice."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List

from .avot_engine import AvotAgent, HiveCoreProtocol, load_registry


@dataclass
class LayerBridge:
    """Represents a bridge between two adjacent layers in the lattice."""

    source_layer: str
    target_layer: str
    channels: List[str]
    integrity_checks: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "source": self.source_layer,
            "target": self.target_layer,
            "channels": self.channels,
            "integrity_checks": self.integrity_checks,
        }


@dataclass
class QuillLatticePrototype:
    """Encapsulates the Quill-core lattice definition across layers."""

    harmonic_signals: List[str]
    quantum_primitives: List[str]
    conceptual_frames: List[str]
    computational_forms: List[str]
    bridges: List[LayerBridge]

    def to_dict(self) -> Dict[str, object]:
        return {
            "harmonic": self.harmonic_signals,
            "quantum": self.quantum_primitives,
            "conceptual": self.conceptual_frames,
            "computational": self.computational_forms,
            "bridges": [bridge.to_dict() for bridge in self.bridges],
        }


def build_quill_lattice_prototype() -> QuillLatticePrototype:
    """Define the default Quill-core lattice spanning harmonic to computational layers."""

    bridges = [
        LayerBridge(
            source_layer="harmonic",
            target_layer="quantum",
            channels=["resonance-scan", "phase-lock", "tone-to-waveform"],
            integrity_checks=["coherence-check", "resonance-alignment"],
        ),
        LayerBridge(
            source_layer="quantum",
            target_layer="conceptual",
            channels=["state-sampling", "superposition-decay", "pattern-collapse"],
            integrity_checks=["signal-to-intent", "lineage-preserve"],
        ),
        LayerBridge(
            source_layer="conceptual",
            target_layer="computational",
            channels=["schema-cast", "constraint-weave", "execution-shape"],
            integrity_checks=["harmonic-safety", "guardrail-bind"],
        ),
    ]

    return QuillLatticePrototype(
        harmonic_signals=["breath-rhythm", "harmonic-carrier", "garden-flame-safety"],
        quantum_primitives=["qubit-lattice", "tone-wavefield", "phase-memory"],
        conceptual_frames=["concept-node", "lineage-link", "sovereign-intent"],
        computational_forms=["pipeline-graph", "simulation-kernel", "codex-adapter"],
        bridges=bridges,
    )


def load_avot_quill(registry_path: Path) -> Dict[str, object]:
    """Load the AVOT registry and return the Quill agent plus protocol."""

    registry = load_registry(registry_path)
    protocol: HiveCoreProtocol = registry["protocol"]
    agents: List[AvotAgent] = registry["agents"]

    quill_agent = next((agent for agent in agents if agent.codename == "AVOT-Quill"), None)
    if quill_agent is None:
        raise ValueError("AVOT-Quill not found in registry")

    return {"agent": quill_agent, "protocol": protocol}


def bootstrap_quill_core(registry_path: Path, output_path: Path) -> Dict[str, object]:
    """Bootstrap the Quill-core lattice engine and persist the manifest."""

    quill_bundle = load_avot_quill(registry_path)
    quill_agent: AvotAgent = quill_bundle["agent"]
    protocol: HiveCoreProtocol = quill_bundle["protocol"]

    activation = quill_agent.activate(f"{protocol.tyme_core_binding}::Lattice-Engine")
    lattice = build_quill_lattice_prototype()

    manifest = {
        "engine": "Quill-core", 
        "binding": protocol.tyme_core_binding,
        "agent": activation,
        "lattice": lattice.to_dict(),
        "protocol": protocol.protocol_name,
        "installed_at": datetime.now(UTC).isoformat(),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2))
    return manifest


__all__ = [
    "LayerBridge",
    "QuillLatticePrototype",
    "build_quill_lattice_prototype",
    "bootstrap_quill_core",
    "load_avot_quill",
]
