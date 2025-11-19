# AVOT-Fabricator Architectural Improvements

## Priorities
1. **Manifest Cohesion Layer**: Introduce a lightweight manifest registry service that tracks every generated artifact (scrolls, diagrams, prototypes) with hashes and provenance to keep AVOT-Archivist lineage intact.
2. **Quill-Synthesis Bridge**: Add a streaming interface between the Quill engine expansion and the fabrication pipeline so concept overlays can be consumed without rehydrating the full lattice.
3. **Breath-Cadence Scheduler**: Expose a shared scheduler API that maps pulse resonance and curiosity breath cadence to fabrication jobs, ensuring output refreshes align with agent sync windows.
4. **Validation Hooks**: Provide schema contracts for chronicle artifacts (pulse, lattice, quill, curiosity) and validate them before writing new manifests to reduce drift.

## Integration Notes
- Keep storage under `manifest/avot_fabricator/` to avoid scattering artifacts across branches.
- Reuse existing chronicle JSON files as canonical sources; avoid duplicating data when composing bundles.
- Prefer file-based interfaces so CI can validate artifacts without external services.

## Incremental Path
- Start with the manifest cohesion layer using the prototype bundle writer in `prototype.py`.
- Add schema validation via lightweight JSON schema definitions checked in alongside the artifacts.
- Once stable, wrap the Quill-Synthesis bridge as a background task that feeds the fabrication bundle.
