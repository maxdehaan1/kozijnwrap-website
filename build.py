#!/usr/bin/env python3
"""
Bouwt de statische site uit src/pages/ naar de repo-root.

Elke bron in src/pages/ bestaat uit een JSON-blok in een HTML-comment (de
paginagegevens) gevolgd door de eigenlijke inhoud. Alles wat op elke pagina
hetzelfde is — de <head>, de navigatie, de footer — staat alleen hier.

Gebruik:  python3 build.py
"""

import json
from html import escape
import re
import hashlib
import time
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "pages"
SITE = "https://kozijnwrap.nl"

# Navigatie en footer worden hieruit gegenereerd; de volgorde is de volgorde
# waarin ze in de balk staan.
# Hoofdnavigatie. "Overzicht" staat hier bewust niet in: het logo linksboven is
# al de weg naar de homepage, en met vijf items wikkelde de balk op een telefoon
# naar twee regels. In de footer staat hij wel.
# Sinds november 2026 ingedeeld rond de vraag van de bezoeker (zie README, "De indeling"):
# herken wat je ziet, vergelijk je opties, kies met de keuzehulp, en laat het iWrap doen.
NAV = [
    ("wat-zie-je", "/wat-zie-je", "Wat zie je?"),
    ("vergelijken", "/vergelijken", "Vergelijken"),
    ("kozijnherstel", "/kozijnherstel", "Herstellen"),
    ("kozijnwrappen", "/kozijnwrappen", "Wrappen"),
    ("blog/index", "/blog", "Kennisbank"),
]

FOOTER_KOLOMMEN = [
    ("Uitzoeken", [("wat-zie-je", "/wat-zie-je", "Wat zie je aan je kozijn?"),
                   ("vergelijken", "/vergelijken", "Je opties vergeleken"),
                   ("keuzehulp", "/keuzehulp", "Keuzehulp")]),
    ("De opties", [("kozijnherstel", "/kozijnherstel", "Kozijn herstellen"),
                   ("kozijnwrappen", "/kozijnwrappen", "Kozijn wrappen"),
                   ("blog/kunststof-kozijnen-schilderen", "/blog/kunststof-kozijnen-schilderen", "Schilderen"),
                   ("blog/kozijn-vervangen-of-herstellen", "/blog/kozijn-vervangen-of-herstellen", "Vervangen of herstellen")]),
    ("Meer", [("blog/index", "/blog", "Kennisbank"),
              ("over-deze-site", "/over-deze-site", "Over deze site"),
              ("privacy", "/over-deze-site#privacy", "Privacy")]),
]
FOOTER = [x for _, k in FOOTER_KOLOMMEN for x in k]

# De route, voor de stappen op de homepage en "volgende stap" onderaan elke pagina.
ROUTE = [
    ("wat-zie-je", "/wat-zie-je", "Herken wat je ziet", "i-oog"),
    ("vergelijken", "/vergelijken", "Vergelijk je opties", "i-weegschaal"),
    ("keuzehulp", "/keuzehulp", "Doe de keuzehulp", "i-vraag"),
]
VOLGENDE = {
    "wat-zie-je": ("vergelijken", "Je weet wat je ziet. Wat zijn je opties?", "Herstellen, een nieuwe kleur, schilderen of vervangen, naast elkaar."),
    "vergelijken": ("keuzehulp", "Welke optie past bij jouw kozijn?", "Vier vragen, en je weet het. Je hoeft geen gegevens achter te laten."),
    "kozijnherstel": ("keuzehulp", "Twijfel je of herstel bij jou kan?", "Vier vragen, en je weet het."),
    "kozijnwrappen": ("wat-zie-je", "Zit er schade of verkleuring op je kozijn?", "Dan is het meestal geen wrapvraag maar herstel. Kijk wat je ziet."),
    "over-deze-site": ("wat-zie-je", "Waar wil je beginnen?", "Bij wat je aan je kozijn ziet."),
    "blog": ("keuzehulp", "Weten wat jouw kozijn nodig heeft?", "Vier vragen, en je weet of herstel volstaat."),
    "blog/index": ("wat-zie-je", "Liever kijken dan lezen?", "Elke klacht met een foto, wat het is en wat je eraan kunt doen."),
}

# iWrap staat op één plek gedefinieerd, want reviewscore en aantal veranderen.
# Deze gegevens komen terug in de brug naar iWrap onderaan de pagina's, in de footer en
# in de structured data.
# Sinds 2014: het aantal jaren rekent zichzelf uit ({{iwrap.jaren}} in de bron).
IWRAP_JAREN = str(time.localtime().tm_year - 2014)

IWRAP = {
    "naam": "iWrap",
    "site": "https://iwrap.nl",
    "offerte": "https://iwrap.nl/contact/",
    # Score en aantal komen uit reviews.json van iwrap.nl (staat naast deze map,
    # zie _iwrap_reviews hieronder), zodat de sites hetzelfde zeggen.
    "reviews_score": "4,9",
    "reviews_aantal": "84",
    "reviews_url": "https://search.google.com/local/reviews?placeid=ChIJyzBbwf-FxkcRIdeuLPGJt9U",
    "reviews": [],
}

def _iwrap_reviews():
    """Reviewscore en -aantal uit ../iwrap-project/reviews.json, het bestand dat
    iwrap.nl bijhoudt (python3 reviews.py daar). Ontbreekt het, dan blijven de
    getallen hierboven staan."""
    pad = Path(__file__).resolve().parent.parent / "iwrap-project" / "reviews.json"
    try:
        r = json.loads(pad.read_text(encoding="utf-8"))
        IWRAP["reviews_score"] = str(r["score"]).replace(".", ",")
        IWRAP["reviews_aantal"] = str(r["aantal"])
        IWRAP["reviews_url"] = "https://search.google.com/local/reviews?placeid=" + r["place_id"]
        IWRAP["reviews"] = r["reviews"]
    except (OSError, ValueError, KeyError):
        pass


