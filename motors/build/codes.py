# -*- coding: utf-8 -*-
"""Transmission fault codes (SAE OBD-II generic + verified manufacturer codes) and symptom sets,
linked to the repair catalogue."""
import re

# code, title, meaning, symptoms, gearboxes, regex of catalogue repairs that typically fix it
CODES = [
    ("P0700", "Eroare în sistemul de control al cutiei automate",
     "Cod general: calculatorul motorului anunță că și calculatorul cutiei (TCM) are erori memorate. Codul în sine nu spune defectul; trebuie citite codurile din cutie.",
     ["martorul Check Engine aprins", "cutia poate intra în modul de avarie", "schimbări dure sau întârziate"],
     "toate cutiile automate", r"mecatronic|placă electronică|electrovalve|bloc de valve|Reparație (completă )?cutie"),
    ("P0705", "Senzorul de poziție a selectorului, circuit defect",
     "Calculatorul nu primește corect poziția manetei (P, R, N, D). Cauzele frecvente sunt senzorul de poziție, conectorul sau, la cutiile cu mecatronic, senzorul integrat.",
     ["pe bord nu apare corect treapta selectată", "mașina nu pornește în P sau N", "cutia intră în avarie"],
     "ZF, Aisin, Mercedes, DSG", r"mecatronic|placă electronică|G676"),
    ("P0710", "Senzorul de temperatură a uleiului din cutie, circuit defect",
     "Senzorul de temperatură a uleiului transmite valori lipsă sau imposibile. La multe cutii senzorul e integrat în mecatronic sau în placa electronică.",
     ["schimbări dure la rece sau la cald", "cutia intră în avarie", "ventilatorul sau răcirea cutiei nu funcționează corect"],
     "ZF, Mercedes 7G-Tronic, Aisin", r"placă electronică|Recondiționare mecatronic|electrovalve"),
    ("P0715", "Senzorul de turație de intrare (turbină), circuit defect",
     "Calculatorul nu citește corect turația arborelui de intrare. Tipic la Mercedes 7G-Tronic, unde senzorii de turație sunt pe placa conductoare.",
     ["cutia rămâne în treapta a 2-a sau a 3-a", "mod de avarie", "vitezometrul sau turometrul se comportă ciudat"],
     "Mercedes 7G-Tronic, ZF, Aisin", r"placă electronică|mecatronic"),
    ("P0717", "Senzorul de turație de intrare (turbină), lipsă semnal",
     "Semnalul senzorului de turație de intrare lipsește. La Mercedes 722.9 (7G-Tronic) e unul dintre codurile clasice ale plăcii conductoare defecte.",
     ["cutia rămâne în treapta a 2-a", "mod de avarie", "schimbări bruște după ce cutia se resetează"],
     "Mercedes 7G-Tronic (722.9), ZF", r"placă electronică|mecatronic"),
    ("P0720", "Senzorul de turație de ieșire, circuit defect",
     "Calculatorul nu citește turația arborelui de ieșire. Poate fi senzorul, cablajul sau electronica din mecatronic.",
     ["schimbări haotice", "vitezometrul nu funcționează sau sare", "mod de avarie"],
     "ZF, Aisin, Mercedes", r"placă electronică|mecatronic"),
    ("P0730", "Raport de transmisie incorect",
     "Raportul dintre turația de intrare și cea de ieșire nu corespunde treptei cuplate: un ambreiaj intern patinează sau presiunea e prea mică.",
     ["patinare la schimbare", "turația crește fără accelerare", "mod de avarie"],
     "toate cutiile automate", r"Înlocuire ambreiaje cutie|kit ambreiaje|Reparație (completă )?cutie|bloc de valve"),
    ("P0731", "Raport incorect în treapta 1",
     "Treapta 1 nu ține raportul corect, de obicei din cauza uzurii ambreiajelor sau a presiunii insuficiente.",
     ["plecare greoaie", "patinare în treapta 1", "smucitură la trecerea din 1 în 2"],
     "cutii cu convertizor", r"Înlocuire ambreiaje cutie|Reparație (completă )?cutie|bloc de valve"),
    ("P0732", "Raport incorect în treapta 2",
     "Treapta 2 patinează: uzura pachetului de ambreiaje sau presiune scăzută în circuitul treptei.",
     ["patinare la trecerea în 2", "turație mare fără accelerare", "mod de avarie"],
     "cutii cu convertizor", r"Înlocuire ambreiaje cutie|Reparație (completă )?cutie|bloc de valve"),
    ("P0733", "Raport incorect în treapta 3",
     "Treapta 3 nu ține raportul. Cauza tipică e uzura ambreiajelor sau o pierdere de presiune.",
     ["patinare în treapta 3", "schimbare întârziată", "mod de avarie"],
     "cutii cu convertizor", r"Înlocuire ambreiaje cutie|Reparație (completă )?cutie|bloc de valve"),
    ("P0734", "Raport incorect în treapta 4",
     "Treapta 4 patinează. Apare des la cutiile cu ulei degradat sau cu ambreiaje uzate.",
     ["patinare la viteză de oraș", "consum crescut", "mod de avarie"],
     "cutii cu convertizor", r"Înlocuire ambreiaje cutie|Reparație (completă )?cutie|bloc de valve"),
    ("P0735", "Raport incorect în treapta 5",
     "Treapta 5 nu ține raportul corect: uzură internă sau presiune insuficientă.",
     ["patinare la viteză mare", "turație mare pe autostradă", "mod de avarie"],
     "cutii cu convertizor", r"Înlocuire ambreiaje cutie|Reparație (completă )?cutie"),
    ("P0740", "Ambreiajul convertizorului de cuplu, circuit defect",
     "Calculatorul detectează o problemă în circuitul de comandă al ambreiajului de blocare din convertizor.",
     ["tremurături la viteză constantă", "consum crescut", "turație mai mare decât normal"],
     "ZF 6HP, ZF 8HP, Mercedes, Aisin", r"convertizor|electrovalve|Recondiționare mecatronic"),
    ("P0741", "Ambreiajul convertizorului de cuplu, performanță slabă sau blocat deschis",
     "Ambreiajul de blocare din convertizor patinează sau nu se cuplează. E cauza clasică a tremurăturilor între 60 și 100 km/h.",
     ["tremurături fine între 60 și 100 km/h", "turația crește fără accelerare", "cutia se încălzește"],
     "ZF 6HP, ZF 8HP, Mercedes 7G / 9G-Tronic, Aisin", r"convertizor"),
    ("P0743", "Ambreiajul convertizorului de cuplu, circuit electric",
     "Defect electric în circuitul electrovalvei care comandă ambreiajul convertizorului.",
     ["convertizorul nu se blochează", "consum crescut", "mod de avarie"],
     "ZF, Aisin, Mercedes", r"electrovalve|Recondiționare mecatronic|placă electronică"),
    ("P0745", "Electrovalva de control al presiunii A, defect",
     "Electrovalva care reglează presiunea principală nu funcționează corect. Cod foarte frecvent la cutia AL4 / DP0 (Peugeot, Citroën, Renault).",
     ["schimbări dure", "mod de avarie, de obicei în treapta 3", "martor de avarie al cutiei aprins"],
     "AL4 / DP0, ZF, Aisin", r"electrovalve|bloc de valve"),
    ("P0746", "Electrovalva de control al presiunii A, performanță slabă sau blocată",
     "Presiunea reglată de electrovalvă nu corespunde comenzii. Tipic pentru electrovalvele uzate sau pentru uleiul degradat.",
     ["șocuri la schimbare", "mod de avarie", "schimbări întârziate"],
     "AL4 / DP0, ZF, Aisin", r"electrovalve|bloc de valve"),
    ("P0750", "Electrovalva de schimbare A, defect",
     "Una dintre electrovalvele care comandă schimbarea treptelor nu răspunde corect.",
     ["cutia nu schimbă una dintre trepte", "mod de avarie", "schimbări dure"],
     "cutii cu convertizor", r"electrovalve|bloc de valve|Recondiționare mecatronic"),
    ("P0755", "Electrovalva de schimbare B, defect",
     "Electrovalva B de schimbare nu funcționează corect: bobină defectă, conector sau uzură.",
     ["lipsesc anumite trepte", "mod de avarie", "smucituri"],
     "cutii cu convertizor", r"electrovalve|bloc de valve|Recondiționare mecatronic"),
    ("P0776", "Electrovalva de control al presiunii B, performanță slabă sau blocată",
     "Presiunea din circuitul B nu e cea comandată. Cod frecvent la cutiile Aisin cu 6 trepte (TF-80SC, AWF21), legat de uzura blocului de valve.",
     ["șoc la trecerea din 2 în 3", "smucituri la decelerare", "mod de avarie"],
     "Aisin TF-80SC / AWF21 (Volvo, Ford, Opel, Peugeot)", r"bloc de valve|Aisin"),
    ("P0780", "Defect la schimbarea treptelor",
     "Calculatorul a detectat o schimbare de treaptă care nu s-a realizat corect sau la timp.",
     ["schimbări întârziate", "smucituri", "mod de avarie"],
     "toate cutiile automate", r"mecatronic|bloc de valve|electrovalve|Reparație (completă )?cutie"),
    ("P0796", "Electrovalva de control al presiunii C, performanță slabă sau blocată",
     "Presiunea din circuitul C diferă de comandă: uzura blocului de valve sau a electrovalvei.",
     ["schimbări dure", "flare (turația sare) la schimbare", "mod de avarie"],
     "Aisin, ZF, GM 6T", r"bloc de valve|electrovalve|Aisin"),
    ("P0841", "Senzorul de presiune A, valori în afara intervalului",
     "Senzorul de presiune din cutie raportează valori neplauzibile. La DSG DQ381 / DQ500 indică de obicei senzorii de presiune din mecatronic.",
     ["șocuri la schimbare", "litera treptei clipește pe bord", "mod de avarie"],
     "DSG DQ250 / DQ381 / DQ500, ZF", r"senzori de presiune|mecatronic DSG|Recondiționare mecatronic"),
    ("P0846", "Senzorul de presiune B, valori în afara intervalului",
     "Al doilea senzor de presiune (de obicei pentru celălalt ambreiaj la cutiile DSG) dă valori greșite.",
     ["lipsesc treptele pare sau impare", "șocuri", "mod de avarie"],
     "DSG DQ250 / DQ381 / DQ500", r"senzori de presiune|mecatronic DSG"),
    ("P0868", "Presiune scăzută a uleiului din cutie",
     "Presiunea de ulei nu ajunge la valoarea necesară: nivel scăzut, scurgeri, pompă uzată sau garnituri întărite.",
     ["patinare", "întârziere la cuplarea în D sau R", "mod de avarie"],
     "toate cutiile automate, CVT", r"pompă auxiliară|Set garnituri mecatronic|Reparație (completă )?cutie|Înlocuire ambreiaje cutie"),
    ("P0894", "O componentă a cutiei patinează",
     "Calculatorul observă patinare internă: ambreiaje uzate, presiune insuficientă sau convertizor uzat.",
     ["turația crește fără accelerare", "miros de ulei ars", "mod de avarie"],
     "toate cutiile automate", r"Înlocuire ambreiaje cutie|kit ambreiaje|Reparație (completă )?cutie|convertizor"),
    ("P0218", "Temperatură prea mare a uleiului din cutie",
     "Uleiul cutiei s-a supraîncălzit: convertizor care patinează, răcire insuficientă, ulei degradat sau tractare grea.",
     ["mesaj de supraîncălzire a cutiei", "cutia reduce puterea", "mod de avarie"],
     "toate cutiile automate", r"convertizor"),
    ("P0810", "Eroare de control al poziției ambreiajului",
     "La cutiile cu dublu ambreiaj uscat (Powershift, EDC, DQ200), calculatorul nu poate controla corect poziția ambreiajului.",
     ["vibrații la plecare", "smucituri la manevre", "mod de avarie"],
     "Ford Powershift, Renault EDC, DSG DQ200", r"Powershift|EDC|DQ200|DCT"),
    ("P0811", "Patinare excesivă a ambreiajului A",
     "Ambreiajul A (treptele impare la cutiile cu dublu ambreiaj) patinează peste limită. Semn tipic de uzură a ambreiajului.",
     ["plecare greoaie", "turația crește la accelerare", "miros de ambreiaj ars"],
     "Ford Powershift, Renault EDC, DSG, Hyundai / Kia DCT", r"ambreiaj|ambreiaje"),
    ("P0900", "Circuitul actuatorului de ambreiaj, întrerupt",
     "Actuatorul care acționează ambreiajul nu mai e comandat electric. Cod cunoscut la Ford Powershift (DPS6, 6DCT250).",
     ["mașina nu pleacă sau pleacă cu greu", "mod de avarie", "mesaj de defect al cutiei"],
     "Ford Powershift 6DCT250 (DPS6)", r"Powershift|6DCT250"),
    ("P07A3", "Elementul de fricțiune A blocat cuplat",
     "Un ambreiaj (element de fricțiune) rămâne cuplat când ar trebui să se decupleze. Apare la cutiile Powershift și DCT.",
     ["smucituri puternice la oprire", "motorul se poate opri la stop", "mod de avarie"],
     "Ford Powershift, cutii DCT", r"Powershift|DCT|EDC"),
    ("U0101", "Comunicație pierdută cu calculatorul cutiei (TCM)",
     "Calculatoarele mașinii nu mai comunică cu calculatorul cutiei: defect de TCU, alimentare, conector sau rețea CAN.",
     ["cutia rămâne într-o singură treaptă", "multe martoare aprinse pe bord", "mașina nu pornește în unele cazuri"],
     "toate cutiile automate", r"calculator TCU|mecatronic|placă electronică"),
    ("P17BF", "DSG DQ200: protecție la suprasarcină a sistemului pompei hidraulice",
     "Cod specific cutiei DSG cu 7 trepte DQ200 (0AM / 0CW): pompa hidraulică a mecatronicului funcționează prea mult, pentru că presiunea nu se menține. Cauze tipice: acumulator fisurat, bloc de valve sau mecatronic uzat.",
     ["litera treptei clipește pe bord", "cutia intră în avarie sau nu mai pleacă", "pompa mecatronicului se aude funcționând des"],
     "DSG DQ200 (VW, Skoda, Audi, Seat)", r"DQ200"),
    ("P189C", "DSG DQ200: funcționare limitată din cauza presiunii insuficiente",
     "Cod specific DQ200: presiunea necesară nu se formează sau se formează prea încet, iar calculatorul limitează funcționarea cutiei. Adesea apare împreună cu P17BF.",
     ["mod de avarie", "lipsesc treptele pare sau impare", "mașina pleacă greu sau deloc"],
     "DSG DQ200 (VW, Skoda, Audi, Seat)", r"DQ200"),
    ("P179E", "S tronic 0B5: senzorul de poziție G676",
     "Eroare a senzorului de poziție G676 (Drive Position Sensor) din cutia Audi S tronic 0B5 cu 7 trepte. Apare împreună cu P179F.",
     ["lipsesc anumite trepte", "mod de avarie", "smucituri"],
     "Audi S tronic 0B5 (A4, A5, A6, Q5), Porsche Macan", r"G676|0B5"),
    ("P179F", "S tronic 0B5: senzorul de poziție G676",
     "A doua variantă a erorii senzorului de poziție G676 din cutia 0B5. Se repară prin înlocuirea senzorului și a componentelor afectate din mecatronic.",
     ["mod de avarie", "cutia nu cuplează una dintre trepte", "eroare intermitentă"],
     "Audi S tronic 0B5, Porsche Macan", r"G676|0B5"),
    ("P1731", "Porsche PDK: senzorul de distanță (poziție)",
     "Eroare a senzorului de distanță din cutia Porsche PDK (ZF 7DT). Apare de obicei împreună cu P1732.",
     ["cutia intră în avarie", "nu cuplează unele trepte", "mesaj PDK pe bord"],
     "Porsche PDK (ZF 7DT)", r"PDK"),
    ("P1732", "Porsche PDK: senzorul de distanță (poziție)",
     "A doua eroare a senzorului de distanță din PDK. Reparația presupune demontarea cutiei și înlocuirea senzorului.",
     ["mod de avarie", "smucituri la schimbare", "mesaj PDK pe bord"],
     "Porsche PDK (ZF 7DT)", r"PDK"),
    ("P0718", "Mercedes 722.9: senzorul de turație turbină, semnal defect",
     "Semnalul senzorului de turație de la turbină (Y3/8n1) e defect. Indică de obicei placa conductoare a cutiei 7G-Tronic.",
     ["cutia rămâne în treapta a 2-a", "mod de avarie", "schimbări dure după repornire"],
     "Mercedes 7G-Tronic (722.9)", r"placă electronică"),
    ("P2767", "Mercedes 722.9: senzorul de turație internă N2, lipsă semnal",
     "Lipsește semnalul senzorului intern de turație (Y3/8n2) de pe placa conductoare a cutiei 7G-Tronic. E unul dintre cele mai frecvente coduri la 722.9.",
     ["cutia rămâne în treapta a 2-a", "mod de avarie", "mesaj de defect al cutiei pe bord"],
     "Mercedes 7G-Tronic (722.9)", r"placă electronică"),
    ("P17F0", "CVT Nissan / Jatco: patinarea curelei sau defect al cutiei CVT",
     "Cod Nissan pentru cutiile CVT Jatco: curea care patinează, bloc de valve sau calculator defect. La versiunile 4x4 poate indica și cuplajul electronic.",
     ["tremurături la accelerare", "pierdere de putere", "mod de avarie"],
     "Jatco CVT (Nissan, Renault, Dacia, Mitsubishi)", r"CVT|JF01|RE0F"),
    ("P17F1", "CVT Nissan / Jatco: cutia nu respectă parametrii de funcționare",
     "Cutia CVT nu funcționează în parametrii de fabrică, de obicei din cauza blocului de valve. Dacă evoluează în P17F0, cureaua patinează deja serios.",
     ["tremurături la accelerare", "zgomot de urlet", "consum crescut"],
     "Jatco CVT (Nissan, Renault, Dacia, Mitsubishi)", r"CVT|JF01|RE0F"),
]
CODE_MAP = {c[0]: c for c in CODES}

