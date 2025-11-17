# Tyme-Core-Dev

Tyme-Core-Dev is the working branch for building the central Tyme Core runtime and documentation hub. Use this space to prototype modules, document the lattice, and prepare artifacts that will later feed the main Crown of Tyme manifest.

## What's inside
- `index.html` — landing page for the developer node.
- `notes/` — scratchpad for design docs and module sketches (add as needed).
- `manifests/` — draft manifests for emerging components before promotion to the root manifest.

## Quickstart
1) Serve the directory locally to preview the portal:
   ```sh
   python -m http.server 8000
   ```
   Then open http://localhost:8000/branches/tyme-core-dev/index.html.
2) Capture design notes in `notes/` and sync updates into `manifests/` as the Core stabilizes.
3) When stable, promote modules into `manifest/tyme_manifest.json` at the repository root.

## Next steps
- Sketch the Tyme Core runtime interfaces (AVOT orchestration, manifest loader, and doc generator).
- Define contracts for plugging in AVOT modules and Scroll renderers.
- Align naming and styling with the Crown of Tyme sovereign language.
