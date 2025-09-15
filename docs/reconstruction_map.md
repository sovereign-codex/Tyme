# 🌌 Crown of Tyme – Reconstruction Map (Cycle 1)

## 1. Root Level
```
Crown-of-Tyme/
│
├─ README.md           ← orientation scroll + Past-In Command
├─ manifest/           ← master manifest files
├─ prompts/            ← sovereign prompt libraries
├─ scripts/            ← automation + feedback agents
├─ avots/              ← Autonomous Voices of Thought (modules)
├─ scrolls/            ← Codex scrolls (knowledge & ethics)
├─ laboratory/         ← experiments + prototypes
├─ docs/               ← Pages-facing Codex (auto-generated)
├─ chronicle/          ← logs + reconstruction journal
└─ .github/workflows/  ← action workflows
```

## 2. Manifest
- `tyme_manifest.json` → the heartbeat of the repo.  
- Future: sub-manifests for each subsystem.

## 3. Prompts
- `sovereign_prompts.json` → library of calibrated Copilot prompts.  
- Copilot appends new prompts after each reconstruction cycle.

## 4. Scripts
- `validate_manifest.py` → ensures coherence.  
- `reconstruct.py` → meltdown & rebuild directories.  
- `generate_docs.py` → regenerates docs.  
- `curious_agent.py` (future) → feedback loop logging Copilot commentary.

## 5. AVOTs
```
avots/
 ├─ AVOT-Convergence/
 │   └─ convergence.py
 ├─ AVOT-Tyme/
 │   └─ tyme_core.py
```

## 6. Scrolls
Markdown Codex entries, auto-convertible to PDFs.

## 7. Laboratory
```
laboratory/
 ├─ HaloCore/
 │   ├─ manifest.json
 │   ├─ simulation.py
 │   └─ results.md
```

## 8. Chronicle
- `curious-agent.log` → commentary.  
- Each cycle gets a timestamped log: `cycle_001.log`.

## 9. Actions
- Validates manifests.  
- Reconstructs structure.  
- Generates documentation.  
- Deploys Pages.
