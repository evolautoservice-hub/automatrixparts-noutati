# -*- coding: utf-8 -*-
"""Static site generator for automatrixmotors.ro.  python3 build.py prod|preview"""
import json, re, sys, base64, pathlib, html, os, hashlib
from data import *
from codes import CODES, CODE_MAP, enrich, fixes_for
from boxcodes import BOXES, BOX_BY_SLUG, ROWS, KIND_ORDER, DIAG_ROWS, DIAG_OPS, DIAG_PARTS
from catalog import family
enrich(CATALOG)


def _base(k):
    return re.split(r"[-\s(]", k)[0].upper()


def box_rows(b, kind=None, limit=None, with_diag=True):
    """Price rows (catalogue + diagnosis rows) that belong to a gearbox, optionally filtered by code kind."""
    rows = [c for c in CATALOG + DIAG if re.search(b["match"], c["name"], re.I)]
    if kind:
        rx = ROWS[kind]
        if kind == "oil":
            sel = [c for c in rows if c["kind"] == "revizie"] + [c for c in rows if c["kind"] == "reparatie" and re.search(rx, c["name"], re.I)]
        else:
            sel = [c for c in rows if c["kind"] == "reparatie" and re.search(rx, c["name"], re.I)]
        rows = sel or [c for c in rows if c["kind"] == "reparatie"]
    if not with_diag:
        rows = [c for c in rows if c.get("price")]
    out, names = [], set()
    for c in sorted(rows, key=lambda c: (c.get("price") is None, c["kind"] != "reparatie", c.get("price") or 0)):
        key = re.sub(r"\b(VW|Audi|Skoda|Seat|Volvo|Ford|Renault|Peugeot|Citroen|Opel|Kia|Hyundai|BMW|Land Rover|Mini)\b", "", c["name"]).strip()
        if key in names:
            continue
        names.add(key); out.append(c)
        if limit and len(out) >= limit:
            break
    return out


# rânduri noi: cutii pe care le reparăm, cu preț stabilit după diagnoză
DIAG = []
for _name, _slug in DIAG_ROWS:
    _b = BOX_BY_SLUG[_slug]
    _sym = []
    for _c in _b["codes"]:
        for _x in _c["sym"]:
            if _x not in _sym:
                _sym.append(_x)
    _rid = "l-" + re.sub(r"[^a-z0-9]+", "-", "".join(ch for ch in __import__("unicodedata").normalize("NFD", _name.lower()) if __import__("unicodedata").category(ch) != "Mn")).strip("-")[:80]
    DIAG.append({"name": _name, "kind": "reparatie", "price": None, "fam": _b["fam"], "ops": DIAG_OPS, "parts": DIAG_PARTS,
                 "rid": _rid, "symptoms": _sym[:4], "codes": [], "box": _slug})


def attach_box_codes():
    for c in CATALOG + DIAG:
        picked = []
        for b in BOXES:
            if not re.search(b["match"], c["name"], re.I):
                continue
            cands = [x for x in b["codes"] if not x["main"].startswith("Fără cod")]
            if c["kind"] == "revizie":
                cands = [x for x in cands if x["oil"]][:4]
            elif c.get("price") is not None:
                cands = [x for x in cands if re.search(ROWS[x["kind"]], c["name"], re.I)]
            cands.sort(key=lambda x: KIND_ORDER.index(x["kind"]))
            for x in cands:
                picked.append({"k": x["main"], "href": url(b["slug"]) + "#" + x["id"], "t": x["title"], "all": x["codes"]})
        c["bcodes"] = picked[:6]
        if c["kind"] == "revizie" and picked and not c.get("symptoms"):
            c["codes"] = []


MODE = sys.argv[1] if len(sys.argv) > 1 else "prod"
PREVIEW = MODE == "preview"
ROOT = pathlib.Path(os.environ.get("AM_ROOT") or pathlib.Path(__file__).resolve().parent.parent)
SRC = ROOT / "site2"
OUT = ROOT / ("preview2" if PREVIEW else "dist")
OUT.mkdir(parents=True, exist_ok=True)

CSS = (SRC / "assets/css/style.css").read_text()
MAINJS = (SRC / "assets/js/main.js").read_text().replace("/*PRICES*/null", json.dumps(PRICES, ensure_ascii=False))
SCENEJS = (SRC / "assets/js/scene.js").read_text()
FONTS = "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap"


def b64(p, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode((SRC / p).read_bytes()).decode())


IMG = {
    "emb": b64("assets/img/emblema.webp", "image/webp") if PREVIEW else "/assets/img/emblema.webp",
    "logo": b64("assets/img/logo-automatrix.webp", "image/webp") if PREVIEW else "/assets/img/logo-automatrix.webp",
    "dark": b64("assets/img/emblema-dark.webp", "image/webp") if PREVIEW else "/assets/img/emblema-dark.webp",
}


def url(slug):
    """internal link"""
    if PREVIEW:
        return "./" if slug == "" else slug + ".html"
    return "/" if slug == "" else "/" + slug


def canon(slug):
    return SITE + ("/" if slug == "" else "/" + slug)


def esc(s):
    return html.escape(s, quote=True)


ALL_SERVICES = PAGES  # services incl. guides
PRICE_PAGE = dict(slug="preturi-cutii-automate", nav="Prețuri", navsub="Revizii și reparații, cu manoperă")
CODES_NAV = dict(slug="coduri-eroare-cutie-automata", nav="Coduri de eroare", navsub="P0700, P0741, P17BF și altele")
ARTICLES_NAV = dict(slug="articole", nav="Articole și sfaturi", navsub="Ghiduri despre cutii automate")

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
<symbol id="i-phone" viewBox="0 0 24 24"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.15l-.3-.18-3 .78.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.25-.12-1.46-.72-1.69-.8s-.39-.12-.55.12-.63.8-.78.96-.29.18-.53.06a6.7 6.7 0 0 1-3.3-2.9c-.25-.43.25-.4.71-1.33a.45.45 0 0 0-.02-.42c-.06-.12-.55-1.33-.76-1.82s-.4-.41-.55-.42h-.47a.9.9 0 0 0-.65.3 2.73 2.73 0 0 0-.85 2.03 4.74 4.74 0 0 0 1 2.52 10.86 10.86 0 0 0 4.16 3.68c1.55.67 2.16.73 2.93.61a2.5 2.5 0 0 0 1.65-1.16 2.04 2.04 0 0 0 .14-1.16c-.06-.1-.22-.16-.46-.28z"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" d="M4 5h16v11H9l-5 4z"/><path stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="M8 10.5h8"/></symbol>
<symbol id="i-send" viewBox="0 0 24 24"><path fill="currentColor" d="M3 20.5v-6l9-2.5-9-2.5v-6L22 12z"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M20 7 10 17l-5-5"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M12 3 4.5 6v5.5c0 4.6 3.2 8.3 7.5 9.5 4.3-1.2 7.5-4.9 7.5-9.5V6z"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="m8.5 12 2.5 2.5 4.5-5"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="1.6"/><path stroke="currentColor" stroke-width="1.6" stroke-linecap="round" d="m20 20-3.5-3.5"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M4 12h15M13 6l6 6-6 6"/></symbol>
<symbol id="i-down" viewBox="0 0 10 10"><path fill="none" stroke="currentColor" stroke-width="1.4" d="m1.5 3.5 3.5 3.5 3.5-3.5"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.5" d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.5"/></symbol>
<symbol id="i-fb" viewBox="0 0 24 24"><path fill="currentColor" d="M13.5 21v-7.7h2.6l.4-3h-3V8.4c0-.87.24-1.46 1.5-1.46h1.6V4.24A21 21 0 0 0 14.3 4c-2.3 0-3.9 1.4-3.9 4v2.3H7.8v3h2.6V21z"/></symbol>
<symbol id="i-ig" viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor"/></symbol>
<symbol id="i-tt" viewBox="0 0 24 24"><path fill="currentColor" d="M16.6 3c.3 2.2 1.6 3.6 3.9 3.8v2.7a7 7 0 0 1-3.8-1.1v6.3c0 3.3-2.3 5.8-5.6 5.8a5.6 5.6 0 0 1-5.6-5.6c0-3.4 3-6 6.5-5.5v2.9a2.7 2.7 0 0 0-3.6 2.6 2.6 2.6 0 0 0 2.7 2.7c1.6 0 2.7-1 2.7-3.1V3z"/></symbol>
</svg>"""


def brand(extra=""):
    return f'<a class="brand{extra}" href="{url("")}" aria-label="AutoMatrix Motors, prima pagină"><img src="{IMG["emb"]}" width="200" height="183" alt=""><span class="brand-txt"><b>AUTOMATRIX</b><span>GEARBOX SPECIALIST</span></span></a>'


def header(active=""):
    items = "".join(f'<a href="{url(p["slug"])}">{esc(p["nav"])}<small>{esc(p["navsub"])}</small></a>' for p in [x for x in ALL_SERVICES if not x.get("brand")] + [PRICE_PAGE, CODES_NAV, ARTICLES_NAV])
    def cur(s): return ' aria-current="page"' if active == s else ""
    return f"""<header class="top">
<div class="wrap">
{brand()}
<nav class="nav" id="nav" aria-label="Meniu principal">
<div class="nav-drop"><button type="button" aria-expanded="false" aria-haspopup="true">Servicii<svg aria-hidden="true"><use href="#i-down"/></svg></button><div class="drop">{items}</div></div>
<a href="{url("preturi-cutii-automate")}"{cur("preturi-cutii-automate")}>Prețuri</a>
<a href="{url("lucrari-efectuate")}"{cur("lucrari-efectuate")}>Lucrări</a>
<a href="{url("")}#garantie">Garanție</a>
<a href="#contact">Contact</a>
</nav>
<a class="top-call" href="tel:{PHONE1_T}"><span>Programări</span><strong>{PHONE1}</strong></a>
<a class="btn btn-red btn-sm" href="{PROG}" target="_blank" rel="noopener">Programează-te</a>
<button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false" aria-label="Meniu"><span></span></button>
</div>
</header>"""


def footer():
    svc = "".join(f'<li><a href="{url(p["slug"])}">{esc(p["nav"])}</a></li>' for p in ALL_SERVICES if p["slug"] not in ("probleme-cutie-automata",) and not p.get("brand"))
    brands = "".join(f'<li><a href="{url(p["slug"])}">{esc(p["nav"])}</a></li>' for p in ALL_SERVICES if p.get("brand"))
    cities = "".join(f'<li><a href="{url(c["slug"])}">Cutii automate {esc(c["city"])}</a></li>' for c in CITIES)
    return f"""<footer class="foot">
<div class="wrap">
<div class="foot-grid">
<div class="foot-brand">{brand()}<p>Atelier specializat în reparații și revizii pentru cutii de viteze automate și motoare de performanță. Băicoi, Prahova.</p>
<div class="socials" style="margin-top:22px"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><svg><use href="#i-fb"/></svg></a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#i-ig"/></svg></a><a href="{TT}" target="_blank" rel="noopener" aria-label="TikTok"><svg><use href="#i-tt"/></svg></a></div></div>
<div><p class="ft">SERVICII</p><ul>{svc}</ul></div>
<div><p class="ft">INFORMAȚII</p><ul>
<li><a href="{url("preturi-cutii-automate")}">Prețuri cutii automate</a></li>
<li><a href="{url("lucrari-efectuate")}">Lucrări efectuate</a></li>
<li><a href="{url("coduri-eroare-cutie-automata")}">Coduri de eroare cutie automată</a></li>
<li><a href="{url("probleme-cutie-automata")}">Probleme cutie automată</a></li>
<li><a href="{url("articole")}">Articole și sfaturi</a></li>
<li><a href="{url("despre-noi")}">Despre AutoMatrix Motors</a></li>
{brands}
{cities}
<li><a href="{url("politica-confidentialitate")}">Politica de confidențialitate</a></li>
<li><a href="{url("politica-cookies")}">Politica de cookie-uri</a></li>
<li><button class="linkbtn" type="button" data-cookie-settings>Setări cookie-uri</button></li>
</ul></div>
<div><p class="ft">CONTACT</p><ul>
<li><a href="tel:{PHONE1_T}">{PHONE1}</a></li>
<li><a href="tel:{PHONE2_T}">{PHONE2}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="{MAPS}" target="_blank" rel="noopener">Str. Înfrățirii nr. 111, Băicoi, jud. Prahova</a></li>
<li>Atelier: L–V 06:00–14:30</li>
<li>Programări: L–V 07:00–18:00, S 09:00–15:00</li>
</ul></div>
</div>
<div class="foot-legal">
<span>© <span data-year>2026</span> E-VOL AUTO SERVICE CENTER S.R.L., CUI RO40377191, Reg. Com. J2019000071295. AutoMatrix Motors este marca sub care operează societatea.</span>
<span class="anpc"><a href="https://anpc.ro/ce-este-sal/" target="_blank" rel="noopener nofollow">ANPC – Soluționarea alternativă a litigiilor</a><a href="https://anpc.ro/" target="_blank" rel="noopener nofollow">ANPC</a></span>
</div>
</div>
</footer>"""


def chrome_end():
    wa_txt = "Bun%C4%83%20ziua!%20Am%20o%20%C3%AEntrebare%20despre%20cutia%20automat%C4%83."
    return f"""<div class="fab">
