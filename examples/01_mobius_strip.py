"""01_mobius_strip.py — render a Möbius strip and prove it has one edge.

Two things happen here:
  1. We plot the strip, coloured by the *side* of the band (sign of v), so you
     can watch the two colours meet — there is really only one side.
  2. We trace the single boundary curve. A cylinder has two boundary circles;
     the Möbius strip has one. We walk u from 0 to 4π along the edge v = +1 and
     show it closes only after going around *twice*.

Usage:
    python 01_mobius_strip.py            # interactive window
    python 01_mobius_strip.py out.png    # save to file
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from surfaces import mobius, grid, TAU


def main(outfile=None):
    u, v = grid([0, TAU], [-1, 1], nu=300, nv=30)
    x, y, z = mobius(u, v)

    fig = plt.figure(figsize=(10, 5))

    # --- panel 1: the surface, coloured by side -----------------------------
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    facecolors = cm.coolwarm((v - v.min()) / (v.max() - v.min()))
    ax1.plot_surface(x, y, z, facecolors=facecolors, rstride=1, cstride=1,
                     linewidth=0, antialiased=True, shade=False)
    ax1.set_title("One side: the two colours merge")
    _equal_box(ax1, x, y, z)
    ax1.axis("off")

    # --- panel 2: the single edge -------------------------------------------
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    # Surface, faint, for context.
    ax2.plot_surface(x, y, z, color="0.8", alpha=0.15, linewidth=0, shade=False)
    # Walk the edge v = +1 around TWICE; it only closes after 4π.
    ue = np.linspace(0, 2 * TAU, 800)
    ex, ey, ez = mobius(ue, np.ones_like(ue))
    ax2.plot(ex, ey, ez, color="#ff5d73", lw=2.5)
    ax2.set_title("One edge: closes only after going around twice")
    _equal_box(ax2, x, y, z)
    ax2.axis("off")

    fig.suptitle("Möbius strip — one side, one edge", fontsize=13)
    fig.tight_layout()
    _show(fig, outfile)


def _equal_box(ax, x, y, z):
    """matplotlib 3D has no set_aspect('equal'); fake it with cube bounds."""
    xs = [x.min(), x.max()]
    ys = [y.min(), y.max()]
    zs = [z.min(), z.max()]
    r = max(xs[1] - xs[0], ys[1] - ys[0], zs[1] - zs[0]) / 2
    cx, cy, cz = np.mean(xs), np.mean(ys), np.mean(zs)
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
