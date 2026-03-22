import socket, ssl, urllib.request

print("=== Netzwerk-Diagnose ===")

# 1. Basis-Internet
try:
    urllib.request.urlopen("https://www.google.com", timeout=5)
    print("✅ Internet erreichbar (google.com)")
except Exception as e:
    print(f"❌ Internet nicht erreichbar: {e}")

# 2. DNS
for host in ["v6.db.transport.rest", "dbf.finalreboot.net", "bahn.de"]:
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS OK: {host} → {ip}")
    except Exception as e:
        print(f"❌ DNS fehlgeschlagen: {host} → {e}")

# 3. HTTPS
for url in ["https://bahn.de", "https://api.deutschebahn.com"]:
    try:
        r = urllib.request.urlopen(url, timeout=8)
        print(f"✅ HTTPS OK: {url} → {r.status}")
    except Exception as e:
        print(f"⚠️  {url} → {e}")



# TCP-Verbindungstest
for host, port in [("v6.db.transport.rest", 443), ("v6.db.transport.rest", 80)]:
    try:
        sock = socket.create_connection((host, port), timeout=8)
        print(f"✅ TCP OK: {host}:{port}")
        sock.close()
    except Exception as e:
        print(f"❌ TCP fehlgeschlagen: {host}:{port} → {e}")

# SSL-Test
try:
    ctx = ssl.create_default_context()
    conn = ctx.wrap_socket(
        socket.create_connection(("v6.db.transport.rest", 443), timeout=8),
        server_hostname="v6.db.transport.rest"
    )
    print(f"✅ SSL OK: {conn.version()}")
    conn.close()
except Exception as e:
    print(f"❌ SSL fehlgeschlagen: {e}")

# requests mit erhöhtem Timeout
try:
    import requests
    r = requests.get(
        "https://v6.db.transport.rest/stops/search",
        params={"query": "Berlin Hbf", "results": 1},
        timeout=30
    )
    print(f"✅ requests OK: Status {r.status_code}, {len(r.json())} Treffer")
except Exception as e:
    print(f"❌ requests fehlgeschlagen: {e}")
