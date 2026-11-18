"""De deelafbeelding (WhatsApp, LinkedIn): images/og-image-v6.jpg, in de kleuren van het palet.

Links het woordmerk en "Herstellen of wrappen?" (in Montserrat, net als op de site), rechts hetzelfde 3D-kozijn half crème (herstellen)
en half antraciet (wrappen). Gebruik: python3 tools/maak_og.py   (ander palet: eerst PALET in
build.py aanpassen). Geef het bestand bij een nieuwe versie een nieuw nummer (en zet dat in
build.py): /images/ staat op een cache van een jaar.
Nodig: Chrome en cdp.py uit iwrap-project/beweging/tools (staat naast deze map).
"""
import base64, os, sys, time
HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
import importlib.util
# build.py van déze site (er staat er ook een in de map met cdp.py, dus niet via sys.path)
_spec = importlib.util.spec_from_file_location("kozijnwrap_build", os.path.join(ROOT, "build.py"))
build = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(build)
sys.path.append(os.path.join(os.path.dirname(ROOT), "iwrap-project", "beweging", "tools"))
from cdp import Chrome

UIT = os.path.join(ROOT, "images", "og-image-v6.jpg")
palet = build.palet_attr()
html = """<!doctype html><html lang="nl"%s><head><meta charset="utf-8">
<link rel="stylesheet" href="../css/style.css">
<style>
  /* Montserrat uit fonts/ (style.css verwijst naar /fonts/, en dat bestaat niet via file://) */
  @font-face{font-family:"Montserrat-og";font-weight:100 900;src:url(../fonts/montserrat-latin-83a31c81.woff2) format("woff2");}
  :root{--kop:"Montserrat-og",Arial,sans-serif;}
  html,body{margin:0;width:1200px;height:630px;overflow:hidden;}
  body{background:var(--gloed),var(--paper);font-family:var(--sans);-webkit-font-smoothing:antialiased;}
  .vak{display:grid;grid-template-columns:540px 1fr;align-items:center;gap:44px;height:100%%;padding:0 60px;box-sizing:border-box;}
  .merk{font-family:var(--kop);font-size:56px;line-height:1;letter-spacing:-.035em;}
  .w1{color:var(--merk-tekst);font-weight:500;} .w2{color:var(--ink);font-weight:800;} .tld{font-size:.5em;font-weight:600;color:var(--merk-tekst);}
  h1{font-family:var(--kop);font-size:56px;line-height:1.06;letter-spacing:-.032em;margin:36px 0 16px;color:var(--ink);}
  p{font-size:27px;line-height:1.35;color:var(--sub);margin:0;max-width:20ch;}
  .door{display:flex;align-items:center;gap:12px;margin-top:34px;font-size:21px;font-weight:600;color:var(--ink);}
  .v{width:34px;height:34px;border-radius:50%%;background:var(--iwrap-mint);display:grid;place-items:center;font-size:19px;}
  .beeld{position:relative;height:440px;border-radius:30px;overflow:hidden;box-shadow:0 0 0 1px rgba(34,38,42,.06),0 34px 60px -34px rgba(34,38,42,.55);}
  .beeld img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;}
  .beeld .b{clip-path:polygon(50%% 0,100%% 0,100%% 100%%,28%% 100%%);}
  .lab{position:absolute;bottom:18px;padding:9px 17px;border-radius:999px;font-family:var(--kop);font-size:21px;font-weight:700;}
  .l1{left:18px;background:var(--iwrap-mint);color:var(--ink);} .l2{right:18px;background:var(--ink);color:#fff;}
</style></head><body>
<div class="vak">
  <div>
    <div class="merk"><span class="w1">kozijn</span><span class="w2">wrap<span class="tld">.nl</span></span></div>
    <h1>Herstellen of wrappen?</h1>
    <p>Zie het verschil, en weet wat je kozijn nodig heeft.</p>
    <div class="door"><span class="v">&#10003;</span>Uitleg van iWrap, al %s jaar specialist in kozijnherstel</div>
  </div>
  <div class="beeld">
    <img src="../images/kozijn3d-hersteld-1400.webp" alt=""><img class="b" src="../images/kozijn3d-antraciet-1400.webp" alt="">
    <span class="lab l1">Herstellen</span><span class="lab l2">Wrappen</span>
  </div>
</div></body></html>""" % (palet, build.IWRAP_JAREN)
tmp = os.path.join(HIER, "_og.html")
open(tmp, "w", encoding="utf-8").write(html)
c = Chrome(1200, 630)
try:
    c.goto("file://" + tmp, wait=1.0)
    c.js("document.fonts.ready.then(() => document.fonts.check('700 56px Montserrat-og'))") or sys.exit("Montserrat niet geladen")
    time.sleep(0.4)
    open(UIT, "wb").write(base64.b64decode(c.call("Page.captureScreenshot", {"format": "jpeg", "quality": 86})["data"]))
finally:
    c.close()
    os.remove(tmp)
print("ok", UIT)
