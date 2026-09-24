# -*- coding: utf-8 -*-
"""Staattisen SlatePro-sivuston generaattori.

    python3 build.py                 -> site/ NordicHostiin (Node, server.js) + ../slatepro-nordichost.zip
    HOSTING=webhotelli python3 build.py -> tavallinen webhotelli (PHP-lomake + .htaccess)
    HOSTING=netlify python3 build.py -> demo Netlifyyn (noindex, data-netlify, "Sivustoehdotus") + ../slatepro-netlify.zip
    python3 build.py --preview       -> kuten yllä, mutta ei zipiä

Tekstit: content.py. Tyylit: src/style.css. Toiminnallisuus: src/app.js. Vaatii Pillow-kirjaston.
"""
import json
import os
import shutil
import sys
import zipfile

from PIL import Image, ImageDraw, ImageFont, ImageOps

from content import (
    AREAS, AUDIENCES, BEFORE_AFTER, BEFORE_RENO, BIG_CHANGE, COMPANY, FAQ, GALLERY, HERO, KOTITALOUS, NAV,
    PROBLEMS, PROCESS, SERVICE, SERVICES, WHY, wa,
)
os.environ.setdefault("HOSTING", "nordichost")  # oletus: NordicHost (sopimus 9/2026)
from hosting import HOSTING, form_attrs, hidden_fields, write_host_files

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
SRC = os.path.join(ROOT, "src")
BASE_URL = f"https://{COMPANY['domain']}"
DEMO = HOSTING == "netlify"
TEL = f"tel:{COMPANY['phone_intl']}"


def esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


ICONS = {
    "phone": '<path d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v4a2 2 0 0 1-2 2C9.5 21 3 14.5 3 6a2 2 0 0 1 1-2Z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "pin": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "x": '<path d="M7 7l10 10M17 7 7 17"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.8-3 8-7 9-4-1-7-4.2-7-9V6l7-3Z"/><path d="M9 12l2 2 4-4.2"/>',
    "grid": '<rect x="3.5" y="3.5" width="17" height="17" rx="1.5"/><path d="M3.5 9.2h17M3.5 14.8h17M9.2 3.5v17M14.8 3.5v17"/>',
    "drop": '<path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z"/><path d="M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5"/>',
    "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "camera": '<path d="M4 8h3l2-2.5h6L17 8h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "house": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M9.5 15.5l5-5M10 11h.01M14 15h.01"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "lr": '<path d="M9 7 4 12l5 5M15 7l5 5-5 5"/>',
}
WA_ICON = ('<svg class="wa-ico" viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3C8.8 3 3 8.7 3 15.8c0 '
           '2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.4c-2.1 0-4.1-.6-5.9-1.7l-.4-.3'
           '-3.8 1.2 1.2-3.7-.3-.4a10.4 10.4 0 0 1-1.7-5.7C5.1 9.9 10 5.2 16 5.2s10.9 4.7 10.9 10.6S22 26.4 16 26.4zm6-7.9c-.3-.2'
           '-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7'
           'l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7s1.2 3.2 1.4 '
           '3.4c.2.2 2.4 3.6 5.7 5 .8.4 1.4.6 1.9.7.8.2 1.5.2 2.1.1.6-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>')


def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


# ---------------------------------------------------------------------------
# Kuvat
# ---------------------------------------------------------------------------
IMG_SRC = {}  # nimi -> lähdetiedosto (src/kuvat: optimoidut lähteet; alkuperäiset _materiaali/, ei gitissä)
for f in os.listdir(os.path.join(SRC, "kuvat")):
    if f.endswith(".jpg"):
        IMG_SRC[f[:-4]] = os.path.join(SRC, "kuvat", f)

IMG_OUT = os.path.join(SITE, "img")
IMG_DIMS = {}
IMG_WS = {}
WIDTHS = (640, 1100, 1800)


def build_images():
    os.makedirs(IMG_OUT, exist_ok=True)
    for name, path in IMG_SRC.items():
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        IMG_DIMS[name] = im.size
        ws = [w for w in WIDTHS if w < im.width] + ([im.width] if im.width < WIDTHS[-1] else [WIDTHS[-1]])
        IMG_WS[name] = ws
        for w in ws:
            out = os.path.join(IMG_OUT, f"{name}-{w}.webp")
            if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(path):
                continue
            r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            r.save(out, "WEBP", quality=80, method=6)


def img(name, alt, sizes="100vw", cls="", eager=False):
    w0, h0 = IMG_DIMS[name]
    ws = IMG_WS[name]
    srcset = ", ".join(f"/img/{name}-{w}.webp {w}w" for w in ws)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/img/{name}-{ws[min(1, len(ws) - 1)]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w0}" height="{h0}" alt="{esc(alt)}" {load}>')


# ---------------------------------------------------------------------------
# Yhteiset palat
# ---------------------------------------------------------------------------

def btn_wa(label="Lähetä kuva WhatsAppiin", text=None, cls="btn btn-wa"):
    href = wa(text) if text else wa()
    return f'<a class="{cls}" href="{esc(href)}" target="_blank" rel="noopener" data-track="whatsapp">{WA_ICON}<span>{label}</span></a>'


def btn_tel(cls="btn btn-ghost"):
    return f'<a class="{cls}" href="{TEL}" data-track="puhelu">{icon("phone")}<span>{COMPANY["phone"]}</span></a>'


def logo_html():
    return (f'<a class="brand" href="/" aria-label="SlatePro – etusivu">'
            f'<img src="/img/logo.png" width="537" height="197" alt="SlatePro – Puhtaat saumat. Uusi ilme."></a>')