def render_reviewkaarten(aantal=2):
    """Twee echte reviews van iWrap, elk aan te klikken naar Google. Van ongeveer
    dezelfde lengte, zodat ze naast elkaar netjes even hoog zijn."""
    # Geen reviews die over "wrappen" gaan: deze site zegt juist dat iWrap dat niet doet, en
    # klanten gebruiken het woord soms voor herstel. "iWrap" zelf telt niet mee.
    kaarten = [r for r in IWRAP["reviews"] if 120 <= len(r["tekst"]) <= 230
               and not re.search(r"(?<![iI])wrap", r["tekst"], re.I)][:aantal]
    return '<div class="pquotes">\n' + "\n".join(
        '  <a class="pquote" href="%s" target="_blank" rel="noopener">'
        '<span class="pq-sterren" role="img" aria-label="5 van de 5 sterren">★★★★★</span>'
        "<span class=\"pq-tekst\">%s</span><span class=\"pq-naam\">%s, op Google</span></a>"
        % (escape(r.get("url") or IWRAP["reviews_url"]), escape(r["tekst"]), escape(r["naam"]))
        for r in kaarten) + "\n</div>"


# Bezoekers tellen met Vercel Web Analytics: zonder cookies, dus zonder banner.
# Werkt pas als Analytics aanstaat in het Vercel-project (zie LIVEGANG.md van iwrap).
ANALYTICS = '\n<script defer src="/_vercel/insights/script.js"></script>'

# Het cijfer van iWrap live: de API van iwrap.nl heeft het van Google. Lukt het
# ophalen niet, dan blijft de stand van de laatste build staan. Tot iwrap.nl naar
# de nieuwe site is overgezet, antwoordt alleen het Vercel-adres.
LIVE_REVIEWS = """<script>
(function () {
  var velden = document.querySelectorAll("[data-rv]");
  function zet(d) {
    window.iwrapReviews = d;
    velden.forEach(function (v) { v.textContent = v.getAttribute("data-rv") === "score" ? d.score_tekst : String(d.aantal); });
  }
  try {
    var b = JSON.parse(sessionStorage.getItem("iwrap-reviews"));
    if (b && b.d && Date.now() - b.t < 1800000) return zet(b.d);
  } catch (e) {}
  if (!window.fetch) return;
  var bronnen = ["https://iwrap.nl/api/reviews", "https://iwrap-website.vercel.app/api/reviews"];
  (function probeer(i) {
    if (i >= bronnen.length) return;
    fetch(bronnen[i]).then(function (r) { if (!r.ok) throw r; return r.json(); }).then(function (d) {
      if (!d || !d.aantal) throw d;
      try { sessionStorage.setItem("iwrap-reviews", JSON.stringify({ t: Date.now(), d: d })); } catch (e) {}
      zet(d);
    }).catch(function () { probeer(i + 1); });
  })(0);
})();
</script>"""


_iwrap_reviews()

# De kleuren van de site (css/style.css): "hemel" (hemelsblauw, gekozen door Max op 17 november
# 2026, de waarden in :root), "nacht" (nachtblauw), "messing" (antraciet met messing) of "baksteen".
# Een ander palet: verander PALET en bouw opnieuw (en maak de deelafbeelding opnieuw, tools/maak_og.py).
PALET = "hemel"
STANDAARD_PALET = "hemel"
PALETTEN = {
    "nacht": {"merk": "1F3D63", "licht": "9FBBE0", "papier": "F6F5F1"},
    "hemel": {"merk": "175A99", "licht": "8EC0EA", "papier": "F4F7FA"},
    "messing": {"merk": "2A2E33", "licht": "D4B97F", "papier": "F7F5F0"},
    "baksteen": {"merk": "8F3E24", "licht": "E2A78C", "papier": "F8F5F1"},
}

# Het beeldmerk: een kozijn van voren, met de onderdorpel in een lichte kleur. Dat is het verhaal
# van de site: de dorpel is bijna altijd het eerst versleten. In de kleuren van het palet; leesbaar
# tot 16px, waar een fijnere tekening dichtslibt.
FAVICON = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
    "<rect width='64' height='64' rx='14' fill='%%23%(merk)s'/>"
    "<path d='M14 12h36v36H14z M22 20v20h20V20z' fill='%%23%(papier)s' fill-rule='evenodd'/>"
    "<path d='M14 40h36v8H14z' fill='%%23%(licht)s'/></svg>"
) % PALETTEN[PALET]

WORDMARK = (
    '<span class="w1">kozijn</span>'
    '<span class="w2">wrap<span class="tld">.nl</span></span>'
)

# Staat onder de merknaam in de footer. Eén plek, dus makkelijk te wisselen.
SLOGAN = "Weet wat je kozijn nodig heeft"

