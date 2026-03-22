import zipfile,io 
z=zipfile.ZipFile('geonames_data/GV100.zip') 
fname=[n for n in z.namelist() if 'GV100' in n and n.endswith('.txt')][0] 
f=z.open(fname) 
lines=io.TextIOWrapper(f,encoding='utf-8',errors='replace').readlines() 
muenchen=[l for l in lines if l[0]=='6' and 'nchen' in l] 
[print(repr(l[:100])) for l in muenchen[:3]] 
