import sqlite3

conn = sqlite3.connect('data/geo.sqlite')
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tabellen:', cur.fetchall())

cur.execute("SELECT * FROM staedte WHERE name LIKE '%Mainz%'")
rows = cur.fetchall()
print('Mainz-Eintraege:', rows)

# Auch Spaltennamen anzeigen
cur.execute("PRAGMA table_info(staedte)")
print('Spalten:', cur.fetchall())

conn.close()
