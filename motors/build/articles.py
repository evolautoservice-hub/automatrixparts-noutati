# -*- coding: utf-8 -*-
"""Articole (ghiduri) – conținut original pentru căutări informaționale."""
import re
from catalog import CATALOG


def _rows(rx, kind=None):
    return [c for c in CATALOG if re.search(rx, c["name"]) and (kind is None or c["kind"] == kind)]


def _min(rx, kind=None):
    p = [c["price"] for c in _rows(rx, kind)]
    return min(p) if p else 0


def _max(rx, kind=None):
    p = [c["price"] for c in _rows(rx, kind)]
    return max(p) if p else 0


def articles(fmt):
    L = lambda s, t: f'<a class="link" href="/{s}">{t}</a>'
    A = []
    # 1 ----------------------------------------------------------------
    A.append(dict(
        slug="dsg-smuceste-la-plecare", date="2026-10-31",
        title="DSG smucește la plecare: cauze, ce faci și cât costă",
        desc="Cutia DSG smucește sau tremură la plecarea de pe loc? Cauzele reale (ambreiaj, mecatronic, adaptări), ce poți verifica și cât costă reparația DQ200, DQ250 și DQ381.",
        h1="DSG smucește la plecare: cauze, ce faci și cât costă",
        lead="Smuciturile la plecarea de pe loc sunt cea mai frecventă plângere la cutiile DSG. Vestea bună: în multe cazuri cauza e clară și reparația are un preț cunoscut dinainte.",
        body=f"""
<h2>Mai întâi: ce DSG ai</h2>
<p>Contează foarte mult ce cutie DSG are mașina. <b>DQ200</b> (7 trepte, ambreiaj uscat) e montată pe motoarele mici și medii: Golf, Polo, Octavia, Fabia, Leon, A3. <b>DQ250</b> (6 trepte) și <b>DQ381 / DQ500</b> (7 trepte) au ambreiajul în baie de ulei și sunt pe motoarele mai puternice și pe diesel. Simptomele seamănă, dar cauzele și prețurile diferă.</p>

<h2>Cauzele, de la cea mai frecventă</h2>
<ul class="dots">
<li><b>Ambreiajul dublu uzat</b> (mai ales la DQ200): tremur la plecare, în pantă și la manevre, uneori miros de ambreiaj</li>
<li><b>Adaptările ambreiajului pierdute</b> după o baterie descărcată sau o intervenție: se refac cu aparatul, fără piese</li>
<li><b>Mecatronicul</b>: blocul de valve, acumulatorul de presiune sau senzorii; apar coduri precum {L("coduri-eroare-dsg-dq200#p17bf", "P17BF")} sau {L("coduri-eroare-dsg-dq200#p189c", "P189C")}</li>
<li><b>Volanta cu masă dublă</b>: bătăi și vibrații la ralanti și la plecare</li>
<li><b>Uleiul vechi</b> la DQ250 și DQ381: ambreiajele în baie de ulei lucrează prost cu ulei degradat</li>
</ul>

<h2>Ce poți verifica singur</h2>
<p>Dacă smuciturile au apărut brusc după ce s-a descărcat bateria, cel mai probabil s-au pierdut adaptările. Dacă au venit treptat, în luni de zile, e uzură. Dacă litera treptei clipește pe bord sau mașina nu mai pleacă în D sau R, e aproape sigur mecatronicul și nu mai trebuie condusă.</p>

<h2>Cât costă</h2>
<ul class="dots">
<li>Set reparație ambreiaj DSG 7 DQ200: de la {fmt(_min(r"ambreiaj DSG 7 DQ200"))} lei</li>
<li>Set reparație mecatronic DQ200: de la {fmt(_min(r"Set reparație mecatronic DSG 7 DQ200"))} lei</li>
<li>Kit ambreiaje DQ250: de la {fmt(_min(r"kit ambreiaje DSG 02E"))} lei</li>
<li>Kit ambreiaje DQ381 / DQ500: de la {fmt(_min(r"kit ambreiaje DSG 0BH"))} lei</li>
<li>Revizie DSG: de la {fmt(_min(r"Revizie cutie DSG"))} lei</li>
</ul>
<p>Toate prețurile includ manopera și TVA și sunt pe {L("preturi-cutii-automate", "pagina de prețuri")}, cu operațiunile și piesele fiecărei lucrări. Reparațiile au garanție 24 de luni, fără limită de kilometri.</p>
""",
        faq=[("Pot conduce cu DSG-ul care smucește?", "Dacă smucește doar la plecare și litera treptei nu clipește, poți ajunge la service, dar evită pantele și traficul aglomerat. Dacă litera clipește sau mașina nu pleacă, oprește și cheamă platforma."),
             ("Resetarea adaptărilor rezolvă smuciturile?", "Doar dacă ambreiajul și mecatronicul sunt în regulă. Dacă ambreiajul e uzat, adaptările ajută câteva zile, apoi problema revine.")],
        related=["reparatie-cutie-dsg", "reparatie-mecatronic-dsg", "coduri-eroare-dsg-dq200"],
    ))
    # 2 ----------------------------------------------------------------
    A.append(dict(
        slug="probleme-powershift-ford-focus", date="2026-10-31",
        title="Probleme Powershift la Ford Focus și Fiesta: ce se strică și cât costă",
        desc="Cutia Powershift DPS6 de pe Ford Focus, Fiesta și C-Max: tremur la plecare, smucituri, Transmission malfunction. Cauze, soluții și prețuri de reparație.",
        h1="Probleme Powershift la Ford Focus și Fiesta",
        lead="Cutia Powershift DPS6, cu dublu ambreiaj uscat, e montată pe Ford Focus 3, Fiesta, B-Max, EcoSport și C-Max pe benzină. Are câteva defecte cunoscute, care se repară definitiv dacă sunt tratate corect.",
        body=f"""
<h2>Simptomele pe care le vedem cel mai des</h2>
<ul class="dots">
<li>Tremurături puternice la plecarea de pe loc, mai ales în pantă sau cu motorul rece</li>
<li>Smucituri la mers încet în trafic și la schimbarea din 1 în 2</li>
<li>Zgomote metalice sau „clonc” la oprire</li>
<li>Mesajul „Transmission malfunction” pe bord, uneori mașina rămâne în neutru</li>
</ul>

<h2>De unde vin</h2>
<p>La DPS6, cauza principală e <b>ambreiajul contaminat cu ulei</b>: simeringurile arborilor de intrare încep să piardă, uleiul ajunge pe garniturile ambreiajului uscat și acesta începe să „vibreze”. A doua cauză e <b>calculatorul cutiei (TCM)</b>, care poate ceda și blochează cutia. Mai rar, <b>actuatoarele ambreiajelor</b> sau furcile de schimbare.</p>
<p>Codurile de eroare frecvente: {L("coduri-eroare-cutie-automata#p0900", "P0900")}, {L("coduri-eroare-cutie-automata#p07a3", "P07A3")}, {L("coduri-eroare-cutie-automata#p0810", "P0810")}.</p>

<h2>Ce rezolvă definitiv problema</h2>
<p>Doar schimbarea ambreiajului nu e suficientă dacă simeringurile pierd: noul ambreiaj se contaminează din nou în câteva luni. Corect este să înlocuiești <b>ambreiajul dublu, rulmentul de presiune și simeringurile</b>, să verifici actuatoarele și apoi să faci adaptările cu aparatul.</p>

<h2>Prețuri</h2>
<p>Înlocuirea ambreiajelor la Powershift 6DCT250 pornește de la {fmt(_min(r"ambreiaje cutie Powershift 6DCT250"))} lei. Toate lucrările pentru Powershift, inclusiv cutiile MPS6 de pe Mondeo, Kuga și Volvo, sunt pe pagina {L("reparatie-cutie-powershift", "reparație cutie Powershift")}, cu garanție 24 de luni, fără limită de kilometri.</p>
""",
        faq=[("Merită reparată cutia Powershift sau înlocuită?", "O cutie la mâna a doua are aceleași piese uzate și aceleași simeringuri. O reparație corectă, cu ambreiaj și simeringuri noi și garanție, e de obicei varianta mai sigură și mai ieftină pe termen lung."),
             ("Cât durează reparația?", "Câteva zile lucrătoare, în funcție de piese. Termenul exact îl primești odată cu devizul.")],
        related=["reparatie-cutie-powershift", "reparatie-cutie-edc", "coduri-eroare-cutie-automata"],
    ))
    # 3 ----------------------------------------------------------------
    fams = [("DSG", r"Revizie cutie DSG|Revizie cutie Audi S tronic"), ("ZF 6HP și 8HP", r"Revizie cutie .*[68]HP"), ("Mercedes 7G / 9G-Tronic", r"Revizie cutie [79]G-Tronic"),
            ("Aisin", r"Revizie cutie Aisin"), ("CVT și Multitronic", r"Revizie cutie .*(CVT|Multitronic)"), ("Powershift MPS6", r"Revizie cutie DCT MPS6")]
    lines = "".join(f"<li><b>{n}:</b> {fmt(_min(rx, 'revizie'))} – {fmt(_max(rx, 'revizie'))} lei</li>" for n, rx in fams if _min(rx, "revizie"))
    A.append(dict(
        slug="cat-costa-revizia-cutiei-automate", date="2026-10-31",
        title="Cât costă revizia cutiei automate în 2026: prețuri pe tipuri de cutii",
        desc="Prețuri reale pentru revizia cutiei automate în 2026: DSG, ZF 8HP, 7G-Tronic, Aisin, CVT, Powershift. Ce include o revizie corectă și de ce contează manualul producătorului.",
        h1="Cât costă revizia cutiei automate în 2026",
        lead="Prețul unei revizii de cutie automată depinde de tipul cutiei, de cantitatea și tipul uleiului și de piesele care se schimbă obligatoriu. Mai jos sunt intervalele reale de preț de la noi, cu manoperă și TVA.",
        body=f"""
<h2>Prețuri pe tipuri de cutii</h2>
<ul class="dots">{lines}</ul>
<p>Lista completă, cu fiecare model și cu ce include fiecare pachet, e pe {L("preturi-cutii-automate", "pagina de prețuri")}.</p>

<h2>Ce include o revizie corectă</h2>
<ul class="dots">
<li>Diagnoză și verificarea codurilor din cutie înainte de lucrare</li>
<li>Ulei nou cu specificația cerută de producătorul cutiei (noi folosim Motul)</li>
<li>Filtru nou și, la multe cutii, baie de ulei sau garnituri noi</li>
<li>Completarea uleiului la nivelul corect, <b>la temperatura de control</b> indicată de producător</li>
<li>Adaptări cu aparatul și test la drum</li>
</ul>

<h2>De ce diferă atât de mult prețurile între service-uri</h2>
<p>Un „schimb de ulei la cutie” rapid, fără filtru, fără măsurarea nivelului la temperatura corectă și cu ulei universal costă mai puțin, dar nu e o revizie. Noi lucrăm după manualul de reparație emis de producătorul cutiei, fără aparat de schimb ulei care „spală” cutia, pentru că așa se respectă exact procedura și cantitățile.</p>

<h2>Când se face revizia</h2>
<p>Pentru majoritatea cutiilor recomandăm revizia la 60.000 km, la DSG cu ambreiaj în baie de ulei la 60.000 km, iar la cutiile solicitate (tractare, oraș, motoare modificate) mai des. Detalii în {L("cand-se-schimba-uleiul-la-cutia-automata", "articolul despre schimbul de ulei")}.</p>
""",
        faq=[("Revizia cutiei automate se face în aceeași zi?", "De obicei da. O revizie durează în jur de 3 ore, așa că poți lăsa mașina dimineață și o iei în aceeași zi."),
             ("Prețul include uleiul?", "Da. Prețurile includ uleiul Motul, filtrul, garniturile și manopera, cu TVA.")],
        related=["revizie-cutie-automata", "preturi-cutii-automate", "cand-se-schimba-uleiul-la-cutia-automata"],
    ))
    # 4 ----------------------------------------------------------------
    A.append(dict(
        slug="cutie-automata-mod-avarie", date="2026-10-31",
        title="Cutie automată în mod avarie: ce înseamnă și ce faci",
        desc="Cutia automată a intrat în mod avarie (rămâne în treapta a 2-a sau a 3-a)? Ce înseamnă, cauzele frecvente și pașii corecți ca să nu agravezi defectul.",
        h1="Cutie automată în mod avarie: ce înseamnă și ce faci",
        lead="Modul de avarie (sau „modul de urgență”) este felul în care cutia se protejează când calculatorul observă o problemă. Mașina merge, dar într-o singură treaptă și fără putere. Nu e un defect în sine, ci un semnal.",
        body=f"""
<h2>Cum îl recunoști</h2>
<ul class="dots">
<li>Mașina pleacă greu, dintr-o treaptă mare (de obicei 2 sau 3)</li>
<li>Nu mai schimbă treptele, iar turația crește mult la viteză mare</li>
<li>Se aprinde martorul cutiei sau Check Engine; la DSG litera treptei clipește</li>
<li>Uneori problema dispare după ce oprești și pornești motorul, apoi revine</li>
</ul>

<h2>Cauze frecvente</h2>
<ul class="dots">
<li><b>Senzori de turație sau de temperatură</b> defecți, mai ales la Mercedes 7G-Tronic (placa conductoare)</li>
<li><b>Electrovalve sau bloc de valve</b> uzate, frecvent la cutiile Aisin și ZF</li>
<li><b>Mecatronicul</b> la DSG și S tronic</li>
<li><b>Nivel scăzut de ulei</b> sau ulei supraîncălzit</li>
<li><b>Tensiune scăzută</b>: o baterie slabă poate da erori în cutie</li>
</ul>

<h2>Ce faci, pas cu pas</h2>
<ol class="steps-list">
<li>Oprește în siguranță și repornește motorul după un minut; dacă revine normal, poți ajunge cu grijă la service</li>
<li>Nu conduce pe autostradă și nu urca pante lungi în modul de avarie</li>
<li>Nu șterge codurile la întâmplare: ele sunt exact ce ne trebuie la diagnoză</li>
<li>Notează codul de eroare, dacă îl ai, și caută-l în {L("coduri-eroare-cutie-automata", "ghidul nostru de coduri")}</li>
<li>Dacă mașina nu mai pleacă deloc, cheamă platforma: tractarea cu roțile motoare pe asfalt strică cutia</li>
</ol>
<p>Primul pas la noi e diagnoza; prețul reparației îl primești în scris înainte să începem. Reparațiile au garanție 24 de luni, fără limită de kilometri.</p>
""",
        faq=[("Pot merge mult în modul de avarie?", "Distanțe scurte, cu viteză redusă, ca să ajungi la service. Mersul îndelungat așa supraîncălzește cutia și poate transforma o reparație mică într-una mare."),
             ("Bateria poate băga cutia în avarie?", "Da. Tensiunea scăzută dă erori de comunicație și de senzori. Verificăm întotdeauna și bateria la diagnoză.")],
        related=["probleme-cutie-automata", "coduri-eroare-cutie-automata", "reparatii-cutii-automate"],
    ))
    # 5 ----------------------------------------------------------------
    A.append(dict(
        slug="cand-se-schimba-uleiul-la-cutia-automata", date="2026-10-31",
        title="Când se schimbă uleiul la cutia automată (DSG, ZF, Aisin, CVT)",
        desc="La câți km se schimbă uleiul la cutia automată? Intervale recomandate pentru DSG, S tronic, ZF 8HP, 7G-Tronic, Aisin, CVT și Powershift, plus semnele că uleiul e degradat.",
        h1="Când se schimbă uleiul la cutia automată",
        lead="Mulți producători spun că uleiul din cutie e „pe viață”. În practică, „viața” aceea e cam cât garanția mașinii. Uleiul degradat e cauza numărul unu a defectelor scumpe la cutiile automate.",
        body=f"""
<h2>Intervale pe care le recomandăm</h2>
<ul class="dots">
<li><b>DSG cu ambreiaj în baie de ulei</b> (DQ250, DQ381, DQ500) și <b>S tronic</b>: la 60.000 km</li>
<li><b>DSG DQ200</b> (ambreiaj uscat): uleiul mecanic și cel din mecatronic, verificate la 60.000–80.000 km</li>
<li><b>ZF 6HP și 8HP</b>, <b>Mercedes 7G / 9G-Tronic</b>, <b>Aisin</b>: la 60.000–80.000 km</li>
<li><b>CVT și Multitronic</b>: la 40.000–60.000 km</li>
<li><b>Powershift MPS6</b>: la 60.000 km</li>
<li>Mai des pentru tractare, mers mult în oraș, taxi sau motoare modificate</li>
</ul>

<h2>Semne că uleiul e degradat</h2>
<ul class="dots">
<li>Schimbări mai dure sau întârziate decât înainte, mai ales cu cutia caldă</li>
<li>Ușoare tremurături la viteză constantă</li>
<li>La verificare: ulei închis la culoare și cu miros de ars</li>
</ul>

<h2>Schimb parțial sau revizie completă</h2>
<p>Un simplu schimb de ulei prin bușonul de golire înlocuiește doar o parte din ulei. O revizie corectă, după manualul producătorului cutiei, schimbă și filtrul, garniturile și, unde e cazul, baia de ulei, iar nivelul se face la temperatura de control. Vezi {L("cat-costa-revizia-cutiei-automate", "cât costă revizia pe tipuri de cutii")}.</p>
""",
        faq=[("E adevărat că uleiul din cutie e pe viață?", "Pentru producător, „viața” cutiei e de obicei perioada de garanție. După 100.000–150.000 km fără schimb, uleiul nu mai protejează ambreiajele și blocul de valve."),
             ("Schimbul de ulei la o cutie cu mulți km o poate strica?", "O revizie făcută corect, cu ulei cu specificația corectă și nivel la temperatura de control, nu strică o cutie sănătoasă. Dacă cutia are deja probleme, diagnoza arată ce trebuie făcut înainte.")],
        related=["revizie-cutie-automata", "cat-costa-revizia-cutiei-automate", "preturi-cutii-automate"],
    ))
    # 6 ----------------------------------------------------------------
    A.append(dict(
        slug="cutie-automata-second-hand-sau-reparatie", date="2026-10-31",
        title="Cutie automată second-hand sau reparație? Ce merită de fapt",
        desc="Merită să cumperi o cutie automată la mâna a doua sau e mai bine să o repari pe a ta? Riscuri, costuri ascunse și ce garanție primești în fiecare caz.",
        h1="Cutie automată second-hand sau reparație?",
        lead="Când primești un deviz mare pentru cutie, varianta „luăm una de la dezmembrări” pare tentantă. Uneori are sens, dar de cele mai multe ori iese mai scump.",
        body=f"""
<h2>Ce primești de fapt cu o cutie second-hand</h2>
<ul class="dots">
<li>O cutie cu kilometraj necunoscut și cu ulei de cele mai multe ori neschimbat</li>
<li>Aceleași piese de uzură ca a ta: ambreiaje, bloc de valve, simeringuri</li>
<li>Garanție de obicei de câteva zile sau doar „la montaj”</li>
<li>Costuri în plus: montaj, adaptări, uneori programarea calculatorului și imobilizatorul</li>
</ul>

<h2>Ce primești cu o reparație</h2>
<ul class="dots">
<li>Cutia ta, desfăcută, cu piesele uzate înlocuite cu piese noi</li>
<li>Prețul în scris înainte de lucrare, pe operațiuni și piese</li>
<li>La noi: <b>garanție 24 de luni, fără limită de kilometri</b></li>
</ul>

<h2>Când are sens o cutie la mâna a doua</h2>
<p>Doar dacă carcasa cutiei tale e spartă sau angrenajele sunt distruse și piesele nu se mai găsesc, ori dacă mașina are o valoare foarte mică. Și atunci, o cutie second-hand merită o revizie înainte de montaj.</p>
<p>Prețurile reparațiilor sunt publice pe {L("preturi-cutii-automate", "pagina de prețuri")}: le poți compara cu orice ofertă de cutie second-hand plus montaj.</p>
""",
        faq=[("O cutie recondiționată e același lucru cu una reparată?", "Depinde cine o recondiționează și ce garanție dă. Întreabă exact ce piese s-au schimbat și cât e garanția, în luni și în kilometri."),
             ("Cât costă montajul unei cutii aduse de client?", "Montajul și adaptările se stabilesc după model. Întreabă de la început ce garanție primești pentru o cutie adusă de tine, pentru că starea ei internă nu e cunoscută.")],
        related=["reparatii-cutii-automate", "preturi-cutii-automate", "probleme-cutie-automata"],
    ))
    # 7 ----------------------------------------------------------------
    A.append(dict(
        slug="masina-tremura-intre-60-si-100-km-h", date="2026-10-31",
        title="Mașina tremură între 60 și 100 km/h: convertizorul de cuplu",
        desc="Tremurături fine între 60 și 100 km/h la mașinile cu cutie automată? Cel mai des e ambreiajul convertizorului de cuplu. Cum îl recunoști, cod P0741 și cât costă recondiționarea.",
        h1="Mașina tremură între 60 și 100 km/h? Verifică convertizorul",
        lead="Dacă mașina cu cutie automată clasică tremură ușor, ca pe un drum cu denivelări fine, la viteze între 60 și 100 km/h, cel mai probabil vinovat e ambreiajul de blocare din convertizorul de cuplu.",
        body=f"""
<h2>Cum îl recunoști</h2>
<ul class="dots">
<li>Vibrații fine la viteză constantă, care dispar când accelerezi sau frânezi ușor</li>
<li>Turația „sare” cu 100–200 rpm la viteză constantă</li>
<li>Consum puțin mai mare și cutie mai caldă</li>
<li>Uneori codul {L("coduri-eroare-cutie-automata#p0741", "P0741")}</li>
</ul>
<p>Apare la cutiile cu convertizor: ZF 6HP și 8HP, Mercedes 7G-Tronic, Aisin și altele. Nu apare la DSG sau Powershift, care nu au convertizor.</p>

<h2>De ce apare</h2>
<p>Ambreiajul de blocare din convertizor are o garnitură de fricțiune care se uzează, iar uleiul degradat o face să „lipească-dezlipească” în loc să cupleze lin. Netratat, materialul uzat ajunge în tot circuitul de ulei și în blocul de valve.</p>

<h2>Soluția</h2>
<p>Dacă problema e la început, o revizie cu ulei nou poate ajuta. Dacă vibrațiile persistă, convertizorul se recondiționează: se taie, se schimbă garniturile și ambreiajul, se sudează și se echilibrează. Recondiționarea pornește de la {fmt(_min(r"Recondiționare convertizor"))} lei. Detalii pe pagina {L("reconditionare-convertizor-cuplu", "recondiționare convertizor de cuplu")}.</p>
""",
        faq=[("Pot circula cu convertizorul care vibrează?", "Da, pe termen scurt, dar nu amâna luni de zile: materialul de fricțiune uzat ajunge în blocul de valve și reparația se scumpește."),
             ("Ajunge doar schimbul de ulei?", "Uneori, la început. Dacă vibrațiile revin după revizie, convertizorul trebuie recondiționat.")],
        related=["reconditionare-convertizor-cuplu", "revizie-cutie-automata", "reparatie-cutie-zf"],
    ))
    # 8 ----------------------------------------------------------------
    A.append(dict(
        slug="cum-se-tracteaza-masina-cu-cutie-automata", date="2026-10-31",
        title="Cum se tractează corect o mașină cu cutie automată",
        desc="Tractarea greșită poate distruge o cutie automată în câțiva kilometri. Când e voie cu cablu, când doar pe platformă și ce faci dacă mașina nu iese din P.",
        h1="Cum se tractează corect o mașină cu cutie automată",
        lead="O cutie automată se unge doar când merge motorul, pentru că pompa de ulei e antrenată de motor. Tractată cu roțile motoare pe asfalt, se rotește fără ulei și se poate distruge în câțiva kilometri. Iată regulile de bază.",
        body=f"""
<h2>Regula simplă</h2>
<p><b>Pe platformă, întotdeauna când se poate.</b> Este singura variantă sigură pentru orice cutie automată, DSG, CVT sau 4x4.</p>

<h2>Dacă trebuie totuși tractată cu cablu</h2>
<ul class="dots">
<li>Doar dacă manualul mașinii permite; multe modele (CVT, 4x4, DSG) nu permit deloc</li>
<li>Selectorul în N, contactul pus, ca să nu se blocheze volanul</li>
<li>De obicei maximum 50 km/h și maximum 50 km, conform manualului</li>
<li>La 4x4 și xDrive / quattro / 4Matic: doar pe platformă</li>
</ul>

<h2>Dacă mașina nu iese din P</h2>
<p>Majoritatea mașinilor au o deblocare de urgență a poziției P (un orificiu lângă selector sau o procedură din manual). La cutiile cu frână de parcare electrică sau selector electronic poate fi nevoie de baterie sau de aparat. Nu forța selectorul.</p>

<h2>Dacă mașina ta nu mai pleacă</h2>
<p>Sună-ne la 0734 607 050 sau scrie-ne pe WhatsApp: îți spunem cum s-o aduci în siguranță la atelierul din Băicoi și, dacă ai codul de eroare, îți spunem ce înseamnă. Vezi și {L("cutie-automata-mod-avarie", "ce faci când cutia intră în mod avarie")}.</p>
""",
        faq=[("Pot tracta un DSG cu cablul?", "Pe distanță foarte scurtă și doar dacă manualul permite. Recomandarea noastră e platforma: o tractare greșită poate costa cât o reparație completă."),
             ("Dacă mașina a fost tractată greșit, ce fac?", "Spune-ne la diagnoză. Verificăm uleiul și cutia înainte să o pornești pe drum lung.")],
        related=["probleme-cutie-automata", "cutie-automata-mod-avarie", "reparatii-cutii-automate"],
    ))
    # articole adăugate automat (sarcina programată scrie în ../articole.json)
    import json, os, pathlib
    root = pathlib.Path(os.environ.get("AM_ROOT") or pathlib.Path(__file__).resolve().parent.parent)
    extra = root / "articole.json"
    if extra.exists():
        have = {a["slug"] for a in A}
        for a in json.loads(extra.read_text()):
            if a["slug"] in have:
                continue
            a["faq"] = [tuple(x) for x in a.get("faq", [])]
            A.append(a); have.add(a["slug"])
    A.sort(key=lambda a: a["date"], reverse=True)
    return A