# Eén set lijniconen voor de hele site (klachten, opties, de route), als SVG-symbolen
# bovenin elke pagina. Gebruik: <svg class="icoon"><use href="#i-zon"/></svg>.
ICONEN = {
    "i-zon": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/>',
    "i-barst": '<path d="M4 20V4h16"/><path d="M13 4l-2 4.5 3 2.5-3.5 3.5 2 5.5"/><path d="M11 8.5L7.5 9.5"/>',
    "i-los": '<path d="M12 20h8V4H4v8"/><path d="M4 12c4.5 0 8 3.5 8 8"/><path d="M4 12l8 8"/>',
    "i-lijm": '<path d="M12 3.5c3.2 4.2 5.2 7 5.2 9.6a5.2 5.2 0 0 1-10.4 0c0-2.6 2-5.4 5.2-9.6z"/>',
    "i-blaas": '<circle cx="8.5" cy="14" r="3.5"/><circle cx="16" cy="8.5" r="2.5"/><circle cx="16.5" cy="16.5" r="1.7"/>',
    "i-plooi": '<path d="M3.5 7c2.8-2 5.6 2 8.5 0s5.7 2 8.5 0M3.5 12c2.8-2 5.6 2 8.5 0s5.7 2 8.5 0M3.5 17c2.8-2 5.6 2 8.5 0s5.7 2 8.5 0"/>',
    "i-kras": '<path d="M5 19L19 5M10 20l9-9M4 14l9-9"/>',
    "i-tocht": '<path d="M3 8h10.5a3 3 0 1 0-3-3M3 12.5h15a3 3 0 1 1-3 3M3 17h7"/>',
    "i-hout": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M7 9.5c2.2 0 3.2 1.2 3.2 2.5S9.2 14.5 7 14.5M14 5v14M17.5 8.5v7"/>',
    "i-kleur": '<rect x="3.5" y="4" width="7" height="16" rx="2"/><path d="M10.5 8.5l2.6-2.6a2 2 0 0 1 2.8 0l2.2 2.2a2 2 0 0 1 0 2.8l-7.6 7.6"/><path d="M10.5 20H19a1.5 1.5 0 0 0 1.5-1.5v-3a1.5 1.5 0 0 0-1.5-1.5h-2"/><circle cx="7" cy="16.5" r=".6"/>',
    "i-herstel": '<circle cx="7" cy="9" r="3.5"/><path d="M10.5 9H20v4.5H7.2"/><path d="M17.5 16.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
    "i-schilder": '<rect x="3" y="3.5" width="14" height="6" rx="2"/><path d="M17 6.5h3.5v5.5H12v2.5"/><rect x="10" y="14.5" width="4" height="6.5" rx="1"/>',
    "i-vervangen": '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M12 3v18M4 12h16"/>',
    "i-oog": '<path d="M2.5 12s3.5-6.5 9.5-6.5 9.5 6.5 9.5 6.5-3.5 6.5-9.5 6.5S2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "i-weegschaal": '<path d="M12 4v16M8 20h8M5 7.5h14"/><path d="M5 7.5L2.5 13a2.5 2.5 0 0 0 5 0zM19 7.5L16.5 13a2.5 2.5 0 0 0 5 0z"/>',
    "i-vraag": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.3a2.6 2.6 0 1 1 3.6 2.4c-.7.3-1.1.9-1.1 1.6v.7"/><path d="M12 17h.01"/>',
    "i-vink": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "i-pijl": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "i-klok": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V12l3 2"/>',
    "i-huis": '<path d="M4 11l8-7 8 7v9.5H4z"/><path d="M10 20.5v-5h4v5"/>',
    "i-schild": '<path d="M12 3l7 3v6c0 4.4-3 7.6-7 9-4-1.4-7-4.6-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "i-glas": '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M9 10.2c0-1.1 1.5-3 1.5-3s1.5 1.9 1.5 3a1.5 1.5 0 0 1-3 0zM13 15.2c0-1.1 1.5-3 1.5-3s1.5 1.9 1.5 3a1.5 1.5 0 0 1-3 0z"/>',
    "i-schoon": '<path d="M11 3.5l1.7 4.3 4.3 1.7-4.3 1.7L11 15.5l-1.7-4.3L5 9.5l4.3-1.7z"/><path d="M18 14.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
    "i-boek": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
}
SPRITE = ('<svg class="sprite" aria-hidden="true" focusable="false"><defs>' + "".join(
    '<symbol id="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round" stroke-linejoin="round">%s</symbol>' % (k, v) for k, v in ICONEN.items()) + "</defs></svg>")


# De uitkomstlabels: overal hetzelfde label voor waar iets op uitkomt. Mint = herstellen, wat
# iWrap doet; de rest neutraal. Gebruik in een pagina: {{uit:herstel}}.
UITKOMST = {
    "herstel": ("Herstellen", "i-herstel"),
    "kleur": ("Nieuwe kleur", "i-kleur"),
    "schilder": ("Schilder", "i-schilder"),
    "vervangen": ("Vervangen", "i-vervangen"),
    "glas": ("Nieuw glas", "i-glas"),
    "schoon": ("Schoonmaken", "i-schoon"),
}

# De kennisbank in drie groepen. Een artikel kiest zijn groep met "thema" in zijn metadatablok
# en zijn plek met "orde"; "kaart" is de korte tekst op de tegel.
THEMAS = [
    ("herkennen", "Wat zie je?", "Loslaten, verweren, de onderdorpel: wat er met de folie gebeurt.", "i-oog"),
    ("kiezen", "Herstellen, schilderen of vervangen?", "Wat elke route kost, wat hij oplevert en wanneer hij niet werkt.", "i-weegschaal"),
    ("kleur", "Een andere kleur", "Wrappen, schilderen en de kleur die iedereen kiest.", "i-kleur"),
]


def icoon(naam, klasse="icoon"):
    return '<svg class="%s" aria-hidden="true"><use href="#%s"/></svg>' % (klasse, naam)


def offerte_link(medium, klacht=""):
    """De knop naar het offerteformulier van iwrap.nl. iwrap.nl herkent de utm-codes en stuurt
    door naar /offerte; de klacht gaat mee, zodat die meteen goed in de aanvraag staat."""
    return "%s?utm_source=kozijnwrap.nl&amp;utm_medium=%s&amp;utm_campaign=herstel%s" % (
        IWRAP["offerte"], medium, ("&amp;klacht=" + klacht) if klacht else "")


