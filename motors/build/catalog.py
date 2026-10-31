# -*- coding: utf-8 -*-
"""Full price catalogue: reviziecutie.ro packages (29.10.2026) -> AutoMatrix prices.
Revisions +35 %, repairs +20 %, rounded to the nearest price ending in 99.
Each package gets its own list of operations and parts (written for AutoMatrix, Motul oil only)."""
import json, re, pathlib

RAW = json.load(open(pathlib.Path(__file__).with_name("rv_prices.json")))


def r99(x):
    lo = int(x) // 100 * 100 - 1
    return min((lo, lo + 100, lo + 200), key=lambda v: (abs(v - x), -v))


# ------------------------------------------------------------------ name cleanup
WORDS = [
    (r"\bBmw\b", "BMW"), (r"\bVw\b", "VW"), (r"\bVOLKSWAGEN\b", "Volkswagen"), (r"\bAUDI\b", "Audi"), (r"\bSeat\b", "Seat"),
    (r"\bHibrid\b", "Hybrid"), (r"\bHIBRID\b", "Hybrid"), (r"\bHYBRID\b", "Hybrid"), (r"\b4 motion\b", "4Motion"), (r"\bEdc7\b", "EDC7"), (r"\bEdc\b", "EDC"), (r"\bDw6\b", "DW6"),
    (r"\bsezori\b", "senzori"), (r"mecatronic Înlocuire sezori presiune", "mecatronic, înlocuire senzori de presiune"), (r"mecatronic Inlocuire sezori presiune", "mecatronic, înlocuire senzori de presiune"), (r"\bPozition\b", "Position"), (r"\bDq500\b", "DQ500"), (r"\bdistance sensor\b", "senzor de distanță"),
    (r"\bInlocuire\b", "Înlocuire"), (r"\binlocuire\b", "înlocuire"), (r"\breconditionare\b", "recondiționare"), (r"\bsenzor\b", "senzor"), (r"\bReconditionare\b", "Recondiționare"), (r"\bReparatie\b", "Reparație"), (r"\breparatie\b", "reparație"),
    (r"\bcompleta\b", "completă"), (r"\bautomata\b", "automată"), (r"\bmecanica\b", "mecanică"), (r"\bauxiliara\b", "auxiliară"), (r"\bPompa\b", "pompă"),
    (r"\belectrica\b", "electronică"), (r"\bplaca\b", "placă"), (r"\bsi\b", "și"), (r"\btractiune\b", "tracțiune"), (r"\beroare\b", "eroare"),
    (r"\bconvertizor cuplu\b", "convertizor de cuplu"), (r"\bbloc valve\b", "bloc de valve"), (r"\bVolanta\b", "volantă"), (r"\bvolant\b", "volantă"),
    (r"\bAmbreiaje\b", "ambreiaje"), (r"\bCutie Transfer\b", "cutie de transfer"), (r"\bcutie transfer\b", "cutie de transfer"), (r"\bMecatronic\b", "mecatronic"),
    (r"\bSolenoizi\b", "electrovalve"), (r"\bModul\b", "modul"), (r"\bSet\b", "Set"), (r"\bPachet\b", "Pachet"), (r"\bspeed\b", "trepte"), (r"\bSpeed\b", "trepte"),
    (r"\bautomatic\b", ""), (r"\bTronic\b", "Tronic"), (r"\btronic\b", "Tronic"), (r"\b7g Tronic\b", "7G-Tronic"), (r"\b(\d)G Tronic\b", r"\1G-Tronic"),
    (r"\bS-Tronic\b", "S tronic"), (r"\bS-tronic\b", "S tronic"), (r"\bAUDI\b", "Audi"), (r"\bOEM eco\b", "Eco"), (r"\bkit ambreiaje\b", "kit ambreiaje"),
    (r"\bvariatoare\b", "variatoare"), (r"\bTransmission\b", ""), (r"\btransmission\b", ""), (r"\bMustang\b", "Ford Mustang"),
]


def clean_subject(s):
    for a, b in WORDS:
        s = re.sub(a, b, s)
    s = re.sub(r"\s+", " ", s).strip(" -,")
    return s


