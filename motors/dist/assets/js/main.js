/* AutoMatrix Motors – site script. Edit CONFIG to change contact data or enable third-party services. */
var CONFIG = {
  phones: [
    { label: '0734 607 050', tel: '+40734607050', wa: '40734607050' },
    { label: '0734 960 810', tel: '+40734960810', wa: '40734960810' }
  ],
  email: 'service@automatrixmotors.ro',
  address: 'Str. Înfrățirii nr. 111, Băicoi, jud. Prahova',
  maps: 'https://g.page/r/CaVPuXWOanrLEBM',
  booking: 'https://programari.automatrixmotors.ro',
  formEndpoint: 'send.php',
  // Live chat extern (opțional): completează din contul Tawk.to → Administration → Chat Widget.
  // Se încarcă DOAR după acordul pentru cookie-uri funcționale.
  tawk: { propertyId: '', widgetId: '' },
  ga4: 'G-L4WBX29Z4E', // Google Analytics 4 – se încarcă doar cu acord „Analiză”
  metricool: '59a379d500bfeac5d1db9e404d839cb8', // Metricool, hash din codul de urmărire – doar cu acord „Analiză”
  clarity: 'z5osdl9492', // Microsoft Clarity, ID proiect – se încarcă doar cu acord „Analiză”
  metaPixel: '1158968863755327' // Meta Pixel „Automatrix Site” – se încarcă doar cu acord „Marketing”
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
  $$('.nav-drop>button').forEach(function (b) {
    b.addEventListener('click', function () { var d = b.parentNode; var o = d.classList.toggle('open'); b.setAttribute('aria-expanded', o ? 'true' : 'false'); });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.nav-drop')) $$('.nav-drop.open').forEach(function (d) { d.classList.remove('open'); }); });
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

/* ---------- hero logo: turns 360° horizontally and vertically with the pointer ---------- */
(function () {
  var el = $('.logo3d');
  if (!el || reduceMotion) return;
  var tx = -18, ty = -8, x = tx, y = ty, lastMove = 0, visible = true, raf = 0;
  window.addEventListener('pointermove', function (e) {
    tx = (e.clientX / window.innerWidth - 0.5) * 360;
    ty = -(e.clientY / window.innerHeight - 0.5) * 360;
    if (performance.now() - lastMove > 2500) { x = ((x % 360) + 540) % 360 - 180; } // resume without a long spin
    lastMove = performance.now();
    if (!raf) raf = requestAnimationFrame(tick);
  }, { passive: true });
  function tick(now) {
    if (now - lastMove > 2500) { tx += 0.25; ty += (0 - ty) * 0.02; } // slow idle turn
    x += (tx - x) * 0.08; y += (ty - y) * 0.08;
    el.style.transform = 'rotateX(' + y.toFixed(2) + 'deg) rotateY(' + x.toFixed(2) + 'deg)';
    raf = visible && !document.hidden ? requestAnimationFrame(tick) : 0;
  }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible && !raf) raf = requestAnimationFrame(tick); }).observe(el);
  document.addEventListener('visibilitychange', function () { if (!document.hidden && !raf) raf = requestAnimationFrame(tick); });
  raf = requestAnimationFrame(tick);
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
var PRICES = {"revizii": [["Revizie cutie 9G-Tronic Mercedes", 3799], ["Revizie cutie DSG VW", 1999], ["Revizie cutie 7G-Tronic", 2399], ["Revizie cutie BMW 6HP", 2699], ["Revizie cutie BMW 8HP", 3699], ["Revizie cutie 9G-Tronic OEM", 4499], ["Revizie cutie Audi 8HP55A 0BK", 2899], ["Revizie cutie Aisin 6 trepte Tiptronic VW 09D", 2599], ["Revizie cutie Aisin 6 trepte Tiptronic Audi", 2599], ["Revizie cutie Aisin 6 trepte Tiptronic Porsche", 2599], ["Revizie cutie Aisin 6 trepte Tiptronic Seat", 2599], ["Revizie cutie DSG Audi", 1999], ["Revizie cutie DSG Seat", 1999], ["Revizie cutie DSG Skoda", 1999], ["Revizie cutie BMW 5HP", 1899], ["Revizie cutie VW 5HP", 1899], ["Revizie cutie Audi 5HP", 1899], ["Revizie cutie Porsche 5HP", 1899], ["Revizie cutie BMW GM 5L40", 1899], ["Revizie cutie 5G-Tronic", 2499], ["Revizie cutie Audi 6HP", 2699], ["Revizie cutie Aisin F33 Opel", 1999], ["Revizie cutie Aisin F33 Chevrolet", 1999], ["Revizie cutie Aisin F33 Pontiac", 1999], ["Revizie cutie Aisin F33 Saab", 1999], ["Revizie cutie Aisin F33 Renault", 1999], ["Revizie cutie Aisin F33 Volvo", 1999], ["Revizie cutie CVT Temic VGS (722.8)", 1999], ["Revizie cutie VW 4 Trepte", 1899], ["Revizie cutie Audi Multitronic CVT", 2399], ["Revizie cutie DCT MPS6 Volvo", 1999], ["Revizie cutie A750F 5/1 Toyota", 2499], ["Revizie cutie 0C8 8 trepte VW", 2999], ["Revizie cutie 0C8 8 trepte Audi", 2999], ["Revizie cutie 6 trepte 09G VW", 2399], ["Revizie cutie Aisin AF40 4 trepte Saab", 1999], ["Revizie cutie Aisin AF40 4 trepte Alfa Romeo", 1999], ["Revizie cutie Aisin AF40 4 trepte Cadillac", 1999], ["Revizie cutie Aisin AF40 4 trepte Citroen", 1999], ["Revizie cutie Aisin AF40 4 trepte Fiat", 1999], ["Revizie cutie 4F27E 4 trepte Ford", 1999], ["Revizie cutie Aisin AF40 4 trepte Hyundai", 1999], ["Revizie cutie Aisin AF40 4 trepte Jaguar", 1999], ["Revizie cutie Aisin AF40 4 trepte Lancia", 1999], ["Revizie cutie Aisin AF40 4 trepte Rover", 1999], ["Revizie cutie Aisin AF40 4 trepte Lincoln", 1999], ["Revizie cutie Aisin AF40 4 trepte Mazda", 1999], ["Revizie cutie Aisin AF40 4 trepte Mercury", 1999], ["Revizie cutie Aisin AF40 4 trepte Opel", 1999], ["Revizie cutie Aisin AF40 4 trepte Peugeot", 1999], ["Revizie cutie Aisin AF40 4 trepte Renault", 1999], ["Revizie cutie Aisin AF40 4 trepte Volvo", 1999], ["Revizie cutie automată 6T40 6T45 6T50 Opel", 2199], ["Revizie cutie automată 6T40 6T45 6T50 Chevrolet", 2199], ["Revizie cutie automată 6T40 6T45 6T50 Daewoo", 2199], ["Revizie cutie CVT 01J Seat", 2399], ["Revizie cutie BMW 8HP OEM", 3399], ["Revizie cutie BMW 8HP Eco", 1999], ["Revizie cutie BMW 6HP Eco", 2299], ["Revizie cutie BMW 6HP OEM", 2699], ["Revizie cutie 4 trepte AL4 Renault", 1999], ["Revizie cutie 4 trepte AL4 Peugeot", 1799], ["Revizie cutie 4 trepte AL4 Citroen", 1799], ["Revizie cutie 6 trepte JF613E / AJ0 Renault", 1999], ["Revizie cutie 5 trepte Nissan", 2199], ["Revizie cutie 6 trepte JF613E / AJ0 Mitsubishi", 1999], ["Revizie cutie 4 trepte AF17 Opel", 1999], ["Revizie cutie DCT MPS6 Ford", 1999], ["Revizie cutie DCT MPS6 Dodge", 1999], ["Revizie cutie A5HF1 5 trepte Hyundai", 1999], ["Revizie cutie 6DCT470 Mitsubishi", 2199], ["Revizie cutie 6DCT470 Peugeot", 2199], ["Revizie cutie 6DCT470 Citroen", 2199], ["Revizie cutie AW6AX-EL 6 trepte Mazda", 1999], ["Revizie cutie Aisin AM6 6 trepte Volvo", 1999], ["Revizie cutie Aisin AM6 6 trepte Suzuki", 1999], ["Revizie cutie Aisin AM6 6 trepte Peugeot", 1999], ["Revizie cutie Aisin AM6 6 trepte Citroen", 1999], ["Revizie cutie Aisin AM6 6 trepte Mazda", 1999], ["Revizie cutie Aisin AM6 6 trepte Mahindra", 1999], ["Revizie cutie Aisin AM6 6 trepte Luxgen", 1999], ["Revizie cutie Aisin AM6 6 trepte Land Rover", 1999], ["Revizie cutie Aisin AM6 6 trepte Jaguar", 1999], ["Revizie cutie Aisin AM6 6 trepte Hyundai", 1999], ["Revizie cutie Aisin AM6 6 trepte Saab", 1999], ["Revizie cutie Aisin AM6 6 trepte Opel", 1999], ["Revizie cutie Aisin AM6 6 trepte Chevrolet", 1999], ["Revizie cutie Aisin AM6 6 trepte Cadillac", 1999], ["Revizie cutie Aisin AM6 6 trepte Mercury", 1999], ["Revizie cutie Aisin AM6 6 trepte Lincoln", 1999], ["Revizie cutie Aisin AM6 6 trepte Ford", 1999], ["Revizie cutie Aisin AM6 6 trepte Lancia", 1999], ["Revizie cutie Aisin AM6 6 trepte Fiat", 1999], ["Revizie cutie Aisin AM6 6 trepte Alfa Romeo", 1999], ["Revizie cutie Aisin AM6 6 trepte Mini", 1999], ["Revizie cutie Aisin AM6 6 trepte BMW", 1999], ["Revizie cutie 7G-DCT Mercedes", 2399], ["Revizie cutie 6 trepte 09G Skoda", 2399], ["Revizie cutie 6 trepte 09G Seat", 2399], ["Revizie cutie 6 trepte 09G Audi", 2399], ["Revizie cutie 9HP Acura", 2099], ["Revizie cutie 9HP Chrysler", 2099], ["Revizie cutie 9HP Fiat", 2099], ["Revizie cutie 9HP Honda", 2099], ["Revizie cutie 9HP Jeep", 2099], ["Revizie cutie U140F 4/1 Toyota", 2199], ["Revizie cutie DCT MPS6 Renault", 1999], ["Revizie cutie DSG 7 VW", 1099], ["Revizie cutie DSG 7 Skoda", 1099], ["Revizie cutie DSG 7 Audi", 1099], ["Revizie cutie DSG 7 Seat", 1099], ["Revizie cutie Audi S tronic 7 trepte 0CK 0CJ", 2199], ["Revizie cutie DCT250 Powershift Ford", 1099], ["Revizie cutie Land Rover 6HP", 2699], ["Revizie cutie Audi S tronic 7 trepte tracțiune quattro 2014-2020", 3199], ["Revizie cutie Audi S tronic 7 trepte tracțiune quattro 2008-2014", 2799], ["Revizie cutie Land Rover 8HP OEM", 3399], ["Revizie cutie Land Rover 8HP", 2899], ["Revizie cutie A6LF1 6 trepte Hyundai", 2199], ["Revizie cutie Aisin F21 Hyundai", 1999], ["Revizie cutie Jatco JF506E 5 trepte Mitsubishi", 2099], ["Revizie cutie Jatco JF506E 5 trepte Volkswagen", 2099], ["Revizie cutie Jatco JF506E 5 trepte Land Rover", 2099], ["Revizie cutie Jatco JF506E 5 trepte Jaguar", 2099], ["Revizie cutie Jatco JF506E 5 trepte Ford", 2099], ["Revizie cutie Jatco JF506E 5 trepte Mazda", 2199], ["Revizie cutie Jatco JF506E 5 trepte Audi", 2099], ["Revizie cutie A6LF1 6 trepte Kia", 2199], ["Revizie cutie 6F35 6 trepte Ford", 2199], ["Revizie cutie 4HP 4 trepte Mercedes", 1899], ["Revizie cutie 4HP 4 trepte Peugeot", 1899], ["Revizie cutie 4HP 4 trepte Citroen", 1899], ["Revizie cutie 4HP 4 trepte Renault", 1899], ["Revizie cutie 4HP 4 trepte Alfa Romeo", 1899], ["Revizie cutie 4HP 4 trepte Lancia", 1999], ["Revizie cutie 4HP22 4 trepte Land Rover", 1899], ["Revizie cutie Aisin F21 Mini", 1999], ["Revizie cutie GW6AX-EL 6 trepte Mazda", 2699], ["Revizie cutie BMW 5HP30", 1899], ["Revizie cutie 4HP22 4 trepte BMW", 1899], ["Revizie cutie 4HP22 4 trepte Chevrolet", 1899], ["Revizie cutie 4HP22 4 trepte Jaguar", 1899], ["Revizie cutie 4HP22 4 trepte Maserati", 1899], ["Revizie cutie 4HP22 4 trepte Peugeot", 1899], ["Revizie cutie 4HP22 4 trepte Volvo", 1899], ["Revizie cutie Audi 6HP26", 2699], ["Revizie cutie 8 trepte Porsche Cayenne", 2999], ["Revizie cutie BMW GM 6L50", 1899], ["Revizie cutie CVT RE0F11A 1/1 Nissan", 2599], ["Revizie cutie DSG DQ250 VW OEM", 3399], ["Revizie cutie DSG DQ250 Audi OEM", 3399], ["Revizie cutie DSG DQ250 Skoda OEM", 3399], ["Revizie cutie DSG DQ250 Seat OEM", 3399], ["Revizie cutie 7G-Tronic OEM", 2699], ["Revizie cutie CVT RE0F10G 1/1 Nissan", 2399], ["Revizie cutie Skoda 5HP", 1899], ["Revizie cutie BMW GM 5L50", 1899], ["Revizie cutie CVT FK0 1/1 Renault", 1999], ["Revizie cutie CVT RE0FO9 1/1 Nissan", 2299], ["Revizie cutie Aisin 8 trepte BMW", 2199], ["Revizie cutie Aisin 8 trepte Mini", 2199], ["Revizie cutie Aisin 8 trepte Lexus", 2199], ["Revizie cutie Aisin 8 trepte Opel", 2199], ["Revizie cutie Aisin 8 trepte Peugeot", 2199], ["Revizie cutie Aisin 8 trepte Toyota", 2199], ["Revizie cutie Aisin 8 trepte VW", 2199], ["Revizie cutie Aisin 8 trepte Volvo", 2199], ["Revizie cutie Jatco JF404E 4 trepte Volkswagen", 1999], ["Revizie cutie Skoda 4 trepte", 1999], ["Revizie cutie VW 4 trepte", 1999], ["Revizie cutie CVT Honda", 1999], ["Revizie cutie U660E 6 trepte Toyota", 2099], ["Revizie cutie 5 trepte 545RFE", 2399], ["Revizie cutie 7 trepte BMW DKG", 3099], ["Revizie cutie 6 trepte Nissan RE6F01A", 1999], ["Revizie cutie Land Rover GM 5L40", 1899], ["Revizie cutie DCT MPS6 Ford OEM", 2399], ["Revizie cutie BMW 8HP Hybrid", 4699], ["Revizie cutie BMW 8HP Hybrid OEM", 4599], ["Revizie cutie BTR M11 6 trepte Ssangyong", 1999], ["Revizie cutie 7G-DCT Mercedes OEM", 3199], ["Revizie cutie 4F27E 4 trepte Mazda", 2399], ["Revizie cutie Audi 8HP55AH Hybrid 0BW", 3399], ["Revizie cutie 6 trepte Infiniti RE6F01A", 2099], ["Revizie cutie CVT F1CJA 1/1 Mitsubishi", 2399], ["Revizie cutie 9HP Land Rover", 2299], ["Revizie cutie CVT CFT23", 1999], ["Revizie cutie 5G-Tronic OEM", 1999], ["Revizie cutie CVT GACVT16Z", 1799], ["Revizie cutie Audi S tronic 7 trepte tracțiune quattro OEM", 4499], ["Revizie cutie Audi Multitronic CVT OEM", 3899], ["Revizie cutie Seat Multitronic CVT OEM", 3899], ["Revizie cutie Jaguar 6HP", 2699], ["Revizie cutie Aisin GA6F21WA Mini", 1999], ["Revizie cutie Audi 4 trepte", 2199], ["Revizie cutie DC4 Renault", 699], ["Revizie cutie TG-81SC 8 trepte Volvo", 2199], ["Revizie cutie Audi 8HP 0D5 OEM", 3799], ["Revizie cutie P313 6 trepte Lexus", 2299], ["Revizie cutie DW5 Renault", 1099], ["Revizie cutie 7DCT300 Powershift Ford", 1799], ["Revizie cutie Ford Mustang 10 trepte 10R80", 4499], ["Revizie cutie Porsche 5HP OEM", 2699], ["Revizie cutie CVT Jatco JF015 Renault", 2599], ["Revizie cutie RE7R24A 7G-Tronic", 2799], ["Revizie cutie CVT RE0F11A 1/1 Dacia", 2599], ["Revizie cutie GM 4T65E 4 trepte Volvo", 1899], ["Revizie cutie 6R80 6 trepte Ford", 2599], ["Revizie cutie CVT Hybrid HSD Toyota", 1899], ["Revizie cutie Aston Martin 6HP OEM", 3199], ["Revizie cutie Alfa Romeo 8HP OEM", 3399], ["Revizie cutie Alfa Romeo 8HP", 2899], ["Revizie cutie Audi S tronic 7 trepte 0CK, cu filtre", 4499], ["Revizie cutie Audi 8HP 0D5 Hybrid OEM", 4699], ["Revizie cutie Porsche 8HP 0D5 Hybrid OEM", 4699], ["Revizie cutie Audi S tronic 7 trepte 0CK, cu baie de ulei", 4899], ["Revizie cutie 8F40 8 trepte Ford", 2499], ["Revizie cutie 7DCT300 Mercedes", 1799], ["Revizie cutie 9G-Tronic Hybrid OEM", 4899], ["Revizie cutie ZF 7DT75 PDK 7 trepte Porsche", 3599], ["Revizie cutie Porsche 8HP95 OEM", 4699], ["Revizie cutie DSG DQ381/DQ500 Seat OEM", 3999], ["Revizie cutie DSG DQ381/DQ500 VW OEM", 3999], ["Revizie cutie ATN8 AMN8 8 trepte Peugeot", 2699], ["Revizie cutie 8F40 8 trepte Ford OEM", 3199], ["Revizie cutie Toyota K CVT", 2599], ["Revizie cutie 8G-DCT Mercedes", 2599], ["Revizie cutie DCT 7 Trepte D7UF1", 1199], ["Revizie cutie 7DCT300 BMW Mini Cooper", 1799], ["Revizie cutie A8LF1 8 trepte Hyundai", 1899], ["Revizie cutie A8LF1 8 trepte Kia", 1899], ["Revizie cutie 7 trepte BMW DKG OEM", 4499], ["Revizie cutie PDK 7 trepte Porsche Macan 0B5", 3999]], "reparatii": [["Înlocuire mecatronic DSG DQ250 VW", 17399], ["Înlocuire volantă cu masă dublă, cutie DSG VW", 6599], ["Înlocuire volantă cu masă dublă, cutie DSG Seat", 6599], ["Înlocuire volantă cu masă dublă, cutie DSG Audi", 6599], ["Înlocuire volantă cu masă dublă, cutie DSG Skoda", 6599], ["Înlocuire volantă cu masă dublă, cutie DSG 4Motion VW", 7799], ["Înlocuire volantă cu masă dublă, cutie DQ200 7 Seat", 5499], ["Înlocuire volantă cu masă dublă, cutie DQ200 Skoda", 5499], ["Înlocuire volantă cu masă dublă, cutie DQ200 Audi", 5499], ["Set garnituri mecatronic ZF 6HP19", 1199], ["Set reparație mecatronic DSG 7 DQ200 VW", 4199], ["Set reparație mecatronic DSG 7 DQ200 Audi", 4199], ["Set reparație mecatronic DSG 7 DQ200 Skoda", 4199], ["Set reparație mecatronic DSG 7 DQ200 Seat", 4199], ["Set reparație modul Multitronic 0AW", 5899], ["Set garnituri mecatronic ZF 6HP26", 1199], ["Set reparație ambreiaj DSG 7 DQ200 Seat", 6599], ["Set reparație ambreiaj DSG 7 DQ200 VW", 6599], ["Set reparație ambreiaj DSG 7 DQ200 Skoda", 6599], ["Set reparație ambreiaj DSG 7 DQ200 Audi", 6599], ["Înlocuire volantă cu masă dublă, cutie DSG 0BH 0GC DQ381 DQ500 Audi", 7799], ["Înlocuire volantă cu masă dublă, cutie DSG 7 VW", 4999], ["Recondiționare convertizor de cuplu BMW 6 trepte 6HP", 7099], ["Recondiționare convertizor de cuplu BMW 8 trepte 8HP", 9499], ["Recondiționare convertizor de cuplu Audi 5 trepte 5HP", 7099], ["Recondiționare convertizor de cuplu Audi 8 trepte 8HP", 9099], ["Recondiționare convertizor de cuplu Audi 6 trepte 6HP", 7799], ["Recondiționare convertizor de cuplu Mercedes 5 trepte 5G-Tronic", 7499], ["Recondiționare convertizor de cuplu Mercedes 7 trepte 7G-Tronic", 7699], ["Recondiționare convertizor de cuplu Mercedes 9 trepte 9G-Tronic", 11799], ["Înlocuire volantă cu masă dublă, cutie CVT Audi Multitronic", 5799], ["Înlocuire volantă cu masă dublă, cutie CVT Seat Multitronic", 5799], ["Set reparație ambreiaj DCT 7 trepte Hyundai D7UF1", 11399], ["Set reparație ambreiaj DCT 7 trepte D7UF1 Kia", 11399], ["Set recondiționare ambreiaje S tronic 7 trepte Audi", 9599], ["Set înlocuire ambreiaje PDK 7 trepte Porsche", 11999], ["Recondiționare convertizor de cuplu Audi Q7 Aisin 6 trepte", 7899], ["Recondiționare convertizor de cuplu VW Touareg Aisin 6 trepte", 7899], ["Recondiționare convertizor de cuplu Porsche Cayenne Aisin 6 trepte", 7899], ["Recondiționare convertizor de cuplu Porsche Aisin 8 trepte", 9499], ["Recondiționare convertizor de cuplu VW Touareg Aisin 8 trepte", 8299], ["Recondiționare convertizor de cuplu Audi Q7 Aisin 8 trepte", 8299], ["Recondiționare ambreiaje cutie de transfer BMW ATC350 / ATC450", 5999], ["Kit electrovalve cutie AL4 DP0 Renault", 4199], ["Kit electrovalve cutie AL4 DP0 Citroen", 4199], ["Kit electrovalve cutie AL4 DP0 Peugeot", 4199], ["Kit electrovalve cutie 6HP Audi", 4999], ["Kit electrovalve cutie 6HP BMW", 4799], ["Set înlocuire mecatronic DSG 7 DQ200 Seat", 11899], ["Set înlocuire mecatronic DSG 7 DQ200 Skoda", 11899], ["Set înlocuire mecatronic DSG 7 DQ200 Audi", 11899], ["Set înlocuire mecatronic DSG 7 DQ200 VW", 11899], ["Înlocuire ambreiaje cutie BMW 6 trepte 6HP", 9499], ["Înlocuire ambreiaje cutie Audi 6 trepte 6HP", 10399], ["Înlocuire volantă cu masă dublă, cutie S tronic Audi DL501", 7799], ["Înlocuire ambreiaje cutie Land Rover 6 trepte 6HP", 10399], ["Recondiționare mecatronic BMW 6HP", 6599], ["Recondiționare mecatronic Audi 6HP", 7199], ["Înlocuire Actuator / Motor cutie de transfer BMW ATC350, ATC450, ATC35L, ATC45L", 8799], ["Set reparație cutie automată Mercedes CVT W169 / W245", 4399], ["Set reparație mecatronic DSG DQ250 VW", 4799], ["Recondiționare mecatronic BMW 8HP", 7799], ["Recondiționare mecatronic Audi 8HP", 6599], ["Pachet reparație cutie mecanică DSG 7 DQ200 VW", 7199], ["Pachet reparație cutie mecanică DSG 7 DQ200 Audi", 7199], ["Pachet reparație cutie mecanică DSG 7 DQ200 Skoda", 7199], ["Pachet reparație cutie mecanică DSG 7 DQ200 Seat", 7199], ["Înlocuire ambreiaje cutie BMW 8 trepte 8HP", 10699], ["Înlocuire ambreiaje cutie Audi 8 trepte 8HP", 11399], ["Înlocuire kit ambreiaje DSG 02E / 0D9 DQ250 VW", 7199], ["Înlocuire kit ambreiaje DSG 02E / 0D9 DQ250 Audi", 7199], ["Înlocuire kit ambreiaje DSG 02E / 0D9 DQ250 Skoda", 7199], ["Înlocuire kit ambreiaje DSG 02E / 0D9 DQ250 Seat", 7199], ["Înlocuire bloc de valve Aisin TF-80SC, AF40-6, AM6, AW6A-EL, TF-81SC, 6 trepte Opel", 9599], ["Înlocuire kit ambreiaje Multitronic CVT 0AW - 0AN", 9499], ["Înlocuire ambreiaje cutie EDC DC4 - 6DCT250", 12499], ["Înlocuire ambreiaje cutie EDC DW6 - 6DCT451", 14099], ["Înlocuire ambreiaje cutie 7G-Tronic 722.9xx", 10199], ["Înlocuire placă electronică cutie Mercedes 5 trepte 5G-Tronic", 4599], ["Pachet reparație mecatronic 0B5 S tronic 7 trepte Audi", 8199], ["Reparație cutie automată înlocuire mecatronic Audi S tronic 7 trepte 0CK, 0CL, 0CJ, 0DK", 21599], ["Reparație cutie automată DSG DQ381 VW", 11399], ["Reparație cutie automată DSG DQ381 Seat", 11399], ["Reparație cutie automată DSG DQ500 Audi", 17999], ["Reparație cutie automată 0B5 S tronic 7 trepte Audi", 20999], ["Reparație completă cutie automată MPS6 Powershift - 6DCT450", 15599], ["Reparație completă cutie automată MPS6 Powershift - 6DCT450 Volvo", 15599], ["Reparație completă cutie automată Powershift Gen 2 - 6DCT451 Volvo", 16199], ["Reparație completă cutie automată Powershift Gen 2 - 6DCT451 Ford", 16199], ["Reparație completă cutie automată DW6 Powershift Gen 2 - 6DCT451 Renault", 16199], ["Reparație cutie de transfer Mercedes DCS 4 matic", 5399], ["Reparație cutie automată S tronic 7 trepte 0B5 eroare P179E sau P179F Drive Position Senzor G676 Audi", 11199], ["Recondiționare convertizor de cuplu cutie automată GM 6T40 6T45 6T50", 7899], ["Înlocuire ambreiaje cutie EDC7 DW5 - 7DCT300", 11899], ["Reparație cutie automată înlocuire volantă Audi S tronic 7 trepte 0CK, 0CL, 0CJ, 0DK", 9399], ["Pachet reparație cutie automată DSG7 DQ200 VW", 7199], ["Set reparație ambreiaj DSG 7 DQ200 Hybrid VW", 8999], ["Pachet reparație cutie automată DSG7 DQ250 VW", 8399], ["Reparație cutie automată înlocuire ambreiaje Audi S tronic 7 trepte 0CK, 0CL, 0CJ, 0DK", 22199], ["Reparație completă cutie automată Mitsubishi Powershift - 6DCT470", 17399], ["Reparație completă cutie automată Citroen și Peugeot Powershift - 6DCT470", 16199], ["Înlocuire kit ambreiaje DSG 0BH 0GC DQ381 DQ500 Seat", 8299], ["Înlocuire kit ambreiaje DSG 0BH 0GC DQ381 DQ500 VW", 8299], ["Înlocuire kit ambreiaje DSG 0BH 0GC DQ381 DQ500 Skoda", 8299], ["Înlocuire kit ambreiaje DSG 0BH 0GC DQ381 DQ500 Audi", 8299], ["Înlocuire ambreiaje cutie Powershift MPS6 6DCT250", 11299], ["Înlocuire ambreiaje cutie Powershift 6DCT250", 11299], ["Înlocuire bloc de valve DSG 7 DQ200 VW", 7799], ["Înlocuire calculator TCU DSG 7 DQ200 VW", 7799], ["Recondiționare ambreiaje cutie de transfer BMW ATC300 / ATC400 / ATC500 ATC700", 5999], ["Reparație cutie automată CVT JF017E, RE0F10E, RE0F10G, CVT8, FK0, FR8", 18599], ["Înlocuire ambreiaje cutie 9G-Tronic 725.0", 11399], ["Reparație cutie automată CVT JF015E / JF016E / RE0F11 CVT7", 17999], ["Reparație cutie automată PDK Porsche ZF 7DT eroare P1731 P1732 senzor de distanță", 25199], ["Recondiționare ambreiaje cutie de transfer 95B PDK Porsche Macan", 4799], ["Înlocuire ambreiaje cutie Land Rover 8 trepte 8HP", 11599], ["Reparație completă cutie automată BMW/Mini GA8F22AW", 17399], ["Înlocuire ambreiaje cutie Audi 0D5 ZF 8 trepte 8HP65A", 15199], ["Înlocuire calculator TCU DSG 7 DQ200 Gen 2 VW", 8299], ["Reparație cutie automată DSG DQ500 VW", 17999], ["Înlocuire mecatronic cutie 9G-Tronic 725.0", 13099], ["Reparație completă cutie automată Ford 8F35 / 8F40", 17399], ["Recondiționare variatoare și ambreiaje Multitronic CVT 0AW - 0AN", 17899], ["Recondiționare ambreiaje cutie de transfer ATC13", 7199], ["Reparație mecatronic Înlocuire senzori presiune DSG DQ381 DQ500 VW", 5999], ["Set Reparație pompă auxiliară 0GC DSG DQ381", 9599], ["Înlocuire mecatronic DSG 0DD DQ400 Hybrid VW", 19199], ["Reparație cutie de transfer Mercedes VITO/VIANO W639 4MATIC", 19099]]};
function fmt(n) { return n.toLocaleString('ro-RO'); }
(function () {
  var all = $('#pall');
  if (!all) return;
  var rows = $$('.prow', all), groups = $$('.pgroup', all), tabs = $$('.tabs button'), q = $('#price-q'), empty = $('#price-empty'), kind = '';
  function norm(t) { return t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function apply() {
    var terms = norm(q.value.trim()).split(/\s+/).filter(Boolean), shown = 0;
    rows.forEach(function (r) {
      var ok = (!kind || r.dataset.k === kind) && terms.every(function (t) { return r.dataset.s.indexOf(t) > -1; });
      r.hidden = !ok; if (ok) shown++;
    });
    groups.forEach(function (g) { g.hidden = !$$('.prow:not([hidden])', g).length; });
    empty.hidden = shown > 0;
  }
  tabs.forEach(function (b) { b.addEventListener('click', function () { kind = b.dataset.kind; tabs.forEach(function (t) { t.setAttribute('aria-selected', t === b ? 'true' : 'false'); }); apply(); }); });
  q.addEventListener('input', apply);
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
      '<br>Prețul final îl confirmăm după diagnoză. <a href="/preturi-cutii-automate">Vezi toate prețurile</a>', ['Cât durează?', 'Vreau o programare']];
    if (/garant/.test(n)) return ['Reparațiile la cutii automate au <b>24 de luni garanție, fără limită de kilometri</b>, în scris, pe piese și manoperă. Este cea mai lungă garanție din România pentru acest tip de lucrare.', ['Ce prețuri aveți?', 'Vreau o programare']];
    if (/pret|cost|cat (ma )?costa|tarif|oferta|lei/.test(n)) return ['Revizia unei cutii automate pornește de la <b>699 lei</b>, iar reparațiile de la <b>1.199 lei</b>, cu manoperă inclusă. Spune-mi ce cutie ai (DSG, ZF 8HP, 7G-Tronic…) și îți dau prețul exact din listă. <a href="/preturi-cutii-automate">Vezi lista</a>', ['DSG', 'ZF 8HP', 'Mercedes 7G-Tronic']];
    if (/programa|programez|rezerv|\bvin\b|loc liber/.test(n) || /vreau o programare/.test(n)) return ['Te poți programa singur online, alegând ziua și ora: <a target="_blank" rel="noopener" href="' + CONFIG.booking + '">programari.automatrixmotors.ro</a>.<br>Sau la telefon și WhatsApp:<br>• <b>' + CONFIG.phones[0].label + '</b><br>• <b>' + CONFIG.phones[1].label + '</b><br>Sau completează <a href="#contact">formularul</a> și te sunăm noi.' + waBtn('Bună ziua! Aș dori o programare pentru cutia automată.'), null];
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
    if (c.analytics && CONFIG.clarity && !window.clarity) {
      (function (w, d, t, i) { w.clarity = w.clarity || function () { (w.clarity.q = w.clarity.q || []).push(arguments); }; var s = d.createElement(t); s.async = 1; s.src = 'https://www.clarity.ms/tag/' + i; d.head.appendChild(s); })(window, document, 'script', CONFIG.clarity);
      window.clarity('consent');
    }
    if (c.analytics && CONFIG.metricool && !window.beTracker && !window.__mtc) {
      window.__mtc = 1; var m = document.createElement('script'); m.type = 'text/javascript'; m.src = 'https://tracker.metricool.com/resources/be.js';
      m.onload = function () { try { window.beTracker.t({ hash: CONFIG.metricool }); } catch (e) {} }; document.head.appendChild(m);
    }
    if (c.marketing && CONFIG.metaPixel && !window.fbq) {
      !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', CONFIG.metaPixel); fbq('track', 'PageView');
    }
  }
  function save(o) {
    c = { v: 1, ts: Date.now(), necessary: true, functional: !!o.functional, analytics: !!o.analytics, marketing: !!o.marketing };
    store(KEY, c); if (bar) bar.hidden = true; apply(c);
    if ((!o.functional || !o.analytics || !o.marketing) && (window.Tawk_API || window.gtag || window.fbq || window.clarity)) location.reload();
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

/* ---------- open a price row linked by #id (e.g. from the fault-codes page) ---------- */
(function () {
  function openHash() {
    var id = location.hash.slice(1); if (!id) return;
    var el = document.getElementById(id);
    if (el && el.tagName === 'DETAILS') { el.open = true; setTimeout(function () { el.scrollIntoView({ block: 'start', behavior: reduceMotion ? 'auto' : 'smooth' }); }, 60); }
  }
  window.addEventListener('hashchange', openHash); openHash();
})();

/* ---------- facts strip: numbers count up to the real value when the strip comes into view ---------- */
(function () {
  var nums = $$('.facts .cnt');
  if (!nums.length || reduceMotion || !('IntersectionObserver' in window)) return;
  var strip = $('.facts'), done = false;
  new IntersectionObserver(function (en, obs) {
    if (!en[0].isIntersecting || done) return;
    done = true; obs.disconnect();
    nums.forEach(function (el, i) {
      var to = parseInt(el.dataset.to, 10), D = 1400 + i * 120, t0 = performance.now() + i * 90;
      el.textContent = '0';
      (function tick(now) {
        var p = Math.min(1, Math.max(0, (now - t0) / D)), e = 1 - Math.pow(1 - p, 4);
        el.textContent = Math.round(to * e);
        if (p < 1) requestAnimationFrame(tick);
      })(performance.now());
    });
  }, { threshold: 0.45 }).observe(strip);
})();

/* ---------- măsurarea acțiunilor importante (doar dacă analiza e acceptată) ---------- */
(function () {
  function track(name, params) {
    try { if (window.gtag) gtag('event', name, params || {}); } catch (e) {}
    try { if (window.clarity) clarity('event', name); } catch (e) {}
    try { if (window.fbq && (name === 'phone_call' || name === 'whatsapp_click' || name === 'booking_click')) fbq('track', 'Contact', { method: name }); } catch (e) {}
  }
  window.amTrack = track;
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    var h = a.getAttribute('href') || '', where = location.pathname;
    if (h.indexOf('tel:') === 0) track('phone_call', { phone: h.slice(4), page: where });
    else if (/wa\.me\//.test(h)) track('whatsapp_click', { phone: (h.match(/wa\.me\/(\d+)/) || [])[1] || '', page: where });
    else if (/programari\.automatrixmotors\.ro/.test(h)) track('booking_click', { page: where });
    else if (/^mailto:/.test(h)) track('email_click', { page: where });
  }, true);
  document.addEventListener('toggle', function (e) {
    var d = e.target; if (!d.classList || !d.classList.contains('prow') || !d.open) return;
    var n = d.querySelector('.pn'), p = d.querySelector('.pp');
    track('view_price_item', { item_name: n ? n.firstChild.textContent.trim() : d.id, price: p ? p.textContent.trim() : '' });
  }, true);
  ['code-q', 'price-q'].forEach(function (id) {
    var q = document.getElementById(id), tm; if (!q) return;
    q.addEventListener('input', function () {
      clearTimeout(tm); var v = q.value.trim(); if (v.length < 3) return;
      tm = setTimeout(function () { track('search', { search_term: v.toUpperCase(), search_type: id === 'code-q' ? 'cod_eroare' : 'pret' }); }, 1500);
    });
  });
})();
