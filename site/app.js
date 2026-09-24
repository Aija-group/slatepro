/* SlatePro – header, mobiilivalikko, ennen/jälkeen-liukusäädin, kotitalousvähennyslaskuri, scroll-reveal. */
(function () {
  var doc = document.documentElement;
  var shot = /[?&]shot=1/.test(location.search);
  if (shot) doc.classList.add('shot');

  // Header kiinteäksi vieritettäessä
  var hdr = document.querySelector('.hdr');
  function onScroll() { hdr.classList.toggle('solid', window.scrollY > 30 || doc.classList.contains('menu-open')); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobiilivalikko
  var burger = document.querySelector('.burger');
  burger.addEventListener('click', function () {
    var open = doc.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? 'Sulje valikko' : 'Avaa valikko');
    onScroll();
  });
  document.querySelectorAll('.nav a').forEach(function (a) {
    a.addEventListener('click', function () { doc.classList.remove('menu-open'); burger.setAttribute('aria-expanded', false); onScroll(); });
  });

  // Ennen/jälkeen
  document.querySelectorAll('.ba').forEach(function (ba) {
    var r = ba.querySelector('.ba-range');
    function set(v) { ba.style.setProperty('--pos', v + '%'); }
    r.addEventListener('input', function () { set(r.value); });
    set(r.value);
  });
  // Pieni esittelyliike, kun säädin tulee näkyviin ensimmäistä kertaa
  var stage = document.querySelector('.ba-stage');
  if (stage && 'IntersectionObserver' in window && !shot) {
    var played = false;
    new IntersectionObserver(function (es, o) {
      if (!es[0].isIntersecting || played) return;
      played = true; o.disconnect();
      var ba = stage.querySelector('.ba:not([hidden])'), r = ba.querySelector('.ba-range');
      var t0 = null;
      function step(t) {
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / 1800, 1);
        var v = 50 + Math.sin(p * Math.PI * 2) * 28 * (1 - p);
        r.value = v; ba.style.setProperty('--pos', v + '%');
        if (p < 1) requestAnimationFrame(step);
      }
      setTimeout(function () { requestAnimationFrame(step); }, 500);
    }, { threshold: .5 }).observe(stage);
  }
  document.querySelectorAll('.ba-tabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      var key = b.dataset.ba;
      document.querySelectorAll('.ba-tabs button').forEach(function (x) { x.setAttribute('aria-selected', x === b); });
      document.querySelectorAll('.ba').forEach(function (p) { p.hidden = p.dataset.pane !== key; });
    });
  });

  // Kotitalousvähennyslaskuri
  document.querySelectorAll('.calc').forEach(function (f) {
    var pct = +f.dataset.pct / 100, max = +f.dataset.max, omav = +f.dataset.omav;
    var out = f.querySelector('[data-out]'), net = f.querySelector('[data-net]');
    var fmt = function (n) { return Math.round(n).toLocaleString('fi-FI') + ' €'; };
    function calc() {
      var tyo = Math.max(0, +f.tyo.value || 0);
      var hlo = +f.querySelector('input[name=hlo]:checked').value;
      var per = Math.min(max, Math.max(0, (tyo / hlo) * pct - omav));
      var total = per * hlo;
      out.textContent = fmt(total);
      net.textContent = total > 0 ? 'Työn hinta vähennyksen jälkeen ' + fmt(tyo - total) : 'Työn osuus jää alle omavastuun';
    }
    f.addEventListener('input', calc);
    calc();
  });

  // Scroll-reveal
  var els = document.querySelectorAll('.reveal');
  if (shot || !('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    els.forEach(function (e, i) {
      var sib = e.parentElement ? Array.prototype.indexOf.call(e.parentElement.children, e) : 0;
      e.style.transitionDelay = Math.min(sib, 4) * 80 + 'ms';
      io.observe(e);
    });
  }

  // WhatsApp-vinkki näkyy hetken vierityksen jälkeen
  var wf = document.querySelector('.wa-float');
  if (wf && !shot) {
    var shown = false;
    window.addEventListener('scroll', function () {
      if (shown || window.scrollY < 900) return;
      shown = true; wf.classList.add('tip');
      setTimeout(function () { wf.classList.remove('tip'); }, 4500);
    }, { passive: true });
  }

  // Lomakkeen virheilmoitus (?virhe=1)
  if (/[?&]virhe=1/.test(location.search)) {
    var form = document.querySelector('.form');
    if (form) {
      var p = document.createElement('p');
      p.className = 'note'; p.textContent = 'Lähetys ei onnistunut. Tarkista pakolliset kentät tai ota yhteyttä WhatsAppilla.';
      form.insertBefore(p, form.querySelector('h2').nextSibling);
    }
  }
})();
