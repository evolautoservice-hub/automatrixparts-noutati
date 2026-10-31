<?php
/* AutoMatrix Motors – pagina „Lucrări efectuate”.
   Preia ultimele postări de pe pagina de Facebook prin Graph API, salvează pozele local
   și le afișează în designul site-ului. Fără token configurat afișează varianta de rezervă din HTML.
   Configurare: copiază fb-config.sample.php ca fb-config.php și completează page_id și token. */
declare(strict_types=1);
date_default_timezone_set('Europe/Bucharest');

$tpl = @file_get_contents(__DIR__ . '/lucrari-efectuate.html');
if ($tpl === false) { http_response_code(500); exit('Pagina lipsește.'); }
$cfg = is_file(__DIR__ . '/fb-config.php') ? (require __DIR__ . '/fb-config.php') : [];

$posts = am_posts(is_array($cfg) ? $cfg : []);
if ($posts) {
    $tpl = preg_replace('/<!--FEED-START-->.*<!--FEED-END-->/s', '<div class="works">' . am_render($posts) . '</div>', $tpl, 1);
}
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=600');
echo $tpl;

function am_get(string $url, int $timeout = 12): ?string {
    if (function_exists('curl_init')) {
        $c = curl_init($url);
        curl_setopt_array($c, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true, CURLOPT_TIMEOUT => $timeout, CURLOPT_USERAGENT => 'AutoMatrix-Site/1.0']);
        $r = curl_exec($c); $code = (int)curl_getinfo($c, CURLINFO_HTTP_CODE); curl_close($c);
        return ($r !== false && $code >= 200 && $code < 300) ? (string)$r : null;
    }
    $r = @file_get_contents($url, false, stream_context_create(['http' => ['timeout' => $timeout]]));
    return $r === false ? null : $r;
}

function am_posts(array $cfg): array {
    $pageId = trim((string)($cfg['page_id'] ?? '')); $token = trim((string)($cfg['access_token'] ?? ''));
    $ver = (string)($cfg['graph_version'] ?? 'v26.0'); $ttl = (int)($cfg['cache_minutes'] ?? 60) * 60; $max = (int)($cfg['max_posts'] ?? 24);
    $cacheDir = dirname(__DIR__) . '/.am-cache'; if (!is_dir($cacheDir)) @mkdir($cacheDir, 0750, true);
    if (!is_writable($cacheDir)) $cacheDir = sys_get_temp_dir();
    $cacheFile = $cacheDir . '/fb-feed.json';
    $cached = is_file($cacheFile) ? json_decode((string)file_get_contents($cacheFile), true) : null;
    if (is_array($cached) && time() - (int)($cached['ts'] ?? 0) < $ttl) return $cached['posts'] ?? [];
    if ($pageId === '' || $token === '') return is_array($cached) ? ($cached['posts'] ?? []) : [];

    $url = "https://graph.facebook.com/{$ver}/" . rawurlencode($pageId) . '/posts?' . http_build_query([
        'fields' => 'id,message,created_time,permalink_url,full_picture,attachments{media_type,type,url,target}', 'limit' => 50, 'access_token' => $token]);
    $raw = am_get($url);
    $data = $raw ? json_decode($raw, true) : null;
    if (!is_array($data) || !isset($data['data'])) {               // API error: keep showing the last good feed
        am_alert($cacheDir, is_array($data) ? (string)($data['error']['message'] ?? 'răspuns necunoscut') : 'Facebook nu a răspuns');
        if (is_array($cached)) { $cached['ts'] = time() - $ttl + 600; @file_put_contents($cacheFile, json_encode($cached)); return $cached['posts'] ?? []; }
        return [];
    }
    $imgDir = __DIR__ . '/assets/fb'; if (!is_dir($imgDir)) @mkdir($imgDir, 0755, true);
    $out = []; $keep = [];
    foreach ($data['data'] as $p) {
        if (empty($p['full_picture']) || trim((string)($p['message'] ?? '')) === '') continue;
        $name = substr(sha1((string)$p['id']), 0, 16) . '.jpg';
        $path = $imgDir . '/' . $name;
        if (!is_file($path)) { $bin = am_get((string)$p['full_picture'], 20); if ($bin === null) continue; am_save_img($bin, $path); }
        if (!is_file($path)) continue;
        $keep[] = $name;
        $video = '';
        foreach (($p['attachments']['data'] ?? []) as $a) {
            $kind = strtolower((string)($a['media_type'] ?? '') . ' ' . (string)($a['type'] ?? ''));
            if (strpos($kind, 'video') !== false) { $video = (string)($a['target']['url'] ?? ($a['url'] ?? ($p['permalink_url'] ?? ''))); break; }
        }
        $out[] = ['msg' => (string)$p['message'], 'time' => (string)$p['created_time'], 'link' => (string)($p['permalink_url'] ?? ''), 'img' => '/assets/fb/' . $name, 'video' => $video];
        if (count($out) >= $max) break;
    }
    foreach (glob($imgDir . '/*.jpg') ?: [] as $f) if (!in_array(basename($f), $keep, true)) @unlink($f);
    @file_put_contents($cacheFile, json_encode(['ts' => time(), 'posts' => $out], JSON_UNESCAPED_UNICODE));
    return $out;
}

