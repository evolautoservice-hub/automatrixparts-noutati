# -*- coding: utf-8 -*-
"""City / county landing pages. Each one has its own route, local driving context and FAQ.
The workshop is only in Băicoi: pages never claim a local address."""

PHONE = "0734 607 050"


def city(slug, city, county, km, time, lead, route, local, faq, nav=None):
    return dict(slug=slug, city=city, county=county, km=km, time=time, nav=nav or city, lead=lead, route=route, local=local, faq=faq,
                title=f"Reparații cutii automate {city} | Garanție 24 luni",
                desc=f"Reparații și revizii cutii automate pentru clienți din {city} ({county}): DSG, ZF, Aisin, Mercedes, CVT. Atelier la ~{km} km, garanție 24 luni fără limită de km.")


FAR = """<h2>Cum lucrăm cu clienții care vin de departe</h2>
<ul class="ticks">
<li><b>Programare la oră fixă</b>, online, la telefon sau pe WhatsApp, ca să nu aștepți la atelier</li>
<li><b>Atelierul se deschide la 06:00.</b> Dacă pleci devreme, intri primul la diagnoză</li>
<li><b>Devizul îl primești în scris</b> în ziua în care ajungi, înainte de orice lucrare</li>
<li><b>O revizie se face de obicei în aceeași zi</b>, deci poți pleca acasă cu mașina seara</li>
<li><b>La o reparație completă</b>, de circa 5 zile lucrătoare, îți trimitem poze pe WhatsApp și te sunăm când mașina e gata</li>
</ul>"""