<div class="fab-group"><button class="fab-btn fab-wa" type="button" data-pop="pop-wa" aria-expanded="false" aria-label="Scrie-ne pe WhatsApp"><svg><use href="#i-wa"/></svg></button>
<div class="fab-pop" id="pop-wa" hidden><p>Scrie-ne pe WhatsApp</p><a href="https://wa.me/{PHONE1_W}?text={wa_txt}" target="_blank" rel="noopener">{PHONE1} <small>WhatsApp</small></a><a href="https://wa.me/{PHONE2_W}?text={wa_txt}" target="_blank" rel="noopener">{PHONE2} <small>WhatsApp</small></a></div></div>
<div class="fab-group"><button class="fab-btn fab-call" type="button" data-pop="pop-call" aria-expanded="false" aria-label="Sună-ne"><svg><use href="#i-phone"/></svg></button>
<div class="fab-pop" id="pop-call" hidden><p>Programări L–V 07–18, S 09–15</p><a href="tel:{PHONE1_T}">{PHONE1} <small>Sună</small></a><a href="tel:{PHONE2_T}">{PHONE2} <small>Sună</small></a></div></div>
<button class="fab-btn fab-chat" id="chat-open" type="button" aria-controls="chat" aria-expanded="false" aria-label="Deschide chatul"><svg><use href="#i-chat"/></svg><span class="badge" aria-hidden="true"></span></button>
</div>
<section class="chat" id="chat" role="dialog" aria-label="Chat AutoMatrix" hidden>
<div class="chat-head"><img src="{IMG["emb"]}" width="200" height="183" alt=""><div><b>AutoMatrix Motors</b><span><i></i>Asistent automat, răspunde pe loc</span></div><button class="chat-close" type="button" aria-label="Închide chatul">×</button></div>
<div class="chat-body" aria-live="polite"></div>
<form class="chat-form"><label class="sr" for="chat-in">Scrie mesajul</label><input id="chat-in" type="text" placeholder="Scrie o întrebare…" autocomplete="off"><button type="submit" aria-label="Trimite"><svg><use href="#i-send"/></svg></button></form>
</section>
<section class="cookie" id="cookie" role="dialog" aria-labelledby="ck-title" hidden>
<p class="ct" id="ck-title">Folosim cookie-uri</p>
<p>Cookie-urile strict necesare țin site-ul funcțional. Pe celelalte le activăm doar dacă ești de acord. Detalii în <a href="{url("politica-cookies")}">Politica de cookie-uri</a>.</p>
<div class="cookie-prefs" hidden>
<label class="pref"><b>Strict necesare</b><span>Rețin alegerea ta despre cookie-uri. Mereu active.</span><input type="checkbox" checked disabled></label>
<label class="pref"><b>Funcționale</b><span>Chat live extern și hărți.</span><input id="ck-fun" type="checkbox"></label>
<label class="pref"><b>Analiză</b><span>Statistici despre vizite și despre cum e folosit site-ul (Google Analytics, Microsoft Clarity, Metricool).</span><input id="ck-ana" type="checkbox"></label>
<label class="pref"><b>Marketing</b><span>Măsurarea reclamelor Facebook și Instagram.</span><input id="ck-mkt" type="checkbox"></label>
</div>
<div class="cookie-acts"><button type="button" id="ck-none">Refuz</button><button type="button" class="solid" id="ck-all">Accept toate</button><button type="button" class="solid full" id="ck-save" hidden>Salvează alegerea</button><button type="button" class="text full" id="ck-set">Setări</button></div>
</section>"""


def contact_section(heading="Cere o ofertă pentru cutia ta"):
    brands = ["Volkswagen", "Audi", "BMW", "Mercedes-Benz", "Skoda", "Seat", "Cupra", "Porsche", "Volvo", "Land Rover", "Jaguar", "Ford", "Opel", "Hyundai", "Kia", "Mini", "Toyota", "Lexus", "Renault", "Dacia", "Peugeot", "Citroën", "Nissan", "Mazda", "Alfa Romeo", "Altă marcă"]
    opts = "".join(f"<option>{b}</option>" for b in brands)
    chips = [("Smucituri la schimbare",), ("Patinează",), ("Intră în avarie",), ("Zgomot sau vibrații",), ("Întârzie cuplarea",), ("Vreau revizie",), ("Probleme motor",)]
    chips_html = "".join(f'<label><input type="checkbox" name="simptome[]" value="{c[0]}"><span>{c[0]}</span></label>' for c in chips)
    return f"""<section class="sec contact" id="contact" aria-labelledby="contact-h">
<div class="wrap contact-grid">
<div class="form-card">
<h2 id="contact-h">{heading}</h2>
<p>Durează un minut. Te sunăm sau îți scriem pe WhatsApp cu o estimare, în cel mult o zi lucrătoare.</p>
<form id="lead" novalidate>
<div class="progress" aria-hidden="true"><i></i><i></i><i></i></div>
<p class="step-label" aria-live="polite">Pasul 1 din 3: Mașina ta</p>
<fieldset class="fstep"><legend>Ce mașină ai?</legend><div class="fields">
<div class="field"><label for="f-marca">Marca</label><select id="f-marca" name="marca" required><option value="">Alege marca</option>{opts}</select><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="f-model">Modelul</label><input id="f-model" name="model" type="text" required placeholder="ex. Passat B8 2.0 TDI" autocomplete="off"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="f-an">Anul fabricației</label><input id="f-an" name="an" type="number" inputmode="numeric" required placeholder="ex. 2017" min="1990" max="2027"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="f-cutie">Tipul cutiei</label><select id="f-cutie" name="cutie"><option value="">Nu știu</option><option>DSG / S tronic</option><option>ZF (6HP, 8HP)</option><option>Aisin</option><option>Mercedes G-Tronic</option><option>CVT</option><option>Altul</option></select><span class="err"></span></div>
</div></fieldset>
<fieldset class="fstep" hidden><legend>Ce observi la cutie?</legend>
<div class="chips" role="group" aria-label="Simptome">{chips_html}</div>
<div class="fields" style="margin-top:18px"><div class="field full"><label for="f-detalii">Detalii (opțional)</label><textarea id="f-detalii" name="detalii" placeholder="ex. La rece smucește din 1 în 2, iar pe bord apare eroare de cutie."></textarea></div></div>
</fieldset>
<fieldset class="fstep" hidden><legend>Cum te contactăm?</legend><div class="fields">
<div class="field"><label for="f-nume">Numele</label><input id="f-nume" name="nume" type="text" required autocomplete="name" placeholder="Prenume și nume"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="f-tel">Telefon</label><input id="f-tel" name="telefon" type="tel" required autocomplete="tel" inputmode="tel" placeholder="07xx xxx xxx"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="f-loc">Localitatea</label><input id="f-loc" name="localitate" type="text" required autocomplete="address-level2" placeholder="ex. Ploiești"><span class="err" aria-live="polite"></span></div>
<div class="field"><span class="lbl" id="pref-l">Preferi să fii contactat pe</span><div class="chips" role="radiogroup" aria-labelledby="pref-l"><label><input type="radio" name="contact" value="Telefon" checked><span>Telefon</span></label><label><input type="radio" name="contact" value="WhatsApp"><span>WhatsApp</span></label></div></div>
</div>
<label class="consent"><input id="f-gdpr" type="checkbox" name="gdpr" value="da"><span>Sunt de acord ca datele mele să fie folosite pentru a primi oferta solicitată, conform <a href="{url("politica-confidentialitate")}">Politicii de confidențialitate</a>.</span></label>
<div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
</fieldset>
<p class="form-msg" role="alert"></p>
<div class="form-nav"><button class="btn btn-line" id="f-back" type="button" hidden>Înapoi</button><button class="btn btn-red push" id="f-next" type="button">Continuă</button><button class="btn btn-red push" id="f-send" type="submit" hidden>Trimite cererea</button></div>
</form>
<div class="form-done" hidden><svg><use href="#i-check"/></svg><h3>Am primit cererea ta</h3><p id="done-text">Te sunăm în cel mult o zi lucrătoare.</p><a class="btn btn-wa" id="done-wa" style="margin-top:24px" href="https://wa.me/{PHONE1_W}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Trimite și pe WhatsApp</a></div>
</div>
<aside class="info" aria-label="Date de contact">
<div class="info-b"><h3>TELEFON ȘI WHATSAPP</h3>
<div class="phone-row"><a class="num tnum" href="tel:{PHONE1_T}">{PHONE1}</a><span class="acts"><a class="icon-btn call" href="tel:{PHONE1_T}" aria-label="Sună la {PHONE1}"><svg><use href="#i-phone"/></svg></a><a class="icon-btn wa" href="https://wa.me/{PHONE1_W}" target="_blank" rel="noopener" aria-label="WhatsApp {PHONE1}"><svg><use href="#i-wa"/></svg></a></span></div>
<div class="phone-row"><a class="num tnum" href="tel:{PHONE2_T}">{PHONE2}</a><span class="acts"><a class="icon-btn call" href="tel:{PHONE2_T}" aria-label="Sună la {PHONE2}"><svg><use href="#i-phone"/></svg></a><a class="icon-btn wa" href="https://wa.me/{PHONE2_W}" target="_blank" rel="noopener" aria-label="WhatsApp {PHONE2}"><svg><use href="#i-wa"/></svg></a></span></div>
<p class="open-now" id="open-now"><i></i><span>Programări L–V 07–18, S 09–15</span></p></div>
<div class="info-b"><h3>PROGRAMARE ONLINE</h3><p>Alege singur ziua și ora care ți se potrivesc.</p><a class="btn btn-red btn-sm" style="margin-top:14px" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a></div>
<div class="info-b"><h3>PROGRAM</h3><dl class="hours"><dt>Atelier</dt><dd>Luni–Vineri, 06:00–14:30</dd><dt>Programări</dt><dd>Luni–Vineri, 07:00–18:00</dd><dt></dt><dd>Sâmbătă, 09:00–15:00</dd></dl></div>
<div class="info-b"><h3>ADRESA</h3><address class="addr">AutoMatrix Motors<br>Str. Înfrățirii nr. 111<br>Băicoi, jud. Prahova</address><p style="margin-top:12px"><a class="link" href="{MAPS}" target="_blank" rel="noopener">Indicații în Google Maps</a></p><p style="margin-top:8px;font-size:.88rem">Email: <a class="link" href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div class="info-b"><h3>URMĂREȘTE-NE</h3><div class="socials"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><svg><use href="#i-fb"/></svg></a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#i-ig"/></svg></a><a href="{TT}" target="_blank" rel="noopener" aria-label="TikTok"><svg><use href="#i-tt"/></svg></a></div></div>
</aside>
</div>
</section>"""


def faq_block(items, heading="Întrebări frecvente", intro=""):
    det = "".join(f'<details{" open" if i == 0 else ""}><summary>{esc(q)}<i aria-hidden="true"></i></summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(items))
    return f"""<section class="sec sec-tint" id="intrebari" aria-labelledby="faq-h"><div class="wrap faq">
<div class="faq-intro"><span class="eyebrow">Răspunsuri</span><h2 id="faq-h" style="margin-top:22px">{heading}</h2><p>{intro or "Nu găsești răspunsul? Scrie-ne pe WhatsApp sau întreabă asistentul din colțul paginii."}</p>
<button class="btn btn-line btn-sm" style="margin-top:26px" type="button" data-chat><svg><use href="#i-chat"/></svg>Întreabă acum</button></div>
<div class="faq-list">{det}</div></div></section>"""


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": canon(s)} for i, (n, s) in enumerate(trail)]}


BUSINESS = {
    "@type": "AutoRepair", "@id": SITE + "/#business", "name": "AutoMatrix Motors", "legalName": "E-VOL AUTO SERVICE CENTER S.R.L.",
    "alternateName": ["Auto Matrix Motors", "AutoMatrix Gearbox Specialist"],
    "description": "Atelier specializat în reparații și revizii pentru cutii de viteze automate (DSG, S tronic, ZF, Aisin, Mercedes G-Tronic, CVT) și motoare de performanță, cu garanție de 24 de luni fără limită de kilometri pentru reparații.",
    "url": SITE + "/", "logo": SITE + "/assets/img/logo-automatrix.png", "image": [SITE + "/assets/img/og-automatrix.jpg", SITE + "/assets/img/logo-automatrix.png"],
    "telephone": PHONE1_T, "email": EMAIL, "taxID": "RO40377191", "vatID": "RO40377191", "priceRange": "699 – 25.199 lei", "currenciesAccepted": "RON", "paymentAccepted": "Numerar, card, transfer bancar",
    "address": {"@type": "PostalAddress", "streetAddress": "Str. Înfrățirii nr. 111", "addressLocality": "Băicoi", "postalCode": "105200", "addressRegion": "Prahova", "addressCountry": "RO"},
    "hasMap": MAPS,
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "06:00", "closes": "14:30"}],
    "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": PHONE1_T, "availableLanguage": "ro",
                      "hoursAvailable": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "18:00"},
                                         {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "15:00"}]},
                     {"@type": "ContactPoint", "contactType": "customer service", "telephone": PHONE2_T, "availableLanguage": "ro"}],
    "areaServed": [{"@type": "City", "name": c} for c in ["Băicoi", "Ploiești", "Câmpina", "Sinaia", "Târgoviște", "București", "Buzău", "Brașov", "Pitești", "Brăila", "Galați", "Constanța", "Craiova"]] + [{"@type": "AdministrativeArea", "name": j} for j in ["Județul Prahova", "Județul Dâmbovița", "Județul Buzău", "Municipiul București", "Județul Ilfov", "Județul Galați", "Județul Constanța", "Județul Brăila", "Județul Argeș", "Județul Brașov", "Județul Dolj"]],
    "sameAs": [FB, IG, TT, MAPS],
    "potentialAction": {"@type": "ReserveAction", "target": PROG, "name": "Programare online"},
    "knowsAbout": ["Reparații cutii automate", "Revizie cutie automată", "DSG", "S tronic", "ZF 8HP", "ZF 6HP", "Mercedes 7G-Tronic", "Mercedes 9G-Tronic", "Aisin", "CVT", "Mecatronic DSG", "Convertizor de cuplu", "Motoare de performanță"],
}


def service_schema(name, slug, min_price, desc):
    s = {"@type": "Service", "@id": canon(slug) + "#service", "name": name, "serviceType": name, "description": desc, "url": canon(slug),
         "provider": {"@id": SITE + "/#business"}, "areaServed": [{"@type": "AdministrativeArea", "name": "Prahova"}, {"@type": "Country", "name": "România"}]}
    if min_price:
        s["offers"] = {"@type": "Offer", "priceCurrency": "RON", "priceSpecification": {"@type": "PriceSpecification", "minPrice": min_price, "priceCurrency": "RON", "valueAddedTaxIncluded": True}, "url": canon(slug)}
    return s


def head(title, desc, slug, schema, extra_head=""):
    ld = json.dumps({"@context": "https://schema.org", "@graph": schema}, ensure_ascii=False, separators=(",", ":"))
    if PREVIEW:
        fonts = f'<link rel="stylesheet" href="{FONTS}">'
    else:
        fonts = (f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                 f'<link rel="preload" as="style" href="{FONTS}"><link rel="stylesheet" href="{FONTS}" media="print" onload="this.media=\'all\'"><noscript><link rel="stylesheet" href="{FONTS}"></noscript>')
    icons = "" if PREVIEW else ('<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">'
                                '<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">')
    return f"""<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon(slug)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#FFFFFF">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="RO-PH"><meta name="geo.placename" content="Băicoi">
