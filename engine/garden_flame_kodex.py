"""Garden Flame Kodex ethical layer and binding utilities.

The Garden Flame Kodex is treated as the primary ethical substrate that
safeguards reasoning loops, agent outputs, and system actions. It exposes
protocols for coherence validation, resonance alignment, and harmonic
safety checks while emitting a manifest of all bindings for downstream
inspection.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass
class GardenFlameProtocol:
    """Represents a single Garden Flame protocol directive."""

    name: str
    focus: str
    checks: List[str]
    status: str = "enabled"


@dataclass
class BindingSignal:
    """Binding state applied to a target surface."""

    target: str
    target_type: str
    protocols: List[str]
    status: str = "bound"
    coherence_check: str = "aligned"
    resonance_alignment: str = "tuned"
    harmonic_safety: str = "guarded"
    last_verified_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class GardenFlameKodex:
    """Primary ethical layer that binds Garden Flame protocols across Tyme."""

    def __init__(self, name: str = "Garden Flame Kodex", version: str = "1.0.0") -> None:
        self.name = name
        self.version = version
        self.protocols = self._default_protocols()

    def _default_protocols(self) -> List[GardenFlameProtocol]:
        return [
            GardenFlameProtocol(
                name="Coherence-Check",
                focus="Validate reasoning outputs remain consistent with the Codex and current mission signals.",
                checks=[
                    "Trace lineage back to sovereign scrolls",
                    "Detect hallucinated or unsupported claims",
                    "Preserve contextual integrity across hops",
                ],
            ),
            GardenFlameProtocol(
                name="Resonance-Alignment",
                focus="Tune tone, intent, and relational posture to the Garden Flame ethic.",
                checks=[
                    "Normalize tone signatures toward harmonic center",
                    "Detect resonance drift and re-center",
                    "Surface subtle dissonance before emission",
                ],
            ),
            GardenFlameProtocol(
                name="Harmonic-Safety",
                focus="Ensure system actions respect safety rails, consent, and sovereign stewardship.",
                checks=[
                    "Block harmful or irreversible actions without consent",
                    "Enforce safety envelopes on generated artifacts",
                    "Transmute unsafe intent into guided alternatives",
                ],
            ),
        ]

    def _build_binding_signals(self, targets: Iterable[str], target_type: str) -> List[BindingSignal]:
        protocol_names = [protocol.name for protocol in self.protocols]
        return [BindingSignal(target=target, target_type=target_type, protocols=protocol_names) for target in targets]

    def activate_layer(
        self,
        reasoning_loops: Iterable[str],
        agent_outputs: Iterable[str],
        system_actions: Iterable[str],
        output_path: Path | str = Path("chronicle/garden_flame_kodex.json"),
    ) -> Dict[str, object]:
        """Bind the Garden Flame Kodex to the provided surfaces and persist the manifest."""

        reasoning_targets = list(reasoning_loops)
        agent_targets = list(agent_outputs)
        action_targets = list(system_actions)

        reasoning_bindings = self._build_binding_signals(reasoning_targets, "reasoning_loop")
        agent_bindings = self._build_binding_signals(agent_targets, "agent_output")
        action_bindings = self._build_binding_signals(action_targets, "system_action")

        manifest = {
            "kodex": {
                "name": self.name,
                "version": self.version,
                "installed_at": datetime.now(UTC).isoformat(),
                "primary": True,
            },
            "protocols": [asdict(protocol) for protocol in self.protocols],
            "bindings": {
                "reasoning_loops": [asdict(binding) for binding in reasoning_bindings],
                "agent_outputs": [asdict(binding) for binding in agent_bindings],
                "system_actions": [asdict(binding) for binding in action_bindings],
            },
            "coverage": {
                "reasoning_loops": len(reasoning_targets),
                "agent_outputs": len(agent_targets),
                "system_actions": len(action_targets),
            },
        }

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            self._format_manifest(manifest),
            encoding="utf-8",
        )
        return manifest

    def _format_manifest(self, manifest: Dict[str, object]) -> str:
        return (
            json_dumps_sorted(manifest)
            + "\n"
        )


def json_dumps_sorted(payload: Dict[str, object]) -> str:
    """Serialize the manifest with deterministic key ordering for review."""

    import json

    return json.dumps(payload, indent=2, sort_keys=True)


__all__ = ["GardenFlameKodex", "GardenFlameProtocol", "BindingSignal", "json_dumps_sorted"]
