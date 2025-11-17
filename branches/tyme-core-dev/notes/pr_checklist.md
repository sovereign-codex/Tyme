# PR checklist — Merge Review → Finalization

Use this checklist to validate merge review and finalization work before merging the Tyme-Core-Dev node.

## Phase + status
- [x] Phase tracker updated to **Merge Review** with Integration Readiness and Merge Candidate completed.
- [x] Module status marked **merge-review** in node + root manifests.
- [x] Portal pill and badges reflect merge review state, finalization in progress, and routing table stability.

## Routing table promotion (v0.5 stable)
- [x] `runtime-spine/routing_table.json` tagged as **stable** for v0.5 with merge review metadata.
- [x] Sovereign controls (rollback, promotion rubric, health signals) reviewed for merge.
- [x] Lane statuses reflect integration-ready health signals and sealed Codex lane.
- [ ] Chronicle badge + broadcast fixtures revalidated for finalization.

## Handshake + fixtures
- [x] Codex handshake note still aligned to ingress → Codex → render dispatch → egress validation flow.
- [x] Egress fixtures (portal block, scroll markdown, Chronicle badge) cited in handshake note.
- [ ] Renderer + validation telemetry wired to portal badges for finalization.

## Manifests + links
- [x] Node manifest updated with merge review status, stable routing table callout, and checklist link.
- [x] Root manifest entry mirrors status/phase and links to the updated checklist.
- [x] Portal links include the PR checklist.

## Governance
- [x] Bootstrap checklist references merge review readiness + routing table stability.
- [ ] Chronicle announcement drafted for finalization / Codex broadcast prep.