<meta property="og:type" content="website"><meta property="og:locale" content="ro_RO"><meta property="og:site_name" content="AutoMatrix Motors">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon(slug)}">
<meta property="og:image" content="{SITE}/assets/img/og-automatrix.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="AutoMatrix Motors, 24 de luni garanție la reparații de cutii automate">
<meta name="twitter:card" content="summary_large_image">
{icons}{fonts}
<style>{CSS}</style>
{extra_head}<script type="application/ld+json">{ld}</script>"""


def scripts(scene=False):
    if PREVIEW:
        s = f"<script>\n{SCENEJS}\n</script>\n" if scene else ""
        return s + f"<script>\n{MAINJS}\n</script>"
    import hashlib
    v = hashlib.md5(MAINJS.encode()).hexdigest()[:8]
    return f'<script src="/assets/js/main.js?v={v}" defer></script>'


def page(slug, title, desc, schema, body, active="", scene=False, extra_head=""):
    hd = head(title, desc, slug, schema, extra_head)
    inner = f"""<a class="skip" href="#main">Sari la conținut</a>
{SPRITE}
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{chrome_end()}
{scripts(False)}"""
    if PREVIEW and slug == "":
        return hd + "\n" + inner  # artifact page: skeleton added at publish
    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{hd}
</head>
<body>
{inner}
</body>
</html>"""


def counters(html_):
    """facts strip: number in a counter span, unit as <small>, label as span.lbl"""
    def strip(m):
        blk = m.group(0)
        def num(mm):
            pre, n, unit = mm.group(1) or "", mm.group(2), (mm.group(3) or "").strip()
            u = f"<small>{unit}</small>" if unit else ""
            return f'<strong>{pre}<span class="cnt" data-to="{n}">{n}</span>{u}</strong><span class="lbl">'
        return re.sub(r'<strong>(~)?(\d+)(\s[^<]*)?</strong><span>', num, blk)
    return re.sub(r'<section class="facts".*?</section>', strip, html_, flags=re.S)


def write(slug, content):
    content = counters(content)
    name = "index.html" if slug == "" else slug + ".html"
    (OUT / name).write_text(content)


def norm_s(t):
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(ch) != "Mn")


def prow(c):
    ops = "".join(f"<li>{esc(o)}</li>" for o in c["ops"])
    parts = "".join(f"<li>{esc(x)}</li>" for x in c["parts"])
    badge = '<span class="g">24 luni</span>' if c["kind"] == "reparatie" else ""
    extra = ""
    if c.get("symptoms"):
        extra += '<div><p class="pdh">Simptome</p><ul>' + "".join(f"<li>{esc(x)}</li>" for x in c["symptoms"]) + "</ul></div>"
    chips = [(x["k"], x["href"], x["t"]) for x in c.get("bcodes", [])]
    have = {_base(k) for x in c.get("bcodes", []) for k in x["all"]}
    for k in c.get("codes", []):
        if _base(k) not in have and len(chips) < 8:
            chips.append((k, f'{url("coduri-eroare-cutie-automata")}#{k.lower()}', CODE_MAP[k][1])); have.add(_base(k))
    if chips:
        extra += '<div><p class="pdh">Coduri de eroare frecvente</p><p class="pcodes">' + "".join(f'<a class="ecode" href="{h}" title="{esc(t)}">{esc(k)}</a>' for k, h, t in chips) + "</p></div>"
    sdata = norm_s(c["name"] + " " + " ".join(k + " " + k.replace("-", "") for k, _, _ in chips) + " " + " ".join(c.get("symptoms", [])) + (" dupa diagnoza" if c.get("price") is None else ""))
    if c.get("price") is None:
        price_html = '<span class="pp pdiag">Preț după diagnoză</span>'
        note = f'<div class="pnote"><p><b>Prețul se stabilește după diagnoză,</b> în funcție de codurile de eroare și de ce găsim la verificare. Primești prețul în scris înainte de orice lucrare. <a class="link" href="{url(c["box"])}">Vezi codurile de eroare pentru această cutie</a></p></div>'
    else:
        price_html = f'<span class="pp tnum">{fmt(c["price"])} lei</span>'
        note = ""
    return (f'<details class="prow" id="{c["rid"]}" data-k="{c["kind"]}" data-s="{esc(sdata)}"><summary><span class="pn">{esc(c["name"])}{badge}</span>'
            f'{price_html}<i aria-hidden="true"></i></summary>'
            f'<div class="pd">{note}{extra}<div><p class="pdh">Operațiuni</p><ul>{ops}</ul></div><div><p class="pdh">Piese și consumabile</p><ul>{parts}</ul></div></div></details>')


def price_rows_html(rws):
    return '<div class="plist2">' + "".join(prow(c) for c in rws) + '</div>'



def logo3d(n=14, depth=15.0):
    out = []
    for i in range(n):
        z = round((i - (n - 1) / 2) * depth / (n - 1), 2)
        edge = i in (0, n - 1)
        style = f"transform:translateZ({z}px)" + ("" if edge else ";filter:brightness(.26) saturate(.6)")
        out.append(f'<i class="ly" style="{style}"></i>')
    return f'<div class="logo3d-wrap" aria-hidden="true"><div class="logo3d" style="--logo:url({IMG["dark"]})">' + "".join(out) + '</div></div>'

# ------------------------------------------------------------------ HOME
def home():
    svc_rows = [
        ("reparatii-cutii-automate", "Reparații cutii automate", "Diagnoză, demontare, piese noi și test la drum, pentru orice tip de cutie automată.", min_price(kind="reparatie")),
        ("revizie-cutie-automata", "Revizie cutie automată", "Ulei Motul, filtru și garnituri, exact după manualul de reparație al producătorului cutiei.", min_price(kind="revizie")),
        ("reparatie-cutie-dsg", "Cutii DSG și S tronic", "Ambreiaje DQ200, DQ250, DQ381, DQ500 și S tronic 0B5.", min(c["price"] for c in CATALOG if c["fam"] == "dsg")),
        ("reparatie-mecatronic-dsg", "Mecatronic DSG", "Senzori de presiune, bloc de valve, electrovalve, adaptări.", min_price(r"mecatronic DSG", "reparatie")),
        ("reparatie-cutie-zf", "Cutii ZF 6HP și 8HP", "BMW, Audi, Land Rover, Jaguar, Porsche, Alfa Romeo.", min(c["price"] for c in CATALOG if c["fam"] == "zf")),
        ("reparatie-cutie-mercedes", "Mercedes 7G și 9G-Tronic", "Placă conductoare, bloc de valve, convertizor, revizie.", min(c["price"] for c in CATALOG if c["fam"] == "mercedes")),
        ("reconditionare-convertizor-cuplu", "Convertizor de cuplu", "Recondiționare completă, echilibrare și test de presiune.", min_price(r"convertizor")),
        ("reparatie-cutie-cvt", "Cutii CVT și Multitronic", "Audi Multitronic, Jatco, Toyota și alte cutii cu variație continuă.", min(c["price"] for c in CATALOG if c["fam"] == "cvt")),
        ("reparatii-motoare-performanta", "Motoare de performanță", "Reparații capitale, distribuție, turbo pentru BMW M, Audi RS, AMG.", None),
    ]
    idx = "".join(f'<li><a href="{url(s)}"><h3>{esc(n)}</h3><p>{esc(d)}</p><span class="from">{"de la<b class=\"tnum\">" + fmt(p) + " lei</b>" if p else "preț<b>după diagnoză</b>"}</span><svg class="arrow" aria-hidden="true"><use href="#i-arrow"/></svg></a></li>' for s, n, d, p in svc_rows)
    def P(rx): return pick(rx)[0]["price"]
    plist_items = [("Revizie cutie DSG (VW, Skoda, Audi, Seat)", P(r"^Revizie cutie DSG VW$")), ("Revizie cutie BMW 8HP", P(r"^Revizie cutie BMW 8HP$")), ("Revizie cutie Mercedes 7G-Tronic", P(r"^Revizie cutie 7G-Tronic$")),
                   ("Convertizor de cuplu BMW 6HP", P(r"convertizor de cuplu BMW 6")), ("Set ambreiaj DSG 7 DQ200", P(r"Set reparație ambreiaj DSG 7 DQ200 VW")), ("Reparație cutie DSG DQ381", P(r"Reparație cutie automată DSG DQ381 VW"))]
    plist = "".join(f'<div><span>{esc(n)}</span><b class="tnum"><small>de la</small>{fmt(p)} lei</b></div>' for n, p in plist_items)
    city_links = {c["city"]: c["slug"] for c in CITIES}
    cl = '<li class="home">Băicoi<span>atelierul nostru</span></li>' + "".join(f'<li><a href="{url(c["slug"])}">{esc(c["city"])}</a><span>~{c["km"]} km</span></li>' for c in sorted(CITIES, key=lambda c: int(c["km"])))
    brands = ["Volkswagen", "Audi", "BMW", "Mercedes-Benz", "Porsche", "Skoda", "Seat", "Cupra", "Volvo", "Land Rover", "Jaguar", "Mini", "Ford", "Hyundai", "Kia", "Toyota"]
    bt = "".join(f"<span>{b}</span>" for b in brands) + "".join(f'<span aria-hidden="true">{b}</span>' for b in brands)
    body = f"""<section class="hero" id="acasa" aria-labelledby="h1">
<div class="wrap">
<div class="hero-copy">
<span class="eyebrow">Garanție 24 de luni, fără limită de kilometri</span>
<h1 id="h1"><span class="reveal-line"><span>Reparații cutii</span></span><span class="reveal-line"><span>automate, executate</span></span><span class="reveal-line"><span>cu <em>precizie</em>.</span></span></h1>
<p class="hero-lead">Atelier specializat în cutii DSG, S tronic, ZF, Aisin, Mercedes G-Tronic și CVT, în Băicoi, Prahova. Știi prețul înainte și pleci cu garanția în scris.</p>
<div class="hero-cta"><a class="btn btn-red" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a><a class="btn btn-line" href="#contact">Cere o ofertă</a></div>
<div class="hero-meta"><span><b>Atelier</b> L–V 06:00–14:30</span><span><b>Programări</b> <a href="tel:{PHONE1_T}" style="text-decoration:none">{PHONE1}</a></span></div>
</div>
{logo3d()}
</div>
</section>

<section class="facts" aria-label="Pe scurt"><ul class="wrap">
<li><strong>24 luni</strong><span>garanție fără limită de kilometri, unică în România</span></li>
<li><strong>5</strong><span>elevatoare în atelier</span></li>
<li><strong>6</strong><span>mecanici specializați pe cutii</span></li>
<li><strong>~5 zile</strong><span>lucrătoare pentru o reparație completă</span></li>
<li><strong>200 km</strong><span>raza din care vin clienții</span></li>
</ul></section>

<section class="sec" id="servicii" aria-labelledby="svc-h"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Servicii</span><h2 id="svc-h">Tot ce ține de cutia automată, într-un singur atelier</h2></div>
<p>Diagnoza o facem noi, piesele le alegem noi, testul la drum îl facem noi. Așa putem garanta fiecare reparație 24 de luni.</p></div>
<ul class="index">{idx}</ul>
</div></section>

<section class="showroom" id="garantie" aria-labelledby="w-h"><div class="wrap">
<div class="big24-wrap"><p class="big24 tnum" aria-hidden="true">24</p><small>LUNI GARANȚIE</small></div>
<div>
<span class="eyebrow">Avantajul AutoMatrix</span>
<h2 id="w-h" style="margin-top:22px">24 de luni garanție. Unică în România.</h2>
<p class="lead">24 de luni și fără limită de kilometri. Nimeni altcineva din țară nu garantează atât de mult o reparație de cutie automată. Noi o facem pentru că știm ce montăm și cum lucrăm.</p>
<ul>
<li><svg><use href="#i-shield"/></svg><span><b>Fără limită de kilometri.</b> Contează doar cele 24 de luni, oricât ai conduce.</span></li>
<li><svg><use href="#i-shield"/></svg><span><b>Garanție scrisă</b>, pe certificat, pentru piese și manoperă.</span></li>
<li><svg><use href="#i-shield"/></svg><span><b>Deviz aprobat de tine.</b> Nu lucrăm nimic fără acordul tău.</span></li>
<li><svg><use href="#i-shield"/></svg><span><b>Test la drum</b> înainte să-ți predăm mașina.</span></li>
<li><svg><use href="#i-shield"/></svg><span><b>Factură și certificat</b> la predare.</span></li>
</ul>
<p class="fine">Garanția se aplică reparațiilor de cutii automate efectuate în atelierul AutoMatrix Motors, în condițiile din certificatul de garanție.</p>
</div>
</div></section>

<section class="sec sec-tint" id="proces" aria-labelledby="p-h"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Cum lucrăm</span><h2 id="p-h">Cinci pași, fără surprize</h2></div><p>Știi în fiecare moment unde e mașina ta și cât te costă.</p></div>
<ol class="steps">
<li><span class="n">1</span><h3>Programare</h3><p>Ne suni, ne scrii pe WhatsApp sau completezi formularul. Primești o primă estimare și o dată.</p></li>
<li><span class="n">2</span><h3>Diagnoză</h3><p>Citim erorile, testăm mașina la drum și aflăm exact cauza problemei.</p></li>
<li><span class="n">3</span><h3>Deviz aprobat</h3><p>Primești prețul final în scris. Începem doar după ce ești de acord.</p></li>
<li><span class="n">4</span><h3>Reparație</h3><p>În medie 5 zile lucrătoare, cu poze pe WhatsApp cu piesele și lucrarea.</p></li>
<li><span class="n">5</span><h3>Predare</h3><p>Test la drum, factură și certificatul de garanție de 24 de luni.</p></li>
</ol>
</div></section>

<section class="sec" id="preturi" aria-labelledby="pr-h"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Prețuri</span><h2 id="pr-h">Prețuri afișate, cu manoperă inclusă</h2></div><p>Câteva repere din lista completă. Prețul final îl confirmăm după diagnoză, în scris, înainte să începem.</p></div>
<div class="plist">{plist}</div>
<div class="after-list"><p>Prețuri cu TVA și manoperă incluse. Pot varia în funcție de motorizare, de starea cutiei și de piesele necesare.</p><a class="btn btn-line btn-sm" href="{url("preturi-cutii-automate")}">Toate prețurile</a></div>
</div></section>

<div class="brands" aria-label="Mărci cu care lucrăm"><div class="brands-track">{bt}</div></div>

<section class="sec" id="zona" aria-labelledby="z-h"><div class="wrap area">
<div class="area-copy"><span class="eyebrow">Zona deservită</span><h2 id="z-h" style="margin-top:22px">Clienți din tot sudul și centrul țării</h2>
<p>Atelierul este în Băicoi, între Ploiești și Câmpina, aproape de DN1. Clienții vin din Prahova, Dâmbovița, Buzău, București, Ilfov, Brașov, Argeș, dar și din Galați, Brăila, Constanța sau Craiova, pentru reparațiile mari. Alege orașul tău ca să vezi traseul.</p>
<a class="btn btn-line btn-sm" style="margin-top:28px" href="{MAPS}" target="_blank" rel="noopener"><svg><use href="#i-pin"/></svg>Deschide în Google Maps</a></div>
<ul class="cities">{cl}</ul>
</div></section>

{faq_block(HOME_FAQ)}
{contact_section()}"""
    schema = [BUSINESS, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "AutoMatrix Motors", "inLanguage": "ro-RO", "publisher": {"@id": SITE + "/#business"}},
              {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": "Service cutii de viteze automate | AutoMatrix Motors", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#business"}, "inLanguage": "ro-RO", "dateModified": UPDATED},
              faq_schema(HOME_FAQ)]
    preload = "" if PREVIEW else '<link rel="preload" as="image" href="/assets/img/emblema-dark.webp" fetchpriority="high">'
    write("", page("", "Service cutii de viteze automate | Garanție 24 luni | AutoMatrix", "Service specializat în cutii de viteze automate: reparații și revizii DSG, S tronic, Powershift, ZF, Aisin, Mercedes, CVT. 361 de prețuri afișate, garanție 24 luni fără limită de km. Băicoi, Prahova.", schema, body, scene=True, extra_head=preload))


