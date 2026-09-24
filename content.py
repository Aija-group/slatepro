# -*- coding: utf-8 -*-
"""SlatePro – sivuston tekstit ja data. Pohjana asiakkaan tekstitiedosto (slatepro tekstit.pdf) ja esite."""
from urllib.parse import quote

COMPANY = {
    "name": "SlatePro Oy",
    "brand": "SlatePro",
    "slogan": "Puhtaat saumat. Uusi ilme.",
    "contact": "Henri Takkinen",
    "phone": "040 185 6969",
    "phone_intl": "+358401856969",
    "email": "slateprooy@gmail.com",
    "area": "Koko Pirkanmaa",
    "domain": "slatepro.fi",          # vahvistettava
    "ytunnus": "",                    # vahvistettava
}

WA_BASE = "https://wa.me/358401856969"


def wa(text="Hei SlatePro! Haluaisin maksuttoman arvion kylpyhuoneen saumoista. Liitän kuvia:"):
    return f"{WA_BASE}?text={quote(text)}"


# Kotitalousvähennys 2026–2027 (hallituksen esitys 6/2026, takautuvasti 1.1.2026 alkaen). Tarkista vero.fi.
KOTITALOUS = {"pct": 40, "max": 2100, "omavastuu": 150, "vuosi": "2026"}

NAV = [
    {"href": "/palvelut/", "label": "Palvelut"},
    {"href": "/#ennen-jalkeen", "label": "Ennen & jälkeen"},
    {"href": "/#nain-etenee", "label": "Näin homma etenee"},
    {"href": "/kotitalousvahennys/", "label": "Kotitalousvähennys"},
    {"href": "/toimialue/", "label": "Toimialue"},
    {"href": "/yhteystiedot/", "label": "Yhteystiedot"},
]

HERO = {
    "eyebrow": "Märkätilojen saumojen uusinta · Pirkanmaa",
    "h1": "Kylpyhuoneen ilme uusiksi – ilman kokonaista remonttia.",
    "lead": "Kuluneet silikonit, tummuneet laattasaumat ja irtoilevat saumat tekevät kylpyhuoneesta nopeasti vanhan "
            "ja epäsiistin näköisen. SlatePro uusii märkätilojen silikonit ja laattasaumat siististi ja huolellisesti "
            "koko Pirkanmaan alueella.",
    "chips": ["Maksuton arvio kuvista", "Kotitalousvähennys 40 %", "Koko Pirkanmaa"],
}

PROBLEMS = {
    "title": "Näyttävätkö kylpyhuoneesi saumat tältä?",
    "items": [
        {"img": "ennen-nurkka", "label": "Likaiset ja homeiset saumat", "text": "Homepilkut ja tummentumat nurkissa ja silikoneissa."},
        {"img": "ennen-suihku", "label": "Kuluneet ja haalistuneet", "text": "Lika ja kosteus värjäävät laattasaumat ruskeiksi."},
        {"img": "ennen-halkeama", "label": "Rikkinäiset ja irtoilevat saumat", "text": "Rikkinäinen sauma päästää veden paikkoihin, joihin sen ei kuulu."},
        {"img": "ennen-silikoni", "label": "Kellastuneet silikonit", "text": "Kalusteiden ympärillä silikoni tummuu ja irtoaa."},
    ],
    "outro": "Kylpyhuone näyttää muuten hyvältä, mutta saumat vetävät koko ilmeen alas.",
    "answer_title": "Usein koko kylpyhuonetta ei tarvitse uusia.",
    "answer": "Saumojen ja silikonien uusiminen voi tehdä tilasta huomattavasti siistimmän ja raikkaamman murto-osalla "
              "täydellisen kylpyhuoneremontin vaivasta. Lähetä meille kuva kylpyhuoneestasi, niin kerromme, mitä sille "
              "kannattaa tehdä.",
}

BEFORE_AFTER = [
    {"key": "suihku", "label": "Suihkunurkka", "before": "ennen-suihku", "after": "jalkeen-suihku"},
    {"key": "nurkka", "label": "Seinän ja lattian liitos", "before": "ennen-nurkka", "after": "jalkeen-nurkka"},
]

