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
- **De knop naar iWrap** (`.knop-iwrap`, 19 november 2026): op deze site en op houtnerffolie.nl
  dezelfde, in de knopkleur van iwrap.nl met het beeldmerk van iWrap ervoor (als plaatje in
  `onderdelen.css`, dus elke knop met die klasse krijgt het vanzelf). In de kopbalk "Offerte bij
  iWrap" (op een telefoon "Offerte"), in de blokken "Offerte aanvragen bij iWrap".
- **De familieregel** onderaan elke pagina: "De sites van iWrap", drie kaartjes met elk de naam
  in zijn eigen woordmerk en wat die site doet (`render_familie`). Deze site linkt daar alleen
  naar iwrap.nl, **niet naar houtnerffolie.nl**: de zustersites sturen door naar iWrap, niet naar
  elkaar (Max, 19 november 2026).
- **Het menu** staat tot 1080px breed achter een knop met het woord "Menu" (open: "Sluiten"),
  met grote regels en onderin de knop naar iWrap (`js/menu.js`), net als op iwrap.nl en
  houtnerffolie.nl. De kopbalk blijft ook op een telefoon staan.
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
  menu.js             Het menu op telefoon en tablet (zelfde bestand als op houtnerffolie.nl)
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

Licht en rustig, "iets meer Apple" (sinds 16 november 2026): koppen in Montserrat en lopende
tekst in het lettertype van het apparaat zelf, grote strakke koppen, een zachte gloed bovenaan elke pagina, een wit doorschijnend menu dat
blijft staan (ook op een telefoon), witte vlakken met een zachte rand en een lichte voet.