def header(current):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{n["href"]}"{cur if current == n["href"] else ""}>{n["label"]}</a>' for n in NAV)
    return f'''<header class="hdr" id="top">
  <div class="hdr-in">
    {logo_html()}
    <nav class="nav" id="nav" aria-label="Päävalikko">{links}
      <div class="nav-cta">{btn_tel("btn btn-ghost")}{btn_wa("WhatsApp")}</div>
    </nav>
    <div class="hdr-cta">
      <a class="hdr-tel" href="{TEL}" data-track="puhelu">{icon("phone")}<span>{COMPANY["phone"]}</span></a>
      {btn_wa("WhatsApp", cls="btn btn-wa btn-sm")}
    </div>
    <button class="burger" aria-label="Avaa valikko" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>'''


def footer():
    svc = "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    areas = ", ".join(AREAS[:8])
    demo = ('<p class="demo-note">Sivustoehdotus – Äijä Group. Tämä on esikatseluversio.</p>' if DEMO else "")
    return f'''<footer class="ftr">
  <div class="wrap ftr-grid">
    <div class="ftr-brand">
      <img src="/img/logo.png" width="537" height="197" alt="SlatePro" loading="lazy">
      <p>Märkätilojen silikonien ja laattasaumojen uusinta koko Pirkanmaalla.</p>
      {btn_wa("Lähetä kuva WhatsAppiin")}
    </div>
    <div><h3>Palvelut</h3><ul>{svc}<li><a href="/kotitalousvahennys/">Kotitalousvähennys</a></li></ul></div>
    <div><h3>Toimialue</h3><p>{areas} ja <a href="/toimialue/">koko Pirkanmaa</a>.</p></div>
    <div><h3>Yhteystiedot</h3>
      <ul class="ftr-contact">
        <li>{icon("phone")}<a href="{TEL}">{COMPANY["phone"]}</a></li>
        <li>{icon("mail")}<a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a></li>
        <li>{icon("pin")}<span>{COMPANY["area"]}</span></li>
      </ul>
      <p class="ftr-person">{COMPANY["name"]} · {COMPANY["contact"]}</p>
    </div>
  </div>
  <div class="wrap ftr-bottom"><span>© 2026 {COMPANY["name"]} · {COMPANY["slogan"]}</span><a href="/tietosuoja/">Tietosuojaseloste</a></div>
  {demo}
</footer>
<div class="mbar" aria-label="Pikayhteys">
  <a href="{TEL}" class="mbar-tel" data-track="puhelu">{icon("phone")}<span>Soita</span></a>
  <a href="{esc(wa())}" class="mbar-wa" target="_blank" rel="noopener" data-track="whatsapp">{WA_ICON}<span>Lähetä kuva WhatsAppiin</span></a>
</div>
<a class="wa-float" href="{esc(wa())}" target="_blank" rel="noopener" aria-label="Lähetä viesti WhatsAppissa" data-track="whatsapp">{WA_ICON}<span class="wa-float-tip">Lähetä kuva – saat arvion</span></a>'''


def org_schema():
    return {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
        "@id": BASE_URL + "/#yritys", "name": COMPANY["name"], "alternateName": "SlatePro",
        "slogan": COMPANY["slogan"], "url": BASE_URL + "/", "telephone": COMPANY["phone_intl"],
        "email": COMPANY["email"], "logo": BASE_URL + "/img/logo.png", "image": BASE_URL + "/img/og.jpg",
        "founder": {"@type": "Person", "name": COMPANY["contact"]},
        "address": {"@type": "PostalAddress", "addressRegion": "Pirkanmaa", "addressCountry": "FI"},
        "areaServed": [{"@type": "AdministrativeArea", "name": "Pirkanmaa"}] + [{"@type": "City", "name": a} for a in AREAS[:10]],
        "priceRange": "Maksuton arvio",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Märkätilojen saumaus",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                                                 "url": f"{BASE_URL}/{s['slug']}/"}} for s in SERVICES]},
    }


def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE_URL + u} for i, (n, u) in enumerate(items)]}


def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def page(path, title, description, body, current="", schema=None, og="og.jpg", noindex=False):
    robots = "noindex, nofollow" if (DEMO or noindex) else "index, follow"
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    html = f'''<!doctype html>
<html lang="fi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{BASE_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fi_FI">
<meta property="og:site_name" content="SlatePro">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}/img/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0b0c">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css?v={VERSION}">
{ld}
</head>
<body>
<a class="skip" href="#main">Siirry sisältöön</a>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/app.js?v={VERSION}" defer></script>
</body>
</html>'''
    if path.endswith(".html"):
        out = os.path.join(SITE, path.strip("/"))
    else:
        d = os.path.join(SITE, path.strip("/"))
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    if not noindex and not path.endswith(".html"):
        SITEMAP.append(path)


SITEMAP = []
VERSION = "1"


# ---------------------------------------------------------------------------
# Osiot
# ---------------------------------------------------------------------------

def sec_head(eyebrow, title, lead="", center=False):
    c = " center" if center else ""
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="sec-head{c} reveal"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2>{lead_html}</div>'


def hero_home():
    chips = "".join(f'<li>{icon("check")}{c}</li>' for c in HERO["chips"])
    return f'''<section class="hero">
  <div class="hero-media">{img("hero", "Ammattilainen tekee uutta silikonisaumaa kylpyhuoneen seinän ja lattian liitokseen", eager=True)}</div>
  <div class="hero-shade"></div>
  <div class="wrap hero-in">
    <p class="eyebrow">{HERO["eyebrow"]}</p>
    <h1>Kylpyhuoneen ilme uusiksi – <em>ilman kokonaista remonttia.</em></h1>
    <p class="hero-lead">{HERO["lead"]}</p>
    <div class="hero-ctas">{btn_wa("Pyydä maksuton arvio WhatsAppilla", cls="btn btn-wa btn-lg")}{btn_tel("btn btn-ghost btn-lg")}</div>
    <ul class="chips">{chips}</ul>
  </div>
  <a class="hero-scroll" href="#saumat" aria-label="Vieritä alas"><span></span></a>
</section>'''


