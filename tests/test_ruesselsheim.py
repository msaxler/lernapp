# -*- coding: utf-8 -*-
import sqlite3
c = sqlite3.connect('geo.sqlite')
r = c.execute(
    "SELECT s.id, s.kreis_id, t.value FROM stadt s "
    "JOIN translations t ON t.objekt_id=s.id AND t.lang='de' AND t.key='name' "
    "WHERE t.value LIKE 'Rüssels%'"
).fetchall()
print("Rüsselsheim LIKE:", r)

# Auch englischen Namen prüfen
r2 = c.execute(
    "SELECT s.id, s.kreis_id FROM stadt s "
    "JOIN translations t ON t.objekt_id=s.id AND t.key='name' "
    "WHERE t.value LIKE 'R_sselsheim%' LIMIT 5"
).fetchall()
print("Alle Sprachen:", r2)
