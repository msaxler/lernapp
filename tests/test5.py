import zipfile,io 
z=zipfile.ZipFile('geonames_data/GV100.zip') 
fname=[n for n in z.namelist() if 'GV100' in n and n.endswith('.txt')][0] 
f=z.open(fname) 
lines=io.TextIOWrapper(f,encoding='utf-8',errors='replace').readlines() 
hits=[l for l in lines if l[0]=='4' and l[10:15] in ('08121','08221','08111')] 
[print(l[10:15],repr(l[22:60].strip())) for l in hits] 
