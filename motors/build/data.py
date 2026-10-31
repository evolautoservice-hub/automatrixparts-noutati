# -*- coding: utf-8 -*-
"""Content and data for automatrixmotors.ro (v2)."""
import re

SITE = "https://automatrixmotors.ro"
PHONE1, PHONE1_T, PHONE1_W = "0734 607 050", "+40734607050", "40734607050"
PHONE2, PHONE2_T, PHONE2_W = "0734 960 810", "+40734960810", "40734960810"
EMAIL = "service@automatrixmotors.ro"
MAPS = "https://g.page/r/CaVPuXWOanrLEBM"
FB = "https://www.facebook.com/cutiiautomateploiesti"
IG = "https://www.instagram.com/automatrix_prahova/"
TT = "https://www.tiktok.com/@automatrixmotors"
PROG = "https://programari.automatrixmotors.ro"
UPDATED = "2026-10-29"

from catalog import CATALOG, pick, min_price, FAM_LABEL, FAM_ORDER
PRICES = {"revizii": [[c["name"], c["price"]] for c in CATALOG if c["kind"] == "revizie"],
          "reparatii": [[c["name"], c["price"]] for c in CATALOG if c["kind"] == "reparatie"]}


def fmt(n):
    return f"{n:,}".replace(",", ".")


# ---------------------------------------------------------------- services
# Each page: slug, nav label, title, description, h1, eyebrow, lead, spec rows, body html, price rows, faq, related
PAGES = []

PAGES.append(dict(
    slug="reparatii-cutii-automate", nav="Reparații cutii automate", navsub="DSG, ZF, Aisin, Mercedes, CVT",
    title="Reparații cutii automate: prețuri, deviz și garanție 24 luni",
    desc="Reparații cutii de viteze automate DSG, S tronic, ZF, Aisin, Mercedes și CVT în Băicoi, Prahova. Deviz înainte de lucru, garanție scrisă 24 de luni.",
    h1="Reparații cutii automate, garantate 24 de luni",
    eyebrow="Serviciul principal",
    lead="Desfacem cutia, aflăm exact ce s-a uzat, înlocuim doar ce trebuie și o testăm la drum. Primești prețul în scris înainte să începem și garanție de 24 de luni după.",
    spec=[("Preț reparație", "de la 1.199 lei", "big"), ("Durată medie", "5 zile lucrătoare", ""), ("Garanție", "24 luni, fără limită de km", "red"), ("Cutii", "DSG, ZF, Aisin, G-Tronic, CVT", "")],
    service_type="Reparații cutii de viteze automate", min_price=1199,
    body="""
<h2>Când are nevoie cutia automată de reparație</h2>
<p>O cutie automată anunță aproape mereu din timp că ceva nu e în regulă. Dacă observi unul dintre semnele de mai jos, merită o diagnoză acum. O problemă prinsă devreme costă de obicei de câteva ori mai puțin decât o cutie care a mers luni de zile cu defectul.</p>
<ul class="dots">
<li><b>Smucituri sau șocuri</b> la schimbarea treptelor, mai ales la rece sau la plecarea de pe loc</li>
<li><b>Patinare:</b> turația crește, dar mașina nu accelerează pe măsură</li>
<li><b>Modul de avarie:</b> cutia rămâne într-o singură treaptă și apare o eroare pe bord</li>
<li><b>Întârziere</b> la cuplarea în D sau R, cu o bufnitură la final</li>
<li><b>Zgomote, vibrații</b> sau tremurături la viteză constantă</li>
<li><b>Pete de ulei roșiatic</b> sub mașină</li>
</ul>
<p>Pe fiecare simptom în parte am scris un ghid detaliat: <a class="link" href="/probleme-cutie-automata">probleme la cutia automată, cauze și ce faci</a>.</p>

<h2>Cum facem o reparație corect</h2>
<p>Garanția de 24 de luni o putem da pentru că nu ghicim și nu schimbăm piese la întâmplare. Fiecare cutie trece prin aceiași pași:</p>
<ul class="ticks">
<li><b>Diagnoză completă:</b> citim erorile, urmărim presiunile și adaptările în mers și testăm mașina la drum.</li>
<li><b>Deviz în scris:</b> îți spunem ce are cutia, ce piese trebuie și cât costă. Lucrăm doar după acordul tău.</li>
<li><b>Demontare și măsurare:</b> verificăm ambreiajele, pompa, bucșele, garniturile și blocul hidraulic.</li>
<li><b>Piese de calitate:</b> seturi de reparație complete, uleiul și filtrul cerute de producător.</li>
<li><b>Reasamblare la cote</b> și adaptările de bază pe calculator.</li>
<li><b>Test la drum</b> în toate treptele, la rece și la cald, înainte de predare.</li>
</ul>

<h2>Ce cutii automate reparăm</h2>
<h3>Cutii cu convertizor de cuplu</h3>
<p>Cutiile clasice, cu planetare și convertizor hidraulic: <a class="link" href="/reparatie-cutie-zf">ZF 6HP și 8HP</a> (BMW, Audi, Land Rover, Jaguar, Porsche), <a class="link" href="/reparatie-cutie-mercedes">Mercedes 5G, 7G și 9G-Tronic</a>, Aisin (VW Touareg, Volvo, Opel, Hyundai). Defectele frecvente sunt uzura ambreiajelor interne, a blocului hidraulic și a <a class="link" href="/reconditionare-convertizor-cuplu">convertizorului de cuplu</a>.</p>
<h3>Cutii cu dublu ambreiaj</h3>
<p>Cutiile <a class="link" href="/reparatie-cutie-dsg">DSG și S tronic</a> (DQ200, DQ250, DQ381, DQ500, 0B5), dar și DCT-urile Ford, Hyundai și Kia. Aici problemele vin de obicei din ambreiaje și din <a class="link" href="/reparatie-mecatronic-dsg">mecatronic</a>.</p>
<h3>Cutii CVT</h3>
<p>Cutii cu variație continuă: Audi Multitronic, Jatco (Nissan, Renault, Mitsubishi) și Toyota. Detalii pe pagina despre <a class="link" href="/reparatie-cutie-cvt">reparația cutiilor CVT</a>.</p>

<h2>Cât costă reparația unei cutii automate</h2>
<p>Prețul depinde de tipul cutiei și de ce s-a uzat. Un set de garnituri pentru mecatronic pornește de la 1.199 lei, o recondiționare de convertizor de la 7.099 lei, iar o reparație completă de cutie cu dublu ambreiaj trece de 20.000 de lei. Câteva repere, cu manopera inclusă. Apasă pe o lucrare ca să vezi operațiunile și piesele.</p>
""",
    prices=pick(r"Set garnituri mecatronic ZF 6HP19|convertizor de cuplu BMW 6|Set reparație ambreiaj DSG 7 DQ200 VW|Recondiționare mecatronic BMW 8HP|Înlocuire ambreiaje cutie BMW 8|7G-Tronic 722|DSG DQ381 VW|0B5 S tronic 7 trepte Audi$|GA8F22AW|Ford 8F35", "reparatie"),
    faq=[
        ("Cât costă reparația unei cutii automate?", "Între 1.199 lei, pentru un set de garnituri de mecatronic, și 25.199 lei, pentru reparația completă a unei cutii Porsche PDK. Prețul exact îl primești în scris după diagnoză, înainte să începem."),
        ("Cât durează reparația?", "În medie 5 zile lucrătoare. Termenul exact depinde de piese și îl afli după diagnoză."),
        ("Ce acoperă garanția de 24 de luni?", "Garanția de 24 de luni, fără limită de kilometri, se acordă în scris pentru reparațiile de cutii automate făcute în atelierul nostru. Acoperă piesele montate și manopera, în condițiile din certificatul de garanție."),
        ("Merită reparată cutia sau e mai bine una la mâna a doua?", "O cutie la mâna a doua are istoric necunoscut și de obicei garanție scurtă. O cutie reparată la noi are piesele uzate înlocuite, ulei nou și garanție de 24 de luni. În majoritatea cazurilor reparația iese mai sigur și pe termen lung mai ieftin."),
    ],
    related=["revizie-cutie-automata", "reparatie-cutie-dsg", "probleme-cutie-automata"],
))

