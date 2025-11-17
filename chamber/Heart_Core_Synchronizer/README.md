# Heart-Core Synchronizer Foundation

The Heart-Core Synchronizer keeps the lattice's core rhythm aligned as new nodes join or amplitude increases. Use this space to design, test, and tune synchronization runs before promoting them across the lattice.

## Purpose
- Provide a dedicated staging ground for Heart-Core synchronization and retuning work.
- Keep observability and rollback plans attached to every synchronization attempt.
- Maintain auto-merge readiness so approved updates can flow without friction when guardians apply the right labels.

## Layout
- `foundation.md` — checklist and logging template for initializing or refreshing the Heart-Core Synchronizer.
- `.github/workflows/auto-merge.yml` — shared auto-merge/auto-resolve guardrails (open same-repo PRs only) that apply once guardians label a change.

## Stewardship
1. Stage new Heart-Core synchronization steps here before propagating to other chambers or coupling through Crownflow Integration.
2. Attach telemetry links and rollback notes to every log entry, and record which harmonic rites are affected.
3. Only apply `automerge` or `autoresolve` after guardians verify signals are green and the open same-repo restriction is satisfied; route multi-chamber updates through Crownflow Integration so the guarded workflow context is clear.
4. If synchronization work also touches Pulse Chamber rehearsals and Crownflow coupling, activate the Tri-Chamber Interlock to keep guardrails, observability, and label usage synchronized.