def trust_strip():
    items = [("drop", "Silikonien uusinta"), ("grid", "Laattasaumojen uusinta"), ("shield", "Homeen poisto & ennaltaehkäisy"),
             ("house", "Kotitalousvähennys"), ("star", "Nopea, siisti & luotettava")]
    li = "".join(f'<li>{icon(i)}<span>{t}</span></li>' for i, t in items)
    return f'<section class="strip" aria-label="Palvelut lyhyesti"><ul class="wrap strip-in">{li}</ul></section>'


def problems():
    cards = "".join(f'''<figure class="prob reveal">
      {img(p["img"], p["label"], "(max-width: 700px) 50vw, 25vw")}
      <figcaption><span class="xmark">{icon("x")}</span><strong>{p["label"]}</strong><span>{p["text"]}</span></figcaption>
    </figure>''' for p in PROBLEMS["items"])
    return f'''<section class="sec sec-dark" id="saumat">
  <div class="wrap">
    {sec_head("Tunnistatko nämä?", "Näyttävätkö kylpyhuoneesi saumat <span class='red'>tältä?</span>", PROBLEMS["outro"])}
    <div class="prob-grid">{cards}</div>
    <div class="answer reveal">
      <div><h3>{PROBLEMS["answer_title"]}</h3><p>{PROBLEMS["answer"]}</p></div>
      {btn_wa("Pyydä maksuton arvio", cls="btn btn-red btn-lg")}
    </div>
  </div>
</section>'''


def before_after():
    tabs = "".join(f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}" data-ba="{b["key"]}">{b["label"]}</button>'
                   for i, b in enumerate(BEFORE_AFTER))
    panes = "".join(f'''<div class="ba" data-pane="{b["key"]}"{" hidden" if i else ""}>
      <div class="ba-img ba-after">{img(b["after"], b["label"] + " saumojen uusinnan jälkeen", "(max-width: 900px) 100vw, 900px")}</div>
      <div class="ba-img ba-before">{img(b["before"], b["label"] + " ennen saumojen uusintaa", "(max-width: 900px) 100vw, 900px")}</div>
      <span class="ba-tag ba-tag-b">Ennen</span><span class="ba-tag ba-tag-a">Jälkeen</span>
      <div class="ba-handle" aria-hidden="true"><span>{icon("lr")}</span></div>
      <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Vertaa ennen ja jälkeen">
    </div>''' for i, b in enumerate(BEFORE_AFTER))
    return f'''<section class="sec sec-ink" id="ennen-jalkeen">
  <div class="wrap ba-wrap">
    <div class="ba-copy reveal">
      <p class="eyebrow">Näin voi olla</p>
      <h2>…mutta et halua aloittaa <span class="red">täydellistä kylpyhuonesaneerausta?</span></h2>
      <p class="lead">Me uusimme silikonit ja laattasaumat nopeasti ja siististi – kylpyhuoneesi näyttää taas uudelta.</p>
      <p class="hint">{icon("arrow")} Vedä liukusäädintä ja vertaa.</p>
      <div class="ba-tabs" role="tablist">{tabs}</div>
      <p class="fine">Havainnekuvat. SlatePron tekemiä saumauksia löydät alempaa.</p>
    </div>
    <div class="ba-stage reveal">{panes}</div>
  </div>
</section>'''


def services_grid(heading=True):
    cards = "".join(f'''<a class="svc reveal" href="/{s["slug"]}/">
      <div class="svc-img">{img(s["img"], s["name"], "(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 25vw")}</div>
      <div class="svc-body"><span class="svc-ico">{icon(s["icon"])}</span><h3>{s["name"]}</h3><p>{s["short"]}</p>
      <span class="more">Lue lisää {icon("arrow")}</span></div>
    </a>''' for s in SERVICES)
    head = sec_head("Palvelut", "Märkätilojen saumaukset Pirkanmaalla",
                    "SlatePro on erikoistunut kylpyhuoneiden ja muiden märkätilojen saumojen kunnostamiseen.") if heading else ""
    return f'<section class="sec" id="palvelut"><div class="wrap">{head}<div class="svc-grid">{cards}</div></div></section>'


def big_change():
    rows = "".join(f'<tr><th scope="row">{a}</th><td class="us">{icon("check")}{b}</td><td>{c}</td></tr>'
                   for a, b, c in BIG_CHANGE["compare"])
    paras = "".join(f"<p>{p}</p>" for p in BIG_CHANGE["text"])
    return f'''<section class="sec sec-light">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Fiksumpi vaihtoehto</p>
      <h2>{BIG_CHANGE["title"]}</h2>
      {paras}
    </div>
    <div class="compare reveal">
      <table>
        <thead><tr><th></th><th class="us">Saumojen uusinta</th><th>Täysi kylpyhuoneremontti</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>'''


def why():
    items = "".join(f'<li class="reveal"><span class="why-ico">{icon(w["icon"])}</span><h3>{w["title"]}</h3><p>{w["text"]}</p></li>'
                    for w in WHY["items"])
    return f'''<section class="band">
  <div class="band-media">{img("tekija", "SlatePron ammattilainen uusii silikonisaumaa kylpyhuoneessa")}</div>
  <div class="band-shade"></div>
  <div class="wrap band-in">
    {sec_head(WHY["eyebrow"], WHY["title"], WHY["lead"])}
    <ul class="why">{items}</ul>
  </div>
</section>'''


