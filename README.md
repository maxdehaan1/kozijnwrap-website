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

## De indeling (november 2026)

Max (16 november 2026): "het doel moet duidelijk zijn en uiteindelijk is het belangrijkst dat
het complementair is aan de iwrap website." Daarom is de site ingedeeld rond de vraag van de
bezoeker, niet rond diensten. **kozijnwrap.nl zoekt uit wat je kozijn nodig heeft, iwrap.nl
doet het herstel.** Elke pagina hoort bij één stap van die route:

| Stap | Pagina | Wat hij doet |
|---|---|---|
| 1. Herken wat je ziet | `/wat-zie-je` | Tien dingen die je aan een kozijn kunt zien, met foto, wat het is en wat je kunt doen. Elke klacht krijgt een uitkomst. |
| 2. Vergelijk je opties | `/vergelijken` | Herstellen, nieuwe kleur (wrappen), schilderen en vervangen naast elkaar: wanneer, kosten (zonder bedragen), overlast, hoe lang het meegaat. |
| 3. Kies | `/keuzehulp` | Vier vragen, één uitkomst. |
| 4. Laten doen | iwrap.nl | Herstel nodig? Dan gaat de bezoeker naar het offerteformulier van iwrap.nl, met de klacht erbij. |

Daarnaast de twee optiepagina's (`/kozijnherstel`, `/kozijnwrappen`), de kennisbank (`/blog`,
in drie groepen) en `/over-deze-site`. De homepage laat de route in het klein zien.

**Hoe het een geheel wordt (vaste onderdelen, in `build.py` en `css/onderdelen.css`):**
- **Uitkomstlabels**: overal dezelfde gekleurde labels voor waar iets op uitkomt: mint =
  herstellen (wat iWrap doet), en neutraal voor nieuwe kleur, schilder en vervangen. Op de
  klachten, in de vergelijking, in de keuzehulp en bij de artikelen.
- **Eén set lijniconen** (`ICONEN` in `build.py`), voor klachten, opties en de route.
- **Hetzelfde 3D-kozijn als iwrap.nl**: de hero (zie hieronder), de nieuwe kleur als schuif op
  /kozijnwrappen (crème en antraciet) en de drie vaste stappen op /kozijnherstel (toplaag eraf,
  reinigen, nieuwe folie). Gerenderd uit de 3D-animatie van iwrap.nl.
- **Dezelfde klachtfoto's als iwrap.nl**, zodat iemand op beide sites hetzelfde herkent.
- **"Volgende stap"** onderaan elke pagina, naar de logische volgende stap van de route, en
  de **iWrap-brug**: herstel nodig, dan iWrap, met het logo, het reviewcijfer en de knop
  naar het offerteformulier.
- **Artikelen**: bovenaan "In dit artikel" (uit de koppen) en de leestijd, onderaan
  verwante artikelen en de brug.

**De hero: "Herstellen of wrappen?"** (Max, 17 november 2026: de hero moet voor déze site werken
en het verschil tussen wrappen en herstellen en de opties laten zien). Links het 3D-kozijn, rechts
de vier keuzes. Elke keuze speelt een eigen kort verhaal, live getekend met de motor van iwrap.nl:
herstellen (oude folie eraf, nieuwe erop, zelfde kleur), wrappen (antraciet over een goed crème
kozijn), schilderen (verfroller, dan drie jaar later bladdert het) en vervangen (het tocht, het
kozijn gaat eruit, er zakt een nieuw in). Linksboven in beeld staat wat je ziet. Hij speelt de vier
na elkaar zodra hij in beeld is en pauzeert daarbuiten; een klik op een keuze speelt die keuze. Er
is een pauzeknop. Bij "minder beweging" staat per keuze het eindbeeld stil; zonder WebGL2 wisselen
foto's (`images/keuze-*.jpg`). Het startbeeld (`images/keuze-start-*`) staat er tot het canvas
tekent. Bron: `beweging/3d kozijn/kozijn-keuze.js` in iwrap-project, gekopieerd naar
`js/kozijn-keuze.js`; de motor zelf is `js/kozijn-3d.js` (dezelfde als op iwrap.nl). Na een
wijziging daar: beide bestanden opnieuw kopiëren en de beelden opnieuw maken (zie de LEES MIJ daar).

