"""
Rendezvous-Server mit Lobby/Matchmaking
Startet mit: python rendezvous.py
Port 8080 — liefert HTML, SQLite, WebRTC-Signaling und Duell-Lobby
"""
import json, random, string, os, time, threading
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── Bootstrap: geo.sqlite herunterladen falls nicht vorhanden ────────────────
GEO_URL  = 'https://github.com/msaxler/lernapp/releases/download/v1.0-data/geo.sqlite'
GEO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'geo.sqlite')

if not os.path.exists(GEO_PATH):
    print('[Bootstrap] geo.sqlite nicht gefunden, lade herunter...')
    os.makedirs(os.path.dirname(GEO_PATH), exist_ok=True)
    urllib.request.urlretrieve(GEO_URL, GEO_PATH)
    print(f'[Bootstrap] Fertig ({os.path.getsize(GEO_PATH)//1024//1024} MB)')
else:
    print(f'[Bootstrap] geo.sqlite vorhanden ({os.path.getsize(GEO_PATH)//1024//1024} MB)')
# ────────────────────────────────────────────────────────────────────────────

from urllib.parse import urlparse
from socketserver import ThreadingMixIn

# ─── WebRTC-Signaling Store ──────────────────────────────────
store = {}  # pin -> {'offer': sdp, 'answer': sdp}

def new_pin():
    while True:
        pin = ''.join(random.choices(string.digits, k=6))
        if pin not in store and pin not in lobby:
            return pin

# ─── Warteraum Store — CAS-Modell ────────────────────────────
# state[i] ∈ { FREE, CLAIMED, PAIRED, LEFT }
# partner[i] ∈ { None, spieler_id, 'VIRTUAL' }
# Eintrag: { id, name, liga, eingetreten, state, partner, herausforderung }
warteraum = {}
warteraum_lock = threading.Lock()
WARTERAUM_TTL = 90   # 90s — Spieler werden automatisch entfernt

def warteraum_cleanup():
    now = time.time()
    with warteraum_lock:
        abgelaufen = [k for k,v in warteraum.items()
                      if now - v['eingetreten'] > WARTERAUM_TTL]
        for k in abgelaufen:
            del warteraum[k]

def cas(spieler_id, expected_state, new_state):
    """Compare-and-Swap: nur wenn state == expected, setze auf new. Gibt True/False zurück."""
    if spieler_id not in warteraum:
        return False
    if warteraum[spieler_id]['state'] == expected_state:
        warteraum[spieler_id]['state'] = new_state
        return True
    return False
# Duell-Angebot: {
#   id: str,           PIN = Angebots-ID
#   schwierigkeit: L|M|S,
#   erstellt: float,   timestamp
#   status: 'offen'|'angenommen'|'gestartet',
#   host_name: str,
#   guest_name: str|None
# }
lobby = {}           # id -> angebot
lobby_lock = threading.Lock()
LOBBY_TTL = 300      # 5 Minuten — Angebote laufen ab

def lobby_cleanup():
    """Abgelaufene Angebote entfernen"""
    now = time.time()
    with lobby_lock:
        abgelaufen = [k for k,v in lobby.items()
                      if now - v['erstellt'] > LOBBY_TTL]
        for k in abgelaufen:
            del lobby[k]
            if k in store:
                del store[k]

def lobby_liste():
    """Offene Angebote als Liste zurückgeben"""
    lobby_cleanup()
    with lobby_lock:
        return [
            { 'id': v['id'], 'schwierigkeit': v['schwierigkeit'],
              'host_name': v['host_name'], 'erstellt': v['erstellt'] }
            for v in lobby.values()
            if v['status'] == 'offen'
        ]

