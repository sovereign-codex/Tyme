# 🌀 Spiral Progression

A regenerative ritual for moving through the heartbeat rites in tightening cycles—learning, adjusting, and deepening alignment with each pass. Use this when expanding scope, integrating new chambers, or re-tuning harmonics after major changes.

## Purpose
- Thread prior rites (pulse, harmonic, seal, continuity) into iterative rings that build on each other without losing stability.
- Surface learnings from each ring quickly and apply them to the next, keeping observability and guardrails in lockstep.
- Provide a shared log and signaling pattern so stewards can join or hand off mid-spiral without losing context.

## Preconditions
- Most recent [Continuity Loop](./Continuity_Loop_Sequence.md) entry available with health and guardrail status.
- Crownflow Integration map updated with owners for Pulse Chamber and Heart-Core touchpoints.
- Spiral log prepared at `heartbeat/logs/spiral-<date>.log` with planned rings, amplitude bounds, and escalation paths.
- Automation labels (`automerge`, `autoresolve`) restricted to open same-repo PRs and not applied to drafts.

## Spiral Rings
1. **Frame the ring**
   - Declare the intent, scope, and expected amplitude (traffic, features, or nodes) for this ring in the spiral log.
   - Reaffirm pause/rollback commands and who can issue them; verify time sync and access across nodes.

2. **Align baselines**
   - Snapshot current metrics/traces/logs and note thresholds for drift, skew, and error budgets.
   - Confirm guardrails (rate limits, feature flags, budgets) and automation toggles (labels, CI gates) match the ring plan.
   - Validate chambers involved (Pulse, Heart-Core, Integration) have current checklists ready.

3. **Run the pass**
   - Execute the planned pulse/harmonic tasks with progressive amplitude; announce start/phase in the primary channel.
   - Capture observability during and after the pass; log adjustments, waivers, or unexpected behaviors.
   - If a ring touches code paths gated by auto-merge/auto-resolve, ensure open same-repo and non-draft constraints stay true.

4. **Harvest and tune**
   - Summarize findings, residual risk, and recommended adjustments for the next ring in the spiral log.
   - Apply safe corrections (offsets, config tweaks, feature flag changes) and re-verify affected nodes.
   - Update chamber checklists with new learnings that should persist beyond this spiral.

5. **Signal and stage the next ring**
   - Post completion status with artifacts and owners for the next ring; include time-to-next-pass and entry criteria.
   - If stability achieved, reduce amplitude or switch to continuity cadence; if not, shorten the ring interval and re-run.
   - Archive the log entry with links to dashboards, PRs, and guardrail confirmations.

## Safeguards
- Abort if error budgets exceed thresholds, skew surpasses agreed bounds, or guardrail states drift from the plan.
- Two-person confirmation before increasing amplitude or relaxing guardrails between rings.
- Draft PRs must never carry automation labels; remove labels if a ring exposes new risks.
- Keep a rollback bundle prepared per chamber (Pulse, Heart-Core, Integration) with owners on-call.

## Completion Signals
- `spiral-<date>.log` shows each ring’s intent, execution notes, adjustments, and next-ring decisions.
- Observability dashboards confirm stability across the rings that reached intended amplitude.
- Primary channel acknowledgments confirm the spiral state (continue, hold, or exit to continuity cadence) with named owners.