# ------------------------------------------------------------------ SERVICE PAGES
def related_html(slugs):
    m = {p["slug"]: p for p in PAGES}
    m["preturi-cutii-automate"] = dict(PRICE_PAGE, desc="Lista completă cu revizii și reparații.")
    out = "".join(link_card(x) for x in slugs)
    return f'<section class="sec" aria-labelledby="rel-h" style="padding-top:0"><div class="wrap"><div class="sec-head" style="margin-bottom:32px"><h2 id="rel-h" style="font-size:var(--s-lg)">Citește și</h2></div><div class="related">{out}</div></div></section>'


def aside_html(slug):
    links = "".join(f'<li><a href="{url(p["slug"])}">{esc(p["nav"])}</a></li>' for p in PAGES if p["slug"] != slug)
    return f"""<aside class="aside" aria-label="Contact și alte servicii">
<div class="aside-card"><h3>PROGRAMĂRI</h3><a class="phone tnum" href="tel:{PHONE1_T}">{PHONE1}</a><a class="phone tnum" href="tel:{PHONE2_T}">{PHONE2}</a><p style="font-size:.86rem;margin-top:8px">L–V 07:00–18:00, S 09:00–15:00</p><a class="btn btn-red btn-sm" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a><a class="btn btn-line btn-sm" href="#contact">Cere o ofertă</a><a class="btn btn-wa btn-sm" href="https://wa.me/{PHONE1_W}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a></div>
<div class="aside-card"><h3>ALTE SERVICII</h3><ul>{links}<li><a href="{url("preturi-cutii-automate")}">Prețuri cutii automate</a></li></ul></div>
</aside>"""


def spec_html(spec):
    rowsh = "".join(f'<div><dt>{esc(k)}</dt><dd class="{c}">{esc(v)}</dd></div>' for k, v, c in spec)
    return f'<div class="spec"><div class="spec-h"><span>FIȘĂ TEHNICĂ</span><img src="{IMG["emb"]}" width="200" height="183" alt=""></div><dl>{rowsh}</dl></div>'


def page_codes(p):
    seen = []
    for c in p.get("prices") or []:
        for k in c.get("codes", []):
            if k not in seen:
                seen.append(k)
    if p["slug"] == "probleme-cutie-automata":
        seen = ["P0700", "P0730", "P0741", "P0868", "P0894", "P0218", "P17BF", "P189C", "P2767", "P0776", "P0841", "P17F0"]
    if not seen:
        return ""
    spec = [k for k in seen if not re.match(r"(P0[0-9A-F]{3}|U0[0-9]{3})$", k)]
    bx = [b for b in BOXES if any(re.search(b["match"], c["name"], re.I) for c in (p.get("prices") or []))]
    guides = (f'<p style="margin-top:14px">Coduri specifice pe cutii: ' + ", ".join(f'<a class="link" href="{url(b["slug"])}">{esc(b["short"])}</a>' for b in bx) + ".</p>") if bx else ""
    return codes_block((spec + [k for k in seen if k not in spec])[:12]) + guides + f'<p style="margin-top:14px"><a class="link" href="{url("coduri-eroare-cutie-automata")}">Toate codurile de eroare explicate</a></p>'


def service_page(p):
    trail = [("Acasă", ""), (p["nav"], p["slug"])]
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">{esc(p["nav"])}</li></ol></nav>'
    prices = ""
    if p["prices"]:
        prices = f'<div style="margin-top:26px">{price_rows_html(p["prices"])}</div><p style="font-size:.86rem;color:var(--ink-3);margin-top:14px">Prețuri cu TVA și manoperă incluse. Apasă pe o lucrare ca să vezi operațiunile și piesele. Prețul final se confirmă după diagnoză. <a class="link" href="{url("preturi-cutii-automate")}">Toate prețurile</a></p>'
    body = f"""<section class="phero"><div class="wrap">{crumbs}
<div class="grid"><div><span class="eyebrow">{esc(p["eyebrow"])}</span><h1>{esc(p["h1"])}</h1><p class="lead">{esc(p["lead"])}</p>
<div class="hero-cta"><a class="btn btn-red" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a><a class="btn btn-line" href="#contact">Cere o ofertă</a><a class="btn btn-line" href="tel:{PHONE1_T}"><svg><use href="#i-phone"/></svg>{PHONE1}</a></div></div>
{spec_html(p["spec"])}</div></div></section>
<section class="sec"><div class="wrap article"><div class="prose">{p["body"]}{prices}
{page_codes(p)}<div class="callout" style="margin-top:44px"><p><b>Garanție 24 de luni, fără limită de kilometri, unică în România.</b> Reparațiile de cutii automate făcute la AutoMatrix Motors au garanție scrisă pentru piese și manoperă.</p></div>
</div>{aside_html(p["slug"])}</div></section>
{faq_block(p["faq"])}
{related_html(p["related"])}
{contact_section()}"""
    schema = [service_schema(p["service_type"], p["slug"], (min(c["price"] for c in p["prices"]) if p["prices"] else p["min_price"]), p["desc"]), crumbs_schema(trail), faq_schema(p["faq"]),
              {"@type": "WebPage", "@id": canon(p["slug"]) + "#webpage", "url": canon(p["slug"]), "name": p["title"], "inLanguage": "ro-RO", "dateModified": UPDATED, "isPartOf": {"@id": SITE + "/#website"}}]
    write(p["slug"], page(p["slug"], p["title"], p["desc"], schema, body, active=p["slug"]))


# ------------------------------------------------------------------ PRICE PAGE
def price_page():
    slug = "preturi-cutii-automate"
    rmin, rmax = min_price(kind="reparatie"), max(c["price"] for c in CATALOG if c["kind"] == "reparatie")
    vmin, vmax = min_price(kind="revizie"), max(c["price"] for c in CATALOG if c["kind"] == "revizie")
    faq = [
        ("Cât costă reparația unei cutii automate?", f"Între {fmt(rmin)} lei, pentru un set de garnituri de mecatronic, și {fmt(rmax)} lei, pentru reparația completă a unei cutii Porsche PDK. Prețul exact îl primești în scris după diagnoză."),
        ("Cât costă revizia cutiei automate?", f"Între {fmt(vmin)} lei și {fmt(vmax)} lei, în funcție de cutie. Prețul include uleiul Motul, filtrul, garniturile și manopera."),
        ("Ce ulei folosiți?", "Folosim ulei Motul, cu specificația cerută de producătorul cutiei: ATF pentru cutiile clasice, ulei dedicat pentru cutiile cu dublu ambreiaj și ulei pentru CVT."),
        ("Ce înseamnă pachetele OEM și Eco?", "Toate reviziile urmează manualul de reparație al producătorului cutiei. Pachetele OEM folosesc filtru sau baie de ulei originale. Pachetele Eco sunt variante cu preț redus; ce piese diferă la cutia ta îți confirmăm la programare."),
        ("Prețurile includ TVA și manopera?", "Da. Toate prețurile din listă includ TVA și manopera."),
    ]
    groups = ""
    chips = ""
    for k in FAM_ORDER:
        items = [c for c in CATALOG + DIAG if c["fam"] == k]
        if not items:
            continue
        items.sort(key=lambda c: (c["kind"] != "revizie", c["name"]))
        chips += f'<a href="#f-{k}">{esc(FAM_LABEL[k].split(" (")[0])} <small>{len(items)}</small></a>'
        groups += f'<section class="pgroup" id="f-{k}" aria-labelledby="h-{k}"><h2 id="h-{k}">{esc(FAM_LABEL[k])}</h2>{price_rows_html(items)}</section>'
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">Prețuri</li></ol></nav>
<div class="grid"><div><span class="eyebrow">Prețuri</span><h1>Prețuri reparații și revizii cutii automate</h1><p class="lead">{len(CATALOG)} de pachete, cu manoperă și TVA incluse. Fiecare revizie urmează manualul de reparație emis de producătorul cutiei. Caută cutia ta și apasă pe o lucrare ca să vezi simptomele, codurile de eroare, operațiunile și piesele.</p><p class="lead" style="margin-top:12px;font-size:1rem">Reparăm și cutii care nu au încă un pachet cu preț fix, cum ar fi GM 6T40, Audi DL382, Mercedes 7G-DCT, ZF 9HP, Toyota U660E și K313, Nissan RE0F09 sau Jatco JF506E. La ele prețul se stabilește după diagnoză.</p>
<div class="hero-cta"><a class="btn btn-red" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a><a class="btn btn-line" href="#contact">Cere preț pentru mașina ta</a></div></div>
{spec_html([("Revizii", f"{fmt(vmin)} – {fmt(vmax)} lei", "big"), ("Reparații", f"{fmt(rmin)} – {fmt(rmax)} lei", ""), ("Garanție reparații", "24 luni, fără limită de km", "red"), ("Ulei", "Motul", "")])}</div></div></section>
<section class="sec" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap">
<div class="price-tools"><div class="tabs" role="tablist" aria-label="Tip lucrare"><button type="button" role="tab" data-kind="" aria-selected="true">Toate</button><button type="button" role="tab" data-kind="revizie" aria-selected="false">Revizii</button><button type="button" role="tab" data-kind="reparatie" aria-selected="false">Reparații</button></div>
<label class="search"><span class="sr">Caută cutia</span><svg aria-hidden="true"><use href="#i-search"/></svg><input id="price-q" type="search" placeholder="Caută: DQ200, 8HP, 7G-Tronic, Touareg…" autocomplete="off"></label></div>
<nav class="fam-chips" aria-label="Familii de cutii">{chips}</nav>
<div id="pall">{groups}</div>
<p class="price-empty" id="price-empty" hidden>Nu avem încă un pachet afișat pentru căutarea ta. <a class="link" href="#contact">Cere o ofertă</a> și îți răspundem în aceeași zi lucrătoare.</p>
<div class="after-list"><p>Prețuri cu TVA și manoperă. Pot varia în funcție de motorizare, de starea cutiei și de piesele necesare. Prețul final îl confirmăm în scris, după diagnoză.</p><a class="btn btn-red btn-sm" href="#contact">Cere o ofertă</a></div>
</div></section>
{faq_block(faq)}
{contact_section("Cere prețul exact pentru cutia ta")}"""
    offers = [{"@type": "Offer", "name": c["name"], "price": c["price"], "priceCurrency": "RON", "itemOffered": {"@type": "Service", "name": c["name"]}} for c in CATALOG]
    schema = [{"@type": "OfferCatalog", "@id": canon(slug) + "#catalog", "name": "Prețuri cutii automate AutoMatrix Motors", "url": canon(slug), "itemListElement": offers},
              crumbs_schema([("Acasă", ""), ("Prețuri", slug)]), faq_schema(faq)]
    write(slug, page(slug, "Prețuri cutii automate: revizii și reparații | AutoMatrix", f"Prețuri pentru {len(CATALOG)} de pachete de revizie și reparație cutie automată DSG, ZF, Aisin, Mercedes, CVT: revizii de la {fmt(vmin)} lei, reparații de la {fmt(rmin)} lei.", schema, body, active=slug))


# ------------------------------------------------------------------ CITY PAGES
def city_page(c):
    slug = c["slug"]
    svc = "".join(f'<li><a class="link" href="{url(p["slug"])}">{esc(p["nav"])}</a>: {esc(p["navsub"])}</li>' for p in PAGES if p["slug"] not in ("probleme-cutie-automata",))
    trail = [("Acasă", ""), ("Cutii automate " + c["city"], slug)]
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">Cutii automate {esc(c["city"])}</li></ol></nav>
<div class="grid"><div><span class="eyebrow">Clienți din {esc(c["city"])}, jud. {esc(c["county"])}</span><h1>Reparații cutii automate {esc(c["city"])}</h1><p class="lead">{esc(c["lead"])}</p>
<div class="hero-cta"><a class="btn btn-red" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a><a class="btn btn-line" href="{MAPS}" target="_blank" rel="noopener"><svg><use href="#i-pin"/></svg>Traseu în Google Maps</a></div></div>
{spec_html([("Distanță", "~" + c["km"] + " km", "big"), ("Drum", c["time"], ""), ("Atelier", "Băicoi, Str. Înfrățirii 111", ""), ("Garanție reparații", "24 luni, fără limită de km", "red")])}</div></div></section>
<section class="sec"><div class="wrap article"><div class="prose">
<h2>Cum ajungi la noi din {esc(c["city"])}</h2><p>{esc(c["route"])}</p>
{c["local"]}
<h2>Ce lucrări facem</h2><ul class="dots">{svc}</ul>
<h2>Prețuri, înainte să pleci de acasă</h2><p>Toate prețurile sunt pe site, cu manoperă inclusă: revizii de la {fmt(min_price(kind="revizie"))} lei, reparații de la {fmt(min_price(kind="reparatie"))} lei. Vezi <a class="link" href="{url("preturi-cutii-automate")}">lista completă de prețuri</a> sau cere o ofertă pentru mașina ta.</p>
<div class="callout"><p><b>Garanție 24 de luni, fără limită de kilometri, unică în România.</b> Contează mai mult decât câțiva kilometri în plus până la atelier.</p></div>
</div>{aside_html(slug)}</div></section>
{faq_block(c["faq"])}
{contact_section("Programează mașina pentru o diagnoză")}"""
    schema = [service_schema("Reparații cutii automate pentru clienți din " + c["city"], slug, 2399, c["desc"]), crumbs_schema(trail), faq_schema(c["faq"])]
    schema[0]["areaServed"] = ([{"@type": "City", "name": c["city"]}] if c["city"] != c["county"] or c["city"] in ("București", "Buzău", "Galați", "Constanța", "Brăila", "Brașov") else []) + [{"@type": "AdministrativeArea", "name": ("Municipiul București" if c["county"] == "București" else "Județul " + c["county"])}]
    write(slug, page(slug, c["title"], c["desc"], schema, body))