def rename(raw):
    s = raw.strip()
    m = re.match(r"(?i)schimb ulei (?:și|si) (filtre|baie) cutie (.*)", s)
    if m:
        what = "filtre" if m.group(1).lower() == "filtre" else "baie de ulei"
        return f"Revizie cutie {clean_subject(m.group(2))}, cu {what}", "revizie"
    m = re.match(r"(?i)schimb ulei cutie (.*)", s)
    if m:
        return f"Revizie cutie {clean_subject(m.group(1))}", "revizie"
    m = re.match(r"(?i)revizie cutie (.*)", s)
    if m:
        return f"Revizie cutie {clean_subject(m.group(1))}", "revizie"
    m = re.match(r"(?i)schimb volanta cutie (.*)", s)
    if m:
        return f"Înlocuire volantă cu masă dublă, cutie {clean_subject(m.group(1))}", "reparatie"
    m = re.match(r"(?i)pachet garnituri mecatronic (.*)", s)
    if m:
        return f"Set garnituri mecatronic ZF {clean_subject(m.group(1))}", "reparatie"
    m = re.match(r"(?i)kit solenoizi (.*)", s)
    if m:
        return f"Kit electrovalve cutie {clean_subject(m.group(1))}", "reparatie"
    return clean_subject(s[0].upper() + s[1:]), "reparatie"


# ------------------------------------------------------------------ families (for grouping on the price page)
FAMILIES = [
    ("pdk", "Porsche PDK", r"PDK|7DT"),
    ("dsg", "DSG și S tronic", r"DSG|DQ\d{3}|S tronic|0B5|0CK|0CJ|0CL|0DK|DL501|02E|0BH|0GC|0DD"),
    ("zf", "ZF (4HP, 5HP, 6HP, 8HP, 9HP)", r"\bZF\b|[4-9]HP|5HP|6HP|8HP|9HP|8 trepte Porsche|Jaguar 6HP|Land Rover 6HP|Land Rover 8HP"),
    ("mercedes", "Mercedes-Benz", r"G-Tronic|722\.|725\.|7G-DCT|8G-DCT|Mercedes|W169|W245|4MATIC|4 matic"),
    ("aisin", "Aisin", r"Aisin|TF-8|AF40|AM6|AW6|TG-81|GA6F|GA8F|U140|U660|A750|P313|09G|09D"),
    ("cvt", "CVT și Multitronic", r"CVT|Multitronic|01J|0AW|0AN|JF01|RE0F|FK0|CFT23|GACVT|F1CJA|HSD|Toyota K"),
    ("dct", "Powershift, EDC și alte DCT", r"Powershift|DCT|MPS6|EDC|DC4|DW5|DW6|D7UF1|DKG|6DCT"),
    ("transfer", "Cutii de transfer", r"transfer|\bATC\d|\bDCS\b|95B"),
    ("other", "Alte cutii automate (GM, Ford, Hyundai, Jatco, Renault, Toyota)", r".*"),
]


def family(name):
    for key, label, rx in FAMILIES:
        if re.search(rx, name, re.I):
            return key
    return "other"


# ------------------------------------------------------------------ oil type (Motul only)
def oil(name):
    n = name
    if re.search(r"CVT|Multitronic|01J|0AW|0AN|JF01|RE0F|FK0|CFT23|GACVT|F1CJA|Toyota K|HSD", n, re.I):
        return "Ulei Motul pentru cutii CVT"
    if re.search(r"DSG 7\b|DQ200|DCT250|DC4|DW5|7DCT300|D7UF1|DCT 7", n) and not re.search(r"DQ250|DQ381|DQ500|0BH|0GC", n):
        return "Ulei de transmisie Motul pentru cutii cu ambreiaj dublu uscat"
    if re.search(r"DSG|DQ\d{3}|S tronic|0B5|0CK|0CJ|0CL|0DK|DL501|PDK|7DT|MPS6|6DCT|DKG|7G-DCT|8G-DCT|DCT|Powershift|EDC|DW6", n, re.I):
        return "Ulei Motul pentru cutii cu dublu ambreiaj în baie de ulei"
    if re.search(r"transfer|\bATC\d|\bDCS\b|95B|4MATIC", n, re.I):
        return "Ulei Motul pentru cutii de transfer"
    return "Ulei Motul pentru cutii automate (ATF)"


