<?php
/*
 * AutoMatrix Motors – actualizare automată a site-ului din GitHub.
 * Rulează doar din cron (linie de comandă), de 2 ori pe zi:
 *   /usr/local/bin/php /home/omgvzxpk/public_html/deploy-continut.php
 * Descarcă manifest.json din repo, compară amprentele SHA-256 și rescrie doar
 * paginile .html, sitemap.xml și assets/js/main.js care s-au schimbat.
 * Nu atinge niciodată fișiere .php, .htaccess sau fb-config.php.
 * La final anunță paginile schimbate prin IndexNow (Bing, Yandex, Seznam).
 */
if (php_sapi_name() !== 'cli') { http_response_code(404); exit; }

const BASE = 'https://raw.githubusercontent.com/evolautoservice-hub/automatrixparts-noutati/main/motors/dist/';
const SITE = 'https://automatrixmotors.ro';
const INDEXNOW_KEY = 'df86ff09ede0f5fe9303b2c19de9adee';
const ALLOWED = '~^([a-z0-9-]+\.html|sitemap\.xml|assets/js/main\.js)$~';

$root = __DIR__;
$logDir = dirname(__DIR__) . '/.am-cache';
if (!is_dir($logDir)) { @mkdir($logDir, 0750, true); }
$logFile = $logDir . '/deploy-continut.log';

function logm($m) {
    global $logFile;
    file_put_contents($logFile, date('Y-m-d H:i:s') . ' ' . $m . "\n", FILE_APPEND);
}

function fetch($url) {
    $c = curl_init($url);
    curl_setopt_array($c, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_TIMEOUT => 60, CURLOPT_USERAGENT => 'automatrixmotors-deploy/1.0']);
    $r = curl_exec($c);
    $code = curl_getinfo($c, CURLINFO_HTTP_CODE);
    curl_close($c);
    return $code === 200 ? $r : false;
}

$raw = fetch(BASE . 'manifest.json?t=' . time());
$man = $raw ? json_decode($raw, true) : null;
if (!$man || empty($man['files']) || !is_array($man['files'])) {
    logm('EROARE: manifest indisponibil');
    exit(1);
}

$changed = [];
foreach ($man['files'] as $name => $sha) {
    if (!preg_match(ALLOWED, $name) || !preg_match('~^[a-f0-9]{64}$~', $sha)) { continue; }
    $path = $root . '/' . $name;
    if (is_file($path) && hash_file('sha256', $path) === $sha) { continue; }
    $data = fetch(BASE . $name . '?v=' . substr($sha, 0, 12));
    if ($data === false || hash('sha256', $data) !== $sha) {
        logm("EROARE: descărcare sau amprentă greșită pentru $name");
        continue;
    }
    if (!is_dir(dirname($path))) { @mkdir(dirname($path), 0755, true); }
    file_put_contents($path . '.tmp', $data);
    rename($path . '.tmp', $path);
    $changed[] = $name;
}

if (!$changed) { logm('nimic nou (' . ($man['generated'] ?? '?') . ')'); exit(0); }
logm('actualizat: ' . implode(', ', $changed));

// IndexNow pentru paginile schimbate
$urls = [];
foreach ($changed as $n) {
    if (substr($n, -5) !== '.html' || $n === '404.html') { continue; }
    $slug = substr($n, 0, -5);
    $urls[] = SITE . ($slug === 'index' ? '/' : '/' . $slug);
}
if ($urls) {
    $body = json_encode(['host' => 'automatrixmotors.ro', 'key' => INDEXNOW_KEY,
        'keyLocation' => SITE . '/' . INDEXNOW_KEY . '.txt', 'urlList' => array_slice($urls, 0, 1000)]);
    $c = curl_init('https://api.indexnow.org/indexnow');
    curl_setopt_array($c, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30, CURLOPT_HTTPHEADER => ['Content-Type: application/json; charset=utf-8']]);
    curl_exec($c);
    logm('IndexNow: HTTP ' . curl_getinfo($c, CURLINFO_HTTP_CODE) . ' pentru ' . count($urls) . ' adrese');
    curl_close($c);
}