def render_brug(medium, kop=None, reviews=False):
    """De brug naar iWrap, onderaan bijna elke pagina: herstel nodig, dan iWrap. Met het logo van
    iWrap, zodat je ziet dat het om het bedrijf achter deze site gaat."""
    return (
        '<section class="brug">\n  <div class="wrap">\n    <div class="brug-kaart">\n'
        '      <div class="brug-tekst">\n'
        '        <img class="brug-logo" src="/images/iwrap-logo.svg" width="150" height="31" alt="iWrap" loading="lazy">\n'
        '        <h2>%s</h2>\n'
        '        <p>iWrap maakt deze site, en doet zelf het herstel: al %s jaar alleen kunststof kozijnen '
        'herstellen met Renolit folie, door heel Nederland. Wij besteden niets uit.</p>\n'
        '        <ul class="brug-punten">\n'
        '          <li>%s Een vaste prijs op basis van je foto&rsquo;s</li>\n'
        '          <li>%s Tien jaar Renolit-garantie op de folie, vijf op de uitvoering</li>\n'
        '          <li>%s <a href="%s" target="_blank" rel="noopener"><span data-rv="score">%s</span> uit <span data-rv="aantal">%s</span> Google-reviews</a></li>\n'
        '        </ul>\n'
        '        <div class="knoprij">\n'
        '          <a class="knop knop-primair" href="%s" target="_blank" rel="noopener">Offerte aanvragen bij iWrap %s</a>\n'
        '          <a class="knop knop-tweede" href="%s?utm_source=kozijnwrap.nl&amp;utm_medium=%s" target="_blank" rel="noopener">Naar iwrap.nl</a>\n'
        '        </div>\n      </div>\n'
        '      <figure class="brug-beeld"><picture><source type="image/webp" srcset="/images/proces-squeegee.webp">'
        '<img src="/images/proces-squeegee.jpg" width="1372" height="896" loading="lazy" decoding="async" '
        'alt="Een monteur van iWrap drukt nieuwe Renolit folie met een rakel aan op een onderdorpel"></picture></figure>\n'
        '    </div>\n%s  </div>\n</section>' % (
            kop or "Herstel nodig? Dat doet iWrap.", IWRAP_JAREN,
            icoon("i-vink", "icoon klein"), icoon("i-vink", "icoon klein"), icoon("i-vink", "icoon klein"),
            IWRAP["reviews_url"], IWRAP["reviews_score"], IWRAP["reviews_aantal"],
            offerte_link(medium), icoon("i-pijl", "icoon klein"), IWRAP["site"], medium,
            ('    <div class="brug-reviews">%s</div>\n' % render_reviewkaarten(3)) if reviews else "")
    )


def render_schuif(m, eerste):
    """{{schuif:voor|na|label voor|label na|alt voor|alt na[|positie[|klasse]]}}: twee beelden van hetzelfde
    kozijn op elkaar, met een schuif ertussen (js/voorna.js). De beelden staan in /images als
    <naam>-800.webp, <naam>-1400.webp en <naam>-1400.jpg, allemaal 4:3. De eerste schuif op een
    pagina staat bovenaan en laadt meteen; de rest pas als hij in de buurt komt."""
    d = [x.strip() for x in m.group(1).split("|")]
    voor, na, label_voor, label_na, alt_voor, alt_na = d[:6]
    pos = d[6] if len(d) > 6 and d[6] else "50"
    klasse = (" " + d[7]) if len(d) > 7 else ""
    laden = ' fetchpriority="high"' if eerste else ' loading="lazy"'

    def beeld(naam, alt):
        return (
            '<picture><source type="image/webp" srcset="/images/%s-800.webp 800w, /images/%s-1400.webp 1400w" '
            'sizes="(max-width:900px) 100vw, 560px"><img src="/images/%s-1400.jpg" width="1400" height="1050" '
            'alt="%s" draggable="false" decoding="async"%s></picture>' % (naam, naam, naam, alt, laden))

    ident = "schuif-" + na
    return (
        '<div class="vergelijk%s" style="--pos:%s%%">%s<div class="na">%s</div>'
        '<span class="label label-voor">%s</span><span class="label label-na">%s</span>'
        '<span class="greep" aria-hidden="true"></span>'
        '<label class="sr-only" for="%s">Schuif om %s en %s te vergelijken</label>'
        '<input id="%s" type="range" min="0" max="100" value="%s" step="1"></div>' % (
            klasse, pos, beeld(voor, alt_voor), beeld(na, alt_na), label_voor, label_na,
            ident, label_voor.lower(), label_na.lower(), ident, pos))


def render_levensduur():
    """{{levensduur}}: het kozijnprofiel gaat 50 tot 75 jaar mee, de folie 15 tot 25. Op dezelfde
    schaal naast elkaar, zodat je ziet dat de folie twee, drie keer opnieuw kan in een kozijnleven."""
    return (
        '<div class="levensduur" role="img" aria-label="Een kunststof kozijnprofiel gaat 50 tot 75 jaar mee. '
        'De folie erop 15 tot 25 jaar, dus in één kozijnleven kan de folie twee of drie keer opnieuw.">\n'
        '  <div class="ld-rij"><div class="ld-naam">Het kozijn<small>50 tot 75 jaar</small></div>'
        '<div class="ld-baan"><span class="ld-balk ld-profiel">Kunststof profiel</span></div></div>\n'
        '  <div class="ld-rij"><div class="ld-naam">De folie<small>15 tot 25 jaar</small></div>'
        '<div class="ld-baan"><span class="ld-balk ld-folie">Nieuw</span><span class="ld-balk ld-folie">Herstel</span>'
        '<span class="ld-balk ld-folie">Herstel</span></div></div>\n'
        '  <div class="ld-as" aria-hidden="true"><span>0</span><span>25 jaar</span><span>50 jaar</span><span>75 jaar</span></div>\n'
        '  <div class="ld-uitleg"><p>De folie is een <b>slijtlaag</b>, met tien jaar Renolit-garantie. Ziet je kozijn '
        'er na twintig jaar verweerd uit, dan doet het precies wat je mag verwachten: de jas is versleten, het '
        'kozijn niet. Die jas vervangen kan twee, drie keer in een kozijnleven.</p></div>\n'
        '</div>')


