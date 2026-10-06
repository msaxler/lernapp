"""QuizAway Grundversorgung, Teil VG250 (Mike 2026-10-07): Nachbarn, Küste, Regionalsprachen-Namen, amtliche Beinamen.

Quelle: Bundesamt für Kartographie und Geodäsie, Verwaltungsgebiete 1:250 000 (VG250), Stand 31.12.2024,
geonames_data/vg250_12-31.utm32s.gpkg.ebenen/vg250_ebenen_1231/DE_VG250.gpkg (GeoPackage, UTM 32).
  - Nachbarn: Gemeindeflächen (GF 4, Land) mit gemeinsamer Grenze
  - Küste: Gemeinde berührt eine Grenzlinie mit Merkmal „an Küste“ (GMK 9); Nordsee oder Ostsee nach Lage
  - Regionalsprache: Tabelle vgtb_rgs_vg (Dänisch, Nord-/Saterfriesisch, Nieder-/Obersorbisch, Niederdeutsch)
  - Beiname: amtliche Zusatzbezeichnung, Tabelle vgtb_azb_vg (Hansestadt, Ostseebad, Münchhausenstadt …)
Schreibt data/grundversorgung/vg250-auszug.json: {ags: {"n": [ags…], "k": "N"|"O", "rgs": [name, sprache], "azb": "…"}}.

Aufruf:  python -X utf8 scripts/data-build/quizaway_vg250.py
"""
import io
import json
import os
import sqlite3
import struct
import sys
import time

from shapely import wkb
from shapely.strtree import STRtree

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GPKG = os.path.join(WURZEL, 'geonames_data', 'vg250_12-31.utm32s.gpkg.ebenen', 'vg250_ebenen_1231', 'DE_VG250.gpkg')
ZIEL = os.path.join(WURZEL, 'data', 'grundversorgung', 'vg250-auszug.json')
SPRACHE = {'dan': 'Dänisch', 'dsb': 'Niedersorbisch', 'frr': 'Nordfriesisch', 'hsb': 'Obersorbisch', 'nds': 'Niederdeutsch',
           'stq': 'Saterfriesisch'}


def geom(blob):
    """GeoPackage-Geometrie: 8 Byte Kopf, Hüllrechteck je nach Flag, dann WKB."""
    flags = blob[3]
    env = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 7]
    return wkb.loads(bytes(blob[8 + env:]))


def meer(x, y, land):
    """Nordsee oder Ostsee nach Land und Lage (UTM 32: x Ost, y Nord in Metern)."""
    if land in ('03', '04', '02'):
        return 'N'
    if land == '13':
        return 'O'
    # Schleswig-Holstein: Westküste Nordsee, Ostküste und Flensburger Förde Ostsee
    return 'N' if x < 515000 else 'O'   # Husum 9,05° Ost (x ≈ 503 km) Nordsee, Flensburg 9,43° (x ≈ 527 km) Ostsee


def main():
    t0 = time.time()
    db = sqlite3.connect(GPKG)
    gem = [(ags, geom(g)) for ags, g in db.execute("select AGS, geom from vg250_gem where GF = 4")]
    print('%d Gemeindeflächen (%.0f s)' % (len(gem), time.time() - t0))
    baum = STRtree([g for _, g in gem])
    nachbarn = {}
    for i, (ags, g) in enumerate(gem):
        for j in baum.query(g, predicate='intersects'):
            if j != i and gem[j][0] != ags:
                nachbarn.setdefault(ags, set()).add(gem[j][0])
    print('Nachbarn: %d Paare (%.0f s)' % (sum(len(v) for v in nachbarn.values()) // 2, time.time() - t0))
    kueste = [geom(g) for (g,) in db.execute("select geom from vg250_li where GMK = 9")]
    kbaum = STRtree(kueste)
    an_kueste = {}
    for ags, g in gem:
        treffer = kbaum.query(g, predicate='intersects')
        # nur Küstenländer (das VG250 führt auch das Bodenseeufer als Küste) und nicht die Elbe oberhalb der Mündung
        # (Glückstadt, Drochtersen; Prüfung 2026-10-07): östlich von x 490 km und südlich von y 5975 km
        if len(treffer) and ags[:2] in ('01', '02', '03', '04', '13'):
            c = g.centroid
            if not (c.x > 490000 and c.y < 5975000 and ags[:2] in ('01', '02', '03')):
                an_kueste[ags] = meer(c.x, c.y, ags[:2])
    print('Küste: %d Gemeinden (%.0f s)' % (len(an_kueste), time.time() - t0))
    rgs = {}
    for ars, name, spr in db.execute("select ARS, RGS, SPR from vgtb_rgs_vg where ADE = 6"):
        rgs[ars[:5] + ars[-3:]] = [name, SPRACHE.get(spr, spr)]
    azb = {ars[:5] + ars[-3:]: z for ars, z in db.execute("select ARS, AZB from vgtb_azb_vg where ADE = 6")}
    aus = {}
    for ags in set(nachbarn) | set(an_kueste) | set(rgs) | set(azb):
        e = {}
        if ags in nachbarn:
            e['n'] = sorted(nachbarn[ags])
        if ags in an_kueste:
            e['k'] = an_kueste[ags]
        if ags in rgs:
            e['rgs'] = rgs[ags]
        if ags in azb:
            e['azb'] = azb[ags]
        aus[ags] = e
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    with io.open(ZIEL, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'_doc': 'aus VG250 (BKG, 31.12.2024), scripts/data-build/quizaway_vg250.py', 'gemeinden': aus}, f,
                  ensure_ascii=False, separators=(',', ':'))
    print('Regionalsprache: %d, Beiname: %d; geschrieben %s (%.0f s)' % (len(rgs), len(azb), ZIEL, time.time() - t0))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
