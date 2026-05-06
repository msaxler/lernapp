# WP-MIKE-PC-WAKE: Mobiler PC-Aufweck-Mechanismus über Pi-Mediator

**Status:** Proposed
**Datum:** 2026-05-06
**Geltungsbereich:** Mike-Copilot Infrastruktur, Vorstufe zu `/rc`-Workflow
**Verwandt:** ADR-001 Copilot-Architektur-Pattern
**Abhängigkeit:** Kein Blocker für den QuizAway-Pilot — Pilot läuft manuell bis dieses WP umgesetzt ist.

---

## 1. Zielbild

Vom Smartphone aus den heimischen Windows-PC aufwecken, sodass Claude
Code mit `/rc` automatisch erreichbar wird — auch wenn der PC nur per
WLAN angebunden ist.

**Kernidee:** Ein Raspberry Pi als kleiner, dauerhaft erreichbarer
Mediator im Heimnetz. Pi nimmt vom Handy einen Aufweck-Befehl entgegen
und löst PC-Boot aus — über zwei Pfade (Soft / Hard) für Robustheit.

---

## 2. Architektur (Soll-Zustand)

```
Smartphone (Tailscale-App)
      ↕
Tailscale-Netzwerk
      ↕
Raspberry Pi (24/7, WLAN, Tailscale)
      ├── Soft-Pfad: sendet Magic Packet ins LAN
      └── Hard-Pfad (Fallback): GPIO → Relais → PC Power-Button-Pin
              ↕
       Windows-PC
       ├── Auto-Login
       ├── Aufgabenplanung startet nach Login Claude Code mit /rc
       └── Tailscale Daemon (unattended)
              ↕
       Anthropic API (für /rc-Polling)
```

**Sicherheitsmodell:** Keine eingehenden Ports am Heim-Router.
Sämtlicher Zugriff von außen läuft ausschließlich über Tailscale.

---

## 3. Hardware-Beschaffung

**Pflicht:**
- Raspberry Pi (4, 5 oder Zero 2 W)
- microSD-Karte 32 GB (Class 10 / A1 oder besser)
- Pi-Netzteil (offiziell, passend zum Modell)
- microSD-Kartenleser für initiale Bespielung am PC

**Für Hard-Pfad-Fallback:**
- 1-Channel-Relais-Modul für Raspberry Pi, 3,3V-kompatibel
- 2 × Jumper-Kabel female-female (GPIO → Relais)
- 2 × Jumper-Kabel female-female (Relais → Mainboard)

Budget gesamt: ca. 60–90 €.

---

## 4. Schritte

### Schritt 0 — BIOS-Check (vor Hardware-Beschaffung)

- BIOS aufrufen (F2 / Entf / F12 beim Boot)
- Suche nach: *Wake on LAN*, *Wake on Wireless LAN*, *WoWLAN*, *Power on by PME*
- Falls vorhanden: aktivieren, Werte notieren
- Suche nach: *Deep Sleep*, *ErP Ready* — falls aktiv, deaktivieren

**Ergebnis-Dokumentation:**
- [ ] WoWLAN-Option im BIOS gefunden und aktiviert
- [ ] Keine WoWLAN-Option → Soft-Pfad ausgeschlossen, Hard-Pfad zwingend
- [ ] Unsicher → beim Test klären

### Schritt 1 — Pi beschaffen und Grundsystem

- Hardware kaufen (siehe Abschnitt 3)
- Raspberry Pi OS Lite (64-bit) auf microSD flashen (Raspberry Pi Imager)
- Beim Flashen konfigurieren: Hostname (`wake-mediator`), WLAN, SSH, User
- Pi booten, SSH verbinden, System aktualisieren

**Abbruch-Kriterium:** Kein SSH-Erreichen nach 30 Minuten → neu flashen.

### Schritt 2 — Tailscale auf dem Pi

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Login im Browser. Pi erscheint im Tailscale-Admin als neuer Knoten.

**Test:** Vom Handy (außerhalb Heim-WLAN) per SSH-App auf den Pi verbinden.

### Schritt 3 — Soft-Pfad: Magic Packet vom Pi

```bash
sudo apt install wakeonlan
# MAC-Adresse des PC-WLAN-Adapters: am PC ipconfig /all
wakeonlan AA:BB:CC:DD:EE:FF
```

