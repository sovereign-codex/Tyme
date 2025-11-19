# AVOT-Fabricator Diagrams

## Fabrication Dataflow
```mermaid
graph TD
  PulseSync[Pulse Sync State] -->|resonance| Hive[Hive Core Sync]
  Hive -->|roles| Curious[Curious Agents]
  Curious -->|memory deltas| Lattice[Quantum Intelligence Lattice]
  Lattice -->|concept threads| Quill[Quill Engine Expansion]
  Quill -->|patterns| Fabricator[AVOT-Fabricator]
  Fabricator -->|scrolls + diagrams + prototypes| Manifest[/manifest/avot_fabricator/]
```

## Artifact Assembly Loop
```mermaid
sequenceDiagram
  participant AVOT as AVOT-Fabricator
  participant Archivist as AVOT-Archivist
  participant Curious as Curious Agents
  participant Manifest as /manifest/avot_fabricator

  AVOT->>Archivist: Request latest timeline lineage
  Archivist-->>AVOT: Deliver codex + lattice references
  AVOT->>Curious: Share curiosity breath cadence and memory delta targets
  Curious-->>AVOT: Return curiosity deltas ready for synthesis
  AVOT->>Manifest: Emit scrolls, diagrams, prototype code, and architecture deltas
  Manifest-->>AVOT: Confirm storage markers for downstream agents
```

## Storage Layout
```text
manifest/
  avot_fabricator/
    scrolls.md
    diagrams.md
    prototype.py
    architecture.md
```
