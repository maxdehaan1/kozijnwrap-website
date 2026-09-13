# kozijnwrap.nl

Adviessite over kozijnherstel en kozijnwrappen, gemaakt vanuit iWrap.

## Wat deze site moet doen

iwrap.nl staat al bovenaan op "kunststof kozijnen herstellen" en vangt de mensen die al
weten wat ze zoeken. Deze site vangt de fase daarvóór: iemand die ziet dat zijn kozijnen
er niet meer uitzien en nog niet weet dat folieherstel bestaat. Die zoekt op wat hij
ziet ("folie laat los", "dorpel verkleurd") of op het woord dat hij kent ("wrappen").

**De site kiest, iwrap.nl offreert.** Er staat bewust geen formulier op kozijnwrap.nl —
elke conversie loopt via het bestaande offerteformulier op iwrap.nl, zodat er geen tweede
inbox en geen tweede proces ontstaat. De keuzehulp doet de diagnose die anders per mail
beantwoord zou moeten worden.

De doelgroep is de **kleine particuliere klus** (een paar dorpels, rond de €500): het beste
rendement per uur, geen aanbesteding, snel betaald. De site zegt daarom expliciet dat een
kleine opdracht welkom is — vrijwel niemand neemt dat uit zichzelf aan.

Wrappen doet iWrap niet zelf. Die helft van de site is er om wrappen-zoekers te vangen die
eigenlijk herstel nodig hebben; de échte wrapvraag loopt eerlijk dood.

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
keuzehulp.html        4 vragen → uitkomst, de conversiemotor   (gegenereerd)
kozijnherstel.html    Kozijnherstel + aanbeveling iWrap         (gegenereerd)
kozijnwrappen.html    Kozijnwrappen, eerlijk doodlopend         (gegenereerd)
404.html              Niet-gevonden-pagina                      (gegenereerd)
blog/                 Overzicht + 7 artikelen                   (gegenereerd)
sitemap.xml                                                     (gegenereerd)

css/
  style.css           Gedeeld: variabelen, typografie, header, footer, .callout / .note
  home.css            Alleen index.html (hero, de twee kleurblokken, polaroid)
  content.css         Tekstpagina's en blog (hero-band, checklists, feiten, partnerblokken)
  blog.css            Blogoverzicht, artikelen, diagrammen
  keuzehulp.css       Alleen de keuzehulp

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
- Reviewcijfers iWrap (4,9★, 81 reviews) staan hardcoded op kozijnherstel.html — bijwerken
  als het aantal wijzigt. Net als de bedragen in de keuzehulp (`PRIJS` in
  `src/pages/keuzehulp.html`), het kostenartikel en het blok "Ook als het maar om een paar
  dorpels gaat".
- Nog geen aparte "Over deze site"-pagina. De disclosure staat nu alleen op de
  kozijnwrappen-pagina ("Deze site is gemaakt vanuit iWrap").
- Geen analytics. De uitgaande links naar iwrap.nl hebben wel UTM-tags
  (`utm_medium=keuzehulp`), dus in de statistieken van iwrap.nl is te zien hoeveel
  aanvragen hiervandaan komen.
- De symptoompagina's staan er (folie laat los, kozijn verkleurd, onderdorpel, schilderen).
  Kandidaten voor een volgende ronde: krassen en stootschade, kozijn schoonmaken, en
  "kozijn 20 jaar oud — vervangen of niet". Schrijf ze vanuit wat iemand ziét, niet vanuit
  de vakterm: daar zit de kleine particuliere klus, en daar schrijven de grote
  kozijnleveranciers niet over omdat die vervangingsopdrachten willen.
- houtnerffolie.nl overlapt met twee blogartikelen hier. Check in Search Console of die site
  verkeer krijgt: zo ja, smal houden op het product; zo nee, 301 hierheen.