def process():
    steps = "".join(f'<li class="step reveal"><span class="num">{i + 1}</span><h3>{p["title"]}</h3><p>{p["text"]}</p></li>'
                    for i, p in enumerate(PROCESS))
    return f'''<section class="sec sec-dark" id="nain-etenee">
  <div class="wrap">
    {sec_head("Näin homma etenee", "Neljä askelta puhtaisiin saumoihin", "Kaikki alkaa muutamasta kuvasta. Ei sitoumuksia, ei turhia käyntejä.")}
    <ol class="steps">{steps}</ol>
    <div class="center-cta reveal">{btn_wa("Aloita lähettämällä kuva", cls="btn btn-wa btn-lg")}</div>
  </div>
</section>'''


def before_reno():
    return f'''<section class="sec sec-red">
  <div class="wrap reno reveal">
    <div><h2>{BEFORE_RENO["title"]}</h2><p>{BEFORE_RENO["text"]}</p><p class="strong">{BEFORE_RENO["cta"]}</p></div>
    <div class="reno-cta">{btn_wa("Lähetä kuva WhatsAppiin", cls="btn btn-white btn-lg")}{btn_tel("btn btn-outline-w btn-lg")}</div>
  </div>
</section>'''


def audiences():
    cards = "".join(f'''<article class="aud reveal">{img(a["img"], a["title"], "(max-width: 700px) 100vw, 25vw")}
      <div class="aud-body"><h3>{a["title"]}</h3><p>{a["text"]}</p></div></article>''' for a in AUDIENCES)
    return f'''<section class="sec">
  <div class="wrap">
    {sec_head("Kenelle palvelu sopii?", "Koteihin, vuokra-asuntoihin, taloyhtiöille ja myyntiin")}
    <div class="aud-grid">{cards}</div>
  </div>
</section>'''


def kv_teaser():
    k = KOTITALOUS
    return f'''<section class="sec sec-ink">
  <div class="wrap split kv">
    <div class="reveal">
      <p class="eyebrow">Kotitalousvähennys {k["vuosi"]}</p>
      <h2>Saat <span class="red">{k["pct"]} %</span> työn osuudesta takaisin verotuksessa.</h2>
      <p>Saumojen uusinta on kodin kunnossapitotyötä, joten työn osuudesta saa kotitalousvähennystä. Vähennys on enintään
      {k["max"]:,} € henkilöä kohden – pariskunta voi saada kaksinkertaisen määrän. Omavastuu on {k["omavastuu"]} €.</p>
      <a class="link" href="/kotitalousvahennys/">Lue lisää kotitalousvähennyksestä {icon("arrow")}</a>
    </div>
    {kv_calc()}
  </div>
</section>'''.replace("2,100", "2 100")


def kv_calc():
    k = KOTITALOUS
    return f'''<form class="calc reveal" data-pct="{k["pct"]}" data-max="{k["max"]}" data-omav="{k["omavastuu"]}" onsubmit="return false">
      <h3>{icon("house")} Laske vähennyksesi</h3>
      <label>Työn osuus laskusta (sis. alv)<span class="inp"><input type="number" inputmode="numeric" min="0" step="10" value="800" name="tyo"><em>€</em></span></label>
      <label class="radio-row">Vähennyksen hakijat
        <span class="seg"><input type="radio" name="hlo" value="1" id="h1" checked><label for="h1">1 henkilö</label>
        <input type="radio" name="hlo" value="2" id="h2"><label for="h2">2 henkilöä</label></span></label>
      <div class="calc-out"><span>Vähennys verotuksessa</span><strong data-out>0 €</strong><small data-net></small></div>
      <p class="fine">Suuntaa-antava laskelma: {k["pct"]} % työn osuudesta, omavastuu {k["omavastuu"]} € / hlö, enintään
      {k["max"]} € / hlö ({k["vuosi"]}). Vähennys edellyttää, että sinulla on maksettavia veroja.</p>
    </form>'''


def gallery():
    items = "".join(f'<figure class="gal-item reveal">{img(g["img"], g["cap"], "(max-width: 700px) 50vw, 33vw")}<figcaption>{g["cap"]}</figcaption></figure>'
                    for g in GALLERY)
    return f'''<section class="sec sec-light" id="kohteet">
  <div class="wrap">
    {sec_head("Oikeita kohteita", "SlatePron tekemiä saumauksia", "Kuvat ovat omista kohteistamme – suoraan työmaalta, ilman kuvankäsittelyä.")}
    <div class="gal">{items}</div>
  </div>
</section>'''


def faq_block(faq):
    items = "".join(f'<details class="qa reveal"><summary>{q}<span>{icon("plus")}</span></summary><p>{a}</p></details>' for q, a in faq)
    return f'''<section class="sec" id="ukk">
  <div class="wrap narrow">
    {sec_head("Usein kysyttyä", "Kysymyksiä saumojen uusinnasta", center=True)}
    <div class="faq">{items}</div>
  </div>
</section>'''


