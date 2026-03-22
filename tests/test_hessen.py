# -*- coding: utf-8 -*-
import zipfile, io

with zipfile.ZipFile('geonames_data/GV100.zip') as zf:
    fname = next(n for n in zf.namelist() if n.endswith('.txt'))
    with zf.open(fname) as f:
        for line in io.TextIOWrapper(f, encoding='utf-8', errors='replace'):
            if len(line) < 25 or line[0] != '4': continue
            ags = line[10:15].strip()
            name = line[22:60].strip()
            if ags.startswith('06'):
                print(f"{ags}  {name}")
