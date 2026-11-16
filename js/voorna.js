/* ---------------------------------------------------------------------------
   De voor/na-schuif (.vergelijk), dezelfde als op iwrap.nl: twee beelden van
   hetzelfde kozijn op elkaar, het bovenste afgesneden op --pos. Slepen met de
   muis of een vinger (verticaal scrollen blijft gewoon werken: touch-action
   pan-y in onderdelen.css), of met de pijltjestoetsen op de verborgen schuif.

   De eerste schuif die goed in beeld komt, gaat één keer zelf even heen en weer,
   zodat je ziet dat hij beweegt. Niet als iemand er al aan zit, en niet bij
   "minder beweging" in de instellingen van het apparaat.
   --------------------------------------------------------------------------- */
(function () {
  "use strict";

  var blokken = document.querySelectorAll(".vergelijk");
  if (!blokken.length) return;
  var aangeraakt = false;

  function zetOp(blok, pct) {
    pct = Math.max(0, Math.min(100, pct));
    blok.style.setProperty("--pos", pct.toFixed(2) + "%");
    var schuif = blok.querySelector("input[type=range]");
    if (schuif && Math.round(pct) !== Number(schuif.value)) schuif.value = String(Math.round(pct));
  }

  Array.prototype.forEach.call(blokken, function (blok) {
    var schuif = blok.querySelector("input[type=range]");
    var slepen = false;

    function vanPunt(e) {
      var r = blok.getBoundingClientRect();
      zetOp(blok, ((e.clientX - r.left) / r.width) * 100);
    }
    function los() {
      slepen = false;
      blok.classList.remove("sleept");
    }

    if (schuif) {
      zetOp(blok, Number(schuif.value));
      schuif.addEventListener("input", function () {
        aangeraakt = true;
        zetOp(blok, Number(schuif.value));
      });
    }

    blok.addEventListener("pointerdown", function (e) {
      if (e.button) return;
      aangeraakt = true;
      slepen = true;
      blok.classList.add("sleept");
      try { blok.setPointerCapture(e.pointerId); } catch (x) {}
      vanPunt(e);
    });
    blok.addEventListener("pointermove", function (e) { if (slepen) vanPunt(e); });
    blok.addEventListener("pointerup", los);
    blok.addEventListener("pointercancel", los);
    // Geen sleepbeeld van de foto zelf.
    blok.addEventListener("dragstart", function (e) { e.preventDefault(); });
  });

  /* Eén keer heen en weer --------------------------------------------------- */
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  function hint(blok) {
    var schuif = blok.querySelector("input[type=range]");
    var start = schuif ? Number(schuif.value) : 50;
    var t0 = null, DUUR = 1700;
    function golf(p) {
      // Naar links, dan naar rechts, dan terug naar het begin, met zachte overgangen.
      return Math.sin(p * Math.PI * 2) * Math.sin(p * Math.PI) * -14;
    }
    function stap(nu) {
      if (aangeraakt) return;
      if (t0 === null) t0 = nu;
      var p = Math.min(1, (nu - t0) / DUUR);
      zetOp(blok, start + golf(p));
      if (p < 1) requestAnimationFrame(stap);
      else zetOp(blok, start);
    }
    requestAnimationFrame(stap);
  }

  var kijker = new IntersectionObserver(function (rijen) {
    rijen.forEach(function (rij) {
      if (!rij.isIntersecting) return;
      kijker.disconnect();
      if (!aangeraakt) setTimeout(function () { hint(rij.target); }, 450);
    });
  }, { threshold: 0.6 });
  kijker.observe(blokken[0]);
})();
