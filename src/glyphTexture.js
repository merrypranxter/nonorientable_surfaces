// glyphTexture.js
// ---------------------------------------------------------------------------
// Procedurally draw the "tracking" texture: a tile holding a deliberately
// asymmetric, chiral glyph (the letter R) plus a cell border. Asymmetry is the
// point — a symmetric mark wouldn't reveal the mirror flip when transported
// around a non-orientable surface.
//
// White = paper (texture .r = 1), dark = ink (.r = 0). The shader treats ink
// as the glyph.
// ---------------------------------------------------------------------------

import * as THREE from "three";

export function makeGlyphTexture(size = 256) {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext("2d");

  // paper
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, size, size);

  // cell border
  ctx.strokeStyle = "#000000";
  ctx.lineWidth = size * 0.04;
  ctx.strokeRect(0, 0, size, size);

  // the chiral glyph
  ctx.fillStyle = "#000000";
  ctx.font = `bold ${size * 0.74}px Georgia, "Times New Roman", serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("R", size * 0.5, size * 0.54);

  const tex = new THREE.CanvasTexture(canvas);
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.anisotropy = 4;
  tex.needsUpdate = true;
  return tex;
}
