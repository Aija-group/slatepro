/* SlatePro – NordicHost cPanel "AI App Hosting" -palvelin.
 *
 * Tarjoilee valmiiksi rakennetun sivuston site/-kansiosta ja käsittelee yhteydenottolomakkeen (POST /lahetys).
 * Sivusto rakennetaan omalla koneella (python3 build.py) ja site/ commitoidaan repoon – palvelimella ei tarvita Pythonia.
 *
 * Ympäristömuuttujat (cPanel → sovelluksen asetukset):
 *   PORT            palvelimen antama portti (asettuu yleensä automaattisesti)
 *   MAIL_TO         mihin lomakeviestit tulevat (oletus slateprooy@gmail.com)
 *   MAIL_FROM       lähettäjä, saman domainin osoite (oletus no-reply@slatepro.fi)
 *   SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
 *                   cPanelin sähköpostitilin SMTP-tiedot. Jos puuttuvat, käytetään palvelimen sendmailia.
 *   MAIL_DRYRUN=1   testaus: viestiä ei lähetetä
 */
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { URLSearchParams } = require('url');

const ROOT = path.join(__dirname, 'site');
const PORT = process.env.PORT || 3000;
const MAIL_TO = process.env.MAIL_TO || 'slateprooy@gmail.com';
const MAIL_FROM = process.env.MAIL_FROM || 'no-reply@slatepro.fi';
const SITE_NAME = 'SlatePro Oy';
const THANKS = '/kiitos/';
const ERROR = '/yhteystiedot/?virhe=1';
const FIELDS = [['nimi', 'Nimi'], ['puhelin', 'Puhelin'], ['email', 'Sähköposti'], ['aihe', 'Paikkakunta'], ['viesti', 'Viesti'], ['sivu', 'Lähetetty sivulta']];
const REQUIRED = ['nimi', 'puhelin', 'email', 'viesti'];

const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon', '.woff2': 'font/woff2', '.pdf': 'application/pdf',
};
const SECURITY = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Frame-Options': 'SAMEORIGIN',
};

let transport = null;
function mailer() {
  if (transport) return transport;
  const nodemailer = require('nodemailer');
  if (process.env.MAIL_DRYRUN) return (transport = nodemailer.createTransport({ jsonTransport: true }));
  transport = process.env.SMTP_HOST
    ? nodemailer.createTransport({
        host: process.env.SMTP_HOST, port: +(process.env.SMTP_PORT || 465), secure: +(process.env.SMTP_PORT || 465) === 465,
        auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
      })
    : nodemailer.createTransport({ sendmail: true, newline: 'unix', path: '/usr/sbin/sendmail' });
  return transport;
}

function redirect(res, to, code = 303) {
  res.writeHead(code, { Location: to, ...SECURITY });
  res.end();
}

function send(res, status, file, extra = {}) {
  const ext = path.extname(file).toLowerCase();
  const headers = { 'Content-Type': TYPES[ext] || 'application/octet-stream', ...SECURITY, ...extra };
  if (ext === '.html') headers['Cache-Control'] = 'no-cache';
  else if (file.includes(`${path.sep}img${path.sep}`)) headers['Cache-Control'] = 'public, max-age=31536000, immutable';
  else headers['Cache-Control'] = 'public, max-age=86400';
  res.writeHead(status, headers);
  fs.createReadStream(file).pipe(res);
}

function notFound(res) {
  send(res, 404, path.join(ROOT, '404.html'));
}

function serveStatic(req, res, url) {
  let rel;
  try { rel = decodeURIComponent(url.pathname); } catch { return notFound(res); }
  const file = path.normalize(path.join(ROOT, rel));
  if (!file.startsWith(ROOT)) return notFound(res);
  fs.stat(file, (err, st) => {
    if (!err && st.isFile()) return send(res, 200, file);
    if (!err && st.isDirectory()) {
      if (!rel.endsWith('/')) return redirect(res, rel + '/' + url.search, 301);
      const index = path.join(file, 'index.html');
      return fs.stat(index, (e2, s2) => (!e2 && s2.isFile() ? send(res, 200, index) : notFound(res)));
    }
    notFound(res);
  });
}

function clean(s) {
  return String(s || '').replace(/[\r\n]+/g, ' ').trim();
}

function handleForm(req, res) {
  let body = '';
  req.on('data', (c) => {
    body += c;
    if (body.length > 50000) req.destroy();
  });
  req.on('end', async () => {
    const f = Object.fromEntries(new URLSearchParams(body));
    // Roskapostisuoja: piilokenttä täytetty tai lomake täytetty alle 3 sekunnissa → hiljainen "kiitos"
    if (f['bot-field']) return redirect(res, THANKS);
    const ts = parseInt(f.ts, 10);
    if (ts && Date.now() / 1000 - ts < 3) return redirect(res, THANKS);
    if (REQUIRED.some((k) => !String(f[k] || '').trim())) return redirect(res, ERROR);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clean(f.email))) return redirect(res, ERROR);

    const text = FIELDS.filter(([k]) => String(f[k] || '').trim())
      .map(([k, label]) => `${label}:\n${String(f[k]).trim()}`).join('\n\n');
    try {
      await mailer().sendMail({
        from: `"${SITE_NAME} – verkkosivu" <${MAIL_FROM}>`,
        to: MAIL_TO,
        replyTo: clean(f.email),
        subject: `Yhteydenotto verkkosivulta: ${clean(f.nimi)}`,
        text: `${text}\n\n—\nLähetetty ${SITE_NAME}n verkkosivun lomakkeella.`,
      });
      redirect(res, THANKS);
    } catch (e) {
      console.error('Lomakkeen lähetys epäonnistui:', e.message);
      redirect(res, ERROR);
    }
  });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  // www → juuri (yksi kanoninen osoite)
  const host = req.headers.host || '';
  if (host.startsWith('www.')) return redirect(res, `https://${host.slice(4)}${req.url}`, 301);
  if (req.method === 'POST' && url.pathname === '/lahetys') return handleForm(req, res);
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { Allow: 'GET, HEAD', ...SECURITY });
    return res.end();
  }
  serveStatic(req, res, url);
});

server.listen(PORT, () => console.log(`SlatePro käynnissä portissa ${PORT}`));
