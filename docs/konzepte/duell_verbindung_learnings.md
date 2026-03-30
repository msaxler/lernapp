# Duell-Verbindung: Learnings aus dem QuizAway v4 Prototyp

*Erfahrungen aus der Implementierung und dem Debugging des P2P-Duells — relevant für den Neubau.*

---

## 1. Das Tanzpartner-Problem (Signaling / Rendezvous)

Zwei Geräte im Internet können sich nicht direkt finden — beide kennen nur ihre eigene private IP. Ein **Rendezvous-Server** ist deshalb zwingend nötig, selbst wenn die eigentliche Kommunikation danach P2P laufen soll.

Im Prototyp übernimmt `rendezvous.py` diese Rolle: Host legt ein Angebot (SDP Offer) ab, Guest pollt danach und legt die Antwort (SDP Answer) zurück. Beide tauschen so ICE-Kandidaten aus ohne sich direkt zu kennen.

**Wichtigste Erkenntnis:** Der Rendezvous-Server muss immer erreichbar sein — auch wenn P2P danach funktioniert. Bei Render schläft der Server nach 15 min. Der erste Request nach dem Aufwachen dauert ~30s. Das ist für einen spontanen Duell-Start inakzeptabel. Im Neubau: Rendezvous auf einem Always-On-Dienst oder mit Keep-Alive-Ping lösen.

---

## 2. WebRTC ICE: wann P2P funktioniert und wann nicht

WebRTC versucht automatisch den direkten Pfad zwischen zwei Geräten zu finden (ICE = Interactive Connectivity Establishment):

| Situation | Ergebnis |
|---|---|
| Beide im selben WLAN | P2P direkt ✓ |
| Beide hinter verschiedenen Heimroutern | STUN reicht oft ✓ |
| Mobilnetz ↔ WLAN (Carrier-Grade-NAT) | STUN scheitert, TURN nötig |
| Mobilnetz ↔ Mobilnetz | Fast immer TURN nötig |

**STUN** gibt einem Gerät seine öffentliche IP+Port. **TURN** ist ein Relay-Server, der den Traffic durchleitet wenn kein direkter Pfad möglich ist. Öffentliche TURN-Server (z.B. openrelay.metered.ca) sind unzuverlässig — sie sind überlastet und haben keine SLA. Im Neubau entweder einen eigenen TURN-Server (coturn) oder einen bezahlten Dienst (Metered.ca, Twilio) verwenden.

**Konsequenz für den Prototyp:** TURN wurde nicht zuverlässig genug. Stattdessen wurde ein eigener Server-Relay-Fallback implementiert.

---

## 3. Der Server-Relay-Fallback

Wenn WebRTC/ICE scheitert, leitet der Rendezvous-Server die Nachrichten selbst durch — als einfacher Message-Queue per HTTP-Polling.

```
Gerät A  →  POST /relay/{id}/send  →  Server-Queue
Gerät B  ←  GET  /relay/{id}?fuer=B  ←  Server-Queue
```

Der Server hält pro Session zwei Queues (eine für Host, eine für Guest). Jedes Gerät pollt seine Queue alle ~3 Sekunden (Short-Poll mit 3s Blocking auf Serverseite). Der Overhead ist gering, da nur wenige kleine JSON-Nachrichten pro Runde ausgetauscht werden.

**Wichtig:** Der Relay-Fallback muss *automatisch* aktiviert werden — der Nutzer merkt nichts davon. Auslöser:
- ICE-State wechselt zu `failed` → sofort Relay
- 12-Sekunden-Safety-Timer → Relay falls DC nie öffnete
- 3 Pings ohne Pong → Relay auch wenn DC kurz offen war

---

## 4. Subtile Fallstricke beim Relay-Übergang

Der schwierigste Teil war nicht der Relay selbst, sondern der **nahtlose Übergang** von WebRTC zu Relay ohne Spielunterbrechung. Drei Bugs, die dabei auftraten:

### Bug A — `dc.onclose` resettet das laufende Spiel
Wenn der DataChannel schloss (weil ICE fehlschlug), setzte `dc.onclose` das Flag `verbunden = false` und stoppte den Ping-Timer. Der anschliessende Relay-Start dachte dann, das Spiel sei noch nicht gestartet, und initialisierte alles neu — inklusive einem zweiten "Runde 1 starten"-Aufruf.

**Fix:** `dc.onclose` prüft jetzt: War das Spiel bereits aktiv (`verbunden === true`)? Dann sofort `activateRelayMode()` aufrufen statt den State zurückzusetzen. Kein doppelter Neustart, Scores bleiben erhalten.

