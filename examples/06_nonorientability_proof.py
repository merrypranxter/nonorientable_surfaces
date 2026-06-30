"""06_nonorientability_proof.py — a numerical proof that the Möbius strip is non-orientable.

Orientability has a crisp test: can you choose a continuous unit normal over the
whole surface? Walk the centerline of the Möbius strip (v = 0) and carry the
surface normal with you. You return to the *same point* with the *opposite*
normal. No continuous choice exists — hence non-orientable.

We compute the normal n(u) = (r_u × r_v) / |r_u × r_v| numerically along the
loop, transport it continuously (forbidding sudden sign flips between
neighbouring samples), and check n(2π) against n(0).

This script prints a result and, if asked, draws the normal field.

Usage:
    python 06_nonorientability_proof.py [out.png]
"""

import sys

import numpy as np
import matplotlib.pyplot as plt

from surfaces import mobius, TAU


def normal_at(u, v, eps=1e-5):
    """Numerical unit normal n = r_u × r_v / |...| at parameter (u, v)."""
    def r(uu, vv):
        return np.array(mobius(uu, vv))

    r_u = (r(u + eps, v) - r(u - eps, v)) / (2 * eps)
    r_v = (r(u, v + eps) - r(u, v - eps)) / (2 * eps)
    n = np.cross(r_u, r_v)
    return n / np.linalg.norm(n)


def transported_normals(n_samples=400):
    """Sample n(u) along v=0 and transport continuously around the loop."""
    us = np.linspace(0, TAU, n_samples)
    normals = []
    prev = None
    for u in us:
        n = normal_at(u, 0.0)
        # continuous transport: keep the sign that agrees with the previous step
        if prev is not None and np.dot(n, prev) < 0:
            n = -n
        normals.append(n)
        prev = n
    return us, np.array(normals)


def main(outfile=None):
    us, normals = transported_normals()
    n0 = normals[0]
    n_end = normals[-1]
    dot = float(np.dot(n0, n_end))

    print("Möbius strip — non-orientability check")
    print("-" * 42)
    print(f"  n(0)   = {np.round(n0, 4)}")
    print(f"  n(2π)  = {np.round(n_end, 4)}")
    print(f"  n(0)·n(2π) = {dot:+.4f}")
    if dot < -0.9:
        print("  => the normal REVERSED after one loop. NON-ORIENTABLE. ✓")
    else:
        print("  => normal preserved (orientable) — unexpected for a Möbius strip!")

    # Contrast: a cylinder (no twist) returns the SAME normal.
    print()
    print("Contrast — cylinder (no half-twist):")
    cyl_dot = _cylinder_check()
    print(f"  n(0)·n(2π) = {cyl_dot:+.4f}  => orientable ✓")

    if outfile is not None:
        _plot(us, normals, outfile)


def _cylinder_check(n_samples=400):
    def cyl_normal(u, eps=1e-5):
        def r(uu, vv):
            return np.array([np.cos(uu), np.sin(uu), vv])
        r_u = (r(u + eps, 0) - r(u - eps, 0)) / (2 * eps)
        r_v = (r(u, eps) - r(u, -eps)) / (2 * eps)
        n = np.cross(r_u, r_v)
        return n / np.linalg.norm(n)

    us = np.linspace(0, TAU, n_samples)
    prev, first = None, None
    for u in us:
        n = cyl_normal(u)
        if prev is not None and np.dot(n, prev) < 0:
            n = -n
        if first is None:
            first = n
        prev = n
    return float(np.dot(first, prev))


def _plot(us, normals, outfile):
    x, y, z = mobius(us, np.zeros_like(us))
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, z, color="0.4", lw=1.5)
    step = max(1, len(us) // 60)
    ax.quiver(x[::step], y[::step], z[::step],
              normals[::step, 0], normals[::step, 1], normals[::step, 2],
              length=0.35, color="#4ea1ff", normalize=True)
    ax.set_title("Transported normal flips after one loop")
    ax.axis("off")
    fig.savefig(outfile, dpi=130, bbox_inches="tight")
    print(f"\nsaved {outfile}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
