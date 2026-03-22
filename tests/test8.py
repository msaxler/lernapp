import zipfile,io 
z=zipfile.ZipFile('geonames_data/GV100.zip') 
fname=[n for n in z.namelist() if 'GV100' in n and n.endswith('.txt')][0] 
f=z.open(fname) 
ags_map={} 
lines=io.TextIOWrapper(f,encoding='utf-8',errors='replace').readlines() 
[ags_map.update({l[22:72].strip().split(',')[0].strip().lower():l[10:15].strip()}) for l in lines if len(l) and l[0]=='4'] 
print('freiburg im breisgau in map:','freiburg im breisgau' in ags_map) 
treffer=[(k,v) for k,v in ags_map.items() if k.startswith('freiburg ')] 
print('Treffer freiburg*:',treffer) 