PAGES.append(dict(
    slug="revizie-cutie-automata", nav="Revizie cutie automată", navsub="Ulei Motul, după manualul producătorului",
    title="Revizie cutie automată și schimb ulei | de la 699 lei",
    desc="Revizie cutie automată făcută exact după manualul producătorului cutiei: ulei Motul, filtru, garnituri, nivel reglat la temperatură. DSG, ZF, Aisin, Mercedes. De la 699 lei.",
    h1="Revizie cutie automată și schimb de ulei",
    eyebrow="Întreținere",
    lead="Uleiul este sângele cutiei automate. Facem revizia exact după manualul de reparație emis de producătorul cutiei: ulei Motul, filtru și garnituri noi, nivel reglat la temperatura de lucru. Fără scurtături. Este cea mai ieftină asigurare pentru cutia ta.",
    spec=[("Preț revizie", "de la 699 lei", "big"), ("Durată", "de obicei în aceeași zi", ""), ("Interval recomandat", "60.000–80.000 km", ""), ("Include", "ulei, filtru, garnituri, manoperă", "")],
    service_type="Revizie cutie automată / schimb ulei cutie automată", min_price=699,
    body="""
<h2>De ce trebuie schimbat uleiul cutiei automate</h2>
<p>În cutia automată, uleiul face trei lucruri deodată: transmite presiunea care cuplează ambreiajele, unge angrenajele și răcește. Cu timpul se încălzește de mii de ori, își pierde aditivii și se încarcă cu particule fine din ambreiaje. Un ulei obosit înseamnă schimbări mai dure, uzură accelerată și, în final, reparații scumpe.</p>
<p>Mulți producători spun că uleiul e „pe viață”. În practică, „viața” aceea e adesea calculată pentru perioada de garanție a mașinii noi. Specialiștii în cutii automate recomandă schimbul preventiv.</p>

<h2>Ce include revizia la AutoMatrix</h2>
<div class="callout" style="margin-top:20px"><p><b>Revizia ca la fabrică.</b> Lucrăm după manualul de reparație emis de producătorul fiecărei cutii: aceleași piese, aceleași cantități, aceleași cupluri de strângere și aceeași temperatură de verificare a nivelului. Așa știi că cutia ta a primit exact ce a cerut constructorul ei.</p></div>
<ul class="ticks">
<li><b>Ulei Motul</b> care respectă specificația producătorului cutiei.</li>
<li><b>Filtru sau sită nouă.</b> La cutiile ZF 6HP și 8HP, filtrul este integrat în baia de ulei și se schimbă împreună cu ea.</li>
<li><b>Garnituri și dopuri noi</b>, ca să nu apară scurgeri.</li>
<li><b>Procedura producătorului, pas cu pas:</b> urmăm manualul de reparație al cutiei, cu cantitățile, cuplurile de strângere și temperaturile prescrise de fabrică.</li>
<li><b>Nivel verificat la temperatura</b> indicată de producător, singura metodă corectă la o cutie automată.</li>
<li><b>Citirea erorilor și adaptări</b> pe calculator, unde cutia o cere.</li>
<li><b>Test la drum</b> după revizie.</li>
</ul>

<h2>La câți kilometri se face revizia</h2>
<p>Ca regulă generală, între 60.000 și 80.000 km, sau la 4–5 ani. Intervalul se scurtează dacă mergi mult în oraș, tractezi remorcă, urci des pe munte sau ai un stil de condus sportiv.</p>
<ul class="dots">
<li><b>DSG cu ambreiaje în baie de ulei</b> (DQ250, DQ381, DQ500): la 60.000 km, conform recomandării producătorului.</li>
<li><b>ZF 6HP / 8HP, Aisin, Mercedes 7G / 9G:</b> între 60.000 și 80.000 km.</li>
<li><b>CVT:</b> între 40.000 și 60.000 km, pentru că uleiul lucrează la temperaturi mari.</li>
<li><b>Dacă nu știi când s-a făcut ultima dată,</b> fă revizia acum. E cel mai sigur punct de plecare.</li>
</ul>
<div class="callout"><p>Dacă cutia smucește deja sau patinează, un schimb de ulei nu repară uzura mecanică și uneori o poate scoate la iveală. În acest caz îți recomandăm întâi o diagnoză. Vezi și <a class="link" href="/probleme-cutie-automata">ghidul de simptome</a>.</p></div>

<h2>Prețuri revizie cutie automată</h2>
<p>Pachet complet: ulei Motul, filtru, garnituri și manoperă. Aici sunt cutiile cerute cel mai des. Toate cele peste 230 de pachete de revizie sunt pe pagina de <a class="link" href="/preturi-cutii-automate">prețuri</a>.</p>
""",
    prices=pick(r"^Revizie cutie (DSG VW|DSG DQ250 VW OEM|DSG DQ381/DQ500 VW OEM|DSG 7 VW|BMW 6HP|BMW 8HP|Audi 8HP55A 0BK|7G-Tronic|9G-Tronic Mercedes|Aisin 6 trepte Tiptronic VW 09D|Aisin 8 trepte BMW|Audi Multitronic CVT|DCT MPS6 Ford|A8LF1 8 trepte Hyundai|6 trepte 09G VW|Land Rover 8HP|Audi S tronic 7 trepte 0CK 0CJ)$", "revizie"),
    faq=[
        ("Cât costă revizia cutiei automate?", "Între 699 lei (Renault DC4) și 4.899 lei (BMW 8HP Hybrid). Prețul include uleiul Motul, filtrul, garniturile și manopera."),
        ("Cât durează o revizie?", "De obicei o faci în aceeași zi. Te rugăm să faci programare, ca să avem piesele pregătite pentru cutia ta."),
        ("Schimbul de ulei poate strica o cutie automată?", "Un schimb făcut corect, cu uleiul potrivit și nivelul reglat la temperatură, nu strică o cutie sănătoasă. La o cutie deja uzată, schimbul nu repară defectul. De aceea facem diagnoza înainte."),
        ("Pot face doar schimb de ulei, fără filtru?", "Nu recomandăm. Filtrul reține particulele din ambreiaje, iar un filtru colmatat scade presiunea din cutie. Revizia completă costă puțin în plus și protejează cutia."),
    ],
    related=["preturi-cutii-automate", "reparatii-cutii-automate", "probleme-cutie-automata"],
))