**Kleur (sinds 17 november 2026).** kozijnwrap.nl heeft een eigen kleur (Max: "voer deze website
uit maar dan met andere kleuren"), en het mint van iWrap staat alleen nog waar iWrap in beeld komt:
de brug onderaan, elke knop en link naar iWrap (`.knop-iwrap`, de knop in het menu, "Dit herken
ik"), de iWrap-stap van de route, het label "Herstellen" en "Dit doet iWrap", en de uitkomst
herstel (in de hero, de vergelijking en de keuzehulp). Zo zie
je meteen wat van de site zelf is en wat van het bedrijf dat het werk doet.

Er zijn vier paletten, allemaal getoetst op 7:1 voor knoppen en grijze tekst:

| Palet | `PALET` | Karakter | Merk | Tekst | Licht | Papier |
|---|---|---|---|---|---|---|
| Nachtblauw | `nacht` | betrouwbaar en rustig, als een consumentengids | `#1f3d63` | `#2b5689` | `#9fbbe0` | `#f6f5f1` |
| **Hemelsblauw** (in gebruik, gekozen door Max) | `hemel` | fris, sluit aan op de lucht in het 3D-beeld | `#175a99` | `#175a99` | `#8ec0ea` | `#f4f7fa` |
| Antraciet en messing | `messing` | chic, architectonisch | `#2a2e33` | `#74572a` | `#d4b97f` | `#f7f5f0` |
| Baksteen | `baksteen` | warm, de Hollandse gevel | `#8f3e24` | `#8f3e24` | `#e2a78c` | `#f8f5f1` |

Hemelsblauw staat in `:root`; een ander palet: zet `PALET` in `build.py` op de naam en bouw opnieuw
(de site krijgt dan `data-palet` op `<html>`; de blokken staan bovenin `css/style.css`). Bij een
blauw palet zijn de grijstinten koel (`--line`, `--voet`, `--spoor`, `--grijs-vlak`, `--streep`),
bij de andere warm. Het favicon kleurt mee; de
deelafbeelding maak je opnieuw met `python3 tools/maak_og.py` (geef hem een nieuw nummer).

De kleuren lopen via variabelen in `:root` (zie het commentaar daar): `--merk` (knoppen, links),
`--merk-hover`, `--merk-tekst` (opschriften, iconen), `--merk-licht` (lijntjes, balkjes),
`--merk-vlak` (zachte vlakjes met donkere tekst), `--merk-zacht`, `--merk-wash`, `--op-donker`
(lichte tekst op `--merk`) en `--schade` (terracotta). Het mint van iWrap: `--iwrap`,
`--iwrap-mint`, `--iwrap-wash` en verder. Zet nergens een losse kleurcode in de opmaak.

- **Letters**: koppen, menu, knoppen, opschriften, labels en het woordmerk in Montserrat, de
  letter van het iWrap-logo (sinds 17 november 2026, net als op iwrap.nl en houtnerffolie.nl;
  `--kop`). Lopende tekst in het lettertype van het apparaat zelf (San Francisco op een Mac en
  iPhone, Segoe UI op Windows, Roboto op Android), `--sans`, 18px. Montserrat staat op de site
  zelf (`fonts/`, één variabel bestand voor alle gewichten, gedeclareerd bovenin
  `css/style.css`) en wordt in de `<head>` vooraf geladen; de terugval `Montserrat-terugval`
  (Arial op maat) zorgt dat er niets verspringt. Op een smal scherm mogen lange woorden in koppen
  afbreken. De teksten in het 3D-beeld (canvas) en de getekende diagrammen blijven in `--sans`.
  **Eén reeks maten** (compositieronde, 19 november 2026, dezelfde als op iwrap.nl), als
  variabelen in `:root` van `css/style.css`: `--h1` `clamp(2.1rem,1.45rem + 2.3vw,3.1rem)`, `--h2`
  `clamp(1.65rem,1.25rem + 1.35vw,2.3rem)` en `--h3` `clamp(1.14rem,1.06rem + .3vw,1.28rem)`: op
  een breed scherm 50 / 37 / 20px, op een telefoon 34 / 26 / 18px. `h1`, `h2` en `h3` krijgen die
  maat in `style.css`; een onderdeel zet er geen eigen maat overheen. Dus ook de homepagekop
  ("Herstellen of wrappen?", eerst 74px), een artikelkop, de brug, de keuzehulp en het blauwe
  vlak met de eerste vraag hebben dezelfde maten. Een kop in een kanttekening (De vuistregel, Even
  eerlijk) en de titel van Volgende stap en van het slotkader in een artikel zijn een `--h3`. In
  een kaart is de titel `1.18rem` (`--kaart-titel`) en de tekst `1.02rem` grijs
  (`--kaart-tekst`): de route, de signalen, de drie stappen, de kennisbank, de artikeltegels, de
  vergelijking en de rest. Alleen de klachtkaarten met een foto hebben een titel van `1.11rem`,
  zodat "Dof, ruw en vol haarscheuren" op één regel past. De inleiding onder een sectiekop is
  `--lede` (19,5px), op een paginakop `--lede-kop` (20px). Een kop breekt op een breed scherm
  nooit op een los woord, en titels in een rij kaarten staan allemaal op één regel. Zijn ze daar te
  lang voor (de artikeltegels, de kennisbank op de homepage, "Zo kijk je" en "Dit lost nieuwe
  folie niet op" op /wat-zie-je), dan staan de regels eronder met subgrid toch op één lijn. De
  vier signalen op /kozijnherstel staan in twee kolommen in plaats van vier smalle (eerst brak
  "Krassen of / stootschade").
- **Regellengte**: lopende tekst niet breder dan zo'n 85 tekens. De tekstkolom van een artikel en
  van de andere tekstpagina's is 660px, op de linkerrand van de inhoud (zie Uitlijning), een alinea
  maximaal `36em`. De inleiding onder een kop en op een paginakop `34em`,
  de tekst in een kanttekening `36em`, de zin onder de vergelijking `35em`. Reken in `em`, niet in
  `ch`: `ch` is in deze letter breder dan een gemiddeld teken (64ch was zo'n 95 tekens).
- **Witruimte**: één sectie-eenheid (`--sectie`: 100px op een breed scherm, 56px op een telefoon)
  tussen twee blokken met dezelfde achtergrond, en aan elke kant van een kleurrand (wit en papier)
  één eenheid. Elk blok in `main` (`.sectie`, `.sectie-dun`, `.volgende`, `.brug`, `.verwant` en
  de tekstsecties) heeft die ruimte boven en onder; volgt het op een blok met dezelfde
  achtergrond, dan valt de ruimte erboven weg (zie "Ritme" bovenin `css/onderdelen.css`). Eerst
  gold die regel ook voor papier na wit, en dan stond de kop van zo'n sectie tegen de kleurrand.
  Onder elke paginakop staat precies één eenheid (de kop houdt die zelf onderin), ook op een
  artikel. Wat als eerste of laatste in een blok staat, voegt geen eigen marge toe; `.ruimte-onder`
  is niet meer nodig. Een kop in de lopende tekst heeft erboven `2em` en eronder `.45em`, zodat hij
  bij de tekst eronder hoort.
- **Compositie**: wat naast elkaar staat, is ongeveer even hoog. Op /kozijnwrappen staan naast
  "Zit er schade op je kunststof kozijn?" één hoge foto en twee gestapelde foto's, even hoog als de
  tekst (eerst drie kleine foto's van half die hoogte). Controleer na een wijziging in de opmaak
  de pagina's op 1440x900, 1366x768 en 390 breed met schermafdrukken die scherm voor scherm worden
  gemaakt (een schermafdruk van de hele pagina in één keer geeft in Chrome afwijkingen), en meet
  koppen met een los woord, rijen kaarttitels, regellengtes en de witruimte tussen blokken (alleen
  100/200 op een breed scherm en 56/112 op een telefoon zijn goed).
- **Voor oudere bezoekers** (leesbaarheid zoals iwrap.nl, 19 november 2026): lopende tekst 18px,
  alle andere zichtbare tekst minstens `.94rem` (15px), ook labels op foto's en balken, de nummers
  van de kleine route en de chip "Dit doet iWrap". Alleen de letters in getekende diagrammen (SVG)
  schalen mee, en het woordmerk is het logo. Grijze tekst (`--sub`) haalt 7:1 op papier, wit, de
  voet en de lichte vlakken: in Hemelsblauw `#424c58` (eerst `#4b5765`, 6,85:1 op papier); de
  andere drie paletten zijn op dezelfde manier een tint donkerder. Knoppen zijn minstens 54px hoog
  (ook de themaknoppen van de kennisbank), de knoppen in de kopbalk 44px. Geen kleine hoofdletters
  met spaties ertussen. De iWrap-stap van de route staat op `--iwrap-hover`, een tint donkerder
  dan de knoppen: dan haalt de mintkleurige link "Offerte bij iWrap" 5,8:1 (eerst 4,47:1). De
  sterren bij de reviews zijn versiering (het cijfer staat erbij), net als op iwrap.nl.
- **Uitlijning** (zoals iwrap.nl): één rand. De kopbalk en de inhoud zijn even breed (`.nav` en
  `.wrap` allebei 1100px met 24px marge, ook op een telefoon): het woordmerk staat recht boven de
  koppen en de knop naar iWrap eindigt waar de inhoud eindigt. Ook op de tekstpagina's (artikelen,
  over deze site, de keuzehulp) staan de kop en de tekst op die linkerrand, in een kolom van 660px;
  eerst stond die kolom in het midden. Een artikelkop is daar maximaal 18em breed. Op een telefoon
  (tot 700px) staat alles links, ook de kop van de homepage en "In vier stappen". Op een telefoon
  vullen de knoppen in een rij de regel, zodat gestapelde knoppen even breed zijn. Lijsten hebben
  hier allemaal een eigen opmaak (bolletjes, vinkjes, stappen) en staan op de tekstrand. Op een heel
  smal scherm (onder 360px) zijn het woordmerk en de knop in de kopbalk iets kleiner, zodat ze naast
  elkaar passen.
- **Woordmerk**: de naam is het logo: `kozijn` in `--merk-tekst` (normaal gewicht) direct
  gevolgd door `wrap` in de inktkleur (extra vet), met `.nl` klein erachter. Echte tekst, dus
  voorleessoftware en zoekmachines lezen de naam gewoon. `WORDMARK` in `build.py`, `.brand` in
  `style.css`.
- **Deelafbeelding**: `images/og-image-v6.jpg`: woordmerk en "Herstellen of wrappen?" in
  Montserrat, en hetzelfde 3D-kozijn half crème en half antraciet. Gemaakt met
  `tools/maak_og.py`; geef een nieuwe versie een nieuw nummer (`/images/` staat een jaar in de cache).
- **Favicon**: een kozijn van voren met de onderdorpel in de lichte kleur van het palet: de
  dorpel is bijna altijd het eerst versleten. `FAVICON` in `build.py`, kleurt mee met `PALET`.
- **Slogan**: "Weet wat je kozijn nodig heeft" (`SLOGAN` in `build.py`): in de footer en als
  opschrift boven de hero.
- **Wat níet meekleurt**: het 3D-kozijn, de RAL-staaltjes en de materiaalkleuren in de
  diagrammen (folie, verf, vuil, glas, profiel). Die stellen echte dingen voor.

## URL's

`vercel.json` heeft `cleanUrls` aan: de site draait op `/kozijnherstel`, niet op
`/kozijnherstel.html`. Interne links, canonicals en de sitemap zijn daarop afgestemd.
Gebruik in de bronbestanden root-relatieve links (`/blog/renolit-folie-uitgelegd`).

## Openstaand

- **Het domein `kozijnwrap.nl` is nog niet aan Vercel gekoppeld** — het wijst op dit moment
  naar een parkeerpagina, terwijl alle canonicals en de sitemap er al naar verwijzen.
  Zolang dat zo is, levert de SEO niets op.
- Reviewcijfers en de gegevens van iWrap staan in het blok `IWRAP` bovenin `build.py`.
  Daaruit komen de brug naar iWrap, de regel boven elk artikel en de `author` in de
  structured data. Eén plek aanpassen dus. Op kozijnherstel.html staan ze daarnaast nog
  in de lopende tekst — die twee even meenemen als het aantal wijzigt. Net als de bedragen in de keuzehulp — die staan in
  `src/pages/keuzehulp.html` in `PRIJS` (per omvang, bij de uitkomst folieherstel) en in het
  veld `prijs` op de uitkomst `vervangen` — en verder in het kostenartikel en in het blok
  "Ook als het maar om een paar dorpels gaat".
- Bezoekers worden geteld met Vercel Web Analytics (zonder cookies). De uitgaande links naar
  iwrap.nl hebben UTM-tags (`utm_source=kozijnwrap.nl`, `utm_medium` per plek), dus in de
  statistieken van iwrap.nl is te zien hoeveel aanvragen hiervandaan komen.
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
- **Levensduur** (Max, 19 november 2026, op alle drie de sites hetzelfde): 15 tot 25 jaar gaat
  over de **oude** folie die er nu op zit. De nieuwe folie is veel sterker en gaat naar
  verwachting veel langer mee; noem daar **geen jaartal** bij. Tien jaar is de garantie, niet de
  levensduur. Daarom loopt de balk "Nieuwe folie" in `{{levensduur}}` open uit.
- **Kleur** (Max, 19 november 2026): iWrap herstelt aangetaste kozijnen, bijna altijd in dezelfde
  kleur; een andere kleur kan bij het herstel. Kozijnen omkleuren waarvan de folie nog goed is
  (wrappen) doet iWrap niet. Dat zegt deze site al; iwrap.nl zegt het sinds die dag ook zo.
- houtnerffolie.nl blijft de plek voor de diepte: decors, kleuren en specificaties. Ga hier geen
  kleurenoverzicht of specificatietabel bouwen, dan concurreren de twee sites alsnog met elkaar.
  Maar link er **niet** heen: deze site stuurt door naar iWrap (Max, 19 november 2026). Het
  artikel [renolit-folie-uitgelegd](src/pages/blog/renolit-folie-uitgelegd.html) verwijst voor de
  kleur van je kozijn daarom naar iWrap, dat de passende folie opzoekt aan de hand van je foto's.

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
