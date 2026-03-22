# -*- coding: utf-8 -*-
import sqlite3
c = sqlite3.connect('geo.sqlite')

for name in ['Muelheim an der Ruhr', 'Oldenburg (Oldenburg)', 'Mülheim an der Ruhr', 'Oldenburg']:
    r = c.execute(
        "SELECT s.id, s.kreis_id, s.einwohner, t.value FROM stadt s "
        "JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name' "
        "WHERE t.value=?", (name,)).fetchall()
    if r:
        print(f"{name}: {r}")
        # KFZ prüfen
        for row in r:
            if row[1]:
                kfz = c.execute("SELECT id FROM kfz_kennzeichen WHERE kreis_id=?", (row[1],)).fetchall()
                print(f"  → KFZ: {[x[0] for x in kfz]}")