**Drei Ergebnisse:**
- PC wacht auf → Soft-Pfad funktioniert → weiter zu Schritt 5.
- PC wacht nicht auf, BIOS hat WoWLAN → Treiber/Windows prüfen (max. 60 Min).
- PC wacht nicht auf, kein WoWLAN → direkt Schritt 4.

**Falsifikationspunkt:** Nach 60 Min Fehlersuche → Hard-Pfad akzeptieren.

### Schritt 4 — Hard-Pfad: Relais am Power-Button

**Voraussetzung:** PC ausgeschaltet, vom Strom getrennt, Gehäuse offen.

- Power-Button-Pins am Mainboard identifizieren (oft `PWR_SW` oder `PWR BTN`)
- Relais-Modul am Pi:
  - VCC → Pi 3,3V (Pin 1)
  - GND → Pi GND (Pin 6)
  - IN → GPIO17 (Pin 11)
- Relais-Ausgang (NO + COM) parallel zum Power-Button-Pin
- Steuer-Skript (Python mit `RPi.GPIO`): GPIO17 für ~300 ms auf HIGH

**Abbruch-Kriterium:** Pin-Identifikation unklar → Mainboard-Handbuch besorgen. Nicht raten.

### Schritt 5 — Auslösung vom Handy

**Variante A — minimal (SSH):**
- SSH-App (Termius, JuiceSSH) → Pi über Tailscale → Skript ausführen

**Variante B — komfortabler (Flask Web-UI):**
- Mini-Flask-Server am Pi, Endpunkt `/wake`
- Nur über Tailscale-IP erreichbar, einfacher Token-Header
- Lesezeichen am Handy → ein Tap

Empfehlung: Mit A starten, B als Patch nachziehen.

### Schritt 6 — Windows-Seite: Auto-Start Claude Code

- Auto-Login: `netplwiz` → Häkchen entfernen
- Aufgabenplanung: bei Anmeldung → Terminal → Projektordner → `claude --remote-control`
- Tailscale auf PC: Auto-Start, unattended

**Test des kompletten Pfads:**
1. PC ausschalten
2. Vom Handy (mobile Daten) Aufweck-Befehl an Pi
3. PC bootet, einloggen, Claude Code startet mit `/rc`
4. In Claude-App auf Handy: Session sichtbar
5. Antippen → mobil arbeiten

---

## 5. Sicherheitsabwägung

**Unkritisch:** Keine eingehenden Ports. Pi und PC nur über Tailscale erreichbar.

**Bewusst akzeptiert:**
- **Auto-Login auf Windows-PC:** Wer physischen Zugriff hat, ist eingeloggt. Akzeptabel bei räumlichem Schutz.
- **Pi mit Tailscale:** Wer Zugriff auf Tailscale-Konto hat, kann PC wecken. → 2FA aktivieren.

---

## 6. Validierung

**Akzeptanzkriterien (alle müssen erfüllt sein):**
1. Vom Handy außerhalb Heim-WLAN PC innerhalb 90 Sekunden wecken, `/rc`-Session sichtbar.
2. Mechanismus funktioniert nach 7 Tagen ohne Eingriff.
3. 5 von 5 Versuchen erfolgreich.

**Falsifikationskriterium:** < 4/5 Versuche erfolgreich → Hard-Pfad als Default oder Always-On neu erwägen.

---

## 7. Offene Punkte

- [ ] BIOS-Check-Ergebnis (Schritt 0)
- [ ] Pi-Modell beschafft
- [ ] Soft-Pfad funktioniert ja/nein
- [ ] Hard-Pfad nötig ja/nein
- [ ] Steuerungs-Variante: A (SSH) oder B (Web-UI)
- [ ] Auto-Login auf PC akzeptiert ja/nein

---

## 8. Zeitschätzung

| Schritt | Aufwand |
|---------|---------|
| 0 BIOS-Check | 15–30 Min |
| 1 Pi-Grundsystem | 30–45 Min |
| 2 Tailscale | 15 Min |
| 3 Soft-Pfad-Test | 30 Min |
| 4 Hard-Pfad (falls nötig) | 60–90 Min |
| 5 Steuerung Variante A | 15 Min |
| 5 Steuerung Variante B (optional) | 60 Min |
| 6 Windows-Seite | 30 Min |
| **Gesamt** | **3–5 Stunden** |