PAGES.append(dict(
    slug="reparatie-cutie-dsg", nav="Reparație cutie DSG", navsub="DQ200, DQ250, DQ381, DQ500, S tronic",
    title="Reparație cutie DSG și S tronic | DQ200, DQ381, DQ500",
    desc="Reparație cutie DSG și S tronic: ambreiaj DQ200, mecatronic DQ250, DQ381, DQ500, 0B5. Prețuri afișate, garanție 24 luni. VW, Audi, Skoda, Seat. Băicoi, Prahova.",
    h1="Reparație cutie DSG și S tronic",
    eyebrow="Cutii cu dublu ambreiaj",
    lead="Lucrăm zilnic pe cutii DSG și S tronic, de la DQ200 cu ambreiaj uscat până la DQ500 și 0B5. Știm defectele tipice ale fiecărui cod și le reparăm cu garanție de 24 de luni.",
    spec=[("Ambreiaj DQ200", "de la 6.599 lei", "big"), ("Mecatronic", "de la 4.199 lei", ""), ("Garanție", "24 luni, fără limită de km", "red"), ("Coduri", "DQ200, DQ250, DQ381, DQ500, 0B5", "")],
    service_type="Reparație cutie DSG / S tronic", min_price=4199,
    body="""
<h2>Cum funcționează o cutie DSG</h2>
<p>DSG (Direct Shift Gearbox) are două ambreiaje: unul pentru treptele impare, celălalt pentru cele pare. Când mergi într-o treaptă, cutia are deja următoarea pregătită și trece dintr-un ambreiaj în celălalt în câteva sutimi de secundă. De aici vin schimbările rapide și consumul mic. De aici vin și defectele specifice: ambreiajele se uzează, iar <a class="link" href="/reparatie-mecatronic-dsg">mecatronicul</a> care le comandă lucrează sub presiune mare.</p>
<div class="codes"><span>DQ200 / 0AM / 0CW</span><span>DQ250 / 02E</span><span>DQ381 / 0GC</span><span>DQ500 / 0BH / 0BT</span><span>S tronic 0B5</span><span>S tronic 0CK / 0CL / 0CJ / 0DK</span></div>

<h2>Defectele tipice, pe cod de cutie</h2>
<h3>DQ200, 7 trepte, ambreiaj uscat</h3>
<p>Cea mai răspândită cutie DSG, montată pe Golf, Octavia, Leon, A3, Polo, Fabia, cu motoare de până la 250 Nm. Ambreiajele uscate se încălzesc mult în trafic de oraș.</p>
<ul class="dots">
<li>Vibrații și smucituri la plecarea de pe loc și la manevre</li>
<li>Uzura ambreiajului dublu și a rulmentului de presiune</li>
<li>Bloc de valve sau acumulator fisurat în mecatronic, cu pierdere de presiune</li>
<li>Litera treptei clipește pe bord și cutia intră în avarie</li>
</ul>
<h3>DQ250, DQ381 și DQ500, ambreiaje în baie de ulei</h3>
<p>Cutiile pentru motoare puternice și SUV-uri: Passat, Tiguan, Superb, Kodiaq, Golf GTI și R, Audi S3, Transporter. Rezistă mai bine la cuplu, dar cer schimb de ulei la 60.000 km.</p>
<ul class="dots">
<li>Senzori de presiune defecți în mecatronic, cu șocuri și erori</li>
<li>Pompă auxiliară de ulei uzată la DQ381</li>
<li>Uzura ambreiajelor la mașinile cu putere mărită</li>
<li>Pierderea treptelor pare sau impare</li>
</ul>
<h3>S tronic 0B5 și cutiile longitudinale Audi</h3>
<p>Pe Audi A4, A5, A6, Q5 și Macan. Defectele frecvente sunt în mecatronic și în pachetele de ambreiaje, iar reparația cere demontarea completă a cutiei.</p>

<h2>Reparăm sau înlocuim?</h2>
<p>În cele mai multe cazuri nu e nevoie de o cutie nouă. Un set de ambreiaj, o reparație de mecatronic sau înlocuirea senzorilor rezolvă problema la o fracțiune din preț. După orice intervenție facem adaptările de bază și un test la drum, ca schimbările să fie din nou fine.</p>

<h2>Prețuri reparații DSG și S tronic</h2>
""",
    prices=[c for c in CATALOG if c["fam"] == "dsg" and (c["kind"] == "reparatie" or re.search(r"\bVW\b", c["name"]))],
    faq=[
        ("Cât costă schimbarea ambreiajului la DSG DQ200?", "Setul de reparație ambreiaj DSG 7 DQ200, montat, pornește de la 6.599 lei, cu manoperă și adaptări incluse."),
        ("De ce smucește DSG-ul la plecare?", "La DQ200 cauza cea mai des întâlnită este uzura ambreiajului dublu sau o adaptare pierdută. Poate fi și o problemă de presiune în mecatronic. O diagnoză arată exact cauza."),
        ("Ce înseamnă când litera treptei clipește pe bord?", "Cutia a detectat o eroare și s-a protejat intrând în modul de avarie. Cel mai des este o problemă de mecatronic sau de senzori. Evită să conduci mult așa și programează o diagnoză."),
        ("La câți km se schimbă uleiul la DSG?", "La cutiile cu ambreiaje în baie de ulei (DQ250, DQ381, DQ500), la 60.000 km. DQ200 are un circuit diferit, pe care îl verificăm la diagnoză."),
    ],
    related=["reparatie-mecatronic-dsg", "revizie-cutie-automata", "preturi-cutii-automate"],
))