def render_route():
    """{{route}}: de vier stappen van de site, met de laatste bij iWrap (homepage en 404)."""
    return """<ol class="route">
      <li><a class="route-stap" href="/wat-zie-je">
        <span class="route-boven"><span class="route-nr">1</span>{{icoon:i-oog}}</span>
        <h3>Herken wat je ziet</h3>
        <p>Dof, gebarsten, loslatend, of tocht het? Elke klacht met foto en wat je eraan kunt doen.</p>
        <span class="verder">Wat zie je? {{icoon:i-pijl|icoon klein}}</span>
      </a></li>
      <li><a class="route-stap" href="/vergelijken">
        <span class="route-boven"><span class="route-nr">2</span>{{icoon:i-weegschaal}}</span>
        <h3>Vergelijk je opties</h3>
        <p>Herstellen, een nieuwe kleur, schilderen of vervangen: wanneer, wat het in huis betekent en hoe lang het meegaat.</p>
        <span class="verder">Vergelijken {{icoon:i-pijl|icoon klein}}</span>
      </a></li>
      <li><a class="route-stap" href="/keuzehulp">
        <span class="route-boven"><span class="route-nr">3</span>{{icoon:i-vraag}}</span>
        <h3>Doe de keuzehulp</h3>
        <p>Vier vragen over je kozijn, en je weet welke route bij jou past. Klaar in een halve minuut.</p>
        <span class="verder">Naar de keuzehulp {{icoon:i-pijl|icoon klein}}</span>
      </a></li>
      <li><a class="route-stap iwrap" href="{{offerte:route}}" target="_blank" rel="noopener">
        <span class="route-boven"><span class="route-nr">4</span><img class="route-logo" src="/images/iwrap-logo.svg" width="106" height="22" alt="iWrap"></span>
        <h3>Laat het herstellen</h3>
        <p>Herstel nodig? Stuur iWrap een foto van het hele kozijn en krijg een vaste prijs.</p>
        <span class="verder">Offerte bij iWrap {{icoon:i-pijl|icoon klein}}</span>
      </a></li>
    </ol>"""


def palet_attr():
    """Het palet op <html>, als het niet het standaardpalet uit :root is."""
    return (' data-palet="%s"' % PALET) if PALET != STANDAARD_PALET else ""


def render_uit(naam):
    label, ic = UITKOMST[naam]
    return '<span class="uit uit-%s">%s%s</span>' % (naam, icoon(ic, "icoon klein"), label)


def artikelen():
    """Alle artikelen uit src/pages/blog, met titel (de h1), korte tekst, thema en leestijd."""
    lijst = []
    for path in SRC.glob("blog/*.html"):
        meta, body = read_page(path)
        if meta["slug"] == "blog/index":
            continue
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        lijst.append({
            "slug": meta["slug"], "url": url_for(meta["slug"]),
            "titel": re.sub(r"\s+", " ", h1.group(1)).strip() if h1 else meta["title"],
            "kaart": meta.get("kaart", meta["description"]),
            "thema": meta.get("thema", "herkennen"), "orde": meta.get("orde", 99),
            "minuten": leestijd(body),
        })
    volgorde = [t[0] for t in THEMAS]
    lijst.sort(key=lambda a: (volgorde.index(a["thema"]), a["orde"]))
    return lijst


def leestijd(body):
    """Minuten lezen, op 200 woorden per minuut (zonder de HTML en de kaders onderaan)."""
    tekst = re.sub(r'<div class="article-cta".*', "", body, flags=re.S)
    tekst = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", tekst, flags=re.S)
    woorden = len(re.sub(r"<[^>]+>", " ", tekst).split())
    return max(2, round(woorden / 200))


def tegel(a):
    return (
        '<a class="artikeltegel" href="%s"><span class="at-thema">%s</span>'
        '<span class="at-titel">%s</span><span class="at-tekst">%s</span>'
        '<span class="at-meta">%s %d min lezen</span></a>' % (
            a["url"], dict((t[0], t[1]) for t in THEMAS)[a["thema"]], a["titel"], a["kaart"],
            icoon("i-klok", "icoon klein"), a["minuten"]))


def render_kennisbank(kort=False):
    """De kennisbank per thema. Kort (homepage): per thema de titels als lijst."""
    alle = artikelen()
    uit = []
    for sleutel, kop, tekst, ic in THEMAS:
        groep = [a for a in alle if a["thema"] == sleutel]
        if kort:
            uit.append(
                '<div class="kb-kort">%s<h3>%s</h3><ul>%s</ul></div>' % (
                    icoon(ic, "icoon groot"), kop,
                    "".join('<li><a href="%s">%s</a></li>' % (a["url"], a["titel"]) for a in groep)))
        else:
            uit.append(
                '<section class="kb-groep" id="%s" aria-labelledby="kb-%s">\n'
                '  <div class="kb-kop">%s<div><h2 id="kb-%s">%s</h2><p>%s</p></div></div>\n'
                '  <div class="tegels">%s</div>\n</section>' % (
                    sleutel, sleutel, icoon(ic, "icoon groot"), sleutel, kop, tekst,
                    "".join(tegel(a) for a in groep)))
    return ('<div class="kb-kort-raster">%s</div>' if kort else "%s") % "\n".join(uit)


