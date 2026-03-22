import sqlite3 
c=sqlite3.connect('geo.sqlite') 
r=c.execute("SELECT id,kreis_id FROM stadt WHERE einwohner>1000000").fetchall() 
print(r) 