PAGES.append(dict(
    slug="reparatie-mecatronic-dsg", nav="Mecatronic DSG", navsub="Reparație sau înlocuire",
    title="Reparație mecatronic DSG | DQ200, DQ250, DQ381, DQ500",
    desc="Reparație și înlocuire mecatronic DSG: senzori presiune, bloc valve, acumulator, adaptări. Litera clipește pe bord sau cutia intră în avarie? Garanție 24 luni.",
    h1="Reparație mecatronic DSG",
    eyebrow="Cutii cu dublu ambreiaj",
    lead="Mecatronicul este creierul și sistemul hidraulic al cutiei DSG. Când cedează, cutia smucește, pierde trepte sau intră în avarie. De cele mai multe ori se poate repara, fără un mecatronic nou.",
    spec=[("Reparație mecatronic", "de la 4.199 lei", "big"), ("Înlocuire DQ250", "de la 17.399 lei", ""), ("Garanție", "24 luni, fără limită de km", "red"), ("După montaj", "adaptări și test la drum", "")],
    service_type="Reparație mecatronic DSG", min_price=4199,
    body="""
<h2>Ce este mecatronicul</h2>
<p>Mecatronicul unește două componente într-un singur bloc: calculatorul cutiei (TCU) și blocul hidraulic cu electrovalve, senzori și, la unele cutii, acumulatorul de presiune. El decide când se schimbă treapta și apasă ambreiajele cu presiunea potrivită. Orice abatere de presiune se simte imediat în schimbări.</p>

<h2>Simptomele unui mecatronic defect</h2>
<ul class="dots">
<li>Litera treptei clipește pe bord, iar cutia rămâne în avarie</li>
<li>Mașina nu pleacă în D sau în R, ori pleacă cu întârziere</li>
<li>Lipsesc treptele pare sau impare</li>
<li>Șocuri puternice la schimbare, mai ales între 1 și 2</li>
<li>Erori de presiune, de senzori sau de electrovalve în memoria cutiei</li>
</ul>

<h2>Reparație sau mecatronic nou</h2>
<p>Un mecatronic nou costă mult, iar adesea defectul este localizat. Repararea se face pe componentă:</p>
<ul class="ticks">
<li><b>Senzori de presiune</b> înlocuiți, frecvent la DQ381 și DQ500</li>
<li><b>Bloc de valve sau acumulator</b> fisurat, tipic la DQ200</li>
<li><b>Electrovalve</b> blocate sau uzate</li>
<li><b>Etanșări și conexiuni</b> refăcute</li>
</ul>
<p>Când placa electronică este arsă sau carcasa este deteriorată, înlocuirea este varianta corectă. Îți spunem asta după diagnoză, cu prețurile pentru ambele variante.</p>
<div class="callout"><p>După orice lucrare la mecatronic facem adaptările de bază și învățarea punctelor de cuplare a ambreiajelor. Fără ele, chiar și un mecatronic nou schimbă prost.</p></div>

<h2>Prețuri mecatronic DSG</h2>
""",
    prices=pick(r"mecatronic|calculator TCU|pompă auxiliară|senzori|bloc de valve DSG", "reparatie"),
    faq=[
        ("Se poate repara mecatronicul DSG?", "Da, în majoritatea cazurilor. Senzorii de presiune, blocul de valve, acumulatorul și electrovalvele se pot înlocui separat. Înlocuirea completă este necesară doar când electronica sau carcasa sunt deteriorate."),
        ("Cât costă reparația mecatronicului DSG?", "Setul de reparație pentru mecatronicul DQ200 pornește de la 4.199 lei, iar înlocuirea senzorilor de presiune la DQ381 / DQ500 de la 5.999 lei. Înlocuirea mecatronicului DQ250 pornește de la 17.399 lei."),
        ("Pot conduce cu mecatronicul defect?", "Nu e recomandat. În modul de avarie cutia folosește o singură treaptă, iar un defect de presiune poate arde ambreiajele. Mergi doar cât e nevoie până la atelier."),
    ],
    related=["reparatie-cutie-dsg", "probleme-cutie-automata", "reparatii-cutii-automate"],
))

