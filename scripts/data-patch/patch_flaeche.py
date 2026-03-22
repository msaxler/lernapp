"""
patch_flaeche.py — Trägt fehlende Flächen manuell nach
=======================================================
Für Städte die fetch_flaeche.py nicht gefunden hat.
Aufruf: python patch_flaeche.py
"""
import json, shutil

STAEDTE_F = 'staedte.json'

# Flächen in km² (Quelle: Wikipedia / Destatis)
KORREKTUREN = {
    'Freiburg':                                153.1,  # Freiburg im Breisgau
    'Marburg an der Lahn':                     123.5,
    'Dessau':                                  244.9,  # Dessau-Roßlau
    'Aalen':                                   146.4,
    'Universitäts- und Hansestadt Greifswald':  37.9,
    'Singen':                                   62.0,  # Singen (Hohentwiel)
    'Hennef (Sieg)':                           110.7,
    'Weiden':                                   40.7,  # Weiden in der Oberpfalz
    'Mühlhausen':                              136.3,  # Mühlhausen/Thüringen
    'Schwedt (Oder)':                          284.0,
    'Idar-Oberstein':                          180.5,
    'Neustrelitz':                             167.2,
    'Weißwasser':                               97.6,
    'Luckenwalde':                              49.9,
    'Guben':                                    67.0,
    'Prenzlau':                                194.0,
    'Giengen an der Brenz':                     54.7,
    # Runde 2
    'Wittenberg':                                219.0,
    'Saalfeld':                                   83.6,
    'Verden':                                     83.8,
    'Strausberg':                                 74.8,
    'Garmisch-Partenkirchen':                    201.7,
    'Weilheim':                                   47.2,
}

with open(STAEDTE_F, encoding='utf-8') as f:
    staedte = json.load(f)

shutil.copy2(STAEDTE_F, STAEDTE_F.replace('.json', '_backup_patch.json'))

gesetzt = []
for s in staedte:
    if s['name'] in KORREKTUREN and not s.get('flaeche'):
        s['flaeche'] = KORREKTUREN[s['name']]
        gesetzt.append(f"  ✅  {s['name']}: {s['flaeche']} km²")

for g in gesetzt:
    print(g)

noch_leer = [s['name'] for s in staedte if not s.get('flaeche')]
if noch_leer:
    print(f'\n⚠️  Noch ohne Fläche: {", ".join(noch_leer)}')
else:
    print(f'\n✅  Alle {len(staedte)} Städte haben Fläche')

with open(STAEDTE_F, 'w', encoding='utf-8') as f:
    json.dump(staedte, f, ensure_ascii=False, indent=2)

print(f'\n✅  staedte.json aktualisiert ({len(gesetzt)} Flächen ergänzt)')
print('Nächste Schritte:\n  python generate_questions.py\n  python inject_questions.py')