CONV = {"zf", "mercedes", "aisin", "other"}
ALL = {"dsg", "pdk", "zf", "mercedes", "aisin", "cvt", "dct", "other"}
FAMS = {
    "P0700": ALL, "P0780": ALL, "P0868": ALL, "P0894": ALL, "U0101": ALL,
    "P0705": CONV, "P0710": CONV, "P0715": CONV, "P0717": CONV, "P0720": CONV,
    "P0730": CONV, "P0731": CONV, "P0732": CONV, "P0733": CONV, "P0734": CONV, "P0735": CONV,
    "P0740": CONV, "P0741": CONV, "P0743": CONV, "P0750": CONV, "P0755": CONV,
    "P0745": {"other", "aisin", "zf"}, "P0746": {"other", "aisin", "zf"},
    "P0776": {"aisin", "other", "zf"}, "P0796": {"aisin", "other", "zf"},
    "P0218": CONV | {"cvt"}, "P0841": {"dsg", "pdk"}, "P0846": {"dsg", "pdk"},
    "P0810": {"dsg", "dct"}, "P0811": {"dsg", "dct"}, "P0900": {"dct"}, "P07A3": {"dct"},
    "P17BF": {"dsg"}, "P189C": {"dsg"}, "P179E": {"dsg", "pdk"}, "P179F": {"dsg", "pdk"},
    "P1731": {"pdk"}, "P1732": {"pdk"}, "P0718": {"mercedes"}, "P2767": {"mercedes"},
    "P17F0": {"cvt"}, "P17F1": {"cvt"},
}