PAGES.append(dict(
    slug="reparatie-cutie-zf", nav="Reparație cutie ZF", navsub="6HP și 8HP, BMW, Audi, Land Rover",
    title="Reparație cutie ZF 6HP și 8HP | BMW, Audi, Land Rover",
    desc="Reparație și revizie cutie automată ZF 6HP și 8HP pentru BMW, Audi, Land Rover, Jaguar, Porsche. Mecatronic, convertizor, ambreiaje. Garanție 24 luni.",
    h1="Reparație cutie ZF 6HP și 8HP",
    eyebrow="Cutii cu convertizor",
    lead="ZF 6HP și 8HP sunt printre cele mai bune cutii automate construite vreodată, cu o condiție: să fie întreținute. Le reparăm și le revizuim pentru BMW, Audi, Land Rover, Jaguar, Porsche și Alfa Romeo.",
    spec=[("Revizie ZF 8HP", "de la 1.999 lei", "big"), ("Convertizor ZF", "de la 7.099 lei", ""), ("Garanție reparații", "24 luni, fără limită de km", "red"), ("Mărci", "BMW, Audi, Land Rover, Jaguar, Porsche", "")],
    service_type="Reparație cutie automată ZF 6HP / 8HP", min_price=1899,
    body="""
<h2>ZF 6HP și ZF 8HP, pe scurt</h2>
<p><b>ZF 6HP</b> are 6 trepte și a fost montată din 2001 pe BMW Seria 3, 5, 7 și X5, pe Range Rover, Jaguar și pe unele modele Audi. <b>ZF 8HP</b> a venit în 2009, cu 8 trepte, și o găsești astăzi pe aproape orice BMW, pe Audi A6, A8, Q7, pe Land Rover, Jaguar, Alfa Romeo Giulia și Stelvio, Maserati sau Porsche Cayenne.</p>
<div class="codes"><span>6HP19</span><span>6HP21</span><span>6HP26</span><span>6HP28</span><span>8HP45</span><span>8HP50</span><span>8HP70</span><span>8HP75</span><span>8HP95</span><span>8HP Hybrid</span></div>

<h2>Defectele întâlnite cel mai des</h2>
<ul class="dots">
<li><b>Tremurături la viteză constantă</b>, între 60 și 100 km/h: ambreiajul de blocare din convertizor e uzat</li>
<li><b>Schimbări dure sau întârziate</b> din cauza uleiului degradat ori a electrovalvelor uzate</li>
<li><b>Scurgeri de ulei</b> la baie sau la conectorul mecatronicului, cu pierderea treptat a presiunii</li>
<li><b>Modul de avarie</b> după erori de mecatronic sau de senzori de turație</li>
<li><b>Uzura ambreiajelor interne</b> la mașinile cu kilometraj mare și fără schimb de ulei</li>
</ul>

<h2>Uleiul „pe viață” și cutiile ZF</h2>
<p>ZF însăși recomandă schimbul uleiului la cutiile 6HP și 8HP, deși multe mașini au ieșit din fabrică cu mențiunea de ulei permanent. La aceste cutii filtrul este integrat în baia de plastic, așa că revizia corectă înseamnă baie nouă, ulei nou și nivel reglat la temperatură. Detalii pe pagina de <a class="link" href="/revizie-cutie-automata">revizie cutie automată</a>.</p>

<h2>Prețuri ZF</h2>
""",
    prices=[c for c in CATALOG if c["fam"] == "zf"],
    faq=[
        ("La câți km se schimbă uleiul la ZF 8HP?", "Recomandăm între 60.000 și 80.000 km, chiar dacă manualul mașinii vorbește de ulei pe viață. Revizia include baia de ulei cu filtru integrat."),
        ("De ce tremură mașina la 80 km/h la cutia ZF?", "Cel mai des, ambreiajul de blocare din convertizorul de cuplu este uzat sau uleiul și-a pierdut proprietățile. Diagnoza arată dacă ajunge o revizie sau e nevoie de recondiționarea convertizorului."),
        ("Reparați cutii ZF pentru Land Rover și Jaguar?", "Da. Range Rover, Range Rover Sport, Discovery și modelele Jaguar folosesc cutii ZF 6HP și 8HP, pe care le reparăm și le revizuim."),
    ],
    related=["reconditionare-convertizor-cuplu", "revizie-cutie-automata", "reparatii-cutii-automate"],
))

PAGES.append(dict(
    slug="reparatie-cutie-mercedes", nav="Cutie Mercedes G-Tronic", navsub="5G, 7G și 9G-Tronic",
    title="Reparație cutie Mercedes 7G-Tronic și 9G-Tronic",
    desc="Reparație și revizie cutie automată Mercedes 5G-Tronic (722.6), 7G-Tronic (722.9) și 9G-Tronic (725.0). Convertizor, placă conductoare, bloc valve. Garanție 24 luni.",
    h1="Reparație cutie Mercedes 7G-Tronic și 9G-Tronic",
    eyebrow="Cutii cu convertizor",
    lead="Reparăm și revizuim cutiile automate Mercedes-Benz 5G, 7G și 9G-Tronic. Fiecare are defectele ei tipice, pe care le cunoaștem bine și le rezolvăm cu garanție de 24 de luni.",
    spec=[("Revizie 7G-Tronic", "de la 2.399 lei", "big"), ("Convertizor 7G", "de la 7.699 lei", ""), ("Garanție reparații", "24 luni, fără limită de km", "red"), ("Coduri", "722.6, 722.9, 725.0", "")],
    service_type="Reparație cutie automată Mercedes G-Tronic", min_price=2399,
    body="""
<h2>Cutiile automate Mercedes</h2>
<ul class="dots">
<li><b>5G-Tronic (722.6):</b> 5 trepte, montată din 1996 până după 2010 pe Clasa C, E, ML, Sprinter și Vito. Robustă, dar sensibilă la ulei vechi.</li>
<li><b>7G-Tronic (722.9):</b> 7 trepte, din 2003, pe aproape toate modelele cu motor longitudinal. Cea mai întâlnită cutie Mercedes pe care o reparăm.</li>
<li><b>9G-Tronic (725.0):</b> 9 trepte, din 2013, pe Clasa C, E, S, GLC, GLE și pe multe Sprinter și Vito noi.</li>
</ul>

<h2>Defectele tipice ale cutiei 7G-Tronic</h2>
<ul class="dots">
<li><b>Placa conductoare cu senzori de turație</b>: cutia intră în avarie, apar erori de senzori și treapta rămâne blocată</li>
<li><b>Bloc de valve uzat</b>: schimbări dure între 2 și 3 sau la decelerare</li>
<li><b>Convertizor de cuplu</b>: vibrații la viteză constantă și supraîncălzire</li>
<li><b>Ulei degradat</b>: smucituri la rece și schimbări întârziate</li>
</ul>

<h2>9G-Tronic: întreținerea face diferența</h2>
<p>9G-Tronic lucrează cu ulei special și cu toleranțe foarte strânse. Un ulei necorespunzător sau un nivel greșit duc rapid la schimbări dure și la uzura convertizorului. Revizia o facem cu ulei Motul cu specificația Mercedes potrivită și reglăm nivelul exact la temperatura cerută de manualul de reparație Mercedes, citită pe testerul de diagnoză.</p>

<h2>Prețuri cutii Mercedes</h2>
""",
    prices=[c for c in CATALOG if c["fam"] == "mercedes"],
    faq=[
        ("De ce intră în avarie cutia 7G-Tronic?", "Cel mai des de la placa conductoare cu senzorii de turație sau de la o problemă de presiune în blocul de valve. Cu o diagnoză aflăm exact componenta defectă."),
        ("Cât costă revizia la 7G-Tronic?", "Revizia completă la 7G-Tronic, cu ulei, filtru, garnituri și manoperă, pornește de la 2.399 lei. La 9G-Tronic pornește de la 3.799 lei."),
        ("Reparați și cutiile de pe Sprinter și Vito?", "Da. Sprinter și Vito folosesc aceleași cutii 5G, 7G și 9G-Tronic, pe care le reparăm și le revizuim."),
    ],
    related=["reconditionare-convertizor-cuplu", "revizie-cutie-automata", "reparatii-cutii-automate"],
))

