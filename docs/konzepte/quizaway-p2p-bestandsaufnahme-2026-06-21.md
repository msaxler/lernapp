# QuizAway P2P/Mehrspieler — Bestandsaufnahme: realisiert vs. konzipiert

**Datei:** `quizaway-p2p-bestandsaufnahme-2026-06-21.md`
**Pfad:** LernApp `docs/konzepte/`
**Anlass:** Frage aus der Transfer-Diskussion (v1.1 §7 / PC-Session-Fokus Punkt 4): „`@xalento/p2p-tele` existiert als Paket nicht — wie vollständig hatte QuizAway P2P schon?"
**Datum:** 2026-06-21 · Bestandsaufnahme, kein Auftrag.

> **Kurzantwort:** Sehr vollständig. QuizAways P2P-Duell ist ein **lauffähiger, auf Render deployter Prototyp** — Rendezvous, WebRTC, STUN/TURN, automatischer Server-Relay-Fallback, ACK+Dedup, Heartbeat, Warteraum mit serverseitiger CAS-Paarung, Rundensync. **Nur** die Liga-/Ledger-/Krypto-Schicht (signierte Events, Bloom/Merkle, Nostr) ist Konzept. **Wichtige Korrektur zu Punkt 4:** Der Transport ist *nicht* „nur ein vermischter Single-File-Prototyp ohne Vorbild" — er ist eine **brauchbare Referenz-Implementierung**, und die Xalento-`p2p-tele`-Konzepte definieren bereits die Ziel-Schichtung (Plattform/Verben/Domäne) deckungsgleich zu v1.1 §7.

---

## 1. Maßgebliche Artefakte & Verortung

