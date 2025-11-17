# Tyme Runtime Spine (TRS)

This directory captures the Runtime Spine scaffolding for Tyme-Core-Dev. Use it to model lanes, routing, and sovereignty rules before they are promoted into the Crown.

## Layout
- `lanes/` — lane definitions and placeholders for ingress, validation, orchestration, Codex integration, render dispatchers, and egress validation.
- `routing_table.json` — sovereign routing table draft that binds inputs to lanes and downstream emitters (v0.5 stable, integration readiness sealed).
- `README.md` — this guide.
- `lanes/ingress.md` — ingress envelope and deduplication rules.
- `lanes/validation.md` — schema + readiness enforcement and enrichment.
- `lanes/orchestration.md` — split-routing and rollback hooks for AVOT and Codex.
- `lanes/trs_codex_integration.md` — sealed TRS → Routing Table → Codex lane contract and verification steps.
- `lanes/render_dispatch.md` — dispatch rubric and emission controls for portal + scrolls.
- `lanes/egress_validation.md` — outbound validation prior to portal/scroll/Chronicle broadcast.

## Usage
- Add lane specs or stubs under `lanes/` as they are defined in the TRS specification.
- Keep the routing table in sync with manifest capabilities and portal surfacing so downstream nodes can rely on it.
- Mirror any stable routing or lane definitions into the root manifest when ready.