PAGES.append(dict(
    slug="reconditionare-convertizor-cuplu", nav="Convertizor de cuplu", navsub="Recondiționare și echilibrare",
    title="Recondiționare convertizor de cuplu | de la 7.099 lei",
    desc="Recondiționare convertizor de cuplu ZF 6HP, 8HP, Aisin, Mercedes 7G și 9G-Tronic: lamele, etanșări, sudură, echilibrare și test. De la 7.099 lei, garanție 24 luni.",
    h1="Recondiționare convertizor de cuplu",
    eyebrow="Cutii cu convertizor",
    lead="Vibrațiile la viteză constantă și turația care crește fără să accelerezi vin de multe ori din convertizorul de cuplu. Îl recondiționăm complet, la o fracțiune din prețul unuia nou.",
    spec=[("Recondiționare", "de la 7.099 lei", "big"), ("Include", "lamele, etanșări, echilibrare", ""), ("Garanție", "24 luni, fără limită de km", "red"), ("Tipuri", "ZF, Aisin, Mercedes 7G / 9G", "")],
    service_type="Recondiționare convertizor de cuplu", min_price=7099,
    body="""
<h2>Ce face convertizorul de cuplu</h2>
<p>Convertizorul leagă motorul de cutie prin ulei, nu printr-un ambreiaj clasic. Are în interior o pompă, o turbină și un stator, plus un ambreiaj de blocare care unește mecanic motorul cu cutia la viteză constantă, pentru consum mic. Ambreiajul acesta se uzează primul.</p>

<h2>Simptomele unui convertizor uzat</h2>
<ul class="dots">
<li><b>Tremurături ușoare</b> între 60 și 100 km/h, la accelerație mică, ca și cum ai trece peste un drum cu denivelări fine</li>
<li><b>Turația crește</b> fără ca mașina să accelereze pe măsură</li>
<li><b>Cutia se încălzește</b> și uleiul se degradează repede</li>
<li><b>Zgomot de bâzâit</b> din zona clopotului cutiei</li>
<li><b>Erori de alunecare</b> a ambreiajului de blocare în memoria cutiei</li>
</ul>

<h2>Cum îl recondiționăm</h2>
<ul class="ticks">
<li>Deschidem convertizorul prin strunjire</li>
<li>Curățăm complet carcasa și componentele interne</li>
<li>Înlocuim lamelele ambreiajului de blocare, garniturile și rulmenții axiali</li>
<li>Îl sudăm la loc și îl echilibrăm dinamic</li>
<li>Testăm etanșeitatea sub presiune înainte de montaj</li>
</ul>
<div class="callout"><p>Un convertizor uzat contaminează uleiul cu particule. De aceea, la montarea convertizorului recondiționat facem și revizia completă a cutiei.</p></div>

<h2>Prețuri recondiționare convertizor</h2>
""",
    prices=pick(r"convertizor"),
    faq=[
        ("Cât costă recondiționarea convertizorului de cuplu?", "Pornește de la 7.099 lei pentru BMW 6HP și Audi 5HP. Pentru Mercedes 7G-Tronic de la 7.699 lei, iar pentru 9G-Tronic de la 11.799 lei."),
        ("Cum îmi dau seama că e convertizorul?", "Simptomul clasic este o tremurătură fină la viteză constantă și accelerație mică, între 60 și 100 km/h. Confirmăm cauza la diagnoză, pe baza datelor de alunecare ale ambreiajului de blocare."),
        ("E mai bine recondiționat sau nou?", "Un convertizor recondiționat corect, cu lamele și etanșări noi și echilibrat, funcționează ca unul nou, la o fracțiune din preț. Îl garantăm 24 de luni."),
    ],
    related=["reparatie-cutie-zf", "reparatie-cutie-mercedes", "probleme-cutie-automata"],
))

