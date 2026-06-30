"""02_klein_bottle.py — the two faces of the Klein bottle.

Side by side:
  - the classic 'bottle' immersion (the glass shape everyone pictures), and
  - the figure-8 immersion (the 'Klein bagel').

Both are immersions in R^3: a true Klein bottle cannot live in 3-space without
passing through itself. The self-intersection is the price of the projection,
not a property of the surface.

Usage:
    python 02_klein_bottle.py [out.png]
"""

import sys

import numpy as np
import matplotlib.pyplot as plt

from surfaces import klein_classic, klein_figure8, grid, TAU


def main(outfile=None):
    fig = plt.figure(figsize=(11, 5))

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    u, v = grid([0, TAU], [0, TAU], nu=260, nv=80)
    x, y, z = klein_classic(u, v)
    ax1.plot_surface(x, y, z, cmap="viridis", rstride=2, cstride=2,
                     linewidth=0, antialiased=True, alpha=0.92)
    ax1.set_title("Classic immersion")
    _equal_box(ax1, x, y, z)
    ax1.axis("off")

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    u2, v2 = grid([0, TAU], [0, TAU], nu=200, nv=120)
    x2, y2, z2 = klein_figure8(u2, v2)
    ax2.plot_surface(x2, y2, z2, cmap="plasma", rstride=2, cstride=2,
                     linewidth=0, antialiased=True, alpha=0.92)
    ax2.set_title("Figure-8 immersion")
    _equal_box(ax2, x2, y2, z2)
    ax2.axis("off")

    fig.suptitle("Klein bottle — no boundary, no inside (χ = 0)", fontsize=13)
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
