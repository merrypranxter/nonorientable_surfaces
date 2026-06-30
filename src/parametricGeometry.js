// parametricGeometry.js
// ---------------------------------------------------------------------------
// Build (and cheaply rebuild) a THREE.BufferGeometry from a parametric surface
// definition out of surfaces.js. We roll our own instead of leaning on the
// addon ParametricGeometry so that:
//   - UVs map cleanly to (u,v) for the orientation-tracking texture, and
//   - dynamic surfaces (the 4D Klein bottle) can refresh positions in place
//     without reallocating buffers every frame.
// ---------------------------------------------------------------------------

import * as THREE from "three";

export function buildGeometry(surface) {
  const { uSegments: us, vSegments: vs } = surface;
  const rows = us + 1;
  const cols = vs + 1;
  const vertCount = rows * cols;

  const positions = new Float32Array(vertCount * 3);
  const uvs = new Float32Array(vertCount * 2);
  const indices = new Uint32Array(us * vs * 6);

  // UVs only depend on the grid, so fill them once.
  let p = 0;
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      uvs[p++] = i / us;
      uvs[p++] = j / vs;
    }
  }

  // Triangle indices (two per quad).
  let k = 0;
  for (let i = 0; i < us; i++) {
    for (let j = 0; j < vs; j++) {
      const a = i * cols + j;
      const b = a + cols;
      const c = a + 1;
      const d = b + 1;
      indices[k++] = a; indices[k++] = b; indices[k++] = c;
      indices[k++] = c; indices[k++] = b; indices[k++] = d;
    }
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geo.setAttribute("uv", new THREE.BufferAttribute(uvs, 2));
  geo.setIndex(new THREE.BufferAttribute(indices, 1));

  refreshPositions(geo, surface, { time: 0 });
  return geo;
}

// Recompute only the position attribute (and normals). Used every frame for
// dynamic surfaces and once for static ones.
export function refreshPositions(geo, surface, ctx) {
  const { uSegments: us, vSegments: vs, uRange, vRange, f } = surface;
  const rows = us + 1;
  const cols = vs + 1;
  const pos = geo.attributes.position.array;

  let p = 0;
  for (let i = 0; i < rows; i++) {
    const u = uRange[0] + (uRange[1] - uRange[0]) * (i / us);
    for (let j = 0; j < cols; j++) {
      const v = vRange[0] + (vRange[1] - vRange[0]) * (j / vs);
      const xyz = f(u, v, ctx);
      pos[p++] = xyz[0];
      pos[p++] = xyz[1];
      pos[p++] = xyz[2];
    }
  }

  geo.attributes.position.needsUpdate = true;
  geo.computeVertexNormals();
  geo.computeBoundingSphere();
}