PAGES.append(dict(
    slug="reparatie-cutie-cvt", nav="Reparație cutie CVT", navsub="Multitronic, Jatco, Toyota",
    title="Reparație cutie CVT și Multitronic | Nissan, Audi, Toyota",
    desc="Reparație și revizie cutie CVT: Audi Multitronic, Jatco pentru Nissan, Renault, Mitsubishi și Toyota. Zgomot, patinare, smucituri la plecare. Băicoi, Prahova.",
    h1="Reparație cutie CVT și Multitronic",
    eyebrow="Cutii cu variație continuă",
    lead="Cutiile CVT nu au trepte fixe. Folosesc o curea sau un lanț între două fulii cu diametru variabil. Sunt fine și economice, dar sensibile la ulei și la căldură. Le diagnosticăm și le reparăm.",
    spec=[("Revizie CVT", "de la 1.799 lei", "big"), ("Interval revizie", "40.000–60.000 km", ""), ("Garanție reparații", "24 luni, fără limită de km", "red"), ("Tipuri", "Multitronic, Jatco, Toyota", "")],
    service_type="Reparație cutie CVT", min_price=1799,
    body="""
<h2>Unde întâlnești o cutie CVT</h2>
<ul class="dots">
<li><b>Audi Multitronic</b> (01J, 0AW), cu lanț, pe A4, A5 și A6 cu tracțiune față</li>
<li><b>Jatco</b> pe Nissan Qashqai, X-Trail, Juke, pe Renault, Dacia, Mitsubishi și Suzuki</li>
<li><b>Toyota și Lexus</b>, inclusiv sistemele hibride cu transmisie e-CVT</li>
<li><b>Honda, Subaru</b> și alte modele japoneze</li>
</ul>

<h2>Simptome frecvente</h2>
<ul class="dots">
<li>Zgomot de urlet sau șuierat care crește cu viteza</li>
<li>Turația urcă mult, dar mașina accelerează greu</li>
<li>Smucituri la plecarea de pe loc, tipice la Multitronic</li>
<li>Mașina intră în regim de protecție după drum lung sau în pantă</li>
</ul>

<h2>Uleiul la CVT</h2>
<p>CVT-ul folosește un ulei dedicat, cu frecare controlată între curea și fulii. Orice alt ulei, chiar și un ATF bun, poate face cureaua să patineze. Recomandăm schimbul între 40.000 și 60.000 km, cu ulei Motul pentru CVT, cu specificația producătorului.</p>
<div class="callout"><p>Reparațiile diferă mult între Multitronic, Jatco și Toyota. Trimite-ne pe WhatsApp un video cu simptomul și îți dăm o primă estimare.</p></div>
<h2>Prețuri CVT și Multitronic</h2>
""",
    prices=[c for c in CATALOG if c["fam"] == "cvt"],
    faq=[
        ("Ce ulei se pune la cutia CVT?", "Doar ulei pentru CVT cu specificația producătorului cutiei. Noi folosim ulei Motul pentru CVT. Un ATF clasic poate face cureaua sau lanțul să patineze."),
        ("De ce urlă cutia CVT?", "Zgomotul care crește cu viteza vine de obicei de la rulmenții fuliilor sau de la uzura curelei sau a lanțului. Diagnoza arată exact componenta."),
        ("Cât costă reparația unei cutii CVT?", "Revizia pornește de la 1.799 lei. Reparațiile pornesc de la 5.899 lei pentru setul de reparație al modulului Multitronic, iar o reparație completă de CVT costă între 17.899 și 18.599 lei. Prețul exact îl primești în scris după diagnoză."),
    ],
    related=["probleme-cutie-automata", "revizie-cutie-automata", "reparatii-cutii-automate"],
))

PAGES.append(dict(
    slug="probleme-cutie-automata", nav="Probleme cutie automată", navsub="Simptome, cauze, ce faci",
    title="Cutia automată smucește? Simptome, cauze și soluții",
    desc="Cutia automată smucește, patinează, intră în avarie sau întârzie în D și R? Ghid cu cauzele fiecărui simptom și ce trebuie să faci, scris de mecanici specializați.",
    h1="Probleme la cutia automată: simptome, cauze și ce faci",
    eyebrow="Ghid",
    lead="Am adunat aici simptomele pe care le vedem cel mai des la atelier, cu cauzele posibile și cu ce merită făcut în fiecare caz. Folosește ghidul ca punct de plecare. Răspunsul exact îl dă diagnoza.",
    spec=[("Diagnoză", "cu programare", "big"), ("Răspuns pe WhatsApp", "de regulă în aceeași zi", ""), ("Reparații", "garanție 24 de luni", "red"), ("Telefon", PHONE1, "")],
    service_type="Diagnoză cutie automată", min_price=None,
    body="""
<h2>Cutia automată smucește la schimbarea treptelor</h2>
<p>Cel mai des întâlnit simptom. Dacă smucește doar la rece și se liniștește după câțiva kilometri, de obicei uleiul e degradat sau presiunea e la limită. Dacă smucește tot timpul, cauza poate fi uzura ambreiajelor, blocul de valve sau mecatronicul.</p>
<ul class="dots">
<li><b>La DSG DQ200:</b> uzura ambreiajului dublu sau o adaptare pierdută</li>
<li><b>La ZF și Mercedes:</b> ulei vechi, electrovalve uzate, bloc de valve</li>
<li><b>Ce faci:</b> o diagnoză, apoi, după caz, <a class="link" href="/revizie-cutie-automata">revizie</a> sau reparație</li>
</ul>

<h2>Cutia patinează sau turează fără să accelereze</h2>
<p>Turația urcă, dar mașina nu ține pasul. Înseamnă că un ambreiaj din cutie alunecă. Cauzele sunt nivelul scăzut de ulei, presiunea insuficientă sau ambreiajele uzate. Patinarea încălzește repede cutia, iar fiecare kilometru agravează uzura.</p>
<ul class="dots"><li><b>Ce faci:</b> verifici dacă sunt scurgeri sub mașină și mergi cât mai puțin până la diagnoză.</li></ul>

<h2>Cutia a intrat în modul de avarie</h2>
<p>Apare un mesaj sau o lumină pe bord, cutia rămâne într-o singură treaptă (de obicei a 2-a sau a 3-a) și mașina accelerează greu. Este modul în care cutia se protejează. Cauza poate fi un senzor, mecatronicul, o problemă electrică sau o presiune anormală.</p>
<ul class="dots"><li><b>Ce faci:</b> nu șterge erorile la întâmplare. Ele ne spun exact unde e problema. Vezi <a class="link" href="/reparatie-mecatronic-dsg">mecatronic DSG</a> și <a class="link" href="/reparatie-cutie-mercedes">7G-Tronic</a>.</li></ul>

<h2>Întârziere la cuplarea în D sau R</h2>
<p>Pui selectorul în D sau R și mașina reacționează după o secundă sau două, uneori cu o bufnitură. Semnul clasic al unei pierderi de presiune: garnituri întărite, ulei puțin sau uzat, pompă slăbită.</p>

<h2>Vibrații și tremurături la viteză constantă</h2>
<p>O tremurătură fină între 60 și 100 km/h, la accelerație mică, indică de cele mai multe ori ambreiajul de blocare din <a class="link" href="/reconditionare-convertizor-cuplu">convertizorul de cuplu</a>. La DSG, vibrațiile la plecare vin din ambreiajul dublu.</p>

<h2>Zgomote și pete de ulei</h2>
<p>Un urlet care crește cu viteza poate veni de la rulmenți. Petele de ulei roșiatic sub mașină înseamnă scurgeri la baie, la garnituri sau la conectorul mecatronicului. O cutie automată cu nivel scăzut de ulei se poate distruge în câteva sute de kilometri.</p>

<h2>Ce să nu faci</h2>
<ul class="dots">
<li>Nu turna aditivi „miraculoși” în cutie. Pot masca simptomul și pot afecta ambreiajele.</li>
<li>Nu completa cu orice ulei. Fiecare cutie cere o specificație anume.</li>
<li>Nu conduce zile întregi în modul de avarie.</li>
<li>Nu cumpăra o cutie la mâna a doua până nu știi exact ce are a ta.</li>
</ul>
<div class="callout"><p>Trimite-ne pe WhatsApp, la <b>""" + PHONE1 + """</b>, un video scurt cu simptomul, marca, modelul și anul. Îți spunem ce credem și ce pași urmează.</p></div>
""",
    prices=[],
    faq=[
        ("De ce smucește cutia automată la rece?", "Cel mai des, uleiul e degradat sau presiunea e la limită până se încălzește cutia. Poate fi și începutul uzurii unui ambreiaj. O diagnoză și, de multe ori, o revizie rezolvă problema dacă e prinsă la timp."),
        ("Pot merge cu cutia în modul de avarie?", "Doar cât e nevoie ca să ajungi la service. Modul de avarie protejează cutia, dar condusul îndelungat așa poate agrava defectul."),
        ("Ajută un aditiv pentru cutia automată?", "Nu recomandăm aditivi. Ei pot masca simptomele pentru scurt timp, dar nu repară uzura și pot schimba frecarea ambreiajelor."),
        ("Cât costă o diagnoză la cutia automată?", "Sună-ne la " + PHONE1 + " și îți spunem costul la programare. Diagnoza include citirea erorilor, analiza datelor în mers și testul la drum."),
    ],
    related=["reparatii-cutii-automate", "revizie-cutie-automata", "reparatie-cutie-dsg"],
))

