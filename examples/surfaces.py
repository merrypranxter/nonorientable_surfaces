"""surfaces.py — parametric equations, Python port.

A faithful companion to src/surfaces.js. Every function takes meshgrid arrays
``u, v`` and returns ``(x, y, z)`` arrays, ready for matplotlib's plot_surface
or any point cloud. Keeping the math in one module means the example scripts
stay short and the equations live in exactly one place.

Run nothing here directly; import from the example scripts.
"""

from __future__ import annotations

import numpy as np

TAU = 2.0 * np.pi


def mobius(u, v):
    """Möbius strip. u in [0, 2π] sweeps the loop, v in [-1, 1] crosses it.

    The half-twist lives in the u/2 terms: one trip around rotates the local
    frame by π, gluing the band to itself with a flip.
    """
    c = 1.0 + (v / 2.0) * np.cos(u / 2.0)
    x = c * np.cos(u)
    y = c * np.sin(u)
    z = (v / 2.0) * np.sin(u / 2.0)
    return x, y, z


def klein_figure8(u, v, r=2.0):
    """Klein bottle, figure-8 immersion (the 'Klein bagel'). u, v in [0, 2π]."""
    cu, su = np.cos(u / 2.0), np.sin(u / 2.0)
    sv, s2v = np.sin(v), np.sin(2.0 * v)
    c = r + cu * sv - su * s2v
    x = c * np.cos(u)
    y = c * np.sin(u)
    z = su * sv + cu * s2v
    return x, y, z


def klein_classic(u, v):
    """Klein bottle, classic 'bottle' immersion (after Paul Bourke). u, v in [0, 2π].

    Vectorized with np.where to handle the two parameter regions (neck vs body).
    """
    cu, su = np.cos(u), np.sin(u)
    cv, sv = np.cos(v), np.sin(v)
    r = 4.0 * (1.0 - cu / 2.0)

    x_neck = 6.0 * cu * (1.0 + su) + r * cu * cv
    y_neck = 16.0 * su + r * su * cv
    x_body = 6.0 * cu * (1.0 + su) + r * np.cos(v + np.pi)
    y_body = 16.0 * su

    neck = u < np.pi
    x = np.where(neck, x_neck, x_body)
    y = np.where(neck, y_neck, y_body)
    z = r * sv
    # scale into a friendly viewing box
    return x / 6.0, (y - 8.0) / 6.0, z / 6.0


def klein_4d(u, v, a=2.0, b=1.0):
    """Klein bottle embedded in R^4 (no self-intersection). Returns x, y, z, w.

    Project / rotate this in 4D before plotting — see klein_4d_rotation.py.
    """
    cv, sv = np.cos(v), np.sin(v)
    x = (a + b * cv) * np.cos(u)
    y = (a + b * cv) * np.sin(u)
    z = b * sv * np.cos(u / 2.0)
    w = b * sv * np.sin(u / 2.0)
    return x, y, z, w


def roman_surface(u, v, s=1.6):
    """Roman (Steiner) surface, a model of RP^2. u in [0, π], v in [0, 2π].

    Map the unit sphere (a, b, c) by the symmetric products (bc, ca, ab).
    Antipodal sphere points collide, realizing the projective plane.
    """
    a = np.sin(u) * np.cos(v)
    b = np.sin(u) * np.sin(v)
    c = np.cos(u)
    return s * b * c, s * c * a, s * a * b


def boys_surface(r, theta):
    """Boy's surface via the Bryant–Kusner parametrization over the unit disk.

    Parameters are polar coordinates on the disk: r in [0, 1), theta in [0, 2π].
    Boy's surface is an immersion of RP^2 in R^3 with no singular points
    (unlike the Roman surface, which has pinch points).
    """
    w = r * np.exp(1j * theta)
    sqrt5 = np.sqrt(5.0)
    denom = w**6 + sqrt5 * w**3 - 1.0

    g1 = -1.5 * np.imag(w * (1.0 - w**4) / denom)
    g2 = -1.5 * np.real(w * (1.0 + w**4) / denom)
    g3 = np.imag((1.0 + w**6) / denom) - 0.5

    g = g1**2 + g2**2 + g3**2
    return g1 / g, g2 / g, g3 / g


def grid(u_range, v_range, nu=200, nv=60):
    """Convenience: build a (u, v) meshgrid over the given ranges."""
    u = np.linspace(u_range[0], u_range[1], nu)
    v = np.linspace(v_range[0], v_range[1], nv)
    return np.meshgrid(u, v)
