# Rocket Dodge 3D — Rebuilt

A from-scratch Three.js browser game.

## Play locally

From this folder, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\serve_v2.ps1
```

Then open `http://localhost:8766/`.

## Controls

- **WASD / Arrow keys** — move
- **Space** — fire (a quick tap also fires)
- **R** — restart
- **● REC** — record a WebM clip of the game canvas

## Rebuild notes

- Rocket model built in Blender 5.2 (`build_rocket_clean.py`), exported as `rocket.glb`.
- glTF is Y-up, so the rocket is rotated `-90°` around X in code to point forward (`-Z`).
- Hitboxes are real `THREE.Box3` boxes fitted to the rendered object dimensions with `setFromObject`.
- No health bars are rendered, so they cannot count as hitbox space.
- Score is always an integer (`Math.floor`).
- Three.js is vendored locally so the game does not depend on a CDN at runtime.

## Publish

Pushing to `main` runs `.github/workflows/deploy.yml` and publishes to GitHub Pages.
