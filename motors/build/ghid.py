# -*- coding: utf-8 -*-
"""Ghid video: probleme tipice ale cutiilor automate, explicate de mecanicii AutoMatrix Motors.
Fiecare pagină pornește de la un clip publicat pe pagina de Facebook a atelierului (03.11.2026).
videos: (link reel Facebook, fișier miniatură din /assets/img/ghid/, lățime, înălțime, data publicării)"""

HUB = "ghid-video-cutii-automate"

GHID = [
dict(slug="ghid-dsg-dq250-pilitura-ulei",
     title="DSG DQ250: pilitura din ulei și mecatronicul | Ghid video",
     desc="DSG DQ250 cu 6 trepte rezistă mult, dar are un punct slab: pilitura din ulei. Semnele, intervalul de schimb și ce se întâmplă dacă îl amâni.",
     h1="DSG DQ250: e chiar indestructibilă?",
     lead="DQ250, cutia DSG cu 6 trepte și ambreiaje umede de pe VW, Audi, Skoda și Seat, e una dintre cele mai rezistente cutii automate. Are însă un punct slab pe care îl vedem des în atelier: pilitura metalică din ulei.",
     fam="DSG", box="coduri-eroare-dsg-dq250",
     videos=[("https://www.facebook.com/reel/1617899446689148/", "dq250-pilitura-ulei.jpg", 900, 1600, "2026-10-29")],
     body="""<h2>De unde vine pilitura</h2>
<p>La DQ250, ambreiajele lucrează în baie de ulei. Fiecare cuplare lasă în ulei particule metalice foarte fine, iar același ulei trece și prin mecatronic, unde comandă electrovalvele. Cât timp uleiul e schimbat la timp, filtrul și uleiul nou țin particulele sub control.</p>
<p>Când schimbul se amână mult peste 60.000 km, pilitura se adună în electrovalve. Acestea nu mai reglează presiunea corect, iar ambreiajele încep să patineze. Un ambreiaj care patinează se încălzește și se uzează mult mai repede, iar uzura produce și mai multă pilitură.</p>
<h2>Semnele pe care le vedem la clienți</h2>
<ul class="dots"><li>dimineața, la rece, cutia intră greu în D</li><li>un șoc la trecerea din treapta 3 în 2, când încetinești</li><li>o întârziere la plecarea de pe loc, ca și cum cutia „se gândește”</li></ul>
<p>Niciunul dintre aceste semne nu înseamnă automat o reparație mare. De multe ori, un schimb de ulei și filtru făcut corect, urmat de adaptări, rezolvă problema dacă e prinsă devreme.</p>
<h2>Ce recomandăm</h2>
<p>Schimbul de ulei și filtru DSG la intervalul corect, cu ulei conform specificației producătorului și cu adaptările făcute pe calculator după schimb. Costă mult mai puțin decât o reparație de mecatronic sau de ambreiaje. Vezi <a class="link" href="/revizie-cutie-automata">ce include revizia cutiei</a> și <a class="link" href="/coduri-eroare-dsg-dq250">codurile de eroare DQ250</a>.</p>""",
     faq=[("La câți km se schimbă uleiul la DSG DQ250?", "Recomandăm schimbul de ulei și filtru la cel mult 60.000 km. La mers mult în oraș sau cu remorcă, chiar mai des."),
          ("Cutia intră greu în D dimineața. E grav?", "Nu neapărat, dar e un semn timpuriu. O verificare a uleiului și a adaptărilor îți spune dacă ajunge o revizie.")]),

dict(slug="ghid-zf-8hp-baie-ulei-plastic",
     title="ZF 8HP: baia de ulei din plastic și pierderile de ulei",
     desc="Cutia ZF 8HP are baia de ulei din plastic, care se poate deforma în timp. Cum pierzi ulei fără să vezi pete și ce se întâmplă cu ambreiajele.",
     h1="ZF 8HP: punctul sensibil al unei cutii foarte bune",
     lead="ZF 8HP, cutia automată cu 8 trepte de pe BMW, Audi, Jeep, Land Rover și multe alte mărci, e una dintre cele mai bune transmisii construite vreodată. Are totuși un detaliu de care mulți proprietari nu știu: baia de ulei e din plastic.",
     fam="ZF", box="coduri-eroare-zf-8hp",
     videos=[("https://www.facebook.com/reel/1115109714260686/", "zf-8hp-baie-plastic.jpg", 900, 1600, "2026-10-25")],
     body="""<h2>De ce contează baia din plastic</h2>
<p>La ZF 8HP, baia de ulei e din plastic și are filtrul integrat. Cu anii, căldura de la motor și de la cutie deformează ușor plasticul și garnitura. Rezultatul e o pierdere lentă de ulei, de câțiva mililitri pe zi, care de multe ori nu lasă nicio pată vizibilă în parcare.</p>
<p>Nivelul scade încet. Cât timp mai e ulei suficient, cutia merge normal. Când nivelul coboară sub limită, la turații mari unele ambreiaje interne nu mai primesc presiunea necesară, patinează și se ard.</p>
<h2>Semnul care nu trebuie ignorat</h2>
<p>Dacă mașina patinează între treptele superioare, de exemplu între 5 și 6, sau turația crește fără ca mașina să accelereze, dauna a început deja. Din acel moment, fiecare kilometru crește costul reparației.</p>
<h2>Ce recomandăm</h2>
<p>O revizie preventivă la timp, cu baia de ulei nouă (care include filtrul), ulei conform specificației ZF și nivelul reglat la temperatură, cum cere manualul. Verificarea nivelului la ZF 8HP nu se face cu joja, ci pe calculator, la o temperatură anume. Vezi <a class="link" href="/reparatie-cutie-zf">reparația și revizia cutiilor ZF</a> și <a class="link" href="/coduri-eroare-zf-8hp">codurile de eroare ZF 8HP</a>.</p>""",
     faq=[("Cum verific nivelul uleiului la ZF 8HP?", "Nu are jojă. Nivelul se verifică pe elevator, cu mașina pornită și uleiul la temperatura indicată de producător, citită pe calculator."),
          ("Se schimbă doar uleiul sau și baia?", "La ZF 8HP filtrul e integrat în baia de ulei, deci la revizie se schimbă baia cu filtru și garnitură, plus uleiul.")]),

dict(slug="ghid-dsg-dq381-pompa-auxiliara",
     title="DSG DQ381: mod avarie și pompa auxiliară de ulei",
     desc="Mod avarie brusc pe Golf, Passat, Kodiaq sau Octavia cu DSG DQ381? De multe ori e pompa electrică auxiliară, nu toată cutia. Ce verificăm.",
     h1="DSG DQ381: mod avarie brusc și pompa auxiliară",
     lead="DQ381 este cutia DSG cu 7 trepte și ambreiaje umede de pe VW, Skoda, Seat, Cupra și Audi fabricate după 2017. Consumă puțin și schimbă foarte bine, dar în atelier vedem des aceeași problemă: pompa electrică auxiliară de ulei.",
     fam="DSG", box="coduri-eroare-dsg-dq381",
     videos=[("https://www.facebook.com/reel/1835390007491203/", "dq381-mod-avarie.jpg", 900, 1600, "2026-10-12"),
             ("https://www.facebook.com/reel/1580545880026466/", "dq381-problema-ascunsa.jpg", 900, 1600, "2026-10-23")],
     body="""<h2>Ce face pompa auxiliară</h2>
<p>Pe lângă pompa mecanică, DQ381 are o pompă electrică de ulei care menține presiunea în cutie, de exemplu când motorul se oprește la semafor prin sistemul start-stop. Dacă pompa cedează sau nu mai etanșează bine, presiunea din cutie nu se mai formează la timp.</p>
<h2>Cum se manifestă</h2>
<ul class="dots"><li>mesajul „Transmission emergency run” sau „Gearbox malfunction” în bord</li><li>pierderea bruscă a tracțiunii, uneori chiar în depășire</li><li>la început, o ezitare foarte mică între treptele pare</li></ul>
<p>Mulți șoferi cred că o mașină nouă nu are nevoie de întreținere la cutie. La DQ381, uleiul lăsat mult peste intervalul recomandat accelerează uzura pompei și a pachetului de ambreiaj.</p>
<h2>Ce facem în atelier</h2>
<p>Citim erorile și presiunile din cutie. De cele mai multe ori nu e nevoie de o cutie nouă: înlocuim pompa defectă, schimbăm uleiul și filtrele, apoi facem adaptările și actualizarea software. Dacă rămâi în avarie pe drum, nu forța mașina: o platformă costă mai puțin decât o reparație mai mare. Vezi <a class="link" href="/coduri-eroare-dsg-dq381">codurile de eroare DQ381</a> și <a class="link" href="/reparatie-cutie-dsg">reparația cutiilor DSG</a>.</p>""",
     faq=[("Pe ce mașini e montată cutia DQ381?", "Pe multe modele VAG după 2017 cu motoare mai puternice: VW Passat B8, Tiguan, Golf 7.5 și 8, Skoda Kodiaq, Superb, Octavia, Seat și Cupra."),
          ("Trebuie schimbată toată cutia dacă intră în avarie?", "De cele mai multe ori nu. Des e pompa auxiliară sau un senzor. Diagnoza arată exact ce s-a defectat.")]),

dict(slug="ghid-dsg-dq200-ulei-mecatronic",
     title="DSG DQ200: uleiul din mecatronic se schimbă? | Ghid",
     desc="DSG DQ200 are ambreiaje uscate, dar mecatronicul are ulei separat. De ce se degradează, ce simptome dă și de ce merită schimbat la timp.",
     h1="DSG DQ200: mitul cutiei „uscate” fără întreținere",
     lead="DQ200, cutia DSG cu 7 trepte de pe Golf, Octavia, Leon, Polo sau A3, are ambreiaje uscate. De aici vine un mit periculos: că nu are nevoie de întreținere. Mecatronicul ei are însă un circuit de ulei separat.",
     fam="DSG", box="coduri-eroare-dsg-dq200",
     videos=[("https://www.facebook.com/reel/1399885368795446/", "dq200-ulei-mecatronic.jpg", 900, 1600, "2026-10-22")],
     body="""<h2>Două uleiuri, nu niciunul</h2>
<p>La DQ200, ambreiajele lucrează uscat, dar cutia are ulei pentru pinioane și un circuit hidraulic separat pentru mecatronic, care acționează ambreiajele și schimbă treptele. Uleiul din mecatronic lucrează la presiune mare și se încălzește mult.</p>
<p>În timp, acest ulei adună particule fine de metal și se degradează. Un ulei îmbătrânit, cu particule, uzează electrovalvele și pompa mecatronicului și poate afecta placa electronică. Așa apar smuciturile în treapta 1 și 2 și, mai târziu, codurile de presiune, de tipul P189C.</p>
<h2>Ce recomandăm</h2>
<p>Producătorul nu cere un interval fix pentru acest ulei, dar din experiența atelierului recomandăm verificarea și schimbul lui în jur de 60.000 km, împreună cu adaptările de ambreiaj. E o lucrare mică în comparație cu o reparație de mecatronic.</p>
<p>Dacă DSG-ul tău smucește deja în treapta a doua, citește <a class="link" href="/dsg-smuceste-la-plecare">de ce smucește DSG-ul la plecare</a> și vezi <a class="link" href="/reparatie-mecatronic-dsg">reparația mecatronicului DSG</a>.</p>""",
     faq=[("DQ200 are nevoie de schimb de ulei?", "Da. Ambreiajele sunt uscate, dar mecatronicul are ulei hidraulic propriu, iar cutia are ulei pentru pinioane."),
          ("Ce se întâmplă dacă nu schimb uleiul din mecatronic?", "Crește riscul de uzură a electrovalvelor și a pompei, de erori de presiune și de smucituri. Reparația mecatronicului costă mult mai mult decât schimbul.")]),

dict(slug="ghid-dsg-dq200-trafic-tremura",
     title="DSG DQ200 în trafic: tremurat la plecare și uzură",
     desc="DQ200 tremură la semafor sau sare din 1 în 2? Cum îți uzează traficul bară la bară ambreiajele și ce semne arată că e timpul de o verificare.",
     h1="DSG DQ200 în trafic: tremuratul la plecare",
     lead="Cel mai des, DQ200 ajunge la noi pentru tremurat la plecarea de pe loc. Cauza principală e uzura ambreiajului dublu uscat, accelerată de mersul bară la bară.",
     fam="DSG", box="coduri-eroare-dsg-dq200",
     videos=[("https://www.facebook.com/reel/1649226176540880/", "dq200-tremura-plecare.jpg", 900, 1600, "2026-10-20"),
             ("https://www.facebook.com/reel/1093930199918881/", "dq200-trafic.jpg", 900, 1600, "2026-10-21")],
     body="""<h2>De ce îl uzează traficul</h2>
<p>La o cutie automată clasică, convertizorul de cuplu absoarbe plecările de pe loc. La DQ200, ambreiajul uscat trebuie să patineze controlat la fiecare plecare și la fiecare târâit în coloană. În traficul bară la bară, ambreiajul lucrează aproape continuu și se încălzește, iar uzura vine mult mai repede.</p>
<h2>Semnele uzurii</h2>
<ul class="dots"><li>un tremurat la plecarea de la semafor</li><li>trecerea bruscă, „sărită”, din treapta 1 în 2</li><li>mai târziu, mesajul de avarie a cutiei și mașina care nu mai pleacă</li></ul>
<p>Un ambreiaj foarte uzat cere presiuni din ce în ce mai mari din mecatronic, iar asta poate afecta și blocul hidraulic. Ce era o reparație de ambreiaj devine o reparație de ambreiaj plus mecatronic.</p>
<h2>Cum îți protejezi cutia</h2>
<p>În coloană, lasă spațiu în față și înaintează mai rar, în loc să te târăști continuu. La opriri mai lungi, ține frâna fermă, ca ambreiajul să se decupleze complet. Iar la primele tremurături, fă o diagnoză a valorilor de adaptare: îți arată cât mai are ambreiajul. Vezi și <a class="link" href="/coduri-eroare-dsg-dq200">codurile de eroare DQ200</a>.</p>""",
     faq=[("Pe ce mașini e DQ200?", "Pe multe modele VW, Skoda, Seat și Audi cu motoare mici și medii: Golf, Polo, Octavia, Fabia, Leon, Ibiza, A1, A3 și altele."),
          ("Tremuratul la plecare înseamnă ambreiaj nou?", "Nu întotdeauna. Uneori ajută adaptările sau o actualizare software. Diagnoza valorilor de uzură arată sigur.")]),

dict(slug="ghid-s-tronic-dl382-schimb-ulei",
     title="S tronic DL382: schimbul de ulei făcut greșit | Ghid",
     desc="S tronic DL382 de pe Audi A4 B9, A6 C8 și Q5 are două circuite de ulei separate. De ce un schimb făcut greșit poate bloca cutia.",
     h1="S tronic DL382: greșeala de la schimbul de ulei",
     lead="DL382 este cutia S tronic cu 7 trepte de pe Audi A4 B9, A5, A6 C8 și Q5 fabricate după 2015–2016. La ea, un schimb de ulei făcut greșit poate face mai mult rău decât niciun schimb.",
     fam="S tronic", box="coduri-eroare-s-tronic-dl382",
     videos=[("https://www.facebook.com/reel/1965719264097283/", "dl382-schimb-ulei.jpg", 900, 1600, "2026-10-19")],
     body="""<h2>Două circuite, două uleiuri</h2>
<p>DL382 are două circuite de ulei complet separate: unul hidraulic, pentru mecatronic și ambreiaje, și unul mecanic, pentru pinioane și diferențial. Fiecare are uleiul lui, cu specificație proprie, și procedura lui de umplere.</p>
<p>Dacă la schimb se golește un compartiment și se umple greșit celălalt, unul dintre circuite rămâne cu prea puțin ulei sau cu un ulei nepotrivit. Circuitul hidraulic fără fluidul corect pierde presiune, acumulatorul hidraulic se poate deteriora, iar cutia începe să smucească, mai ales la decelerare, din treapta 2 în 1.</p>
<h2>Cum se face corect</h2>
<p>Schimbul la DL382 se face cu uleiurile specificate pentru fiecare circuit, cu nivelul verificat la temperatura cerută și cu adaptările făcute pe calculator la final. Nu e o lucrare pentru o mașină de schimb ulei sau pentru o procedură „universală”.</p>
<p>Noi lucrăm după manualul de reparații al producătorului cutiei. Vezi <a class="link" href="/coduri-eroare-s-tronic-dl382">codurile de eroare DL382</a> și <a class="link" href="/reparatie-cutie-automata-audi">reparația cutiilor automate Audi</a>.</p>""",
     faq=[("Pe ce Audi e montată cutia DL382?", "Pe A4 B9, A5, A6 C8, A7, Q5 și alte modele cu motor longitudinal, fabricate după 2015–2016."),
          ("Câte uleiuri are cutia DL382?", "Două: unul pentru circuitul hidraulic al mecatronicului și ambreiajelor și unul pentru partea mecanică.")]),

dict(slug="ghid-dsg-dq500-trepte-pare",
     title="DSG DQ500: dispar treptele pare, erori P1735 și P1736",
     desc="DSG DQ500 de pe Transporter, Tiguan sau RS3 pierde treptele 2, 4, 6 și marșarierul? Erorile P1735 și P1736 și ce înseamnă pentru ambreiaje.",
     h1="DSG DQ500: când dispar treptele pare",
     lead="DQ500 este cea mai puternică dintre cutiile DSG cu 7 trepte, montată pe VW Transporter T5 și T6, Tiguan BiTDI, Audi RS3 și TT RS. Rezistă la cupluri mari, dar are un punct sensibil: senzorii de presiune din mecatronic.",
     fam="DSG", box="reparatie-cutie-dsg",
     videos=[("https://www.facebook.com/reel/1122910400711794/", "dq500-trepte-pare.jpg", 900, 1600, "2026-10-18")],
     body="""<h2>Ce se întâmplă</h2>
<p>Mecatronicul DQ500 măsoară presiunea pe fiecare ambreiaj cu senzori dedicați. Șocurile termice repetate, de exemplu la un Transporter încărcat sau la o mașină condusă sportiv, pot afecta acești senzori. Când calculatorul nu mai citește corect presiunea pe un ambreiaj, se protejează: dezactivează treptele de pe acel ambreiaj.</p>
<p>Simptomul tipic: dispar treptele pare, 2, 4 și 6, împreună cu marșarierul, apare martorul cutiei în bord, iar în memorie găsim erori de tipul P1735 sau P1736.</p>
<h2>De ce nu trebuie să continui drumul</h2>
<p>Cu o jumătate de cutie, mașina se mișcă, dar ambreiajul rămas lucrează în condiții pentru care nu e făcut. Fiecare kilometru crește riscul de a arde ambreiajele, iar reparația se scumpește mult.</p>
<h2>Ce facem</h2>
<p>Nu e nevoie de o cutie nouă. Identificăm senzorul defect, îl înlocuim, recalibrăm mecatronicul și verificăm starea ambreiajelor. Vezi <a class="link" href="/reparatie-cutie-dsg">reparația cutiilor DSG</a> și <a class="link" href="/reparatie-mecatronic-dsg">reparația mecatronicului</a>.</p>""",
     faq=[("Ce înseamnă erorile P1735 și P1736 la DQ500?", "Sunt legate de senzorii de presiune ai ambreiajelor din mecatronic. Calculatorul nu mai poate controla corect presiunea și dezactivează o parte din trepte."),
          ("Pot merge până la atelier fără treptele pare?", "Doar pe distanță scurtă și încet. Pe distanțe mari, folosește o platformă.")]),

dict(slug="ghid-s-tronic-0b5-gearbox-malfunction",
     title="S tronic 0B5 (DL501): mesajul Gearbox malfunction",
     desc="„Gearbox malfunction: you can continue driving” pe Audi A4, A5, A6, Q5 cu S tronic 0B5? De ce nu e bine să continui și ce reparăm.",
     h1="S tronic 0B5: când bordul spune că poți continua",
     lead="Pe Audi A4, A5, A6, A7 și Q5 din generațiile B8 și C7, cutia S tronic cu 7 trepte 0B5 (DL501) afișează uneori „Gearbox malfunction: you can continue driving”. Mesajul e liniștitor, dar realitatea din cutie de obicei nu e.",
     fam="S tronic", box="coduri-eroare-s-tronic-0b5",
     videos=[("https://www.facebook.com/reel/1106426218411627/", "s-tronic-0b5-malfunction.jpg", 900, 1600, "2026-10-16")],
     body="""<h2>Ce înseamnă mesajul</h2>
<p>Când calculatorul cutiei detectează o problemă pe unul dintre ambreiaje sau în mecatronic, trece cutia într-un mod de rezervă: folosește doar o parte din trepte, ca să poți ajunge acasă. De aici textul „you can continue driving”. Cutia nu e în regulă, doar te lasă să ajungi la service.</p>
<h2>Ce se strică dacă mergi mult așa</h2>
<p>În modul de rezervă, piesele rămase lucrează peste limită. Ambreiajele K1 și K2 se încălzesc, mecatronicul lucrează la presiuni greșite, iar o problemă inițial mică, de exemplu un cablaj intern deteriorat de căldură sau o electrovalvă uzată, ajunge la ambreiaje arse și piese mecanice afectate.</p>
<h2>Ce reparăm</h2>
<p>Prinsă devreme, problema se rezolvă de obicei în mecatronic: refacem cablajul intern și înlocuim electrovalvele uzate, apoi facem adaptările. Așa eviți o recondiționare completă a cutiei. Vezi <a class="link" href="/coduri-eroare-s-tronic-0b5">codurile de eroare 0B5</a> și <a class="link" href="/reparatie-cutie-automata-audi">reparația cutiilor Audi</a>.</p>""",
     faq=[("Pot conduce cu „Gearbox malfunction” aprins?", "Doar până la cel mai apropiat atelier, liniștit. Cu cât mergi mai mult, cu atât crește riscul de daune mari."),
          ("Ce înseamnă 0B5 și DL501?", "Sunt două denumiri pentru aceeași cutie S tronic cu 7 trepte, montată longitudinal pe Audi.")]),

dict(slug="ghid-dsg-hurait-decelerare-rulmenti",
     title="Huruit la decelerare la DSG: rulmenții cutiei | Ghid",
     desc="Auzi un hârâit metalic când iei piciorul de pe accelerație, la DSG DQ500 sau DQ381? Des sunt rulmenții axului secundar. Ce riști și ce facem.",
     h1="Huruit metalic la decelerare la cutiile DSG",
     lead="Un zgomot specific pe care îl auzim des la DSG-urile DQ500 și DQ381 de pe VW, Audi, Skoda și Seat: iei piciorul de pe accelerație și se aude un hârâit metalic sub schimbător.",
     fam="DSG", box="reparatie-cutie-dsg",
     videos=[("https://www.facebook.com/reel/1425338249784802/", "dsg-hurait-rulmenti.jpg", 900, 1600, "2026-10-15")],
     body="""<h2>De unde vine zgomotul</h2>
<p>De cele mai multe ori, zgomotul vine de la rulmenții axului secundar. Suprafața lor durificată începe să se exfolieze, din cauza uleiului neschimbat sau a cuplului mare transmis ani la rând. Bilele încep să ruleze pe o suprafață deteriorată, iar zgomotul se aude mai ales la decelerare, când sarcina pe rulment se schimbă.</p>
<h2>Ce riști</h2>
<p>Un rulment degradat continuă să se uzeze, iar particulele de metal ajung în ulei, deci și în mecatronic. Dacă rulmentul cedează complet în mers, poate distruge pinioane, arbori sau chiar carcasa cutiei. Atunci reparația devine o recondiționare completă.</p>
<h2>Ce facem</h2>
<p>Demontăm cutia, o desfacem, înlocuim rulmenții afectați și verificăm restul componentelor: pinioane, sincroane, ambreiaje. Curățăm cutia de particule, schimbăm uleiul și filtrul și facem adaptările. Prinsă la timp, problema rămâne o reparație de rulmenți. Vezi <a class="link" href="/reparatie-cutie-dsg">reparația cutiilor DSG</a>.</p>""",
     faq=[("Huruitul la decelerare poate fi de la altceva?", "Da, de exemplu de la diferențial, rulmenții de roată sau volanta. O probă de drum și o verificare pe elevator lămuresc sursa."),
          ("Pot amâna reparația?", "Nu recomandăm. Un rulment degradat se uzează repede, iar pilitura afectează și mecatronicul.")]),

dict(slug="ghid-audi-0ck-volanta-masa-dubla",
     title="Țăcănit la relanti la Audi B9 cu cutia 0CK: volanta",
     desc="Țăcănit metalic la relanti la Audi A4/A5 B9 cu S tronic 0CK? Înainte să schimbi distribuția, verifică volanta cu masă dublă.",
     h1="Audi B9 cu S tronic 0CK: țăcănitul de la relanti",
     lead="Audi A4 și A5 B9 cu cutia S tronic 0CK (DL382, în varianta Ultra) fac uneori un țăcănit metalic la relanti. Mulți proprietari primesc recomandarea să schimbe distribuția, când cauza e în altă parte.",
     fam="S tronic", box="coduri-eroare-s-tronic-dl382",
     videos=[("https://www.facebook.com/reel/1759200988644319/", "audi-0ck-volanta.jpg", 900, 1600, "2026-10-14")],
     body="""<h2>Volanta cu masă dublă</h2>
<p>Între motor și cutia 0CK lucrează o volantă cu masă dublă, care preia vibrațiile motorului. În timp, arcurile ei interne se uzează, iar volanta capătă joc. La relanti, jocul se aude ca un țăcănit metalic ritmic, care poate semăna cu un zgomot de distribuție.</p>
<h2>De ce contează diagnosticul corect</h2>
<p>Dacă schimbi distribuția și zgomotul rămâne, ai plătit o lucrare scumpă degeaba. Iar dacă volanta e lăsată să se uzeze în continuare, se poate rupe și poate deteriora carcasa din aluminiu a cutiei.</p>
<h2>Ce verificăm</h2>
<p>Ascultăm zgomotul pe elevator, verificăm jocul volantei și starea distribuției și îți spunem exact sursa înainte de orice lucrare. Nu schimbăm piese pe ghicite. Vezi <a class="link" href="/reparatie-cutie-automata-audi">reparația cutiilor automate Audi</a> și <a class="link" href="/coduri-eroare-s-tronic-dl382">codurile de eroare DL382</a>.</p>""",
     faq=[("Cum deosebesc volanta de distribuție?", "Zgomotul de volantă se schimbă de obicei la apăsarea frânei sau la schimbarea poziției selectorului. Diagnoza pe elevator confirmă sigur."),
          ("Volanta se schimbă cu cutia jos?", "Da. Cutia se demontează, deci e momentul potrivit să verificăm și ambreiajele și uleiul.")]),

dict(slug="ghid-zf-8hp-shudder-convertizor",
     title="ZF 8HP: tremurat la drum întins, convertizorul (BMW)",
     desc="Îți „dansează” acul turometrului la viteză constantă pe BMW cu ZF 8HP? Des e convertizorul de cuplu care patinează. Simptome și ce facem.",
     h1="ZF 8HP: tremuratul la drum întins",
     lead="Mulți proprietari de BMW cu cutie ZF 8HP observă că acul turometrului „dansează” ușor la drum întins, iar mașina tremură fin. Pare de la motor, dar de cele mai multe ori e convertizorul de cuplu.",
     fam="ZF", box="coduri-eroare-zf-8hp",
     videos=[("https://www.facebook.com/reel/1578545280968515/", "zf-8hp-shudder.jpg", 900, 1600, "2026-10-13")],
     body="""<h2>Ce este „shudder”-ul</h2>
<p>La viteză constantă, ZF 8HP blochează convertizorul de cuplu cu un ambreiaj intern, ca să nu piardă energie. Când garnitura acestui ambreiaj se uzează sau uleiul s-a degradat, ambreiajul nu mai cuplează curat și patinează ușor. Se simte ca o vibrație fină, iar turația oscilează cu câteva zeci de rotații.</p>
<h2>De ce nu e bine să aștepți</h2>
<p>Convertizorul care patinează produce căldură și particule care ajung în ulei și apoi în blocul hidraulic. Ce începe ca o problemă de convertizor poate deveni o problemă de bloc de valve și de ambreiaje interne.</p>
<h2>Ce facem</h2>
<p>Facem proba de drum și citim pe calculator diferența de turație a convertizorului. Dacă e uzat, îl recondiționăm, apoi schimbăm uleiul și baia cu filtru. Am explicat fenomenul și în articolul despre <a class="link" href="/masina-tremura-intre-60-si-100-km-h">mașina care tremură între 60 și 100 km/h</a>. Vezi și <a class="link" href="/reconditionare-convertizor-cuplu">recondiționarea convertizorului de cuplu</a>.</p>""",
     faq=[("Cum știu că e convertizorul și nu motorul?", "Vibrația apare la viteză constantă, cu ușoare oscilații ale turației, și dispare de obicei la accelerare sau la decuplare. Diagnoza pe calculator confirmă."),
          ("Se poate repara convertizorul sau trebuie înlocuit?", "Se poate recondiționa: îl desfacem, înlocuim garniturile și etanșările, îl sudăm și îl echilibrăm.")]),

dict(slug="ghid-cost-reparatie-garantie",
     title="De ce costă mult reparația cutiei automate | Garanție",
     desc="De ce o reparație de cutie ZF, DSG sau S tronic costă mult și de ce unele service-uri dau doar 3 luni garanție. Ce să ceri înainte de reparație.",
     h1="De ce costă o reparație de cutie automată și ce garanție să ceri",
     lead="Două întrebări pe care le auzim zilnic: de ce costă atât o reparație de cutie automată și de ce unele service-uri dau doar 3 luni garanție. Răspunsul e același: modul în care se face lucrarea.",
     fam="General", box="preturi-cutii-automate",
     videos=[("https://www.facebook.com/reel/1852662359062236/", "cost-reparatie.jpg", 900, 1600, "2026-10-27"),
             ("https://www.facebook.com/reel/1434885378828476/", "garantie-3-luni.jpg", 900, 1600, "2026-11-01")],
     body="""<h2>Ce intră într-o reparație corectă</h2>
<p>O cutie ZF 8HP, un DSG sau un S tronic modern nu se repară schimbând piesa care „pare” defectă. Reparația corectă începe cu o diagnoză dedicată, continuă cu desfacerea completă a cutiei, măsurarea fiecărei componente și înlocuirea tuturor pieselor uzate, nu doar a celei care a cedat. La final urmează strângerile la cuplu, după valorile din manualul de fabrică, adaptările pe calculator și proba de drum.</p>
<h2>De ce apare garanția de 3 luni</h2>
<p>O garanție scurtă spune de obicei ceva despre lucrare. Când o cutie e reparată în grabă, fără proceduri și fără să fie verificate toate piesele, defectul revine. Iar de multe ori revine după ce expiră garanția.</p>
<p>Noi dăm <b>24 de luni garanție, fără limită de kilometri</b>, pentru că lucrăm după manualul de reparații al producătorului cutiei, cu cheie dinamometrică și cu piese din seturi complete. Când știi ce ai făcut, nu-ți e frică să garantezi.</p>
<h2>Ce să ceri înainte de reparație</h2>
<ul class="dots"><li>devizul în scris, înainte de orice lucrare</li><li>lista pieselor care se înlocuiesc</li><li>garanția în scris: durată, kilometri, ce acoperă</li><li>termenul de execuție</li></ul>
<p>Toate prețurile noastre sunt publice: vezi <a class="link" href="/preturi-cutii-automate">lista de prețuri pe tipuri de cutii</a>.</p>""",
     faq=[("Ce acoperă garanția de 24 de luni?", "Piesele și manopera reparației cutiei automate, în condițiile din certificatul de garanție, fără limită de kilometri."),
          ("Pot afla prețul înainte să vin?", "Da. Prețurile standard sunt pe site, iar prețul exact pentru mașina ta îl primești în scris după diagnoză.")]),
]

