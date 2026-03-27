# Duellmaschine

Standalone Proof-of-Concept für den QuizAway Duell-Modus.

## Dateien

| Datei | Zweck |
|---|---|
| `duellmaschine.html` | Client — vollständig timergesteuert, keine echten Fragen |
| `duellmaschine.py`   | Rendezvous-Server — Warteraum, WebRTC-Signaling, CAS |
| `Procfile`           | Render-Deployment |

## Lokal starten

```bash
python duellmaschine.py
# öffne http://localhost:8081
```

## Auf Render deployen

1. Neuen Web Service anlegen
2. Root Directory: Ordner mit diesen Dateien
3. Start Command: `python duellmaschine.py`
4. Port: automatisch via `$PORT`

## UptimeRobot

Monitor Type: HTTP(s)
URL: `https://<dein-service>.onrender.com/ping`
Interval: 5 Minuten

## Testen

Vier Tabs im selben Browser öffnen — alle zeigen die Debug-Leiste oben.
Spieler-Namen vergeben, Warteraum betreten, gegenseitig finden und duellieren.
Log-Panel über den LOG-Button öffnen für detaillierte Protokollansicht.