def render_artikelen(slugs):
    """{{artikelen:blog/a,blog/b}}: een rij artikeltegels."""
    per = dict((a["slug"], a) for a in artikelen())
    return '<div class="tegels">%s</div>' % "".join(tegel(per[x.strip()]) for x in slugs.split(","))


def render_verwant(slug):
    """Onder een artikel: drie verwante artikelen, eerst uit hetzelfde thema."""
    alle = artikelen()
    zelf = next(a for a in alle if a["slug"] == slug)
    keus = [a for a in alle if a["thema"] == zelf["thema"] and a["slug"] != slug]
    keus += [a for a in alle if a["thema"] != zelf["thema"] and a["thema"] != "kleur"] if zelf["thema"] != "kleur" else \
            [a for a in alle if a["thema"] == "kiezen"]
    return (
        '<section class="verwant">\n  <div class="wrap breed">\n'
        '    <h2>Verder lezen</h2>\n    <div class="tegels">%s</div>\n'
        '    <p class="verwant-alle"><a href="/blog">Alle artikelen in de kennisbank %s</a></p>\n'
        '  </div>\n</section>' % ("".join(tegel(a) for a in keus[:3]), icoon("i-pijl", "icoon klein")))


def artikel_opmaak(meta, body):
    """Een artikel krijgt bovenaan de leestijd en "In dit artikel" (uit de h2-koppen, die daarvoor
    een id krijgen), en onderaan verwante artikelen en de brug naar iWrap."""
    minuten = leestijd(body)
    koppen = []

    def anker(m):
        tekst = re.sub(r"<[^>]+>", "", m.group(1))
        ident = re.sub(r"[^a-z0-9]+", "-", tekst.lower().replace("\u2019", "").replace("'", "")).strip("-")[:48].strip("-")
        koppen.append((ident, tekst))
        return '<h2 id="%s">%s</h2>' % (ident, m.group(1))

    # Alleen de koppen in de lopende tekst, niet die in het slotkader.
    delen = body.split('<div class="article-cta">', 1)
    delen[0] = re.sub(r"<h2>(.*?)</h2>", anker, delen[0], flags=re.S)
    body = '<div class="article-cta">'.join(delen)

    meta_regel = '<p class="article-meta">%sDoor <a href="%s?utm_source=kozijnwrap.nl&amp;utm_medium=artikel" target="_blank" rel="noopener">iWrap</a> &middot; %s%d minuten lezen</p>' % (
        "", IWRAP["site"], icoon("i-klok", "icoon klein"), minuten)
    body = re.sub(r'<p class="article-meta">.*?</p>', meta_regel, body, count=1, flags=re.S)

    if len(koppen) >= 3:
        inhoud = (
            '<nav class="inhoud" aria-labelledby="inhoud-kop">\n'
            '      <p class="inhoud-kop" id="inhoud-kop">In dit artikel</p>\n'
            '      <ol>%s</ol>\n    </nav>\n' % "".join(
                '<li><a href="#%s">%s</a></li>' % (i, t) for i, t in koppen))
        # Direct na de inleiding: na de eerste alinea van het artikel.
        body = re.sub(r'(</section>\s*<section>\s*<div class="wrap">\s*<p>.*?</p>)',
                      lambda m: m.group(1) + "\n\n    " + inhoud, body, count=1, flags=re.S)
    return body + "\n\n" + render_verwant(meta["slug"]) + "\n\n" + render_brug("artikel")


def render_volgende(slug):
    """Onderaan een pagina: de volgende stap van de route, met de route zelf eronder in het klein."""
    sleutel = slug if slug in VOLGENDE else ("blog" if slug.startswith("blog/") else slug)
    if sleutel not in VOLGENDE:
        return ""
    doel, kop, tekst = VOLGENDE[sleutel]
    url = dict((s_, u) for s_, u, _, _ in ROUTE).get(doel, "/" + doel)
    stappen = "".join(
        '<li class="%s"><span class="route-nr">%d</span>%s</li>' % ("nu" if s_ == sleutel else ("volgt" if s_ == doel else ""), i + 1, label)
        for i, (s_, u, label, ic) in enumerate(ROUTE)) + '<li><span class="route-nr">4</span>Laten herstellen door iWrap</li>'
    return (
        '<section class="volgende">\n  <div class="wrap">\n'
        '    <a class="volgende-kaart" href="%s">\n'
        '      <span class="volgende-label">Volgende stap</span>\n'
        '      <span class="volgende-kop">%s</span>\n'
        '      <span class="volgende-tekst">%s</span>\n'
        '      <span class="volgende-pijl">%s</span>\n'
        '    </a>\n'
        '    <ol class="route-mini" aria-label="De route op deze site">%s</ol>\n'
        '  </div>\n</section>' % (url, kop, tekst, icoon("i-pijl"), stappen)
    )


def url_for(slug):
    """Schone URL zonder .html — vercel.json heeft cleanUrls aan staan."""
    if slug == "index":
        return "/"
    if slug == "blog/index":
        return "/blog"
    return "/" + slug


def css_version():
    """Één hash over alle stylesheets, als cache-buster achter de href.

    Zo mogen de CSS-bestanden een jaar in de browsercache blijven staan en zien
    bezoekers een wijziging tóch meteen: de URL verandert mee met de inhoud.
    """
    h = hashlib.sha1()
    for f in sorted((ROOT / "css").glob("*.css")) + sorted((ROOT / "js").glob("*.js")):
        h.update(f.read_bytes())
    return h.hexdigest()[:8]


