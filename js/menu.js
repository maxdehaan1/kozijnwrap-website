/* Het menu op een telefoon en tablet, op alle drie de sites van iWrap hetzelfde (op iwrap.nl in
   js/main.js). Een knop met het woord "Menu" (open: "Sluiten"), een paneel dat van boven over de
   pagina openklapt met grote regels, en een donkere laag erachter. Een tik op de laag of Escape sluit
   het; met Tab blijf je in het open menu. */
(function () {
  'use strict';
  var knop = document.querySelector('.nav-toggle');
  var menu = document.getElementById('hoofdmenu');
  if (!knop || !menu) return;
  var woord = knop.querySelector('.nav-toggle-woord');
  var laag = document.createElement('div');
  laag.className = 'menu-laag';
  document.body.appendChild(laag);

  function zet(open) {
    knop.setAttribute('aria-expanded', String(open));
    if (woord) woord.textContent = open ? 'Sluiten' : 'Menu';
    menu.classList.toggle('open', open);
    laag.classList.toggle('open', open);
    // Met het menu open scrolt de pagina eronder niet mee.
    document.documentElement.classList.toggle('menu-open', open);
  }
  function isOpen() { return knop.getAttribute('aria-expanded') === 'true'; }

  knop.addEventListener('click', function () { zet(!isOpen()); });
  laag.addEventListener('click', function () { zet(false); });
  menu.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('a')) zet(false);
  });
  document.addEventListener('keydown', function (e) {
    if (!isOpen()) return;
    if (e.key === 'Escape') { zet(false); knop.focus(); return; }
    if (e.key !== 'Tab') return;
    var doelen = [knop].concat(Array.prototype.slice.call(menu.querySelectorAll('a[href], button:not([disabled])'))
      .filter(function (el) { return el.getClientRects().length > 0; }));
    var eerste = doelen[0], laatste = doelen[doelen.length - 1], nu = doelen.indexOf(document.activeElement);
    if (nu === -1) { e.preventDefault(); (e.shiftKey ? laatste : eerste).focus(); }
    else if (e.shiftKey && nu === 0) { e.preventDefault(); laatste.focus(); }
    else if (!e.shiftKey && nu === doelen.length - 1) { e.preventDefault(); eerste.focus(); }
  });
  // Wordt het scherm zo breed dat het menu weer in de balk staat (telefoon gedraaid), dan gaat het dicht.
  window.addEventListener('resize', function () {
    if (isOpen() && !knop.getClientRects().length) zet(false);
  });
})();
