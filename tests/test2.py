import sqlite3,zipfile,io 
z=zipfile.ZipFile('geonames_data/DE.zip') 
f=z.open('DE.txt') 
lines=[l for l in io.TextIOWrapper(f,encoding='utf-8') if l.split('\t')[0]=='2867714'] 
parts=lines[0].split('\t') 
print('admin1=',parts[10],'admin2=',parts[11]) 
