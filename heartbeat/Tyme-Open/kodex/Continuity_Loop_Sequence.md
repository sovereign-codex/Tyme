# ♾️ Continuity Loop Sequence

A recurring ritual to sustain aligned operation over multiple cycles after the lattice is sealed. Use this to keep rhythm, detect drift early, and refresh shared context without losing momentum.

## Purpose
- Maintain steady-state alignment across nodes between major pulses and seals.
- Continuously observe for drift, fatigue, or resource depletion and correct before degradation.
- Refresh agreements, ownership, and recovery handles so the lattice stays ready for the next expansion.

## Preconditions
- [Coherence Seal](./Coherence_Seal.md) completed with current guardrails and contacts logged.
- Active observability dashboards for latency, error rates, capacity, and skew accessible to all stewards.
- A continuity log prepared at `heartbeat/logs/continuity-<date>.log` with the cycle cadence and owner.

### Log Template
Use this scaffold for each loop entry so handoffs stay crisp:
```text
[time start-end] cadence=<minutes> owner=<name> nodes=<n>
health: latency=<p95>ms error=<rate> skew=<delta> capacity=<percent>
changes: <adjustments or "none">
risks: <top 1–2 items> | guardrails: <flags/budgets checked>
actions: <follow-ups, waivers, next loop time>
```

## Loop Steps
1. **Anchor the loop**
   - Record the intended cadence (e.g., every 30–60 minutes) and key health thresholds in the continuity log.
   - Reaffirm control commands: pause, rollback, and escalation paths with named responders.

2. **Run the check pass**
   - Sample metrics/traces/logs for each node plus aggregate views; note anomalies, drift, or saturation signals.
   - Verify guardrails (rate limits, budgets, feature flags) are still applied and unchanged.
   - Capture skew readings (clock or offset) to ensure time-based signals remain trustworthy.

3. **Stabilize and adjust**
   - If drift detected, apply offsets, reduce load, or remove an outlier node; timestamp each adjustment.
   - Trigger a light self-test (synthetic check or low-risk transaction) to confirm recovery after adjustments.
   - Re-check any node you touched to verify the next loop will start from a healthy baseline.

4. **Renew agreements**
   - Confirm on-call coverage, contact paths, and decision owners; rotate duties if fatigue risk is noted.
   - Capture any temporary waivers or exceptions with expiry times in the log.
   - Restate the next loop time and who will anchor it to avoid gaps during handoffs.

5. **Signal and archive**
   - Post a brief loop update: status, notable adjustments, risks, and next cycle time.
   - Append artifacts (dash snapshots, traces, command outputs) to the log for continuity across shifts.
   - Tag any follow-ups that must occur before the next major rite (e.g., harmonic or seal refresh).

## Safeguards
- Abort criteria defined for accumulated error budgets, rising skew, or repeated guardrail breaks.
- Dual confirmation required before relaxing guardrails or extending the cadence beyond agreed bounds.
- Manual pause and rollback commands validated at least once per shift with a dry-run record in the log.
- If two consecutive loops require corrective action, escalate and consider shortening the cadence until stable.

## Completion Signals
- `continuity-<date>.log` shows cadence, observations per cycle, adjustments taken, and handoff notes.
- Observability dashboards reflect stable metrics within thresholds across consecutive loops.
- Primary channel contains the latest loop update with acknowledgment from on-call owners.