SERVICES = [
    {
        "slug": "silikonisaumojen-uusinta", "icon": "drop", "img": "silikoni",
        "name": "Silikonisaumojen uusinta",
        "short": "Vanha silikoni pois, tilalle uusi ja siisti silikonisauma. Nurkat ja liitoskohdat näyttävät taas viimeistellyiltä.",
        "title": "Silikonisaumojen uusinta Tampere & Pirkanmaa | SlatePro",
        "description": "Kylpyhuoneen silikonien uusinta Pirkanmaalla. Poistamme vanhan, tummuneen silikonin ja teemme tilalle "
                       "siistin, tiiviin saumauksen. Maksuton arvio kuvista.",
        "h1": "Silikonisaumojen uusinta",
        "lead": "Vanha silikoni poistetaan huolellisesti ja tilalle tehdään uusi, siisti silikonisauma. Silikonien "
                "uusiminen tekee kylpyhuoneen nurkista ja liitoskohdista jälleen viimeistellyn näköiset.",
        "body": [
            ("Missä silikonia on – ja miksi se kuluu", [
                "Silikoni on märkätilan joustava sauma: sitä on seinän ja lattian liitoksessa, sisänurkissa, "
                "suihkuseinien ja -kaappien reunoilla, ammeen ja altaan ympärillä sekä WC-istuimen ja kalusteiden juurella.",
                "Koska silikoni joustaa, se kestää rakenteen pienet liikkeet. Samalla se on kuitenkin jatkuvasti "
                "tekemisissä veden, pesuaineiden ja lämpötilavaihteluiden kanssa. Ajan myötä pinta tummuu, homepilkut "
                "tarttuvat siihen ja reunat alkavat irrota.",
            ]),
            ("Näin uusimme silikonit", [
                "Leikkaamme ja kaavimme vanhan silikonin kokonaan pois – uutta ei koskaan vedetä vanhan päälle.",
                "Puhdistamme ja kuivaamme saumakohdan, jotta uusi silikoni tarttuu pohjaansa kunnolla.",
                "Teemme uuden sauman märkätiloihin tarkoitetulla, homeenestolla varustetulla saniteettisilikonilla "
                "ja viimeistelemme sen tasaiseksi ja suoraksi.",
                "Siivoamme työalueen ja kerromme, milloin tilaa voi taas käyttää normaalisti.",
            ]),
        ],
        "signs": ["Silikoni on tummunut tai siinä on mustia pilkkuja", "Sauma on irronnut reunoiltaan tai haljennut",
                  "Nurkassa näkyy rako seinän ja lattian välissä", "Altaan tai istuimen juuri on kellastunut"],
    },
    {
        "slug": "laattasaumojen-uusinta", "icon": "grid", "img": "laattasauma",
        "name": "Laattasaumojen uusinta",
        "short": "Kuluneet, värjäytyneet tai rikkoutuneet laattasaumat uusitaan ilman koko laatoituksen purkamista.",
        "title": "Laattasaumojen uusinta Tampere & Pirkanmaa | SlatePro",
        "description": "Kylpyhuoneen laattasaumojen uusinta ilman laatoituksen purkamista. Tummuneet ja rikkinäiset saumat "
                       "tilalle puhtaat uudet. Koko Pirkanmaa, maksuton arvio.",
        "h1": "Laattasaumojen uusinta",
        "lead": "Kuluneet, värjäytyneet tai rikkoutuneet laattasaumat voidaan uusia ilman koko laatoituksen purkamista. "
                "Uudet saumat muuttavat koko tilan ilmettä yllättävän paljon.",
        "body": [
            ("Laatat kunnossa, saumat eivät", [
                "Kylpyhuoneen laatat voivat olla täysin hyvässä kunnossa vielä vuosienkin jälkeen. Saumalaasti sen "
                "sijaan on huokoista ja imee likaa, saippuaa ja kosteutta – siksi juuri saumat alkavat näyttää "
                "kuluneilta ensimmäisenä.",
                "Kun saumat uusitaan, lattia ja seinät näyttävät taas yhtenäisiltä ja puhtailta. Muutos on usein "
                "niin suuri, että tila näyttää uudelta.",
            ]),
            ("Näin uusimme laattasaumat", [
                "Poistamme vanhaa saumalaastia tarvittavalta syvyydeltä laattoja vahingoittamatta.",
                "Imuroimme ja puhdistamme saumat pölystä ja irtonaisesta aineksesta.",
                "Saumaamme uudelleen märkätiloihin sopivalla saumalaastilla. Sävyn voi pitää ennallaan tai vaihtaa – "
                "vaalea sauma raikastaa, tumma on huoltovapaampi.",
                "Pesemme laattapinnat saumauksen jälkeen ja jätämme tilan siistiksi.",
            ]),
        ],
        "signs": ["Lattiasaumat ovat tummuneet eivätkä puhdistu pesemällä", "Saumoista irtoaa murenaa",
                  "Saumoissa on halkeamia tai koloja", "Seinäsaumat ovat kellastuneet suihkun kohdalta"],
    },
    {
        "slug": "saumojen-korjaus-ja-tiivistys", "icon": "shield", "img": "korjaus",
        "name": "Saumojen korjaus ja tiivistys",
        "short": "Halkeilevat ja irtoilevat saumat kannattaa korjata ajoissa. Käymme märkätilan saumaukset läpi.",
        "title": "Märkätilan saumojen korjaus ja tiivistys | SlatePro Pirkanmaa",
        "description": "Halkeilevat ja irtoilevat saumat kannattaa korjata ajoissa. Käymme märkätilan saumaukset läpi ja "
                       "korjaamme kohdat, jotka tarvitsevat uusimista tai tiivistystä.",
        "h1": "Saumojen korjaus ja tiivistys",
        "lead": "Halkeilevat tai irtoilevat saumat kannattaa korjata ajoissa. Käymme läpi märkätilan saumaukset ja "
                "korjaamme kohdat, jotka tarvitsevat uusimista tai tiivistystä.",
        "body": [
            ("Pieni vika kannattaa korjata ennen kuin se kasvaa", [
                "Rikkinäinen sauma ei ole vain ulkonäköasia. Kun sauma halkeaa tai irtoaa, vesi pääsee kulkeutumaan "
                "sinne, minne sen ei kuulu – ja pienestä raosta voi kasvaa iso ja kallis ongelma.",
                "Kaikkea ei aina tarvitse uusia. Käymme tilan läpi ja korjaamme ne kohdat, joissa korjausta "
                "oikeasti tarvitaan. Näin et maksa turhasta työstä.",
            ]),
            ("Mitä tarkastamme", [
                "Seinän ja lattian liitokset, sisänurkat ja lattiakaivon ympäristön.",
                "Suihkuseinien, altaan, ammeen ja WC-istuimen liitokset.",
                "Läpiviennit, kuten putkien ja hanojen ympärykset.",
                "Laattasaumojen kunnon: halkeamat, kolot ja murenevat kohdat.",
            ]),
        ],
        "signs": ["Saumassa on halkeama tai rako", "Sauma on irronnut laatan reunasta",
                  "Lattiakaivon ympärys on tummunut", "Putken läpiviennin tiiviste on haljennut"],
        "note": "Jos epäilet, että vettä on jo päässyt rakenteisiin (esim. kosteus- tai hajuhaitta), kerro siitä "
                "yhteydenotossa. Arvioimme, riittääkö saumojen uusinta vai tarvitaanko ensin kosteuskartoitus.",
    },
    {
        "slug": "homeen-ja-pinttymien-poisto", "icon": "spark", "img": "home",
        "name": "Homeen ja pinttymien poisto",
        "short": "Saumojen lika, tummentumat ja homekasvusto käsitellään työn yhteydessä tilanteen mukaan.",
        "title": "Homeen ja pinttymien poisto kylpyhuoneen saumoista | SlatePro",
        "description": "Tummuneet ja homeiset saumat? Käsittelemme saumojen lian ja homekasvuston ja vaihdamme "
                       "huonokuntoiset saumaukset uusiin. Koko Pirkanmaa.",
        "h1": "Homeen ja pinttymien poisto",
        "lead": "Saumojen pinnalle kertynyt lika, tummentumat ja homekasvusto käsitellään työn yhteydessä tilanteen "
                "mukaan. Samalla vanhat ja huonokuntoiset saumaukset voidaan vaihtaa kokonaan uusiin.",
        "body": [
            ("Miksi saumat mustuvat", [
                "Kylpyhuoneessa on lämmintä ja kosteaa, ja saumoihin kertyy saippuaa ja ihon rasvaa. Siinä on hyvä "
                "kasvualusta pintahomeelle, joka näkyy mustina pilkkuina nurkissa ja silikoneissa.",
                "Pintahome saadaan usein pois laattapinnoilta, mutta silikonin sisään kasvanut home ei lähde "
                "pesemällä. Silloin ainoa kestävä ratkaisu on vaihtaa silikoni uuteen.",
            ]),
            ("Näin käsittelemme", [
                "Puhdistamme tummuneet pinnat ja saumat tarkoitukseen sopivilla aineilla.",
                "Poistamme silikonit ja saumat, joihin home on kasvanut sisään.",
                "Teemme uudet saumat homeenestolla varustetuilla märkätilatuotteilla.",
                "Annamme vinkit, joilla uudet saumat pysyvät pitkään puhtaina: tuuletus, kuivaus ja oikeat pesuaineet.",
            ]),
        ],
        "signs": ["Nurkissa ja silikoneissa on mustia pilkkuja", "Saumat tummuvat nopeasti pesun jälkeen",
                  "Kylpyhuoneessa on tunkkainen haju", "Suihkun kohdalla saumat ovat selvästi muita tummempia"],
    },
]
SERVICE = {s["slug"]: s for s in SERVICES}

