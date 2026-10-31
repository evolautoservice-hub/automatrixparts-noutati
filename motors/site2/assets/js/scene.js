/* AutoMatrix Motors – cinematic studio reveal of the brand emblem.
   Dark studio, volumetric light cone, glossy floor with reflection, red car-paint lacquer, piano black, polished gold.
   HDR render -> bloom -> filmic tone map -> vignette, chromatic fringe and film grain.
   Requires THREE r128. Exposes window.AMScene(stageEl). */
(function () {
  window.AMScene = function (stage) {
    var THREE = window.THREE, canvas = stage.querySelector('canvas');
    if (!THREE || !canvas) return;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var mobile = window.innerWidth < 760;
    var renderer;
    try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: false, alpha: false, powerPreference: 'high-performance' }); }
    catch (e) { return; }
    var DPR = Math.min(window.devicePixelRatio || 1, mobile ? 1.5 : 1.6);
    renderer.setPixelRatio(DPR);
    renderer.toneMapping = THREE.NoToneMapping;        // done in the composite pass
    renderer.outputEncoding = THREE.LinearEncoding;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    function lin(hex) { return new THREE.Color(hex).convertSRGBToLinear(); }
    var BG = lin(0x060607);
    renderer.setClearColor(BG, 1);

    var scene = new THREE.Scene();
    scene.fog = new THREE.Fog(BG, 9, 22);
    var camera = new THREE.PerspectiveCamera(30, 1, 0.1, 60);

    /* ---------- studio reflections: black room with strip softboxes ---------- */
    var pmrem = new THREE.PMREMGenerator(renderer);
    var studio = new THREE.Scene();
    studio.add(new THREE.Mesh(new THREE.BoxGeometry(30, 16, 30), new THREE.MeshBasicMaterial({ color: 0x020202, side: THREE.BackSide })));
    function strip(w, h, x, y, z, ry, rx, k, tint) {
      var p = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: lin(tint || 0xffffff).multiplyScalar(k), side: THREE.DoubleSide }));
      p.position.set(x, y, z); p.rotation.y = ry || 0; p.rotation.x = rx || 0; studio.add(p);
    }
    strip(1.2, 12, 0, 7.5, 0, 0, Math.PI / 2, 9);                    // long overhead strip
    strip(0.7, 8, -7, 1.5, 2.5, Math.PI / 2, 0, 12);                 // left vertical strip
    strip(0.7, 8, 7, 1.5, 1.5, -Math.PI / 2, 0, 7, 0xffd9a3);        // right warm strip
    strip(6, 0.5, 0, 0.6, -10, 0, 0, 6, 0xffe2b8);                   // low back rim
    strip(3.5, 2.2, -3.5, 3.2, 9, Math.PI, 0, 5);                    // soft front key
    strip(2, 2, 4.5, -0.5, 6, Math.PI * 1.2, 0, 2.5, 0xff2a3a);       // red kicker
    scene.environment = pmrem.fromScene(studio, 0.02).texture;

    /* ---------- lights ---------- */
    var spot = new THREE.SpotLight(0xfff3e2, 0, 18, 0.42, 0.65, 1.3);
    spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -0.0005; spot.shadow.radius = 6;
    scene.add(spot, spot.target);
    var redRim = new THREE.PointLight(0xff1a2e, 0, 9, 2); scene.add(redRim);
    var goldRim = new THREE.PointLight(0xffc77a, 0, 9, 2); scene.add(goldRim);
    var amb = new THREE.HemisphereLight(0x302a2a, 0x050505, 0.0); scene.add(amb);

    /* ---------- light sweep injected into PBR materials ---------- */
    var U = { uSweep: { value: -9 }, uSweepI: { value: 0 } };
    function sweep(mat) {
      mat.onBeforeCompile = function (sh) {
        sh.uniforms.uSweep = U.uSweep; sh.uniforms.uSweepI = U.uSweepI;
        sh.vertexShader = 'varying vec3 vWPos;\n' + sh.vertexShader.replace('#include <project_vertex>', '#include <project_vertex>\n vWPos = (modelMatrix * vec4(transformed, 1.0)).xyz;');
        sh.fragmentShader = 'uniform float uSweep; uniform float uSweepI; varying vec3 vWPos;\n' + sh.fragmentShader.replace('#include <tonemapping_fragment>',
          'float sd = (vWPos.x * 0.8 + vWPos.y * 0.6) - uSweep; float band = exp(-sd * sd * 30.0) + 0.25 * exp(-sd * sd * 4.0);\n gl_FragColor.rgb += band * uSweepI * vec3(1.0, 0.9, 0.78) * (0.15 + gl_FragColor.rgb * 1.6);\n#include <tonemapping_fragment>');
      };
      return mat;
    }
    var red = sweep(new THREE.MeshPhysicalMaterial({ color: lin(0xa3061c), metalness: 0.25, roughness: 0.32, clearcoat: 1, clearcoatRoughness: 0.025, envMapIntensity: 1.0 }));
    var black = sweep(new THREE.MeshPhysicalMaterial({ color: lin(0x070708), metalness: 0.0, roughness: 0.12, clearcoat: 1, clearcoatRoughness: 0.02, envMapIntensity: 1.0 }));
    var gold = sweep(new THREE.MeshStandardMaterial({ color: lin(0xe7c27a), metalness: 1, roughness: 0.14, envMapIntensity: 1.5 }));

    /* ---------- emblem (traced from the logo, 3-fold symmetric) ---------- */
    var BASE = [[0.2978, 0.26], [0.4533, -0.06], [0.12, -0.0467], [0.2889, -0.3689], [0.9378, -0.3667], [0.6089, 0.2533]];
    function rot(p, a) { var c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; }
    function area(q) { var a = 0; for (var i = 0; i < q.length; i++) { var p = q[i], r = q[(i + 1) % q.length]; a += p[0] * r[1] - r[0] * p[1]; } return a / 2; }
    function inset(q, w) {
      var n = q.length, out = [];
      function line(i) { var a = q[i], b = q[(i + 1) % n], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy); return { p: [a[0] - dy / L * w, a[1] + dx / L * w], d: [dx, dy] }; }
      for (var i = 0; i < n; i++) {
        var l1 = line((i - 1 + n) % n), l2 = line(i), den = l1.d[0] * l2.d[1] - l1.d[1] * l2.d[0];
        var t = ((l2.p[0] - l1.p[0]) * l2.d[1] - (l2.p[1] - l1.p[1]) * l2.d[0]) / den;
        out.push([l1.p[0] + l1.d[0] * t, l1.p[1] + l1.d[1] * t]);
      }
      return out;
    }
    function shapeOf(q) { var s = new THREE.Shape(); s.moveTo(q[0][0], q[0][1]); for (var i = 1; i < q.length; i++) s.lineTo(q[i][0], q[i][1]); s.closePath(); return s; }
    function pathOf(q) { var r = q.slice().reverse(), p = new THREE.Path(); p.moveTo(r[0][0], r[0][1]); for (var i = 1; i < r.length; i++) p.lineTo(r[i][0], r[i][1]); p.closePath(); return p; }
    function ext(s, depth, bevel) { return new THREE.ExtrudeGeometry(s, { depth: depth, bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 4, curveSegments: 1 }); }

    var D = 0.3, RIM = 0.034;
    function buildEmblem(cast) {
      var em = new THREE.Group(), list = [];
      for (var k = 0; k < 3; k++) {
        var q = BASE.map(function (p) { return rot(p, k * 2 * Math.PI / 3); });
        if (area(q) < 0) q.reverse();
        var inner = inset(q, RIM), g = new THREE.Group();
        var body = new THREE.Mesh(ext(shapeOf(q), D, 0.01), black); body.position.z = -D / 2; g.add(body);
        var fs = shapeOf(q); fs.holes.push(pathOf(inner));
        var ff = new THREE.Mesh(ext(fs, 0.014, 0.006), gold); ff.position.z = D / 2 + 0.002; g.add(ff);
        var fb = ff.clone(); fb.position.z = -D / 2 - 0.016; g.add(fb);
        var face = new THREE.Mesh(ext(shapeOf(inner), 0.008, 0.004), red); face.position.z = D / 2 + 0.003; g.add(face);
        for (var v = 0; v < q.length; v++) {
          var cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, D + 0.012, 12), gold);
          cyl.rotation.x = Math.PI / 2; cyl.position.set(q[v][0], q[v][1], 0); g.add(cyl);
        }
        g.traverse(function (o) { if (o.isMesh) { o.castShadow = cast; o.receiveShadow = cast; } });
        var cx = 0, cy = 0; q.forEach(function (p) { cx += p[0]; cy += p[1]; }); cx /= q.length; cy /= q.length;
        var L = Math.hypot(cx, cy);
        em.add(g); list.push({ g: g, dir: [cx / L, cy / L] });
      }
      return { group: em, pieces: list };
    }
    var main = buildEmblem(true), mirror = buildEmblem(false);
    var holder = new THREE.Group(); holder.add(main.group); scene.add(holder);
    var reflHolder = new THREE.Group(); reflHolder.add(mirror.group); reflHolder.scale.y = -1; scene.add(reflHolder);

    /* ---------- glossy floor (semi-transparent over the mirrored emblem) ---------- */
    var FLOOR = -1.18;
    function radial(stops, size) {
      var c = document.createElement('canvas'); c.width = c.height = size || 256;
      var x = c.getContext('2d'), g = x.createRadialGradient(c.width / 2, c.height / 2, 0, c.width / 2, c.height / 2, c.width / 2);
      stops.forEach(function (s) { g.addColorStop(s[0], s[1]); }); x.fillStyle = g; x.fillRect(0, 0, c.width, c.height);
      return new THREE.CanvasTexture(c);
    }
    var floor = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ color: lin(0x0b0b0d), roughness: 0.42, metalness: 0.0, transparent: true, opacity: 0.86, envMapIntensity: 0.35 }));
    floor.rotation.x = -Math.PI / 2; floor.position.y = FLOOR; floor.receiveShadow = true; scene.add(floor);
    // fade the floor into the darkness
    var fade = new THREE.Mesh(new THREE.PlaneGeometry(26, 26), new THREE.MeshBasicMaterial({
      map: radial([[0, 'rgba(255,255,255,0)'], [0.2, 'rgba(255,255,255,0)'], [0.55, 'rgba(255,255,255,0.93)'], [1, 'rgba(255,255,255,1)']], 512), transparent: true, depthWrite: false, fog: false
    }));
    fade.material.color = BG.clone();
    fade.rotation.x = -Math.PI / 2; fade.position.y = FLOOR + 0.004; scene.add(fade);

    /* ---------- volumetric light cone ---------- */
    var coneH = 6.2;
    var cone = new THREE.Mesh(new THREE.ConeGeometry(2.25, coneH, 64, 1, true), new THREE.ShaderMaterial({
      uniforms: { uI: { value: 0 }, uT: { value: 0 } }, transparent: true, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, fog: false,
      vertexShader: 'varying vec3 vN; varying vec3 vV; varying vec2 vUv; varying vec3 vW; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); vV = -mv.xyz; vN = normalize(normalMatrix * normal); vUv = uv; vW = position; gl_Position = projectionMatrix * mv; }',
      fragmentShader: 'uniform float uI; uniform float uT; varying vec3 vN; varying vec3 vV; varying vec2 vUv; varying vec3 vW;\n' +
        'float h(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5453); }\n' +
        'float n(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.0-2.0*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x), mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x), f.y); }\n' +
        'void main(){ float f = abs(dot(normalize(vN), normalize(vV))); f = pow(f, 3.0);\n' +
        ' float along = vUv.y; float att = smoothstep(0.0, 0.35, along) * (0.35 + 0.65 * along);\n' +
        ' float haze = 0.65 + 0.35 * n(vec2(atan(vW.z, vW.x) * 3.0, vW.y * 1.5 - uT * 0.25));\n' +
        ' gl_FragColor = vec4(vec3(1.0, 0.86, 0.66) * f * att * haze * uI, 1.0); }'
    }));
    scene.add(cone);

    /* ---------- dust in the beam ---------- */
    var N = mobile ? 140 : 320, pos = new Float32Array(N * 3), seed = new Float32Array(N);
    for (var i = 0; i < N; i++) {
      var yy = Math.random(), rr = Math.sqrt(Math.random()) * (0.3 + 1.9 * (1 - yy)), aa = Math.random() * 6.283;
      pos[i * 3] = Math.cos(aa) * rr; pos[i * 3 + 1] = FLOOR + 0.2 + yy * 4.6; pos[i * 3 + 2] = Math.sin(aa) * rr; seed[i] = Math.random();
    }
    var dg = new THREE.BufferGeometry(); dg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    var dust = new THREE.Points(dg, new THREE.PointsMaterial({
      size: mobile ? 0.03 : 0.024, map: radial([[0, 'rgba(255,255,255,1)'], [0.3, 'rgba(255,230,190,0.6)'], [1, 'rgba(255,220,170,0)']], 64),
      color: new THREE.Color(1.6, 1.35, 1.0), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, sizeAttenuation: true, fog: false
    }));
    var dustGroup = new THREE.Group(); dustGroup.add(dust); scene.add(dustGroup);

    /* ---------- post-processing: HDR -> bloom -> filmic grade ---------- */
    var gl2 = renderer.capabilities.isWebGL2;
    var half = gl2 || (renderer.extensions.has('OES_texture_half_float') && renderer.extensions.has('EXT_color_buffer_half_float'));
    var TYPE = half ? THREE.HalfFloatType : THREE.UnsignedByteType;
    function makeRT(w, h, depth, ms) {
      var o = { type: TYPE, format: THREE.RGBAFormat, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, depthBuffer: !!depth, stencilBuffer: false };
      var t = (ms && gl2 && THREE.WebGLMultisampleRenderTarget) ? new THREE.WebGLMultisampleRenderTarget(w, h, o) : new THREE.WebGLRenderTarget(w, h, o);
      if (ms && t.samples !== undefined) t.samples = 4;
      return t;
    }
    var VQ = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }';
    var quad = new THREE.PlaneGeometry(2, 2), oCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    function pass(frag, uni) { var m = new THREE.ShaderMaterial({ uniforms: uni, vertexShader: VQ, fragmentShader: frag, depthTest: false, depthWrite: false }); var s = new THREE.Scene(); s.add(new THREE.Mesh(quad, m)); return { m: m, s: s }; }
    function run(p, target) { renderer.setRenderTarget(target); renderer.render(p.s, oCam); }
    var rtScene, rtA, rtB, rtC, rtD;
    var pBright = pass('uniform sampler2D t; uniform float th; varying vec2 vUv; void main(){ vec3 c = texture2D(t, vUv).rgb; float l = max(max(c.r, c.g), c.b); gl_FragColor = vec4(c * smoothstep(th, th + 0.8, l), 1.0); }', { t: { value: null }, th: { value: 0.85 } });
    var pBlur = pass('uniform sampler2D t; uniform vec2 dir; varying vec2 vUv; void main(){ vec3 c = texture2D(t, vUv).rgb * 0.227027;\n' +
      ' c += texture2D(t, vUv + dir * 1.3846).rgb * 0.3162162; c += texture2D(t, vUv - dir * 1.3846).rgb * 0.3162162;\n' +
      ' c += texture2D(t, vUv + dir * 3.2307).rgb * 0.0702702; c += texture2D(t, vUv - dir * 3.2307).rgb * 0.0702702; gl_FragColor = vec4(c, 1.0); }', { t: { value: null }, dir: { value: new THREE.Vector2() } });
    var pComp = pass('uniform sampler2D tS; uniform sampler2D tB1; uniform sampler2D tB2; uniform float uT; uniform float uFade; uniform float uExp; uniform vec2 uRes; varying vec2 vUv;\n' +
      'vec3 aces(vec3 x){ return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0); }\n' +
      'void main(){ vec2 d = vUv - 0.5; float r2 = dot(d, d); vec2 o = d * 0.0022;\n' +
      ' vec3 c = vec3(texture2D(tS, vUv + o).r, texture2D(tS, vUv).g, texture2D(tS, vUv - o).b);\n' +
      ' c += texture2D(tB1, vUv).rgb * 0.5 + texture2D(tB2, vUv).rgb * 0.9;\n' +
      ' c = aces(c * uExp); c = pow(c, vec3(1.0 / 2.2));\n' +
      ' c = mix(c, c * c * (3.0 - 2.0 * c), 0.18);\n' +
      ' c *= mix(1.0, 1.0 - r2 * 1.35, 0.9);\n' +
      ' float g = fract(sin(dot(vUv * uRes + fract(uT) * 91.7, vec2(12.9898, 78.233))) * 43758.5453); c += (g - 0.5) * 0.028;\n' +
      ' gl_FragColor = vec4(c * uFade, 1.0); }', { tS: { value: null }, tB1: { value: null }, tB2: { value: null }, uT: { value: 0 }, uFade: { value: 0 }, uExp: { value: 1.0 }, uRes: { value: new THREE.Vector2() } });

    var W = 1, H = 1, wide = true;
    function resize() {
      var r = canvas.getBoundingClientRect();
      W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
      renderer.setSize(W, H, false);
      camera.aspect = W / H; camera.updateProjectionMatrix();
      wide = camera.aspect > 1.15;
      var pw = Math.round(W * DPR), ph = Math.round(H * DPR);
      [rtScene, rtA, rtB, rtC, rtD].forEach(function (t) { if (t) t.dispose(); });
      rtScene = makeRT(pw, ph, true, !mobile);
      rtA = makeRT(pw >> 1, ph >> 1); rtB = makeRT(pw >> 1, ph >> 1);
      rtC = makeRT(pw >> 2, ph >> 2); rtD = makeRT(pw >> 2, ph >> 2);
      pComp.m.uniforms.uRes.value.set(pw, ph);
    }
    window.addEventListener('resize', resize); resize();

    function composite(t) {
      renderer.setRenderTarget(rtScene); renderer.clear(); renderer.render(scene, camera);
      pBright.m.uniforms.t.value = rtScene.texture; run(pBright, rtA);
      pBlur.m.uniforms.t.value = rtA.texture; pBlur.m.uniforms.dir.value.set(1 / rtA.width, 0); run(pBlur, rtB);
      pBlur.m.uniforms.t.value = rtB.texture; pBlur.m.uniforms.dir.value.set(0, 1 / rtA.height); run(pBlur, rtA);
      pBlur.m.uniforms.t.value = rtA.texture; pBlur.m.uniforms.dir.value.set(2 / rtC.width, 0); run(pBlur, rtC);
      pBlur.m.uniforms.t.value = rtC.texture; pBlur.m.uniforms.dir.value.set(0, 2 / rtC.height); run(pBlur, rtD);
      pComp.m.uniforms.tS.value = rtScene.texture; pComp.m.uniforms.tB1.value = rtA.texture; pComp.m.uniforms.tB2.value = rtD.texture;
      pComp.m.uniforms.uT.value = t; run(pComp, null);
    }

    /* ---------- input ---------- */
    var mx = 0, my = 0, tmx = 0, tmy = 0;
    window.addEventListener('pointermove', function (e) { tmx = e.clientX / window.innerWidth - 0.5; tmy = e.clientY / window.innerHeight - 0.5; }, { passive: true });
    var hero = stage.closest('section') || stage, sP = 0, tS = 0;
    function onScroll() { var r = hero.getBoundingClientRect(); tS = Math.min(1, Math.max(0, -r.top / (r.height * 0.85))); }
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

    /* ---------- timeline ---------- */
    function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
    function expo(x) { return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); }
    function inout(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
    var START = [{ o: [0.4, 2.4, -3.0], r: [1.3, -1.0, 0.7] }, { o: [-2.6, -0.6, 1.4], r: [-0.9, 1.4, -0.6] }, { o: [2.8, -0.9, -2.0], r: [0.8, 0.9, 1.2] }];
    var t0 = performance.now(), last = t0, raf = 0, visible = true;
    var LOCK = 3.1, nextSweep = LOCK, sw = null;

    function frame(now) {
      var t = (now - t0) / 1000, dt = Math.min(0.05, (now - last) / 1000); last = now;
      if (reduce) t = 60;
      mx += (tmx - mx) * 0.04; my += (tmy - my) * 0.04; sP += (tS - sP) * 0.07;

      // lights come up like a studio switching on
      var on = cl((t - 0.15) / 1.6), onE = on * on * (3 - 2 * on);
      var flick = t < 1.0 ? (0.75 + 0.25 * Math.sin(t * 47.0) * Math.sin(t * 13.0)) : 1;
      spot.intensity = 9.5 * onE * flick; cone.material.uniforms.uI.value = 0.55 * onE * flick;
      redRim.intensity = 3.2 * cl((t - 0.8) / 1.8); goldRim.intensity = 2.2 * cl((t - 1.1) / 1.8); amb.intensity = 0.35 * onE;
      pComp.m.uniforms.uFade.value = cl(t / 0.9);
      dust.material.opacity = 0.9 * cl((t - 0.6) / 2.2);

      // assembly
      for (var i = 0; i < 3; i++) {
        var p = main.pieces[i], s = START[i], q = expo(cl((t - 0.5 - i * 0.24) / 2.3)), iq = 1 - q, sp = sP * 0.34;
        p.g.position.set(s.o[0] * iq + p.dir[0] * sp, s.o[1] * iq + p.dir[1] * sp, s.o[2] * iq + (i - 1) * sP * 0.4);
        p.g.rotation.set(s.r[0] * iq, s.r[1] * iq, s.r[2] * iq);
        var m = mirror.pieces[i]; m.g.position.copy(p.g.position); m.g.rotation.copy(p.g.rotation);
      }

      // placement: right of the headline on wide screens, centred on phones
      var X = wide ? Math.min(1.75, 0.95 + (camera.aspect - 1.15) * 0.9) : 0, Y = 0.1;
      var c = inout(cl(t / 4.2)), idle = cl((t - LOCK) / 2);
      var drift = idle * 0.03;
      holder.position.set(X, Y + Math.sin(t * 0.6) * 0.035 * idle, 0);
      holder.rotation.y = -0.5 + (1 - c) * 1.1 + Math.sin(t * 0.2) * 0.14 * idle + mx * 0.5 - sP * 1.0;
      holder.rotation.x = 0.16 + Math.sin(t * 0.17) * 0.04 * idle + my * 0.22 + sP * 0.22;
      holder.rotation.z = (1 - c) * -0.25;
      var pulse = Math.exp(-Math.pow((t - LOCK) * 5, 2)) * 0.018; holder.scale.setScalar(1 + pulse);
      reflHolder.position.set(X, 2 * FLOOR - holder.position.y, 0);
      reflHolder.rotation.set(-holder.rotation.x, holder.rotation.y, -holder.rotation.z);
      reflHolder.scale.set(holder.scale.x, -holder.scale.y, holder.scale.z);

      // beam, lights and dust follow the emblem
      cone.position.set(X + 0.15, FLOOR + coneH / 2 + 0.05, 0.2);
      spot.position.set(X + 0.15, FLOOR + coneH + 0.2, 0.2); spot.target.position.set(X, FLOOR, 0);
      redRim.position.set(X - 2.4, 0.4, -1.6); goldRim.position.set(X + 2.2, 1.2, -1.2);
      fade.position.x = X; dustGroup.position.set(X + 0.15, 0, 0.2);
      cone.material.uniforms.uT.value = t;
      var a = dg.attributes.position.array;
      for (var j = 0; j < N; j++) { a[j * 3 + 1] += (0.035 + seed[j] * 0.05) * dt; a[j * 3] += Math.sin(t * 0.4 + j) * 0.0007; if (a[j * 3 + 1] > FLOOR + 4.9) a[j * 3 + 1] = FLOOR + 0.2; }
      dg.attributes.position.needsUpdate = true;

      // camera: low close start, slow dolly back, faint handheld drift
      var dist = wide ? 7.5 : Math.max(7.5, 5.0 / camera.aspect);
      var lookY = wide ? 0.05 + 0.05 * c : -0.536 * dist * 0.22;
      camera.position.set(X * 0.55 + Math.sin(t * 0.31) * drift, lookY - 0.2 + 0.55 * c + Math.sin(t * 0.43) * drift * 0.6, dist * (0.52 + 0.48 * c) - sP * 1.1);
      camera.lookAt(X * 0.62, lookY, 0);

      // light sweep across the lacquer
      if (t >= nextSweep) { sw = { s: t, strong: nextSweep === LOCK }; nextSweep = t + (sw.strong ? 7 : 9); }
      if (sw) {
        var k = (t - sw.s) / (sw.strong ? 1.6 : 2.4);
        U.uSweep.value = X * 0.8 + Y * 0.6 - 2.3 + k * 4.6;
        U.uSweepI.value = k < 1 ? Math.sin(k * Math.PI) * (sw.strong ? 2.2 : 1.0) : 0;
      }

      composite(t);
      if (!stage.classList.contains('live')) stage.classList.add('live');
      if (visible && !reduce && !document.hidden) raf = requestAnimationFrame(frame);
    }
    function loop() { cancelAnimationFrame(raf); last = performance.now(); raf = requestAnimationFrame(frame); }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) loop(); }).observe(canvas);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) loop(); });
    if (reduce) { window.addEventListener('resize', loop); window.addEventListener('scroll', loop, { passive: true }); }
    loop();
  };
})();
