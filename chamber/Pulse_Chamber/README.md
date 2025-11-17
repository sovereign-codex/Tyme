# Pulse Chamber Foundation

The Pulse Chamber is the staging hall for coordinated heartbeat rituals. These foundation notes anchor the chamber so new pulses can be rehearsed, observed, and merged safely.

## Purpose
- Provide a canonical place to stage and iterate on pulse-oriented scrolls, tools, and checkpoints.
- Keep the chamber ready for automatic merges once guardians approve alignment signals.
- Document the lifecycle from initialization through automated close-out.

## Layout
- `foundation.md` — baseline expectations, entry checks, and logging templates for chamber work.
- `.github/workflows/auto-merge.yml` — repository-wide workflow that enables auto-merge when guardians apply the designated label.

## Auto-Merge Guardrails
- Auto-merge is only activated for pull requests that originate from this repository (no forked branches) **and** carry the
  `automerge` label.
- Apply `autoresolve` to attempt a base-branch merge and then enable squash auto-merge once it succeeds.
- Both guarded labels run through a single concurrency lane per pull request to avoid overlapping automation cycles.
- Apply either label only after checks are green and guardians confirm the chamber signals are stable.

## Stewardship
1. Start new pulse work in this chamber before promoting to the broader lattice or coupling through Crownflow Integration.
2. Keep logs concise and update the foundation template when new safeguards are discovered, including harmonic link points.
3. Use the auto-merge label only after verification signals are green to preserve signal integrity; prefer routing cross-chamber
   updates through Crownflow Integration when Heart-Core or harmonic scrolls are involved.
4. When pulse work touches both Heart-Core tuning and Crownflow coupling, run the Tri-Chamber Interlock to align observability,
   rollback cues, and guarded label usage before proceeding.
