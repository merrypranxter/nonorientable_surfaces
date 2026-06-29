"""07_texture_tracking.py — carry a chiral arrow around the Möbius strip.

The repo's one rule: *always show the orientation reversal.* Here it is in the
plainest possible form. Place a small right-handed frame (an arrow plus a
perpendicular barb) on the strip and slide it once around the centerline. The
frame returns to the same spot flipped into a left-handed frame.

We transport the surface tangent/normal frame and draw the little 2D arrow it
induces. Watch the barb swap sides.

Usage:
    python 07_texture_tracking.py            # animated window
    python 07_texture_tracking.py out.gif    # save a gif (needs pillow)
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from surfaces import mobius, TAU


def frame_at(u, eps=1e-5):
    """Right-handed frame (T, B, N) on the centerline at parameter u.

    T = along-loop tangent, N = surface normal, B = N × T (across the band).
    Transported continuously these stay a consistent handedness locally, but
    globally B and N return reversed — that's the reversal we visualize.
    """
    def r(uu, vv):
        return np.array(mobius(uu, vv))

    T = (r(u + eps, 0) - r(u - eps, 0)) / (2 * eps)
    R_v = (r(u, eps) - r(u, -eps)) / (2 * eps)
    N = np.cross(T, R_v)
    T /= np.linalg.norm(T)
    N /= np.linalg.norm(N)
    B = np.cross(N, T)
    B /= np.linalg.norm(B)
    return T, B, N


def main(outfile=None):
    # full surface for context
    uu = np.linspace(0, TAU, 240)
    vv = np.linspace(-1, 1, 16)
    U, V = np.meshgrid(uu, vv)
    X, Y, Z = mobius(U, V)

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    # continuously transported frames around the loop
    us = np.linspace(0, 2 * TAU, 240)   # twice around to show the closure
    prevN = None
    Ts, Bs, Ns, Ps = [], [], [], []
    for u in us:
        T, B, N = frame_at(u % TAU)
        if prevN is not None and np.dot(N, prevN) < 0:
            N, B = -N, -B           # keep transport continuous
        prevN = N
        Ts.append(T); Bs.append(B); Ns.append(N)
        Ps.append(np.array(mobius(u % TAU, 0.0)))
    Ts, Bs, Ns, Ps = map(np.array, (Ts, Bs, Ns, Ps))

    def draw(i):
        ax.clear()
        ax.axis("off")
        ax.plot_surface(X, Y, Z, color="0.8", alpha=0.18, linewidth=0, shade=False)
        p = Ps[i]
        # the arrow (T) and its right-hand barb (B): a chiral mark
        ax.quiver(*p, *Ts[i], length=0.6, color="#4ea1ff", lw=2)
        ax.quiver(*p, *Bs[i], length=0.35, color="#ff5d73", lw=2)
        loops = "1st pass" if i < len(us) // 2 else "2nd pass (note the flip)"
        ax.set_title(f"texture tracking — {loops}")
        ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-1.2, 1.2)

    anim = animation.FuncAnimation(fig, draw, frames=len(us), interval=40)

    if outfile:
        anim.save(outfile, writer="pillow", fps=24)
        print(f"saved {outfile}")
    else:
        plt.show()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