def render_nav(slug):
    """Het menu: de route (wat zie je, vergelijken) en de twee optiepagina's, met rechts de
    keuzehulp en de knop naar iWrap. Geen uitklapmenu meer: de kennisbank is één pagina."""
    current = "blog/index" if slug.startswith("blog/") else slug
    links = "\n".join(
        '      <a %shref="%s">%s</a>' % ('class="current" aria-current="page" ' if s_ == current else "", u, label)
        for s_, u, label in NAV)
    kh = ' class="nav-kh current" aria-current="page"' if current == "keuzehulp" else ' class="nav-kh"'
    return (
        '<header class="site">\n'
        '  <div class="nav">\n'
        '    <a class="brand" href="/" aria-label="kozijnwrap.nl, naar de homepage">%s</a>\n'
        '    <nav class="navlinks" aria-label="Hoofdnavigatie">\n%s\n'
        '      <a class="alleen-smal%s" href="/keuzehulp">Keuzehulp</a>\n'
        '    </nav>\n'
        '    <div class="nav-knoppen">\n'
        '      <a%s href="/keuzehulp">Keuzehulp</a>\n'
        '      <a class="nav-cta" href="%s" target="_blank" rel="noopener">Offerte bij iWrap</a>\n'
        '    </div>\n'
        '  </div>\n'
        '</header>' % (WORDMARK, links, " current" if current == "keuzehulp" else "", kh,
                       offerte_link("header"))
    )


def render_footer(slug):
    current = "blog/index" if slug.startswith("blog/") else slug
    kolommen = "\n".join(
        '    <nav class="fkolom" aria-label="%s">\n      <p class="fkop">%s</p>\n      <ul>%s</ul>\n    </nav>' % (
            kop, kop, "".join(
                '<li><a href="%s"%s>%s</a></li>' % (u, ' aria-current="page"' if s_ == current else "", label)
                for s_, u, label in items))
        for kop, items in FOOTER_KOLOMMEN)
    return (
        "<footer>\n"
        '  <div class="wrap fgrid">\n'
        '    <div class="fbrand">\n'
        '      <a class="brand" href="/" aria-label="kozijnwrap.nl, naar de homepage">%s</a>\n'
        '      <p class="fslogan">%s</p>\n'
        "      <p>Uitleg over kunststof kozijnen: wat je ziet, wat je kunt doen en wat het oplevert. "
        "Zodat je weet wat je kozijn nodig heeft voordat je iemand belt.</p>\n"
        '      <a class="fby" href="%s?utm_source=kozijnwrap.nl&amp;utm_medium=footer" target="_blank" rel="noopener">'
        '<span>Een site van</span><img src="/images/iwrap-logo.svg" width="96" height="20" alt="iWrap" loading="lazy"></a>\n'
        "    </div>\n%s\n"
        "  </div>\n"
        "</footer>" % (WORDMARK, SLOGAN, IWRAP["site"], kolommen)
    )


def render_head(meta, ver):
    url = SITE + url_for(meta["slug"])
    og_title = meta.get("ogTitle") or meta["title"]
    og_desc = meta.get("ogDescription") or meta["description"]
    # Nieuwe bestandsnaam bij elke herziening: /images/ staat op een cache van een
    # jaar met immutable, dus onder dezelfde naam zou de oude afbeelding blijven hangen.
    img = SITE + "/images/og-image-v5.jpg"

    # De losse .html-URL's uit de oorspronkelijke structured data meeschrijven
    # naar de schone URL's, zodat canonical en schema niet uit elkaar lopen.
    jsonld = json.dumps(meta.get("jsonld", []), ensure_ascii=False)
    jsonld = jsonld.replace(".html", "").replace(SITE + "/blog/\"", SITE + "/blog\"")
    schema = json.loads(jsonld)
    for b in schema:
        # De artikelen stonden op naam van de site zelf, een uitgever zonder
        # gezicht. iWrap is de partij met de ervaring; dat hoort in het schema
        # te staan, net als in de regel bovenaan het artikel ("Door iWrap").
        if b.get("@type") == "BlogPosting":
            b["author"] = {"@type": "Organization", "name": IWRAP["naam"], "url": IWRAP["site"]}
    blocks = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>'
        % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        for b in schema
    )

    namen = list(meta["css"])
    if "onderdelen" not in namen:
        namen.insert(namen.index("style") + 1 if "style" in namen else 0, "onderdelen")
    css = "\n".join(
        '<link rel="stylesheet" href="/css/%s.css?v=%s">' % (name, ver) for name in namen
    )
    if meta.get("noindex"):
        css = '<meta name="robots" content="noindex">\n' + css

    # Het grootste beeld bovenaan (de voor/na-schuif) is het LCP-element: alvast ophalen.
    preload = ""
    if meta.get("preload"):
        naam, sizes = meta["preload"]
        preload = (
            '\n<link rel="preload" as="image" type="image/webp" fetchpriority="high" '
            'imagesrcset="/images/%s-800.webp 800w, /images/%s-1400.webp 1400w" imagesizes="%s">' % (naam, naam, sizes)
        )

    return """<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{favicon}">
<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Kozijnwrap.nl">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{ogdesc}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{ogdesc}">
<meta name="twitter:image" content="{img}">
{jsonld}
<link rel="preload" href="/fonts/montserrat-latin-83a31c81.woff2" as="font" type="font/woff2" crossorigin>
{css}{preload}""".format(
        title=meta["title"],
        desc=meta["description"],
        url=url,
        favicon=FAVICON,
        ogtype=meta.get("ogType", "website"),
        ogtitle=og_title,
        ogdesc=og_desc,
        img=img,
        jsonld=blocks,
        css=css,
        preload=preload,
    )


