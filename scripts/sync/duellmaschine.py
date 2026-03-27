"""
Duellmaschine — Rendezvous-Server
Dieselbe Architektur wie rendezvous.py (http.server + ThreadingMixIn)
Separater Endpunkt für die Duellmaschine — keine Interferenz mit QuizAway

Startet mit: python duellmaschine.py
Port: $PORT (Render) oder 8081 (lokal)

Endpunkte:
  GET  /                        → duellmaschine.html
  GET  /ping                    → Health-Check
  GET  /warteraum/liste         → Alle FREE-Spieler
  GET  /warteraum/status/ID     → Eigener Zustand + Herausforderung
  POST /warteraum/betreten      → Warteraum betreten
  POST /warteraum/verlassen     → Warteraum verlassen
  POST /warteraum/heartbeat     → Lebenszeichen (verhindert TTL-Ablauf)
  POST /warteraum/reservieren   → Atomare Host/Guest-Zuweisung (CAS)
  POST /warteraum/herausforderung/update  → Angebots-ID nachliefern
  POST /lobby/create            → WebRTC-Angebot erstellen
  POST /lobby/join/ID           → Angebot beitreten
  POST /lobby/offer/ID          → Offer hinterlegen
  POST /lobby/cancel/ID         → Angebot abbrechen
  GET  /lobby/offer/ID          → Offer abrufen (Guest)
  GET  /lobby/status/ID         → Angebots-Status (Host polling)
  POST /answer/ID               → Answer hinterlegen
  GET  /answer/ID               → Answer abrufen (Host)
"""

import json, random, string, os, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from socketserver import ThreadingMixIn

# ─── Stores ──────────────────────────────────────────────────
store        = {}   # pin -> { offer, answer }
lobby        = {}   # id  -> angebot
warteraum    = {}   # id  -> spieler

warteraum_lock = threading.Lock()
lobby_lock     = threading.Lock()

# TTL-Konstanten
WARTERAUM_TTL = 120   # 120s — Puffer für mobile Background-Tabs (Heartbeat alle 10s)
LOBBY_TTL     = 300   # 5 Minuten

# ─── Hilfsfunktionen ─────────────────────────────────────────

def new_id(n=8):
    """Zufällige numerische ID die noch nicht vergeben ist."""
    while True:
        pid = ''.join(random.choices(string.digits, k=n))
        if pid not in store and pid not in lobby and pid not in warteraum:
            return pid

def cas(spieler_id, expected, new):
    """Compare-and-Swap auf warteraum[spieler_id].state — muss unter warteraum_lock aufgerufen werden."""
    if spieler_id not in warteraum:
        return False
    if warteraum[spieler_id]['state'] == expected:
        warteraum[spieler_id]['state'] = new
        return True
    return False

def warteraum_cleanup():
    now = time.time()
    with warteraum_lock:
        abgelaufen = [k for k, v in warteraum.items()
                      if now - v['zuletzt_gesehen'] > WARTERAUM_TTL]
        for k in abgelaufen:
            print(f"  [cleanup] Warteraum: {warteraum[k]['name']} ({k}) abgelaufen (TTL={WARTERAUM_TTL}s)")
            del warteraum[k]

def lobby_cleanup():
    now = time.time()
    with lobby_lock:
        abgelaufen = [k for k, v in lobby.items()
                      if now - v['erstellt'] > LOBBY_TTL]
        for k in abgelaufen:
            del lobby[k]
            if k in store:
                del store[k]

def lobby_liste_offen():
    lobby_cleanup()
    with lobby_lock:
        return [
            {'id': v['id'], 'schwierigkeit': v['schwierigkeit'],
             'host_name': v['host_name'], 'erstellt': v['erstellt']}
            for v in lobby.values()
            if v['status'] == 'offen'
        ]

# ─── Hintergrund-Cleanup ─────────────────────────────────────

def _hintergrund_cleanup():
    while True:
        time.sleep(15)
        try:
            # Timeout-Ereignisse loggen bevor cleanup löscht
            now = time.time()
            with warteraum_lock:
                abgelaufen = [(k, v['name']) for k, v in warteraum.items()
                              if now - v['zuletzt_gesehen'] > WARTERAUM_TTL]
            for k, name in abgelaufen:
                event_add('verlassen', name, 'timeout')
            warteraum_cleanup()
            lobby_cleanup()
        except Exception as e:
            print(f'  [cleanup] Fehler: {e}')

# ─── Event-Log ───────────────────────────────────────────────
# Ereignisse sichtbar für alle Clients im Warteraum
# typ:   betreten | verlassen | verbunden | fallback
# grund: aktiv | timeout | klick | timer | vg | p2p

events      = []
events_lock = threading.Lock()
MAX_EVENTS  = 50

