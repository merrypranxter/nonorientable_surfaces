# nonorientable_surfaces

> Möbius strips, Klein bottles, and surfaces that have no "outside."

## What This Is

Most surfaces are orientable: they have two distinct sides (inside/outside). **Non-orientable surfaces** do not. If you walk along a Möbius strip, you return to your starting point mirror-reversed.

This repo visualizes:
- **Möbius strip** — one-sided, one-edged
- **Klein bottle** — no inside or outside, no edges
- **Real projective plane** — every pair of lines intersects
- **Boy's surface** — immersion of RP² in 3D (self-intersecting)

It ships two things: an **interactive WebGL viewer** (no build step) and a set of
**standalone Python examples** that each demonstrate one idea — including a
numerical *proof* of non-orientability.

## Quickstart

### Web viewer

ES modules need to be served over HTTP (not opened as a `file://`). From the repo root:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Pick a surface from the panel, then toggle **Texture tracking** and **Two-tone
sides**. Drag to orbit. The 4D Klein bottle rotates on its own.

### Python examples

```bash
pip install -r examples/requirements.txt
python examples/01_mobius_strip.py            # opens a window
python examples/06_nonorientability_proof.py  # prints the proof to the terminal
```

See [`examples/README.md`](examples/README.md) for the full list.

## Key Properties

| Surface | Euler χ | Orientable? | Boundary? |
|---------|---------|-------------|-----------|
| Möbius strip | 0 | No | Yes (1 circle) |
| Klein bottle | 0 | No | No |
| Real projective plane | 1 | No | No |
| Boy's surface | 1 | No | No (immersion) |

Full parametrizations and the χ / orientability reasoning live in
[`docs/MATH.md`](docs/MATH.md).

## Visual Approaches

### 1. Parametric Surfaces
Classic parametric equations, rendered with normal mapping. The canonical
equations live in [`src/surfaces.js`](src/surfaces.js) (web) and
[`examples/surfaces.py`](examples/surfaces.py) (Python) — one source of truth each.

### 2. Texture Tracking
Show how textures wrap "wrong" — a right-handed arrow becomes left-handed. The
orientation shader ([`shaders/orientation.frag.glsl`](shaders/orientation.frag.glsl))
mirrors a chiral glyph on back faces; `examples/07_texture_tracking.py` carries a
frame around by hand.

### 3. Cut-and-Fold
Animate the construction: rectangle → twist → glue. See
`examples/05_cut_and_fold.py`.

### 4. 4D Rotation
The Klein bottle properly lives in 4D. Rotate through the 4th dimension and the
self-intersection sweeps away. See `examples/04_klein_4d_rotation.py` and the
`Klein bottle (4D rotation)` surface in the viewer.

## Note: Klein Bottle in 3D
A true Klein bottle cannot be embedded in 3D without self-intersection. All 3D visualizations are either:
- **Immersions** (self-intersecting, like Boy's surface)
- **Truncated** (cut open to avoid intersection)
- **4D projections** (rotate through 4D, project to 3D)

## Repository Layout

```
index.html                  web viewer entry point
css/style.css               viewer styling
src/
  surfaces.js               parametric equations (source of truth, web)
  parametricGeometry.js     BufferGeometry builder + per-frame refresh
  shaders.js                the orientation shader (GLSL strings)
  glyphTexture.js           procedural chiral tracking texture
  main.js                   scene, GUI, render loop
shaders/                    reference .glsl copies of the orientation shader
examples/
  surfaces.py               parametric equations (source of truth, Python)
  01..07_*.py               standalone demonstrations
docs/MATH.md                every surface, its parametrization and invariants
.github/agents/             the "One-Sided Wanderer" custom-agent definition
```

## Related

- `kleinian_groups` — completely different! That's complex dynamics / limit sets
- `hopf_fibration` — shared fiber bundle topology

---

*There is no inside. There is no outside. There is only the surface, and it goes on forever.*