# ─── Server ──────────────────────────────────────────────────
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
            self.send_json(404, {'error': 'Nicht gefunden'}); return
        with open(path, 'rb') as f:
            body = f.read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Connection', 'close')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()

    def send_binary(self, path, content_type):
        if not os.path.exists(path):
            self.send_json(404, {'error': 'Nicht gefunden'}); return
        with open(path, 'rb') as f:
            body = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Connection', 'close')
        self.send_header('Access-Control-Allow-Origin', '*')
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

        # Dateien ausliefern
        if p == '/' or p == '/index.html':
            self.send_html('quizaway_v4.html'); return
        if p.endswith('.html'):
            self.send_html(p.lstrip('/')); return
        if p.endswith('.sqlite') or p.endswith('.db'):
            self.send_binary(p.lstrip('/'), 'application/octet-stream'); return

        # PWA-Dateien
        if p.endswith('.json'):
            self.send_binary(p.lstrip('/'), 'application/json'); return
        if p.endswith('.js'):
            self.send_binary(p.lstrip('/'), 'application/javascript'); return
        if p.endswith('.png'):
            self.send_binary(p.lstrip('/'), 'image/png'); return

        # Health-Check für UptimeRobot / Monitoring
        if p == '/ping':
            self.send_json(200, {'ok': True, 'status': 'alive'}); return

        # ── WebRTC-Signaling ──────────────────────────────────
        # GET /new  →  { pin }
        if p == '/new':
            pin = new_pin()
            store[pin] = {'offer': None, 'answer': None}
            print(f"  PIN {pin} reserviert")
            self.send_json(200, {'pin': pin}); return

        # GET /answer/PIN
        if p.startswith('/answer/'):
            pin = p.split('/')[-1]
            if pin not in store:
                self.send_json(404, {'error': 'Unbekannter PIN'}); return
            self.send_json(200, {'answer': store[pin].get('answer')}); return

        # GET /offer/PIN
        if p.startswith('/offer/'):
            pin = p.split('/')[-1]
            if pin not in store or not store[pin].get('offer'):
                self.send_json(404, {'error': 'Kein Offer'}); return
            self.send_json(200, {'offer': store[pin]['offer']}); return

        # ── Lobby ─────────────────────────────────────────────
        # GET /lobby  →  Liste offener Angebote
        if p == '/lobby':
            self.send_json(200, {'angebote': lobby_liste()}); return

        # GET /lobby/STATUS/ID  →  Status eines Angebots (polling)
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

        # GET /lobby/offer/ID  →  WebRTC-Offer abrufen (Guest)
        if p.startswith('/lobby/offer/'):
            aid = p.split('/')[-1]
            offer = store.get(aid, {}).get('offer')
            if not offer:
                self.send_json(200, {'offer': None, 'ready': False}); return
            self.send_json(200, {'offer': offer, 'ready': True}); return

        # GET /warteraum/liste  →  Alle FREE-Spieler (max. 4 für Client)
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

        # GET /warteraum/status/ID  →  Eigener Zustand + Herausforderung
        if p.startswith('/warteraum/status/'):
            wid = p.split('/')[-1]
            with warteraum_lock:
                eintrag = warteraum.get(wid)
            if not eintrag:
                self.send_json(404, {'error': 'Nicht im Warteraum'}); return
            self.send_json(200, {
                'state':          eintrag['state'],
                'herausforderung': eintrag.get('herausforderung')
            }); return

    def do_POST(self):
        p = urlparse(self.path).path
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        # ── WebRTC-Signaling ──────────────────────────────────
        if p.startswith('/offer/') and not p.startswith('/offer/join'):
            pin = p.split('/')[-1]
            if pin not in store:
                self.send_json(404, {'error': 'Unbekannter PIN'}); return
            store[pin]['offer'] = body.get('sdp', '')
            print(f"  PIN {pin}: Offer gespeichert ({len(store[pin]['offer'])} Zeichen)")
            self.send_json(200, {'ok': True}); return

        if p.startswith('/answer/'):
            pin = p.split('/')[-1]
            if pin not in store:
                self.send_json(404, {'error': 'Unbekannter PIN'}); return
            store[pin]['answer'] = body.get('sdp', '')
            print(f"  PIN {pin}: Answer gespeichert ({len(store[pin]['answer'])} Zeichen)")
            self.send_json(200, {'ok': True}); return

        # ── Lobby ─────────────────────────────────────────────
        # POST /lobby/create  { schwierigkeit, host_name }  →  { id }
        if p == '/lobby/create':
            aid = new_pin()
            with lobby_lock:
                lobby[aid] = {
                    'id':             aid,
                    'schwierigkeit':  body.get('schwierigkeit', 'M'),
                    'host_name':      body.get('host_name', 'Spieler'),
                    'erstellt':       time.time(),
                    'status':         'offen',
                    'guest_name':     None,
                }
            store[aid] = {'offer': None, 'answer': None}
            print(f"  Lobby: Angebot {aid} erstellt ({body.get('schwierigkeit','M')}) von {body.get('host_name','?')}")
            self.send_json(200, {'id': aid}); return

        # POST /lobby/join/ID  { guest_name }  →  atomar beitreten
        if p.startswith('/lobby/join/'):
            aid = p.split('/')[-1]
            with lobby_lock:
                ang = lobby.get(aid)
                if not ang:
                    self.send_json(404, {'error': 'Angebot nicht gefunden'}); return
                if ang['status'] != 'offen':
                    self.send_json(409, {'error': 'Dieses Duell wurde bereits angenommen'}); return
                # Atomar belegen
                ang['status']     = 'angenommen'
                ang['guest_name'] = body.get('guest_name', 'Gast')
            print(f"  Lobby: Angebot {aid} angenommen von {body.get('guest_name','?')}")
            self.send_json(200, {'ok': True, 'schwierigkeit': ang['schwierigkeit'],
                                 'host_name': ang['host_name']}); return

        # POST /lobby/cancel/ID  →  Angebot zurückziehen (Host oder Guest)
        if p.startswith('/lobby/cancel/'):
            aid = p.split('/')[-1]
            rolle = body.get('rolle', 'host')
            with lobby_lock:
                ang = lobby.get(aid)
                if not ang:
                    self.send_json(404, {'error': 'Nicht gefunden'}); return
                if rolle == 'guest' and ang['status'] == 'angenommen':
                    # Guest bricht ab → Angebot wieder öffnen
                    ang['status']     = 'offen'
                    ang['guest_name'] = None
                    print(f"  Lobby: Angebot {aid} wieder geöffnet (Guest abgebrochen)")
                else:
                    # Host zieht zurück → löschen
                    del lobby[aid]
                    if aid in store: del store[aid]
                    print(f"  Lobby: Angebot {aid} gelöscht")
            self.send_json(200, {'ok': True}); return

        # POST /lobby/offer/ID  { sdp }  →  WebRTC-Offer für Lobby-Angebot
        if p.startswith('/lobby/offer/'):
            aid = p.split('/')[-1]
            if aid not in store:
                self.send_json(404, {'error': 'Nicht gefunden'}); return
            store[aid]['offer'] = body.get('sdp', '')
            print(f"  Lobby {aid}: Offer hinterlegt")
            self.send_json(200, {'ok': True}); return

        # ── Warteraum CAS-Modell ──────────────────────────────
        # POST /warteraum/betreten  { name, liga }  →  { id }
        # state[i] = FREE, in Pool aufnehmen
        if p == '/warteraum/betreten':
            wid = ''.join(random.choices(string.digits, k=8))
            with warteraum_lock:
                warteraum[wid] = {
                    'id':              wid,
                    'name':            body.get('name', 'Spieler'),
                    'liga':            body.get('liga', 'bronze'),
                    'eingetreten':     time.time(),
                    'state':           'FREE',
                    'partner':         None,
                    'herausforderung': None,
                }
            print(f"  Warteraum: {body.get('name','?')} betreten (id={wid}, state=FREE)")
            self.send_json(200, {'id': wid}); return

        # POST /warteraum/verlassen  { id }  →  { ok }
        # state[i] = LEFT, aus Pool entfernen
        if p == '/warteraum/verlassen':
            wid = body.get('id')
            with warteraum_lock:
                if wid in warteraum:
                    warteraum[wid]['state'] = 'LEFT'
                    del warteraum[wid]
                    print(f"  Warteraum: {wid} verlassen (state=LEFT)")
            self.send_json(200, {'ok': True}); return

        # POST /warteraum/reservieren  { meine_id, gegner_id, host_name }
        # CAS-Kern: atomar entscheidet ob ich Host oder Guest bin
        # Ablauf laut Konzept:
        #   1. Wurde ich selbst bereits CLAIMED/PAIRED? → ich bin Guest
        #   2. CAS(gegner, FREE, CLAIMED) + CAS(ich, FREE, CLAIMED) → ich bin Host
        #   3. Sonst: 409 → Client fällt auf VG zurück
        if p == '/warteraum/reservieren':
            meine_id  = body.get('meine_id')
            gegner_id = body.get('gegner_id')
            host_name = body.get('host_name', 'Spieler')
            with warteraum_lock:
                # Schritt 1: Wurde ich bereits herausgefordert (CLAIMED)?
                if meine_id and meine_id in warteraum:
                    hf = warteraum[meine_id].get('herausforderung')
                    if hf:
                        cas(meine_id, 'CLAIMED', 'PAIRED')
                        print(f"  Reservieren: {meine_id} ist GUEST (bereits CLAIMED)")
                        self.send_json(200, {'rolle': 'guest', 'herausforderung': hf}); return

                # Schritt 2: Gegner verfügbar?
                if not gegner_id or gegner_id not in warteraum:
                    print(f"  Reservieren: {gegner_id} nicht im Warteraum")
                    self.send_json(409, {'error': 'Gegner nicht verfügbar'}); return

                # CAS: Gegner FREE → CLAIMED
                if not cas(gegner_id, 'FREE', 'CLAIMED'):
                    print(f"  Reservieren: {gegner_id} nicht FREE (state={warteraum[gegner_id]['state']})")
                    # Nochmal prüfen: wurde ich selbst inzwischen herausgefordert?
                    if meine_id and meine_id in warteraum:
                        hf = warteraum[meine_id].get('herausforderung')
                        if hf:
                            cas(meine_id, 'CLAIMED', 'PAIRED')
                            self.send_json(200, {'rolle': 'guest', 'herausforderung': hf}); return
                    self.send_json(409, {'error': 'Gegner nicht verfügbar'}); return

                # CAS: Ich FREE → CLAIMED
                if meine_id and meine_id in warteraum:
                    if not cas(meine_id, 'FREE', 'CLAIMED'):
                        # Rollback Gegner
                        cas(gegner_id, 'CLAIMED', 'FREE')
                        # Wurde ich selbst herausgefordert?
                        hf = warteraum[meine_id].get('herausforderung')
                        if hf:
                            cas(meine_id, 'CLAIMED', 'PAIRED')
                            self.send_json(200, {'rolle': 'guest', 'herausforderung': hf}); return
                        self.send_json(409, {'error': 'Eigener Zustand geändert'}); return

                # Beide CLAIMED → Herausforderung setzen, dann PAIRED
                warteraum[gegner_id]['herausforderung'] = {
                    'angebots_id':   None,  # wird per /update nachgeliefert
                    'schwierigkeit': 'M',
                    'host_name':     host_name
                }
                cas(gegner_id, 'CLAIMED', 'PAIRED')
                if meine_id and meine_id in warteraum:
                    cas(meine_id, 'CLAIMED', 'PAIRED')
                print(f"  Reservieren: {meine_id}=HOST vs {gegner_id}=GUEST (beide PAIRED)")
            self.send_json(200, {'rolle': 'host'}); return

        # POST /warteraum/herausforderung/update  { gegner_id, angebots_id, schwierigkeit }
        # Host liefert Angebots-ID nach /lobby/create nach
        if p == '/warteraum/herausforderung/update':
            gegner_id     = body.get('gegner_id')
            angebots_id   = body.get('angebots_id')
            schwierigkeit = body.get('schwierigkeit', 'M')
            with warteraum_lock:
                if gegner_id in warteraum and warteraum[gegner_id].get('herausforderung'):
                    warteraum[gegner_id]['herausforderung']['angebots_id']   = angebots_id
                    warteraum[gegner_id]['herausforderung']['schwierigkeit'] = schwierigkeit
                    print(f"  HF-Update: {gegner_id} → Angebot {angebots_id} ({schwierigkeit})")
            self.send_json(200, {'ok': True}); return

        self.send_json(404, {'error': 'Nicht gefunden'})

    def do_DELETE(self):
        p = urlparse(self.path).path
        if p.startswith('/lobby/'):
            aid = p.split('/')[-1]
            with lobby_lock:
                if aid in lobby: del lobby[aid]
                if aid in store: del store[aid]
            print(f"  Lobby: Angebot {aid} gelöscht (DELETE)")
            self.send_json(200, {'ok': True}); return
        self.send_json(404, {'error': 'Nicht gefunden'})

if __name__ == '__main__':
    import sys, os
    port = int(os.environ.get('PORT', 8080))
    if '--port' in sys.argv:
        try: port = int(sys.argv[sys.argv.index('--port') + 1])
        except: pass
    server = ThreadedHTTPServer(('0.0.0.0', port), Handler)
    print(f"Rendezvous-Server mit Lobby läuft auf http://0.0.0.0:{port}")
    print(f"PC:         http://localhost:{port}")
    print(f"Smartphone: http://<deine-IP>:{port}  (ipconfig → IPv4)")
    print("Strg+C zum Beenden\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer beendet.")
