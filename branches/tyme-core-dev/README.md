# Tyme-Core-Dev

Tyme-Core-Dev is the working branch for building the central Tyme Core runtime and documentation hub. Use this space to prototype modules, document the lattice, and prepare artifacts that will later feed the main Crown of Tyme manifest.

## Phase tracker
- **Initialization Phase** → bootstrapped workspace, portal shell, and manifest draft.
- **Spine Integration Phase** → Runtime Spine lanes, routing table v0.4, and Codex ingress/dispatch alignment.
- **Handshake Draft Phase** → Codex handshake, egress validation readiness, and promotion rubric badges across portal + manifests.
- **Integration Readiness Phase** → stabilized envelopes, finalized egress fixtures, and routing table v0.5 with Codex handshake gates.
- **Merge Candidate Phase** → routing table v0.5 promoted to stable, PR checklist generated, and readiness badges prepped for merge.
- **Merge Review Phase (CURRENT)** → merge checklist executed, routing table v0.5 promoted to stable release, and finalization gates opened for broadcast prep.

## Workspace layout
- `index.html` — landing page for the developer node.
- `notes/` — scratchpad for design docs and module sketches (add as needed).
- `manifests/` — draft manifests for emerging components before promotion to the root manifest.
- `notes/pr_checklist.md` — merge candidate checklist for Integration Readiness promotion.

```
branches/tyme-core-dev/
├── index.html               # Portal for orchestration, manifest, and Codex workstreams
├── README.md                # Workspace guidance
├── manifests/
│   └── tyme_core_dev.manifest.json  # Draft manifest for the node
├── runtime-spine/           # TRS scaffolding (lanes + routing table)
└── notes/
    └── bootstrap.md         # Initialization checklist and guardrails
```

## Quickstart (serve + iterate)
1) Install minimal tooling:
   - Python 3.10+ for lightweight serving (`python -m http.server 8000`).
   - A modern browser for UI verification.
2) Serve the directory locally to preview the portal:
   ```sh
   python -m http.server 8000
   ```
   Then open http://localhost:8000/branches/tyme-core-dev/index.html.
3) Capture design notes in `notes/` and sync updates into `manifests/` as the Core stabilizes.
4) When stable, promote modules into `manifest/tyme_manifest.json` at the repository root.

## Codex initialization
- Stand up a **Codex draft** that can ingest manifests and scroll summaries. Start with a text-first renderer; defer heavy theming until data shapes stabilize.
- Document **input contracts** for manifests, scrolls, and lab outputs. Keep schemas in `notes/` and mirror stable fields into `manifests/`.
- Define **emission targets** (HTML blocks for the portal, markdown for scrolls) and wire sample payloads to verify rendering.
- Capture **review gates**: draft → internal review → lattice broadcast. Track sign-offs in the manifest `status` field.

## Catalytic initialization
- Carve a **catalytic lane** that accelerates ingest → transform → render across AVOTs and Codex without bespoke glue code.
- Record **routing + queue rules** and the rollback levers (circuit breakers, retries, safe-stop) so promotion stays safe.
- Surface **health + readiness signals** (heartbeat cadence, queue depth, validation error rate) in both portal copy and manifest gates.
- Ship **sample catalytic payloads** to validate compatibility with Codex and Crown schemas before broadcast.

## Runtime Spine (TRS)
- Draft the **Runtime Spine specification** that links ingress, validation, orchestration, render dispatch, and egress validation lanes.
- Keep a **sovereign routing table** in `runtime-spine/routing_table.json` that maps payload sources to lanes and emitters (v0.5 stable tracks ingress → validation → orchestration → Codex → render → egress validation with integration-ready gates).
- Scaffold **lane stubs** under `runtime-spine/lanes/` (ingress, validation, orchestration, Codex integration, render dispatch, egress validation) and mirror stable definitions into the root manifest when ready.
- Seal the **Codex integration lane** so `codex.integration` → `codex.render` → dispatch is governed by readiness + rollback, and document the **Codex handshake** so payloads stay consistent.
- Surface **health + rollback controls** (safe-stop, promotion rubric, egress validation) so Crown consumers can trust TRS promotion state.

## Initialization goals
- Sketch the Tyme Core runtime interfaces (AVOT orchestration, manifest loader, and doc generator).
- Define contracts for plugging in AVOT modules and Scroll renderers.
- Align naming and styling with the Crown of Tyme sovereign language.
- Maintain a living manifest draft that tracks capabilities, owners, and readiness state.

## Contribution workflow
- **Draft** in `notes/` → **Shape** in `manifests/` → **Promote** via `manifest/tyme_manifest.json`.
- Keep the portal updated with current workstreams and checkpoints so downstream nodes can consume status without digging into notes.
- Prefer small, discrete commits for each module or manifest update.