BIG_CHANGE = {
    "title": "Pienellä työllä iso muutos kylpyhuoneen ilmeeseen.",
    "text": [
        "Kylpyhuoneen laatat voivat olla täysin hyvässä kunnossa vielä vuosienkin jälkeen. Saumat sen sijaan joutuvat "
        "jatkuvasti tekemisiin veden, kosteuden, pesuaineiden ja lämpötilavaihteluiden kanssa. Siksi juuri ne alkavat "
        "usein näyttää kuluneilta ensimmäisenä.",
        "Saumojen uusimisella voidaan palauttaa kylpyhuoneeseen puhdas ja viimeistelty ilme ilman viikkojen remonttia, "
        "pölyä ja suurta remonttilaskua.",
    ],
    "compare": [
        ("Kesto", "Nopea, kohteesta riippuen", "Useita viikkoja"),
        ("Kylpyhuone käytössä", "Heti kuivumisen jälkeen", "Ei koko remontin aikana"),
        ("Pöly ja purku", "Vähäinen, rajattu saumoihin", "Laatat ja pinnat puretaan"),
        ("Kustannus", "Murto-osa", "Moninkertainen"),
        ("Lopputulos", "Siistit, uudet saumat", "Kokonaan uusi tila"),
    ],
}

WHY = {
    "eyebrow": "Miksi SlatePro?",
    "title": "Märkätilat ovat meidän erikoisalaamme.",
    "lead": "Teemme saumauksia ja märkätilojen kunnostuksia jatkuvasti, joten tiedämme, millainen lopputulos näyttää "
            "hyvältä myös läheltä katsottuna.",
    "items": [
        {"icon": "spark", "title": "Siisti työnjälki", "text": "Saumat viimeistellään huolellisesti ja työalue jätetään siistiksi työn jälkeen."},
        {"icon": "clock", "title": "Nopea palvelu", "text": "Saumojen uusinta on huomattavasti kevyempi työ kuin kokonainen kylpyhuoneremontti ja valmistuu kohteesta riippuen nopeasti."},
        {"icon": "drop", "title": "Märkätiloihin keskittynyt osaaminen", "text": "Silikonit, laattasaumat ja märkätilojen tiivistykset ovat meidän jokapäiväistä tekemistämme."},
        {"icon": "pin", "title": "Palvelu koko Pirkanmaalla", "text": "Palvelemme kotitalouksia, taloyhtiöitä ja muita kiinteistönomistajia koko Pirkanmaan alueella."},
    ],
}

