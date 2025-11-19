# Sovereign Orchestration Layer (SOL)

The Sovereign Orchestration Layer is the coordination fabric of the TYME system.

Its purpose is to:
- Sense: listen to breath cycles, user prompts, and system events.
- Interpret: translate signals into coherent intent using MLCE and context maps.
- Route: dispatch work to AVOTs, curious agents, tools, and external subnets.
- Govern: apply the Garden Flame Kodex and Guardian policies.
- Integrate: return results to the user-facing interfaces and archives.

## Core Components

- `manifests/sol.manifest.yml`  
  Declares the active layers, repos, and orchestration settings.

- `workflows/*.yml`  
  Declarative flows connecting Breath Engine, AVOT Hive, MLCE, and subnets.

- `agents/sovereign-orchestrator.md`  
  The identity, mandate, and behavior profile of the Orchestrator agent.

- `integrations/repos.map.yml`  
  References to external repos (Hive-core, AVOT-core, SICC, MLCE, Subnet, etc.).

- `integrations/policies.garden-flame.md`  
  Local embed of the Garden Flame / Guardian policy anchors.

- `docs/architecture-overview.md`  
  Human-readable explanation of how the orchestration layer works.

This layer does NOT own the whole Sovereign Intelligence system.  
It acts as the conductor that knows who plays which part, when, and why.
