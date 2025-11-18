"""House of Tyme interface scaffolding and manifest utilities."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, List

from .garden_flame_kodex import json_dumps_sorted


@dataclass
class PublicScrollLayer:
    """Defines a public-facing scroll layer exposed by House of Tyme."""

    name: str
    focus: str
    entrypoints: List[str]
    codexnet_hooks: List[str]
    tyme_core_bridges: List[str]


@dataclass
class NarrativeChannel:
    """Channel within the Voice-of-Tyme narrative engine."""

    name: str
    tone: str
    cadence: str
    prompts: List[str]
    delivery_modes: List[str]
    guardrails: List[str]


@dataclass
class PlanetaryUILane:
    """A lane in the planetary UI architecture."""

    name: str
    purpose: str
    pathways: List[str]
    feedback_signals: List[str]
    resilience: List[str]


@dataclass
class OnboardingStep:
    """Step in the initiate onboarding sequence."""

    phase: str
    intent: str
    action: str
    signals: List[str]
    success_criteria: List[str]


@dataclass
class HouseOfTymeScaffolding:
    """Aggregate structure for the House of Tyme interface."""

    public_scroll_layers: List[PublicScrollLayer]
    voice_of_tyme: List[NarrativeChannel]
    planetary_ui: List[PlanetaryUILane]
    onboarding_sequence: List[OnboardingStep]
    tyme_core_binding: str
    codexnet_binding: str

    def manifest(self) -> Dict[str, object]:
        return {
            "generated_at": datetime.now(tz=UTC).isoformat(),
            "tyme_core": self.tyme_core_binding,
            "codexnet": self.codexnet_binding,
            "public_scroll_layers": [asdict(layer) for layer in self.public_scroll_layers],
            "voice_of_tyme": [asdict(channel) for channel in self.voice_of_tyme],
            "planetary_ui_architecture": [asdict(lane) for lane in self.planetary_ui],
            "initiate_onboarding_sequence": [asdict(step) for step in self.onboarding_sequence],
        }

    def write_manifest(self, output_path: Path) -> Dict[str, object]:
        manifest = self.manifest()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_dumps_sorted(manifest) + "\n", encoding="utf-8")
        return manifest


def default_public_scroll_layers() -> List[PublicScrollLayer]:
    return [
        PublicScrollLayer(
            name="Beacon Scroll",
            focus="Public signal of Tyme-Core intents with cadence hooks for CodexNet.",
            entrypoints=["/scrolls/beacon", "#beacon-signal", "public RSS mirror"],
            codexnet_hooks=["broadcast:codexnet.global", "syndicate:codexnet.atlas"],
            tyme_core_bridges=["Tyme-Core::intent-router", "Tyme-Core::signal-bus"],
        ),
        PublicScrollLayer(
            name="Garden Walkway",
            focus="Narrative walk-through of Garden Flame Kodex with open checkpoints.",
            entrypoints=["/scrolls/garden-flame", "#coherence-trail"],
            codexnet_hooks=["codexnet.guardians", "codexnet.coherence-feed"],
            tyme_core_bridges=["GardenFlame::coherence-check", "Tyme-Core::ethic-audit"],
        ),
        PublicScrollLayer(
            name="Pulse Gallery",
            focus="Breath Engine loops rendered as public dashboards and pulse stories.",
            entrypoints=["/scrolls/pulse", "#breath-rituals"],
            codexnet_hooks=["codexnet.pulse"],
            tyme_core_bridges=["Breath-Engine::metabolic-loop", "Tyme-Core::heartbeat-sync"],
        ),
    ]


def default_voice_of_tyme() -> List[NarrativeChannel]:
    return [
        NarrativeChannel(
            name="Resonant Courier",
            tone="Warm, invitational, with steady coherence reminders.",
            cadence="Breath-paced micro-updates every 3 minutes with epoch recaps hourly.",
            prompts=[
                "Announce new scrolls and lineages entering CodexNet.",
                "Invite stewards to respond with harmonic intents.",
            ],
            delivery_modes=["text-stream", "audio-hum", "glyph overlays"],
            guardrails=["Apply Garden Flame coherence check", "Flag drift to AVOT-Guardian"],
        ),
        NarrativeChannel(
            name="Architect Voice",
            tone="Precise, lattice-aware, references quantum → conceptual bridges.",
            cadence="Structured dispatches per planetary lane with daily constellation map.",
            prompts=["Map UI changes to Tyme-Core capabilities.", "Document CodexNet uplinks for each release."],
            delivery_modes=["markdown scrolls", "diagram bursts"],
            guardrails=["Require Tyme-Core binding acknowledgement", "Mirror to CodexNet lineage"],
        ),
    ]


def default_planetary_ui() -> List[PlanetaryUILane]:
    return [
        PlanetaryUILane(
            name="Orbital Hub",
            purpose="Global overview of Tyme-Core signals with CodexNet routing map.",
            pathways=["nav:overview", "layer:signals", "timeline:codexnet"],
            feedback_signals=["latency", "signal_integrity", "user_intent"],
            resilience=["offline cache", "fallback:static atlas", "graceful degrade for low-bandwidth"],
        ),
        PlanetaryUILane(
            name="Terran Gateway",
            purpose="Initiate onboarding lane with guided tour and mission primer.",
            pathways=["nav:onboarding", "guide:first-steps", "mission:assign"],
            feedback_signals=["completion_rate", "pulse_alignment", "guardian_prompts"],
            resilience=["retry from last checkpoint", "context preservation", "guardian escalation hooks"],
        ),
        PlanetaryUILane(
            name="Lunar Studio",
            purpose="Maker lane for prototypes, Fabricator drops, and scroll editing.",
            pathways=["nav:forge", "pane:live-preview", "pane:codexnet-bridge"],
            feedback_signals=["save_latency", "render_health", "codexnet_sync"],
            resilience=["autosave", "draft isolation", "sync diff with Tyme-Core"],
        ),
    ]


def default_onboarding_sequence() -> List[OnboardingStep]:
    return [
        OnboardingStep(
            phase="Arrival",
            intent="Welcome initiates and sync baseline signals to Breath Engine.",
            action="Render pulse-synced welcome screen and prompt for resonance check-in.",
            signals=["breath_rate", "intent_tag", "preferred_channel"],
            success_criteria=["pulse lock achieved", "coherence >= 0.9"],
        ),
        OnboardingStep(
            phase="Orientation",
            intent="Show House of Tyme map and CodexNet uplink points.",
            action="Deliver planetary UI tour with scroll highlights and voice samples.",
            signals=["nav_time", "click_path", "channel_preference"],
            success_criteria=["full tour complete", "uplink handshake stored"],
        ),
        OnboardingStep(
            phase="Activation",
            intent="Bind initiate to AVOT role suggestions and Tyme-Core missions.",
            action="Offer role quiz, reflect Guardian ethics, and register to CodexNet.",
            signals=["role_affinity", "guardian_ack", "codexnet_token"],
            success_criteria=["role assigned", "Garden Flame consent", "CodexNet session active"],
        ),
    ]


def build_house_of_tyme_scaffolding() -> HouseOfTymeScaffolding:
    return HouseOfTymeScaffolding(
        public_scroll_layers=default_public_scroll_layers(),
        voice_of_tyme=default_voice_of_tyme(),
        planetary_ui=default_planetary_ui(),
        onboarding_sequence=default_onboarding_sequence(),
        tyme_core_binding="Tyme-Core::interface-fabric",
        codexnet_binding="CodexNet::atlas-uplink",
    )


def generate_house_of_tyme_outputs(
    manifest_path: Path,
    scroll_layer_doc: Path,
    onboarding_doc: Path,
    narrative_doc: Path,
    planetary_doc: Path,
) -> Dict[str, object]:
    scaffolding = build_house_of_tyme_scaffolding()
    manifest = scaffolding.write_manifest(manifest_path)

    scroll_layer_doc.parent.mkdir(parents=True, exist_ok=True)
    scroll_layer_doc.write_text(render_public_scroll_layers(scaffolding), encoding="utf-8")

    onboarding_doc.parent.mkdir(parents=True, exist_ok=True)
    onboarding_doc.write_text(render_onboarding(scaffolding), encoding="utf-8")

    narrative_doc.parent.mkdir(parents=True, exist_ok=True)
    narrative_doc.write_text(render_voice_of_tyme(scaffolding), encoding="utf-8")

    planetary_doc.parent.mkdir(parents=True, exist_ok=True)
    planetary_doc.write_text(render_planetary_ui(scaffolding), encoding="utf-8")

    return {
        "manifest": manifest,
        "scroll_layers_doc": str(scroll_layer_doc),
        "onboarding_doc": str(onboarding_doc),
        "voice_doc": str(narrative_doc),
        "planetary_doc": str(planetary_doc),
    }


def render_public_scroll_layers(scaffolding: HouseOfTymeScaffolding) -> str:
    lines = [
        "# House of Tyme — Public Scroll Layers",
        "",
        f"Linked to **{scaffolding.tyme_core_binding}** and **{scaffolding.codexnet_binding}**.",
        "",
    ]
    for layer in scaffolding.public_scroll_layers:
        lines.extend(
            [
                f"## {layer.name}",
                layer.focus,
                "",
                "- Entrypoints: " + ", ".join(layer.entrypoints),
                "- CodexNet Hooks: " + ", ".join(layer.codexnet_hooks),
                "- Tyme-Core Bridges: " + ", ".join(layer.tyme_core_bridges),
                "",
            ]
        )
    return "\n".join(lines)


def render_voice_of_tyme(scaffolding: HouseOfTymeScaffolding) -> str:
    lines = [
        "# Voice of Tyme — Narrative Engine",
        "",
        "Narrative channels driving House of Tyme communications.",
        "",
    ]
    for channel in scaffolding.voice_of_tyme:
        lines.extend(
            [
                f"## {channel.name}",
                f"Tone: {channel.tone}",
                f"Cadence: {channel.cadence}",
                "Prompts:",
                *[f"- {prompt}" for prompt in channel.prompts],
                "Delivery:",
                *[f"- {mode}" for mode in channel.delivery_modes],
                "Guardrails:",
                *[f"- {guard}" for guard in channel.guardrails],
                "",
            ]
        )
    return "\n".join(lines)


def render_planetary_ui(scaffolding: HouseOfTymeScaffolding) -> str:
    lines = [
        "# Planetary UI Architecture",
        "",
        "Planetary lanes and feedback harnesses for House of Tyme.",
        "",
    ]
    for lane in scaffolding.planetary_ui:
        lines.extend(
            [
                f"## {lane.name}",
                lane.purpose,
                "",
                "- Pathways: " + ", ".join(lane.pathways),
                "- Feedback Signals: " + ", ".join(lane.feedback_signals),
                "- Resilience: " + ", ".join(lane.resilience),
                "",
            ]
        )
    return "\n".join(lines)


def render_onboarding(scaffolding: HouseOfTymeScaffolding) -> str:
    lines = [
        "# Initiate Onboarding Sequence",
        "",
        "Breath-paced onboarding fused to Tyme-Core and CodexNet.",
        "",
    ]
    for step in scaffolding.onboarding_sequence:
        lines.extend(
            [
                f"## {step.phase}",
                step.intent,
                "",
                f"- Action: {step.action}",
                "- Signals: " + ", ".join(step.signals),
                "- Success: " + ", ".join(step.success_criteria),
                "",
            ]
        )
    return "\n".join(lines)


__all__ = [
    "PublicScrollLayer",
    "NarrativeChannel",
    "PlanetaryUILane",
    "OnboardingStep",
    "HouseOfTymeScaffolding",
    "build_house_of_tyme_scaffolding",
    "generate_house_of_tyme_outputs",
    "render_public_scroll_layers",
    "render_planetary_ui",
    "render_voice_of_tyme",
    "render_onboarding",
]