# ------------------------------------------------------------------ LEGAL + 404
def legal(slug, src_name, title, desc):
    srch = (ROOT / "site" / src_name).read_text()
    art = re.search(r"<article>(.*?)</article>", srch, re.S).group(1)
    art = art.replace('href="/politica-cookies.html"', f'href="{url("politica-cookies")}"').replace('href="/politica-confidentialitate.html"', f'href="{url("politica-confidentialitate")}"')
    art = art.replace('style="color:var(--red);text-decoration:underline"', 'style="color:var(--red);text-decoration:underline;padding:0"')
    art = art.replace('<td>Păstrează conversația din chatul live</td><td>sesiune – 6 luni</td><td>terță parte</td></tr>', '<td>Păstrează conversația din chatul live</td><td>sesiune – 6 luni</td><td>terță parte</td></tr><tr><td>datr, sb, fr și altele</td><td>Meta Platforms Ireland (modulul Facebook de pe pagina Lucrări efectuate)</td><td>Afișarea postărilor și a video-urilor de pe pagina noastră de Facebook, doar dacă apeși „Afișează postările” sau „Redă”, ori ai acceptat cookie-urile funcționale</td><td>până la 2 ani</td><td>terță parte</td></tr>')
    body = f'<section class="legal"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb" style="padding-top:0"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">{esc(title)}</li></ol></nav><article>{art}</article></div></section>'
    schema = [crumbs_schema([("Acasă", ""), (title, slug)])]
    write(slug, page(slug, title + " | AutoMatrix Motors", desc, schema, body))


def notfound():
    body = f'<section class="legal" style="text-align:center"><div class="wrap narrow"><img src="{IMG["emb"]}" width="120" height="110" alt="" style="margin:0 auto 26px"><h1>Pagina nu există</h1><p style="margin-top:16px">Linkul e greșit sau pagina a fost mutată.</p><p style="margin-top:30px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn btn-red" href="{url("")}">Mergi la prima pagină</a><a class="btn btn-line" href="{url("preturi-cutii-automate")}">Vezi prețurile</a></p></div></section>'
    c = page("404", "Pagina nu există | AutoMatrix Motors", "Pagina căutată nu există.", [], body)
    c = c.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', '<meta name="robots" content="noindex">')
    c = re.sub(r'<link rel="canonical"[^>]*>\n', '', c)
    (OUT / "404.html").write_text(c)



# ------------------------------------------------------------------ PROGRAMĂRI (landing page on programari.automatrixmotors.ro)
def programari():
    PURL = "https://programari.automatrixmotors.ro/"
    faq = [
        ("Ce înseamnă recondiționare la standard de producător?", "Desfacem complet cutia sau motorul, măsurăm fiecare componentă și înlocuim tot ce e uzat cu piese din seturi complete. Reasamblăm la cotele producătorului, facem adaptările pe calculator și testăm mașina la drum."),
        ("Ce acoperă garanția?", "Reparațiile de cutii automate au garanție scrisă de 24 de luni, fără limită de kilometri, pentru piese și manoperă, în condițiile din certificatul de garanție."),
        ("Cât durează?", "O recondiționare completă durează în medie 5 zile lucrătoare. Termenul exact îl primești după diagnoză, odată cu prețul."),
        ("Cât costă?", "Depinde de cutie sau de motor și de ce s-a uzat. Prețurile standard pentru peste 360 de lucrări sunt pe automatrixmotors.ro, iar prețul exact pentru mașina ta îl primești în scris după diagnoză."),
        ("De ce îmi cereți seria de șasiu (VIN)?", "Din seria de șasiu identificăm exact tipul cutiei și al motorului, ca să știm de la început ce piese sunt necesare. Nu e obligatorie, dar grăbește diagnoza."),
    ]
    steps = [("Completezi chestionarul", "Ne spui ce mașină ai și ce simptome are. Îți ia sub un minut."),
             ("Diagnoză cu Daniel", "Daniel analizează datele, îți pune câteva întrebări și stabilim exact cauza."),
             ("Ofertă clară", "Primești un preț ferm și termenul de execuție, fără costuri care apar pe parcurs."),
             ("Recondiționare și garanție", "Refacem cutia sau motorul la standard de producător și pleci cu garanția scrisă de 24 de luni, fără limită de kilometri.")]
    st = "".join(f'<li><span class="n">{i+1}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(steps))
    body = f"""<section class="hero" id="acasa" aria-labelledby="h1">
<div class="wrap">
<div class="hero-copy">
<span class="eyebrow">Recondiționări cutii automate și motoare</span>
<h1 id="h1"><span class="reveal-line"><span>Cutia sau motorul tău,</span></span><span class="reveal-line"><span>refăcute la standard</span></span><span class="reveal-line"><span>de <em>producător</em>.</span></span></h1>
<p class="hero-lead">Recondiționare integrală, cu 24 de luni garanție, fără limită de kilometri. Completează chestionarul în 60 de secunde și vezi dacă mașina ta se încadrează.</p>
<div class="hero-cta"><a class="btn btn-red" href="#formular">Vezi dacă te încadrezi</a><a class="btn btn-line" href="tel:{PHONE1_T}"><svg><use href="#i-phone"/></svg>{PHONE1}</a></div>
<div class="hero-meta"><span><b>Atelier</b> Băicoi, Prahova</span><span><b>Program</b> L–V 06:00–14:30</span></div>
</div>
{logo3d()}
</div>
</section>

<section class="facts" aria-label="Pe scurt"><ul class="wrap">
<li><strong>24 luni</strong><span>garanție fără limită de kilometri</span></li>
<li><strong>5</strong><span>elevatoare în atelier</span></li>
<li><strong>6</strong><span>mecanici specializați</span></li>
<li><strong>~5 zile</strong><span>pentru o recondiționare completă</span></li>
<li><strong>60 sec</strong><span>durează chestionarul</span></li>
</ul></section>

<section class="sec sec-tint" id="proces" aria-labelledby="p-h"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Cum lucrăm</span><h2 id="p-h">Patru pași până la o mașină reparată corect</h2></div><p>Știi de la început ce are mașina, cât costă și cât durează. Fără surprize pe parcurs.</p></div>
<ol class="steps" style="grid-template-columns:repeat(4,minmax(0,1fr))">{st}</ol>
</div></section>

<section class="sec" id="daniel" aria-labelledby="d-h"><div class="wrap area" style="align-items:center">
<div class="dan-photo"><img src="{IMG["dark"]}" width="520" height="506" alt="" loading="lazy"></div>
<div class="area-copy"><span class="eyebrow">Specialist cutii automate și motoare</span>
<h2 id="d-h" style="margin-top:22px">Diagnoza fiecărei mașini trece pe la mine</h2>
<p>Sunt Daniel Nenu. Mă uit personal peste fiecare chestionar și peste fiecare diagnoză. Îți explic clar ce a cedat, de ce s-a întâmplat și cum se repară, înainte să începem orice lucrare.</p>
<ul class="dan-list">
<li><svg><use href="#i-shield"/></svg><span>Atelier cu 5 elevatoare și 6 mecanici specializați</span></li>
<li><svg><use href="#i-shield"/></svg><span>Cutii DSG, S tronic, ZF, Aisin, Mercedes, CVT și motoare de performanță</span></li>
<li><svg><use href="#i-shield"/></svg><span>Preț ferm în scris, înainte de lucru</span></li>
</ul>
<a class="btn btn-red" style="margin-top:28px" href="#formular">Completează chestionarul</a></div>
</div></section>

<section class="showroom" id="garantie" aria-labelledby="w-h"><div class="wrap">
<div class="big24-wrap"><p class="big24 tnum" aria-hidden="true">24</p><small>LUNI GARANȚIE</small></div>
<div>
<span class="eyebrow">Garanția AutoMatrix</span>
<h2 id="w-h" style="margin-top:22px">24 de luni garanție. Fără limită de kilometri.</h2>
<p class="lead">Nimeni altcineva din țară nu garantează atât de mult o reparație de cutie automată. Noi o facem pentru că știm ce montăm și cum lucrăm.</p>
<ul>
<li><svg><use href="#i-shield"/></svg><span><b>Garanție scrisă</b>, pe certificat, pentru piese și manoperă.</span></li>
<li><svg><use href="#i-shield"/></svg><span><b>Fără limită de kilometri.</b> Contează doar cele 24 de luni.</span></li>
<li><svg><use href="#i-shield"/></svg><span><b>Test la drum</b> înainte să-ți predăm mașina.</span></li>
</ul>
<p class="fine">Garanția se aplică reparațiilor de cutii automate efectuate în atelierul AutoMatrix Motors, în condițiile din certificatul de garanție.</p>
</div>
</div></section>

<section class="sec contact" id="formular" aria-labelledby="f-h">
<div class="wrap contact-grid">
<div class="form-card">
<span class="eyebrow">Chestionar de calificare, 60 de secunde</span>
<h2 id="f-h" style="margin-top:18px">Vezi dacă mașina ta se încadrează</h2>
<p>Completează datele mașinii tale. Daniel se uită personal peste ele și te contactează pentru diagnoză.</p>
<form id="qform" novalidate style="margin-top:26px">
<div class="fields">
<div class="field"><label for="q-nume">Numele tău</label><input id="q-nume" name="nume" type="text" autocomplete="name" placeholder="ex. Adrian"><span class="err"></span></div>
<div class="field"><label for="q-tel">Telefon *</label><input id="q-tel" name="telefon" type="tel" required autocomplete="tel" inputmode="tel" placeholder="ex. 0722 123 456"><span class="err" aria-live="polite"></span></div>
<div class="field full"><label for="q-email">Email *</label><input id="q-email" name="email" type="email" required autocomplete="email" placeholder="ex. nume@mail.ro"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="q-masina">Ce mașină ai?</label><input id="q-masina" name="masina" type="text" placeholder="ex. BMW Seria 5, 2016"><span class="err"></span></div>
<div class="field"><label for="q-vin">Seria de șasiu (VIN)</label><input id="q-vin" name="vin" type="text" maxlength="17" autocomplete="off" placeholder="Ne ajută să identificăm exact cutia"><span class="err" aria-live="polite"></span></div>
<div class="field full"><label for="q-simp">Ce simptome are mașina și ce s-a mai încercat până acum?</label><textarea id="q-simp" name="simptome" placeholder="ex. smucituri la schimbarea treptelor, intră în avarie, alunecă"></textarea></div>
</div>
<label class="consent"><input id="q-gdpr" type="checkbox" name="gdpr" value="da"><span>Sunt de acord ca datele mele să fie folosite pentru a fi contactat în legătură cu mașina mea, conform <a href="/politica-confidentialitate">Politicii de confidențialitate</a>.</span></label>
<div class="hp" aria-hidden="true"><label for="q-web">Website</label><input id="q-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<p class="form-msg" role="alert"></p>
<div class="form-nav"><button class="btn btn-red" id="q-send" type="submit">Completează chestionarul</button></div>
</form>
<div class="form-done" id="q-done" hidden><svg><use href="#i-check"/></svg><h3>Am primit chestionarul</h3><p>Daniel se uită peste datele tale și te sună în cel mult o zi lucrătoare. Ca să grăbești lucrurile, trimite-ne pe WhatsApp un video scurt cu simptomul.</p><a class="btn btn-wa" id="q-wa" style="margin-top:24px" href="https://wa.me/{PHONE1_W}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Trimite pe WhatsApp</a></div>
</div>
<aside class="info" aria-label="Date de contact">
<div class="info-b"><h3>TELEFON ȘI WHATSAPP</h3>
<div class="phone-row"><a class="num tnum" href="tel:{PHONE1_T}">{PHONE1}</a><span class="acts"><a class="icon-btn call" href="tel:{PHONE1_T}" aria-label="Sună la {PHONE1}"><svg><use href="#i-phone"/></svg></a><a class="icon-btn wa" href="https://wa.me/{PHONE1_W}" target="_blank" rel="noopener" aria-label="WhatsApp {PHONE1}"><svg><use href="#i-wa"/></svg></a></span></div>
<div class="phone-row"><a class="num tnum" href="tel:{PHONE2_T}">{PHONE2}</a><span class="acts"><a class="icon-btn call" href="tel:{PHONE2_T}" aria-label="Sună la {PHONE2}"><svg><use href="#i-phone"/></svg></a><a class="icon-btn wa" href="https://wa.me/{PHONE2_W}" target="_blank" rel="noopener" aria-label="WhatsApp {PHONE2}"><svg><use href="#i-wa"/></svg></a></span></div>
<p class="open-now" id="open-now"><i></i><span>Programări L–V 07–18, S 09–15</span></p></div>
<div class="info-b"><h3>PROGRAM</h3><dl class="hours"><dt>Atelier</dt><dd>Luni–Vineri, 06:00–14:30</dd><dt>Programări</dt><dd>Luni–Vineri, 07:00–18:00</dd><dt></dt><dd>Sâmbătă, 09:00–15:00</dd></dl></div>
<div class="info-b"><h3>ADRESA</h3><address class="addr">AutoMatrix Motors<br>Str. Înfrățirii nr. 111<br>Băicoi, jud. Prahova</address><p style="margin-top:12px"><a class="link" href="{MAPS}" target="_blank" rel="noopener">Indicații în Google Maps</a></p></div>
</aside>
</div>
</section>
{faq_block(faq)}"""
    QJS = r"""<script>
(function(){var f=document.getElementById('qform');if(!f)return;var done=document.getElementById('q-done'),btn=document.getElementById('q-send'),msg=f.querySelector('.form-msg');
var LIVE=/(^|\.)automatrixmotors\.ro$/.test(location.hostname);
function err(el,t){var w=el.closest('.field');w.classList.toggle('invalid',!!t);w.querySelector('.err').textContent=t||'';}
function check(){var ok=true,t=f.telefon,e=f.email,v=f.vin;
 var tv=t.value.replace(/[\s.\-()]/g,'');if(!/^(\+?40|0)7\d{8}$/.test(tv)){err(t,'Scrie un număr de mobil valid, ex. 0722 123 456.');ok=false}else err(t,'');
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e.value.trim())){err(e,'Scrie o adresă de email validă.');ok=false}else err(e,'');
 if(v.value.trim()&&!/^[A-HJ-NPR-Z0-9]{17}$/i.test(v.value.trim())){err(v,'Seria de șasiu are 17 caractere (litere și cifre).');ok=false}else err(v,'');
 if(!f.gdpr.checked){msg.textContent='Bifează acordul pentru prelucrarea datelor ca să te putem contacta.';ok=false}else msg.textContent='';
 if(!ok){var b=f.querySelector('.invalid input');if(b)b.focus();}return ok;}
f.addEventListener('submit',function(ev){ev.preventDefault();if(!check())return;btn.disabled=true;btn.textContent='Se trimite…';
 var fd=new FormData(f);
 function ok(){f.hidden=true;done.hidden=false;var txt='Bună ziua! Am completat chestionarul de pe site.\nMașina: '+(f.masina.value||'-')+(f.vin.value?', VIN '+f.vin.value:'')+'\nSimptome: '+(f.simptome.value||'-')+'\nNume: '+(f.nume.value||'-');
  document.getElementById('q-wa').href='https://wa.me/40734607050?text='+encodeURIComponent(txt);done.scrollIntoView({behavior:'smooth',block:'center'});
  if(window.fbq)fbq('track','Lead');if(window.gtag)gtag('event','generate_lead');}
 if(!LIVE){setTimeout(ok,600);return;}
 fetch('send.php',{method:'POST',body:fd,headers:{Accept:'application/json'}}).then(function(r){return r.json()}).then(function(j){if(j&&j.ok)ok();else throw new Error(j&&j.error||'eroare')})
 .catch(function(e){btn.disabled=false;btn.textContent='Completează chestionarul';msg.textContent='Chestionarul nu a plecat ('+e.message+'). Încearcă din nou sau sună-ne la 0734 607 050.';});
});})();
</script>"""
    title = "Automatrix Motors: recondiționări cutii automate și motoare"
    desc = "Recondiționare integrală cutii automate și motoare la standard de producător. 24 luni garanție, fără limită de kilometri. Vezi dacă mașina ta se încadrează."
    schema = [{"@type": "WebPage", "@id": PURL + "#webpage", "url": PURL, "name": title, "inLanguage": "ro-RO", "about": {"@id": SITE + "/#business"}}, faq_schema(faq)]
    extra_css = "<style>.dan-photo{position:relative;background:radial-gradient(60% 60% at 50% 40%,#2a1015,#0f0e11);aspect-ratio:4/4.4;display:grid;place-items:center;overflow:hidden}.dan-photo img{width:62%;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))}.dan-photo img.photo{width:100%;height:100%;object-fit:cover;filter:none}.dan-list{list-style:none;padding:0;margin:26px 0 0;display:grid;gap:12px;border-top:1px solid var(--line);padding-top:20px}.dan-list li{display:grid;grid-template-columns:24px minmax(0,1fr);gap:12px;color:var(--ink)}.dan-list svg{width:20px;height:20px;color:var(--gold);margin-top:3px}@media (max-width:900px){.steps[style]{grid-template-columns:1fr!important}}</style>"
    html_ = page("", title, desc, schema, body, extra_head=extra_css)
    html_ = html_.replace(f'href="{PROG}" target="_blank" rel="noopener"', 'href="#formular"').replace('href="#contact"', 'href="#formular"')
    html_ = html_.replace("</body>", QJS + "\n</body>") if "</body>" in html_ else html_ + QJS
    if PREVIEW:
        html_ = counters(html_)
        (OUT / "programari.html").write_text(html_ if html_.startswith("<!doctype") else "<!doctype html>\n<html lang=\"ro\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">" + html_.split("<a class=\"skip\"")[0] + "</head><body><a class=\"skip\"" + html_.split("<a class=\"skip\"", 1)[1] + "</body></html>")
        return
    html_ = html_.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{PURL}">').replace(f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{PURL}">')
    html_ = re.sub(r'(href|src)="/(?!/)', r'\1="' + SITE + '/', html_)
    html_ = html_.replace("url(/assets/", "url(" + SITE + "/assets/")
    html_ = html_.replace(f'href="{SITE}/politica-confidentialitate"', f'href="{SITE}/politica-confidentialitate"')
    P = ROOT / "dist_prog"; P.mkdir(exist_ok=True)
    (P / "index.html").write_text(counters(html_))


