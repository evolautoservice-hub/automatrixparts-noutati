# -*- coding: utf-8 -*-
"""Pagini noi de servicii: Powershift, EDC, Aisin și pe mărci (BMW, Audi, VW / Skoda / Seat)."""
import re
from catalog import CATALOG

G = ("24 luni, fără limită de km", "red")


def rows(rx=None, fam=None):
    return [c for c in CATALOG if (fam is None or c["fam"] == fam) and (rx is None or re.search(rx, c["name"]))]


def mn(lst, kind=None):
    p = [c["price"] for c in lst if kind is None or c["kind"] == kind]
    return min(p) if p else 0


def extra_pages(fmt):
    P = []
    # ---------------------------------------------------------------- POWERSHIFT
    ps = rows(r"Powershift|MPS6|DPS6|6DCT250|6DCT45|6DCT47")
    ps_rev, ps_rep = mn(ps, "revizie"), mn(ps, "reparatie")
    P.append(dict(
        slug="reparatie-cutie-powershift", nav="Reparație cutie Powershift", navsub="Ford, Volvo, DPS6 și MPS6",
        title="Reparație cutie Powershift Ford și Volvo | Garanție 24 luni",
        desc=f"Reparații și revizii cutii Powershift DPS6 și MPS6 pentru Ford Focus, Fiesta, Mondeo, Kuga, C-Max și Volvo. Revizie de la {fmt(ps_rev)} lei, garanție 24 luni fără limită de km.",
        h1="Reparație cutie Powershift (Ford și Volvo)",
        eyebrow="Cutii cu dublu ambreiaj Getrag",
        lead="Powershift este numele dat de Ford cutiilor cu dublu ambreiaj Getrag. Varianta uscată DPS6 de pe Focus și Fiesta e una dintre cutiile cu cele mai multe probleme cunoscute, iar varianta în baie de ulei MPS6 de pe Mondeo, Kuga și Volvo e mai robustă, dar cere revizii la timp. Le reparăm pe amândouă, cu prețuri afișate.",
        spec=[("Revizie Powershift", f"de la {fmt(ps_rev)} lei", "big"), ("Reparații", f"de la {fmt(ps_rep)} lei", ""), ("Garanție reparații",) + G, ("Tipuri", "DPS6, MPS6, 6DCT470", "")],
        service_type="Reparație cutie Powershift", min_price=ps_rev,
        body="""
<h2>Ce cutie Powershift ai</h2>
<ul class="dots">
<li><b>DPS6 (6DCT250)</b>, cu dublu ambreiaj uscat: Ford Focus 3, Fiesta, B-Max, EcoSport și C-Max cu motoare pe benzină de 1.6 și 2.0</li>
<li><b>MPS6 (6DCT450 / 6DCT451)</b>, cu ambreiaj în baie de ulei: Ford Mondeo, Kuga, S-Max, Galaxy, C-Max diesel și Volvo V40, V60, S60, V70, XC60 cu motoare D3, D4 și D5</li>
<li><b>6DCT470</b>, varianta pentru Mitsubishi Outlander și Lancer, Peugeot 4007 și Citroën C-Crosser</li>
</ul>
<p>Codul exact al cutiei îl găsim din seria de șasiu. Trimite-ne-o pe WhatsApp și îți spunem ce cutie ai și ce prețuri ți se aplică.</p>

<h2>Probleme tipice la Powershift</h2>
<ul class="dots">
<li><b>Tremură la plecarea de pe loc</b>, mai ales la DPS6: ambreiajul uscat e contaminat cu ulei sau uzat</li>
<li><b>Smucituri în trafic și la manevre</b>, schimbări dure din 1 în 2 și din 2 în 1</li>
<li><b>Mesajul „Transmission malfunction”</b> sau mașina care nu mai pleacă: calculatorul cutiei (TCM) sau actuatoarele ambreiajului</li>
<li><b>Pierderi de ulei</b> pe simeringurile arborilor de intrare, care ajung pe ambreiaj</li>
<li><b>La MPS6:</b> schimbări întârziate și patinare când uleiul și filtrul nu au fost schimbate la timp</li>
</ul>
<p>Codurile de eroare frecvente sunt <a class="link" href="/coduri-eroare-cutie-automata#p0900">P0900</a>, <a class="link" href="/coduri-eroare-cutie-automata#p07a3">P07A3</a>, <a class="link" href="/coduri-eroare-cutie-automata#p0810">P0810</a> și <a class="link" href="/coduri-eroare-cutie-automata#p0811">P0811</a>.</p>

<h2>Cum reparăm o cutie Powershift</h2>
<p>Facem diagnoza cu aparat dedicat Ford și Volvo și citim adaptările ambreiajului. Demontăm cutia, schimbăm ambreiajul dublu, rulmentul de presiune, simeringurile și, unde e cazul, actuatoarele sau calculatorul. La final facem adaptările cu aparatul și testul la drum. La MPS6 schimbăm uleiul Motul pentru cutii cu dublu ambreiaj în baie de ulei și filtrul, după manualul producătorului.</p>
<div class="callout"><p><b>Garanție 24 de luni, fără limită de kilometri,</b> la orice reparație de cutie Powershift. Prețul exact îl primești în scris după diagnoză, înainte de lucrare.</p></div>
<h2>Prețuri Powershift</h2>
""",
        prices=ps,
        faq=[
            ("De ce tremură Ford Focus cu Powershift la plecare?", "La cutia DPS6, cu ambreiaj uscat, tremurul la plecare vine aproape întotdeauna de la ambreiajul contaminat cu ulei sau uzat. Se rezolvă cu înlocuirea ambreiajului dublu și a simeringurilor, urmată de adaptări."),
            ("Cât costă reparația cutiei Powershift?", f"Revizia unei cutii MPS6 pornește de la {fmt(ps_rev)} lei. Reparațiile pornesc de la {fmt(ps_rep)} lei, iar o reparație completă de MPS6 / 6DCT451 ajunge la 15.599–17.399 lei. Prețul exact îl primești în scris după diagnoză."),
            ("Cutia Powershift de pe Volvo e aceeași ca la Ford?", "Da. Volvo-urile diesel cu cutie automată cu dublu ambreiaj folosesc cutia Getrag MPS6 (6DCT450 / 6DCT451), aceeași familie ca pe Mondeo și Kuga."),
            ("Se poate tracta o mașină cu Powershift?", "Doar pe platformă. Tractarea cu roțile motoare pe asfalt poate distruge cutia."),
        ],
        related=["reparatie-cutie-edc", "reparatii-cutii-automate", "coduri-eroare-cutie-automata"],
    ))
    # ---------------------------------------------------------------- EDC
    edc = rows(r"EDC|DC4|DW5|DW6")
    P.append(dict(
        slug="reparatie-cutie-edc", nav="Reparație cutie EDC", navsub="Renault și Dacia, DC4, DW5, DW6",
        title="Reparație cutie EDC Renault și Dacia | Garanție 24 luni",
        desc=f"Reparații și revizii cutii automate EDC pentru Renault Megane, Clio, Captur, Kadjar, Scenic, Talisman și Dacia: DC4, DW5 (EDC7), DW6. Revizie de la {fmt(mn(edc, 'revizie'))} lei.",
        h1="Reparație cutie EDC (Renault și Dacia)",
        eyebrow="Cutii cu dublu ambreiaj Renault",
        lead="EDC (Efficient Dual Clutch) este cutia automată cu dublu ambreiaj a Renault. Varianta cu 6 trepte DC4 e aceeași cutie Getrag ca DPS6 de la Ford, iar EDC7 (DW5) are 7 trepte. Reparăm ambreiajele, actuatoarele și calculatorul, cu prețuri afișate.",
        spec=[("Revizie EDC", f"de la {fmt(mn(edc, 'revizie'))} lei", "big"), ("Ambreiaje EDC", f"de la {fmt(mn(edc, 'reparatie'))} lei", ""), ("Garanție reparații",) + G, ("Tipuri", "DC4, DW5, DW6", "")],
        service_type="Reparație cutie EDC", min_price=mn(edc),
        body="""
<h2>Pe ce mașini e cutia EDC</h2>
<ul class="dots">
<li><b>EDC6 DC4 (6DCT250)</b>, ambreiaj uscat: Renault Megane 3 și 4, Clio 4 și 5, Captur, Kadjar, Scenic, Fluence și Dacia Duster cu cutie EDC</li>
<li><b>EDC7 DW5 (7DCT300)</b>, ambreiaj uscat cu 7 trepte: Renault Megane 4, Kadjar, Scenic 4, Talisman și Captur 2 cu motoare TCe</li>
<li><b>DW6 (6DCT451)</b>, ambreiaj în baie de ulei: motoarele diesel mai puternice, inclusiv Espace și Talisman</li>
</ul>

<h2>Simptome frecvente la EDC</h2>
<ul class="dots">
<li>Tremură sau vibrează la plecarea de pe loc, mai ales în pantă</li>
<li>Smucituri în trafic, la mers încet</li>
<li>Mesajul „Verificați cutia de viteze” sau mașina rămâne în neutru</li>
<li>Miros de ambreiaj după manevre și în coloane</li>
</ul>
<p>La cutiile cu ambreiaj uscat, uzura ambreiajului vine mai repede la mersul mult în oraș. Codurile frecvente sunt <a class="link" href="/coduri-eroare-cutie-automata#p0810">P0810</a>, <a class="link" href="/coduri-eroare-cutie-automata#p0811">P0811</a> și <a class="link" href="/coduri-eroare-cutie-automata#p07a3">P07A3</a>.</p>

<h2>Cum lucrăm</h2>
<p>Diagnoza o facem cu aparat Renault și citim uzura și adaptările ambreiajelor. La înlocuirea ambreiajelor schimbăm și rulmenții de presiune, verificăm actuatoarele și simeringurile, apoi facem învățarea punctului de cuplare și testul la drum.</p>
<div class="callout"><p><b>Garanție 24 de luni, fără limită de kilometri,</b> pentru piese și manoperă. Trimite-ne pe WhatsApp seria de șasiu și un video cu simptomul pentru o primă estimare.</p></div>
<h2>Prețuri EDC</h2>
""",
        prices=edc,
        faq=[
            ("Cutia EDC e aceeași cu Powershift?", "Varianta EDC6 DC4 de la Renault și DPS6 de la Ford sunt aceeași cutie Getrag 6DCT250, cu dublu ambreiaj uscat. Au simptome și reparații asemănătoare."),
            ("De ce vibrează Renault cu cutie EDC la plecare?", "Cel mai des, ambreiajul dublu e uzat sau contaminat cu ulei. Uneori ajută adaptările, dar dacă ambreiajul e uzat se înlocuiește."),
            ("Cât costă schimbarea ambreiajelor la EDC?", f"Înlocuirea ambreiajelor la EDC pornește de la {fmt(mn(edc, 'reparatie'))} lei, cu manoperă și TVA. Prețul exact îl primești în scris după diagnoză."),
        ],
        related=["reparatie-cutie-powershift", "reparatii-cutii-automate", "coduri-eroare-cutie-automata"],
    ))
    # ---------------------------------------------------------------- AISIN
    ai = rows(fam="aisin")
    P.append(dict(
        slug="reparatie-cutie-aisin", nav="Reparație cutie Aisin", navsub="09G, TF-80SC, AF40, AM6, 8 trepte",
        title="Reparație cutie automată Aisin | VW, Volvo, Opel, Toyota",
        desc=f"Reparații și revizii cutii automate Aisin: TF-60SN (09G), TF-80SC, AF40-6, AM6, AW6, 8 trepte. VW, Skoda, Volvo, Opel, Ford, Peugeot, Toyota, Mini. Revizie de la {fmt(mn(ai, 'revizie'))} lei.",
        h1="Reparație cutie automată Aisin",
        eyebrow="Cutii automate clasice cu convertizor",
        lead="Aisin face cutiile automate cu convertizor de pe foarte multe mașini europene și japoneze: VW, Skoda, Seat, Volvo, Opel, Ford, Peugeot, Citroën, Toyota, Mini și altele. Sunt cutii bune, dar sensibile la uleiul vechi, care uzează blocul de valve.",
        spec=[("Revizie Aisin", f"de la {fmt(mn(ai, 'revizie'))} lei", "big"), ("Reparații", f"de la {fmt(mn(ai, 'reparatie'))} lei", ""), ("Garanție reparații",) + G, ("Tipuri", "6 și 8 trepte", "")],
        service_type="Reparație cutie automată Aisin", min_price=mn(ai),
        body="""
<h2>Cutiile Aisin pe care le reparăm</h2>
<ul class="dots">
<li><b>TF-60SN (09G / 09K / 09M)</b>, 6 trepte: VW Golf, Passat, Touran, Tiguan, Skoda Octavia, Superb, Seat Leon, Audi A3, Mini</li>
<li><b>TF-80SC, AF40-6, AM6 / AW6</b>, 6 trepte: Volvo, Opel Insignia, Ford Mondeo, Peugeot, Citroën, Land Rover Freelander, Saab</li>
<li><b>Aisin 6 trepte Tiptronic (09D)</b>: VW Touareg, Audi Q7, Porsche Cayenne</li>
<li><b>Aisin 8 trepte</b>: Toyota, Volvo, VW Touareg, Porsche Cayenne, BMW și Mini cu GA8F22AW</li>
</ul>

<h2>Simptome tipice</h2>
<ul class="dots">
<li>Șoc la trecerea din 2 în 3 sau din 3 în 2, mai ales cu cutia caldă</li>
<li>Turația crește puțin la schimbare (patinare), apoi treapta „prinde”</li>
<li>Tremurături între 60 și 100 km/h, de la ambreiajul convertizorului</li>
<li>Coduri <a class="link" href="/coduri-eroare-cutie-automata#p0776">P0776</a>, <a class="link" href="/coduri-eroare-cutie-automata#p0796">P0796</a> sau <a class="link" href="/coduri-eroare-cutie-automata#p0741">P0741</a></li>
</ul>

<h2>Cum reparăm</h2>
<p>La cutiile Aisin, cel mai des se uzează alezajele din blocul de valve și electrovalvele de presiune. În funcție de diagnoză, înlocuim blocul de valve, recondiționăm convertizorul sau desfacem complet cutia. La final schimbăm uleiul Motul cu specificația Aisin, după manualul producătorului, și facem adaptările cu aparatul.</p>
<div class="callout"><p>Dacă ai deja codul <b>P0776</b> sau șocuri din 2 în 3, nu amâna: uleiul degradat accelerează uzura blocului de valve. <b>Garanție 24 de luni, fără limită de kilometri.</b></p></div>
<h2>Prețuri cutii Aisin</h2>
""",
        prices=ai,
        faq=[
            ("Ce cutie Aisin am pe VW Passat sau Skoda Octavia?", "Modelele cu motor transversal și cutie automată clasică (nu DSG) au de obicei cutia Aisin TF-60SN, cu codul VW 09G. Îți confirmăm după seria de șasiu."),
            ("De ce dă șoc cutia Aisin din 2 în 3?", "Cel mai des, blocul de valve e uzat sau electrovalva de presiune nu mai reglează corect. Uleiul vechi grăbește problema. Diagnoza arată dacă ajunge o revizie sau trebuie bloc de valve."),
            ("Cât costă revizia unei cutii Aisin?", f"Revizia pornește de la {fmt(mn(ai, 'revizie'))} lei, cu ulei Motul, filtru, garnituri și manoperă."),
        ],
        related=["revizie-cutie-automata", "reconditionare-convertizor-cuplu", "reparatii-cutii-automate"],
    ))
    # ---------------------------------------------------------------- BRANDS
    def brand(slug, name, rx, navsub, models, boxes, faq_box, related):
        lst = rows(rx)
        rev, rep = mn(lst, "revizie"), mn(lst, "reparatie")
        return dict(
            slug=slug, nav=f"Cutie automată {name}", navsub=navsub, brand=True,
            title=f"Reparație cutie automată {name} | Prețuri și garanție 24 luni",
            desc=f"Reparații și revizii cutii automate {name}: {navsub}. Revizie de la {fmt(rev)} lei, reparații de la {fmt(rep)} lei, garanție 24 luni fără limită de km. Băicoi, Prahova.",
            h1=f"Reparație cutie automată {name}",
            eyebrow="Pe mărci",
            lead=f"Reparăm și revizuim toate cutiile automate montate pe {name}: {navsub}. Mai jos găsești ce cutie are mașina ta și toate prețurile pentru {name}, cu manoperă și TVA incluse.",
            spec=[("Revizie", f"de la {fmt(rev)} lei", "big"), ("Reparații", f"de la {fmt(rep)} lei", ""), ("Garanție reparații",) + G, ("Lucrări cu preț afișat", str(len(lst)), "")],
            service_type=f"Reparație cutie automată {name}", min_price=rev,
            body=f"""
<h2>Ce cutie automată are {name}-ul tău</h2>
<ul class="dots">{"".join(f"<li>{x}</li>" for x in boxes)}</ul>
<p>Modele pe care le vedem des la atelier: {models}. Codul exact al cutiei îl aflăm din seria de șasiu: trimite-ne-o pe WhatsApp.</p>
<h2>Cum lucrăm</h2>
<p>Facem diagnoza cu aparat dedicat mărcii, citim codurile și adaptările cutiei și îți dăm prețul în scris înainte de lucrare. Reviziile le facem după manualul de reparație emis de producătorul cutiei, cu ulei Motul cu specificația cerută. La reparații montăm piese noi și facem adaptările și testul la drum.</p>
<div class="callout"><p><b>Garanție 24 de luni, fără limită de kilometri, unică în România,</b> pentru orice reparație de cutie automată {name}.</p></div>
<h2>Prețuri cutii automate {name}</h2>
""",
            prices=lst,
            faq=[faq_box,
                 (f"Cât costă reparația cutiei automate la {name}?", f"Revizia pornește de la {fmt(rev)} lei, iar reparațiile de la {fmt(rep)} lei, în funcție de cutie și de lucrare. Toate prețurile sunt pe această pagină, cu manoperă și TVA. Prețul final îl primești în scris după diagnoză."),
                 ("Ce garanție aveți?", "24 de luni, fără limită de kilometri, pentru piese și manoperă.")],
            related=related,
        )
    P.append(brand("reparatie-cutie-automata-bmw", "BMW", r"BMW|Mini", "ZF 6HP și 8HP, GM 5L40, Aisin",
                   "Seria 1, 3, 5, 7, X1, X3, X5, X6 și Mini",
                   ["<b>ZF 8HP</b> (8 trepte): aproape toate modelele BMW din 2009 încoace</li><li><b>ZF 6HP</b> (6 trepte): Seria 3 E90, Seria 5 E60, X3 E83, X5 E70", "<b>ZF 5HP</b> și <b>GM 5L40</b>: modelele mai vechi (E46, E39, E53)", "<b>Aisin GA6F21 / GA8F22AW</b>: X1, X2, Seria 2 Active Tourer și Mini cu tracțiune față", "<b>Cutie de transfer xDrive</b> (ATC) la modelele 4x4"],
                   ("Ce cutie are BMW-ul meu?", "Majoritatea BMW-urilor din 2009 încoace au cutia ZF 8HP. Modelele mai vechi au ZF 6HP sau 5HP, iar X1, X2 și Mini cu tracțiune față au cutii Aisin. Îți confirmăm după seria de șasiu."),
                   ["reparatie-cutie-zf", "reconditionare-convertizor-cuplu", "revizie-cutie-automata"]))
    P.append(brand("reparatie-cutie-automata-audi", "Audi", r"Audi", "S tronic, DSG, Multitronic, ZF 8HP, Tiptronic",
                   "A3, A4, A5, A6, A7, Q3, Q5, Q7",
                   ["<b>S tronic 0B5 / DL501</b> și <b>DL382 (0CK, 0CJ)</b>: A4, A5, A6, A7, Q5 cu motor longitudinal", "<b>DSG DQ200, DQ250, DQ381</b>: A1, A3, Q2, Q3, TT cu motor transversal", "<b>Multitronic CVT (01J, 0AW)</b>: A4, A5, A6 cu tracțiune față", "<b>ZF 8HP</b> și <b>Aisin Tiptronic</b>: A6, A8, Q5, Q7"],
                   ("Ce cutie are Audi-ul meu?", "Depinde de model și motor: S tronic (0B5 sau DL382) pe A4–A7 și Q5, DSG pe A3 și Q3, Multitronic pe A4–A6 cu tracțiune față, ZF 8HP sau Aisin pe A6, A8 și Q7. Îți confirmăm după seria de șasiu."),
                   ["reparatie-cutie-dsg", "reparatie-mecatronic-dsg", "reparatie-cutie-cvt"]))
    P.append(brand("reparatie-cutie-automata-vw-skoda-seat", "VW, Skoda și Seat", r"\bVW\b|Volkswagen|Skoda|Seat", "DSG DQ200, DQ250, DQ381, DQ500, Aisin 09G",
                   "Golf, Passat, Tiguan, Touran, Touareg, Octavia, Superb, Kodiaq, Leon, Ateca",
                   ["<b>DSG DQ200</b> (7 trepte, ambreiaj uscat): motoarele mici și medii", "<b>DSG DQ250</b> (6 trepte, în ulei) și <b>DQ381 / DQ500</b> (7 trepte, în ulei): motoarele mai puternice și diesel", "<b>Aisin TF-60SN (09G)</b>: cutiile automate clasice cu convertizor", "<b>Aisin 09D</b> și <b>8 trepte</b>: Touareg"],
                   ("DSG sau automată clasică: ce am pe Golf sau Octavia?", "Majoritatea modelelor recente au DSG (DQ200 la motoarele mici, DQ250 sau DQ381 la cele puternice). Unele modele, mai ales cele mai vechi sau cu motoare de 1.6 pe benzină, au cutia clasică Aisin 09G. Îți confirmăm după seria de șasiu."),
                   ["reparatie-cutie-dsg", "reparatie-mecatronic-dsg", "reparatie-cutie-aisin"]))
    return P
