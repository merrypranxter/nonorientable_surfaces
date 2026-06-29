"""03_rp2_roman_and_boy.py — two immersions of the real projective plane.

RP^2 is the sphere with antipodal points identified. It does not embed in R^3,
but it immerses. Two famous immersions:

  - Roman (Steiner) surface: simple algebra, but has pinch points (singular).
  - Boy's surface: no singular points at all, at the cost of uglier formulae
    (the Bryant–Kusner parametrization over the unit disk).

Both have Euler characteristic χ = 1 — the giveaway that they are RP^2 and not
a Klein bottle (χ = 0).

Usage:
    python 03_rp2_roman_and_boy.py [out.png]
"""

import sys

import numpy as np
import matplotlib.pyplot as plt

from surfaces import roman_surface, boys_surface, grid


def main(outfile=None):
    fig = plt.figure(figsize=(11, 5))

    # --- Roman surface ------------------------------------------------------
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    u, v = grid([0, np.pi], [0, 2 * np.pi], nu=160, nv=160)
    x, y, z = roman_surface(u, v)
    ax1.plot_surface(x, y, z, cmap="cividis", rstride=2, cstride=2,
                     linewidth=0, antialiased=True, alpha=0.95)
    ax1.set_title("Roman surface (pinch points)")
    _equal_box(ax1, x, y, z)
    ax1.axis("off")

    # --- Boy's surface ------------------------------------------------------
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    r = np.linspace(0.0, 1.0, 160)
    th = np.linspace(0.0, 2 * np.pi, 240)
    R, TH = np.meshgrid(r, th)
    # avoid the r=0 removable singularity by nudging off zero
    R = np.clip(R, 1e-3, 1.0)
    bx, by, bz = boys_surface(R, TH)
    ax2.plot_surface(bx, by, bz, cmap="magma", rstride=2, cstride=2,
                     linewidth=0, antialiased=True, alpha=0.95)
    ax2.set_title("Boy's surface (no singularities)")
    _equal_box(ax2, bx, by, bz)
    ax2.axis("off")

    fig.suptitle("Real projective plane RP² — χ = 1", fontsize=13)
    fig.tight_layout()
    _show(fig, outfile)


def _equal_box(ax, x, y, z):
    r = max(np.ptp(x), np.ptp(y), np.ptp(z)) / 2
    cx, cy, cz = x.mean(), y.mean(), z.mean()
    ax.set_xlim(cx - r, cx + r)
    ax.set_ylim(cy - r, cy + r)
    ax.set_zlim(cz - r, cz + r)


def _show(fig, outfile):
    if outfile:
        fig.savefig(outfile, dpi=130, bbox_inches="tight")
        print(f"saved {outfile}")
    else:
        plt.show()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
