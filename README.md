# SlatePro – sivusto

Staattinen sivusto SlatePro Oy:lle (märkätilojen silikonien ja laattasaumojen uusinta, koko Pirkanmaa, Henri Takkinen).
Sama malli kuin muissa asiakassivustoissa: `content.py` (tekstit) + `build.py` (sivupohjat, kuvat, SEO) + `src/style.css` + `src/app.js`.

```bash
python3 build.py                     # NordicHost (oletus): site/ + ../slatepro-nordichost.zip
HOSTING=webhotelli python3 build.py  # tavallinen webhotelli: PHP-lomake + .htaccess
python3 build.py --preview           # ilman zipiä
```

Esikatselu: `site/` kopioidaan scratchpadiin (`.claude/launch.json` → `slatepro-site`, portti 8796). `?shot=1` = animaatiot pois.

## Julkaisu: NordicHost cPanel → "AI App Hosting" (GitHub)

Repo: `github.com/Aija-group/slatepro`. NordicHostin AI App Hosting ajaa **Node.js-sovelluksen** Gitistä, ei PHP:tä:
- `server.js` tarjoilee valmiin `site/`-kansion (ohjaukset, 404, välimuisti, www → juuri) ja käsittelee lomakkeen `POST /lahetys`.
- `site/` **commitoidaan repoon**, koska palvelimella ei ajeta Pythonia. Muutoksen jälkeen: `python3 build.py` → commit → push.
- `package.json`: `npm start` = `node server.js`, riippuvuutena vain nodemailer.
- Lomakeviestit menevät osoitteeseen `slateprooy@gmail.com`. Oletuksena lähetys palvelimen sendmailin kautta; jos se ei toimi,
  aseta cPanelin sovellusasetuksiin `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` (cPanelin sähköpostitili, esim. no-reply@slatepro.fi) ja `MAIL_FROM`.
- Sähköposti (webmail/MX) ei muutu: sovellus vastaa vain verkkosivuliikenteeseen.

## Lähteet
| Aineisto | Mistä |
|---|---|
| Tekstit | asiakkaan `slatepro tekstit.pdf` (pohjana, laajennettu palvelusivuille) |
| Brändi | esite + logo (`_materiaali/orig/`); logo muutettu läpinäkyväksi `src/img/logo.png` |
| Oikeat kohdekuvat | WhatsApp-zip 24.9.2026 → `_materiaali/orig/wa/` (6 kpl, SlatePron valmista työtä): vain galleria |
| AI-kuvat | Higgsfield gpt_image_2_5 (16 kpl, optimoidut lähteet `src/kuvat/`, `_materiaali/ai/`): hero, palvelut, kenelle, ennen/jälkeen-parit (jälkeen-kuvasta editoitu ennen-versio → täsmäävät liukusäätimessä) |

## Rakenne (10 indeksoitavaa sivua)
`/` · `/palvelut/` · 4 palvelusivua (`/silikonisaumojen-uusinta/`, `/laattasaumojen-uusinta/`, `/saumojen-korjaus-ja-tiivistys/`,
`/homeen-ja-pinttymien-poisto/`) · `/kotitalousvahennys/` (laskuri) · `/toimialue/` (23 Pirkanmaan kuntaa) · `/yhteystiedot/` (lomake) · `/tietosuoja/` + `/kiitos/`, `404`.

**Myyntiä tukevat:** WhatsApp joka paikassa esitäytetyllä viestillä (palvelusivuilla palvelukohtainen), kelluva WA-nappi,
mobiilin alapalkki Soita + WhatsApp, ennen/jälkeen-liukusäädin, vertailutaulukko saumojen uusinta vs. täysi remontti,
kotitalousvähennyslaskuri. **SEO:** HomeAndConstructionBusiness + Service + FAQPage + BreadcrumbList, sitemap, OG-kuva.

## Vahvistettava asiakkaalta
- **Y-tunnus** (tietosuojaseloste). Domain slatepro.fi vahvistettu (NordicHost cPanel).
- **Kotitalousvähennys 40 % / 2 100 € / omavastuu 150 €** perustuu hallituksen esitykseen (6/2026, takautuvasti 1.1.2026) – tarkista lain voimaantulo vero.fi:stä. Luvut yhdessä paikassa: `content.py` KOTITALOUS.
- Vertailutaulukon ja palvelusivujen työtapakuvaukset (esim. homeenestolla varustettu saniteettisilikoni, "vastaamme yleensä saman päivän aikana") – ovatko linjassa Henrin käytännön kanssa.
- Testaa lomake julkaisun jälkeen: saapuuko viesti Gmailiin (ja ei roskapostiin).
- Ennen/jälkeen-kuvat ovat havainnekuvia (merkitty sivulle). Kun Henriltä tulee oikeita ennen/jälkeen-pareja samasta kulmasta, vaihda `BEFORE_AFTER`.