# miniaturile vin din cache-ul feed-ului de Facebook al site-ului (/assets/fb/)
THUMB_SRC = {
    "dq250-pilitura-ulei.jpg": "94a4273a2d15723b.jpg", "zf-8hp-baie-plastic.jpg": "c79b7e84170fec09.jpg",
    "dq381-mod-avarie.jpg": "e7b92c44ca33b2e6.jpg", "dq381-problema-ascunsa.jpg": "573fd3edb95d868f.jpg",
    "dq200-ulei-mecatronic.jpg": "fed9f7815e3cde55.jpg", "dq200-tremura-plecare.jpg": "47f4ed56bd62d4ef.jpg",
    "dq200-trafic.jpg": "4a33d535a09ba0b0.jpg", "dl382-schimb-ulei.jpg": "424e5279056c9bb4.jpg",
    "dq500-trepte-pare.jpg": "d1ca24408f4f93fa.jpg", "s-tronic-0b5-malfunction.jpg": "3d4f81f75897a056.jpg",
    "dsg-hurait-rulmenti.jpg": "ac01671b077a5a2f.jpg", "audi-0ck-volanta.jpg": "e60096c9af6feb24.jpg",
    "zf-8hp-shudder.jpg": "3a83097dcae99026.jpg", "cost-reparatie.jpg": "bb1f97842a3a5940.jpg",
    "garantie-3-luni.jpg": "88ce86d0467fd1df.jpg",
}
