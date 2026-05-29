# quizaway — Dev-Setup & Start (PC + Laptop)

quizaway ist eine **statische HTML/JS-PWA** (Vanilla, kein Build, **kein npm**).
Dateien: `quizaway_v*.html`, `duel_sim.html`, `manifest.json`, `sw.js`, `public/`.

> ⚠️ `npm install` schlägt fehl — es gibt **keine `package.json`**. Das ist
> kein Fehler, sondern korrekt: quizaway braucht kein Node.

---

## Shell-Hinweis (cmd vs PowerShell)

| Aktion | cmd | PowerShell |
|---|---|---|
| Verzeichnis (+ Laufwerk) wechseln | `cd /d D:\pfad` | `cd D:\pfad` |

(Hier keine Env-Vars / kein npm nötig — also kaum Shell-Unterschiede.)

---

## 1. Voraussetzungen
- **Browser** + **Python** (für den statischen Server; ist schon installiert).

---

## 2. Starten (statisch servieren)
```
cd  D:\claude-code\LernApp\apps\quizaway       (cmd: cd /d …)
python -m http.server 8765
```
Dann im Browser die **aktuelle Version** öffnen, z. B.:
`http://localhost:8765/quizaway_v5.html`
(welche Version aktuell ist → siehe `STATUS.md` im selben Ordner; es gibt
`quizaway_v2…v5.html` + `duel_sim.html`).

Entspricht der `duel-sim`-Launch-Config (`python -m http.server 8765 --directory …\quizaway`).

---

## 3. Refactoring
Vanilla HTML/JS/PWA → die `.html` / `.js` / `sw.js` **direkt editieren**,
Browser neu laden. **Kein Build, kein node_modules, kein Vite.** Das einfachste
der Urlaubs-Projekte.

PWA-Caveat: `sw.js` (Service Worker) cached aggressiv — bei Änderungen ggf.
**Hard-Reload** (Strg+Shift+R) oder im DevTools-Application-Tab „Unregister".

---

## 4. Randnotiz
Im LernApp-**Root** liegen `requirements.txt` + `python/` + `render.yaml` — das ist
separates Python-Tooling (Daten/Deploy), **nicht** zum Laufenlassen von quizaway.
Nur falls du daran arbeitest, dafür ein venv (`py -3.12 -m venv .venv`).

---

## 5. Cross-Machine-Workflow
- **Code** über git (GitHub-Repo der LernApp): `git pull` → Branch → commit → push.
- **Memory** synct NICHT über git — manuell reconcilen.
- **Regel 10 + System-Verhaltensmodell** gelten (siehe `CLAUDE.md` im LernApp-Root).
