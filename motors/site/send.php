<?php
/* AutoMatrix Motors – handler pentru formularul de ofertă.
   Trimite cererea pe email. Necesită PHP 7.4+ și funcția mail() activă (standard pe găzduirile cPanel). */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

const TO_EMAIL   = 'service@automatrixmotors.ro';      // unde vin cererile
const FROM_EMAIL = 'no-reply@automatrixmotors.ro';     // trebuie să fie pe domeniul tău
const MIN_SECONDS_BETWEEN = 30;                        // anti-spam per IP

function out(bool $ok, string $err = ''): void { echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $err], JSON_UNESCAPED_UNICODE); exit; }
function clean(string $k, int $max = 200): string {
  $v = trim((string)($_POST[$k] ?? ''));
  $v = str_replace(["\r", "\n"], ' ', $v);
  return mb_substr(strip_tags($v), 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); out(false, 'metodă nepermisă'); }

$host = parse_url($_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '', PHP_URL_HOST) ?: '';
if ($host !== '' && !preg_match('/(^|\.)automatrixmotors\.ro$/i', $host)) { http_response_code(403); out(false, 'origine nepermisă'); }

if (!empty($_POST['website'])) out(true); // honeypot: roboții primesc „ok”, dar nu se trimite nimic

// limitare simplă pe IP, fără cookie-uri
$ipHash = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . 'am-salt');
$lock = sys_get_temp_dir() . '/am_' . $ipHash;
if (is_file($lock) && time() - (int)@filemtime($lock) < MIN_SECONDS_BETWEEN) { http_response_code(429); out(false, 'prea multe cereri, încearcă peste un minut'); }

$d = [
  'Nume'       => clean('nume', 80),
  'Telefon'    => clean('telefon', 30),
  'Localitate' => clean('localitate', 80),
  'Contact'    => clean('contact', 20),
  'Marca'      => clean('marca', 40),
  'Model'      => clean('model', 80),
  'An'         => clean('an', 4),
  'Cutie'      => clean('cutie', 40),
];
$simptome = $_POST['simptome'] ?? [];
if (!is_array($simptome)) $simptome = [$simptome];
$d['Simptome'] = mb_substr(implode(', ', array_map(fn($s) => strip_tags(trim((string)$s)), $simptome)), 0, 300);
$detalii = mb_substr(strip_tags(trim((string)($_POST['detalii'] ?? ''))), 0, 2000);

$tel = preg_replace('/[\s.\-()]/', '', $d['Telefon']);
if ($d['Nume'] === '' || $d['Marca'] === '' || $d['Model'] === '' || $d['Localitate'] === '') out(false, 'câmpuri lipsă');
if (!preg_match('/^(\+?40|0)7\d{8}$/', $tel)) out(false, 'telefon invalid');
if (($_POST['gdpr'] ?? '') !== 'da') out(false, 'lipsește acordul GDPR');

$body = "Cerere nouă de ofertă de pe automatrixmotors.ro\n\n";
foreach ($d as $k => $v) if ($v !== '') $body .= str_pad($k . ':', 12) . $v . "\n";
if ($detalii !== '') $body .= "\nDetalii:\n" . $detalii . "\n";
$wa = preg_replace('/^0/', '40', ltrim($tel, '+'));
$body .= "\nSună: tel:" . $tel . "\nWhatsApp: https://wa.me/" . $wa . "\n";
$body .= "\nAcord GDPR: da, " . date('d.m.Y H:i') . "\n";

$subject = '=?UTF-8?B?' . base64_encode('Cerere ofertă: ' . $d['Marca'] . ' ' . $d['Model'] . ' – ' . $d['Nume']) . '?=';
$headers = implode("\r\n", [
  'From: AutoMatrix Site <' . FROM_EMAIL . '>',
  'MIME-Version: 1.0',
  'Content-Type: text/plain; charset=UTF-8',
  'Content-Transfer-Encoding: 8bit',
  'X-Mailer: AutoMatrix'
]);

$sent = @mail(TO_EMAIL, $subject, $body, $headers, '-f' . FROM_EMAIL);
@touch($lock);
if (!$sent) { http_response_code(500); out(false, 'serverul de email nu a răspuns'); }
out(true);