SYMPTOMS = [
    (r"volantă", ["vibrații la ralanti", "zgomot metalic la pornire și oprire", "bătăi la plecarea de pe loc"]),
    (r"cutie de transfer|ATC|DCS|95B|Actuator", ["eroare de tracțiune integrală (4x4 / xDrive / 4Matic) pe bord", "zgomote sau blocare în virajele strânse", "vibrații la accelerare"]),
    (r"convertizor", ["tremurături fine între 60 și 100 km/h", "turația crește fără ca mașina să accelereze", "cutia se încălzește", "bâzâit din zona cutiei"]),
    (r"Multitronic|CVT", ["zgomot de urlet care crește cu viteza", "smucituri la plecarea de pe loc", "patinare la accelerare", "mașina intră în protecție"]),
    (r"(ambreiaj|ambreiaje).*(DQ200|DSG 7|DCT250|DC4|DW5|7DCT300|D7UF1|6DCT250|EDC)|(DQ200|D7UF1).*(ambreiaj)", ["vibrații la plecarea de pe loc", "smucituri la manevre și în trafic", "patinare și miros de ambreiaj", "litera treptei clipește pe bord"]),
    (r"kit ambreiaje|ambreiaje PDK|ambreiaje S tronic|Set recondiționare ambreiaje", ["șocuri la schimbarea treptelor", "patinare la accelerare", "lipsesc treptele pare sau impare", "mod de avarie"]),
    (r"placă electronică", ["cutia rămâne în treapta a 2-a", "mod de avarie", "erori de senzori de turație"]),
    (r"electrovalve|bloc de valve(?! DSG)|Set garnituri mecatronic|Recondiționare mecatronic", ["schimbări dure sau întârziate", "șocuri la decelerare", "mod de avarie", "pierderi de ulei la conector (ZF)"]),
    (r"mecatronic|calculator TCU|senzori|pompă auxiliară|G676|P1731|bloc de valve DSG", ["litera treptei clipește pe bord", "mașina nu pleacă în D sau în R", "lipsesc anumite trepte", "șocuri la schimbare, mai ales din 1 în 2", "mod de avarie"]),
    (r"Înlocuire ambreiaje cutie", ["patinare la schimbarea treptelor", "schimbări întârziate sau dure", "întârziere la cuplarea în D sau R", "mod de avarie"]),
    (r"mecanică", ["zgomot de rulmenți care crește cu viteza", "vibrații", "pierderi de ulei"]),
    (r".*", ["smucituri sau șocuri la schimbare", "patinare", "mod de avarie", "zgomote sau vibrații"]),
]


