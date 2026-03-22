# -*- coding: utf-8 -*-
import sqlite3
c = sqlite3.connect('geo.sqlite')
for stadt in ['Darmstadt', 'Frankfurt', 'Gießen', 'Rüsselsheim am Main', 'Limburg an der Lahn', 'Marburg', 'Kassel', 'Fulda', 'Wiesbaden']:
    r = c.execute(
        "SELECT DISTINCT k.id FROM stadt s "
        "JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name' "
        "JOIN kfz_kennzeichen k ON k.kreis_id=s.kreis_id "
        "WHERE t.value=? AND s.staat_id='DE'", (stadt,)).fetchall()
    print(f"{stadt:25s} → {[x[0] for x in r]}")
