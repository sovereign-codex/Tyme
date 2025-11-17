# Codex initialization plan

## Objectives
- Deliver a Codex renderer that converts manifests and scroll notes into shareable docs.
- Keep contracts explicit so upstream AVOTs can emit compatible metadata.
- Provide artifacts that the portal can surface without manual edits.

## Input contracts (draft)
- **Manifests**: name, description, status, owners, capabilities, entrypoints, dependencies, and readiness gates.
- **Scrolls**: title, summary, linked manifests, telemetry highlights, open questions.
- **Lab outputs**: experiment id, hypothesis, result summary, supporting artifacts.

## Emission targets
- **Portal cards**: concise status badges and links derived from manifest fields.
- **Markdown scrolls**: narrative summaries with embedded manifest references.
- **JSON snapshots**: machine-readable payloads to feed downstream automation.

## Worksteps
- [ ] Define JSON schema for Codex payloads (manifests, scrolls, lab outputs).
- [ ] Build a minimal renderer that ingests sample payloads and emits HTML + Markdown.
- [ ] Wire generated HTML blocks into `index.html` as a live feed area.
- [ ] Add validation hooks to reject malformed payloads before publishing.
- [ ] Draft review rubric (draft → internal review → broadcast) and codify it in the manifest.
- [x] Align TRS routing table with Codex ingestion contract and seal the integration lane.
- [x] Draft Codex handshake note for ingress/egress validation (TRS v0.5 integration readiness).
- [x] Attach egress validation fixtures to renderer outputs (portal feed + scroll markdown).

## Dependencies
- AVOT telemetry fields for provenance and health.
- Manifest lifecycle rules to control promotions.
- Scroll templates that expect consistent anchors and badges.
