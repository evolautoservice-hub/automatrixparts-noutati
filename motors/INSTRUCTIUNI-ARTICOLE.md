# Articol nou pentru automatrixmotors.ro (sarcina programată)

Scopul: un articol nou, original, în română, care răspunde la o întrebare reală a șoferilor despre cutiile automate
și duce cititorul spre o pagină de servicii, de prețuri sau de coduri de eroare de pe site.

## Pași
1. `cd motors` și citește `articole.json` și `build/articles.py` (articolele existente). Nu repeta un subiect deja tratat.
2. Alege UN subiect nou din lista de mai jos (primul netratat) sau unul echivalent:
   - DQ200 P17BF / P189C: ce înseamnă și cât costă (link la /coduri-eroare-dsg-dq200)
   - Cutia ZF 8HP: semne că trebuie revizie (link /reparatie-cutie-zf)
   - Mercedes 7G-Tronic placa conductoare: simptome și reparație (link /reparatie-cutie-mercedes)
   - Renault EDC tremură la plecare (link /reparatie-cutie-edc)
   - Audi S tronic 0B5: senzorul G676 (link /coduri-eroare-s-tronic-0b5)
   - Multitronic CVT: merită reparată? (link /reparatie-cutie-cvt)
   - Aisin 09G: șoc din 2 în 3 (link /reparatie-cutie-aisin)
   - DSG DQ381: senzorii de presiune contrafăcuți (link /coduri-eroare-dsg-dq381)
   - Cutie automată și LPG / motor modificat: ce trebuie știut
   - Ce verifici la o mașină second-hand cu cutie automată
   - Uleiul Motul pentru cutii automate: ce specificație îți trebuie
   - Iarna și cutia automată: pornirea la rece
   - Powershift MPS6 pe Volvo și Ford Mondeo: revizia la 60.000 km
   - Volanta cu masă dublă la DSG și S tronic: simptome
   - Cutia de transfer xDrive / 4Matic: când se repară
   - De ce garanția fără limită de kilometri contează
3. Scrie articolul ca obiect JSON și ADAUGĂ-L la sfârșitul listei din `articole.json`:
   `{"slug": "...", "date": "AAAA-LL-ZZ", "title": "... (max 60 caractere)", "desc": "... (140-160 caractere)", "h1": "...",
     "lead": "...", "body": "<h2>...</h2><p>...</p>...", "faq": [["întrebare", "răspuns"], ["...", "..."]],
     "related": ["slug-pagina-site", "...", "..."]}`
   - `slug`: litere mici, cifre, cratime, fără diacritice; unic.
   - `body`: 450–750 de cuvinte, HTML simplu (`<h2>`, `<p>`, `<ul class="dots"><li>`, `<b>`), cu cel puțin 2 linkuri interne
     de forma `<a class="link" href="/slug">text</a>` spre pagini care există în `dist/` (verifică numele fișierului `slug.html`).
   - Prețuri: doar valori reale din `build/rv_prices.json` prin catalog (rulează `python3 -c "from catalog import CATALOG"` în `build/`
     și caută lucrarea) sau din pagina `dist/preturi-cutii-automate.html`. Nu inventa prețuri, ani de experiență, statistici sau recenzii.
   - Ton: clar, practic, fără exagerări. Diacritice corecte (ș, ț cu virgulă). Fără liniuță lungă de dialog ca separator.
   - Menționează natural garanția de 24 de luni fără limită de kilometri și că prețul exact se dă în scris după diagnoză.
   - Nu copia texte de pe alte site-uri. Informația tehnică trebuie să fie corectă; dacă nu ești sigur de un detaliu, nu-l scrie.
   - `related`: 3 sluguri existente (pagini de servicii, coduri, prețuri sau alte articole).
4. Rulează `cd build && python3 build.py prod`. Trebuie să se termine fără erori și să existe `dist/<slug>.html` și `dist/manifest.json`.
5. Commit doar fișierele din `motors/` (articole.json și dist/) cu mesajul `Motors: articol <slug>` și push pe `main`
   (dacă push-ul e respins, `git pull --rebase` și încearcă din nou).
Serverul preia automat pagina nouă în maximum 12 ore și o anunță motoarelor de căutare.