PAGES.append(dict(
    slug="reparatii-motoare-performanta", nav="Motoare de performanță", navsub="BMW M, Audi RS, AMG",
    title="Reparații motoare de performanță | BMW M, Audi RS, AMG",
    desc="Reparații motoare de performanță: reparații capitale, distribuție, turbo, consum de ulei, refacere după avarie. BMW M, Audi RS, Mercedes-AMG, VW R. Băicoi, Prahova.",
    h1="Reparații motoare de performanță",
    eyebrow="Motoare",
    lead="Pe lângă cutii automate, lucrăm pe motoare de putere mare. Același atelier, aceeași rigoare: diagnoză clară, deviz în scris înainte de lucru și piese de calitate.",
    spec=[("Preț", "după diagnoză", "big"), ("Deviz", "în scris, înainte de lucru", ""), ("Garanție", "scrisă, conform devizului", ""), ("Mărci", "BMW M, Audi RS, AMG, VW R", "")],
    service_type="Reparații motoare de performanță", min_price=None,
    body="""
<h2>Ce lucrări facem</h2>
<ul class="ticks">
<li><b>Reparații capitale</b> ale motorului: cuzineți, segmenți, chiulasă</li>
<li><b>Distribuție</b> pe lanț sau curea, cu întinzătoare și ghidaje</li>
<li><b>Turbosuflante</b> și sistemul de admisie</li>
<li><b>Consum de ulei</b> și pierderi de compresie</li>
<li><b>Refacere după avarie</b>: supraîncălzire, lipsă ulei, rupere de distribuție</li>
<li><b>Diagnoză</b> pentru pierderi de putere, rateuri și erori de motor</li>
</ul>

<h2>Motor și cutie, în același loc</h2>
<p>La mașinile performante, motorul și cutia lucrează împreună. Un motor care trage neuniform sau un convertizor care alunecă se pot confunda ușor. Fiindcă reparăm și cutii automate, putem diagnostica întregul grup motor-transmisie și știm exact unde e problema.</p>
<div class="codes"><span>BMW M</span><span>Audi RS și S</span><span>Mercedes-AMG</span><span>VW Golf GTI și R</span><span>Porsche</span><span>Cupra</span></div>
<div class="callout"><p>Prețul și termenul pentru lucrările la motor le stabilim după diagnoză, în scris. Sună-ne sau trimite-ne pe WhatsApp detaliile mașinii și simptomele.</p></div>
""",
    prices=[],
    faq=[
        ("Ce mărci de motoare de performanță reparați?", "Lucrăm frecvent pe BMW M, Audi RS și S, Mercedes-AMG, VW Golf GTI și R, Cupra și Porsche."),
        ("Faceți și reparații capitale?", "Da. Facem reparații capitale complete, inclusiv lucrări la chiulasă, după o diagnoză și un deviz în scris."),
    ],
    related=["reparatii-cutii-automate", "reconditionare-convertizor-cuplu", "reparatie-cutie-dsg"],
))

# ---------------------------------------------------------------- cities
from cities import CITIES

HOME_FAQ = [
    ("Ce acoperă garanția de 24 de luni?", "Garanția de 24 de luni, fără limită de kilometri, se acordă în scris pentru reparațiile de cutii automate făcute în atelierul nostru. Acoperă piesele montate și manopera, în condițiile din certificatul de garanție pe care îl primești la predare."),
    ("Cât durează o reparație?", "O revizie se face de obicei în aceeași zi. O reparație completă durează în medie 5 zile lucrătoare, în funcție de piese. Termenul exact îl afli după diagnoză."),
    ("La câți kilometri se face revizia cutiei automate?", "În general între 60.000 și 80.000 km, în funcție de cutie și de cum conduci. La DSG cu ambreiaje în baie de ulei, producătorul recomandă schimbul la 60.000 km."),
    ("Prețurile includ manopera?", "Da. Prețurile afișate sunt pentru pachetul complet, cu manoperă inclusă. Prețul final îl confirmăm după diagnoză, în scris, înainte să începem."),
    ("Ce ulei folosiți?", "Folosim ulei Motul, cu specificația cerută de producătorul cutiei. Pentru unele cutii avem și pachete cu filtru sau baie de ulei originale (OEM)."),
    ("Mașina nu mai merge. Ce fac?", "Nu mai conduce, ca să nu agravezi defectul. Sună-ne și găsim împreună cea mai simplă variantă ca mașina să ajungă la atelier."),
]


from pages2 import extra_pages
PAGES.extend(extra_pages(fmt))