def event_add(typ, name, grund=None):
    with events_lock:
        events.append({
            'ts':    int(time.time() * 1000),
            'typ':   typ,
            'name':  name,
            'grund': grund,
        })
        while len(events) > MAX_EVENTS:
            events.pop(0)
    g = f' ({grund})' if grund else ''
    print(f'  [event] {typ} — {name}{g}')

# ─── HTTP-Server ─────────────────────────────────────────────

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} {fmt % args}")

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, path):
        if not os.path.exists(path):
            self.send_json(404, {'error': f'{path} nicht gefunden'}); return
        with open(path, 'rb') as f:
            body = f.read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        p = urlparse(self.path).path

        # ── Statische Dateien ─────────────────────────────────
        if p in ('/', '/index.html', '/duellmaschine.html'):
            self.send_html('duellmaschine.html'); return

        # ── Health-Check ──────────────────────────────────────
        if p == '/ping':
            with warteraum_lock:
                n_spieler = len(warteraum)
            self.send_json(200, {
                'ok': True,
                'status': 'alive',
                'spieler_im_warteraum': n_spieler,
                'ts': int(time.time() * 1000)
            }); return

        # ── Warteraum ─────────────────────────────────────────

        # GET /warteraum/events  →  Letzten N Ereignisse
        if p == '/warteraum/events':
            with events_lock:
                recent = list(events[-30:])
            self.send_json(200, {'events': recent}); return

        # GET /warteraum/liste  →  Alle FREE-Spieler
        if p == '/warteraum/liste':
            warteraum_cleanup()
            with warteraum_lock:
                spieler = [
                    {'id': v['id'], 'name': v['name'], 'liga': v['liga'],
                     'eingetreten': int(v['eingetreten'] * 1000)}
                    for v in warteraum.values()
                    if v['state'] == 'FREE'
                ]
            self.send_json(200, {'spieler': spieler}); return

        # GET /warteraum/status/ID
        if p.startswith('/warteraum/status/'):
            wid = p.split('/')[-1]
            with warteraum_lock:
                eintrag = warteraum.get(wid)
            if not eintrag:
                self.send_json(404, {'error': 'Nicht im Warteraum'}); return
            self.send_json(200, {
                'state': eintrag['state'],
                'herausforderung': eintrag.get('herausforderung')
            }); return

        # ── WebRTC-Signaling ──────────────────────────────────

        # GET /answer/ID
        if p.startswith('/answer/'):
            pid = p.split('/')[-1]
            if pid not in store:
                self.send_json(404, {'error': 'Unbekannte ID'}); return
            self.send_json(200, {'answer': store[pid].get('answer')}); return

        # GET /offer/ID
        if p.startswith('/offer/'):
            pid = p.split('/')[-1]
            if pid not in store or not store[pid].get('offer'):
                self.send_json(404, {'error': 'Kein Offer'}); return
            self.send_json(200, {'offer': store[pid]['offer']}); return

        # ── Lobby ─────────────────────────────────────────────

        # GET /lobby  →  Liste offener Angebote
        if p == '/lobby':
            self.send_json(200, {'angebote': lobby_liste_offen()}); return

        # GET /lobby/status/ID
        if p.startswith('/lobby/status/'):
            aid = p.split('/')[-1]
            with lobby_lock:
                ang = lobby.get(aid)
            if not ang:
                self.send_json(404, {'error': 'Angebot nicht gefunden'}); return
            self.send_json(200, {
                'status':     ang['status'],
                'guest_name': ang.get('guest_name'),
                'offer':      store.get(aid, {}).get('offer')
            }); return

        # GET /lobby/offer/ID  (Guest holt Offer)
        if p.startswith('/lobby/offer/'):
            aid = p.split('/')[-1]
            offer = store.get(aid, {}).get('offer')
            if not offer:
                self.send_json(200, {'offer': None, 'ready': False}); return
            self.send_json(200, {'offer': offer, 'ready': True}); return

        self.send_json(404, {'error': 'Nicht gefunden'})

    do_HEAD = do_GET

    def do_POST(self):
        p      = urlparse(self.path).path
        length = int(self.headers.get('Content-Length', 0))
        body   = json.loads(self.rfile.read(length)) if length else {}

        # ── Warteraum ─────────────────────────────────────────

        # POST /warteraum/event  { name, typ, grund }  →  Client meldet Ereignis
        if p == '/warteraum/event':
            event_add(
                body.get('typ',   'info'),
                body.get('name',  'Spieler'),
                body.get('grund', None)
            )
            self.send_json(200, {'ok': True}); return

        # POST /warteraum/betreten  { name, liga }  →  { id }
        if p == '/warteraum/betreten':
            warteraum_cleanup()
            wid = new_id(8)
            now = time.time()
            with warteraum_lock:
                warteraum[wid] = {
                    'id':              wid,
                    'name':            body.get('name', 'Spieler'),
                    'liga':            body.get('liga', 'bronze'),
                    'eingetreten':     now,
                    'zuletzt_gesehen': now,   # ← NEU: für Heartbeat-TTL
                    'state':           'FREE',
                    'partner':         None,
                    'herausforderung': None,
                }
            print(f"  Warteraum: {body.get('name','?')} betreten (id={wid})")
            event_add('betreten', body.get('name', 'Spieler'))
            self.send_json(200, {'id': wid}); return

        # POST /warteraum/verlassen  { id }  →  { ok }
        if p == '/warteraum/verlassen':
            wid = body.get('id')
            with warteraum_lock:
                if wid in warteraum:
                    name = warteraum[wid]['name']
                    del warteraum[wid]
                    print(f"  Warteraum: {name} ({wid}) verlassen")
                    event_add('verlassen', name, 'aktiv')
            self.send_json(200, {'ok': True}); return

        # POST /warteraum/heartbeat  { id }  →  { ok }
        # Spieler meldet sich — verlängert TTL, verhindert automatisches Austragen
        if p == '/warteraum/heartbeat':
            wid = body.get('id')
            with warteraum_lock:
                if wid in warteraum:
                    warteraum[wid]['zuletzt_gesehen'] = time.time()
                    self.send_json(200, {'ok': True}); return
            self.send_json(404, {'error': 'Nicht im Warteraum'}); return

        # POST /warteraum/reservieren  { meine_id, gegner_id, host_name }
        # CAS-Kern: atomar entscheidet ob Host oder Guest
        if p == '/warteraum/reservieren':
            meine_id  = body.get('meine_id')
            gegner_id = body.get('gegner_id')
            host_name = body.get('host_name', 'Spieler')

            if not meine_id:
                self.send_json(409, {'error': 'Eigene ID fehlt'}); return

            with warteraum_lock:
                # Schritt 1: Wurde ich selbst bereits herausgefordert?
                if meine_id in warteraum:
                    hf = warteraum[meine_id].get('herausforderung')
                    if hf:
                        cas(meine_id, 'CLAIMED', 'PAIRED')
                        print(f"  Reservieren: {meine_id} ist GUEST (bereits CLAIMED)")
                        self.send_json(200, {'rolle': 'guest', 'herausforderung': hf}); return

                # Schritt 2: Gegner verfügbar?
                if not gegner_id or gegner_id not in warteraum:
                    self.send_json(409, {'error': 'Gegner nicht verfügbar'}); return

                # CAS: Gegner FREE → CLAIMED
                if not cas(gegner_id, 'FREE', 'CLAIMED'):
                    # Gegner nicht mehr frei — nochmal prüfen ob ich selbst herausgefordert wurde
                    if meine_id in warteraum:
                        hf = warteraum[meine_id].get('herausforderung')
                        if hf:
                            cas(meine_id, 'CLAIMED', 'PAIRED')
                            self.send_json(200, {'rolle': 'guest', 'herausforderung': hf}); return
                    self.send_json(409, {'error': 'Gegner nicht verfügbar'}); return

                # CAS: Ich FREE → CLAIMED
                if meine_id in warteraum:
                    if not cas(meine_id, 'FREE', 'CLAIMED'):
                        # Rollback Gegner
                        cas(gegner_id, 'CLAIMED', 'FREE')
                        hf = warteraum[meine_id].get('herausforderung')
                        if hf:
                            cas(meine_id, 'CLAIMED', 'PAIRED')
                            self.send_json(200, {'rolle': 'guest', 'herausforderung': hf}); return
                        self.send_json(409, {'error': 'Eigener Zustand geändert'}); return

                # Beide CLAIMED → Herausforderung setzen → PAIRED
                warteraum[gegner_id]['herausforderung'] = {
                    'angebots_id':   None,
                    'schwierigkeit': 'M',
                    'host_name':     host_name
                }
                cas(gegner_id, 'CLAIMED', 'PAIRED')
                if meine_id in warteraum:
                    cas(meine_id, 'CLAIMED', 'PAIRED')
                print(f"  Reservieren: {meine_id}=HOST vs {gegner_id}=GUEST")
                event_add('verbunden',
                          f'{host_name} ↔ {warteraum[gegner_id]["name"]}',
                          'p2p')

            self.send_json(200, {'rolle': 'host'}); return

        # POST /warteraum/herausforderung/update  { gegner_id, angebots_id, schwierigkeit }
        if p == '/warteraum/herausforderung/update':
            gegner_id   = body.get('gegner_id')
            angebots_id = body.get('angebots_id')
            schwier     = body.get('schwierigkeit', 'M')
            with warteraum_lock:
                if gegner_id in warteraum and warteraum[gegner_id].get('herausforderung'):
                    warteraum[gegner_id]['herausforderung']['angebots_id']   = angebots_id
                    warteraum[gegner_id]['herausforderung']['schwierigkeit'] = schwier
                    print(f"  HF-Update: {gegner_id} → Angebot {angebots_id}")
            self.send_json(200, {'ok': True}); return

        # ── WebRTC-Signaling ──────────────────────────────────

        # POST /offer/ID  { sdp }
        if p.startswith('/offer/'):
            pid = p.split('/')[-1]
            if pid not in store:
                self.send_json(404, {'error': 'Unbekannte ID'}); return
            store[pid]['offer'] = body.get('sdp', '')
            print(f"  Offer {pid}: gespeichert ({len(store[pid]['offer'])} Zeichen)")
            self.send_json(200, {'ok': True}); return

        # POST /answer/ID  { sdp }
        if p.startswith('/answer/'):
            pid = p.split('/')[-1]
            if pid not in store:
                self.send_json(404, {'error': 'Unbekannte ID'}); return
            store[pid]['answer'] = body.get('sdp', '')
            print(f"  Answer {pid}: gespeichert ({len(store[pid]['answer'])} Zeichen)")
            self.send_json(200, {'ok': True}); return

        # ── Lobby ─────────────────────────────────────────────

        # POST /lobby/create  { host_name }  →  { id }
        if p == '/lobby/create':
            aid = new_id(6)
            with lobby_lock:
                lobby[aid] = {
                    'id':         aid,
                    'host_name':  body.get('host_name', 'Spieler'),
                    'erstellt':   time.time(),
                    'status':     'offen',
                    'guest_name': None,
                }
            store[aid] = {'offer': None, 'answer': None}
            print(f"  Lobby {aid}: erstellt von {body.get('host_name','?')}")
            self.send_json(200, {'id': aid}); return

        # POST /lobby/join/ID  { guest_name }  →  atomar beitreten
        if p.startswith('/lobby/join/'):
            aid = p.split('/')[-1]
            with lobby_lock:
                ang = lobby.get(aid)
                if not ang:
                    self.send_json(404, {'error': 'Angebot nicht gefunden'}); return
                if ang['status'] != 'offen':
                    self.send_json(409, {'error': 'Bereits angenommen'}); return
                ang['status']     = 'angenommen'
                ang['guest_name'] = body.get('guest_name', 'Gast')
            print(f"  Lobby {aid}: angenommen von {body.get('guest_name','?')}")
            self.send_json(200, {
                'ok': True,
                'schwierigkeit': ang.get('schwierigkeit', 'M'),
                'host_name':     ang['host_name']
            }); return

        # POST /lobby/offer/ID  { sdp }
        if p.startswith('/lobby/offer/'):
            aid = p.split('/')[-1]
            if aid not in store:
                self.send_json(404, {'error': 'Nicht gefunden'}); return
            store[aid]['offer'] = body.get('sdp', '')
            print(f"  Lobby {aid}: Offer hinterlegt")
            self.send_json(200, {'ok': True}); return

        # POST /lobby/cancel/ID  { rolle }
        if p.startswith('/lobby/cancel/'):
            aid = p.split('/')[-1]
            with lobby_lock:
                ang = lobby.get(aid)
                if not ang:
                    self.send_json(404, {'error': 'Nicht gefunden'}); return
                del lobby[aid]
                if aid in store:
                    del store[aid]
            print(f"  Lobby {aid}: abgebrochen")
            self.send_json(200, {'ok': True}); return

        self.send_json(404, {'error': 'Nicht gefunden'})

    def do_DELETE(self):
        p = urlparse(self.path).path
        if p.startswith('/lobby/'):
            aid = p.split('/')[-1]
            with lobby_lock:
                if aid in lobby: del lobby[aid]
                if aid in store: del store[aid]
            print(f"  Lobby {aid}: gelöscht (DELETE)")
            self.send_json(200, {'ok': True}); return
        self.send_json(404, {'error': 'Nicht gefunden'})


if __name__ == '__main__':
    import sys

    port = int(os.environ.get('PORT', 8081))
    if '--port' in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index('--port') + 1])
        except:
            pass

    threading.Thread(target=_hintergrund_cleanup, daemon=True, name='cleanup').start()
    print('[cleanup] Hintergrund-Bereinigung gestartet (alle 15s, TTL=30s)')

    server = ThreadedHTTPServer(('0.0.0.0', port), Handler)
    print(f"\nDuellmaschine Rendezvous-Server")
    print(f"Lokal:      http://localhost:{port}")
    print(f"Smartphone: http://<deine-IP>:{port}")
    print("Strg+C zum Beenden\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer beendet.")