def enrich(catalog):
    """Attach symptoms, fault codes and a unique row id to every catalogue item."""
    import unicodedata
    seen = {}
    for c in catalog:
        base = "".join(ch for ch in unicodedata.normalize("NFD", c["name"].lower()) if unicodedata.category(ch) != "Mn")
        rid = "l-" + re.sub(r"[^a-z0-9]+", "-", base).strip("-")[:80]
        n = seen.get(rid, 0); seen[rid] = n + 1
        c["rid"] = rid if n == 0 else f"{rid}-{n+1}"
        if c["kind"] != "reparatie":
            c["codes"], c["symptoms"] = [], []
            continue
        c["symptoms"] = next(s for rx, s in SYMPTOMS if re.search(rx, c["name"], re.I))
        c["codes"] = codes_for(c)
    return catalog


def codes_for(c):
    if c["fam"] == "transfer" or re.search(r"volantă", c["name"]):
        return []
    codes = [k for k, *_r in CODES if c["fam"] in FAMS[k] and re.search(CODE_MAP[k][5], c["name"], re.I)]
    spec = [k for k in codes if not re.match(r"(P0[0-9]{3}|U0[0-9]{3})$", k)]
    gen = [k for k in codes if k not in spec]
    ratio = [k for k in gen if re.match(r"P073[1-5]$", k)]
    gen = [k for k in gen if k not in ratio] + ratio[:2]
    return (spec + gen)[:6]


def fixes_for(code, catalog, limit=6):
    items = [c for c in catalog if c["kind"] == "reparatie" and code in c.get("codes", [])]
    if not items:
        items = [c for c in catalog if c["kind"] == "reparatie" and c["fam"] in FAMS[code] and re.search(CODE_MAP[code][5], c["name"], re.I)]
    # one per distinct name family, cheapest first
    out, names = [], set()
    for c in sorted(items, key=lambda c: c["price"]):
        key = re.sub(r"\b(VW|Audi|Skoda|Seat|Volvo|Ford|Renault|Peugeot|Citroen|Opel|Kia|Hyundai)\b", "", c["name"]).strip()
        if key in names:
            continue
        names.add(key); out.append(c)
        if len(out) >= limit:
            break
    return out