def final_cta():
    return f'''<section class="final" id="yhteys">
  <div class="final-media">{img("jalkeen-suihku", "Uudet saumat suihkunurkassa")}</div>
  <div class="final-shade"></div>
  <div class="wrap final-in reveal">
    <div class="final-box">
      <span class="final-badge">{icon("calendar")} Maksuton tarjous</span>
      <h2>Maksuton arvio kylpyhuoneesi saumoista</h2>
      <p>Lähetä meille muutama kuva kylpyhuoneesta WhatsAppilla tai sähköpostilla. Katsomme saumojen kunnon ja kerromme,
      mitä lähtisimme tekemään.</p>
      <div class="final-ctas">{btn_wa("Lähetä kuva WhatsAppiin", cls="btn btn-wa btn-lg")}{btn_tel("btn btn-ghost btn-lg")}</div>
      <ul class="final-contact">
        <li>{icon("mail")}<a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a></li>
        <li>{icon("pin")}Toimialue: koko Pirkanmaa</li>
        <li>{icon("phone")}{COMPANY["contact"]}, {COMPANY["name"]}</li>
      </ul>
    </div>
  </div>
</section>'''


def page_hero(eyebrow, h1, lead, image, crumbs, alt=""):
    cr = " / ".join(f'<a href="{u}">{n}</a>' for n, u in crumbs[:-1]) + f" / <span>{crumbs[-1][0]}</span>"
    return f'''<section class="phero">
  <div class="phero-media">{img(image, alt or h1, eager=True)}</div>
  <div class="hero-shade"></div>
  <div class="wrap phero-in">
    <nav class="crumbs" aria-label="Murupolku">{cr}</nav>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="hero-lead">{lead}</p>
    <div class="hero-ctas">{btn_wa("Pyydä maksuton arvio", cls="btn btn-wa btn-lg")}{btn_tel("btn btn-ghost btn-lg")}</div>
  </div>
</section>'''


# ---------------------------------------------------------------------------
# Sivut
# ---------------------------------------------------------------------------

def build_home():
    body = (hero_home() + trust_strip() + problems() + before_after() + services_grid() + big_change() + why() +
            process() + before_reno() + audiences() + kv_teaser() + gallery() + faq_block(FAQ) + final_cta())
    page("/", "Kylpyhuoneen saumojen uusinta Tampere & Pirkanmaa | SlatePro",
         "Silikonien ja laattasaumojen uusinta ilman kylpyhuoneremonttia. Lähetä kuva WhatsAppiin ja saat maksuttoman "
         "arvion. Koko Pirkanmaa, kotitalousvähennys 40 %.",
         body, "/", [org_schema(), faq_schema(FAQ)])


def build_services_hub():
    body = (page_hero("Palvelut", "Märkätilojen saumaukset Pirkanmaalla",
                      "SlatePro on erikoistunut kylpyhuoneiden ja muiden märkätilojen saumojen kunnostamiseen. Uusimme "
                      "silikonit ja laattasaumat, korjaamme ja tiivistämme rikkinäiset kohdat ja käsittelemme homeen.",
                      "tekija", [("Etusivu", "/"), ("Palvelut", "/palvelut/")])
            + services_grid(False) + big_change() + process() + final_cta())
    page("/palvelut/", "Palvelut – silikonit, laattasaumat, tiivistys | SlatePro",
         "Silikonisaumojen ja laattasaumojen uusinta, saumojen korjaus ja tiivistys sekä homeen poisto märkätiloissa "
         "koko Pirkanmaalla. Maksuton arvio kuvista.", body, "/palvelut/",
         [org_schema(), breadcrumb([("Etusivu", "/"), ("Palvelut", "/palvelut/")])])


def build_service(s):
    crumbs = [("Etusivu", "/"), ("Palvelut", "/palvelut/"), (s["name"], f"/{s['slug']}/")]
    sections = ""
    for i, (h, paras) in enumerate(s["body"]):
        if i == 1:
            lis = "".join(f'<li><span class="n">{j + 1}</span><p>{p}</p></li>' for j, p in enumerate(paras))
            sections += f'<div class="prose-block reveal"><h2>{h}</h2><ol class="howto">{lis}</ol></div>'
        else:
            sections += f'<div class="prose-block reveal"><h2>{h}</h2>' + "".join(f"<p>{p}</p>" for p in paras) + "</div>"
    note = f'<div class="note reveal">{icon("shield")}<p>{s["note"]}</p></div>' if s.get("note") else ""
    signs = "".join(f'<li>{icon("check")}{x}</li>' for x in s["signs"])
    others = "".join(f'<li><a href="/{o["slug"]}/">{icon(o["icon"])}<span>{o["name"]}</span>{icon("arrow")}</a></li>'
                     for o in SERVICES if o["slug"] != s["slug"])
    wa_text = f"Hei SlatePro! Haluaisin arvion: {s['name'].lower()}. Liitän kuvia:"
    body = page_hero("Palvelu · Koko Pirkanmaa", s["h1"], s["lead"], s["img"], crumbs) + f'''
<section class="sec">
  <div class="wrap svc-layout">
    <article class="prose">{sections}{note}</article>
    <aside class="side">
      <div class="side-card reveal">
        <h3>Tunnistatko nämä merkit?</h3>
        <ul class="signs">{signs}</ul>
        <p>Lähetä kuva, niin kerromme, mitä kohteelle kannattaa tehdä.</p>
        {btn_wa("Lähetä kuva WhatsAppiin", text=wa_text)}
        <a class="side-tel" href="{TEL}">{icon("phone")} tai soita {COMPANY["phone"]}</a>
      </div>
      <div class="side-card side-kv reveal">
        <p class="eyebrow">Kotitalousvähennys</p>
        <p><strong>{KOTITALOUS["pct"]} %</strong> työn osuudesta takaisin verotuksessa.</p>
        <a class="link" href="/kotitalousvahennys/">Laske vähennys {icon("arrow")}</a>
      </div>
      <nav class="side-card reveal" aria-label="Muut palvelut"><h3>Muut palvelut</h3><ul class="others">{others}</ul></nav>
    </aside>
  </div>
</section>''' + before_after() + process() + faq_block(FAQ[:5]) + final_cta()
    svc_schema = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["description"],
                  "serviceType": s["name"], "provider": {"@id": BASE_URL + "/#yritys"},
                  "areaServed": {"@type": "AdministrativeArea", "name": "Pirkanmaa"}, "url": f"{BASE_URL}/{s['slug']}/"}
    page(f"/{s['slug']}/", s["title"], s["description"], body, "/palvelut/",
         [org_schema(), svc_schema, breadcrumb(crumbs), faq_schema(FAQ[:5])])