def read_page(path):
    raw = path.read_text()
    m = re.match(r"\s*<!--(.*?)-->\s*(.*)", raw, re.S)
    if not m:
        raise SystemExit("Geen metadatablok in %s" % path)
    return json.loads(m.group(1)), m.group(2).strip()


def build():
    ver = css_version()
    pages = sorted(SRC.rglob("*.html"))
    for path in pages:
        meta, body = read_page(path)
        # Het reviewcijfer van iWrap in de lopende tekst, zodat het nergens vastligt.
        # Cijfer en aantal als los veld, zodat LIVE_REVIEWS er de live stand in zet.
        body = body.replace("{{iwrap.reviews_score}}", '<span data-rv="score">%s</span>' % IWRAP["reviews_score"]) \
                   .replace("{{iwrap.reviews_aantal}}", '<span data-rv="aantal">%s</span>' % IWRAP["reviews_aantal"]) \
                   .replace("{{iwrap.reviews_score_tekst}}", IWRAP["reviews_score"]) \
                   .replace("{{iwrap.reviews_aantal_tekst}}", IWRAP["reviews_aantal"]) \
                   .replace("{{iwrap.reviews_url}}", IWRAP["reviews_url"]) \
                   .replace("{{iwrap.jaren}}", IWRAP_JAREN) \
                   .replace("{{iwrap.reviewkaarten}}", render_reviewkaarten())
        slug = meta["slug"]
        # Eerst de vaste blokken die zelf nog codes bevatten, dan de losse codes.
        body = body.replace("{{route}}", render_route())
        body = re.sub(r"\{\{icoon:([\w-]+)(?:\|([\w -]+))?\}\}", lambda m: icoon(m.group(1), m.group(2) or "icoon"), body)
        body = re.sub(r"\{\{uit:(\w+)\}\}", lambda m: render_uit(m.group(1)), body)
        teller = [0]

        def schuif(m):
            teller[0] += 1
            return render_schuif(m, teller[0] == 1)
        body = re.sub(r"\{\{schuif:([^}]+)\}\}", schuif, body)
        body = re.sub(r"\{\{offerte:([\w-]+)(?:\|([\w-]+))?\}\}", lambda m: offerte_link(m.group(1), m.group(2) or ""), body)
        body = re.sub(r"\{\{artikelen:([^}]+)\}\}", lambda m: render_artikelen(m.group(1)), body)
        body = body.replace("{{kennisbank}}", render_kennisbank()).replace("{{kennisbank:kort}}", render_kennisbank(kort=True))
        body = body.replace("{{volgende}}", render_volgende(slug)).replace("{{levensduur}}", render_levensduur())
        body = re.sub(r"\{\{brug(?::([\w-]+))?(?:\|([^}|]+))?(\|reviews)?\}\}",
                      lambda m: render_brug(m.group(1) or slug.replace("/", "-"), m.group(2), bool(m.group(3))), body)
        if slug.startswith("blog/") and slug != "blog/index":
            body = artikel_opmaak(meta, body)
        assert "{{" not in body, "onbekende code in %s: %s" % (slug, body[body.index("{{"):body.index("{{") + 40])
        scripts = ""
        if 'class="vergelijk' in body:
            scripts += '\n<script defer src="/js/voorna.js?v=%s"></script>' % ver
        # De hero met het 3D-kozijn: eerst de motor (dezelfde als op iwrap.nl), dan de vier verhalen.
        if "data-kozijn-keuze" in body:
            scripts += ('\n<script defer src="/js/kozijn-3d.js?v=%s"></script>'
                        '\n<script defer src="/js/kozijn-keuze.js?v=%s"></script>' % (ver, ver))
        live = "\n" + LIVE_REVIEWS if ("data-rv" in body or "iwrapReviews" in body) else ""
        out = ROOT / (meta["slug"] + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            "<!DOCTYPE html>\n"
            '<html lang="nl"%s>\n'
            "<head>\n%s\n</head>\n"
            '<body class="%s">\n\n'
            '<a class="skip" href="#inhoud">Naar de inhoud</a>\n%s\n\n'
            "%s\n\n"
            '<main id="inhoud">\n\n%s\n</main>\n\n'
            "%s\n%s%s%s\n"
            "</body>\n"
            "</html>\n"
            % (
                palet_attr(),
                render_head(meta, ver),
                meta["bodyClass"],
                SPRITE,
                render_nav(slug),
                body,
                render_footer(slug),
                scripts,
                live,
                "" if meta.get("noindex") else ANALYTICS,
            )
        )
        print("  %s" % out.relative_to(ROOT))

    # Sitemap uit dezelfde bron, zodat er nooit een pagina in ontbreekt.
    entries = []
    for path in pages:
        meta, _ = read_page(path)
        slug = meta["slug"]
        if meta.get("noindex"):
            continue
        prio = "1.0" if slug == "index" else "0.8" if "/" not in slug else (
            "0.7" if slug == "blog/index" else "0.6"
        )
        entries.append(
            "  <url>\n    <loc>%s</loc>\n    <priority>%s</priority>\n  </url>"
            % (SITE + url_for(slug), prio)
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(sorted(entries))
        + "\n</urlset>\n"
    )
    print("  sitemap.xml (%d URL's)  ·  css-versie %s" % (len(entries), ver))


if __name__ == "__main__":
    print("Bouwen…")
    build()
    print("Klaar.")
