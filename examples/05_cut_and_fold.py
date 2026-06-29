"""05_cut_and_fold.py — construct a Möbius strip by animation: rectangle → twist → glue.

Start from a flat rectangle (a strip of paper). Smoothly introduce a half-twist
and curl it into a loop. At t = 0 it's a plain band; at t = 1 the ends meet with
a half-turn and the seam glues with a flip — a Möbius strip.

The morph is a single parameter:
  - `twist`  ramps the local half-twist angle from 0 to π,
  - `curl`   bends the straight strip around into a circle.

Usage:
    python 05_cut_and_fold.py            # animated window
    python 05_cut_and_fold.py out.gif    # save a gif (needs pillow)
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

TAU = 2 * np.pi


def strip(u, v, t):
    """Interpolated band. t in [0, 1] goes flat-strip -> Möbius strip.

    u in [0, 2π] runs along the band, v in [-1, 1] across it.
    """
    curl = t                      # how far the strip wraps into a circle
    twist = t                     # how much half-twist is present

    # half-twist angle applied to the cross-section
    phi = twist * u / 2.0
    half_w = 0.5 * v
    # cross-section offset, twisting in the (radial, z) plane
    radial = half_w * np.cos(phi)
    zoff = half_w * np.sin(phi)

    # blend a straight strip (curl=0) with a circular one (curl=1)
    R = 2.0
    # straight layout along x; circular layout around the origin
    straight_x = (u - np.pi) * (R / np.pi)
    straight_y = np.zeros_like(u)

    circ_x = (R + radial) * np.cos(u)
    circ_y = (R + radial) * np.sin(u)

    x = (1 - curl) * (straight_x + radial) + curl * circ_x
    y = (1 - curl) * straight_y + curl * circ_y
    z = zoff
    return x, y, z


def main(outfile=None):
    u = np.linspace(0, TAU, 240)
    v = np.linspace(-1, 1, 16)
    U, V = np.meshgrid(u, v)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")

    def draw(t):
        ax.clear()
        ax.axis("off")
        x, y, z = strip(U, V, t)
        ax.plot_surface(x, y, z, cmap="coolwarm", rstride=1, cstride=4,
                        linewidth=0, antialiased=True, alpha=0.95)
        ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-2, 2)
        stage = "flat strip" if t < 0.05 else ("gluing…" if t < 0.97 else "Möbius strip")
        ax.set_title(f"cut & fold: {stage}")

    # ease in and hold at the end
    ts = np.concatenate([np.linspace(0, 1, 70), np.ones(15)])
    anim = animation.FuncAnimation(
        fig, lambda i: draw(ts[i]), frames=len(ts), interval=60
    )

    if outfile:
        anim.save(outfile, writer="pillow", fps=18)
        print(f"saved {outfile}")
    else:
        plt.show()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
