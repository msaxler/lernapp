"""
Rendezvous-Server mit Lobby/Matchmaking
Startet mit: python rendezvous.py
Port 8080 — liefert HTML, SQLite, WebRTC-Signaling und Duell-Lobby
"""
import json, random, string, os, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from socketserver import ThreadingMixIn

# ─── WebRTC-Signaling Store ──────────────────────────────────
store = {}  # pin -> {'offer': sdp, 'answer': sdp}

def new_pin():
    while True:
        pin = ''.join(random.choices(string.digits, k=6))
        if pin not in store and pin not in lobby:
            return pin

# ─── Lobby Store ─────────────────────────────────────────────
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
                self.send_json(404, {'offer': None, 'error': 'Kein Offer'}); return
            self.send_json(200, {'offer': offer}); return

        self.send_json(404, {'error': 'Nicht gefunden'})

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