- **Primary-Repo:** `D:\claude-code\LernApp\` (zuletzt geändert 31.05.2026). `D:\claude-code\Xalento\apps\quizaway\` ist eine **byte-identische Archiv-Kopie vom 04.04.2026** — und enthält den Server **nicht**.
- **Server (REAL):** `D:\claude-code\LernApp\scripts\sync\rendezvous.py` (625 Z., Python 3 nur Stdlib: `http.server`/`threading`/`json`/`sqlite3`). Deploy: Render (`render.yaml`), `/ping` für UptimeRobot-Keepalive.
- **Client (REAL):** `D:\claude-code\LernApp\apps\quizaway\quizaway_v5.html` (~5787 Z.; v5 = maßgeblich, kosmetisch ggü. v4). P2P-Client-Stack ab Z. ~5180.
- **Lehren:** `LernApp/docs/konzepte/duell_verbindung_learnings.md` (7 Abschnitte Prototyp-Debugging).
- **Verallgemeinerungs-Konzepte (DESIGN):** `Xalento/docs/architektur/plattform/p2p-tele-*` (strategie-synthese, vereinheitlichung-konzept, modell-und-technik **v1.3 2026-06-19**) + `Xalento/docs/konzepte/...`.

---

## 2. Feature-Matrix — REALISIERT vs. KONZEPT

| Feature-Gebiet | Status | Beleg |
|---|---|---|
| Signaling/Rendezvous-Server | ✅ **REALISIERT** | `rendezvous.py` — `/new`,`/offer/{pin}`,`/answer/{pin}` (SDP-Austausch via HTTP-Poll) |
| WebRTC-Verbindungsaufbau (ICE) | ✅ **REALISIERT** | `quizaway_v5.html:5245-5253` — Google-STUN + OpenRelay-TURN, `RTCPeerConnection` |
| Server-Relay-Fallback (HTTP-Queue) | ✅ **REALISIERT** | `rendezvous.py:280-293` — `/relay/{sid}` Short-Poll 6×500ms; Auto-Trigger bei ICE-`failed` / 12s-Timer / 3 misses |
| Zuverlässigkeit: ACK + Seq + Dedup | ✅ **REALISIERT** | `quizaway_v5.html:5191-5194` — `nextSeq`/`pending`/`seenSeqs:Set` („Schicht 2") |
| Ping/Pong-Heartbeat | ✅ **REALISIERT** | Client→Server 10s (`:2883`), P2P-DC 5s, `missedPings`-Eskalation → Relay |
| Warteraum/Lobby + Matchmaking | ✅ **REALISIERT** | `rendezvous.py:382-545` — `/warteraum/*`, **serverseitige atomare CAS-Paarung** (kein Client-Race) |
| GPS-Warteraum (Aktivitätsfilter) | ✅ **REALISIERT** | `rendezvous.py:250-266` — nur `state=FREE` & Heartbeat < 30s sichtbar |
| Rundensync / Wahlrecht / Auto-Advance | ✅ **REALISIERT** | `quizaway_v5.html` — deterministisches Wahlrecht (Host 1/3, Guest 2/4), 30s-Timeout, 5s-Auto-Advance |
| Service-Worker-Cache-Disziplin | ✅ **REALISIERT** (gelernt) | dynamische Endpunkte aus SW-Cache ausgeschlossen (`duell_verbindung_learnings.md §4 Bug C`) |
| Signierte Events / Feed-ID=hash(pubkey) / Content-Hash | 📋 **KONZEPT** | `quizaway_konzept-9.md:406-414` („Zielbild") |
| Event-Ledger-Sync | 📋 **KONZEPT** | `quizaway_konzept-9.md:372-403` („Neubau geplant") |
| Bloom-Filter-Gossip / Merkle-Tree-Sync | 📋 **KONZEPT** | `quizaway_konzept-9.md:386-402` |
| Nostr-Relay | 📋 **KONZEPT** | `quizaway_konzept-9.md:445` (als Möglichkeit) |
| `@xalento/p2p-tele` als extrahiertes Paket | 📋 **KONZEPT** | `Xalento/.../p2p-tele-*` — Design fertig, Code-Extraktion wartet (s. §4) |

---

## 3. Architektonische Lehren des Prototyps (für die Tele-Schicht relevant)

Aus `duell_verbindung_learnings.md` — bereits gelöste, nicht-triviale Probleme, die eine künftige Tele-Schicht *erben* sollte:

- **Rendezvous ist zwingend** (NAT/CGNAT) und muss **Always-On** sein — Render-Free-Tier schläft nach 15 min, erster Request ~30 s (für Duell-Start untragbar).
- **TURN-Realität:** öffentliche Open-Relay-Server unzuverlässig → **eigener Relay-Fallback** wurde robuster als TURN.
- **Nahtloser WebRTC→Relay-Übergang** war der schwierigste Teil (3 dokumentierte Bugs: `dc.onclose`-Spielreset, Poll-Loop nach Spielende, SW-Cache der API).
- **ACK+Dedup über unzuverlässigem HTTP-Poll** ist Pflicht; Timeouts ≥30 s wegen 3 s-Short-Poll-Latenz.
- **Empfehlung Neubau:** WebSocket statt HTTP-Poll; eigener coturn; ACK-Protokoll „in eine generische Klasse auslagern" — exakt der Tele-Schicht-Gedanke.

---

## 4. Verhältnis zu `@xalento/p2p-tele` (Xalento-Konzepte v1.3)

Die `p2p-tele-vereinheitlichung-modell-und-technik-v1.3` definiert eine **app-übergreifende Drei-Ebenen-Architektur** — die **deckungsgleich** mit v1.1 §7 (Tele/Coordinator) ist:

```
DOMÄNE         — App-Spielregeln (NICHT geteilt)            ⇄ v1.1: MatchCoordinator-Inhalt
VERBEN-SCHICHT — Protocol (CommittedAction/ack/epoch/Idempotenz)
               + Session (Rendezvous, Matchmaking, Reconnect)  ⇄ v1.1: MatchCoordinator-Hülle
PLATTFORM      — Transport: WebRTC, STUN/TURN, Relay-Fallback  ⇄ v1.1: @xalento/p2p-tele (Transport)
```

- **Initial-Konsumenten im Konzept:** (1) QuizAway-Duell = **realisiert**; (2) MixMi-Tele = **Konzept**.
- **Setzung (ADR-A12-konform):** **Pattern-Sharing ja, Code-Extraktion nein** — wartet auf den 2. realen Konsumenten (MixMi-Tele). Geplanter Zwischenschritt: **Mobile-WebRTC-Lifecycle-Spike** (Tab-Wechsel/Displaysperre/Reconnect verifizieren), *bevor* Code-Entscheidungen fallen.

---

## 5. Korrektur/Präzisierung zu PC-Session-Fokus Punkt 4

Mein erster Befund („Transport nur als vermischter Single-File-Prototyp; Schicht-Trennung = Green-Field, nichts nachzuziehen") war **zu hart**. Präziser:

1. **Es gibt sehr wohl realen Transport-Code** — nur eben nicht als npm-Paket, sondern als **deployte Referenz-Implementierung** (`rendezvous.py` + Client-Stack). Diese ist die **Extraktions-Quelle**, nicht bloß ein Mahnmal.
2. **Die Ziel-Schichtung ist bereits konzipiert** (`p2p-tele-*` v1.3) und stimmt mit v1.1 §7 überein. „Schicht-Trennung nachziehen" heißt also: die *vorhandene* Prototyp-Logik gemäß *vorhandenem* Konzept extrahieren — nicht von null entwerfen.
3. **Unverändert gilt:** das **Paket** `@xalento/p2p-tele` existiert noch nicht (Code-Extraktion bewusst aufgeschoben bis MixMi-Tele als 2. Konsument), und der Prototyp-Client mischt Transport & Domäne in einer Datei (sauber zu trennen bei Extraktion). Die ESLint/depcruise-Schranke (Tele kennt kein Packet/Round/Reveal) bleibt Regel-11-Pflicht *vor* der Tele-Tranche.

**Netto:** Für die Sparthese ist das **gute Nachricht** — der teuerste Brocken (robuster P2P-Transport inkl. Relay-Fallback) ist **schon einmal gebaut und im Feld erprobt**; er muss „nur" extrahiert/portiert (idealerweise auf WebSocket) werden, nicht erfunden.