CITIES = [
    city("cutii-automate-ploiesti", "Ploiești", "Prahova", "20", "circa 25 de minute",
         "Atelierul nostru este în Băicoi, la circa 20 km de Ploiești, pe DN1 spre Câmpina. Pentru clienții din Ploiești și din tot județul Prahova suntem cel mai apropiat atelier specializat exclusiv pe cutii automate.",
         "Din Ploiești ieși pe DN1 spre Câmpina și Brașov. După aproximativ 20 km ajungi în Băicoi. Atelierul este pe Str. Înfrățirii nr. 111.",
         """<h2>Atelierul de cutii automate al Prahovei</h2>
<p>Din Ploiești, Câmpina, Băicoi, Breaza, Sinaia, Mizil sau Vălenii de Munte ajungi la noi repede. Lași mașina dimineață, iar pentru o revizie o poți lua de obicei în aceeași zi. Pentru o reparație completă, termenul mediu este de 5 zile lucrătoare și te ținem la curent pe WhatsApp, cu poze.</p>
<p>În oraș găsești multe service-uri generale. O cutie automată cere însă scule speciale, aparate de diagnoză dedicate și experiență pe fiecare tip de cutie. Noi lucrăm aproape exclusiv pe cutii automate, iar asta se vede în garanție: 24 de luni, fără limită de kilometri.</p>""",
         [("Aveți service în Ploiești?", "Atelierul nostru este în Băicoi, Str. Înfrățirii nr. 111, la circa 20 km de Ploiești, pe DN1 spre Câmpina."),
          ("Lucrați și pentru clienți din Câmpina, Sinaia sau Mizil?", "Da. Venim în întâmpinarea clienților din tot județul Prahova. Câmpina e la circa 15 km, Sinaia la circa 45 km."),
          ("Cât durează o revizie dacă vin din Ploiești?", "O revizie se face de obicei în aceeași zi. Cu programare, avem piesele pregătite când ajungi.")],
         nav="Ploiești și Prahova"),
    city("cutii-automate-targoviste", "Târgoviște", "Dâmbovița", "60", "circa o oră",
         "Clienții din Târgoviște și din județul Dâmbovița ajung la atelierul nostru din Băicoi în circa o oră, pe DN72 până la Ploiești și apoi pe DN1 spre Câmpina.",
         "Din Târgoviște mergi pe DN72 spre Ploiești. La intrarea în Ploiești iei DN1 spre Câmpina și Brașov, iar după circa 20 km ajungi în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Pentru clienții din Dâmbovița</h2>
<p>Din Târgoviște, Moreni, Găești, Pucioasa sau Fieni, Băicoi este la o distanță pe care o faci dus-întors în aceeași zi. Pentru o revizie de cutie automată poți veni dimineața și pleca după-amiaza.</p>
<p>Moreni și zona de nord a județului sunt chiar mai aproape: ajungi pe drumuri județene, fără să treci prin Ploiești. Te ghidăm la telefon dacă e prima dată când vii.</p>""",
         [("Cât de departe e atelierul de Târgoviște?", "Circa 60 km, adică în jur de o oră, pe DN72 până la Ploiești și apoi pe DN1 spre Câmpina."),
          ("Pot face revizia cutiei într-o singură zi dacă vin din Târgoviște?", "Da. O revizie se face de obicei în aceeași zi. Fă programare ca să avem piesele pregătite.")]),
    city("cutii-automate-buzau", "Buzău", "Buzău", "95", "în jur de o oră și jumătate",
         "Clienții din Buzău ajung la noi pe DN1B până la Ploiești și apoi pe DN1 spre Câmpina. Atelierul din Băicoi este la circa 95 km, iar pentru reparațiile mari garanția de 24 de luni face drumul să merite.",
         "Din Buzău iei DN1B spre Ploiești. Din Ploiești continui pe DN1 spre Câmpina și Brașov, iar după circa 20 km ajungi în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Pentru clienții din județul Buzău</h2>
<p>Din Buzău, Râmnicu Sărat, Pogoanele sau Nehoiu, DN1B este drumul cel mai simplu spre noi. Mulți clienți din zonă vin pentru cutii DSG și pentru cutiile ZF de pe SUV-uri, unde o reparație corectă și o garanție lungă contează mai mult decât câțiva kilometri.</p>"""
         + FAR,
         [("Cât de departe e atelierul de Buzău?", "Circa 95 km, în jur de o oră și jumătate, pe DN1B până la Ploiești și apoi pe DN1 spre Câmpina."),
          ("Merită să vin din Buzău pentru reparația cutiei?", "Clienții din Buzău vin pentru specializarea noastră pe cutii automate, prețurile afișate și garanția de 24 de luni fără limită de kilometri.")]),
    city("cutii-automate-bucuresti", "București", "București", "80", "în jur de o oră",
         "Clienții din București ajung la noi în aproximativ o oră, pe A3 până la Ploiești și apoi pe DN1 spre Câmpina. Primesc prețuri afișate dinainte și o garanție de 24 de luni, fără limită de kilometri.",
         "Din București iei autostrada A3 spre Ploiești, apoi DN1 spre Câmpina. Băicoi este la circa 80 km de București. Atelierul este pe Str. Înfrățirii nr. 111.",
         """<h2>Traficul din București și cutiile DSG</h2>
<p>Pornirile și opririle dese din trafic sunt cel mai greu regim pentru o cutie cu dublu ambreiaj uscat, ca DSG DQ200. Ambreiajele se încălzesc, iar uzura apare mai devreme: vibrații la plecare, smucituri la manevre, apoi erori. Dacă mergi mult în oraș, merită verificate la timp. Detalii despre <a class="link" href="/reparatie-cutie-dsg">reparația cutiilor DSG</a>.</p>"""
         + FAR,
         [("Cât de departe e atelierul de București?", "Circa 80 km, în jur de o oră pe A3 până la Ploiești și apoi pe DN1 spre Câmpina, în funcție de trafic."),
          ("De ce să vin din București la Băicoi?", "Clienții din București vin la noi pentru specializarea pe cutii automate, pentru prețurile afișate și pentru garanția de 24 de luni fără limită de kilometri, unică în România.")]),
    city("cutii-automate-ilfov", "Ilfov", "Ilfov", "70", "între 50 de minute și o oră",
         "Din Otopeni, Voluntari, Pipera, Corbeanca, Snagov sau Buftea ajungi la atelierul nostru din Băicoi în mai puțin de o oră. Nordul Ilfovului are acces direct pe DN1 și pe A3 spre Ploiești.",
         "Din nordul județului Ilfov iei DN1 sau A3 spre Ploiești, apoi DN1 spre Câmpina. Din Chitila, Buftea sau Mogoșoaia, cel mai rapid ajungi pe DN1A și apoi pe A3. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Pentru clienții din Ilfov</h2>
<p>Mulți clienți din Ilfov fac zilnic naveta spre București, cu multe porniri și opriri pe DN1 și pe centură. Pentru cutiile automate, mai ales pentru DSG și pentru cutiile SUV-urilor, acesta e un regim greu: uleiul se încălzește, iar ambreiajele se uzează mai repede. O revizie la timp costă mult mai puțin decât o reparație.</p>
<p>Pentru că ești deja pe drumul spre Ploiești, ajungi la noi mai repede decât în multe zone din București.</p>"""
         + FAR,
         [("Din ce localități din Ilfov vin clienții?", "Din Otopeni, Voluntari, Pipera, Corbeanca, Snagov, Balotești, Buftea, Chitila și din tot nordul județului."),
          ("Cât durează drumul din Ilfov până la atelier?", "Între 50 de minute și o oră, pe DN1 sau A3 până la Ploiești și apoi pe DN1 spre Câmpina.")]),
    city("cutii-automate-galati", "Galați", "Galați", "220", "în jur de 3 ore",
         "Pentru clienții din Galați, atelierul nostru din Băicoi este la circa 220 km. Mulți vin pentru reparațiile mari de cutii automate, unde garanția de 24 de luni fără limită de kilometri face diferența.",
         "Din Galați mergi pe DN22B până la Brăila, apoi pe DN2B spre Buzău, pe DN1B spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>De ce merită drumul din Galați</h2>
<p>O reparație de cutie automată costă de multe ori mii de lei. Diferența dintre o lucrare făcută corect, cu piese complete și garanție lungă, și una făcută pe jumătate se vede abia după câteva luni. De aceea, pentru reparațiile mari, clienții din Galați aleg un atelier specializat, chiar dacă e mai departe.</p>
<p>Înainte să pleci, trimite-ne pe WhatsApp, la """ + PHONE + """, un video cu simptomul, marca, modelul și anul. Îți spunem dacă problema pare de revizie sau de reparație și cât ar costa, ca să știi la ce să te aștepți.</p>"""
         + FAR,
         [("Merită să vin din Galați pentru reparația cutiei automate?", "Pentru reparațiile mari, da: primești diagnoză clară, preț în scris înainte de lucru și garanție de 24 de luni fără limită de kilometri."),
          ("Pot afla un preț înainte să plec din Galați?", "Da. Trimite-ne pe WhatsApp un video cu simptomul și datele mașinii. Îți dăm o primă estimare, iar prețurile standard sunt toate pe site.")]),
    city("cutii-automate-constanta", "Constanța", "Constanța", "300", "în jur de 3 ore și jumătate",
         "Clienții din Constanța ajung la noi pe A2 și A3, în aproximativ trei ore și jumătate. Vin mai ales pentru reparațiile complete de cutii automate, unde contează garanția de 24 de luni, fără limită de kilometri.",
         "Din Constanța mergi pe autostrada A2 până la București, apoi pe A3 spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111, la circa 300 km.",
         """<h2>Căldura, autostrada și cutia automată</h2>
<p>Drumurile lungi pe A2 la viteză constantă, verile foarte calde de pe litoral și traficul aglomerat din sezon pun uleiul cutiei automate la încercare. Un ulei degradat duce la tremurături la viteză constantă și la uzura convertizorului de cuplu. Dacă mergi des pe autostradă, fă revizia cutiei mai aproape de 60.000 km.</p>
<p>Înainte să pleci, trimite-ne pe WhatsApp, la """ + PHONE + """, un video cu simptomul. Îți spunem ce credem și ce pași urmează.</p>"""
         + FAR,
         [("Merită să vin din Constanța?", "Pentru o reparație completă, da. Primești preț în scris înainte de lucru, poze pe parcurs și garanție de 24 de luni fără limită de kilometri. Pentru o revizie simplă, poți face drumul dus-întors în aceeași zi."),
          ("Cât de departe e atelierul de Constanța?", "Circa 300 km, în jur de trei ore și jumătate pe A2, A3 și DN1.")]),
    city("cutii-automate-braila", "Brăila", "Brăila", "190", "în jur de 2 ore și jumătate",
         "Clienții din Brăila ajung la atelierul nostru din Băicoi pe DN2B prin Buzău și pe DN1B spre Ploiești, în aproximativ două ore și jumătate.",
         "Din Brăila mergi pe DN2B până la Buzău, apoi pe DN1B spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111, la circa 190 km.",
         """<h2>Pentru clienții din Brăila</h2>
<p>Din Brăila, Ianca sau Însurăței, drumul spre noi trece prin Buzău și Ploiești, pe drumuri naționale bune. Mulți clienți combină drumul cu o diagnoză și o revizie în aceeași zi. Pentru reparațiile mari lasă mașina la noi, iar noi îi trimitem poze pe WhatsApp pe parcursul lucrării.</p>"""
         + FAR,
         [("Cât de departe e atelierul de Brăila?", "Circa 190 km, în jur de două ore și jumătate, prin Buzău și Ploiești."),
          ("Pot face diagnoza și revizia în aceeași zi?", "Da, cu programare. Atelierul se deschide la 06:00, iar o revizie se face de obicei în aceeași zi.")]),
    city("cutii-automate-pitesti", "Pitești", "Argeș", "145", "în jur de 2 ore",
         "Clienții din Pitești și din județul Argeș ajung la noi pe DN7 până la Găești și apoi pe DN72, prin Târgoviște, spre Ploiești. Atelierul din Băicoi este la circa 145 km.",
         "Din Pitești mergi pe DN7 spre Găești, apoi pe DN72 prin Târgoviște până la Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Cutiile Renault și Dacia din zona Pitești</h2>
<p>În Argeș circulă multe Renault și Dacia cu cutii automate EDC și AL4. Le cunoaștem bine: revizie, electrovalve AL4, ambreiaje EDC DC4 și DW6. Prețurile pentru aceste lucrări sunt toate pe <a class="link" href="/preturi-cutii-automate">pagina de prețuri</a>.</p>
<p>Lucrăm, la fel de bine, pe DSG, ZF, Aisin și Mercedes, pentru clienții din Pitești, Mioveni, Câmpulung și Curtea de Argeș.</p>"""
         + FAR,
         [("Reparați cutiile EDC și AL4 de pe Renault și Dacia?", "Da. Facem revizii, înlocuim electrovalvele AL4 și ambreiajele EDC DC4 și DW6. Prețurile sunt pe site."),
          ("Cât de departe e atelierul de Pitești?", "Circa 145 km, în jur de două ore, pe DN7, DN72 prin Târgoviște și DN1.")]),
    city("cutii-automate-brasov", "Brașov", "Brașov", "90", "sub două ore",
         "Venim în întâmpinarea clienților din Brașov cu un atelier specializat la circa 90 km, pe Valea Prahovei. Programare fixă, diagnoză în ziua sosirii și garanție de 24 de luni, fără limită de kilometri.",
         "Din Brașov cobori pe DN1, prin Predeal, Sinaia și Comarnic, spre Câmpina. Băicoi este la circa 90 km. Atelierul este pe Str. Înfrățirii nr. 111.",
         """<h2>Drumurile de munte și cutia automată</h2>
<p>Urcările lungi, coborârile cu frâna de motor și traficul de pe Valea Prahovei solicită serios cutia automată. Uleiul se încălzește mai mult decât în mers normal și se degradează mai repede. De aceea, pentru mașinile din zona Brașovului recomandăm revizia cutiei mai aproape de 60.000 km decât de 80.000 km.</p>"""
         + FAR,
         [("Merită să vin din Brașov pentru reparația cutiei?", "Clienții din Brașov vin la noi pentru specializarea pe cutii automate, prețurile afișate și garanția de 24 de luni fără limită de kilometri. Drumul durează în medie sub două ore, pe Valea Prahovei."),
          ("Pot face programare pentru o zi anume?", "Da. Te poți programa online, la telefon sau pe WhatsApp, iar diagnoza o facem în ziua în care ajungi.")]),
    city("cutii-automate-craiova", "Craiova", "Dolj", "265", "în jur de 3 ore și jumătate",
         "Clienții din Craiova și din Oltenia ajung la noi prin Pitești, Găești și Târgoviște. Atelierul din Băicoi este la circa 265 km și lucrează pentru reparațiile mari cu garanție de 24 de luni, fără limită de kilometri.",
         "Din Craiova mergi spre Pitești, apoi pe DN7 până la Găești și pe DN72 prin Târgoviște spre Ploiești. Din Ploiești continui pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Pentru clienții din Oltenia</h2>
<p>Din Craiova, Slatina sau Caracal, drumul e lung, așa că îl merită lucrările importante: reparații complete de cutie, convertizoare, mecatronice și ambreiaje DSG. Pentru acestea primești preț în scris înainte de lucru și garanție de 24 de luni fără limită de kilometri.</p>
<p>Înainte să pleci, trimite-ne pe WhatsApp, la """ + PHONE + """, un video cu simptomul și datele mașinii, ca să ai o estimare înainte de drum.</p>"""
         + FAR,
         [("Merită să vin din Craiova?", "Pentru reparațiile mari, da: diagnoză clară, preț în scris, poze pe parcurs și garanție de 24 de luni fără limită de kilometri."),
          ("Cât de departe e atelierul de Craiova?", "Circa 265 km, în jur de trei ore și jumătate, prin Pitești, Găești și Târgoviște.")]),
]

