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
NAV = [
    ("keuzehulp", "/keuzehulp", "Keuzehulp"),
    ("kozijnherstel", "/kozijnherstel", "Kozijnherstel"),
    ("kozijnwrappen", "/kozijnwrappen", "Kozijnwrappen"),
    ("blog/index", "/blog", "Blog"),
]

FOOTER = [("index", "/", "Overzicht")] + NAV + [
    ("over-deze-site", "/over-deze-site", "Over deze site"),
    ("privacy", "/over-deze-site#privacy", "Privacy"),
]

# iWrap staat op één plek gedefinieerd, want reviewscore en aantal veranderen.
# Deze gegevens komen terug in de auteursregel onder elk artikel, in de footer en
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
    "pitch": (
        "Al " + IWRAP_JAREN + " jaar gespecialiseerd in het herstellen van kunststof "
        "kozijnen met Renolit folie, door heel Nederland. Wij besteden niets uit."
    ),
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
    kaarten = [r for r in IWRAP["reviews"] if 120 <= len(r["tekst"]) <= 230][:aantal]
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

# Het beeldmerk: een kozijn van voren, met de onderdorpel in goud. Dat is precies
# het verhaal van de site — de dorpel is bijna altijd het eerst versleten, en goud
# staat voor de nieuwe folie. Leesbaar tot 16px, waar een fijnere tekening dichtslibt.
FAVICON = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
    "<rect width='64' height='64' rx='14' fill='%2315211C'/>"
    "<path d='M14 12h36v36H14z M22 20v20h20V20z' fill='%23E4EDE7' fill-rule='evenodd'/>"
    "<path d='M14 40h36v8H14z' fill='%232F7355'/></svg>"
)

WORDMARK = (
    '<span class="w1">kozijn</span>'
    '<span class="w2">wrap<span class="tld">.nl</span></span>'
)

# Staat onder de merknaam in de footer. Eén plek, dus makkelijk te wisselen.
SLOGAN = "Weet wat je kozijn nodig heeft"

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
    for f in sorted((ROOT / "css").glob("*.css")):
        h.update(f.read_bytes())
    return h.hexdigest()[:8]


def fonts_href(extra_montserrat, ver):
    """De lettertypen staan op de site zelf (css/fonts.css, fonts/): zo gaat het
    IP-adres van een bezoeker niet naar Google en is er geen cookiebanner nodig."""
    uit = '<link rel="stylesheet" href="/css/fonts.css?v=%s">\n' % ver
    if extra_montserrat:
        uit += '<link rel="stylesheet" href="/css/fonts-montserrat.css?v=%s">\n' % ver
    return uit


def blog_menu():
    """Artikelen voor het uitklapmenu, gegroepeerd en op volgorde.

    Komt uit de bronbestanden zelf, zodat een nieuw artikel automatisch in de
    navigatie verschijnt zonder dat hier iets bij hoeft.
    """
    groepen = {"herstel": [], "wrappen": []}
    for path in SRC.glob("blog/*.html"):
        meta, _ = read_page(path)
        if not meta.get("navLabel"):
            continue
        groepen[meta.get("groep", "herstel")].append(
            (meta.get("orde", 99), meta["navLabel"], url_for(meta["slug"]))
        )
    for g in groepen.values():
        g.sort()
    return groepen


