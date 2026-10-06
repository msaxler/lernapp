// QuizAway: Karten eines Orts suchen, die sich denselben Fakt teilen könnten (Mike 2026-10-07: Denzlingen „99 Prozent
// evangelisch“ in zwei Karten). Merkmal: mindestens zwei gemeinsame Zahlen (Jahre, Prozente, Mengen) auf Vorder- und
// Rückseite. Das ist ein Verdacht, kein Urteil: Wahlkarten mit verschiedenen Fragen teilen oft die Prozente der Rückseite.
// Herausnehmen über <raum>/vorrat.json „raus“ (Raum iter1) bzw. korrekturen-hand.json (Raum bahn).
// Aufruf:  node scripts/check/quizaway_doppelte_fakten.js   (liest apps/quizaway-reise/daten.js)
global.window = {};
require('../../apps/quizaway-reise/daten.js');
const zahlen = s => new Set((s.match(/\b\d[\d.,]*\b/g) || []).map(z => z.replace(/[.,]$/, ''))
  .filter(z => z.length >= 2 && !/^(19|20)?\d$/.test(z)));
const kurz = k => (k.art === 'luege' ? 'LÜGE ' + k.loesung + ': ' + k.optionen.join(' / ')
  : k.frage + ' → ' + k.optionen[k.loesung - 1]).slice(0, 200);
let n = 0;
for (const r of window.QA_DATEN.raeume) for (const o of r.orte) {
  const ks = o.karten.map(k => ({ k, z: zahlen(k.frage + ' ' + k.optionen.join(' ') + ' ' + k.rueckseite) }));
  for (let i = 0; i < ks.length; i++) for (let j = i + 1; j < ks.length; j++) {
    const g = [...ks[i].z].filter(x => ks[j].z.has(x));
    if (g.length >= 2) {
      n++;
      console.log('#' + n, r.id, ks[i].k.id, '|', ks[j].k.id, '| gemeinsam:', g.join(' '));
      console.log('   A', kurz(ks[i].k));
      console.log('   B', kurz(ks[j].k));
    }
  }
}
console.log('Verdachtspaare:', n);