def has_pan_filter(n):
    return bool(re.search(r"6HP|8HP|9HP|0D5|0BK|0C8|8 trepte Porsche|Hybrid 0BW|8HP55", n))


# ------------------------------------------------------------------ operations and parts
def describe(name, kind, raw):
    n = name
    o = oil(n)
    ops, parts = [], []
    if kind == "revizie":
        dry = "uscat" in o
        if dry:
            ops = ["Citirea erorilor și verificarea cutiei la drum", "Golirea uleiului de transmisie și curățarea magnetului", "Umplerea cu ulei nou la nivelul prescris", "Verificarea etanșeității și test la drum"]
            parts = [o, "Dop de golire și garnitură noi"]
        elif re.search(r"CVT|Multitronic|01J|0AW|RE0F|JF01|FK0|CFT23|GACVT|F1CJA|Toyota K|HSD", n, re.I):
            ops = ["Diagnoză și citirea parametrilor cutiei", "Golirea uleiului vechi și curățarea băii și a magneților", "Înlocuirea filtrului (sau a sitei) de ulei", "Umplere cu ulei nou și reglarea nivelului la temperatura prescrisă de producător", "Resetarea valorilor de degradare a uleiului, unde cutia o cere", "Test la drum"]
            parts = [o, "Filtru sau sită de ulei", "Garnitură baie și dopuri noi"]
        elif "dublu ambreiaj" in o:
            ops = ["Diagnoză și citirea erorilor cutiei", "Golirea uleiului vechi", "Înlocuirea filtrului de ulei" + (" și a filtrelor exterioare" if re.search(r"filtre|0CK|0B5|DL501|S tronic", n) else ""), "Umplere după procedura producătorului, cu temperatura urmărită pe testerul de diagnoză", "Adaptarea ambreiajelor (adaptări de bază)", "Test la drum"]
            parts = [o, "Filtru de ulei" + (" și filtre suplimentare" if re.search(r"filtre|0CK|S tronic", n) else ""), "Garnituri și dopuri noi"]
        else:
            pan = has_pan_filter(n) or "baie" in n
            ops = ["Diagnoză și citirea erorilor cutiei", "Golirea uleiului vechi" + (" și demontarea băii de ulei" if pan else " și curățarea băii și a magneților"),
                   ("Montarea băii noi cu filtru integrat" if pan else "Înlocuirea filtrului (sau a sitei) de ulei"),
                   "Umplere cu ulei nou, în cantitatea indicată de producătorul cutiei", "Reglarea nivelului la temperatura de lucru", "Resetarea adaptărilor și test la drum"]
            parts = [o, ("Baie de ulei cu filtru integrat" if pan else "Filtru sau sită de ulei"), "Garnituri, șuruburi și dopuri noi"]
        if re.search(r"\bOEM\b", n):
            parts = [p.replace("Filtru", "Filtru original (OEM)").replace("Baie de ulei", "Baie de ulei originală (OEM)") for p in parts]
            if not any("OEM" in p for p in parts):
                parts.append("Filtru și garnituri originale (OEM)")
        if re.search(r"Hybrid", n):
            ops.insert(1, "Verificarea sistemului hibrid înainte de intervenție")
        ops.insert(0, "Procedură completă după manualul de reparație emis de producătorul cutiei")
        if re.search(r"PDK|7DT75", n):
            parts.append("Ulei Motul pentru partea mecanică a cutiei PDK")
        return ops, parts

    # ------------- repairs
    def std_end(oil_name=o, filt=True):
        e = ["Completare sau schimb ulei", "Adaptări de bază pe calculator", "Test la drum și verificarea etanșeității"]
        p = [oil_name] + (["Filtru de ulei"] if filt and "uscat" not in oil_name else [])
        return e, p

    if re.search(r"volantă", n, re.I):
        ops = ["Demontarea cutiei de viteze", "Înlocuirea volantei cu masă dublă", "Verificarea ambreiajului, a rulmentului și a simeringului arborelui cotit", "Montarea cutiei cu șuruburi noi", "Adaptări de bază și test la drum"]
        parts = ["Volantă cu masă dublă nouă", "Șuruburi de prindere noi"]
    elif re.search(r"Set garnituri mecatronic", n):
        ops = ["Golirea uleiului și demontarea băii", "Demontarea mecatronicului", "Înlocuirea garniturilor mecatronicului și a bucșei adaptoare a conectorului", "Montarea mecatronicului și a băii cu filtru", "Umplere cu ulei nou, nivel reglat la temperatură, test la drum"]
        parts = ["Set garnituri mecatronic", "Bucșă adaptoare conector", o]
    elif re.search(r"electrovalve", n, re.I):
        ops = ["Diagnoză și testarea electrovalvelor", "Demontarea blocului hidraulic", "Înlocuirea electrovalvelor uzate", "Curățarea blocului de valve", "Montare, schimb de ulei și resetarea adaptărilor", "Test la drum"]
        parts = ["Kit electrovalve", "Garnituri bloc hidraulic", o, "Filtru de ulei"]
    elif re.search(r"convertizor", n, re.I):
        ops = ["Demontarea cutiei și a convertizorului", "Deschiderea convertizorului prin strunjire", "Înlocuirea lamelelor ambreiajului de blocare, a garniturilor și a rulmenților axiali", "Sudarea, echilibrarea dinamică și testul de etanșeitate", "Montarea convertizorului cu simering de pompă nou", "Schimb de ulei, adaptări și test la drum"]
        parts = ["Kit recondiționare convertizor (lamele, garnituri, rulmenți)", "Simering pompă", o, "Filtru sau baie cu filtru"]
    elif re.search(r"Recondiționare mecatronic", n):
        ops = ["Demontarea mecatronicului", "Testarea pe stand a electrovalvelor și a senzorilor", "Curățarea blocului hidraulic", "Înlocuirea electrovalvelor uzate, a garniturilor și a bucșei conectorului", "Montare, schimb de ulei conform manualului de reparație al producătorului și resetarea adaptărilor", "Test la drum"]
        parts = ["Kit garnituri mecatronic", "Electrovalve, după testare", "Bucșă adaptoare conector", o, "Baie de ulei cu filtru"]
    elif re.search(r"Set reparație mecatronic|Pachet reparație mecatronic", n):
        ops = ["Diagnoză și verificarea presiunilor", "Demontarea mecatronicului", "Înlocuirea componentelor uzate din setul de reparație", "Curățare, etanșare și test de presiune", "Montare, completare ulei", "Adaptări de bază și test la drum"]
        parts = ["Set reparație mecatronic (acumulator, bloc de valve sau etanșări, după cutie)", "Garnituri noi", o]
    elif re.search(r"senzori presiune", n):
        ops = ["Diagnoză și citirea valorilor de presiune", "Demontarea mecatronicului", "Înlocuirea senzorilor de presiune", "Montare și completare ulei", "Adaptări de bază și test la drum"]
        parts = ["Senzori de presiune noi", "Garnituri mecatronic", o]
    elif re.search(r"mecatronic", n, re.I) and re.search(r"Înlocuire|înlocuire", n):
        ops = ["Diagnoză completă a cutiei", "Demontarea mecatronicului defect", "Montarea mecatronicului nou", "Codare și actualizare software, unde e necesar", "Completare ulei, adaptări de bază", "Test la drum"]
        parts = ["Mecatronic nou", "Garnituri și șuruburi noi", o]
    elif re.search(r"calculator TCU", n):
        ops = ["Diagnoză și confirmarea defectului de calculator", "Demontarea mecatronicului", "Înlocuirea calculatorului cutiei (TCU)", "Codare, actualizare software și adaptări de bază", "Test la drum"]
        parts = ["Calculator cutie (TCU) nou", "Garnituri noi", o]
    elif re.search(r"bloc de valve", n):
        ops = ["Diagnoză și verificarea presiunilor", "Demontarea blocului hidraulic", "Montarea blocului de valve nou", "Schimb de ulei conform manualului de reparație al producătorului", "Adaptări de bază și test la drum"]
        parts = ["Bloc de valve nou", "Garnituri noi", o, "Filtru de ulei"]
    elif re.search(r"pompă auxiliară", n):
        ops = ["Diagnoză și verificarea presiunii de ulei", "Demontarea pompei auxiliare", "Montarea setului de reparație", "Completare ulei, adaptări", "Test la drum"]
        parts = ["Set reparație pompă auxiliară", "Garnituri noi", o]
    elif re.search(r"placă electronică", n):
        ops = ["Diagnoză și confirmarea erorilor de senzori de turație", "Golirea uleiului și demontarea băii", "Înlocuirea plăcii electronice cu senzori", "Montare, schimb de ulei și filtru", "Resetarea adaptărilor și test la drum"]
        parts = ["Placă electronică cu senzori de turație", "Filtru de ulei", "Garnituri și conector nou", o]
    elif re.search(r"Actuator", n):
        ops = ["Diagnoză cutie de transfer", "Demontarea actuatorului (servomotorului)", "Montarea actuatorului nou", "Calibrare pe calculator", "Test la drum"]
        parts = ["Actuator cutie de transfer nou", "Șuruburi și garnitură"]
    elif re.search(r"cutie de transfer|95B", n, re.I):
        ops = ["Diagnoză sistem de tracțiune integrală", "Demontarea cutiei de transfer", "Înlocuirea pachetului de ambreiaje (lamele) și a etanșărilor", "Verificarea lanțului, a rulmenților și a actuatorului", "Montare, ulei nou și calibrare", "Test la drum"]
        parts = ["Pachet ambreiaje cutie de transfer", "Simeringuri și garnituri", "Ulei Motul pentru cutii de transfer"]
    elif re.search(r"Reparație cutie de transfer", n):
        ops = ["Diagnoză", "Demontarea cutiei de transfer", "Înlocuirea rulmenților, a etanșărilor și a pieselor uzate", "Montare, ulei nou și test"]
        parts = ["Kit rulmenți și etanșări", "Ulei Motul pentru cutii de transfer"]
    elif re.search(r"kit ambreiaje|ambreiaje DSG|ambreiaj DSG|ambreiaj DCT|ambreiaje PDK|Set recondiționare ambreiaje S tronic|ambreiaje cutie EDC|ambreiaje cutie Powershift|ambreiaje Multitronic", n, re.I):
        dry = "uscat" in o
        ops = ["Diagnoză și verificarea uzurii ambreiajelor", "Demontarea cutiei de viteze", "Înlocuirea ambreiajului dublu" + (" și a rulmenților de presiune" if dry else " (pachet umed) și a garniturilor"), "Reglarea cotelor cu scule dedicate", "Montarea cutiei", "Adaptări de bază și test la drum"]
        parts = ["Kit ambreiaj dublu " + ("uscat" if dry else "umed") + " complet", ("Rulmenți de presiune și siguranțe" if dry else "Garnituri și simeringuri"), o] + ([] if dry else ["Filtru de ulei"])
    elif re.search(r"Înlocuire ambreiaje cutie", n):
        ops = ["Demontarea cutiei de pe mașină", "Dezasamblarea completă și curățarea pieselor", "Înlocuirea pachetelor de ambreiaje (discuri de fricțiune și discuri de oțel)", "Înlocuirea garniturilor de piston și a simeringurilor", "Verificarea pompei, a bucșelor și a blocului de valve", "Reasamblare la cote, montare, schimb de ulei conform manualului de reparație al producătorului", "Adaptări și test la drum"]
        parts = ["Kit lamele ambreiaje", "Kit garnituri și simeringuri", "Baie sau filtru de ulei", o]
    elif re.search(r"mecanică", n):
        ops = ["Demontarea cutiei", "Dezasamblarea părții mecanice", "Înlocuirea rulmenților și a simeringurilor uzate", "Verificarea pinioanelor și a sincronizărilor", "Reasamblare, montare, ulei nou", "Adaptări și test la drum"]
        parts = ["Kit rulmenți cutie", "Simeringuri și garnituri", o]
    elif re.search(r"P179E|G676", n):
        ops = ["Diagnoză și confirmarea erorii senzorului de poziție", "Demontarea mecatronicului", "Înlocuirea senzorului de poziție G676 și a componentelor afectate", "Montare, schimb de ulei", "Adaptări de bază și test la drum"]
        parts = ["Senzor de poziție G676", "Garnituri mecatronic", o, "Filtru de ulei"]
    elif re.search(r"senzor de distanță|P1731", n):
        ops = ["Diagnoză și confirmarea erorilor P1731 / P1732", "Demontarea cutiei PDK", "Înlocuirea senzorului de distanță și a pieselor afectate", "Reasamblare, ulei nou, adaptări", "Test la drum"]
        parts = ["Senzor de distanță", "Garnituri și simeringuri", o]
    elif re.search(r"modul Multitronic", n):
        ops = ["Diagnoză Multitronic", "Demontarea modulului de comandă", "Reparația modulului cu setul dedicat", "Montare, ulei nou, adaptări", "Test la drum"]
        parts = ["Set reparație modul Multitronic", "Garnituri noi", o]
    elif re.search(r"variatoare", n):
        ops = ["Demontarea cutiei Multitronic", "Dezasamblare completă", "Recondiționarea variatoarelor (fuliilor) și verificarea lanțului", "Înlocuirea pachetelor de ambreiaje înainte / înapoi", "Reasamblare, montare, ulei nou", "Adaptări și test la drum"]
        parts = ["Kit recondiționare variatoare", "Kit ambreiaje înainte / înapoi", "Garnituri și simeringuri", o]
    else:  # complete gearbox repairs / packages
        ops = ["Diagnoză completă și test la drum", "Demontarea cutiei de pe mașină", "Dezasamblare, curățare și măsurarea tuturor componentelor", "Înlocuirea pieselor uzate: ambreiaje, rulmenți, garnituri, simeringuri" + (", mecatronic" if re.search(r"mecatronic", n) else ""), "Reasamblare la cotele producătorului", "Montare, ulei nou, adaptări de bază", "Test la drum în toate treptele"]
        parts = ["Kit reparație cutie (ambreiaje, rulmenți, garnituri, simeringuri)", o] + ([] if "uscat" in o else ["Filtru de ulei"])
        if re.search(r"mecatronic", n):
            parts.insert(0, "Mecatronic nou")
        if re.search(r"volantă", n):
            parts.insert(0, "Volantă cu masă dublă nouă")
    return ops, parts


