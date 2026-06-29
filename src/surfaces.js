// surfaces.js
// ---------------------------------------------------------------------------
// The parametric equations. This is the canonical source of truth for every
// surface in the repo; the WebGL geometry builder and the (conceptual) Python
// ports all trace back to the formulae written here.
//
// Each surface is an object:
//   {
//     id, label, blurb,
//     uRange:[a,b], vRange:[a,b],
//     uSegments, vSegments,
//     glyphRepeat: [su, sv],   // how many times the tracking-texture tiles
//     dynamic: bool,           // true => f depends on ctx.time, rebuild per frame
//     f(u, v, ctx) -> [x, y, z]
//   }
//
// Convention: f returns a plain [x,y,z] array (no THREE dependency) so the math
// can be unit-tested and ported without a renderer in the room.
// ---------------------------------------------------------------------------

const TAU = Math.PI * 2;

// --- Möbius strip ----------------------------------------------------------
// One-sided, one-edged. u sweeps the loop, v crosses the band. The half-twist
// lives in the u/2 terms: travel once around (u: 0 -> 2π) and the local frame
// has rotated by π, so the band glues to itself with a flip.
function mobius(u, v) {
  const c = 1 + (v / 2) * Math.cos(u / 2);
  return [
    c * Math.cos(u),
    c * Math.sin(u),
    (v / 2) * Math.sin(u / 2),
  ];
}

// --- Klein bottle, figure-8 immersion --------------------------------------
// The "Klein bagel." A Möbius-like cross-section (the figure 8) is carried
// around a circle while being flipped, closing up with no boundary.
function kleinFigure8(u, v) {
  const r = 2;
  const cu = Math.cos(u / 2);
  const su = Math.sin(u / 2);
  const sv = Math.sin(v);
  const s2v = Math.sin(2 * v);
  const c = r + cu * sv - su * s2v;
  return [
    c * Math.cos(u),
    c * Math.sin(u),
    su * sv + cu * s2v,
  ];
}

// --- Klein bottle, classic "bottle" immersion ------------------------------
// The iconic glass-blower's shape: the neck reaches back through the wall and
// opens into the base. Parametrization after Paul Bourke. Scaled down by /6.
function kleinClassic(u, v) {
  const cu = Math.cos(u);
  const su = Math.sin(u);
  const cv = Math.cos(v);
  const sv = Math.sin(v);
  const r = 4 * (1 - cu / 2);
  let x, y;
  if (u < Math.PI) {
    x = 6 * cu * (1 + su) + r * cu * cv;
    y = 16 * su + r * su * cv;
  } else {
    x = 6 * cu * (1 + su) + r * Math.cos(v + Math.PI);
    y = 16 * su;
  }
  const z = r * sv;
  // recenter-ish and scale into the same rough size as the others
  return [x / 6, (y - 8) / 6, z / 6];
}

// --- Klein bottle in 4D, projected to 3D -----------------------------------
// The honest Klein bottle: it embeds in R^4 with NO self-intersection. We build
// the 4D point, rotate it in the x–w plane by ctx.time, then drop w. Every 3D
// shadow self-intersects, but the intersection sweeps as we turn through 4D —
// proof that the crossings are an artifact of the projection, not the surface.
function klein4D(u, v, ctx) {
  const a = 2, b = 1;
  const cv = Math.cos(v), sv = Math.sin(v);
  // 4D embedding: a torus whose v-circle is glued with a half-turn (u/2).
  const x = (a + b * cv) * Math.cos(u);
  const y = (a + b * cv) * Math.sin(u);
  const z = b * sv * Math.cos(u / 2);
  const w = b * sv * Math.sin(u / 2);
  // rotate in the x–w plane
  const t = ctx && ctx.time ? ctx.time * 0.4 : 0;
  const ct = Math.cos(t), st = Math.sin(t);
  const xr = x * ct - w * st;
  // const wr = x * st + w * ct;  // discarded by the projection
  return [xr, y, z];
}

// --- Roman (Steiner) surface — a model of RP^2 -----------------------------
// Take the unit sphere (a,b,c) and map antipodal points together via the
// symmetric products (bc, ca, ab). Because (a,b,c) and (-a,-b,-c) land on the
// same point, this realizes the real projective plane (with pinch points).
function romanSurface(u, v) {
  // u in [0, π] (polar), v in [0, 2π] (azimuth)
  const a = Math.sin(u) * Math.cos(v);
  const b = Math.sin(u) * Math.sin(v);
  const c = Math.cos(u);
  const s = 1.6;
  return [s * b * c, s * c * a, s * a * b];
}

export const SURFACES = {
  mobius: {
    id: "mobius",
    label: "Möbius strip",
    blurb: "One side, one edge. Walk the loop and come back mirrored.",
    uRange: [0, TAU],
    vRange: [-1, 1],
    uSegments: 240,
    vSegments: 24,
    glyphRepeat: [16, 2],
    dynamic: false,
    f: mobius,
  },
  kleinFigure8: {
    id: "kleinFigure8",
    label: "Klein bottle (figure-8)",
    blurb: "A figure-8 cross-section flipped around a circle. No boundary.",
    uRange: [0, TAU],
    vRange: [0, TAU],
    uSegments: 220,
    vSegments: 80,
    glyphRepeat: [14, 4],
    dynamic: false,
    f: kleinFigure8,
  },
  kleinClassic: {
    id: "kleinClassic",
    label: "Klein bottle (classic)",
    blurb: "The glass-blower's bottle. The neck passes through the wall.",
    uRange: [0, TAU],
    vRange: [0, TAU],
    uSegments: 260,
    vSegments: 70,
    glyphRepeat: [10, 5],
    dynamic: false,
    f: kleinClassic,
  },
  klein4D: {
    id: "klein4D",
    label: "Klein bottle (4D rotation)",
    blurb: "The true Klein bottle in R^4, rotating. Watch the crossing sweep.",
    uRange: [0, TAU],
    vRange: [0, TAU],
    uSegments: 200,
    vSegments: 64,
    glyphRepeat: [12, 4],
    dynamic: true,
    f: klein4D,
  },
  roman: {
    id: "roman",
    label: "Roman surface (RP²)",
    blurb: "The sphere folded onto itself: antipodes identified. χ = 1.",
    uRange: [0, Math.PI],
    vRange: [0, TAU],
    uSegments: 160,
    vSegments: 160,
    glyphRepeat: [8, 8],
    dynamic: false,
    f: romanSurface,
  },
};

export const DEFAULT_SURFACE = "mobius";
export { TAU };
