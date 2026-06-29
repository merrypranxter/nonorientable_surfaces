// orientation.vert.glsl
// Reference copy of the orientation vertex shader (see src/shaders.js).
// Passes the (u,v) parametrization through as UVs so the fragment stage can
// track a chiral glyph around the surface.

varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vViewPos;

void main() {
  vUv = uv;
  vNormal = normalize(normalMatrix * normal);
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  vViewPos = mv.xyz;
  gl_Position = projectionMatrix * mv;
}