**Codes in de bron** (`src/pages/`), door `build.py` vervangen:

| Code | Wordt |
|---|---|
| `{{schuif:voor\|na\|label voor\|label na\|alt voor\|alt na[\|positie[\|klasse]]}}` | De voor/na-schuif (`js/voorna.js`). Beelden als `<naam>-800.webp`, `-1400.webp`, `-1400.jpg`, 4:3. Klasse `kleur`: wit label in plaats van terracotta. |
| `{{uit:herstel}}` | Een uitkomstlabel: `herstel`, `kleur`, `schilder`, `vervangen`, `glas`, `schoon` (`UITKOMST`). |
| `{{icoon:i-zon}}`, `{{icoon:i-zon\|icoon klein}}` | Een lijnicoon uit `ICONEN`. |
| `{{offerte:medium}}`, `{{offerte:medium\|klacht}}` | De link naar het offerteformulier van iwrap.nl, met utm-codes en de klacht. |
| `{{route}}`, `{{levensduur}}` | De vier stappen; de levensduur van kozijn en folie. |
| `{{volgende}}` | "Volgende stap" voor deze pagina (`VOLGENDE`), met de route in het klein. |
| `{{brug}}`, `{{brug:medium\|Kop}}`, `{{brug:medium\|Kop\|reviews}}` | De brug naar iWrap, eventueel met drie reviews. |
| `{{kennisbank}}`, `{{kennisbank:kort}}`, `{{artikelen:blog/a,blog/b}}` | De kennisbank per thema, kort (homepage), of losse tegels. |

