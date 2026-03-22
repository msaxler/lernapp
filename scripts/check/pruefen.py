# -*- coding: utf-8 -*-
import sqlite3, csv, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
conn = sqlite3.connect(os.path.join(BASE, 'data', 'geo.sqlite'))
c    = conn.cursor()

ref = {}
with open(os.path.join(BASE, 'data', 'kfz_kennzeichen.csv'), encoding='utf-8') as f:
    for row in csv.DictReader(f):
        ref[row['kfz'].strip()] = row['stadt'].strip()

def norm(s):
    return (s.upper()
            .replace('Ä','AE').replace('Ö','OE').replace('Ü','UE')
            .replace('ß','SS').replace('-',' ').replace(',',' ').strip())

falsch = []
for kfz_id, kreis_id, kreisname in c.execute("""
    SELECT k.id, k.kreis_id, t.value
    FROM kfz_kennzeichen k
    LEFT JOIN translations t ON t.objekt_id=k.kreis_id AND t.pool='kreis'
        AND t.key='name' AND t.lang='de'
    WHERE k.staat_id='DE' ORDER BY k.id
""").fetchall():
    if kfz_id not in ref:
        continue
    ref_stadt = ref[kfz_id]
    if norm(ref_stadt) not in norm(kreisname or ''):
        falsch.append((kfz_id, kreis_id, kreisname or '', ref_stadt))

print(f"Falsch zugeordnet: {len(falsch)}\n")
print(f"{'KFZ':6s}  {'kreis_id':10s}  {'Kreis in DB':35s}  Ref-Stadt CSV")
print('-' * 80)
for kfz, kid, kname, ref_s in falsch:
    print(f"{kfz:6s}  {kid:10s}  {kname:35s}  {ref_s}")

conn.close()
