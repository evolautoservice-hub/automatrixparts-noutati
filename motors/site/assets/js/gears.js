/* Planetary gear set (sun 24T, 3 planets 18T, ring 60T) – the core of every automatic gearbox.
   Ring fixed, sun driven, carrier turns at 24/84 of sun speed. Scroll explodes the set. */
(function () {
  var canvas = document.getElementById('gears');
  if (!canvas || !window.THREE) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var THREE = window.THREE;
  var renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { return; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);

  /* soft studio environment so metals read well on a white page */
  var pmrem = new THREE.PMREMGenerator(renderer);
  var envScene = new THREE.Scene();
  var envGeo = new THREE.SphereGeometry(10, 32, 16);
  var envMat = new THREE.ShaderMaterial({
    side: THREE.BackSide,
    uniforms: {},
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0);} ',
    fragmentShader: 'varying vec3 vP; void main(){ float h = vP.y*0.5+0.5; vec3 c = mix(vec3(0.55,0.52,0.52), vec3(1.0), smoothstep(0.2,0.9,h));' +
      ' c += vec3(1.0,0.85,0.6)*pow(max(dot(vP, normalize(vec3(0.6,0.5,0.6))),0.0),24.0)*2.0;' +
      ' c += vec3(1.0)*pow(max(dot(vP, normalize(vec3(-0.7,0.3,0.4))),0.0),12.0)*1.4; gl_FragColor = vec4(c,1.0);} '
  });
  envScene.add(new THREE.Mesh(envGeo, envMat));
  scene.environment = pmrem.fromScene(envScene, 0.02).texture;

  scene.add(new THREE.HemisphereLight(0xffffff, 0xe9e1de, 0.55));
  var key = new THREE.DirectionalLight(0xffffff, 1.6);
  key.position.set(4, 7, 6);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.left = -5; key.shadow.camera.right = 5; key.shadow.camera.top = 5; key.shadow.camera.bottom = -5;
  key.shadow.radius = 6; key.shadow.bias = -0.0008;
  scene.add(key);
  var rim = new THREE.PointLight(0xffc977, 1.3, 20); rim.position.set(-5, 2, -2); scene.add(rim);
  var rim2 = new THREE.PointLight(0xff3350, 0.7, 20); rim2.position.set(5, -2, 3); scene.add(rim2);

  var M = 0.1; // module
  function gearShape(z, internal, outerR) {
    var r = M * z / 2;
    var tip = internal ? r - M : r + M;
    var root = internal ? r + 1.25 * M : r - 1.25 * M;
    var path = new THREE.Path();
    var pts = [];
    var prof = [[-0.5, root], [-0.3, root], [-0.15, tip], [0.15, tip], [0.3, root], [0.5, root]];
    for (var i = 0; i < z; i++) {
      for (var k = 0; k < prof.length; k++) {
        if (i > 0 && k === 0) continue;
        var a = (i + prof[k][0]) * 2 * Math.PI / z;
        var rr = prof[k][1];
        pts.push(new THREE.Vector2(Math.cos(a) * rr, Math.sin(a) * rr));
      }
    }
    if (!internal) {
      var s = new THREE.Shape(pts);
      var hole = new THREE.Path();
      hole.absarc(0, 0, Math.max(r * 0.28, 0.12), 0, Math.PI * 2, true);
      s.holes.push(hole);
      return s;
    }
    var outer = new THREE.Shape();
    outer.absarc(0, 0, outerR, 0, Math.PI * 2, false);
    path.setFromPoints(pts.reverse());
    outer.holes.push(path);
    return outer;
  }
  function extrude(shape, depth) {
    var g = new THREE.ExtrudeGeometry(shape, { depth: depth, bevelEnabled: true, bevelThickness: 0.025, bevelSize: 0.018, bevelSegments: 3, curveSegments: 48 });
    g.translate(0, 0, -depth / 2);
    g.computeVertexNormals();
    return g;
  }

  var red = new THREE.MeshPhysicalMaterial({ color: 0xc8102e, metalness: 0.55, roughness: 0.28, clearcoat: 1, clearcoatRoughness: 0.12 });
  var black = new THREE.MeshPhysicalMaterial({ color: 0x1a191d, metalness: 0.7, roughness: 0.32, clearcoat: 0.6, clearcoatRoughness: 0.2 });
  var gold = new THREE.MeshStandardMaterial({ color: 0xc9a14f, metalness: 1, roughness: 0.22 });
  var steel = new THREE.MeshStandardMaterial({ color: 0xd9d6d4, metalness: 1, roughness: 0.18 });

  var S = 24, P = 18, R = 60;
  var rig = new THREE.Group();
  scene.add(rig);

  // ring
  var ring = new THREE.Mesh(extrude(gearShape(R, true, M * R / 2 + 0.42), 0.42), black);
  ring.castShadow = ring.receiveShadow = true;
  var ringGroup = new THREE.Group(); ringGroup.add(ring);
  var ringLip = new THREE.Mesh(new THREE.TorusGeometry(M * R / 2 + 0.42, 0.028, 12, 160), gold);
  ringLip.position.z = 0.24; ringGroup.add(ringLip);
  var ringLip2 = ringLip.clone(); ringLip2.position.z = -0.24; ringGroup.add(ringLip2);
  rig.add(ringGroup);

  // sun
  var sunGroup = new THREE.Group();
  var sun = new THREE.Mesh(extrude(gearShape(S, false), 0.5), red);
  sun.castShadow = sun.receiveShadow = true;
  sunGroup.add(sun);
  var shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 2.6, 48), steel);
  shaft.rotation.x = Math.PI / 2; shaft.position.z = -0.6; shaft.castShadow = true;
  sunGroup.add(shaft);
  var spline = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.12, 24), gold);
  spline.rotation.x = Math.PI / 2; spline.position.z = 0.32; sunGroup.add(spline);
  rig.add(sunGroup);

  // carrier + planets
  var carrier = new THREE.Group();
  var plate = new THREE.Mesh(new THREE.CylinderGeometry(2.45, 2.45, 0.1, 96), black);
  plate.rotation.x = Math.PI / 2; plate.position.z = -0.42; plate.receiveShadow = plate.castShadow = true;
  carrier.add(plate);
  var plateRim = new THREE.Mesh(new THREE.TorusGeometry(2.45, 0.022, 10, 120), gold);
  plateRim.position.z = -0.42; carrier.add(plateRim);
  var planets = [];
  var pr = M * (S + P) / 2;
  var planetGeo = extrude(gearShape(P, false), 0.44);
  for (var i = 0; i < 3; i++) {
    var th = i * 2 * Math.PI / 3;
    var holder = new THREE.Group();
    holder.position.set(Math.cos(th) * pr, Math.sin(th) * pr, 0);
    var pm = new THREE.Mesh(planetGeo, i === 0 ? red : black);
    pm.castShadow = pm.receiveShadow = true;
    holder.add(pm);
    var pin = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.9, 32), gold);
    pin.rotation.x = Math.PI / 2; pin.position.z = -0.12; holder.add(pin);
    var cap = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.03, 10, 40), steel);
    cap.position.z = 0.25; holder.add(cap);
    carrier.add(holder);
    planets.push({ g: holder, m: pm, th: th });
  }
  rig.add(carrier);

  // contact shadow
  var sc = document.createElement('canvas'); sc.width = sc.height = 256;
  var cx = sc.getContext('2d');
  var grd = cx.createRadialGradient(128, 128, 10, 128, 128, 128);
  grd.addColorStop(0, 'rgba(90,20,30,0.38)'); grd.addColorStop(0.55, 'rgba(90,20,30,0.12)'); grd.addColorStop(1, 'rgba(90,20,30,0)');
  cx.fillStyle = grd; cx.fillRect(0, 0, 256, 256);
  var shadow = new THREE.Mesh(new THREE.PlaneGeometry(9, 9), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false }));
  shadow.rotation.x = -Math.PI / 2; shadow.position.y = -2.7;
  scene.add(shadow);

  // meshing phase (see derivation: sun/planet mirrored, ring/planet aligned)
  var ap0 = Math.PI - Math.PI / P;
  var fp0 = (((-ap0) * P / (2 * Math.PI)) % 1 + 1) % 1;
  ring.rotation.z = -(0.5 + fp0) * 2 * Math.PI / R;

  function setAngles(as) {
    var ac = as * S / (S + R);
    sun.rotation.z = as;
    carrier.rotation.z = ac;
    for (var i = 0; i < planets.length; i++) {
      var th = planets[i].th;
      // absolute planet angle minus carrier rotation (planet is child of carrier)
      var apAbs = (th + ac) + Math.PI - Math.PI / P + ((th + ac) - as) * S / P;
      planets[i].m.rotation.z = apAbs - ac;
    }
  }

  var W = 0, H = 0;
  function resize() {
    var r = canvas.getBoundingClientRect();
    W = Math.max(1, r.width); H = Math.max(1, r.height);
    renderer.setSize(W, H, false);
    camera.aspect = W / H; camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  var mx = 0, my = 0, tmx = 0, tmy = 0;
  window.addEventListener('pointermove', function (e) {
    tmx = (e.clientX / window.innerWidth - 0.5);
    tmy = (e.clientY / window.innerHeight - 0.5);
  }, { passive: true });

  var explode = 0, texplode = 0;
  function onScroll() {
    var hero = canvas.closest('.hero');
    if (!hero) return;
    var r = hero.getBoundingClientRect();
    texplode = Math.min(1, Math.max(0, -r.top / (r.height * 0.75)));
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var visible = true;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) loop(); }, { threshold: 0 }).observe(canvas);
  }

  var t0 = performance.now(), intro = 0, raf = 0;
  var angle = 0, speed = 0;
  function frame(now) {
    var dt = Math.min(0.05, (now - (frame.last || now)) / 1000); frame.last = now;
    var el = (now - t0) / 1000;
    intro = reduce ? 1 : Math.min(1, el / 2.2);
    var ease = 1 - Math.pow(1 - intro, 4);
    speed += ((reduce ? 0 : 0.55) - speed) * Math.min(1, dt * 1.5);
    angle += speed * dt;
    setAngles(angle);

    mx += (tmx - mx) * 0.05; my += (tmy - my) * 0.05;
    explode += (texplode - explode) * 0.08;
    var e = explode;

    // exploded view along the gearbox axis
    ringGroup.position.z = -1.6 * e;
    carrier.position.z = 0.15 * e;
    for (var i = 0; i < planets.length; i++) planets[i].g.position.z = 0.9 * e;
    sunGroup.position.z = 1.9 * e;

    rig.rotation.x = -0.62 + my * 0.25 + e * 0.35;
    rig.rotation.y = 0.55 + mx * 0.45 - e * 0.9 + (1 - ease) * 1.4;
    rig.rotation.z = (1 - ease) * -0.6;
    var sc = 0.6 + 0.4 * ease;
    rig.scale.setScalar(sc);
    rig.position.y = 0.15;

    camera.position.set(0, 0.6 + e * 0.6, 13.5 - e * 1.2);
    camera.lookAt(0, 0, 0);
    shadow.material.opacity = 0.9 - e * 0.5;

    renderer.render(scene, camera);
    if (visible && !reduce) raf = requestAnimationFrame(frame);
    else if (reduce && intro < 1) raf = requestAnimationFrame(frame);
  }
  function loop() { cancelAnimationFrame(raf); raf = requestAnimationFrame(frame); }
  if (reduce) { window.addEventListener('scroll', loop, { passive: true }); }
  loop();
  document.documentElement.classList.add('gl-on');
})();
