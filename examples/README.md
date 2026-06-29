# Examples

Standalone, dependency-light Python scripts. They share one module of equations
(`surfaces.py`) so the math lives in exactly one place — the same single source
of truth as `src/surfaces.js` on the web side.

```bash
pip install -r examples/requirements.txt
```

Each script opens an interactive window, or saves a file if you pass a path:

```bash
python examples/01_mobius_strip.py                 # window
python examples/01_mobius_strip.py mobius.png      # save PNG
python examples/04_klein_4d_rotation.py out.gif    # save GIF (needs pillow)
```

| Script | What it shows |
|---|---|
| `surfaces.py` | Shared parametric equations (imported, not run). |
| `01_mobius_strip.py` | One side (colours merge) + one edge (closes after 4π). |
| `02_klein_bottle.py` | Classic vs figure-8 immersions, side by side. |
| `03_rp2_roman_and_boy.py` | Two RP² immersions: Roman (pinched) vs Boy's (smooth). |
| `04_klein_4d_rotation.py` | Rotate the true Klein bottle through R⁴; the crossing sweeps. |
| `05_cut_and_fold.py` | Animate rectangle → half-twist → glued Möbius strip. |
| `06_nonorientability_proof.py` | Numerically transport the normal; it returns **negated**. |
| `07_texture_tracking.py` | Carry a chiral frame around; the barb flips. |

`06_nonorientability_proof.py` prints to the terminal and only draws if you pass
an output path — handy as a quick sanity check:

```
$ python examples/06_nonorientability_proof.py
Möbius strip — non-orientability check
  n(0)·n(2π) = -1.0000
  => the normal REVERSED after one loop. NON-ORIENTABLE. ✓
```