def build_kv():
    k = KOTITALOUS
    crumbs = [("Etusivu", "/"), ("Kotitalousvähennys", "/kotitalousvahennys/")]
    faq = [
        ("Kuka voi saada kotitalousvähennystä?", "Kuka tahansa, joka teettää kunnossapito- tai perusparannustyötä omassa "
         "tai vanhempiensa kodissa tai vapaa-ajan asunnossa ja jolla on maksettavia veroja."),
        ("Mistä osasta laskua vähennyksen saa?", "Vain työn osuudesta (sis. alv). Tarvikkeista, kuten silikoneista ja "
         "saumalaastista, ei saa vähennystä. Erittelemme työn osuuden laskuun."),
        ("Miten vähennystä haetaan?", "Joko verokortin muutoksella heti tai esitäytetyssä veroilmoituksessa jälkikäteen "
         "(OmaVero). Tarvitset laskun ja maksutiedot."),
        ("Voiko taloyhtiö saada vähennystä?", "Taloyhtiö ei, mutta osakas voi saada vähennystä omaan asuntoonsa "
         "kohdistuvasta työstä, jonka hän maksaa itse."),
    ]
    body = page_hero(f"Kotitalousvähennys {k['vuosi']}", f"Saumojen uusinta ja kotitalousvähennys – {k['pct']} % takaisin",
                     f"Saumojen uusinta on kodin kunnossapitotyötä. Vuonna {k['vuosi']} saat verotuksessa takaisin {k['pct']} % "
                     f"työn osuudesta, enintään {k['max']} € henkilöä kohden.", "koti", crumbs, "Siisti kylpyhuone") + f'''
<section class="sec">
  <div class="wrap split kv">
    <div class="prose reveal">
      <h2>Näin vähennys lasketaan</h2>
      <p>Vähennys on <strong>{k["pct"]} %</strong> laskun työn osuudesta (sis. alv). Vähennyksestä vähennetään
      <strong>{k["omavastuu"]} €</strong> omavastuu, ja vähennys voi olla enintään <strong>{k["max"]} €</strong> henkilöä kohden
      vuodessa. Jos puolisot ovat molemmat maksaneet työtä, kumpikin voi hakea omaa vähennystään.</p>
      <p><strong>Esimerkki:</strong> työn osuus 800 € → 40 % = 320 € → omavastuun jälkeen vähennys 170 €.
      Kaksi hakijaa (400 € + 400 €): 2 × (160 € − 150 €) = 20 €. Pienissä töissä yksi hakija on usein edullisempi.</p>
      <p class="fine">Luvut perustuvat hallituksen esitykseen kotitalousvähennyksen korottamisesta vuosille 2026–2027
      (voimassa takautuvasti 1.1.2026 alkaen). Tarkista ajantasaiset tiedot osoitteesta
      <a href="https://www.vero.fi/henkiloasiakkaat/verokortti-ja-veroilmoitus/tulot-ja-vahennykset/kotitalousvahennys/" target="_blank" rel="noopener">vero.fi</a>.</p>
    </div>
    {kv_calc()}
  </div>
</section>''' + faq_block(faq) + services_grid() + final_cta()
    page("/kotitalousvahennys/", f"Kotitalousvähennys {k['vuosi']} saumojen uusinnasta – laskuri | SlatePro",
         f"Saumojen uusinnasta saa kotitalousvähennystä {k['pct']} % työn osuudesta, enintään {k['max']} €/hlö. "
         "Laske vähennyksesi ja pyydä maksuton arvio.", body, "/kotitalousvahennys/",
         [org_schema(), breadcrumb(crumbs), faq_schema(faq)])


def build_area():
    crumbs = [("Etusivu", "/"), ("Toimialue", "/toimialue/")]
    chips = "".join(f"<li>{icon('pin')}{a}</li>" for a in AREAS)
    body = page_hero("Toimialue", "Saumojen uusinta koko Pirkanmaalla",
                     "Palvelemme kotitalouksia, taloyhtiöitä ja muita kiinteistönomistajia Tampereella ja kaikissa "
                     "Pirkanmaan kunnissa.", "taloyhtio", crumbs, "Kerrostalo Tampereella") + f'''
<section class="sec">
  <div class="wrap split">
    <div class="prose reveal">
      <h2>Tampere ja kehyskunnat – ja siitä eteenpäin</h2>
      <p>Toimimme koko Pirkanmaan alueella: Tampereella, Nokialla, Ylöjärvellä, Kangasalla, Lempäälässä ja Pirkkalassa
      sekä kauempana maakunnassa. Arvio tehdään yleensä kuvien perusteella, joten sijainti ei hidasta alkua.</p>
      <p>Taloyhtiöille ja vuokranantajille voimme sopia useamman asunnon saumausten huollosta samalla kertaa, mikä
      tekee työstä sujuvaa ja edullisempaa.</p>
      <div class="hero-ctas">{btn_wa("Kysy aikataulua WhatsAppilla", text="Hei SlatePro! Kysyisin aikataulua. Kohde on paikkakunnalla:")}</div>
    </div>
    <ul class="areas reveal">{chips}</ul>
  </div>
</section>''' + audiences() + final_cta()
    page("/toimialue/", "Toimialue – saumojen uusinta Tampere ja koko Pirkanmaa | SlatePro",
         "SlatePro uusii kylpyhuoneiden silikonit ja laattasaumat Tampereella, Nokialla, Ylöjärvellä, Kangasalla, "
         "Lempäälässä, Pirkkalassa ja koko Pirkanmaalla.", body, "/toimialue/", [org_schema(), breadcrumb(crumbs)])


