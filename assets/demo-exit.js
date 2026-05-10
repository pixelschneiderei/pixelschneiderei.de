/* Demo-Exit: kehrt zur Herkunftsseite zurück.

   Strategie:
   1. Wenn der Besucher von der gleichen Domain (und nicht aus einer
      anderen Demo) kam, fängt der Klick `history.back()` ab. Damit
      stellt der Browser die exakte Scroll-Position wieder her — also
      auch der Sprung zurück zu z.B. #referenzen klappt.
   2. Zusätzlich wird der Label-Text passend gesetzt.
   3. Fallback ist der im HTML gesetzte href (../../index.html). */
(function () {
  var exit = document.querySelector('.demo-exit');
  if (!exit) return;

  function updateLabel(text) {
    if (!text) return;
    var nodes = exit.childNodes;
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.nodeType === 3 && n.textContent.trim()) {
        n.textContent = ' ' + text + ' ';
        return;
      }
    }
  }

  function labelForPath(pathname) {
    var p = pathname.replace(/\/$/, '').split('/').pop().replace(/\.html$/, '');
    var map = {
      '':                          'Zurück zur Startseite',
      'index':                     'Zurück zur Startseite',
      'referenzen':                'Zurück zu Referenzen',
      'komponenten':               'Zurück zu Komponenten',
      'webdesign-coburg':          'Zurück zu Webdesign Coburg',
      'webdesign-oberfranken':     'Zurück zu Webdesign Oberfranken',
      'webdesign-bayern':          'Zurück zu Webdesign Bayern',
      'webseite-handwerker-bayern':'Zurück zu Handwerker-Webseite',
      'premium-webdesign':         'Zurück zu Premium-Webdesign',
      'impressum':                 'Zurück zum Impressum',
      'datenschutz':               'Zurück zum Datenschutz'
    };
    return map[p] || 'Zurück';
  }

  var canGoBack = false;

  try {
    var ref = document.referrer;
    if (ref) {
      var url = new URL(ref);
      var here = new URL(window.location.href);

      // Gleiche Domain und nicht aus einer anderen Demo.
      if (url.host === here.host && !/\/demos\//.test(url.pathname) && url.href !== here.href) {
        canGoBack = true;
        // Label anpassen — Hash kommt im Referrer typischerweise nicht
        // mit, deshalb nur Pfad-basiert.
        updateLabel(labelForPath(url.pathname));
        // href als sichtbarer Fallback (Hover-Anzeige, neuer Tab etc.).
        exit.setAttribute('href', url.href);
      }
    }
  } catch (e) { /* fallback bleibt */ }

  // Klick-Handler: history.back() bevorzugen, weil es die
  // Scroll-Position der Herkunftsseite wiederherstellt
  // (z.B. zurück zu #referenzen statt nach oben).
  exit.addEventListener('click', function (ev) {
    // Mittelklick / Cmd-Klick / neuer Tab: normalen Link nicht abfangen.
    if (ev.defaultPrevented || ev.button !== 0) return;
    if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;

    if (canGoBack && window.history.length > 1) {
      ev.preventDefault();
      window.history.back();
    }
  });
})();
