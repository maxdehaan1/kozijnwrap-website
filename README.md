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
de navigatie, dan zet je hem in de lijst `NAV` bovenin `build.py` (`FOOTER` staat daar
direct onder, voor pagina's die alleen onderaan hoeven te staan).

Een **blogartikel** komt vanzelf in het uitklapmenu onder "Blog" te staan zodra je in
het metadatablok `navLabel` (korte menuregel), `groep` (`herstel` of `wrappen`) en
`orde` (volgnummer binnen die kolom) invult. Laat je `navLabel` weg, dan staat het
artikel wel op het blogoverzicht maar niet in het menu.

## Structuur

```
build.py              Generator: bouwt src/pages/ naar de root
vercel.json           cleanUrls, cachekoppen, securitykoppen
src/pages/            De bron van elke pagina (metadata + inhoud)

index.html            Landingspagina — de tweesplitsing        (gegenereerd)
keuzehulp.html        4 vragen → uitkomst, de conversiemotor   (gegenereerd)
kozijnherstel.html    Kozijnherstel, het werk dat iWrap doet   (gegenereerd)
kozijnwrappen.html    Kozijnwrappen, eerlijk doodlopend         (gegenereerd)
over-deze-site.html   Herkomst en disclosure                    (gegenereerd)
404.html              Niet-gevonden-pagina                      (gegenereerd)
blog/                 Overzicht + 10 artikelen                  (gegenereerd)
sitemap.xml                                                     (gegenereerd)

css/
  style.css           Gedeeld: variabelen, typografie, header, footer, .callout / .note
  home.css            Alleen index.html (hero, de twee kleurblokken, polaroid)
  content.css         Tekstpagina's en blog (hero-band, checklists, feiten, partnerblokken)
  blog.css            Blogoverzicht, artikelen, diagrammen
  keuzehulp.css       Alleen de keuzehulp

images/               Elke foto als .webp met een .jpg ernaast als terugval
  og-image-v2.jpg     Deelafbeelding (WhatsApp, LinkedIn). Geef die bij elke herziening
                      een nieuw volgnummer: /images/ staat op een cache van een jaar met
                      immutable, dus onder dezelfde naam blijft de oude hangen.
```

## Bewegingen

De scroll-onthulling van secties draait op `animation-timeline: view()` — dus volledig in
CSS, zónder JavaScript. Dat is een bewuste keuze: een onthulling die van een script afhangt
kan inhoud onzichtbaar laten als dat script niet draait, en dat risico is een decoratie niet
waard. Zichtbaar is nu de standaard; browsers zonder ondersteuning tonen alles gewoon
statisch. Alles staat achter `prefers-reduced-motion: no-preference`.

## Huisstijl

- **Letters**: Fraunces (koppen) en Karla (lopende tekst). Montserrat staat alléén op
  kozijnherstel.html, voor het iWrap-blok — dat leent bewust de eigen huisstijl van iWrap,
  zodat zichtbaar is dat daar het uitvoerende bedrijf aan het woord is.
- **Woordmerk**: de naam ís het logo — `kozijn` in Fraunces cursief boven `wrap.nl` in
  Karla 800, strak gestapeld. De spanning zit in het contrast tussen de lichte schreef en
  de zware schreefloze, niet in een icoon. Het blijft échte tekst (geen plaatje), dus
  voorleessoftware en zoekmachines lezen de naam gewoon. Markup staat als `WORDMARK` in
  `build.py`, opmaak onder `.brand` in `style.css`; die twee horen bij elkaar.
- **Favicon**: wél een beeldmerk, want een woordmerk van twee regels is op 16px
  onleesbaar. Een kozijn van voren met de onderdorpel in goud — de dorpel is bijna altijd
  het eerst versleten. Staat als `FAVICON` in `build.py`.
- **Slogan**: "Weet wat je kozijn nodig heeft" — constante `SLOGAN` in `build.py`. Staat
  als lockup onder het woordmerk in de header (alléén op de homepage), in de footer, en
  op de deelafbeelding.
- **Accentstreep** onder koppen: `.rule` — twee gestapelde balken, kort en zwaar boven
  lang en licht. Dezelfde opbouw als het woordmerk. Verving een handgetekend golfje.
- **Kleur**: diep groen als merkkleur. Dat verbindt deze site met iWrap (salie) en
  houtnerffolie.nl (donkergroen), en het draagt het argument — herstellen in plaats van
  vervangen. Alles loopt via de variabelen in `:root` in `style.css`.
- **Taakverdeling van het groen**: `--accent` voor lijnen, randen, iconen en het cursieve
  deel van het woordmerk; `--accent-deep` overal waar tekst bovenop komt (5,9:1 met wit);
  `--accent-light` voor tekst op de donkere vlakken. De laagste combinatie op de site zit
  op 4,7:1 — boven de norm van 4,5:1. Let op: `--accent` zelf haalt op de achtergrond
  maar 3,8:1 en mag daarom nooit als tekstkleur worden gebruikt, alleen voor randen.
- **Wat níet meekleurt**: de kleurstalen op de wrappen-kaart, de RAL-staaltjes, en de
  materiaalkleuren in de doorsnede-diagrammen (foliekleur, verf, vuil, glas, kozijnprofiel).
  Die stellen echte dingen voor en horen eruit te zien zoals ze zijn.

## URL's

`vercel.json` heeft `cleanUrls` aan: de site draait op `/kozijnherstel`, niet op
`/kozijnherstel.html`. Interne links, canonicals en de sitemap zijn daarop afgestemd.
Gebruik in de bronbestanden root-relatieve links (`/blog/renolit-folie-uitgelegd`).

## Openstaand

- **Het domein `kozijnwrap.nl` is nog niet aan Vercel gekoppeld** — het wijst op dit moment
  naar een parkeerpagina, terwijl alle canonicals en de sitemap er al naar verwijzen.
  Zolang dat zo is, levert de SEO niets op.
- Reviewcijfers en de omschrijving van iWrap staan in het blok `IWRAP` bovenin `build.py`.
  Daaruit komen de auteursregel onder elk blogartikel, de footerregel en de `author` in de
  structured data. Eén plek aanpassen dus. Op kozijnherstel.html staan ze daarnaast nog
  in de lopende tekst — die twee even meenemen als het aantal wijzigt. Net als de bedragen in de keuzehulp — die staan in
  `src/pages/keuzehulp.html` in `PRIJS` (per omvang, bij de uitkomst folieherstel) en in het
  veld `prijs` op de uitkomst `vervangen` — en verder in het kostenartikel en in het blok
  "Ook als het maar om een paar dorpels gaat".
- Geen analytics. De uitgaande links naar iwrap.nl hebben wel UTM-tags
  (`utm_medium=keuzehulp`), dus in de statistieken van iwrap.nl is te zien hoeveel
  aanvragen hiervandaan komen.
- De symptoompagina's staan er (folie laat los, kozijn verkleurd, onderdorpel, schilderen).
  Kandidaten voor een volgende ronde: krassen en stootschade, kozijn schoonmaken, en
  "kozijn 20 jaar oud — vervangen of niet". Schrijf ze vanuit wat iemand ziét, niet vanuit
  de vakterm: daar zit de kleine particuliere klus, en daar schrijven de grote
  kozijnleveranciers niet over omdat die vervangingsopdrachten willen.
- **Er staan geen bedragen meer op de site.** Die zijn eruit gehaald omdat ze alleen
  klopten bij een paar strekkende meter en daarboven niet in te schatten zijn: een
  richtprijs die niet opgaat is verwarrend en schrikt af bij klussen die juist
  overzichtelijk zijn. Hetzelfde geldt op iwrap.nl. Zet er dus ook geen nieuwe
  bandbreedte in — ook niet voor vervangen. Het argument tegen vervangen zit niet in het
  getal maar in wat er níet in zo'n offerte staat: stucwerk aan de dagkanten,
  schilderwerk binnen, vensterbanken en de afvoer van het oude kozijn.
- **Feiten die op meerdere pagina's staan** en dus samen bijgewerkt moeten worden:
  "tien jaar fabrieksgarantie op de folie, vijf jaar op de montage" en "profiel 50–75
  jaar". Houd het bij die ene formulering:
  Renolit folie is één product met één garantietermijn, ongeacht kleur of structuur. Eerder
  stonden er drie verschillende levensduren op de site en dat is voor een klant alleen maar
  verwarrend.
- houtnerffolie.nl blijft de plek voor de diepte: decors, kleuren en specificaties. Het
  artikel [renolit-folie-uitgelegd](src/pages/blog/renolit-folie-uitgelegd.html) legt de
  basis uit en verwijst daarheen in plaats van het over te doen. Ga daar geen kleurenoverzicht
  of specificatietabel bouwen, dan concurreren de twee sites alsnog met elkaar.

## Samenwerking met iwrap.nl

- **De knop na de keuzehulp** gaat naar `iwrap.nl/contact/?utm_source=kozijnwrap.nl&utm_medium=keuzehulp`,
  met `utm_campaign=herstel` (of `herstel-zakelijk` bij "meerdere panden") en, als de klant
  bij vraag 3 iets koos, `klacht=verweerd|laat-los|scheuren`. Zolang iwrap.nl op WordPress
  draait komt de klant op de contactpagina daar. Na de overstap stuurt de nieuwe iwrap.nl
  deze link door naar het offerteformulier (een VvE naar de VvE-pagina), en staat de klacht
  en "kozijnwrap.nl (keuzehulp)" als herkomst in de aanvraag. Die doorverwijzingen staan in
  `vercel.json` van iwrap.nl. Verander de utm-codes hier dus niet zonder ze daar mee te
  veranderen.
- **Het reviewcijfer van iWrap loopt live mee.** Bij het bouwen komt het uit `reviews.json`
  van iwrap.nl (`../iwrap-project/`), via `{{iwrap.reviews_score}}` en
  `{{iwrap.reviews_aantal}}` in de bron; `{{iwrap.reviewkaarten}}` zet er twee echte reviews
  bij. In de browser haalt een klein script (`LIVE_REVIEWS` in `build.py`) daarna de live
  stand op bij `iwrap.nl/api/reviews`, die hem van Google heeft. Zo klopt het aantal ook
  tussen twee builds door. Tot iwrap.nl is overgezet antwoordt alleen
  `iwrap-website.vercel.app`; het script probeert ze allebei.
- **Het domein kozijnwrap.nl** moet in het DNS naar Vercel wijzen (bij GPO hosting):
  A-record `@` naar `76.76.21.21`, CNAME `www` naar `cname.vercel-dns.com`, en het domein
  toegevoegd in het Vercel-project. Op 25 oktober 2026 wees het nog naar de oude hosting en
  stond het domein nog niet in Vercel. De stappen staan in `../iwrap-project/LIVEGANG.md`
  (stap 4), het draaiboek voor de livegang van alle sites.