def build_contact():
    crumbs = [("Etusivu", "/"), ("Yhteystiedot", "/yhteystiedot/")]
    body = f'''<section class="phero phero-sm">
  <div class="phero-media">{img("jalkeen-nurkka", "Uusi silikonisauma", eager=True)}</div>
  <div class="hero-shade"></div>
  <div class="wrap phero-in">
    <nav class="crumbs" aria-label="Murupolku"><a href="/">Etusivu</a> / <span>Yhteystiedot</span></nav>
    <p class="eyebrow">Maksuton arvio</p>
    <h1>Ota yhteyttä – nopeimmin WhatsAppilla</h1>
    <p class="hero-lead">Lähetä muutama kuva kylpyhuoneesta ja kerro lyhyesti, mitä haluaisit uusia. Vastaamme yleensä saman päivän aikana.</p>
  </div>
</section>
<section class="sec">
  <div class="wrap contact">
    <div class="contact-cards">
      <a class="ccard ccard-wa reveal" href="{esc(wa())}" target="_blank" rel="noopener" data-track="whatsapp">{WA_ICON}
        <span><strong>WhatsApp</strong>Lähetä kuvat suoraan puhelimesta</span>{icon("arrow")}</a>
      <a class="ccard reveal" href="{TEL}" data-track="puhelu">{icon("phone")}<span><strong>{COMPANY["phone"]}</strong>Soita tai laita tekstiviesti</span>{icon("arrow")}</a>
      <a class="ccard reveal" href="mailto:{COMPANY["email"]}">{icon("mail")}<span><strong>{COMPANY["email"]}</strong>Sähköposti – liitä kuvat mukaan</span>{icon("arrow")}</a>
      <div class="ccard ccard-static reveal">{icon("pin")}<span><strong>Koko Pirkanmaa</strong>{COMPANY["contact"]} · {COMPANY["name"]}</span></div>
    </div>
    <form class="form reveal" name="yhteydenotto" method="POST" {form_attrs()}>
      {hidden_fields()}
      <h2>Tai jätä yhteydenottopyyntö</h2>
      <p class="muted">Soitamme tai viestimme takaisin. Kuvat on helpointa lähettää WhatsAppilla.</p>
      <div class="row2">
        <label>Nimi *<input name="nimi" required autocomplete="name"></label>
        <label>Puhelin *<input name="puhelin" type="tel" required autocomplete="tel"></label>
      </div>
      <div class="row2">
        <label>Sähköposti *<input name="email" type="email" required autocomplete="email"></label>
        <label>Paikkakunta<input name="aihe" autocomplete="address-level2" placeholder="esim. Tampere"></label>
      </div>
      <label>Mitä haluaisit uusia? *<textarea name="viesti" rows="5" required placeholder="esim. suihkunurkan silikonit ja lattiasaumat, kylpyhuone n. 5 m²"></textarea></label>
      <p class="fine">Lähettämällä hyväksyt, että tietojasi käytetään yhteydenottoon (<a href="/tietosuoja/">tietosuojaseloste</a>).</p>
      <button class="btn btn-red btn-lg" type="submit">Lähetä yhteydenottopyyntö {icon("arrow")}</button>
    </form>
  </div>
</section>''' + process()
    page("/yhteystiedot/", "Yhteystiedot – maksuton arvio | SlatePro Pirkanmaa",
         f"Pyydä maksuton arvio kylpyhuoneen saumoista: WhatsApp tai puhelin {COMPANY['phone']}, sähköposti "
         f"{COMPANY['email']}. Toimialue koko Pirkanmaa.", body, "/yhteystiedot/", [org_schema(), breadcrumb(crumbs)])


