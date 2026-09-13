#!/usr/bin/env python3
"""
Bouwt de statische site uit src/pages/ naar de repo-root.

Elke bron in src/pages/ bestaat uit een JSON-blok in een HTML-comment (de
paginagegevens) gevolgd door de eigenlijke inhoud. Alles wat op elke pagina
hetzelfde is — de <head>, de navigatie, de footer — staat alleen hier.

Gebruik:  python3 build.py
"""

import json
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "pages"
SITE = "https://kozijnwrap.nl"

# Navigatie en footer worden hieruit gegenereerd; de volgorde is de volgorde
# waarin ze in de balk staan.
NAV = [
    ("index", "/", "Overzicht"),
    ("keuzehulp", "/keuzehulp", "Keuzehulp"),
    ("kozijnherstel", "/kozijnherstel", "Kozijnherstel"),
    ("kozijnwrappen", "/kozijnwrappen", "Kozijnwrappen"),
    ("blog/index", "/blog", "Blog"),
]

FAVICON = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
    "<rect width='64' height='64' rx='14' fill='%2324272a'/>"
    "<rect x='10' y='10' width='19' height='19' rx='2' fill='%23f1e8d3'/>"
    "<rect x='35' y='10' width='19' height='19' rx='2' fill='%2334383b'/>"
    "<rect x='10' y='35' width='19' height='19' rx='2' fill='%2334383b'/>"
    "<rect x='35' y='35' width='19' height='19' rx='2' fill='%23f1e8d3'/></svg>"
)

LOGO_MARK = (
    '<svg class="logo-mark" width="26" height="26" viewBox="0 0 64 64" aria-hidden="true">'
    '<rect width="64" height="64" rx="14" fill="#24272a"/>'
    '<rect x="10" y="10" width="19" height="19" rx="2" fill="#f1e8d3"/>'
    '<rect x="35" y="10" width="19" height="19" rx="2" fill="#34383b"/>'
    '<rect x="10" y="35" width="19" height="19" rx="2" fill="#34383b"/>'
    '<rect x="35" y="35" width="19" height="19" rx="2" fill="#f1e8d3"/></svg>'
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
    for f in sorted((ROOT / "css").glob("*.css")):
        h.update(f.read_bytes())
    return h.hexdigest()[:8]


def fonts_href(extra_montserrat):
    fams = [
        "family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700",
        "family=Karla:wght@400;500;700",
    ]
    if extra_montserrat:
        fams.append("family=Montserrat:wght@400;500;600;700")
    return "https://fonts.googleapis.com/css2?" + "&".join(fams) + "&display=swap"


def render_nav(slug):
    current = "blog/index" if slug.startswith("blog/") else slug
    links = "\n".join(
        '      <a %shref="%s">%s</a>' % ('class="current" ' if s == current else "", u, label)
        for s, u, label in NAV
    )
    return (
        '<header class="site">\n'
        '  <div class="nav">\n'
        '    <a class="brand" href="/">%s kozijnwrap.nl</a>\n'
        '    <nav class="navlinks" aria-label="Hoofdnavigatie">\n'
        "%s\n"
        "    </nav>\n"
        "  </div>\n"
        "</header>" % (LOGO_MARK, links)
    )


def render_footer(slug):
    current = "blog/index" if slug.startswith("blog/") else slug
    items = [(s, u, label) for s, u, label in NAV if s != current]
    # Staat bewust niet in de hoofdnavigatie — wel op elke pagina bereikbaar,
    # want de herkomst van de site hoort niet op één pagina verstopt te zitten.
    if slug != "over-deze-site":
        items.append(("over-deze-site", "/over-deze-site", "Over deze site"))
    links = " · ".join('<a href="%s">%s</a>' % (u, label) for _, u, label in items)
    return (
        "<footer>\n"
        '  <div class="wrap">\n'
        '    <div class="fbrand">\n'
        "      <strong>kozijnwrap.nl</strong>\n"
        "      <p>Uitleg over het herstellen en wrappen van kozijnen, zodat je weet "
        "waar je aan begint voordat je een offerte aanvraagt.</p>\n"
        "    </div>\n"
        '    <div class="flinks">%s</div>\n'
        "  </div>\n"
        "</footer>" % links
    )


def render_head(meta, ver):
    url = SITE + url_for(meta["slug"])
    og_title = meta.get("ogTitle") or meta["title"]
    og_desc = meta.get("ogDescription") or meta["description"]
    img = SITE + "/images/og-image.jpg"

    # De losse .html-URL's uit de oorspronkelijke structured data meeschrijven
    # naar de schone URL's, zodat canonical en schema niet uit elkaar lopen.
    jsonld = json.dumps(meta.get("jsonld", []), ensure_ascii=False)
    jsonld = jsonld.replace(".html", "").replace(SITE + "/blog/\"", SITE + "/blog\"")
    blocks = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>'
        % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        for b in json.loads(jsonld)
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
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
        fonts=fonts_href(meta.get("fonts") == "Montserrat"),
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
        out = ROOT / (meta["slug"] + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            "<!DOCTYPE html>\n"
            '<html lang="nl">\n'
            "<head>\n%s\n</head>\n"
            '<body class="%s">\n\n'
            '<a class="skip" href="#inhoud">Naar de inhoud</a>\n\n'
            "%s\n\n"
            '<main id="inhoud">\n\n%s\n\n</main>\n\n'
            "%s\n\n"
            "</body>\n"
            "</html>\n"
            % (
                render_head(meta, ver),
                meta["bodyClass"],
                render_nav(meta["slug"]),
                body,
                render_footer(meta["slug"]),
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
