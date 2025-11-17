# Tri-Chamber Interlock

The Tri-Chamber Interlock binds the Pulse Chamber, Heart-Core Synchronizer, and Crownflow Integration into a single safeguarded lane. Use it when work spans all three chambers so observability, labels, and harmonics stay in lockstep.

## Purpose
- Keep pulse staging, core synchronization, and cross-chamber coupling aligned under one ritual.
- Enforce the guarded automation path (open same-repo pull requests only, one concurrency lane per PR, no drafts) before labels are applied.
- Centralize logging and rollback cues so guardians can trace how each chamber was engaged.

## Activation Steps
1. **Declare Scope:** list the Pulse Chamber scrolls, Heart-Core steps, and Crownflow harmonics in play.
2. **Sync Guardrails:** confirm `.github/workflows/auto-merge.yml` is present, limited to open same-repo PRs, draft-safe, and single-lane via concurrency.
3. **Align Signals:** point all three chambers to shared observability anchors and harmonize naming for dashboards/logs.
4. **Dry Coupling:** run a reduced-amplitude rehearsal that traverses all three chambers; capture drift/jitter notes and rollback routes.
5. **Label Readiness:** decide if `autoresolve` (merge base first) or `automerge` (ready to squash) applies once checks go green; ensure guardians own the decision.

## Logging Template
```
Interlock: <name>
Scope: <pulse scrolls / synchronizer steps / crownflow links>
Signals: <dashboards, alerts, traces>
Harmonics: <rites touched>
Guardrails: <open same-repo confirmed, draft cleared, concurrency lane noted>
Outcome: <ready / iterate / rollback>
Next Action: <label / hold / expand>
```

## Completion Signals
- All three chambers reference the same observability anchors and rollback cues.
- Label choice (`automerge` or `autoresolve`) is documented with guardian confirmation and open same-repo validation.
- The interlock log is stored alongside the involved scrolls with drift/jitter results and any adjustments.
