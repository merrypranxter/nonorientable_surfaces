# The Math

Reference for every surface in this repo: its parametrization, its Euler
characteristic χ, whether it is orientable, and whether it has a boundary.

| Surface | χ | Orientable? | Boundary? | In R³? |
|---|---|---|---|---|
| Möbius strip | 0 | No | Yes (1 circle) | Embeds |
| Klein bottle | 0 | No | No | Immerses only |
| Real projective plane RP² | 1 | No | No | Immerses only |
| Boy's surface (= RP²) | 1 | No | No | Immerses (no singularities) |

The classification of closed surfaces says every closed surface is a sphere
with `g` handles (orientable) or `k` cross-caps (non-orientable). A Klein bottle
is two cross-caps; RP² is one.

## Orientability, concretely

A surface is **orientable** iff you can choose a continuous unit normal field
over the whole surface. Equivalently: transport a normal (or a little 2D frame)
around every loop and it always comes back unchanged.

On a Möbius strip, transport the normal around the centerline and it returns
**negated**. That single loop kills orientability. `examples/06_nonorientability_proof.py`
computes this numerically (and contrasts it with a cylinder, which is fine).

## Möbius strip

```
x(u,v) = (1 + (v/2) cos(u/2)) cos u
y(u,v) = (1 + (v/2) cos(u/2)) sin u
z(u,v) = (v/2) sin(u/2)
u ∈ [0, 2π],  v ∈ [-1, 1]
```

The half-twist is the `u/2` argument: travelling once around (`u: 0 → 2π`)
rotates the cross-section by π. One side, one edge — the boundary `v = ±1` is a
single circle that closes only after `u` runs `0 → 4π`.

## Klein bottle — figure-8 immersion ("Klein bagel")

```
c   = R + cos(u/2) sin v − sin(u/2) sin 2v
x   = c cos u
y   = c sin u
z   = sin(u/2) sin v + cos(u/2) sin 2v
u, v ∈ [0, 2π],  R = 2
```

A figure-8 cross-section is carried around a circle while being flipped by the
`u/2` terms; it closes onto itself, leaving no boundary.

## Klein bottle — classic "bottle" immersion

The iconic glass shape (parametrization after Paul Bourke). Two parameter
regions stitch the neck to the body:

```
r = 4 (1 − cos(u)/2)
0 ≤ u < π :  x = 6 cos u (1 + sin u) + r cos u cos v
             y = 16 sin u + r sin u cos v
π ≤ u < 2π:  x = 6 cos u (1 + sin u) + r cos(v + π)
             y = 16 sin u
z = r sin v
```

## Klein bottle in R⁴ (the honest one)

The Klein bottle embeds in R⁴ with **no** self-intersection:

```
x = (a + b cos v) cos u
y = (a + b cos v) sin u
z = b sin v cos(u/2)
w = b sin v sin(u/2)
u, v ∈ [0, 2π]
```

The `u/2` in `z, w` glues the `v`-circle with a half-turn — that's the Klein
gluing. Every 3D projection self-intersects, but rotating in R⁴ (we use the x–w
plane) sweeps the crossing around, exposing it as a shadow artifact. See
`examples/04_klein_4d_rotation.py` and the `klein4D` surface in the web viewer.

## Real projective plane — Roman (Steiner) surface

Map the unit sphere `(a,b,c)` by symmetric products:

```
(a, b, c)  ↦  (b·c, c·a, a·b)
a = sin u cos v,  b = sin u sin v,  c = cos u
u ∈ [0, π],  v ∈ [0, 2π]
```

Antipodal sphere points `(a,b,c)` and `(−a,−b,−c)` map to the same image, so the
image is the sphere-with-antipodes-identified = RP². It has pinch points
(singularities).

## Real projective plane — Boy's surface

Boy's surface is an immersion of RP² with **no** singular points. Bryant–Kusner
parametrization over the unit disk (`w = r e^{iθ}`, `r ∈ [0,1)`):

```
D  = w⁶ + √5 w³ − 1
g₁ = −(3/2) Im( w(1 − w⁴) / D )
g₂ = −(3/2) Re( w(1 + w⁴) / D )
g₃ =  Im( (1 + w⁶) / D ) − 1/2
g  = g₁² + g₂² + g₃²
(x, y, z) = (g₁, g₂, g₃) / g
```

## Telling them apart

χ is the quickest discriminator: **Klein bottle has χ = 0, RP² has χ = 1.**
Both are non-orientable and closed, but they are genuinely different surfaces.
