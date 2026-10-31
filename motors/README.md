# automatrixmotors.ro – sursa site-ului și actualizarea automată

- `build/` – generatorul site-ului (Python, fără dependențe externe). Rulează: `cd build && python3 build.py prod`
- `site2/`, `site/` – resurse (CSS, JS, imagini, politici)
- `articole.json` – articolele adăugate automat de sarcina programată (vezi `INSTRUCTIUNI-ARTICOLE.md`)
- `dist/` – site-ul generat + `manifest.json` (amprente SHA-256)
- `server/deploy-continut.php` – pe server, rulat de cron de 2 ori pe zi: preia din `dist/` doar paginile schimbate și le anunță prin IndexNow

Nu se publică niciodată fișiere .php, .htaccess sau chei prin acest mecanism.