function am_alert(string $dir, string $why): void {   // max one email per day when Facebook stops answering
    $f = $dir . '/fb-alert.txt';
    if (is_file($f) && time() - (int)@filemtime($f) < 86400) return;
    @touch($f);
    $body = "Pagina Lucrări efectuate de pe automatrixmotors.ro nu mai poate prelua postările de pe Facebook.\n\nMotiv: $why\n\n"
          . "Pe site rămân afișate ultimele postări salvate. Cel mai probabil trebuie generat un token nou pentru fb-config.php.\n";
    @mail('service@automatrixmotors.ro', '=?UTF-8?B?' . base64_encode('Atenție: Lucrări efectuate nu se mai actualizează') . '?=', $body,
          "From: AutoMatrix Site <no-reply@automatrixmotors.ro>\r\nContent-Type: text/plain; charset=UTF-8", '-fno-reply@automatrixmotors.ro');
}

function am_save_img(string $bin, string $path): void {
    if (function_exists('imagecreatefromstring') && ($im = @imagecreatefromstring($bin))) {
        $w = imagesx($im); $h = imagesy($im); $nw = min(900, $w); $nh = (int)round($h * $nw / $w);
        $dst = imagecreatetruecolor($nw, $nh); imagecopyresampled($dst, $im, 0, 0, 0, 0, $nw, $nh, $w, $h);
        imagejpeg($dst, $path, 80); imagedestroy($dst); imagedestroy($im); return;
    }
    @file_put_contents($path, $bin);
}

function am_tags(string $t): array {
    $map = ['dsg' => '/\b(dsg|dq\s?200|dq\s?250|dq\s?381|dq\s?500|s[\s-]?tronic|0b5)\b/i', 'zf' => '/\b(zf|[5689]\s?hp\d*)\b/i',
            'mercedes' => '/\b(mercedes|[579]g[\s-]?tronic|722\.\d|725\.0)\b/i', 'aisin' => '/\baisin\b/i',
            'cvt' => '/\b(cvt|multitronic|jatco)\b/i', 'motor' => '/\b(motor|motoare|chiulas[aă]|distribu[tț]ie|turbo)\b/iu'];
    $out = []; foreach ($map as $k => $rx) if (preg_match($rx, $t)) $out[] = $k; return $out;
}

function am_render(array $posts): string {
    $luni = ['ian.', 'feb.', 'mar.', 'apr.', 'mai', 'iun.', 'iul.', 'aug.', 'sept.', 'oct.', 'nov.', 'dec.'];
    $labels = ['dsg' => 'DSG / S tronic', 'zf' => 'ZF', 'mercedes' => 'Mercedes', 'aisin' => 'Aisin', 'cvt' => 'CVT', 'motor' => 'Motor'];
    $h = '';
    foreach ($posts as $p) {
        $ts = strtotime($p['time']) ?: time();
        $date = date('j', $ts) . ' ' . $luni[(int)date('n', $ts) - 1] . ' ' . date('Y', $ts);
        $msg = trim(preg_replace('/\s+/u', ' ', $p['msg']));
        $ex = mb_strlen($msg) > 240 ? rtrim(mb_substr($msg, 0, 240)) . '…' : $msg;
        $tags = am_tags($msg);
        $alt = 'Lucrare AutoMatrix Motors: ' . mb_substr($msg, 0, 90);
        $e = fn($s) => htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
        $chips = $tags ? '<div class="work-tags">' . implode('', array_map(fn($t) => '<span>' . $labels[$t] . '</span>', $tags)) . '</div>' : '';
        $h .= '<article class="work" data-tags="' . implode(' ', $tags) . (!empty($p['video']) ? ' video' : '') . '">'
            . (!empty($p['video'])
                ? '<div class="work-img is-video" data-video="' . $e($p['video']) . '"><img src="' . $e($p['img']) . '" alt="' . $e($alt) . '" loading="lazy" decoding="async"><button class="work-play" type="button" aria-label="Redă video-ul"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5v14l11-7z"/></svg></button><span class="work-vlabel">Video</span></div>'
                : '<a class="work-img" href="' . $e($p['link']) . '" target="_blank" rel="noopener"><img src="' . $e($p['img']) . '" alt="' . $e($alt) . '" loading="lazy" decoding="async"></a>')
            . '<div class="work-b"><time datetime="' . date('Y-m-d', $ts) . '">' . $date . '</time><p>' . $e($ex) . '</p>' . $chips
            . '<a class="link" href="' . $e($p['link']) . '" target="_blank" rel="noopener">Vezi postarea pe Facebook</a></div></article>';
    }
    return $h;
}