# ------------------------------------------------------------------ LUCRĂRI EFECTUATE (Facebook feed)
FB_PAGE = "https://www.facebook.com/cutiiautomateploiesti"
PLAY = '<span class="work-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M8 5v14l11-7z"/></svg></span><span class="work-vlabel">Video</span>'


def lucrari():
    slug = "lucrari-efectuate"
    filters = [("", "Toate"), ("video", "Video"), ("dsg", "DSG / S tronic"), ("zf", "ZF"), ("mercedes", "Mercedes"), ("aisin", "Aisin"), ("cvt", "CVT"), ("motor", "Motoare")]
    fl = "".join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if not k else "false"}">{esc(v)}</button>' for k, v in filters)
    if PREVIEW:
        ex = [("2026-10-24", "Cutie DSG DQ200 de pe un VW Golf 7: ambreiaj dublu înlocuit, mecatronic reparat, adaptări și test la drum. Clientul a venit din Ploiești cu smucituri la plecare. Garanție 24 de luni, fără limită de kilometri.", "dsg"),
              ("2026-10-20", "BMW X5 cu cutie ZF 8HP: convertizor de cuplu recondiționat și revizie completă cu baie nouă și ulei Motul. Tremurăturile de la 80 km/h au dispărut.", "zf video"),
              ("2026-10-15", "Mercedes E-Class, 7G-Tronic: placă conductoare înlocuită, ulei și filtru noi. Cutia nu mai intră în avarie.", "mercedes")]
        cards = "".join(f'<article class="work" data-tags="{t}"><div class="work-img{" is-video" if "video" in t else ""}"><img src="{IMG["dark"]}" alt="" loading="lazy"><span class="work-ex">Exemplu</span>{PLAY if "video" in t else ""}</div><div class="work-b"><time datetime="{d}">{d[8:]}.{d[5:7]}.{d[:4]}</time><p>{esc(m)}</p><a class="link" href="{FB_PAGE}" target="_blank" rel="noopener">Vezi postarea pe Facebook</a></div></article>' for d, m, t in ex)
        feed = f'<div class="works">{cards}</div><p class="work-note">În previzualizare apar exemple. Pe site, aici se afișează automat ultimele postări de pe pagina de Facebook.</p>'
    else:
        feed = f'''<div class="fb-fallback" id="fb-fallback">
<p>Postările noastre cu lucrările din atelier se încarcă direct de pe pagina de Facebook.</p>
<div class="hero-cta" style="margin-top:20px"><button class="btn btn-red" type="button" id="fb-load">Afișează postările de pe Facebook</button><a class="btn btn-line" href="{FB_PAGE}" target="_blank" rel="noopener"><svg><use href="#i-fb"/></svg>Deschide pagina de Facebook</a></div>
<p class="work-note">Afișarea postărilor încarcă un modul de la Facebook, care poate seta cookie-uri. Detalii în <a class="link" href="{url("politica-cookies")}">Politica de cookie-uri</a>.</p>
<div id="fb-frame"></div>
</div>'''
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">Lucrări efectuate</li></ol></nav>
<div class="grid"><div><span class="eyebrow">Din atelier</span><h1>Lucrări efectuate</h1><p class="lead">Cutii automate și motoare reparate în atelierul nostru din Băicoi. Postăm aproape fiecare lucrare, cu poze și video: ce a avut mașina, ce am înlocuit și cum a plecat clientul.</p>
<div class="hero-cta"><a class="btn btn-red" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a><a class="btn btn-line" href="{FB_PAGE}" target="_blank" rel="noopener"><svg><use href="#i-fb"/></svg>Urmărește-ne pe Facebook</a></div></div>
{spec_html([("Garanție reparații", "24 luni, fără limită de km", "red"), ("Atelier", "5 elevatoare, 6 mecanici", ""), ("Cutii", "DSG, ZF, Aisin, Mercedes, CVT", ""), ("Motoare", "de performanță", "")])}</div></div></section>
<section class="sec" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap">
<div class="work-filters" role="group" aria-label="Filtrează lucrările">{fl}</div>
<div id="feed"><!--FEED-START-->{feed}<!--FEED-END--></div>
<div class="after-list" style="margin-top:48px"><p>Ai o problemă asemănătoare? Trimite-ne pe WhatsApp un video scurt cu simptomul și îți spunem ce credem.</p><a class="btn btn-wa btn-sm" href="https://wa.me/{PHONE1_W}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Scrie-ne pe WhatsApp</a></div>
</div></section>
{contact_section()}
<script>
(function(){{var bs=[].slice.call(document.querySelectorAll('.work-filters button'));
function ap(k){{[].forEach.call(document.querySelectorAll('.work'),function(w){{w.hidden=!!k&&(' '+(w.dataset.tags||'')+' ').indexOf(' '+k+' ')<0}});bs.forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.f===k?'true':'false')}});}}
bs.forEach(function(b){{b.addEventListener('click',function(){{ap(b.dataset.f)}})}});
document.addEventListener('click',function(e){{var pl=e.target.closest('.work-play');if(!pl)return;var box=pl.closest('.is-video');if(!box||!box.dataset.video)return;
box.innerHTML='<iframe title="Video AutoMatrix Motors" src="https://www.facebook.com/plugins/video.php?href='+encodeURIComponent(box.dataset.video)+'&show_text=false&autoplay=true&width=560" style="border:0;width:100%;height:100%" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share" allowfullscreen></iframe>';}});
var fr=document.getElementById('fb-frame'),btn=document.getElementById('fb-load');if(!fr)return;
document.querySelector('.work-filters').hidden=true;
function load(){{if(fr.firstChild)return;var w=Math.min(500,fr.clientWidth||500);fr.innerHTML='<iframe title="Postări Facebook AutoMatrix Motors" src="https://www.facebook.com/plugins/page.php?href='+encodeURIComponent('{FB_PAGE}')+'&tabs=timeline&width='+w+'&height=900&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false" width="'+w+'" height="900" style="border:0;overflow:hidden;max-width:100%" scrolling="no" allowfullscreen loading="lazy"></iframe>';btn.hidden=true;}}
btn.addEventListener('click',load);
try{{var c=JSON.parse(localStorage.getItem('am_consent'));if(c&&c.functional)load();}}catch(e){{}}
}})();
</script>"""
    schema = [crumbs_schema([("Acasă", ""), ("Lucrări efectuate", slug)]),
              {"@type": "CollectionPage", "@id": canon(slug) + "#webpage", "url": canon(slug), "name": "Lucrări efectuate | AutoMatrix Motors", "inLanguage": "ro-RO", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#business"}}]
    write(slug, page(slug, "Lucrări efectuate: cutii automate reparate | AutoMatrix", "Lucrări efectuate în atelierul AutoMatrix Motors din Băicoi: cutii DSG, ZF, Aisin, Mercedes și CVT reparate, cu poze și detalii. Garanție 24 luni.", schema, body, active=slug))


# ------------------------------------------------------------------ CODURI DE EROARE
CODES_SLUG = "coduri-eroare-cutie-automata"


def code_link(k):
    return f'<a class="ecode" href="{url(CODES_SLUG)}#{k.lower()}">{k}</a>'


def codes_block(codes, heading="Coduri de eroare întâlnite la aceste lucrări"):
    if not codes:
        return ""
    items = "".join(f'<li>{code_link(k)}<span>{esc(CODE_MAP[k][1])}</span></li>' for k in codes)
    return f'<h2>{heading}</h2><p>Dacă aparatul de diagnoză arată unul dintre aceste coduri, apasă pe el ca să vezi ce înseamnă, ce simptome dă și cum se repară.</p><ul class="code-list">{items}</ul>'


def codes_page():
    slug = CODES_SLUG
    groups = [("Coduri generale OBD (toate cutiile automate)", [k for k, *_ in CODES if re.match(r"(P0[0-9A-F]{3}|U0[0-9]{3})$", k) and k not in ("P0718",)]),
              ("Coduri DSG, S tronic și PDK (VW, Audi, Skoda, Seat, Porsche)", ["P17BF", "P189C", "P179E", "P179F", "P1731", "P1732"]),
              ("Coduri Mercedes 7G-Tronic (722.9)", ["P0718", "P2767"]),
              ("Coduri CVT Nissan / Jatco", ["P17F0", "P17F1"])]
    toc = "".join(f'<a href="#{k.lower()}">{k}</a>' for _, ks in groups for k in ks)
    secs = ""
    for title, ks in groups:
        cards = ""
        for k in ks:
            _, t, mean, sym, boxes, _rx = CODE_MAP[k]
            fx = fixes_for(k, CATALOG)
            fix_html = "".join(f'<li><a href="{url("preturi-cutii-automate")}#{c["rid"]}">{esc(c["name"])}</a><b class="tnum">{fmt(c["price"])} lei</b></li>' for c in fx)
            wa = f'https://wa.me/{PHONE1_W}?text=' + html.escape(__import__("urllib.parse").parse.quote(f"Bună ziua! Mașina mea are codul de eroare {k}. Marca, modelul și anul: "))
            cards += f'''<article class="ecard" id="{k.lower()}" data-s="{esc(norm_s(k + " " + t + " " + boxes + " " + " ".join(sym)))}">
<div class="ecard-h"><span class="ecode big">{k}</span><h3>{esc(t)}</h3></div>
<p>{esc(mean)}</p>
<div class="ecard-g"><div><p class="pdh">Simptome</p><ul>{"".join(f"<li>{esc(x)}</li>" for x in sym)}</ul></div>
<div><p class="pdh">Cutii afectate</p><p class="eboxes">{esc(boxes)}</p></div></div>
{f'<p class="pdh" style="margin-top:18px">Lucrări care rezolvă de obicei acest cod</p><ul class="efix">{fix_html}</ul>' if fx else ''}
<div class="ecard-a"><a class="btn btn-wa btn-sm" href="{wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Am codul {k} – scrie-ne</a><a class="btn btn-line btn-sm" href="{PROG}" target="_blank" rel="noopener">Programează diagnoza</a></div>
</article>'''
        secs += f'<section class="egroup"><h2>{esc(title)}</h2>{cards}</section>'
    faq = [(f"Ce înseamnă codul {k}?", f"{CODE_MAP[k][1]}. {CODE_MAP[k][2]}") for k in ["P0700", "P0741", "P0730", "P0868", "P17BF", "P189C", "P2767", "P0776", "P0841", "P17F0"]]
    bx_cards, bx_hits = box_hub()
    ncodes = len(CODES) + sum(len(x["codes"]) for b in BOXES for x in b["codes"] if not x["main"].startswith("Fără cod"))
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">Coduri de eroare</li></ol></nav>
<div class="grid"><div><span class="eyebrow">Ghid</span><h1>Coduri de eroare cutie automată</h1><p class="lead">Ce înseamnă codurile pe care le arată aparatul de diagnoză, ce simptome dau și cum se repară. Caută codul tău sau alege-l din listă.</p>
<label class="search" style="margin-top:28px;max-width:460px"><span class="sr">Caută codul</span><svg aria-hidden="true"><use href="#i-search"/></svg><input id="code-q" type="search" placeholder="ex. P0741, P17BF, tremură, DSG…" autocomplete="off"></label></div>
{spec_html([("Coduri explicate", str(ncodes), "big"), ("Diagnoză", "cu programare", ""), ("Reparații", "24 luni, fără limită de km", "red"), ("Telefon", PHONE1, "")])}</div></div></section>
<section class="sec" style="padding-top:clamp(40px,5vw,64px)"><div class="wrap">
<div class="bxhits" id="bxhits" hidden><p class="pdh">Rezultate pe tipuri de cutii</p>{bx_hits}</div>
<section class="bxhub" id="bxhub" aria-labelledby="h-bx"><h2 id="h-bx">Coduri de eroare pe tipuri de cutii</h2><p>Același cod poate însemna lucruri diferite de la o cutie la alta. Alege cutia ta ca să vezi codurile specifice, simptomele, cum le rezolvăm și prețurile.</p><div class="bxgrid">{bx_cards}</div></section>
<h2 style="margin:56px 0 18px">Coduri generale OBD, valabile la majoritatea cutiilor</h2>
<nav class="etoc" aria-label="Lista codurilor">{toc}</nav>
<div id="ecodes">{secs}</div>
<p class="price-empty" id="code-empty" hidden>Nu avem încă explicat acest cod. Trimite-ne codul pe WhatsApp, la {PHONE1}, împreună cu marca, modelul și anul mașinii, și îți spunem ce înseamnă.</p>
<div class="callout" style="margin-top:48px"><p><b>Un cod de eroare nu e un diagnostic complet.</b> Același cod poate avea cauze diferite: ulei degradat, o electrovalvă, un senzor sau uzura ambreiajelor. Nu ștergeți codurile la întâmplare și nu schimbați piese după cod. Diagnoza arată exact cauza, iar prețul îl primiți în scris înainte de reparație.</p></div>
</div></section>
{faq_block(faq)}
{contact_section("Ai un cod de eroare? Cere o ofertă")}
{CODE_SEARCH_JS}"""
    defined = {"@type": "DefinedTermSet", "@id": canon(slug) + "#coduri", "name": "Coduri de eroare cutie automată", "url": canon(slug),
               "hasDefinedTerm": [{"@type": "DefinedTerm", "termCode": k, "name": f"{k}: {CODE_MAP[k][1]}", "description": CODE_MAP[k][2], "url": canon(slug) + "#" + k.lower()} for k, *_ in CODES]}
    schema = [defined, crumbs_schema([("Acasă", ""), ("Coduri de eroare", slug)]), faq_schema(faq)]
    write(slug, page(slug, "Coduri eroare cutie automată: P0700, P0741, P17BF | AutoMatrix",
                     f"Ce înseamnă codurile de eroare ale cutiei automate: P0700, P0730, P0741, P0868, P17BF, P189C (DSG DQ200), P2767 (7G-Tronic), P17F0 (CVT). Simptome, cauze și prețuri de reparație.",
                     schema, body, active=slug))


