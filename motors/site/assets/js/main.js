/* AutoMatrix Motors – site script. Edit CONFIG to change contact data or enable third-party services. */
var CONFIG = {
  phones: [
    { label: '0734 607 050', tel: '+40734607050', wa: '40734607050' },
    { label: '0734 960 810', tel: '+40734960810', wa: '40734960810' }
  ],
  email: 'service@automatrixmotors.ro',
  address: 'Str. Înfrățirii nr. 111, Băicoi, jud. Prahova',
  maps: 'https://g.page/r/CaVPuXWOanrLEBM',
  formEndpoint: 'send.php',
  // Live chat extern (opțional): completează din contul Tawk.to → Administration → Chat Widget.
  // Se încarcă DOAR după acordul pentru cookie-uri funcționale.
  tawk: { propertyId: '', widgetId: '' },
  ga4: '',        // ex. 'G-XXXXXXX' – se încarcă doar cu acord „Analiză”
  metaPixel: ''   // ex. '1234567890' – se încarcă doar cu acord „Marketing”
};
var LIVE = /(^|\.)automatrixmotors\.ro$/.test(location.hostname);

document.documentElement.classList.add('js');

function $(s, c) { return (c || document).querySelector(s); }
function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
function waLink(n, text) { return 'https://wa.me/' + n + (text ? '?text=' + encodeURIComponent(text) : ''); }
function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- header ---------- */
(function () {
  var top = $('.top');
  if (!top) return;
  function onS() { top.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onS, { passive: true }); onS();
  var btn = $('.menu-btn');
  if (btn) btn.addEventListener('click', function () {
    var open = document.body.classList.toggle('menu-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  $$('.nav a').forEach(function (a) { a.addEventListener('click', function () { document.body.classList.remove('menu-open'); if (btn) btn.setAttribute('aria-expanded', 'false'); }); });
  // active section
  var links = $$('.nav a[href^="#"]');
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
  if ('IntersectionObserver' in window && secs.length) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (e.isIntersecting) links.forEach(function (a) { a.setAttribute('aria-current', a.getAttribute('href') === '#' + e.target.id ? 'true' : 'false'); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    secs.forEach(function (s) { io.observe(s); });
  }
})();

/* ---------- warranty certificate: 3D tilt + month bar ---------- */
(function () {
  var cert = $('.cert'), scene = $('.w-scene');
  if (!cert || !scene) return;
  var bar = $('.cert-bar', cert), num = $('.cert-num strong', cert);
  if (!reduceMotion && window.matchMedia('(hover: hover)').matches) {
    scene.addEventListener('pointermove', function (e) {
      var r = scene.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      cert.style.transform = 'rotateY(' + (x * 16) + 'deg) rotateX(' + (-y * 14) + 'deg)';
      cert.style.setProperty('--gx', (x + 0.5) * 100 + '%'); cert.style.setProperty('--gy', (y + 0.5) * 100 + '%');
    });
    scene.addEventListener('pointerleave', function () { cert.style.transform = 'rotateY(-8deg) rotateX(4deg)'; });
    cert.style.transform = 'rotateY(-8deg) rotateX(4deg)';
  }
  // counts up once the card is on screen; final value is already in the HTML
  if (reduceMotion || !('IntersectionObserver' in window)) return;
  var done = false;
  new IntersectionObserver(function (en, obs) {
    if (!en[0].isIntersecting || done) return;
    done = true; obs.disconnect();
    var t0 = performance.now(), D = 1600;
    bar.style.setProperty('--fill', '0%');
    requestAnimationFrame(function () { bar.style.setProperty('--fill', '100%'); });
    (function tick(n) {
      var p = Math.min(1, (n - t0) / D), e = 1 - Math.pow(1 - p, 3);
      num.textContent = Math.round(24 * e);
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }, { threshold: 0.4 }).observe(cert);
})();

/* ---------- process timeline progress ---------- */
(function () {
  var steps = $('.steps');
  if (!steps) return;
  var items = $$('li', steps);
  function upd() {
    var r = steps.getBoundingClientRect(), vh = window.innerHeight;
    var p = Math.min(1, Math.max(0, (vh * 0.8 - r.top) / (r.height + vh * 0.25)));
    steps.style.setProperty('--prog', (p * 100).toFixed(1) + '%');
    items.forEach(function (li, i) { li.classList.toggle('on', p >= i / items.length + 0.02); });
  }
  window.addEventListener('scroll', upd, { passive: true }); window.addEventListener('resize', upd); upd();
})();

/* ---------- prices ---------- */
var PRICES = {
  revizii: [
    ['DSG 6/7 trepte (VW, Audi, Seat, Skoda)', 1999], ['DSG DQ381 / DQ500, ulei OEM', 3999], ['DCT 7 trepte D7UF1 (Hyundai, Kia)', 1199],
    ['DCT MPS6 PowerShift (Ford, Dodge)', 1999], ['ZF 5HP / GM 5L40 (BMW, Audi, VW, Porsche)', 1899], ['ZF 6HP (BMW, Audi)', 2699],
    ['ZF 8HP (Audi 0BK)', 2899], ['ZF 8HP (BMW)', 3699], ['ZF 8HP Hybrid 0D5 (Audi, Porsche)', 4699], ['BMW DKG 7 trepte, ulei OEM', 4499],
    ['Porsche 8HP95, ulei OEM', 4699], ['Mercedes 5G-Tronic', 2499], ['Mercedes 7G-Tronic', 2399], ['Mercedes 9G-Tronic', 3799],
    ['Aisin 6 trepte Tiptronic (VW, Audi, Porsche, Seat)', 2599], ['Aisin F33 (Opel, Chevrolet)', 1999], ['Aisin AM6 / AF40 (BMW, Volvo, Alfa Romeo)', 1999],
    ['Aisin F21 (Hyundai)', 1999], ['A8LF1 8 trepte (Kia, Hyundai)', 1899]
  ],
  reparatii: [
    ['Recondiționare convertizor ZF 6HP', 2399], ['Recondiționare convertizor ZF 8HP', 2399], ['Recondiționare convertizor Aisin TF80SC', 2399],
    ['Recondiționare convertizor Mercedes 7G-Tronic', 2599], ['Recondiționare convertizor Mercedes 9G-Tronic', 2899],
    ['Reparație mecatronic DSG DQ381 / DQ500 (senzori presiune)', 5999], ['Set reparație ambreiaj DSG 7 DQ200', 6599],
    ['Recondiționare ambreiaje cutie transfer BMW ATC13', 7199], ['Reparație pompă auxiliară DSG DQ381 (0GC)', 9599],
    ['Reparație cutie DSG DQ381', 11399], ['Înlocuire mecatronic DSG DQ250', 17399], ['Reparație cutie DSG DQ500', 17999],
    ['Înlocuire mecatronic DSG DQ400 Hybrid (0DD)', 19199], ['Reparație cutie S tronic 7 trepte 0B5', 20999],
    ['Reparație S tronic 7 trepte 0CK / 0CL / 0CJ / 0DK, cu ambreiaje', 22199]
  ]
};
function fmt(n) { return n.toLocaleString('ro-RO'); }
(function () {
  var body = $('#price-body'), tabs = $$('.tabs button'), q = $('#price-q');
  if (!body) return;
  var cur = 'revizii';
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function render() {
    var term = q ? norm(q.value.trim()) : '';
    var rows = PRICES[cur].filter(function (r) { return !term || norm(r[0]).indexOf(term) > -1; });
    body.innerHTML = rows.length ? rows.map(function (r) {
      return '<tr><td>' + r[0] + (cur === 'reparatii' ? '<span class="g">24 luni</span>' : '') + '</td><td class="p tnum"><small>de la</small>' + fmt(r[1]) + ' lei</td></tr>';
    }).join('') : '<tr class="empty-row"><td colspan="2">Nu avem încă un preț afișat pentru „' + q.value.replace(/[<>&"]/g, '') + '”. Cere o ofertă și îți răspundem în aceeași zi lucrătoare.</td></tr>';
  }
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      cur = b.dataset.tab;
      tabs.forEach(function (t) { t.setAttribute('aria-selected', t === b ? 'true' : 'false'); });
      $('#price-head-label').textContent = cur === 'revizii' ? 'Revizie cutie automată (ulei, filtru, garnituri, manoperă)' : 'Reparație / recondiționare';
      render();
    });
  });
  if (q) q.addEventListener('input', render);
  render();
})();

/* ---------- open-now status (ora României) ---------- */
(function () {
  var el = $('#open-now');
  if (!el) return;
  try {
    var parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Bucharest', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    var get = function (t) { return (parts.filter(function (p) { return p.type === t; })[0] || {}).value; };
    var d = get('weekday'), m = parseInt(get('hour'), 10) * 60 + parseInt(get('minute'), 10);
    var wk = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].indexOf(d) > -1, sat = d === 'Sat';
    var shop = wk && m >= 360 && m < 870;
    var line = (wk && m >= 420 && m < 1080) || (sat && m >= 540 && m < 900);
    var txt = shop ? 'Atelierul e deschis acum' : line ? 'Atelierul e închis, dar răspundem la telefon și WhatsApp' : 'Închis acum. Lasă-ne o cerere și te sunăm';
    el.classList.toggle('yes', shop || line);
    el.lastChild.textContent = txt;
  } catch (e) { /* keep static text */ }
})();

/* ---------- floating call / WhatsApp choosers ---------- */
(function () {
  $$('[data-pop]').forEach(function (btn) {
    var pop = document.getElementById(btn.dataset.pop);
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      $$('.fab-pop').forEach(function (p) { if (p !== pop) p.hidden = true; });
      pop.hidden = !pop.hidden;
      btn.setAttribute('aria-expanded', pop.hidden ? 'false' : 'true');
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.fab-group')) $$('.fab-pop').forEach(function (p) { p.hidden = true; }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') $$('.fab-pop').forEach(function (p) { p.hidden = true; }); });
})();

/* ---------- multi-step request form ---------- */
(function () {
  var form = $('#lead');
  if (!form) return;
  var steps = $$('.fstep', form), bars = $$('.progress i', form), label = $('.step-label', form);
  var back = $('#f-back'), next = $('#f-next'), send = $('#f-send'), msg = $('.form-msg', form);
  var cur = 0;
  var names = ['Mașina ta', 'Ce problemă are', 'Cum te contactăm'];
  function show(i) {
    cur = i;
    steps.forEach(function (s, k) { s.hidden = k !== i; });
    bars.forEach(function (b, k) { b.classList.toggle('done', k <= i); });
    label.textContent = 'Pasul ' + (i + 1) + ' din ' + steps.length + ': ' + names[i];
    back.hidden = i === 0; next.hidden = i === steps.length - 1; send.hidden = i !== steps.length - 1;
  }
  function fieldOk(el) {
    var f = el.closest('.field'); if (!f) return true;
    var v = (el.value || '').trim(), ok = true, err = '';
    if (el.required && !v) { ok = false; err = 'Completează acest câmp.'; }
    else if (el.type === 'tel' && v && !/^(\+?40|0)7\d{8}$/.test(v.replace(/[\s.\-()]/g, ''))) { ok = false; err = 'Scrie un număr de mobil valid, ex. 0734 607 050.'; }
    else if (el.name === 'an' && v && (+v < 1990 || +v > new Date().getFullYear() + 1)) { ok = false; err = 'Scrie anul de fabricație, ex. 2016.'; }
    f.classList.toggle('invalid', !ok);
    var e = $('.err', f); if (e) e.textContent = err;
    return ok;
  }
  function stepOk(i) {
    var ok = true;
    $$('input,select,textarea', steps[i]).forEach(function (el) { if (!fieldOk(el)) ok = false; });
    if (i === 1 && !$$('input[name="simptome[]"]:checked', form).length && !$('#f-detalii').value.trim()) {
      ok = false; msg.textContent = 'Alege cel puțin un simptom sau descrie problema.';
    } else msg.textContent = '';
    if (!ok) { var bad = $('.invalid input,.invalid select', steps[i]); if (bad) bad.focus(); }
    return ok;
  }
  $$('input,select,textarea', form).forEach(function (el) { el.addEventListener('blur', function () { if (el.value) fieldOk(el); }); });
  next.addEventListener('click', function () { if (stepOk(cur)) { show(cur + 1); var f = $('input,select', steps[cur]); if (f) f.focus(); } });
  back.addEventListener('click', function () { show(cur - 1); });
  function summary(d) {
    return 'Bună ziua! Am trimis o cerere de pe site.\n' +
      'Mașina: ' + d.marca + ' ' + d.model + ', ' + d.an + (d.cutie ? ', cutie ' + d.cutie : '') + '\n' +
      (d.simptome ? 'Simptome: ' + d.simptome + '\n' : '') + (d.detalii ? 'Detalii: ' + d.detalii + '\n' : '') +
      'Nume: ' + d.nume + ', ' + d.localitate;
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!stepOk(cur)) return;
    if (!$('#f-gdpr').checked) { msg.textContent = 'Bifează acordul pentru prelucrarea datelor ca să putem răspunde cererii.'; return; }
    var fd = new FormData(form);
    var d = {}; fd.forEach(function (v, k) { k = k.replace('[]', ''); d[k] = d[k] ? d[k] + ', ' + v : v; });
    send.disabled = true; send.textContent = 'Se trimite…';
    function done() {
      var ok = $('.form-done', form.parentNode);
      form.hidden = true; ok.hidden = false;
      var pref = d.contact === 'WhatsApp';
      $('#done-wa').href = waLink(CONFIG.phones[0].wa, summary(d));
      $('#done-text').textContent = pref
        ? 'Îți scriem pe WhatsApp în cel mult o zi lucrătoare. Dacă vrei să grăbești lucrurile, trimite-ne direct mesajul de mai jos.'
        : 'Te sunăm în cel mult o zi lucrătoare, în intervalul de programări. Poți trimite și pe WhatsApp detaliile, cu poze sau video cu problema.';
      ok.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
    }
    if (!LIVE) { setTimeout(done, 700); return; } // previzualizare: nu se trimite nimic
    fetch(CONFIG.formEndpoint, { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
      .then(function (j) {
        if (j && j.ok) { done(); if (window.fbq) fbq('track', 'Lead'); if (window.gtag) gtag('event', 'generate_lead'); }
        else throw new Error(j && j.error || 'eroare');
      })
      .catch(function (err) {
        send.disabled = false; send.textContent = 'Trimite cererea';
        msg.textContent = 'Cererea nu a plecat (' + (err.message || 'conexiune') + '). Încearcă din nou sau sună-ne la ' + CONFIG.phones[0].label + '.';
      });
  });
  show(0);
})();

/* ---------- chat assistant ---------- */
(function () {
  var box = $('#chat'), open = $('#chat-open');
  if (!box || !open) return;
  var body = $('.chat-body', box), input = $('#chat-in'), formEl = $('.chat-form', box);
  var started = false, lastQ = '';
  function tawkOn() { return CONFIG.tawk.propertyId && window.Tawk_API && window.Tawk_API.maximize; }
  function add(html, who) {
    var d = document.createElement('div'); d.className = 'msg ' + (who || 'bot'); d.innerHTML = html;
    body.appendChild(d); body.scrollTop = body.scrollHeight; return d;
  }
  function quick(list) {
    var q = document.createElement('div'); q.className = 'quick';
    list.forEach(function (t) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = t;
      b.addEventListener('click', function () { q.remove(); ask(t); });
      q.appendChild(b);
    });
    body.appendChild(q); body.scrollTop = body.scrollHeight;
  }
  function bot(html, q) {
    var t = document.createElement('div'); t.className = 'msg bot typing'; t.innerHTML = '<i></i><i></i><i></i>';
    body.appendChild(t); body.scrollTop = body.scrollHeight;
    setTimeout(function () { t.remove(); add(html); if (q) quick(q); }, reduceMotion ? 0 : 650);
  }
  function waBtn(text) {
    return '<br><a class="wa-link" target="_blank" rel="noopener" href="' + waLink(CONFIG.phones[0].wa, text || 'Bună ziua! Am o întrebare despre cutia automată.') + '">Scrie-ne pe WhatsApp</a>';
  }
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function findPrice(s) {
    var n = norm(s).replace(/-/g, ' '), hits = [];
    ['revizii', 'reparatii'].forEach(function (g) {
      PRICES[g].forEach(function (r) {
        var keys = norm(r[0]).replace(/-/g, ' ').match(/dsg|dq\d+|s tronic|0b5|[5689]hp|aisin|tiptronic|[579]g tronic|dkg|dct|mps6|d7uf1|a8lf1|convertizor|mecatronic|ambreiaj|f33|f21|am6|af40/g) || [];
        keys.forEach(function (k) { if (n.indexOf(k) > -1 && hits.indexOf(r) < 0) hits.push(r.concat(g)); });
      });
    });
    return hits.slice(0, 4);
  }
  function answer(q) {
    var n = norm(q);
    var hits = findPrice(q);
    if (hits.length) return [
      'Iată ce am găsit în lista de prețuri:<br>' + hits.map(function (h) { return '• ' + h[0] + ': <b>de la ' + fmt(h[1]) + ' lei</b>' + (h[2] === 'reparatii' ? ' (24 luni garanție)' : ''); }).join('<br>') +
      '<br>Prețul final îl confirmăm după diagnoză. <a href="#preturi">Vezi toate prețurile</a>', ['Cât durează?', 'Vreau o programare']];
    if (/garant/.test(n)) return ['Reparațiile la cutii automate au <b>24 de luni garanție</b>, în scris, pe piese și manoperă. Este cea mai lungă garanție din România pentru acest tip de lucrare.', ['Ce prețuri aveți?', 'Vreau o programare']];
    if (/pret|cost|cat (ma )?costa|tarif|oferta|lei/.test(n)) return ['Revizia unei cutii automate pornește de la <b>1.199 lei</b>, iar reparațiile de la <b>2.399 lei</b>, cu manoperă inclusă. Spune-mi ce cutie ai (DSG, ZF 8HP, 7G-Tronic…) și îți dau prețul exact din listă. <a href="#preturi">Vezi lista</a>', ['DSG', 'ZF 8HP', 'Mercedes 7G-Tronic']];
    if (/programa|programez|rezerv|\bvin\b|loc liber/.test(n) || /vreau o programare/.test(n)) return ['Cel mai rapid e la telefon sau WhatsApp:<br>• <b>' + CONFIG.phones[0].label + '</b><br>• <b>' + CONFIG.phones[1].label + '</b><br>Sau completează <a href="#contact">formularul</a> și te sunăm noi.' + waBtn('Bună ziua! Aș dori o programare pentru cutia automată.'), null];
    if (/program|orar|deschis|ora |ore|cand/.test(n)) return ['Atelier: <b>luni–vineri, 06:00–14:30</b>.<br>Programări la telefon și WhatsApp: <b>luni–vineri 07:00–18:00</b>, <b>sâmbătă 09:00–15:00</b>.', ['Unde sunteți?', 'Vreau o programare']];
    if (/adres|unde|locat|harta|baicoi|ajung/.test(n)) return ['Ne găsești pe <b>' + CONFIG.address + '</b>. <a target="_blank" rel="noopener" href="' + CONFIG.maps + '">Deschide în Google Maps</a>. Vin la noi clienți din toată zona, pe o rază de aproximativ 200 km.', ['Program', 'Vreau o programare']];
    if (/durea|zile|timp|gata|repede/.test(n)) return ['O revizie se face de obicei în aceeași zi. O reparație completă durează în medie <b>5 zile lucrătoare</b>, în funcție de piese. Îți spunem termenul exact după diagnoză.', ['Vreau o programare', 'Garanție']];
    if (/smuc|soc|patin|avari|zgomot|nu (mai )?(cupleaza|schimba|intra)|vibr|scap|sacad|limp|eroare/.test(n)) return ['Simptomele astea pot veni de la ulei degradat, mecatronic, ambreiaje sau convertizor. Nu e bine să mergi mult așa, pentru că o problemă mică poate deveni una scumpă. Îți recomand o <b>diagnoză</b>. Trimite-ne pe WhatsApp un video scurt cu problema și îți spunem ce credem.' + waBtn('Bună ziua! Cutia automată are următoarea problemă: ' + q), null];
    if (/motor|performan|tuning|turbo/.test(n)) return ['Pe lângă cutii, lucrăm și pe <b>motoare de performanță</b>: diagnoză, reparații capitale și refacere după avarii. Spune-ne modelul și problema și revenim cu o estimare.' + waBtn('Bună ziua! Am o întrebare despre motor: ' + q), null];
    if (/problem|defect|stricat/.test(n)) return ['Ce observi la cutie?', ['Smucituri la schimbare', 'Patinează', 'Intră în avarie', 'Zgomot sau vibrații']];
    if (/salut|buna|hello|hei|neata/.test(n)) return ['Bună! Cu ce te pot ajuta?', ['Ce prețuri aveți?', 'Garanție', 'Program', 'Vreau o programare']];
    if (/multum|mersi|ms/.test(n)) return ['Cu plăcere! Drum bun și te așteptăm la atelier.', null];
    return ['Nu am un răspuns gata pentru asta. Un coleg de la atelier îți răspunde pe WhatsApp, de regulă în aceeași zi.' + waBtn('Bună ziua! ' + q), ['Ce prețuri aveți?', 'Program']];
  }
  function ask(q) {
    add(q.replace(/[<>&]/g, ''), 'me'); lastQ = q;
    var a = answer(q); bot(a[0], a[1]);
  }
  function start() {
    if (started) return; started = true;
    bot('Bună! Sunt asistentul automat AutoMatrix. Îți pot spune prețuri, programul și cum ajungi la noi. Pentru un mecanic, te trimit pe WhatsApp.', ['Ce prețuri aveți?', 'Garanție', 'Program', 'Am o problemă la cutie']);
  }
  function toggle(force) {
    if (tawkOn()) { window.Tawk_API.maximize(); return; }
    var show = force !== undefined ? force : box.hidden;
    box.hidden = !show; open.setAttribute('aria-expanded', show ? 'true' : 'false');
    var b = $('.badge', open); if (b) b.remove();
    if (show) { start(); setTimeout(function () { input.focus(); }, 50); }
  }
  open.addEventListener('click', function () { toggle(); });
  $('.chat-close', box).addEventListener('click', function () { toggle(false); open.focus(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) toggle(false); });
  formEl.addEventListener('submit', function (e) { e.preventDefault(); var v = input.value.trim(); if (!v) return; input.value = ''; ask(v); });
  $$('[data-chat]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); toggle(true); }); });
})();

/* ---------- cookie consent (Legea 506/2004, GDPR) ---------- */
(function () {
  var bar = $('#cookie');
  var KEY = 'am_consent', MAX = 1000 * 60 * 60 * 24 * 180; // 6 luni
  var c = store(KEY);
  if (c && (Date.now() - c.ts > MAX || c.v !== 1)) c = null;
  function apply(c) {
    if (!c) return;
    if (c.functional && CONFIG.tawk.propertyId && !window.Tawk_API) {
      window.Tawk_API = window.Tawk_API || {}; window.Tawk_LoadStart = new Date();
      window.Tawk_API.onLoad = function () { window.Tawk_API.hideWidget(); };
      var s = document.createElement('script'); s.async = true; s.src = 'https://embed.tawk.to/' + CONFIG.tawk.propertyId + '/' + CONFIG.tawk.widgetId; s.charset = 'UTF-8'; s.setAttribute('crossorigin', '*');
      document.head.appendChild(s);
    }
    if (c.analytics && CONFIG.ga4 && !window.gtag) {
      var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + CONFIG.ga4; document.head.appendChild(g);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
      gtag('js', new Date()); gtag('config', CONFIG.ga4, { anonymize_ip: true });
    }
    if (c.marketing && CONFIG.metaPixel && !window.fbq) {
      !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', CONFIG.metaPixel); fbq('track', 'PageView');
    }
  }
  function save(o) {
    c = { v: 1, ts: Date.now(), necessary: true, functional: !!o.functional, analytics: !!o.analytics, marketing: !!o.marketing };
    store(KEY, c); if (bar) bar.hidden = true; apply(c);
    if ((!o.functional || !o.analytics || !o.marketing) && (window.Tawk_API || window.gtag || window.fbq)) location.reload();
  }
  if (bar) {
    var prefs = $('.cookie-prefs', bar);
    $('#ck-all').addEventListener('click', function () { save({ functional: 1, analytics: 1, marketing: 1 }); });
    $('#ck-none').addEventListener('click', function () { save({}); });
    $('#ck-set').addEventListener('click', function () {
      prefs.hidden = !prefs.hidden;
      $('#ck-save').hidden = prefs.hidden;
      if (c) { $('#ck-fun').checked = c.functional; $('#ck-ana').checked = c.analytics; $('#ck-mkt').checked = c.marketing; }
    });
    $('#ck-save').addEventListener('click', function () { save({ functional: $('#ck-fun').checked, analytics: $('#ck-ana').checked, marketing: $('#ck-mkt').checked }); });
    if (!c) bar.hidden = false; else apply(c);
  }
  $$('[data-cookie-settings]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault(); if (!bar) return; bar.hidden = false;
      var prefs = $('.cookie-prefs', bar); prefs.hidden = false; $('#ck-save').hidden = false;
      if (c) { $('#ck-fun').checked = c.functional; $('#ck-ana').checked = c.analytics; $('#ck-mkt').checked = c.marketing; }
    });
  });
})();

/* ---------- misc ---------- */
$$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
