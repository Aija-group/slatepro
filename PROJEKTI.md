# SlatePro Oy: projektin tausta ja päätökset

Kopio Äijä Groupin projektimuistiosta. Asiakkaan linjaukset ja tehdyt päätökset.

SlatePro Oy (märkätilojen silikonit + laattasaumat, koko Pirkanmaa, Henri Takkinen, 040 185 6969, slateprooy@gmail.com).
Uusi sivusto (ei vanhaa sivua) tehty 24.9.2026 `SlatePro/`-kansioon samalla content.py + build.py + src/style.css + src/app.js -mallilla
kuin project-plg-sivustouudistus. 10 sivua: etusivu, palveluhubi + 4 palvelusivua, kotitalousvähennys+laskuri, toimialue, yhteystiedot.

**Why:** Sulo toi esitteen, logon ja tekstit (PDF) ja pyysi modernin, myyvän, luotettavan sivun suoralla WhatsApp-linkillä.

**How to apply:**
- Brändi esitteestä: musta #0b0b0c, punainen #e11d24, Barlow Condensed -otsikot uppercase. WhatsApp-vihreä vain WA-napeissa.
- Ennen/jälkeen-parit tehty generoimalla ensin "jälkeen"-kuva ja editoimalla siitä "ennen" (gpt_image_2_5 + image_references) → kulmat täsmäävät liukusäätimessä. Hyvä kikka muillekin remonttiasiakkaille.
- Asiakkaan 6 WhatsApp-kuvaa = SlatePron OMAA VALMISTA TYÖTÄ → vain galleriaan "SlatePron tekemiä saumauksia". Ensimmäisessä versiossa ne olivat virheellisesti "Näyttävätkö saumasi tältä?" -ongelmakorteissa; Sulo huomautti 24.9. Ongelmakorteissa nyt AI-ennen-kuvat. Opetus: älä oleta asiakkaan työmaakuvia ennen-kuviksi, vaikka saumat näyttävät tummilta. Viestissä näkynyt suihkunurkkakuva ei tullut tiedostona.
- Kotitalousvähennys 2026: 40 % / 2 100 € / omavastuu 150 € (hallituksen esitys 6/2026, takautuva) – luvut content.py KOTITALOUS.
- Julkaisu: GitHub Aija-group/slatepro → NordicHost cPanel AI App Hosting (ks. project-sivustojen-julkaisuputki); domain slatepro.fi. Avoimet: Y-tunnus, kotitalousvähennyslain voimaantulo, lomakkeen sähköpostitesti. Esikatselu launch.json `slatepro-site`, portti 8796.
- 28.9.2026: livenä slatepro.fi (NordicHost, auto-deploy GitHubista ~4 min, Cloudflare-SSL). Muutokset: ennen/jälkeen-otsikko "Ennen / jälkeen", palveluosion "Palvelut"-eyebrow poistettu (sec_head("") = ei eyebrowta).
