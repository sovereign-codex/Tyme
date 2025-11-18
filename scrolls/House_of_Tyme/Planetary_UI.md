# Planetary UI Architecture

Planetary lanes and feedback harnesses for House of Tyme.

## Orbital Hub
Global overview of Tyme-Core signals with CodexNet routing map.

- Pathways: nav:overview, layer:signals, timeline:codexnet
- Feedback Signals: latency, signal_integrity, user_intent
- Resilience: offline cache, fallback:static atlas, graceful degrade for low-bandwidth

## Terran Gateway
Initiate onboarding lane with guided tour and mission primer.

- Pathways: nav:onboarding, guide:first-steps, mission:assign
- Feedback Signals: completion_rate, pulse_alignment, guardian_prompts
- Resilience: retry from last checkpoint, context preservation, guardian escalation hooks

## Lunar Studio
Maker lane for prototypes, Fabricator drops, and scroll editing.

- Pathways: nav:forge, pane:live-preview, pane:codexnet-bridge
- Feedback Signals: save_latency, render_health, codexnet_sync
- Resilience: autosave, draft isolation, sync diff with Tyme-Core
