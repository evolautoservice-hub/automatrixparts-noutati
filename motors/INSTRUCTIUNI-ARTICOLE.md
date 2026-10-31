# Articol nou pentru automatrixmotors.ro (sarcina programată: duminică, marți, joi după articolul AutoMatrix Parts)

Scopul: un articol nou, original, în română, care răspunde la o întrebare reală a șoferilor despre cutiile automate
și duce cititorul spre o pagină de servicii, de prețuri sau de coduri de eroare de pe site.

## Pași
1. `cd motors` și citește `articole.json` și `build/articles.py` (articolele existente). Nu repeta un subiect deja tratat.
2. Alege subiectul:
   a) **Prima opțiune: noutățile de pe automatrixparts.ro.** Citește `../news.json` (articolele magazinului AutoMatrix Parts, cele mai noi primele).
      Ia cel mai nou articol al cărui `id` NU apare deja ca `parts_id` în `articole.json`. Scrie pe aceeași temă o versiune
      NOUĂ pentru service: ce înseamnă știrea pentru un șofer din România, ce simptome să urmărească, ce întreținere sau reparație
      e implicată și când să vină la atelier. NU copia și NU reformula frază cu frază textul de pe automatrixparts.ro
      (același text pe două site-uri e conținut duplicat și Google îl penalizează): structură proprie, titlu diferit, alt unghi.
      Folosește doar faptele din articolul Parts și din sursele lui (câmpul `sources`); poți deschide sursele cu WebFetch.
      Pune `"parts_id": "<id-ul articolului din news.json>"` și `"sources": [{"title": "...", "url": "https://..."}]` (aceleași surse).
      Poți adăuga la final o frază că piesele pentru cutii automate se găsesc la magazinul partener
      `<a class="link" href="https://automatrixparts.ro/" target="_blank" rel="noopener">automatrixparts.ro</a>`.
      Dacă știrea nu are nicio legătură practică cu șoferii români (ex. un model care nu se vinde în România), sari la b).
   b) **Altfel**, alege primul subiect netratat din lista de mai jos (sau unul echivalent; fără `parts_id`, `sources` opțional):
3. Scrie articolul ca obiect JSON și ADAUGĂ-L la sfârșitul listei din `articole.json`:
   `{"slug": "...", "date": "AAAA-LL-ZZ", "title": "... (max 60 caractere)", "desc": "... (140-160 caractere)", "h1": "...",
     "lead": "...", "body": "<h2>...</h2><p>...</p>...", "faq": [["întrebare", "răspuns"], ["...", "..."]],
     "related": ["slug-pagina-site", "...", "..."], "parts_id": "... (doar la 2a)", "sources": [ ... ] (opțional)}`
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
