import sqlite3 
c=sqlite3.connect('geo.sqlite') 
print(c.execute("SELECT t.value, k.id FROM stadt s JOIN translations t ON t.objekt_id=s.id AND t.lang='de' JOIN kfz_kennzeichen k ON k.kreis_id=s.kreis_id WHERE t.value IN ('Heidelberg','Heilbronn','Stuttgart','MÅnchen')").fetchall()) 
