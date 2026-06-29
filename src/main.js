// main.js
// ---------------------------------------------------------------------------
// The One-Sided Wanderer's viewer. Sets up a THREE scene, swaps between the
// surfaces defined in surfaces.js, drives the orientation shader, and rebuilds
// the 4D Klein bottle every frame so it can rotate through the fourth dimension.
// ---------------------------------------------------------------------------

import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import GUI from "three/addons/libs/lil-gui.module.min.js";

import { SURFACES, DEFAULT_SURFACE } from "./surfaces.js";
import { buildGeometry, refreshPositions } from "./parametricGeometry.js";
import { VERTEX_SHADER, FRAGMENT_SHADER } from "./shaders.js";
import { makeGlyphTexture } from "./glyphTexture.js";

// --- renderer / scene / camera ---------------------------------------------
const canvas = document.getElementById("scene");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b0d12);

const camera = new THREE.PerspectiveCamera(
  45,
  window.innerWidth / window.innerHeight,
  0.01,
  100
);
camera.position.set(3.4, 2.0, 4.2);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotateSpeed = 0.9;

// subtle grid + axes for spatial grounding
const grid = new THREE.GridHelper(10, 20, 0x223044, 0x161c26);
grid.position.y = -2.2;
scene.add(grid);

// --- material ---------------------------------------------------------------
const glyph = makeGlyphTexture();

const uniforms = {
  uFrontColor: { value: new THREE.Color(0x4ea1ff) },
  uBackColor: { value: new THREE.Color(0xff5d73) },
  uLightDir: { value: new THREE.Vector3(0.5, 0.8, 0.6).normalize() },
  uGlyph: { value: glyph },
  uGlyphRepeat: { value: new THREE.Vector2(16, 2) },
  uShowGlyph: { value: 1 },
  uShowSides: { value: 1 },
  uOpacity: { value: 1 },
};

const material = new THREE.ShaderMaterial({
  uniforms,
  vertexShader: VERTEX_SHADER,
  fragmentShader: FRAGMENT_SHADER,
  side: THREE.DoubleSide,
  transparent: false,
});

let current = SURFACES[DEFAULT_SURFACE];
let mesh = new THREE.Mesh(buildGeometry(current), material);
scene.add(mesh);
applySurfaceUniforms(current);

const wireframe = new THREE.LineSegments(
  new THREE.WireframeGeometry(mesh.geometry),
  new THREE.LineBasicMaterial({ color: 0x0a0c10, transparent: true, opacity: 0.18 })
);
wireframe.visible = false;
mesh.add(wireframe);

function applySurfaceUniforms(surface) {
  uniforms.uGlyphRepeat.value.set(surface.glyphRepeat[0], surface.glyphRepeat[1]);
}

function setSurface(id) {
  current = SURFACES[id];
  scene.remove(mesh);
  mesh.geometry.dispose();
  mesh = new THREE.Mesh(buildGeometry(current), material);
  scene.add(mesh);
  applySurfaceUniforms(current);
  rebuildWireframe();
  caption.textContent = current.blurb;
}

function rebuildWireframe() {
  wireframe.geometry.dispose();
  wireframe.geometry = new THREE.WireframeGeometry(mesh.geometry);
  mesh.add(wireframe);
}

// --- GUI --------------------------------------------------------------------
const params = {
  surface: DEFAULT_SURFACE,
  showGlyph: true,
  showSides: true,
  wireframe: false,
  autoRotate: true,
  opacity: 1.0,
  frontColor: "#4ea1ff",
  backColor: "#ff5d73",
};

const gui = new GUI({ title: "One-Sided Wanderer" });

const surfaceOptions = {};
for (const key of Object.keys(SURFACES)) surfaceOptions[SURFACES[key].label] = key;

gui.add(params, "surface", surfaceOptions).name("Surface").onChange(setSurface);
gui.add(params, "showGlyph").name("Texture tracking").onChange((b) => (uniforms.uShowGlyph.value = b ? 1 : 0));
gui.add(params, "showSides").name("Two-tone sides").onChange((b) => (uniforms.uShowSides.value = b ? 1 : 0));
gui.add(params, "wireframe").name("Wireframe").onChange((b) => (wireframe.visible = b));
gui.add(params, "autoRotate").name("Auto-rotate").onChange((b) => (controls.autoRotate = b));
gui.add(params, "opacity", 0.2, 1.0, 0.01).name("Opacity").onChange((o) => {
  uniforms.uOpacity.value = o;
  material.transparent = o < 1.0;
  material.needsUpdate = true;
});
gui.addColor(params, "frontColor").name("Front colour").onChange((c) => uniforms.uFrontColor.value.set(c));
gui.addColor(params, "backColor").name("Back colour").onChange((c) => uniforms.uBackColor.value.set(c));

controls.autoRotate = params.autoRotate;

// caption element
const caption = document.getElementById("caption");
caption.textContent = current.blurb;

// --- resize -----------------------------------------------------------------
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- loop -------------------------------------------------------------------
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  if (current.dynamic) {
    refreshPositions(mesh.geometry, current, { time: t });
    if (params.wireframe) rebuildWireframe();
  }

  controls.update();
  renderer.render(scene, camera);
}
animate();
