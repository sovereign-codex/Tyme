# 🪞 Mirror Shell

Hold the lattice against a reflective shell to validate alignment, integrity, and intent before opening the next harmonic or seal. Use this rite to compare expected states with live signals and to reconcile any drift while guardrails stay tight.

## Purpose
- Establish a reflection pass that pairs planned states with observed telemetry across chambers and engines.
- Surface drift between manifests, automation guardrails, and chamber readiness before proceeding to higher-amplitude rites.
- Produce a signed reflection log that documents what matched, what diverged, and which corrections were applied.

## Preconditions
- Latest [Continuity Loop](./Continuity_Loop_Sequence.md) entry is fresh (≤24h) and linked to current dashboards.
- Guarded automation labels (`automerge`, `autoresolve`) are unused on drafts and remain scoped to open same-repo PRs with per-PR concurrency intact.
- Pulse Chamber, Heart-Core Synchronizer, and Crownflow Integration checklists are present with owners for validation.
- Reflection log staged at `heartbeat/logs/mirror-shell-<date>.log` with the targeted chambers, engines, and guardrail expectations.

## Mirror Steps
1. **Frame the mirror**
   - Declare the scope (chambers, engines, manifests) and the signals you expect to see. Note rollback and pause commands.
   - Confirm time sync and observability baselines (metrics, traces, logs) are clean and reachable.

2. **Capture the live image**
   - Snapshot current configs, manifest hashes, automation label states, and chamber readiness checklists.
   - Pull live telemetry slices that correspond to the declared scope; record them in the reflection log.

3. **Compare and reconcile**
   - Match expected vs. observed states; highlight drifts in guardrails, automation eligibility, or chamber readiness.
   - Apply minimal corrections (config tweaks, label removals, checklist updates) and re-sample until the drift closes.

4. **Seal the reflection**
   - Record corrections, residual risk, and owners responsible for follow-up. Link supporting artifacts.
   - Announce mirror status in the primary channel with next actions (proceed, hold, or revert) and who carries them.

## Safeguards
- Abort if automation labels appear on drafts or cross-repo PRs; remove labels and reset eligibility before continuing.
- Two-person review to approve corrections that touch guarded workflows or chamber entry/exit gates.
- Keep rollback bundles ready for each impacted chamber and engine before applying any change observed in the mirror.

## Completion Signals
- `mirror-shell-<date>.log` contains the scope, telemetry snapshots, drift notes, corrections, and owner sign-offs.
- Observability dashboards match expected bounds with guardrails and automation eligibility clearly noted.
- Primary channel acknowledgment confirms whether to proceed to the next harmonic/seal or to hold for further stabilization.