# ------------------------------------------------------------------ build catalogue
CATALOG = []
_seen = set()
for raw, rv in RAW:
    if (raw, rv) in _seen:
        continue
    _seen.add((raw, rv))
    name, kind = rename(raw)
    price = r99(rv * (1.35 if kind == "revizie" else 1.20))
    ops, parts = describe(name, kind, raw)
    CATALOG.append(dict(name=name, kind=kind, price=price, fam=family(name), ops=ops, parts=parts))

FAM_LABEL = {k: l for k, l, _ in FAMILIES}
FAM_ORDER = [k for k, _, _ in FAMILIES]


def pick(rx, kind=None):
    return [c for c in CATALOG if re.search(rx, c["name"], re.I) and (kind is None or c["kind"] == kind)]


def min_price(rx=".*", kind=None):
    p = [c["price"] for c in pick(rx, kind)]
    return min(p) if p else None


if __name__ == "__main__":
    print(len(CATALOG), "packages")
    from collections import Counter
    print(Counter(c["fam"] for c in CATALOG))
    print(Counter(c["kind"] for c in CATALOG))
    print("min rev", min_price(kind="revizie"), "max rev", max(c["price"] for c in CATALOG if c["kind"] == "revizie"))
    print("min rep", min_price(kind="reparatie"), "max rep", max(c["price"] for c in CATALOG if c["kind"] == "reparatie"))
    for c in CATALOG[::9]:
        print(c["price"], c["kind"][:3], c["fam"], "|", c["name"])