PROCESS = [
    {"title": "Lähetä meille kuva", "text": "Laita WhatsAppilla tai sähköpostilla muutama kuva kylpyhuoneesta ja kerro lyhyesti, mitä haluaisit uusia."},
    {"title": "Saat arvion työstä", "text": "Arvioimme työn laajuuden ja kerromme, mitä kohteelle suosittelemme. Tarvittaessa tulemme katsomaan kohteen paikan päälle."},
    {"title": "Sovitaan työpäivä", "text": "Sovitaan sinulle sopiva aika ja käydään etukäteen läpi, mitä tehdään."},
    {"title": "Saumat uusiksi", "text": "Poistamme vanhat saumaukset tarvittavilta osin, teemme uudet saumat ja siistimme työalueen. Sen jälkeen kylpyhuone näyttää taas huomattavasti raikkaammalta."},
]

BEFORE_RENO = {
    "title": "Ennen kuin varaat kylpyhuoneremontin, katso ensin saumat.",
    "text": "Vanha kylpyhuone ei aina tarvitse täydellistä saneerausta. Jos laatat, kalusteet ja rakenteet ovat muuten "
            "kunnossa, suurin visuaalinen muutos voi löytyä paljon pienemmästä asiasta. Uudet silikonit ja puhtaat "
            "laattasaumat terävöittävät koko tilan ilmeen.",
    "cta": "Lähetä meille kuva kylpyhuoneestasi, niin kerromme suoraan, mitä sille kannattaa tehdä.",
}

