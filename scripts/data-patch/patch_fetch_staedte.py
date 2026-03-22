#!/usr/bin/env python3
"""Fügt 'ars'-Feld in fetch_staedte.py ein. Aufruf: py -3.11 patch_fetch_staedte.py"""
import os, sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fetch_staedte.py')
src = open(path, encoding='utf-8').read()

old = "            'fluesse':    a.get('fluesse',[]),"
new = "            'ars':        d['ars'],\n            'fluesse':    a.get('fluesse',[]),"

if old not in src:
    print("FEHLER: Zielzeile nicht gefunden!")
    sys.exit(1)

if "'ars':        d['ars']" in src:
    print("'ars' bereits korrekt eingetragen.")
    sys.exit(0)

open(path, 'w', encoding='utf-8').write(src.replace(old, new, 1))
print("✅ Gepatcht. Jetzt ausführen:")
print("   py -3.11 fetch_staedte.py")
print("   py -3.11 fetch_kfz.py")