def render_nav(slug):
    current = "blog/index" if slug.startswith("blog/") else slug
    slogan_regel = (
        '      <p class="brand-slogan">%s</p>\n' % SLOGAN if slug == "index" else ""
    )
    groepen = blog_menu()

    def kolom(titel, items):
        regels = "\n".join(
            '            <li><a href="%s">%s</a></li>' % (u, label) for _, label, u in items
        )
        return (
            '          <div class="dd-col">\n'
            '            <p class="dd-kop">%s</p>\n'
            '            <ul>\n%s\n            </ul>\n'
            "          </div>" % (titel, regels)
        )

    links = []
    for s_, u, label in NAV:
        cls = 'class="current" ' if s_ == current else ""
        if s_ != "blog/index":
            links.append('      <a %shref="%s">%s</a>' % (cls, u, label))
            continue
        # De blogartikelen waren alleen via het overzicht te vinden. Dit paneel
        # laat vanuit elke pagina zien wat er is, gegroepeerd per onderwerp.
        links.append(
            '      <div class="has-dd">\n'
            '        <a %shref="%s" aria-haspopup="true">%s <span class="dd-caret" aria-hidden="true">&#9662;</span></a>\n'
            '        <div class="dd">\n'
            '          <div class="dd-cols">\n%s\n%s\n          </div>\n'
            '          <a class="dd-alle" href="/blog">Alle artikelen &rarr;</a>\n'
            "        </div>\n"
            "      </div>"
            % (cls, u, label,
               kolom("Kozijnherstel", groepen["herstel"]),
               kolom("Kozijnwrappen", groepen["wrappen"]))
        )

    offerte = (
        '    <a class="nav-cta" href="%s?utm_source=kozijnwrap.nl&amp;utm_medium=header" '
        'target="_blank" rel="noopener">\n'
        '      <span class="nav-cta-sub">Uitvoerende partij</span>\n'
        '      <span class="nav-cta-main">Offerte bij %s <span aria-hidden="true">&rarr;</span></span>\n'
        "    </a>" % (IWRAP["offerte"], IWRAP["naam"])
    )

    return (
        '<header class="site">\n'
        '  <div class="nav">\n'
        '    <div class="brand-lockup">\n'
        '      <a class="brand" href="/" aria-label="kozijnwrap.nl, naar de homepage">%s</a>\n'
        '%s'
        '    </div>\n'
        '    <div class="nav-right">\n'
        '    <nav class="navlinks" aria-label="Hoofdnavigatie">\n'
        "%s\n"
        "    </nav>\n"
        "%s\n"
        "    </div>\n"
        "  </div>\n"
        "</header>" % (WORDMARK, slogan_regel, "\n".join(links), offerte)
    )


def render_footer(slug):
    current = "blog/index" if slug.startswith("blog/") else slug
    links = " · ".join(
        '<a href="%s">%s</a>' % (u, label) for s, u, label in FOOTER if s != current
    )
    return (
        "<footer>\n"
        '  <div class="wrap">\n'
        '    <div class="fbrand">\n'
        "      <strong>kozijnwrap.nl</strong>\n"
        '      <p class="fslogan">%s</p>\n'
        "      <p>Uitleg over het herstellen en wrappen van kozijnen, zodat je weet "
        "waar je aan begint voordat je een offerte aanvraagt.</p>\n"
        '      <p class="fby">Gemaakt door <a href="%s?utm_source=kozijnwrap.nl&amp;utm_medium=footer" '
        'target="_blank" rel="noopener">%s</a>, specialist in kozijnherstel met Renolit folie.</p>\n'
        "    </div>\n"
        '    <div class="flinks">%s</div>\n'
        "  </div>\n"
        "</footer>" % (SLOGAN, IWRAP["site"], IWRAP["naam"], links)
    )