AUDIENCES = [
    {"img": "koti", "title": "Koteihin", "text": "Kun oman kylpyhuoneen saumat ovat tummuneet, kuluneet tai alkaneet irtoilla."},
    {"img": "vuokra", "title": "Vuokra-asuntoihin", "text": "Kun asunto halutaan siistiä seuraavaa asukasta varten nopeasti ilman raskasta remonttia."},
    {"img": "taloyhtio", "title": "Taloyhtiöille", "text": "Kun useamman asunnon märkätilojen saumauksia halutaan huoltaa tai uusia suunnitelmallisesti."},
    {"img": "myynti", "title": "Asunnon myyntiin", "text": "Kun kylpyhuone halutaan saada siistimmäksi ennen valokuvausta, näyttöjä tai myyntiä."},
]

GALLERY = [
    {"img": "wa1", "cap": "Uusitut silikonit sisänurkassa"},
    {"img": "wa2", "cap": "Seinän ja lattian liitos"},
    {"img": "wa3", "cap": "Silikonit ja lattiasaumat nurkassa"},
    {"img": "wa4", "cap": "Silikoni WC-istuimen juurella"},
    {"img": "wa5", "cap": "Istuimen ja lattian liitos"},
    {"img": "wa6", "cap": "Seinän vierusta ja lattiasaumat"},
]

FAQ = [
    ("Pitääkö koko kylpyhuone remontoida, jos saumat ovat huonossa kunnossa?",
     "Ei välttämättä. Jos ongelma rajoittuu silikonien tai laattasaumojen kuntoon, ne voidaan usein uusia erikseen."),
    ("Kuinka nopeasti työ valmistuu?",
     "Aikataulu riippuu kylpyhuoneen koosta ja työn laajuudesta. Kerromme arvioidun työajan ennen työn aloittamista."),
    ("Uusitteko sekä silikonit että laattasaumat?",
     "Kyllä. Voimme uusia joko yksittäisiä saumauksia tai käydä koko märkätilan saumaukset läpi."),
    ("Toimitteko Tampereen ulkopuolella?",
     "Kyllä. Toimialueemme on koko Pirkanmaa."),
    ("Paljonko saumojen uusinta maksaa?",
     "Hinta riippuu työn laajuudesta ja uusittavien saumojen määrästä. Lähetä meille kuvat kohteesta, niin saat arvion helposti."),
    ("Saako saumojen uusinnasta kotitalousvähennystä?",
     "Kyllä. Saumojen uusinta on kodin kunnossapitotyötä, joten työn osuudesta saa kotitalousvähennystä. Vuonna 2026 "
     "vähennys on 40 % työn osuudesta (omavastuu 150 €, enintään 2 100 € henkilöä kohden). Merkitsemme työn osuuden laskuun."),
    ("Mistä tiedän, riittääkö saumojen uusinta?",
     "Lähetä kuvat WhatsAppiin. Jos laatat, kalusteet ja rakenteet ovat kunnossa, saumojen uusinta on usein kannattavin "
     "tapa saada tila taas siistiksi. Jos näemme merkkejä laajemmasta ongelmasta, kerromme sen suoraan."),
]

AREAS = ["Tampere", "Nokia", "Ylöjärvi", "Kangasala", "Lempäälä", "Pirkkala", "Valkeakoski", "Orivesi",
         "Sastamala", "Akaa", "Hämeenkyrö", "Ikaalinen", "Mänttä-Vilppula", "Parkano", "Vesilahti", "Urjala",
         "Pälkäne", "Kuhmoinen", "Ruovesi", "Virrat", "Juupajoki", "Punkalaidun", "Kihniö"]
