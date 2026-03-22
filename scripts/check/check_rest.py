# -*- coding: utf-8 -*-
import sqlite3, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
c = sqlite3.connect(os.path.join(BASE, 'data', 'geo.sqlite')).cursor()

rows = c.execute("""
    SELECT k.id, k.kreis_id, t.value
    FROM kfz_kennzeichen k
    LEFT JOIN translations t
        ON t.objekt_id=k.kreis_id AND t.pool='kreis'
        AND t.key='name' AND t.lang='de'
    WHERE k.id IN ('AA','WEN','ES','FN','GT','BB','HEI','HDH','HG',
                   'HGW','HX','HR','HOM','HD','GR','GM','GT','FÜS',
                   'EA','DLG','COE','BM','BIR','AW','AB','AN','BA',
                   'BT','HO','LA','P','PA','R','SW','TR','WÜ','A')
    AND k.staat_id='DE'
    ORDER BY k.id
""").fetchall()

print(f"{'KFZ':6s}  {'kreis_id':10s}  Kreisname")
print("-" * 55)
for kfz, kid, kname in rows:
    print(f"{kfz:6s}  {kid:10s}  {kname or '(leer)'}")
