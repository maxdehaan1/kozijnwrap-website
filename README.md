# kozijnwrap.nl

Onafhankelijk kozijnadvies-platform, onderdeel van iWrap. Splitst bezoekers in twee paden:
kozijnherstel (kunststof kozijnen, Renolit folie, uitgevoerd door iWrap zelf) en
kozijnwrappen (omkleuren van nog goede aluminium/kunststof kozijnen, doorverwijzing naar
een nog te kiezen externe partij).

## Structuur

```
index.html            Landingspagina — de tweesplitsing
kozijnherstel.html     Kozijnherstel volledig uitgelegd + aanbeveling iWrap
kozijnwrappen.html     Kozijnwrappen volledig uitgelegd + placeholder-aanbeveling

css/
  style.css            Echt gedeeld: variabelen, basistypografie, header, footer
  home.css             Alleen voor index.html (hero, de twee kleurblokken, polaroidfoto)
  content.css          Gedeeld door kozijnherstel.html en kozijnwrappen.html
                        (gekleurde hero-band, checklists, feiten-grid, adviesbox)

images/
  proces-squeegee.jpg     Eigen foto, achtergrond in de hero op index.html
  kozijn-beschadigd.jpg   Voorbeeld beschadigde folie, polaroidje in het rode blok
```

## Waarom drie CSS-bestanden?

`index.html` en de twee subpagina's gebruiken dezelfde klassenamen (`.wrap`, `.hero`) voor
net iets andere dingen (bredere landingspagina vs. smallere leestekst-pagina's, kleurblokken
vs. een gekleurde hero-band). Om conflicten te voorkomen zijn die regels gescoped onder
`body.home` respectievelijk `body.page` — vandaar de bodyklasse op elke pagina.

## Huisstijl

- Lettertype: Newsreader (serif), via Google Fonts
- Kleuren: gedempt terracotta-rood (`--red`) voor kozijnherstel, gedempt groenblauw
  (`--turq`) voor kozijnwrappen — dezelfde stijlfamilie als houtnerffolie.nl

## Openstaand

- Aanbevolen partij voor kozijnwrappen nog niet gekozen (placeholder op kozijnwrappen.html)
- Reviewcijfers iWrap (4,9★, 81 reviews) staan hardcoded op kozijnherstel.html — bijwerken
  als het aantal wijzigt