# ------------------------------------------------------------------ PAGINI CODURI PE CUTII
def wa_code(k):
    return f'https://wa.me/{PHONE1_W}?text=' + html.escape(__import__("urllib.parse").parse.quote(f"Bună ziua! Mașina mea are codul de eroare {k}. Marca, modelul și anul: "))


def row_li(c):
    pr = '<b class="pdiag">după diagnoză</b>' if c.get("price") is None else f'<b class="tnum">{fmt(c["price"])} lei</b>'
    return f'<li><a href="{url("preturi-cutii-automate")}#{c["rid"]}">{esc(c["name"])}</a>{pr}</li>'


def box_page(b):
    slug = b["slug"]
    allrows = box_rows(b)
    cards, toc, terms = "", "", []
    for x in b["codes"]:
        nocode = x["main"].startswith("Fără cod")
        label = "Fără cod" if nocode else x["main"]
        fx = box_rows(b, x["kind"], limit=3)
        others = [k for k in x["codes"][1:]]
        sdata = norm_s(" ".join(k + " " + k.replace("-", "") for k in x["codes"]) + " " + x["title"] + " " + x["expl"] + " " + " ".join(x["sym"]))
        sym_html = f'<div><p class="pdh">Simptome</p><ul>{"".join(f"<li>{esc(y)}</li>" for y in x["sym"])}</ul></div>' if x["sym"] else ""
        also = f'<p class="pdh" style="margin-top:14px">Coduri din aceeași categorie</p><p class="pcodes">{"".join(f"<span class=ecode>{esc(k)}</span>" for k in others)}</p>' if others else ""
        cards += f'''<article class="ecard" id="{x["id"]}" data-s="{esc(sdata)}">
<div class="ecard-h"><span class="ecode big">{esc(label)}</span><h3>{esc(x["title"])}</h3></div>
<p>{esc(x["expl"])}</p>
<div class="ecard-g">{sym_html}<div><p class="pdh">Cum rezolvăm</p><p class="efixt">{esc(x["fix"])}</p>{also}</div></div>
{f'<p class="pdh" style="margin-top:18px">Lucrări și prețuri</p><ul class="efix">{"".join(row_li(c) for c in fx)}</ul>' if fx else ''}
<div class="ecard-a"><a class="btn btn-wa btn-sm" href="{wa_code(label if not nocode else b['short'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>{"Am codul " + esc(label) if not nocode else "Am această problemă"} – scrie-ne</a><a class="btn btn-line btn-sm" href="{PROG}" target="_blank" rel="noopener">Programează diagnoza</a></div>
</article>'''
        if not nocode:
            toc += f'<a href="#{x["id"]}">{esc(x["main"])}</a>'
            terms.append({"@type": "DefinedTerm", "termCode": x["main"], "name": f'{x["main"]}: {x["title"]} ({b["short"]})', "description": x["expl"], "url": canon(slug) + "#" + x["id"]})
    tips = "".join(f'<li>{esc(t)}</li>' for t in b["tips"])
    nreal = sum(len(x["codes"]) for x in b["codes"] if not x["main"].startswith("Fără cod"))
    priced = [c for c in allrows if c.get("price") and c["kind"] == "reparatie"]
    price_txt = f"de la {fmt(min(c['price'] for c in priced))} lei" if priced else "după diagnoză"
    main = [x for x in b["codes"] if not x["main"].startswith("Fără cod")][:3]
    faq = [(f"Ce înseamnă codul {x['main']} la cutia {b['short']}?", f"{x['title']}. {x['expl']} {x['fix']}") for x in main]
    if priced:
        faq.append((f"Cât costă reparația cutiei {b['short']}?", f"Reparațiile pentru {b['short']} pornesc de la {fmt(min(c['price'] for c in priced))} lei, cu manoperă și TVA incluse. Prețul exact îl primești în scris după diagnoză, în funcție de coduri și de ce găsim la verificare."))
    else:
        faq.append((f"Cât costă reparația cutiei {b['short']}?", f"Reparăm cutiile {b['short']}, iar prețul se stabilește după diagnoză, în funcție de codurile de eroare și de ce găsim la verificare. Îl primești în scris înainte de orice lucrare."))
    faq.append(("Ce garanție are reparația?", "24 de luni, fără limită de kilometri, pentru piese și manoperă. Garanția e scrisă și e unică în România."))
    others = "".join(f'<a href="{url(o["slug"])}">{esc(o["short"])}</a>' for o in BOXES if o["slug"] != slug)
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li><a href="{url(CODES_SLUG)}">Coduri de eroare</a></li><li aria-current="page">{esc(b["short"])}</li></ol></nav>
<div class="grid"><div><span class="eyebrow">Coduri de eroare</span><h1>Coduri de eroare cutie {esc(b["name"])}</h1><p class="lead">{esc(b["intro"])}</p>
<label class="search" style="margin-top:28px;max-width:460px"><span class="sr">Caută codul</span><svg aria-hidden="true"><use href="#i-search"/></svg><input id="code-q" type="search" placeholder="ex. {esc(main[0]['main'] if main else 'simptom')}, patinare, nu pleacă…" autocomplete="off"></label></div>
{spec_html([("Coduri explicate", str(nreal), "big"), ("Reparație", price_txt, ""), ("Garanție reparații", "24 luni, fără limită de km", "red"), ("Telefon", PHONE1, "")])}</div></div></section>
<section class="sec" style="padding-top:clamp(40px,5vw,64px)"><div class="wrap">
<div class="bxinfo"><div><p class="pdh">Pe ce mașini se montează</p><p>{esc(b["cars"])}</p></div>{f'<div><p class="pdh">Bine de știut</p><ul class="dots">{tips}</ul></div>' if tips else ''}</div>
{f'<nav class="etoc" aria-label="Lista codurilor">{toc}</nav>' if toc else ''}
<div id="ecodes"><section class="egroup"><h2>Codurile și ce înseamnă</h2>{cards}</section></div>
<p class="price-empty" id="code-empty" hidden>Nu avem încă explicat acest cod pentru {esc(b["short"])}. Trimite-ne codul pe WhatsApp, la {PHONE1}, împreună cu marca, modelul și anul mașinii, și îți spunem ce înseamnă.</p>
<section class="egroup" style="margin-top:56px"><h2>Lucrări și prețuri pentru {esc(b["short"])}</h2><ul class="efix">{"".join(row_li(c) for c in allrows)}</ul>
<p style="font-size:.9rem;color:var(--ink-3);margin-top:14px">Prețuri cu TVA și manoperă incluse. La lucrările marcate „după diagnoză”, prețul se stabilește în funcție de erori și de constatare și îl primești în scris înainte de reparație. <a class="link" href="{url("preturi-cutii-automate")}">Toate prețurile</a></p></section>
<div class="callout" style="margin-top:48px"><p><b>Un cod de eroare nu e un diagnostic complet.</b> Același cod poate avea cauze diferite. Nu ștergeți codurile la întâmplare și nu schimbați piese după cod: diagnoza arată exact cauza. Reparațiile au <b>garanție 24 de luni, fără limită de kilometri, unică în România.</b></p></div>
<nav class="bxother" aria-label="Alte cutii"><p class="pdh">Coduri pentru alte cutii</p><div class="etoc">{others}<a href="{url(CODES_SLUG)}">Coduri generale OBD</a></div></nav>
</div></section>
{faq_block(faq)}
{contact_section("Ai un cod de eroare? Cere o ofertă")}
{CODE_SEARCH_JS}"""
    schema = [{"@type": "DefinedTermSet", "@id": canon(slug) + "#coduri", "name": f"Coduri de eroare {b['name']}", "url": canon(slug), "hasDefinedTerm": terms},
              crumbs_schema([("Acasă", ""), ("Coduri de eroare", CODES_SLUG), (b["short"], slug)]), faq_schema(faq)]
    first = ", ".join(x["main"].split("-")[0] for x in main[:3])
    title = f"Coduri eroare {b['short']}" + (f": {first}" if first else "") + " | AutoMatrix"
    if len(title) > 70:
        title = f"Coduri eroare {b['short']} | AutoMatrix"
    desc = f"Ce înseamnă codurile de eroare ale cutiei {b['name']}" + (f" ({first})" if first else "") + ": simptome, cauze, cum se repară și prețuri. Reparații cu garanție 24 de luni, fără limită de km."
    write(slug, page(slug, title, desc, schema, body, active=CODES_SLUG))


def nr_coduri(n):
    if n == 1:
        return "1 cod explicat"
    return f"{n} coduri explicate" if 0 < n % 100 < 20 else f"{n} de coduri explicate"


def box_hub():
    cards = ""
    for b in BOXES:
        n = sum(len(x["codes"]) for x in b["codes"] if not x["main"].startswith("Fără cod"))
        diag = not [c for c in box_rows(b) if c.get("price") and c["kind"] == "reparatie"]
        cards += f'<a class="bxcard" href="{url(b["slug"])}"><b>{esc(b["short"])}</b><span>{esc(b["cars"].split(";")[0])}</span><small>{nr_coduri(n) if n else "defecte fără cod"}{" · preț după diagnoză" if diag else ""}</small></a>'
    hits = ""
    for b in BOXES:
        for x in b["codes"]:
            if x["main"].startswith("Fără cod"):
                continue
            sd = norm_s(" ".join(k + " " + k.replace("-", "") for k in x["codes"]) + " " + x["title"] + " " + b["short"] + " " + " ".join(x["sym"]))
            hits += f'<a class="bxhit" hidden data-s="{esc(sd)}" href="{url(b["slug"])}#{x["id"]}"><span class="ecode">{esc(x["main"])}</span><span><b>{esc(b["short"])}</b>: {esc(x["title"])}</span></a>'
    return cards, hits


CODE_SEARCH_JS = """<script>
(function(){var q=document.getElementById('code-q');if(!q)return;var cards=[].slice.call(document.querySelectorAll('.ecard')),gs=[].slice.call(document.querySelectorAll('#ecodes .egroup')),hs=[].slice.call(document.querySelectorAll('.bxhit')),hw=document.getElementById('bxhits'),em=document.getElementById('code-empty');
function n(t){return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')}
q.addEventListener('input',function(){var v=q.value.trim(),ts=n(v).split(/\\s+/).filter(Boolean),c=0,h=0;cards.forEach(function(e){var ok=ts.every(function(t){return e.dataset.s.indexOf(t)>-1});e.hidden=!ok;if(ok)c++});gs.forEach(function(g){g.hidden=!g.querySelector('.ecard:not([hidden])')});
hs.forEach(function(e){var ok=ts.length>0&&ts.every(function(t){return e.dataset.s.indexOf(t)>-1})&&h<40;e.hidden=!ok;if(ok)h++});if(hw)hw.hidden=h===0;var hb=document.getElementById('bxhub');if(hb)hb.hidden=ts.length>0;em.hidden=c+h>0;});
})();
</script>"""


# ------------------------------------------------------------------ ARTICOLE + DESPRE NOI
from articles import articles as _articles
ARTICLES = _articles(fmt)


def link_card(slug):
    m = {p["slug"]: (p["nav"], p.get("navsub", "")) for p in PAGES}
    m.update({a["slug"]: (a["title"], "Articol") for a in ARTICLES})
    m.update({b["slug"]: ("Coduri eroare " + b["short"], "Coduri, simptome și prețuri") for b in BOXES})
    m["preturi-cutii-automate"] = ("Prețuri cutii automate", "Lista completă cu revizii și reparații")
    m["coduri-eroare-cutie-automata"] = ("Coduri de eroare cutie automată", "568 de coduri explicate")
    if slug not in m:
        return ""
    t, sub = m[slug]
    return f'<a href="{url(slug)}"><h3>{esc(t)}</h3><p>{esc(sub)}</p></a>'


def sources_html(a):
    src = [x for x in a.get("sources", []) if isinstance(x, dict) and str(x.get("url", "")).startswith("https://")]
    if not src:
        return ""
    li = "".join(f'<li><a class="link" href="{esc(x["url"])}" target="_blank" rel="noopener nofollow">{esc(x.get("title") or x["url"])}</a></li>' for x in src[:6])
    return f'<h2>Surse</h2><ul class="dots">{li}</ul>'


def article_page(a):
    slug = a["slug"]
    trail = [("Acasă", ""), ("Articole", "articole"), (a["h1"], slug)]
    rel = "".join(link_card(s) for s in a["related"])
    others = "".join(f'<li><a class="link" href="{url(o["slug"])}">{esc(o["h1"])}</a></li>' for o in [x for x in ARTICLES if x["slug"] != slug][:8])
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li><a href="{url("articole")}">Articole</a></li><li aria-current="page">{esc(a["h1"])}</li></ol></nav>
<div class="narrow" style="max-width:820px"><span class="eyebrow">Articol · {a["date"][8:10]}.{a["date"][5:7]}.{a["date"][:4]} · Echipa AutoMatrix Motors</span><h1>{esc(a["h1"])}</h1><p class="lead">{esc(a["lead"])}</p></div></div></section>
<section class="sec"><div class="wrap article"><div class="prose">{a["body"]}
<div class="callout" style="margin-top:44px"><p><b>Ai o problemă la cutie?</b> Sună la {PHONE1} sau scrie-ne pe WhatsApp un video cu simptomul. Reparațiile au <b>garanție 24 de luni, fără limită de kilometri, unică în România.</b></p></div>
{sources_html(a)}<h2>Alte articole</h2><ul class="dots">{others}</ul>
</div>{aside_html(slug)}</div></section>
{faq_block(a["faq"])}
<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head" style="margin-bottom:32px"><h2 style="font-size:var(--s-lg)">Citește și</h2></div><div class="related">{rel}</div></div></section>
{contact_section()}"""
    schema = [{"@type": "Article", "@id": canon(slug) + "#article", "headline": a["h1"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"], "inLanguage": "ro-RO",
               "author": {"@type": "Organization", "name": "AutoMatrix Motors", "url": SITE + "/"}, "publisher": {"@id": SITE + "/#business"}, "mainEntityOfPage": canon(slug), "image": SITE + "/assets/img/og-automatrix.jpg"},
              crumbs_schema(trail), faq_schema(a["faq"])]
    write(slug, page(slug, a["title"] + " | AutoMatrix", a["desc"], schema, body, active="articole"))


def articles_index():
    slug = "articole"
    cards = "".join(f'<a href="{url(a["slug"])}"><h3>{esc(a["h1"])}</h3><p>{esc(a["desc"])}</p></a>' for a in ARTICLES)
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">Articole</li></ol></nav>
<div class="narrow" style="max-width:820px"><span class="eyebrow">Ghiduri</span><h1>Articole despre cutii automate</h1><p class="lead">Răspunsuri scrise de mecanicii noștri la întrebările pe care le auzim zilnic: simptome, costuri, întreținere și ce să faci când cutia dă probleme.</p></div></div></section>
<section class="sec"><div class="wrap"><div class="related">{cards}</div></div></section>
{contact_section()}"""
    schema = [{"@type": "CollectionPage", "@id": canon(slug) + "#page", "name": "Articole despre cutii automate", "url": canon(slug), "inLanguage": "ro-RO",
               "hasPart": [{"@type": "Article", "headline": a["h1"], "url": canon(a["slug"])} for a in ARTICLES]}, crumbs_schema([("Acasă", ""), ("Articole", slug)])]
    write(slug, page(slug, "Articole despre cutii automate: simptome, costuri, sfaturi | AutoMatrix", "Ghiduri despre cutii automate: DSG care smucește, probleme Powershift, cât costă revizia, mod avarie, schimbul de ulei, convertizorul care vibrează, tractarea corectă.", schema, body, active="articole"))


def about_page():
    slug = "despre-noi"
    faq = [("Unde este atelierul?", "În Băicoi, Str. Înfrățirii nr. 111, județul Prahova, pe DN1 între Ploiești și Câmpina."),
           ("Ce garanție oferiți?", "24 de luni, fără limită de kilometri, pentru reparațiile de cutii automate, pentru piese și manoperă."),
           ("Cine este firma din spatele AutoMatrix Motors?", "E-VOL AUTO SERVICE CENTER S.R.L., CUI RO40377191, înregistrată în 2019.")]
    body = f"""<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{url("")}">Acasă</a></li><li aria-current="page">Despre noi</li></ol></nav>
<div class="grid"><div><span class="eyebrow">Despre noi</span><h1>AutoMatrix Motors, atelier specializat în cutii automate</h1><p class="lead">Suntem un atelier din Băicoi, Prahova, care lucrează aproape exclusiv pe cutii de viteze automate și pe motoare de performanță. Avem 7 posturi de lucru și 10 mecanici, iar clienții vin la noi din tot sudul și centrul țării.</p>
<div class="hero-cta"><a class="btn btn-red" href="{PROG}" target="_blank" rel="noopener">Programează-te online</a><a class="btn btn-line" href="{url("lucrari-efectuate")}">Vezi lucrări efectuate</a></div></div>
{spec_html([("Posturi de lucru", "7", "big"), ("Mecanici", "10", ""), ("Garanție reparații", "24 luni, fără limită de km", "red"), ("Recenzii Google", "peste 300", "")])}</div></div></section>
<section class="sec"><div class="wrap article"><div class="prose">
<h2>Ce facem</h2>
<p>Reparăm și revizuim cutii automate de toate tipurile: DSG și S tronic, Powershift și EDC, ZF 6HP, 8HP și 9HP, Aisin, Mercedes 7G-Tronic și 9G-Tronic, CVT și Multitronic. Lucrăm și pe motoare de performanță: BMW M, Audi RS, Mercedes-AMG.</p>
<h2>Cum lucrăm</h2>
<ul class="ticks">
<li><b>Prețuri publice.</b> Peste 360 de lucrări au prețul afișat pe site, cu operațiunile, piesele și simptomele fiecăreia</li>
<li><b>Deviz în scris</b> după diagnoză, înainte de orice lucrare</li>
<li><b>Reviziile după manualul producătorului cutiei,</b> fără aparat de schimb ulei, cu ulei Motul cu specificația cerută</li>
<li><b>Piese noi</b> la reparații și adaptări cu aparat dedicat mărcii</li>
<li><b>Garanție 24 de luni, fără limită de kilometri,</b> unică în România</li>
</ul>
<h2>Firma</h2>
<p>AutoMatrix Motors este marca firmei E-VOL AUTO SERVICE CENTER S.R.L., CUI RO40377191, nr. Registrul Comerțului J2019000071295, cu sediul atelierului în Băicoi, Str. Înfrățirii nr. 111, județul Prahova. Administrator: Daniel Nenu.</p>
<h2>Program</h2>
<p>Atelier: luni–vineri, 06:00–14:30. Programări la telefon și pe WhatsApp: luni–vineri 07:00–18:00, sâmbătă 09:00–15:00, la {PHONE1} și {PHONE2}.</p>
</div>{aside_html(slug)}</div></section>
{faq_block(faq)}
{contact_section()}"""
    schema = [{"@type": "AboutPage", "@id": canon(slug) + "#page", "url": canon(slug), "name": "Despre AutoMatrix Motors", "about": {"@id": SITE + "/#business"}, "inLanguage": "ro-RO"},
              crumbs_schema([("Acasă", ""), ("Despre noi", slug)]), faq_schema(faq)]
    write(slug, page(slug, "Despre AutoMatrix Motors: atelier de cutii automate din Băicoi", "AutoMatrix Motors: atelier specializat în cutii de viteze automate din Băicoi, Prahova. 7 posturi de lucru, 10 mecanici, prețuri publice, garanție 24 luni fără limită de km.", schema, body))


attach_box_codes()
for _a in ARTICLES:
    article_page(_a)
articles_index()
about_page()
home()
programari()
lucrari()
codes_page()
for b in BOXES:
    box_page(b)
for p in PAGES:
    service_page(p)
price_page()
for c in CITIES:
    city_page(c)
legal("politica-confidentialitate", "politica-confidentialitate.html", "Politica de confidențialitate", "Cum prelucrează E-VOL AUTO SERVICE CENTER S.R.L. (AutoMatrix Motors) datele personale, conform GDPR și Legii nr. 190/2018.")
legal("politica-cookies", "politica-cookies.html", "Politica de cookie-uri", "Ce cookie-uri folosește automatrixmotors.ro și cum îți poți schimba acordul, conform Legii nr. 506/2004 și GDPR.")
if not PREVIEW:
    (OUT / "assets/js").mkdir(parents=True, exist_ok=True)
    (OUT / "assets/js/main.js").write_text(MAINJS)
    notfound()
    slugs = [""] + [p["slug"] for p in PAGES] + ["preturi-cutii-automate", "lucrari-efectuate", "coduri-eroare-cutie-automata"] + [b["slug"] for b in BOXES] + ["articole", "despre-noi"] + [a["slug"] for a in ARTICLES] + [c["slug"] for c in CITIES] + ["politica-confidentialitate", "politica-cookies"]
    pri = {"": "1.0", "reparatii-cutii-automate": "0.9", "preturi-cutii-automate": "0.9", "politica-confidentialitate": "0.2", "politica-cookies": "0.2"}
    lm = {a["slug"]: a["date"] for a in ARTICLES}
    lm["articole"] = max([UPDATED] + [a["date"] for a in ARTICLES])
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'  <url><loc>{canon(s)}</loc><lastmod>{lm.get(s, UPDATED)}</lastmod><priority>{pri.get(s, "0.8")}</priority></url>\n' for s in slugs) + "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sm)
    # manifest pentru actualizarea automată de pe server (deploy-continut.php)
    deploy = sorted([f.name for f in OUT.glob("*.html")] + ["sitemap.xml", "assets/js/main.js"])
    man = {"generated": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
           "files": {n: hashlib.sha256((OUT / n).read_bytes()).hexdigest() for n in deploy}}
    (OUT / "manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    (OUT / "df86ff09ede0f5fe9303b2c19de9adee.txt").write_text("df86ff09ede0f5fe9303b2c19de9adee")  # cheie IndexNow (Bing, Yandex)
print("built", MODE, sorted(f.name for f in OUT.glob("*.html")))
