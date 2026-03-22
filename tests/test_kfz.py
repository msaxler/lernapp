# -*- coding: utf-8 -*-
import sqlite3
c = sqlite3.connect('geo.sqlite')
staedte = ['Heidelberg', 'Heilbronn', 'Stuttgart', 'München', 'Karlsruhe', 
           'Freiburg im Breisgau', 'Tübingen', 'Konstanz', 'Rottweil', 'Tuttlingen']
for s in staedte:
    r = c.execute(
        "SELECT DISTINCT k.id FROM stadt st "
        "JOIN translations t ON t.objekt_id=st.id AND t.lang='de' AND t.key='name' "
        "JOIN kfz_kennzeichen k ON k.kreis_id=st.kreis_id "
        "WHERE t.value=?", (s,)).fetchall()
    kfz = [x[0] for x in r]
    if not kfz:
        # Diagnose: kreis_id prüfen
        d = c.execute(
            "SELECT st.id, t.value, st.kreis_id, st.einwohner FROM stadt st "
            "JOIN translations t ON t.objekt_id=st.id AND t.lang='de' AND t.key='name' "
            "WHERE t.value LIKE ?", (s[:8]+'%',)).fetchall()
        print(f"{s:30s} → KEIN KFZ  Diagnose: {d[:3]}")
    else:
        print(f"{s:30s} → {kfz}")
