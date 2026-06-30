// orientation.frag.glsl
// Reference copy of the orientation fragment shader (see src/shaders.js).
//
// The non-orientability is revealed two ways, both keyed on gl_FrontFacing:
//   1. front/back get different colours -> on a one-sided surface both show.
//   2. a chiral glyph is mirrored on back faces -> transport it around the
//      loop and it returns reversed.

precision highp float;

uniform vec3  uFrontColor;
uniform vec3  uBackColor;
uniform vec3  uLightDir;
uniform sampler2D uGlyph;
uniform vec2  uGlyphRepeat;
uniform float uShowGlyph;
uniform float uShowSides;
uniform float uOpacity;

varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vViewPos;

void main() {
  vec3 N = normalize(vNormal);
  if (!gl_FrontFacing) N = -N;

  vec3 L = normalize(uLightDir);
  float diff = max(dot(N, L), 0.0);
  vec3 V = normalize(-vViewPos);
  float rim = pow(1.0 - max(dot(N, V), 0.0), 2.0) * 0.35;
  float lighting = 0.28 + 0.8 * diff + rim;

  vec3 base = gl_FrontFacing ? uFrontColor : uBackColor;
  base = mix(uFrontColor, base, uShowSides);
  vec3 col = base * lighting;

  vec2 guv = vUv * uGlyphRepeat;
  if (!gl_FrontFacing) guv.x = -guv.x;
  float g = texture2D(uGlyph, fract(guv)).r;
  float ink = (1.0 - g) * uShowGlyph;
  col = mix(col, col * 0.12, ink);

  gl_FragColor = vec4(col, uOpacity);
}
