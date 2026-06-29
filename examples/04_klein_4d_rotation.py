"""04_klein_4d_rotation.py — rotate the Klein bottle through the 4th dimension.

The Klein bottle embeds cleanly in R^4. Any 3D shadow self-intersects, but the
self-intersection is a projection artifact: rotate the surface in 4D and the
crossing circle slides around and (instantaneously) vanishes. This is the most
honest way to "see" a Klein bottle.

We rotate in the x–w plane and project orthographically by dropping w.

Usage:
    python 04_klein_4d_rotation.py             # animated window
    python 04_klein_4d_rotation.py out.gif     # save a gif (needs pillow)
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from surfaces import klein_4d, grid, TAU


def rotate_xw(x, y, z, w, angle):
    """Rotate the 4D point in the x–w plane, then project out w."""
    c, s = np.cos(angle), np.sin(angle)
    xr = x * c - w * s
    # wr = x * s + w * c   # dropped by the projection
    return xr, y, z


def main(outfile=None):
    u, v = grid([0, TAU], [0, TAU], nu=160, nv=70)
    x, y, z, w = klein_4d(u, v)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.axis("off")

    def draw(angle):
        ax.clear()
        ax.axis("off")
        xr, yr, zr = rotate_xw(x, y, z, w, angle)
        ax.plot_surface(xr, yr, zr, cmap="twilight", rstride=2, cstride=2,
                        linewidth=0, antialiased=True, alpha=0.9)
        r = 3.2
        ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r)
        ax.set_title(f"4D rotation: θ = {np.degrees(angle):5.0f}°")

    frames = np.linspace(0, TAU, 90)
    anim = animation.FuncAnimation(
        fig, lambda i: draw(frames[i]), frames=len(frames), interval=60
    )

    if outfile:
        anim.save(outfile, writer="pillow", fps=18)
        print(f"saved {outfile}")
    else:
        plt.show()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