De pagina `/keuzehulp` begint bij vraag twee met `?materiaal=kunststof` of `onbekend` (en
toont meteen de uitkomst bij `aluminium` en `hout`): zo werkt de eerste vraag op de homepage.
Alle knoppen naar iWrap hebben `utm_campaign=herstel`; `vercel.json` van iwrap.nl stuurt die
door naar `/offerte` (en `herstel-zakelijk` naar de pagina voor VvE's).

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

Een **artikel** komt vanzelf in de kennisbank (`/blog`) zodra je in het metadatablok
`thema` (`herkennen`, `kiezen` of `kleur`, zie `THEMAS`), `orde` (plek binnen het thema) en
`kaart` (de korte tekst op de tegel) invult. De titel komt uit de `<h1>`. Leestijd, "In dit
artikel", verwante artikelen en de brug zet `build.py` er zelf bij.

## Structuur

```
build.py              Generator: bouwt src/pages/ naar de root
vercel.json           cleanUrls, cachekoppen, securitykoppen
src/pages/            De bron van elke pagina (metadata + inhoud)

index.html            Homepage: herstellen of wrappen? (3D), de route (gegenereerd)
wat-zie-je.html       Stap 1: elke klacht met foto en uitkomst       (gegenereerd)
vergelijken.html      Stap 2: de vier opties naast elkaar             (gegenereerd)
keuzehulp.html        Stap 3: vier vragen, één uitkomst               (gegenereerd)
kozijnherstel.html    Herstellen, het werk dat iWrap doet             (gegenereerd)
kozijnwrappen.html    Wrappen: eerst de vraag of het herstel is       (gegenereerd)
over-deze-site.html   Wie hier achter zit, en privacy                 (gegenereerd)
404.html              Niet gevonden, met de route                     (gegenereerd)
blog/                 Kennisbank + 10 artikelen                       (gegenereerd)
sitemap.xml                                                           (gegenereerd)

css/
  style.css           Basis: kleuren, letters, kop en voet, .callout
  onderdelen.css      De vaste onderdelen (knoppen, labels, schuif, route, brug, tegels)
  home.css            Alleen de homepage
  content.css         Tekstpagina's: koppen, lijsten, foto's, veelgestelde vragen
  blog.css            Artikelen: kruimelpad, diagrammen, slotkader
  keuzehulp.css       Alleen de keuzehulp
js/
  voorna.js           De voor/na-schuif (op /kozijnwrappen)
  kozijn-3d.js        De 3D-motor van iwrap.nl (kopie; bron in iwrap-project/beweging/3d kozijn)
  kozijn-keuze.js     De hero: vier korte 3D-verhalen en de speler (kopie, zelfde bron)
images/               Elke foto als .webp met een .jpg ernaast als terugval
  keuze-*             Startbeeld van de hero, en per keuze het eindbeeld (zonder WebGL)
  kozijn3d-*.webp     Het 3D-kozijn van iwrap.nl: hersteld en antraciet (de schuif op /kozijnwrappen)
  stap-*.webp         De drie stappen uit de 3D-werkwijze van iwrap.nl
  symptoom-*.webp     Dezelfde klachtfoto's als op iwrap.nl
  og-image-v3.jpg     Deelafbeelding. Geef die bij elke herziening een nieuw volgnummer:
                      /images/ staat op een cache van een jaar met immutable.
```

## Bewegingen

De scroll-onthulling van secties draait op `animation-timeline: view()` — dus volledig in
CSS, zónder JavaScript. Dat is een bewuste keuze: een onthulling die van een script afhangt
kan inhoud onzichtbaar laten als dat script niet draait, en dat risico is een decoratie niet
waard. Zichtbaar is nu de standaard; browsers zonder ondersteuning tonen alles gewoon
statisch. Alles staat achter `prefers-reduced-motion: no-preference`.

## Huisstijl

Sinds 16 november 2026 **dezelfde stijl als iwrap.nl en houtnerffolie.nl** ("iets meer Apple"):
licht en rustig, de kleuren van iWrap (mint `#a3cdc2`, donker mint `#2f5a50` voor knoppen en
links, mint `#3f7468` als tekstkleur, papier `#f7f6f3`, antraciet `#22262a`), een zachte
mintgloed bovenaan elke pagina, een wit doorschijnend menu dat blijft staan (op een telefoon
scrolt het mee), witte vlakken met een zachte rand, en een lichte voet. Elke paginakop is licht
(daarvoor had elk thema een eigen gekleurde band); donker mint is er alleen voor wat je moet doen: de knoppen, de keuzehulp op de homepage, de iWrap-stap van de route en de optie herstellen. De oude variabelenamen (`--cream`, `--anthracite`, `--accent`) staan nog in
`style.css` maar wijzen naar de nieuwe kleuren.

- **Letters**: het lettertype van het apparaat zelf (San Francisco op een Mac en iPhone,
  Segoe UI op Windows, Roboto op Android), `--sans` in `style.css`. Koppen vet en strak,
  lopende tekst 18px. Er wordt geen lettertype meer geladen; `css/fonts*.css` en `fonts/`
  (Karla, Fraunces, Montserrat) worden niet meer gebruikt.
- **Voor oudere bezoekers**: kleine teksten minstens 15px, grijs dat 7:1 haalt, knoppen
  minstens 50px hoog en geen piepkleine hoofdletters met spaties ertussen (labels als
  "Kozijnherstel" zijn gewone letters in het mint).
- **Woordmerk**: de naam ís het logo: `kozijn` in mint (normaal gewicht) direct gevolgd door
  `wrap` in antraciet (extra vet), met `.nl` klein erachter. Het blijft échte tekst (geen
  plaatje), dus voorleessoftware en zoekmachines lezen de naam gewoon. Markup staat als
  `WORDMARK` in `build.py`, opmaak onder `.brand` in `style.css`; die twee horen bij elkaar.
- **Deelafbeelding**: `images/og-image-v3.jpg` (woordmerk, slogan en de werkfoto, in de
  nieuwe stijl).
- **Favicon**: wél een beeldmerk, want een woordmerk is op 16px onleesbaar. Een kozijn van
  voren met de onderdorpel in mint, op donker mint: de dorpel is bijna altijd het eerst
  versleten. Staat als `FAVICON` in `build.py`.
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
