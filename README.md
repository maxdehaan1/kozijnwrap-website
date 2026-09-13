# kozijnwrap.nl

Adviessite over kozijnherstel en kozijnwrappen. Splitst bezoekers in twee paden:
kozijnherstel (kunststof kozijnen met Renolit folie — aanbevolen partner: iWrap, op basis van
specialisatie en reviews) en kozijnwrappen (omkleuren van nog goede aluminium/kunststof
kozijnen, partner nog te kiezen). Daarnaast een blog met achtergrondartikelen.

## Bewerken en bouwen

De HTML in de repo-root is **gegenereerd** — bewerk die bestanden niet met de hand.
De bron staat in `src/pages/`, de gedeelde `<head>`, navigatie en footer staan in `build.py`.

```bash
python3 build.py
```

Dat schrijft alle pagina's naar de root en genereert `sitemap.xml` opnieuw. Draai het na
élke wijziging in `src/pages/` of in `css/` — de stylesheets krijgen een versiehash mee in
de URL, en die wordt bij het bouwen bepaald.

Elke bron in `src/pages/` begint met een JSON-blok in een HTML-comment (titel, omschrijving,
body-klasse, welke stylesheets, structured data), gevolgd door de inhoud van de pagina.
Een nieuwe pagina toevoegen = één bestand in `src/pages/` zetten en bouwen; staat hij ook in
de navigatie, dan zet je hem in de lijst `NAV` bovenin `build.py`.

## Structuur

```
build.py              Generator: bouwt src/pages/ naar de root
vercel.json           cleanUrls, cachekoppen, securitykoppen
src/pages/            De bron van elke pagina (metadata + inhoud)

index.html            Landingspagina — de tweesplitsing        (gegenereerd)
kozijnherstel.html    Kozijnherstel + aanbeveling iWrap         (gegenereerd)
kozijnwrappen.html    Kozijnwrappen + nog open aanbeveling      (gegenereerd)
404.html              Niet-gevonden-pagina                      (gegenereerd)
blog/                 Overzicht + 7 artikelen                   (gegenereerd)
sitemap.xml                                                     (gegenereerd)

css/
  style.css           Gedeeld: variabelen, typografie, header, footer, .callout / .note
  home.css            Alleen index.html (hero, de twee kleurblokken, polaroid)
  content.css         Tekstpagina's en blog (hero-band, checklists, feiten, partnerblokken)
  blog.css            Blogoverzicht, artikelen, diagrammen

images/               Elke foto als .webp met een .jpg ernaast als terugval
```

## Huisstijl

- **Letters**: Fraunces (koppen) en Karla (lopende tekst). Montserrat staat alléén op
  kozijnherstel.html, voor het iWrap-blok — dat leent bewust de huisstijl van de partner.
- **Kleur**: crème (`--cream`) voor kozijnherstel, antraciet (`--anthracite`) voor
  kozijnwrappen, goud als accent door de hele site.
- **Let op bij het goud**: `--accent` is voor lijnen, randen en iconen. Zodra er tekst
  bovenop komt gebruik je `--accent-deep` (op licht) of `--accent-light` (op donker) —
  `--accent` haalt met wit maar 3,4:1 en zakt daarmee onder de toegankelijkheidsnorm.

## URL's

`vercel.json` heeft `cleanUrls` aan: de site draait op `/kozijnherstel`, niet op
`/kozijnherstel.html`. Interne links, canonicals en de sitemap zijn daarop afgestemd.
Gebruik in de bronbestanden root-relatieve links (`/blog/renolit-folie-uitgelegd`).

## Openstaand

- **Het domein `kozijnwrap.nl` is nog niet aan Vercel gekoppeld** — het wijst op dit moment
  naar een parkeerpagina, terwijl alle canonicals en de sitemap er al naar verwijzen.
  Zolang dat zo is, levert de SEO niets op.
- Aanbevolen partij voor kozijnwrappen nog niet gekozen (placeholder op kozijnwrappen.html).
- Reviewcijfers iWrap (4,9★, 81 reviews) staan hardcoded op kozijnherstel.html — bijwerken
  als het aantal wijzigt.
- Geen contactgegevens en geen conversiepad: de enige actie op de site is een mailto naar
  iWrap, wat wringt met de onafhankelijke toon. Eigen mailadres + een "Over deze site"-pagina
  zou dat oplossen.
- Geen analytics, dus er is nog niets te meten.
