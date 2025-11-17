# Tyme-Core-Dev bootstrap checklist

## Environment sanity
- [ ] Python 3.10+ available
- [ ] Browser installed for portal review
- [ ] Local HTTP server running (`python -m http.server 8000`)

## Runtime scaffolding
- [x] Mark phase progression (Initialization → Spine Integration → Handshake Draft → Integration Readiness) across portal and manifests
- [ ] Define AVOT orchestration contract (init, dispatch, telemetry)
- [ ] Draft manifest loader phases (ingest → validate → publish)
- [ ] Map Codex generation inputs (scrolls, manifests, lab results)
- [ ] Produce sample Codex payloads and validate against schema draft
- [ ] Integrate Codex output stubs into the portal for live preview
- [ ] Define catalytic routing (ingest/validate/dispatch) and rollback levers
- [ ] Capture catalytic health signals (heartbeat cadence, queue depth, error rate)
- [x] Draft Runtime Spine (TRS) lanes (ingress, validation, orchestration, render dispatch)
- [x] Publish sovereign routing table in `runtime-spine/routing_table.json`
- [x] Mirror TRS readiness gates and rollback controls into manifests + portal
- [x] Seal TRS → Routing Table → Codex integration lane and document acceptance gates
- [x] Establish render dispatch lanes (portal feed, scroll broadcast) and handshake to egress validation
- [x] Draft egress validation lane for portal/scroll/Chronicle outputs
- [x] Capture Codex handshake draft between TRS routing table and renderers
- [ ] Wire portal badges to routing table health signals (renderer success, preview acceptance, render latency)
- [x] Exercise egress fixtures for portal blocks, scroll markdown, and Chronicle badges

## Merge review readiness
- [x] Mark Integration Readiness complete and advance to Merge Candidate in portal + manifests
- [x] Advance to Merge Review and refresh portal + manifests + checklist
- [x] Tag routing table v0.5 as stable for Integration Readiness / Merge Review
- [x] Publish PR checklist at `notes/pr_checklist.md` and link from portal/manifest
- [ ] Chronicle announcement draft prepared for Codex broadcast prep/finalization

## Governance
- [ ] Confirm owner list and escalation path
- [ ] Decide readiness rubric (draft → review → stabilized)
- [ ] Wire promotion steps into `manifest/tyme_manifest.json`