### Bug B — Relay-Poll-Loop lief nach Spielende weiter
`duelAbgebrochen()` stoppte Ping-Timer und ACK-Retries, aber nicht den Relay-Poll-Loop. Der Loop lieferte danach noch verspätete Nachrichten — z.B. eine `kat`-Nachricht, die eine neue Runde startete, obwohl das Spiel bereits als gewonnen angezeigt wurde.

**Fix:** `duelAbgebrochen()` setzt jetzt `relayMode = false` und `relayId = null`. Die While-Schleife des Poll-Loops prüft beide Werte und stoppt.

### Bug C — Service Worker cachte API-Antworten
Der Service Worker (PWA-Cache) hatte keinen Ausschluss für dynamische Endpunkte. Die erste Antwort von `/warteraum/liste` (leer) wurde gecacht — alle Folgeanfragen bekamen die leere Liste zurück, Mitspieler waren unsichtbar.

**Fix:** Alle signaling- und relay-Endpunkte explizit aus dem SW-Cache ausschliessen: `/warteraum/`, `/lobby/`, `/relay/`, `/offer/`, `/answer/`, `/new`, `/ping`.

---

## 5. Zuverlässiger Nachrichtenaustausch (ACK + Duplikat-Schutz)

HTTP-Polling ist nicht garantiert zuverlässig — eine Nachricht kann verloren gehen oder (durch Retries) doppelt ankommen. Das Protokoll braucht deshalb zwei Mechanismen:

**ACK-basierte Wiederholung:** Jede wichtige Nachricht (`kat`, `runde`) trägt eine aufsteigende Sequenznummer. Der Empfänger schickt sofort ein `ack` zurück. Der Sender wiederholt alle 3 Sekunden bis das ACK kommt.

**Duplikat-Erkennung:** Der Empfänger hält ein `Set` aller bereits gesehenen Sequenznummern (`seenSeqs`). Kommt dieselbe Nummer nochmal an, wird die Nachricht verarbeitet (und ACK erneut gesendet), aber die Spiellogik nicht nochmal ausgeführt.

**Ping/Pong-Heartbeat:** Alle 5 Sekunden sendet jede Seite einen Ping. Bleibt der Pong aus, wird nach 3 fehlgeschlagenen Versuchen (15s) der Relay-Fallback aktiviert. Nach 6 fehlgeschlagenen Versuchen (30s) gilt der Gegner als nicht erreichbar.

**Relay-Latenz und Timeouts:** Mit 3s Short-Poll beträgt die maximale Pong-Roundtrip-Zeit ~6s. Timeouts müssen deutlich grösser sein (≥30s), damit normale Relay-Latenz nicht fälschlicherweise als Verbindungsabbruch gewertet wird.

---

## 6. Rundenwechsel-Synchronisation

Das grösste UX-Problem war die Synchronisation des Rundenwechsels: Beide Geräte müssen wissen, wann die andere Seite fertig ist, bevor die nächste Runde startet.

**Wahlrecht:** Pro Runde hat immer genau eine Seite das Wahlrecht für die Kategorie (Host: Runden 1, 3; Guest: Runden 2, 4; Runde 5: wer führt). Das ist deterministisch berechenbar — keine Aushandlung nötig.

**Warte-Mechanismus:** Wer zuerst fertig ist, schickt sein Ergebnis (`runde`-Nachricht) und zeigt "Warte auf Gegner". Wenn beide Ergebnisse da sind, wird `duelZeigeVergleich()` aufgerufen. Ein 30s-Timeout überbrückt Verbindungsprobleme mit einem angenommenen 0/3-Ergebnis.

**Auto-Advance:** Nach dem Vergleich hat der Spieler 5 Sekunden Zeit, manuell weiterzumachen — danach geht es automatisch. Das verhindert Deadlocks wenn einer der Spieler den "Weiter"-Button nicht sieht.

---

## 7. Empfehlungen für den Neubau

| Thema | Empfehlung |
|---|---|
| Signaling | WebSocket statt HTTP-Polling — spart Roundtrips, kein Sleep-Problem |
| TURN | Eigener coturn-Server oder bezahlter Dienst — nicht auf Open-Relay verlassen |
| Relay-Fallback | Beibehalten — ist robust und einfach; als WebSocket effizienter |
| ACK-Protokoll | Beibehalten — bewährt sich; ggf. in eine generische Klasse auslagern |
| SW-Cache | Alle dynamischen Endpunkte von Beginn an ausschliessen |
| Rendezvous | Always-On nötig — kein Render Free Tier für produktiven Einsatz |
| Rundenwechsel | Wahlrecht-Logik beibehalten; Auto-Advance-Timer beibehalten |
