# PR checklist — Finalization → Merge

Use this checklist to validate merge review and finalization work before merging the Tyme-Core-Dev node.

## Phase + status
- [x] Phase tracker updated to **Finalization** with Integration Readiness → Merge Candidate → Merge Review recorded.
- [x] Module status marked **finalization** in node + root manifests.
- [x] Portal pill and badges reflect finalization state, conflicts resolved, and routing table stability.
- [x] Merge conflicts for PR #X resolved and artifacts reconciled across portal, notes, and manifests.

## Routing table promotion (v0.5 stable)
- [x] `runtime-spine/routing_table.json` tagged as **stable** for v0.5 with finalization metadata.
- [x] Sovereign controls (rollback, promotion rubric, health signals) reviewed for merge.
- [x] Lane statuses reflect integration-ready health signals and sealed Codex lane.
- [x] Chronicle badge + broadcast fixtures revalidated for finalization.

## Handshake + fixtures
- [x] Codex handshake note aligned to ingress → Codex → render dispatch → egress validation flow.
- [x] Egress fixtures (portal block, scroll markdown, Chronicle badge) cited in handshake note.
- [ ] Renderer + validation telemetry wired to portal badges for finalization.

## Manifests + links
- [x] Node manifest updated with finalization status, stable routing table callout, and checklist link.
- [x] Root manifest entry mirrors status/phase and links to the updated checklist.
- [x] Portal links include the PR checklist.

## Governance
- [x] Bootstrap checklist references finalization readiness + routing table stability.
- [ ] Chronicle announcement drafted for finalization / Codex broadcast prep.
