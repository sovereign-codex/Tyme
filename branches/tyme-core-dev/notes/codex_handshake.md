# Codex handshake (merge review) — TRS → Codex → Dispatch

## Purpose
Document the handshake between the Runtime Spine (TRS) and Codex renderers so payloads stay consistent from ingress through egress validation. This integration-ready draft sets guardrails for readiness gates, rollback hooks, and telemetry that the routing table can enforce.

## Handshake phases
1) **Ingress affirmation**: payloads entering Codex must carry `metadata.submitter`, `timestamp`, `trace_id`, and `readiness_hint` from ingress normalization; malformed envelopes are rejected.
2) **Merge review (current)**: Codex integration accepts only `[draft, review, soak]` readiness and requires a `rollback_handle` for safe-stop; readiness `broadcast` is set only after egress validation passes and Chronicle badge health aligns.
3) **Renderer contract**: Codex renderers emit `codex.render` (broadcast) and `codex.preview` (soak) bundles with provenance, renderer profile, promotion rubric markers, and checksum placeholders.
4) **Render dispatch lanes**: render bundles are fanned out by render dispatch lanes (portal feed, scroll broadcast) that apply promotion rubric checks before egress validation, attaching badge + provenance anchors.
5) **Egress validation**: validates outbound artifacts (HTML blocks, Markdown scrolls, Chronicle badges) for anchors, provenance, readiness, and checksum integrity before broadcast; fixtures now mirror the stable envelope.

### Stabilized handshake envelope (integration readiness)
```json
{
  "trace_id": "trs-2025-11-17-001",
  "metadata": {
    "submitter": "sovereign-intelligence",
    "timestamp": "2025-11-17T04:00:00Z",
    "readiness_hint": "review"
  },
  "rollback_handle": "global.rollback.safe_stop",
  "provenance": {
    "source_manifest": "Tyme-Core-Dev",
    "ingress_run_id": "ingress-4821"
  },
  "payload": {
    "kind": "manifest.draft",
    "content": { "name": "Tyme-Core-Dev" }
  },
  "renderer_requirements": {
    "provenance_required": true,
    "promotion_rubric": ["draft", "review", "soak", "broadcast"],
    "checksum_expected": true
  },
  "egress_fixture": {
    "portal_block": "<article data-trace=\"trs-2025-11-17-001\" data-readiness=\"review\"><h2>Tyme-Core-Dev</h2></article>",
    "scroll_markdown": "## Tyme-Core-Dev (trace: trs-2025-11-17-001)\n\nReadiness: review",
    "chronicle_badge": {
      "readiness": "review",
      "renderer_success_ratio": 0.98,
      "checksum": "sha256:abc123"
    }
  }
}
```

### Dispatch checkpoints
- Portal and scroll outputs must declare **provenance anchors**, **readiness badge**, and **checksum** before egress validation.
- **Preview acceptance** ≥ 0.9 gates promotion into `render.egress`; **renderer success** ≥ 0.95 before broadcast.
- Egress validator echoes `trace_id` + `rollback_handle` to simplify rollback on checksum or anchor failure.
- Chronicle badge fixtures must mirror renderer health (`renderer_success_ratio`, `preview_acceptance_ratio`) and readiness before promotion.

## Controls & signals
- **Acceptance gates**: readiness within rubric; renderer success ratio ≥ 0.95 for broadcast; preview acceptance ≥ 0.9 before promotion; egress checks for anchors + checksum signatures; Chronicle badge requires renderer + preview health echoed.
- **Rollback**: invoke `global.rollback.safe_stop` on schema drift, renderer regressions, or egress validation failures; divert to `codex.preview` until health clears.
- **Telemetry**: heartbeat cadence, queue depth per lane, validation error rate, renderer success ratio, preview acceptance ratio, egress checksum failures.

## Next steps
- [x] Align render dispatch lane specs with portal + scroll emission checkpoints.
- [x] Implement egress validation fixtures for portal blocks and scroll markdown outputs.
- [x] Mirror handshake expectations into the routing table (v0.5) and manifests.
- [x] Surface handshake status as badges in the developer portal and root manifest.
- [ ] Wire renderer + validation telemetry into portal health badges for finalization broadcast gating.
