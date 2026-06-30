// shaders.js
// ---------------------------------------------------------------------------
// The orientation shader. This is the whole point of the repo: it makes the
// non-orientability *visible*.
//
// Two independent tells, both driven off gl_FrontFacing:
//
//   1. Side colour. Front-facing fragments get uFrontColor, back-facing get
//      uBackColor. On an ORDINARY (orientable) surface you only ever see one
//      colour from outside. On a Möbius strip / Klein bottle the two colours
//      bleed into each other along the surface — because there is only one
//      side, the "front" and the "back" are the same sheet.
//
//   2. Texture tracking. We sample a glyph texture (a grid of asymmetric "R"s).
//      On back-facing fragments we mirror the sample in u. Transport a glyph
//      around the loop and it comes back reversed — a right-handed R becomes
//      left-handed. "A Möbius strip without the texture flip is just a twisted
//      cylinder."
// ---------------------------------------------------------------------------

export const VERTEX_SHADER = /* glsl */ `
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
`;

export const FRAGMENT_SHADER = /* glsl */ `
  precision highp float;

  uniform vec3  uFrontColor;
  uniform vec3  uBackColor;
  uniform vec3  uLightDir;
  uniform sampler2D uGlyph;
  uniform vec2  uGlyphRepeat;
  uniform float uShowGlyph;   // 0 or 1
  uniform float uShowSides;   // 0 or 1
  uniform float uOpacity;

  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vViewPos;

  void main() {
    // Two-sided lighting: flip the geometric normal on back faces so both
    // sides are lit, not just the mathematically "outer" one.
    vec3 N = normalize(vNormal);
    if (!gl_FrontFacing) N = -N;

    vec3 L = normalize(uLightDir);
    float diff = max(dot(N, L), 0.0);
    // a touch of rim light reads the silhouette of the self-intersections
    vec3 V = normalize(-vViewPos);
    float rim = pow(1.0 - max(dot(N, V), 0.0), 2.0) * 0.35;
    float lighting = 0.28 + 0.8 * diff + rim;

    // (1) side colour
    vec3 base = gl_FrontFacing ? uFrontColor : uBackColor;
    base = mix(uFrontColor, base, uShowSides);
    vec3 col = base * lighting;

    // (2) texture tracking — mirror in u on the back side
    vec2 guv = vUv * uGlyphRepeat;
    if (!gl_FrontFacing) guv.x = -guv.x;
    float g = texture2D(uGlyph, fract(guv)).r;   // 1 = paper, 0 = ink
    float ink = (1.0 - g) * uShowGlyph;
    col = mix(col, col * 0.12, ink);

    gl_FragColor = vec4(col, uOpacity);
  }
`;
