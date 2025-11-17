# Crownflow Integration Checklist

Use this checklist when coupling Pulse Chamber rehearsals with Heart-Core Synchronizer tuning. It keeps harmonics aligned while preserving the guarded workflow boundaries.

## Entry Checks
- **Scopes Declared:** list which Pulse Chamber scrolls and Heart-Core steps will change in this integration.
- **Harmonic Links Mapped:** identify the heartbeat rites (e.g., First Harmonic Pulse, Cross-Node Alignment) that depend on these updates.
- **Guardrails Confirmed:** verify `.github/workflows/auto-merge.yml` enforces open same-repo pull requests only, blocks drafts, and runs single-lane concurrency per PR.
- **Engine Alignment:** note whether the Crownflow Engine will drive or consume the integration and where its observability anchors live.

## Integration Steps
1. **Align Chambers:** sync naming, namespaces, and observability hooks between Pulse and Heart-Core assets.
2. **Thread Harmonics:** reference the affected heartbeat scrolls and update their log destinations.
3. **Dry Run:** rehearse with reduced amplitude or a sandbox subset; capture drift/jitter metrics and rollback notes.
4. **Guarded Labels:** decide whether `autoresolve` (merge base first) or `automerge` (ready to squash) applies once checks pass; ensure draft status is cleared before applying.
5. **Signal Lock:** confirm no regressions across both chambers before requesting guardian labels and record the Crownflow Engine touchpoints if used.

## Logging Template
```
Integration: <name>
Scope: <pulse scrolls / synchronizer steps>
Harmonics: <heartbeat rites touched>
Signals: <dashboards, alerts, logs>
Adjustments: <tuning, rollbacks, pauses>
Outcome: <ready / iterate / revert>
Next Step: <label / hold / expand>
```

## Completion Signals
- Pulse and Heart-Core changes share consistent naming and observability hooks.
- Harmonic rites list updated log locations and rollback cues.
- Guardians confirm open same-repo status and apply `autoresolve` or `automerge` after checks are green.