NEAR = """<h2>Pentru clienții din apropiere</h2>
<ul class="ticks">
<li><b>Revizia o faci în aceeași zi:</b> durează în jur de 3 ore, iar atelierul se deschide la 06:00</li>
<li><b>Diagnoza o programăm la oră fixă</b>, ca să nu aștepți</li>
<li><b>Devizul îl primești în scris</b> înainte de orice lucrare</li>
<li><b>La o reparație completă</b> te ținem la curent pe WhatsApp, cu poze</li>
</ul>"""

CITIES += [
    city("cutii-automate-campina", "Câmpina", "Prahova", "15", "circa 15 minute",
         "Atelierul nostru este în Băicoi, la circa 15 km de Câmpina, pe DN1 spre Ploiești. Pentru clienții din Câmpina, Breaza, Cornu și Comarnic suntem cel mai apropiat atelier specializat pe cutii automate.",
         "Din Câmpina mergi pe DN1 spre Ploiești. După aproximativ 15 km intri în Băicoi; atelierul este pe Str. Înfrățirii nr. 111.",
         """<h2>Cutii automate pe Valea Prahovei</h2>
<p>Drumurile de pe Valea Prahovei, cu urcări lungi spre Breaza și Comarnic și cu trafic de weekend spre munte, solicită mult cutia automată: uleiul se încălzește, iar ambreiajele DSG și convertizorul lucrează din greu. De aceea vedem des, la clienții din zonă, uzura ambreiajelor DQ200 și tremurături de la convertizor la mașinile cu cutie clasică.</p>
<p>Fiind la 15 minute, poți lăsa mașina dimineață la diagnoză și te întorci la birou. Pentru o revizie, o iei de obicei în aceeași zi.</p>"""
         + NEAR,
         [("Aveți service în Câmpina?", "Atelierul este în Băicoi, Str. Înfrățirii nr. 111, la circa 15 km de Câmpina, pe DN1."),
          ("Pot face revizia cutiei automate în aceeași zi?", "Da. O revizie durează în jur de 3 ore. Programează-te dimineața și iei mașina în aceeași zi."),
          ("Cât costă revizia cutiei automate?", "Prețurile pornesc de la 699 lei și sunt toate pe site, cu manoperă și TVA, pe tipuri de cutii.")]),
    city("cutii-automate-sinaia", "Sinaia", "Prahova", "50", "circa 50 de minute",
         "Pentru clienții din Sinaia, Bușteni, Azuga și Predeal, atelierul nostru din Băicoi este la mai puțin de o oră pe DN1. Venim în întâmpinarea celor care nu găsesc pe Valea Prahovei un atelier specializat pe cutii automate.",
         "Din Sinaia mergi pe DN1 spre Câmpina și Ploiești. Treci de Comarnic, Breaza și Câmpina; după circa 50 km ajungi în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Munte, pante și cutia automată</h2>
<p>Coborârile lungi și pantele de la munte pun mare presiune pe cutie: la DSG și Powershift ambreiajele se încălzesc la plecările din rampă, iar la cutiile clasice uleiul se degradează mai repede. Dacă locuiești la munte sau tractezi des, recomandăm revizia cutiei mai des decât spune carnetul de service, în jur de 60.000 km.</p>
<p>Mașinile 4x4 de la munte au în plus cutie de transfer (xDrive, 4Matic, quattro), pe care o verificăm la fiecare diagnoză.</p>"""
         + NEAR,
         [("Cât de departe e atelierul de Sinaia?", "Circa 50 km pe DN1, în jur de 50 de minute în afara orelor de vârf."),
          ("Reparați și cutii de transfer la mașinile 4x4?", "Da. Reparăm cutiile de transfer BMW xDrive, Mercedes 4Matic și altele; prețurile sunt pe site.")]),
    city("cutii-automate-urziceni", "Urziceni", "Ialomița", "80", "în jur de o oră și un sfert",
         "Clienții din Urziceni ajung la atelierul nostru din Băicoi pe DN1D, prin Ploiești, în aproximativ o oră și un sfert.",
         "Din Urziceni mergi pe DN1D spre Ploiești, apoi pe DN1 spre Câmpina. După circa 80 km ajungi în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>De ce vin clienții din Urziceni la Băicoi</h2>
<p>Pentru o cutie automată contează sculele dedicate și experiența pe fiecare tip de cutie. La o oră de drum ai un atelier care lucrează aproape doar pe cutii automate, cu prețuri publice și garanție de 24 de luni, fără limită de kilometri.</p>
<p>Mulți dintre clienții din zonă vin cu mașini care fac drumuri lungi zilnic pe DN1D și DN2. La aceste mașini vedem des uleiul de cutie degradat și tremurăturile de la convertizor la viteză constantă.</p>"""
         + FAR,
         [("Cât de departe e atelierul de Urziceni?", "Circa 80 km, în jur de o oră și un sfert, pe DN1D prin Ploiești."),
          ("Pot afla prețul înainte să vin?", "Da. Toate prețurile standard sunt pe site, iar pentru o estimare ne poți trimite pe WhatsApp un video cu simptomul.")]),
    city("cutii-automate-slobozia", "Slobozia", "Ialomița", "140", "în jur de 2 ore",
         "Pentru clienții din Slobozia și din tot județul Ialomița, atelierul nostru din Băicoi este la circa 140 km, pe DN2A și DN1D prin Urziceni și Ploiești.",
         "Din Slobozia mergi pe DN2A spre Urziceni, apoi pe DN1D spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Reparațiile mari merită făcute o singură dată</h2>
<p>O reparație de cutie automată făcută pe jumătate se întoarce după câteva luni. Clienții din Slobozia vin la noi mai ales pentru reparațiile complete și pentru mecatronicurile DSG, unde contează piesele complete, adaptările corecte și garanția lungă.</p>
<p>Înainte să pleci, trimite-ne pe WhatsApp, la """ + PHONE + """, codul de eroare sau un video cu simptomul. Codul îl poți căuta și în ghidul nostru de coduri de eroare.</p>"""
         + FAR,
         [("Merită să vin din Slobozia?", "Pentru reparațiile mari, da: preț în scris înainte de lucru, poze pe parcurs și garanție de 24 de luni, fără limită de kilometri."),
          ("Cât de departe e atelierul?", "Circa 140 km, în jur de două ore, prin Urziceni și Ploiești.")]),
    city("cutii-automate-ramnicu-sarat", "Râmnicu Sărat", "Buzău", "130", "în jur de o oră și 50 de minute",
         "Clienții din Râmnicu Sărat ajung la atelierul nostru din Băicoi pe DN2 până la Buzău și pe DN1B spre Ploiești, în mai puțin de două ore.",
         "Din Râmnicu Sărat mergi pe DN2 spre Buzău, apoi pe DN1B spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111, la circa 130 km.",
         """<h2>Pe DN2, cu cutie automată</h2>
<p>DN2 e unul dintre cele mai circulate drumuri din țară, cu mult mers în coloană și opriri dese. Pentru cutiile cu dublu ambreiaj uscat (DSG DQ200, Powershift, EDC) asta înseamnă uzură mai rapidă a ambreiajelor. Dacă simți tremurături la plecare sau smucituri în coloană, merită o diagnoză din timp.</p>
<p>Ne poți trimite pe WhatsApp un video cu simptomul înainte de drum, ca să știi la ce să te aștepți.</p>"""
         + FAR,
         [("Cât de departe e atelierul de Râmnicu Sărat?", "Circa 130 km, prin Buzău și Ploiești, în mai puțin de două ore."),
          ("Reparați cutii Powershift și EDC?", "Da. Avem pagini dedicate și prețuri afișate pentru Powershift (Ford, Volvo) și EDC (Renault, Dacia).")]),
    city("cutii-automate-focsani", "Focșani", "Vrancea", "170", "în jur de 2 ore și 20 de minute",
         "Pentru clienții din Focșani și din Vrancea, atelierul nostru din Băicoi este la circa 170 km, pe DN2 și DN1B.",
         "Din Focșani mergi pe DN2 spre Râmnicu Sărat și Buzău, apoi pe DN1B spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Când merită drumul din Vrancea</h2>
<p>Pentru o revizie simplă găsești și mai aproape. Pentru reparațiile complete de cutie automată, pentru mecatronic sau convertizor, clienții din Focșani aleg un atelier specializat pentru diagnoză corectă, preț în scris și garanție de 24 de luni, fără limită de kilometri.</p>
<p>Înainte să pleci, trimite-ne pe WhatsApp, la """ + PHONE + """, marca, modelul, anul și codul de eroare. Îți spunem dacă pare o revizie sau o reparație și ce prețuri se aplică.</p>"""
         + FAR,
         [("Merită să vin din Focșani?", "Pentru reparațiile mari, da. Primești preț în scris înainte de lucru și garanție de 24 de luni, fără limită de kilometri."),
          ("Cât de departe e atelierul?", "Circa 170 km, în jur de 2 ore și 20 de minute, prin Buzău și Ploiești.")]),
    city("cutii-automate-giurgiu", "Giurgiu", "Giurgiu", "145", "în jur de 2 ore",
         "Clienții din Giurgiu ajung la atelierul nostru din Băicoi prin București și pe A3 sau DN1, în aproximativ două ore.",
         "Din Giurgiu mergi pe DN5 spre București, apoi pe A3 sau DN1 spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111, la circa 145 km.",
         """<h2>Ocolești Bucureștiul pe centură</h2>
<p>Drumul trece pe lângă București, așa că pleacă devreme: atelierul se deschide la 06:00 și, dacă ajungi dimineață, intri primul la diagnoză. Pentru o revizie, poți fi înapoi acasă în aceeași zi.</p>
<p>Pentru reparațiile mari ne poți trimite înainte un video cu simptomul, iar prețurile standard le găsești pe site, pe fiecare tip de cutie.</p>"""
         + FAR,
         [("Cât de departe e atelierul de Giurgiu?", "Circa 145 km, în jur de două ore, prin București."),
          ("Pot face revizia dus-întors în aceeași zi?", "Da. Revizia durează în jur de 3 ore; dacă ajungi dimineață, pleci cu mașina în aceeași zi.")]),
    city("cutii-automate-alexandria", "Alexandria", "Teleorman", "170", "în jur de 2 ore și jumătate",
         "Pentru clienții din Alexandria și din Teleorman, atelierul nostru din Băicoi este la circa 170 km, prin București.",
         "Din Alexandria mergi pe DN6 spre București, apoi pe A3 sau DN1 spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>De ce vin clienții din Teleorman</h2>
<p>O cutie automată reparată corect ține ani de zile; una reparată pe jumătate se întoarce după câteva luni. Clienții din Alexandria vin la noi mai ales pentru reparații complete, convertizor și mecatronic, unde contează experiența pe tipul exact de cutie și garanția.</p>
<p>Înainte de drum, trimite-ne pe WhatsApp, la """ + PHONE + """, codul de eroare și datele mașinii, ca să primești o estimare.</p>"""
         + FAR,
         [("Merită să vin din Alexandria?", "Pentru reparațiile mari, da: preț în scris înainte de lucru și garanție de 24 de luni, fără limită de kilometri."),
          ("Cât de departe e atelierul?", "Circa 170 km, în jur de două ore și jumătate, prin București.")]),
    city("cutii-automate-calarasi", "Călărași", "Călărași", "200", "în jur de 2 ore și 40 de minute",
         "Clienții din Călărași ajung la atelierul nostru din Băicoi pe A2 până la București și pe A3 sau DN1 spre Ploiești.",
         "Din Călărași mergi spre A2 și pe autostradă până la București, apoi pe A3 sau DN1 spre Ploiești și pe DN1 spre Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111, la circa 200 km.",
         """<h2>Autostradă, căldură și uleiul cutiei</h2>
<p>Mersul lung pe A2 la viteză constantă și verile foarte calde din Bărăgan îmbătrânesc uleiul cutiei. Primul semn sunt tremurăturile fine între 60 și 100 km/h, de la ambreiajul convertizorului. O revizie făcută la timp previne o reparație de mii de lei.</p>
<p>Înainte să pleci, trimite-ne pe WhatsApp un video cu simptomul și datele mașinii, ca să știi la ce să te aștepți.</p>"""
         + FAR,
         [("Merită să vin din Călărași?", "Pentru reparațiile mari, da. Primești diagnoză clară, preț în scris și garanție de 24 de luni, fără limită de kilometri."),
          ("Cât de departe e atelierul?", "Circa 200 km, în jur de 2 ore și 40 de minute, pe A2 și A3.")]),
    city("cutii-automate-sfantu-gheorghe", "Sfântu Gheorghe", "Covasna", "135", "în jur de 2 ore și un sfert",
         "Pentru clienții din Sfântu Gheorghe și din Covasna, atelierul nostru din Băicoi este la circa 135 km, prin Brașov și pe Valea Prahovei.",
         "Din Sfântu Gheorghe mergi spre Brașov, apoi pe DN1 peste Predeal, prin Sinaia și Câmpina. Atelierul este în Băicoi, pe Str. Înfrățirii nr. 111.",
         """<h2>Iarna, frigul și cutia automată</h2>
<p>Temperaturile scăzute din Covasna fac uleiul cutiei mai vâscos la pornire: schimbările sunt dure în primii kilometri, iar un ulei vechi agravează problema. La mașinile 4x4, frecvente în zonă, verificăm la fiecare diagnoză și cutia de transfer.</p>
<p>Înainte să pleci, trimite-ne pe WhatsApp, la """ + PHONE + """, un video cu simptomul. Drumul peste Predeal poate fi aglomerat în weekend, așa că recomandăm programarea în timpul săptămânii.</p>"""
         + FAR,
         [("Cât de departe e atelierul de Sfântu Gheorghe?", "Circa 135 km, în jur de 2 ore și un sfert, prin Brașov și Predeal."),
          ("Reparați și cutii de transfer 4x4?", "Da. Prețurile pentru cutiile de transfer sunt pe pagina de prețuri.")]),
]