def build_simple():
    page("/kiitos/", "Kiitos yhteydenotosta | SlatePro", "Kiitos yhteydenotosta.", f'''<section class="sec simple">
  <div class="wrap narrow center">
    <span class="big-ico">{icon("check")}</span>
    <h1>Kiitos! Viestisi tuli perille.</h1>
    <p class="lead">Otamme yhteyttä mahdollisimman pian. Jos haluat nopeuttaa arviota, lähetä muutama kuva kylpyhuoneesta WhatsAppiin.</p>
    <div class="hero-ctas center">{btn_wa()}{btn_tel()}</div>
  </div>
</section>''', noindex=True)
    page("/tietosuoja/", "Tietosuojaseloste | SlatePro", "SlatePro Oy:n asiakasrekisterin tietosuojaseloste.", f'''<section class="sec simple">
  <div class="wrap narrow prose">
    <h1>Tietosuojaseloste</h1>
    <p><strong>Rekisterinpitäjä:</strong> {COMPANY["name"]}{", Y-tunnus " + COMPANY["ytunnus"] if COMPANY["ytunnus"] else ""},
    yhteyshenkilö {COMPANY["contact"]}, {COMPANY["email"]}, {COMPANY["phone"]}.</p>
    <h2>Mitä tietoja käsittelemme</h2>
    <p>Yhteydenoton yhteydessä antamasi nimi, puhelinnumero, sähköposti, paikkakunta, viestin sisältö ja lähettämäsi kuvat.</p>
    <h2>Käyttötarkoitus ja peruste</h2>
    <p>Tietoja käytetään tarjouksen laatimiseen, työn sopimiseen ja laskutukseen. Käsittely perustuu sopimukseen tai
    sen valmisteluun sekä kirjanpitolain velvoitteisiin.</p>
    <h2>Säilytys ja luovutus</h2>
    <p>Tarjouspyyntöjä säilytetään enintään kaksi vuotta, laskutustietoja kirjanpitolain edellyttämän ajan. Tietoja ei
    luovuteta kolmansille osapuolille markkinointiin. WhatsApp-viestit käsitellään WhatsAppin (Meta) palvelussa.</p>
    <h2>Evästeet</h2>
    <p>Sivusto ei käytä seuranta- tai markkinointievästeitä.</p>
    <h2>Oikeutesi</h2>
    <p>Voit pyytää nähtäväksi, korjata tai poistaa tietosi ottamalla yhteyttä yllä oleviin osoitteisiin. Voit myös tehdä
    valituksen tietosuojavaltuutetulle.</p>
  </div>
</section>''', noindex=False)
    page("/404.html", "Sivua ei löytynyt | SlatePro", "Sivua ei löytynyt.", f'''<section class="sec simple">
  <div class="wrap narrow center">
    <p class="eyebrow">404</p><h1>Sivua ei löytynyt</h1>
    <p class="lead">Mutta saumat löytyvät. Palaa etusivulle tai lähetä meille kuva kylpyhuoneestasi.</p>
    <div class="hero-ctas center"><a class="btn btn-red" href="/">Etusivulle</a>{btn_wa()}</div>
  </div>
</section>''', noindex=True)


# ---------------------------------------------------------------------------
# Resurssit
# ---------------------------------------------------------------------------

def font(size, bold=True):
    name = "BarlowCondensed-ExtraBold.ttf" if bold else "Barlow-Medium.ttf"
    return ImageFont.truetype(os.path.join(SRC, "fonts", name), size)


def build_assets():
    logo = Image.open(os.path.join(SRC, "img", "logo.png")).convert("RGBA")
    logo.save(os.path.join(IMG_OUT, "logo.png"), optimize=True)
    # OG-kuva: jälkeen-kuva tummennettuna + logo
    bg = Image.open(IMG_SRC["hero"]).convert("RGB")
    bg = ImageOps.fit(bg, (1200, 630), Image.LANCZOS)
    shade = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    for x in range(1200):
        a = int(235 * max(0, 1 - x / 900))
        d.line([(x, 0), (x, 630)], fill=(8, 8, 9, a))
    bg = Image.alpha_composite(bg.convert("RGBA"), shade)
    lg = logo.copy()
    lg.thumbnail((420, 160))
    bg.alpha_composite(lg, (70, 70))
    d = ImageDraw.Draw(bg)
    d.text((72, 290), "KYLPYHUONEEN SAUMAT", font=font(76), fill="white")
    d.text((72, 372), "UUSIKSI ILMAN REMONTTIA", font=font(76), fill=(228, 26, 34))
    d.text((72, 470), f"Koko Pirkanmaa · Maksuton arvio · {COMPANY['phone']}", font=font(30, False), fill=(220, 220, 220))
    bg.convert("RGB").save(os.path.join(IMG_OUT, "og.jpg"), quality=86)
    # Favicon: vuori-merkki logon vasemmasta osasta mustalle neliölle
    mark = logo.crop((0, 0, 190, logo.height))
    mark.thumbnail((150, 150))
    for size, name in ((64, "favicon.png"), (180, "apple-touch-icon.png")):
        c = Image.new("RGBA", (size, size), (11, 11, 12, 255))
        m = mark.copy()
        m.thumbnail((int(size * .84), int(size * .84)))
        c.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
        c.save(os.path.join(SITE, name))
    shutil.copy(os.path.join(SRC, "style.css"), os.path.join(SITE, "style.css"))
    shutil.copy(os.path.join(SRC, "app.js"), os.path.join(SITE, "app.js"))
    with open(os.path.join(SITE, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /\n" if DEMO else f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
        urls = "".join(f"<url><loc>{BASE_URL}{p}</loc><changefreq>monthly</changefreq><priority>{'1.0' if p == '/' else '0.8'}</priority></url>"
                       for p in SITEMAP)
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')


def build():
    global VERSION
    VERSION = str(int(max(os.path.getmtime(os.path.join(SRC, f)) for f in ("style.css", "app.js"))))
    for f in os.listdir(SITE) if os.path.isdir(SITE) else []:
        if f != "img":
            p = os.path.join(SITE, f)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(SITE, exist_ok=True)
    build_images()
    build_home()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    build_kv()
    build_area()
    build_contact()
    build_simple()
    build_assets()
    target = write_host_files(SITE, vastaanottaja=COMPANY["email"], domain=COMPANY["domain"], sivusto=COMPANY["name"])
    print(f"Rakennettu {len(SITEMAP)} indeksoitavaa sivua → site/ ({target})")
    if "--preview" not in sys.argv:
        name = os.path.join(ROOT, "..", f"slatepro-{target}.zip")
        with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as z:
            for base, _, files in os.walk(SITE):
                for fn in files:
                    full = os.path.join(base, fn)
                    z.write(full, os.path.relpath(full, SITE))
        print("Zip:", os.path.abspath(name))


if __name__ == "__main__":
    build()