def render_author_box(slug):
    """Auteursregel onder elk blogartikel.

    De artikelen waren tot nu toe anoniem: je kon er vier lezen zonder te weten
    wie ze geschreven had. Dat is zonde van het vertrouwen — juist het feit dat
    dit uit de praktijk komt maakt het advies geloofwaardig — en het laat de
    lezer zonder merknaam achter op het moment dat hij verder gaat zoeken.
    """
    if not slug.startswith("blog/") or slug == "blog/index":
        return ""
    return (
        '\n<aside class="author-box">\n'
        '  <div class="wrap">\n'
        '    <div class="author-inner">\n'
        '      <span class="author-mark" aria-hidden="true">iW</span>\n'
        "      <div>\n"
        '        <p class="author-name">Geschreven door <strong>%s</strong></p>\n'
        "        <p>%s</p>\n"
        '        <p class="author-links">\n'
        '          <a href="%s?utm_source=kozijnwrap.nl&amp;utm_medium=auteur" target="_blank" rel="noopener">Bekijk %s.nl →</a>\n'
        '          <a href="%s" target="_blank" rel="noopener">★ <span data-rv="score">%s</span> uit <span data-rv="aantal">%s</span> Google-reviews</a>\n'
        "        </p>\n"
        "      </div>\n"
        "    </div>\n"
        "  </div>\n"
        "</aside>\n"
        % (
            IWRAP["naam"],
            IWRAP["pitch"],
            IWRAP["site"],
            IWRAP["naam"].lower(),
            IWRAP["reviews_url"],
            IWRAP["reviews_score"],
            IWRAP["reviews_aantal"],
        )
    )


def render_head(meta, ver):
    url = SITE + url_for(meta["slug"])
    og_title = meta.get("ogTitle") or meta["title"]
    og_desc = meta.get("ogDescription") or meta["description"]
    # Nieuwe bestandsnaam bij elke herziening: /images/ staat op een cache van een
    # jaar met immutable, dus onder dezelfde naam zou de oude afbeelding blijven hangen.
    img = SITE + "/images/og-image-v2.jpg"

    # De losse .html-URL's uit de oorspronkelijke structured data meeschrijven
    # naar de schone URL's, zodat canonical en schema niet uit elkaar lopen.
    jsonld = json.dumps(meta.get("jsonld", []), ensure_ascii=False)
    jsonld = jsonld.replace(".html", "").replace(SITE + "/blog/\"", SITE + "/blog\"")
    schema = json.loads(jsonld)
    for b in schema:
        # De artikelen stonden op naam van de site zelf, een uitgever zonder
        # gezicht. iWrap is de partij met de ervaring; dat hoort in het schema
        # te staan, net als in de auteursregel onder het artikel.
        if b.get("@type") == "BlogPosting":
            b["author"] = {"@type": "Organization", "name": IWRAP["naam"], "url": IWRAP["site"]}
    blocks = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>'
        % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        for b in schema
    )

    css = "\n".join(
        '<link rel="stylesheet" href="/css/%s.css?v=%s">' % (name, ver) for name in meta["css"]
    )
    if meta.get("noindex"):
        css = '<meta name="robots" content="noindex">\n' + css

    # De hero-achtergrond op de homepage is het LCP-element: alvast ophalen.
    preload = ""
    if meta["slug"] == "index":
        preload = (
            '\n<link rel="preload" as="image" href="/images/proces-squeegee.webp" '
            'type="image/webp" fetchpriority="high">'
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
{fonts}{css}{preload}""".format(
        title=meta["title"],
        desc=meta["description"],
        url=url,
        favicon=FAVICON,
        ogtype=meta.get("ogType", "website"),
        ogtitle=og_title,
        ogdesc=og_desc,
        img=img,
        jsonld=blocks,
        fonts=fonts_href(meta.get("fonts") == "Montserrat", ver),
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
        auteur = render_author_box(meta["slug"])
        live = "\n" + LIVE_REVIEWS if ("data-rv" in body + auteur or "iwrapReviews" in body) else ""
        out = ROOT / (meta["slug"] + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            "<!DOCTYPE html>\n"
            '<html lang="nl">\n'
            "<head>\n%s\n</head>\n"
            '<body class="%s">\n\n'
            '<a class="skip" href="#inhoud">Naar de inhoud</a>\n\n'
            "%s\n\n"
            '<main id="inhoud">\n\n%s\n%s\n</main>\n\n'
            "%s\n%s%s\n"
            "</body>\n"
            "</html>\n"
            % (
                render_head(meta, ver),
                meta["bodyClass"],
                render_nav(meta["slug"]),
                body,
                auteur,
                render_footer(meta["slug"]),
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
