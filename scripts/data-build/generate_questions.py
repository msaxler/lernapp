"""
Quiz Away — Fragen-Generator
============================
Liest staedte.json und erzeugt fragen.json im Format des Prototyps.

Kategorien (Phase 1):
  geo   — Bundesland, Flüsse
  kfz   — KFZ-Kennzeichen
  ew    — Einwohner-Vergleich, Bevölkerungsdichte
  dist  — Distanz, Himmelsrichtung

Aufruf:
  python generate_questions.py
  python generate_questions.py --staedte staedte.json --out fragen.json
"""

import json, math, random, argparse
from itertools import combinations

# ── Argumente ──────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--staedte", default="staedte.json")
parser.add_argument("--out",     default="fragen.json")
args = parser.parse_args()

# ── Städte laden ───────────────────────────────────────────────────────────
with open(args.staedte, encoding="utf-8") as f:
    STAEDTE = json.load(f)

# Schnellzugriff nach Name
S = {s["name"]: s for s in STAEDTE}

# ── Schwierigkeits-Pools ───────────────────────────────────────────────
EW_GRENZE_L = 35_000   # ~350 Städte → Leicht
EW_GRENZE_M = 25_000   # ~521 Städte → Mittel

POOL_L = [s for s in STAEDTE if s["einwohner"] >= EW_GRENZE_L]
POOL_M = [s for s in STAEDTE if s["einwohner"] >= EW_GRENZE_M]
POOL_S = STAEDTE

def sw_stufe(stadt):
    ew = stadt["einwohner"]
    if ew >= EW_GRENZE_L: return "L"
    if ew >= EW_GRENZE_M: return "M"
    return "S"

def pool_fuer(stadt):
    sw = sw_stufe(stadt)
    if sw == "L": return POOL_L
    if sw == "M": return POOL_M
    return POOL_S

fragen = []

def fid():
    """Eindeutige fortlaufende ID"""
    fid._n += 1
    return f"q{fid._n:04d}"
fid._n = 0

# ── Hilfsfunktionen ────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    """Luftlinien-Distanz in km (Haversine-Formel)"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def bearing(lat1, lon1, lat2, lon2):
    """Kompassrichtung von Punkt 1 zu Punkt 2 in Grad"""
    dlon = math.radians(lon2 - lon1)
    x = math.sin(dlon) * math.cos(math.radians(lat2))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
        math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(dlon)
    return (math.degrees(math.atan2(x, y)) + 360) % 360

def himmelsrichtung(deg):
    """Grad → Himmelsrichtung (8 Richtungen)"""
    richtungen = ["Norden","Nordosten","Osten","Südosten","Süden","Südwesten","Westen","Nordwesten"]
    return richtungen[round(deg / 45) % 8]

def andere_staedte(ausschluss_namen, n=3, pool=None):
    """n zufällige Städte, nicht in ausschluss_namen, aus gegebenem Pool"""
    if pool is None: pool = STAEDTE
    kandidaten = [s for s in pool if s["name"] not in ausschluss_namen]
    return random.sample(kandidaten, min(n, len(kandidaten)))

def runde_distanz(km):
    """Distanz auf sinnvolle Stufen runden für Antwortoptionen"""
    if km < 100:  return round(km / 10) * 10
    if km < 500:  return round(km / 50) * 50
    return round(km / 100) * 100

def distanz_optionen(richtig_km):
    """3 falsche Distanz-Optionen, die nicht zu nah an der richtigen liegen"""
    r = runde_distanz(richtig_km)
    offsets = [
        int(r * 0.4), int(r * 1.7), int(r * 2.8),
        int(r * 0.6), int(r * 2.2), int(r * 0.25),
    ]
    optionen = []
    for o in offsets:
        o = max(50, round(o / 50) * 50)
        if abs(o - r) > 60 and o not in optionen and o != r:
            optionen.append(o)
        if len(optionen) == 3:
            break
    while len(optionen) < 3:
        candidate = random.choice([50, 100, 200, 300, 400, 600, 800, 1000])
        if abs(candidate - r) > 60 and candidate not in optionen:
            optionen.append(candidate)
    return [f"ca. {o} km" for o in optionen]


# ══════════════════════════════════════════════════════════════════════════
# KATEGORIE: geo — Bundesland & Flüsse
# ══════════════════════════════════════════════════════════════════════════

# Alle Bundesländer
alle_bl = list({s["bundesland"] for s in STAEDTE})

for stadt in STAEDTE:
    # Frage: In welchem Bundesland liegt X?
    richtig_bl = stadt["bundesland"]
    falsch_bl  = random.sample([b for b in alle_bl if b != richtig_bl], 3)
    fragen.append({
        "id": fid(),
        "kat": "geo",
        "kat": "geo",
        "sw":     sw_stufe(stadt),
        "stadt": stadt["name"],
        "bl": richtig_bl,
        "frage": f"In welchem Bundesland liegt {stadt['name']}?",
        "richtig": richtig_bl,
        "falsch": falsch_bl,
        "erkl": f"{stadt['name']} liegt in {richtig_bl}."
    })

    # Frage: An welchem Fluss liegt X? (nur wenn Flüsse vorhanden)
    if stadt["fluesse"]:
        richtig_fluss = stadt["fluesse"][0]
        alle_fluesse = ["Rhein","Elbe","Donau","Main","Weser","Oder","Neckar",
                        "Mosel","Saale","Spree","Lech","Inn","Isar","Ems","Werra"]
        falsch_fluesse = random.sample([f for f in alle_fluesse if f != richtig_fluss], 3)
        fragen.append({
            "id": fid(),
            "kat": "geo",
            "kat": "geo",
        "sw":     sw_stufe(stadt),
            "stadt": stadt["name"],
            "bl": richtig_bl,
            "frage": f"An welchem Fluss liegt {stadt['name']}?",
            "richtig": richtig_fluss,
            "falsch": falsch_fluesse,
            "erkl": f"{stadt['name']} liegt am {richtig_fluss}."
        })


# ── Geo Typ 3: 5 Städte — in welchem Bundesland liegt die Mehrheit? ────────
random.shuffle(STAEDTE)
for i in range(0, len(STAEDTE) - 4, 3):
    gruppe = STAEDTE[i:i+5]
    if len(gruppe) < 5:
        continue
    # Zähle Bundesländer
    from collections import Counter
    bl_count = Counter(s["bundesland"] for s in gruppe)
    mehrheit_bl, mehrheit_n = bl_count.most_common(1)[0]
    if mehrheit_n < 2:
        continue  # keine klare Mehrheit — überspringen
    # Falsche Optionen: andere Bundesländer die nicht in der Gruppe sind
    alle_bl_lokal = list({s["bundesland"] for s in STAEDTE})
    falsch_bl = random.sample([b for b in alle_bl_lokal if b != mehrheit_bl], 3)
    namen = ", ".join(s["name"] for s in gruppe)
    fragen.append({
        "id": fid(),
        "kat": "geo",
        "kat": "geo",
        "sw":     sw_stufe(stadt),
        "stadt": gruppe[0]["name"],
        "bl": mehrheit_bl,
        "frage": f"In welchem Bundesland liegt die Mehrheit dieser Städte? {namen}",
        "richtig": mehrheit_bl,
        "falsch": falsch_bl,
        "erkl": (f"{mehrheit_n} der 5 Städte liegen in {mehrheit_bl}.")
    })

# ══════════════════════════════════════════════════════════════════════════

# KFZ-Kennzeichen → Zulassungsbereich (Kreisstadt)
# Wird genutzt wenn Stadt ≠ Zulassungsbereich-Name
KFZ_KREISSTADT = {
    "AC": "Aachen", "ABI": "Anhalt-Bitterfeld", "ABG": "Altenburger Land",
    "AIC": "Aichach-Friedberg", "AK": "Altenkirchen", "AM": "Amberg",
    "AN": "Ansbach", "AÖ": "Altötting", "AP": "Weimarer Land",
    "AS": "Amberg-Sulzbach", "AU": "Augsburg", "AUR": "Aurich",
    "AW": "Ahrweiler", "AZE": "Anhalt-Zerbst",
    "BA": "Bamberg", "BAD": "Baden-Baden", "BAR": "Barnim",
    "BB": "Böblingen", "BBL": "Dahme-Spreewald",
    "BCH": "Buchen (Odenwald)", "BGL": "Berchtesgadener Land",
    "BGD": "Berchtesgadener Land", "BI": "Bielefeld",
    "BIR": "Birkenfeld", "BIT": "Bitburg-Prüm", "BKS": "Birkenfeld",
    "BL": "Zollernalbkreis", "BLK": "Burgenlandkreis",
    "BM": "Rhein-Erft-Kreis", "BN": "Bonn", "BO": "Bochum",
    "BOG": "Bogen", "BOR": "Borken", "BRA": "Wesermarsch",
    "BSK": "Spree-Neiße", "BT": "Bayreuth", "BÜS": "Büsingen",
    "BW": "Baden-Württemberg",
    "CB": "Cottbus", "CE": "Celle", "CHA": "Cham",
    "COC": "Cochem-Zell", "COE": "Coesfeld", "CUX": "Cuxhaven",
    "CW": "Calw",
    "D": "Düsseldorf", "DA": "Darmstadt", "DAH": "Dachau",
    "DAN": "Lüchow-Dannenberg", "DAU": "Daun", "DE": "Dessau-Roßlau",
    "DEG": "Deggendorf", "DEL": "Delmenhorst", "DGF": "Dingolfing-Landau",
    "DH": "Diepholz", "DIL": "Dillkreis", "DI": "Dithmarschen",
    "DLG": "Dillingen a.d. Donau", "DO": "Dortmund",
    "DU": "Duisburg", "DÜW": "Bad Dürkheim", "DW": "Döbeln", "DZ": "Döbeln",
    "E": "Essen", "EA": "Eisenach", "EBE": "Ebersberg",
    "EI": "Eichstätt", "EIC": "Eichsfeld", "EL": "Emsland",
    "EM": "Emmendingen", "EMD": "Emden", "EN": "Ennepe-Ruhr-Kreis",
    "ERB": "Erbach", "ERH": "Erlangen-Höchstadt",
    "ERZ": "Erzgebirgskreis", "ESW": "Eschwege", "EU": "Euskirchen",
    "EWE": "Oldenburg",
    "F": "Frankfurt am Main", "FB": "Wetteraukreis",
    "FDS": "Freudenstadt", "FF": "Frankfurt (Oder)", "FFB": "Fürstenfeldbruck",
    "FN": "Bodenseekreis", "FO": "Forchheim", "FR": "Freiburg im Breisgau",
    "FRG": "Freyung-Grafenau", "FRI": "Friesland", "FT": "Frankenthal",
    "FÜS": "Füssen",
    "GAP": "Garmisch-Partenkirchen", "GE": "Gelsenkirchen",
    "GER": "Germersheim", "GG": "Groß-Gerau", "GI": "Gießen",
    "GL": "Rheinisch-Bergischer Kreis", "GM": "Oberbergischer Kreis",
    "GÖ": "Göttingen", "GP": "Göppingen", "GR": "Görlitz",
    "GRZ": "Greiz", "GT": "Gütersloh", "GTH": "Gotha", "GZ": "Günzburg",
    "H": "Hannover", "HA": "Hagen", "HAL": "Halle (Saale)",
    "HAM": "Hamm", "HAS": "Haßberge", "HB": "Bremen",
    "HD": "Heidelberg", "HDH": "Heidenheim", "HE": "Helmstedt",
    "HEF": "Hersfeld-Rotenburg", "HEI": "Dithmarschen",
    "HER": "Herne", "HF": "Herford", "HGW": "Greifswald",
    "HH": "Hamburg", "HI": "Hildesheim", "HK": "Holzminden",
    "HL": "Lübeck", "HM": "Hameln-Pyrmont", "HOL": "Holzminden",
    "HOM": "Homburg", "HVL": "Havelland", "HX": "Höxter",
    "HZ": "Harz",
    "IK": "Ilm-Kreis", "IN": "Ingolstadt", "IZ": "Steinburg",
    "J": "Jena", "JL": "Jerichower Land",
    "K": "Köln", "KA": "Karlsruhe", "KB": "Waldeck-Frankenberg",
    "KC": "Kronach", "KE": "Kempten", "KEH": "Kelheim",
    "KG": "Bad Kissingen", "KH": "Bad Kreuznach",
    "KIB": "Donnersbergkreis", "KL": "Kaiserslautern",
    "KLE": "Kleve", "KN": "Konstanz", "KO": "Koblenz",
    "KS": "Kassel", "KT": "Kitzingen", "KU": "Kulmbach",
    "KUN": "Künzelsau", "KÜN": "Hohenlohekreis", "KUS": "Kusel",
    "KYF": "Kyffhäuserkreis",
    "L": "Leipzig", "LA": "Landshut", "LAU": "Nürnberger Land",
    "LB": "Ludwigsburg", "LD": "Landau in der Pfalz",
    "LDS": "Dahme-Spreewald", "LEV": "Leverkusen", "LER": "Leer",
    "LG": "Lüneburg", "LI": "Lindau (Bodensee)", "LIF": "Lichtenfels",
    "LIP": "Lippe", "LL": "Landsberg am Lech", "LM": "Limburg-Weilburg",
    "LÖ": "Lörrach", "LOS": "Oder-Spree", "LRO": "Rostock",
    "LU": "Ludwigshafen am Rhein", "LUP": "Ludwigslust-Parchim",
    "M": "München", "MB": "Miesbach", "MD": "Magdeburg",
    "ME": "Mettmann", "MEI": "Meißen", "MG": "Mönchengladbach",
    "MH": "Mülheim an der Ruhr", "MI": "Minden-Lübbecke",
    "MIL": "Miltenberg", "MK": "Märkisches Sauerland",
    "MKK": "Main-Kinzig-Kreis", "MM": "Memmingen",
    "MN": "Unterallgäu", "MOL": "Märkisch-Oderland",
    "MOS": "Mosbach", "MR": "Marburg-Biedenkopf",
    "MSE": "Mecklenburgische Seenplatte", "MSH": "Mansfeld-Südharz",
    "MSP": "Main-Spessart", "MÜ": "Mühldorf am Inn",
    "MYK": "Mayen-Koblenz", "MZG": "Merzig-Wadern",
    "N": "Nürnberg", "NB": "Neubrandenburg",
    "ND": "Neuburg-Schrobenhausen", "NDH": "Nordhausen",
    "NE": "Rhein-Kreis Neuss", "NES": "Rhön-Grabfeld",
    "NEW": "Neustadt a.d. Waldnaab", "NF": "Nordfriesland",
    "NI": "Nienburg/Weser", "NK": "Neunkirchen",
    "NM": "Neumarkt i.d.OPf.", "NMS": "Neumünster",
    "NOH": "Grafschaft Bentheim", "NOM": "Northeim",
    "NÖ": "Neuburg-Schrobenhausen", "NR": "Neuwied",
    "NU": "Neu-Ulm", "NWM": "Nordwestmecklenburg", "NW": "Neustadt an der Weinstraße",
    "OA": "Oberallgäu", "OAL": "Ostallgäu", "OB": "Oberhausen",
    "OD": "Stormarn", "OE": "Olpe", "OF": "Offenbach",
    "OG": "Ortenaukreis", "OH": "Ostholstein", "OHA": "Osterode am Harz",
    "OHZ": "Osterholz", "OL": "Oldenburg", "OPR": "Ostprignitz-Ruppin",
    "OS": "Osnabrück", "OSL": "Oberspreewald-Lausitz",
    "P": "Potsdam", "PA": "Passau", "PAF": "Pfaffenhofen a.d. Ilm",
    "PAN": "Rottal-Inn", "PB": "Paderborn", "PI": "Pinneberg",
    "PIR": "Pirna", "PLÖ": "Plön", "PM": "Potsdam-Mittelmark",
    "PR": "Prignitz", "PS": "Pirmasens",
    "R": "Regensburg", "RA": "Rastatt", "RD": "Rendsburg-Eckernförde",
    "RE": "Recklinghausen", "REG": "Regen", "RÜD": "Rheingau-Taunus-Kreis",
    "RO": "Rosenheim", "ROW": "Rotenburg (Wümme)",
    "RP": "Rhein-Pfalz-Kreis", "RS": "Remscheid",
    "RT": "Reutlingen", "RU": "Saale-Orla-Kreis", "RV": "Ravensburg",
    "RW": "Rottweil", "RZ": "Herzogtum Lauenburg",
    "S": "Stuttgart", "SA": "Salzlandkreis", "SAD": "Schwandorf",
    "SAW": "Altmarkkreis Salzwedel", "SB": "Saarbrücken",
    "SC": "Schwabach", "SDL": "Stendal", "SE": "Segeberg",
    "SG": "Solingen", "SHA": "Schwäbisch Hall", "SHK": "Saale-Holzland-Kreis",
    "SI": "Siegen-Wittgenstein", "SIG": "Sigmaringen",
    "SK": "Saalkreis", "SL": "Schleswig-Flensburg",
    "SLK": "Salzlandkreis", "SLS": "Saarlouis",
    "SN": "Schwerin", "SO": "Soest", "SOK": "Saale-Orla-Kreis",
    "SÖM": "Sömmerda", "SON": "Sonneberg", "SPN": "Spree-Neiße",
    "SR": "Straubing-Bogen", "ST": "Steinfurt",
    "STA": "Starnberg", "STD": "Stade", "SU": "Siegburg",
    "SÜW": "Südliche Weinstraße", "SW": "Schweinfurt",
    "TBB": "Main-Tauber-Kreis", "TF": "Teltow-Fläming",
    "TIR": "Tirschenreuth", "TÖL": "Bad Tölz-Wolfratshausen",
    "TÜ": "Tübingen", "TUT": "Tuttlingen",
    "UE": "Uelzen", "UH": "Unstrut-Hainich-Kreis",
    "UM": "Uckermark", "UN": "Unna",
    "VB": "Vogelsbergkreis", "VEC": "Vechta", "VER": "Verden",
    "VG": "Vorpommern-Greifswald", "VIE": "Viersen",
    "VR": "Vorpommern-Rügen",
    "W": "Wuppertal", "WAF": "Warendorf", "WAK": "Wartburgkreis",
    "WB": "Wittenberg", "WES": "Wesel", "WF": "Wolfenbüttel",
    "WHV": "Wilhelmshaven", "WI": "Wiesbaden",
    "WIZ": "Witzenhausen", "WL": "Harburg", "WM": "Weilheim-Schongau",
    "WND": "St. Wendel", "WN": "Waiblingen", "WOB": "Wolfsburg",
    "WST": "Ammerland", "WT": "Waldshut", "WTM": "Wittmund",
    "WUG": "Weißenburg-Gunzenhausen", "WUN": "Wunsiedel i. Fichtelgebirge",
    "WÜ": "Würzburg",
    "Z": "Zwickau", "ZW": "Zweibrücken",
}


def _kfz_erkl(kfz, stadtname, bundesland):
    """Erklärung für 'Welches Kennzeichen gehört zu X?'"""
    bereich = KFZ_KREISSTADT.get(kfz)
    if bereich and bereich.lower() != stadtname.lower():
        return (f"{kfz} ist das Kennzeichen für den Zulassungsbereich "
                f"{bereich} — {stadtname} gehört dazu ({bundesland}).")
    return f"{kfz} ist das Kennzeichen für {stadtname}."

def _kfz_erkl2(kfz, stadtname, bundesland):
    """Erklärung für 'Für welche Stadt steht Kennzeichen X?'"""
    bereich = KFZ_KREISSTADT.get(kfz)
    if bereich and bereich.lower() != stadtname.lower():
        return (f"„{kfz}“ steht für den Zulassungsbereich {bereich}. "
                f"{stadtname} liegt in diesem Bereich ({bundesland}).")
    return f"„{kfz}“ steht für {stadtname} in {bundesland}."

# KATEGORIE: kfz — KFZ-Kennzeichen
# ══════════════════════════════════════════════════════════════════════════

for stadt in STAEDTE:
    kfz = stadt["kfz"]
    name = stadt["name"]

    # Richtung 1: Welches Kennzeichen gehört zu X?
    falsch_kfz = random.sample([s["kfz"] for s in pool_fuer(stadt) if s["kfz"] != kfz], 3)
    fragen.append({
        "id": fid(),
        "kat": "kfz",
        "kat": "kfz",
        "sw":     sw_stufe(stadt),
        "stadt": name,
        "bl": stadt["bundesland"],
        "frage": f"Welches KFZ-Kennzeichen gehört zu {name}?",
        "richtig": kfz,
        "falsch": falsch_kfz,
        "erkl": _kfz_erkl(kfz, name, stadt["bundesland"])
    })

    # Richtung 2: Für welche Stadt steht das Kennzeichen X?
    falsch_staedte = [s["name"] for s in andere_staedte([name], pool=pool_fuer(stadt))]
    fragen.append({
        "id": fid(),
        "kat": "kfz",
        "kat": "kfz",
        "sw":     sw_stufe(stadt),
        "stadt": name,
        "bl": stadt["bundesland"],
        "frage": f"Welche dieser Städte hat das Kennzeichen \u201e{kfz}\u201c?",
        "richtig": name,
        "falsch": falsch_staedte,
        "erkl": _kfz_erkl2(kfz, name, stadt["bundesland"])
    })


# ══════════════════════════════════════════════════════════════════════════
# KATEGORIE: ew — Einwohner & Bevölkerungsdichte
# ew-Schleifen laufen pro Pool, damit sw korrekt gesetzt wird
for _EW_POOL, _EW_SW in [(POOL_L, "L"), (POOL_M, "M"), (POOL_S, "S")]:
    # Alle Fragen haben genau 4 Antwortoptionen (1 richtig, 3 falsch)
    # ══════════════════════════════════════════════════════════════════════════

    paare = list(combinations(_EW_POOL, 2))
    random.shuffle(paare)
    staedte_gemischt = _EW_POOL[:]
    random.shuffle(staedte_gemischt)

    # Typ 1: Welche Stadt hat die meisten Einwohner? (4 Städte als Optionen)
    for i in range(0, len(staedte_gemischt) - 3, 2):
        gruppe = staedte_gemischt[i:i+4]
        if len(gruppe) < 4:
            continue
        ews = sorted([s["einwohner"] for s in gruppe])
        if ews[-1] >= ews[0] * 50:
            continue  # zu großer Ausreißer wäre zu einfach
        groesste = max(gruppe, key=lambda s: s["einwohner"])
        falsch = [s["name"] for s in gruppe if s["name"] != groesste["name"]]
        fragen.append({
            "id": fid(),
            "kat": "ew",
            "sw": _EW_SW,
            "stadt": groesste["name"],
            "bl": groesste["bundesland"],
            "frage": "Welche dieser Städte hat die meisten Einwohner?",
            "richtig": groesste["name"],
            "falsch": falsch,
            "erkl": (f"{groesste['name']} hat ca. {groesste['einwohner']//1000}.000 Einwohner "
                     f"und ist damit die größte der vier Städte.")
        })

    # Typ 2: Welche Stadt hat ungefähr so viele Einwohner wie X?
    random.shuffle(staedte_gemischt)
    for ziel in staedte_gemischt[:60]:
        kandidaten = [s for s in _EW_POOL if s["name"] != ziel["name"]]
        kandidaten.sort(key=lambda s: abs(s["einwohner"] - ziel["einwohner"]))
        richtige = kandidaten[0]   # nächste Stadt = richtige Antwort
        # 3 Falschantworten: mittel, weit, sehr weit — nie die Zielstadt
        falsch_pool = [s for s in kandidaten[1:] if s["name"] != ziel["name"] and s["name"] != richtige["name"]]
        f1 = falsch_pool[len(falsch_pool)//4]
        f2 = falsch_pool[len(falsch_pool)//2]
        f3 = falsch_pool[-1]
        falsch = [f1["name"], f2["name"], f3["name"]]
        diff = abs(richtige["einwohner"] - ziel["einwohner"])
        fragen.append({
            "id": fid(),
            "kat": "ew",
            "sw": _EW_SW,
            "stadt": ziel["name"],
            "bl": ziel["bundesland"],
            "frage": f"Welche Stadt hat ungefähr so viele Einwohner wie {ziel['name']}?",
            "richtig": richtige["name"],
            "falsch": falsch,
            "erkl": (f"{richtige['name']} hat ca. {richtige['einwohner']//1000}.000 Einwohner — "
                     f"am nächsten an {ziel['name']} mit {ziel['einwohner']//1000}.000.")
        })

    # Typ 3: Bevölkerungsdichte — welche Stadt ist am dichtesten besiedelt?
    random.shuffle(staedte_gemischt)
    for i in range(0, len(staedte_gemischt) - 3, 2):
        gruppe = staedte_gemischt[i:i+4]
        if len(gruppe) < 4:
            continue
        if any(s["flaeche"] == 0 for s in gruppe): continue
        dichtigste  = max(gruppe, key=lambda s: s["einwohner"] / s["flaeche"])
        groesste_ew = max(gruppe, key=lambda s: s["einwohner"])
        if dichtigste["name"] == groesste_ew["name"]:
            continue  # nur kontraintuitive Fälle
        falsch = [s["name"] for s in gruppe if s["name"] != dichtigste["name"]]
        dichte = int(dichtigste["einwohner"] / dichtigste["flaeche"])
        fragen.append({
            "id": fid(),
            "kat": "ew",
            "sw": _EW_SW,
            "stadt": dichtigste["name"],
            "bl": dichtigste["bundesland"],
            "frage": "Welche dieser Städte hat die höchste Bevölkerungsdichte (Einwohner pro km²)?",
            "richtig": dichtigste["name"],
            "falsch": falsch,
            "erkl": (f"{dichtigste['name']} hat {dichte} Einw./km² — obwohl {groesste_ew['name']} "
                     f"mehr Einwohner hat, ist {dichtigste['name']} viel kompakter.")
        })

    # ── Typ 4: Einwohner-Schwelle — über/unter X ──────────────────────────────
    for schwelle in [100000, 200000, 500000]:
        ueber = [s for s in _EW_POOL if s["einwohner"] > schwelle]
        unter = [s for s in _EW_POOL if s["einwohner"] <= schwelle]
        if len(ueber) < 1 or len(unter) < 3: continue
        # "Welche hat ÜBER X?" — richtig=eine mit über X, falsch=drei mit unter X
        for richtig in random.sample(ueber, min(5, len(ueber))):
            falsch3 = random.sample([s["name"] for s in unter], 3)
            fragen.append({
                "id": fid(), "kat": "ew",
            "sw": _EW_SW,
                "stadt": richtig["name"], "bl": richtig["bundesland"],
                "frage": f"Welche dieser Städte hat mehr als {schwelle//1000}.000 Einwohner?",
                "richtig": richtig["name"],
                "falsch": falsch3,
                "erkl": (f"{richtig['name']} hat ca. {richtig['einwohner']//1000}.000 Einwohner "
                         f"— damit über {schwelle//1000}.000.")
            })
        # "Welche hat UNTER X?" — richtig=eine mit unter X, falsch=drei mit über X
        if len(unter) >= 1 and len(ueber) >= 3:
            for richtig in random.sample(unter, min(5, len(unter))):
                falsch3 = random.sample([s["name"] for s in ueber], 3)
                fragen.append({
                    "id": fid(), "kat": "ew",
            "sw": _EW_SW,
                    "stadt": richtig["name"], "bl": richtig["bundesland"],
                    "frage": f"Welche dieser Städte hat weniger als {schwelle//1000}.000 Einwohner?",
                    "richtig": richtig["name"],
                    "falsch": falsch3,
                    "erkl": (f"{richtig['name']} hat ca. {richtig['einwohner']//1000}.000 Einwohner "
                             f"— damit unter {schwelle//1000}.000.")
                })

    # ── Typ 5: Fläche — größte/kleinste Stadt ─────────────────────────────────
    random.shuffle(staedte_gemischt)
    for i in range(0, len(staedte_gemischt) - 3, 2):
        gruppe = staedte_gemischt[i:i+4]
        if len(gruppe) < 4: continue
        flaechen = [s["flaeche"] for s in gruppe]
        if any(f == 0 for f in flaechen): continue
        if max(flaechen) - min(flaechen) < 30: continue
        groesste = max(gruppe, key=lambda s: s["flaeche"])
        kleinste = min(gruppe, key=lambda s: s["flaeche"])
        falsch_g = [s["name"] for s in gruppe if s["name"] != groesste["name"]]
        falsch_k = [s["name"] for s in gruppe if s["name"] != kleinste["name"]]
        fragen.append({
            "id": fid(), "kat": "ew",
            "sw": _EW_SW,
            "stadt": groesste["name"], "bl": groesste["bundesland"],
            "frage": "Welche dieser Städte hat die größte Stadtfläche?",
            "richtig": groesste["name"], "falsch": falsch_g,
            "erkl": (f"{groesste['name']} hat eine Fläche von {groesste['flaeche']} km² "
                     f"— die größte der vier Städte.")
        })
        fragen.append({
            "id": fid(), "kat": "ew",
            "sw": _EW_SW,
            "stadt": kleinste["name"], "bl": kleinste["bundesland"],
            "frage": "Welche dieser Städte hat die kleinste Stadtfläche?",
            "richtig": kleinste["name"], "falsch": falsch_k,
            "erkl": (f"{kleinste['name']} hat nur {kleinste['flaeche']} km² "
                     f"— die kleinste Fläche der vier Städte.")
        })



    # ══════════════════════════════════════════════════════════════════════════
# KATEGORIE: dist — Distanz & Himmelsrichtung
# ══════════════════════════════════════════════════════════════════════════

dist_paare = random.sample(paare, min(60, len(paare)))

for a, b in dist_paare:
    km = haversine(a["lat"], a["lon"], b["lat"], b["lon"])
    r_km = runde_distanz(km)

    # Distanz-Frage
    falsche_dist = distanz_optionen(km)
    fragen.append({
        "id": fid(),
        "kat": "dist",
        "kat": "dist",
        "sw":     sw_stufe(stadt),
        "stadt": a["name"],
        "bl": a["bundesland"],
        "frage": f"Wie weit ist es Luftlinie von {a['name']} nach {b['name']}?",
        "richtig": f"ca. {r_km} km",
        "falsch": falsche_dist,
        "erkl": (f"Die Luftlinie von {a['name']} nach {b['name']} beträgt "
                 f"ca. {r_km} km.")
    })

    # Himmelsrichtungs-Frage — falsche Optionen als ±90°/±180° zum richtigen Wert
    deg = bearing(a["lat"], a["lon"], b["lat"], b["lon"])
    richtig_hr = himmelsrichtung(deg)
    alle_hr = ["Norden","Nordosten","Osten","Südosten","Süden","Südwesten","Westen","Nordwesten"]
    richtig_idx = alle_hr.index(richtig_hr)
    # Nachbarn: ±90° (2 Schritte) und ±180° (4 Schritte)
    falsch_hr = [
        alle_hr[(richtig_idx + 2) % 8],   # +90°
        alle_hr[(richtig_idx - 2) % 8],   # -90°
        alle_hr[(richtig_idx + 4) % 8],   # +180° (Gegenrichtung)
    ]
    fragen.append({
        "id": fid(),
        "kat": "dist",
        "kat": "dist",
        "sw":     sw_stufe(stadt),
        "stadt": b["name"],
        "bl": b["bundesland"],
        "frage": f"In welcher Himmelsrichtung liegt {b['name']} von {a['name']} aus?",
        "richtig": richtig_hr,
        "falsch": falsch_hr,
        "erkl": (f"{b['name']} liegt von {a['name']} aus in Richtung {richtig_hr} "
                 f"(ca. {int(deg)}°).")
    })


# ── Grenzentfernung ─────────────────────────────────────────────────────────
# Koordinaten der nächsten Grenzpunkte je Nachbarland
# Mehrere Grenzpunkte pro Land — es wird der nächste gewählt
GRENZEN_MULTI = {
    "Frankreich":  [(48.9743, 8.2247),  # Lauterbourg
                   (48.2208, 7.0064),   # Breisach
                   (49.1225, 6.8876)],  # Saarbrücken
    "Schweiz":     [(47.5897, 7.5892),  # Basel
                   (47.6558, 8.8694),   # Konstanz
                   (47.4742, 9.6340)],  # Lindau
    "Österreich":  [(47.5809, 12.9699), # Salzburg/Freilassing
                   (47.5778, 12.1733),  # Kufstein
                   (47.5008, 9.7378),   # Bregenz
                   (48.5619, 13.4531)], # Passau/Schärding
    "Tschechien":  [(50.4059, 12.4740), # Aš
                   (50.7564, 12.9236),  # Zwickau-Grenze
                   (50.0292, 14.5388)], # Prag-Richtung
    "Polen":       [(51.1534, 14.9874), # Görlitz
                   (54.3159, 14.1469)], # Swinemünde
    "Dänemark":    [(54.8079, 9.4557),  # Flensburg
                   (54.7500, 8.9000)],  # Tondern
    "Niederlande": [(51.8490, 6.1342),  # Kleve
                   (52.3596, 7.0153),   # Bad Bentheim
                   (53.1676, 7.1949)],  # Bunde
    "Belgien":     [(50.7236, 6.0291),  # Aachen
                   (50.3143, 6.1241)],  # St. Vith
    "Luxemburg":   [(49.4626, 6.3575),  # Trier
                   (49.6766, 6.1592)],  # Perl
}

def naechster_grenzpunkt(stadt_lat, stadt_lon):
    """Gibt {land: min_distanz} zurück, nutzt nächsten Grenzpunkt je Land"""
    ergebnis = {}
    for land, punkte in GRENZEN_MULTI.items():
        min_d = min(haversine(stadt_lat, stadt_lon, lat, lon) for lat, lon in punkte)
        ergebnis[land] = min_d
    return ergebnis

GRENZEN = {land: pts[0] for land, pts in GRENZEN_MULTI.items()}  # Fallback

for stadt in STAEDTE:
    # Nächstes Nachbarland berechnen
    distanzen = naechster_grenzpunkt(stadt["lat"], stadt["lon"])
    naechstes_land = min(distanzen, key=distanzen.get)
    naechste_dist  = distanzen[naechstes_land]
    r_dist = runde_distanz(naechste_dist)

    # Typ 1: Welches Nachbarland liegt X am nächsten?
    alle_laender = list(GRENZEN.keys())
    falsch_laender = random.sample([l for l in alle_laender if l != naechstes_land], 3)
    fragen.append({
        "id": fid(),
        "kat": "dist",
        "kat": "dist",
        "sw":     sw_stufe(stadt),
        "stadt": stadt["name"],
        "bl": stadt["bundesland"],
        "frage": f"Welches Nachbarland liegt {stadt['name']} am nächsten?",
        "richtig": naechstes_land,
        "falsch": falsch_laender,
        "erkl": (f"Von {stadt['name']} bis zur Grenze mit {naechstes_land} "
                 f"sind es nur ca. {r_dist} km Luftlinie.")
    })

    # Typ 2: Wie weit ist X zur nächsten Staatsgrenze?
    falsche_dist = distanz_optionen(naechste_dist)
    fragen.append({
        "id": fid(),
        "kat": "dist",
        "kat": "dist",
        "sw":     sw_stufe(stadt),
        "stadt": stadt["name"],
        "bl": stadt["bundesland"],
        "frage": f"Wie weit ist {stadt['name']} von der nächsten Staatsgrenze entfernt?",
        "richtig": f"ca. {r_dist} km",
        "falsch": falsche_dist,
        "erkl": (f"Die nächste Staatsgrenze von {stadt['name']} ist die Grenze zu "
                 f"{naechstes_land} — ca. {r_dist} km entfernt.")
    })



# ══════════════════════════════════════════════════════════════════════════
# KATEGORIE: hoehe — Höhenunterschiede
# ══════════════════════════════════════════════════════════════════════════

HOEHENB = [
    (0,   50,  "unter 50 m"),
    (50,  150, "50–150 m"),
    (150, 300, "150–300 m"),
    (300, 9999,"über 300 m"),
]

def abstand_zur_linie(px, py, ax, ay, bx, by):
    """Senkrechter Abstand (km) von Punkt P(px,py) zur Linie A→B — filtert Routen-Städte."""
    dx = bx - ax; dy = by - ay
    if dx == 0 and dy == 0:
        return haversine(ay, ax, py, px)
    t = max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy) / (dx*dx + dy*dy)))
    return haversine(ay + t*dy, ax + t*dx, py, px)

MAX_ROUTEN_ABSTAND_KM = 120  # Städte müssen max. 120 km von der Luftlinie entfernt sein

def staedte_auf_route(start, ziel, alle, ausschliessen=()):
    """Gibt Städte auf der Route Start→Ziel zurück, sortiert nach Distanz vom Start."""
    ergebnis = []
    for s in alle:
        if s["name"] in ausschliessen: continue
        abstand = abstand_zur_linie(s["lon"], s["lat"],
                                     start["lon"], start["lat"],
                                     ziel["lon"], ziel["lat"])
        if abstand <= MAX_ROUTEN_ABSTAND_KM:
            ergebnis.append(s)
    ergebnis.sort(key=lambda s: haversine(start["lat"], start["lon"], s["lat"], s["lon"]))
    return ergebnis

def hoehenbereich(h):
    for von, bis, label in HOEHENB:
        if von <= h < bis:
            return label
    return None

def runde_hoehe(h):
    if h < 100: return round(h / 10) * 10
    return round(h / 50) * 50

def hoehen_optionen(richtig_h):
    """3 falsche Höhenangaben mit deutlichem Abstand"""
    r = runde_hoehe(richtig_h)
    kandidaten = []
    for faktor in [0.3, 0.5, 1.8, 2.5, 3.0, 0.15]:
        c = max(5, round(faktor * r / 10) * 10)
        if abs(c - r) > 30 and c not in kandidaten and c != r:
            kandidaten.append(c)
        if len(kandidaten) == 3:
            break
    while len(kandidaten) < 3:
        c = random.choice([10, 50, 100, 200, 350, 450])
        if abs(c - r) > 30 and c not in kandidaten:
            kandidaten.append(c)
    return [f"ca. {c} m" for c in kandidaten]

staedte_h = STAEDTE[:]  # Kopie zum Shufflen

# ── Typ 1: Welche Stadt liegt am höchsten? (4 Städte) ─────────────────────
random.shuffle(staedte_h)
for i in range(0, len(staedte_h) - 3, 2):
    gruppe = staedte_h[i:i+4]
    if len(gruppe) < 4: continue
    hoechen = [s["hoehe"] for s in gruppe]
    if max(hoechen) - min(hoechen) < 50: continue  # zu ähnlich
    hoechste = max(gruppe, key=lambda s: s["hoehe"])
    tiefste  = min(gruppe, key=lambda s: s["hoehe"])
    falsch_h = [s["name"] for s in gruppe if s["name"] != hoechste["name"]]
    falsch_t = [s["name"] for s in gruppe if s["name"] != tiefste["name"]]
    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": hoechste["name"], "bl": hoechste["bundesland"],
        "frage": "Welche dieser Städte liegt am höchsten über dem Meeresspiegel?",
        "richtig": hoechste["name"], "falsch": falsch_h,
        "erkl": f"{hoechste['name']} liegt auf {hoechste['hoehe']} m — am höchsten der vier Städte."
    })
    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": tiefste["name"], "bl": tiefste["bundesland"],
        "frage": "Welche dieser Städte liegt am tiefsten (nächste am Meeresspiegel)?",
        "richtig": tiefste["name"], "falsch": falsch_t,
        "erkl": f"{tiefste['name']} liegt auf nur {tiefste['hoehe']} m — am tiefsten der vier Städte."
    })

# ── Typ 2: Welche ist höher/tiefer als Stadt X? ────────────────────────────
random.shuffle(staedte_h)
for referenz in staedte_h[:30]:
    hoeher = [s for s in STAEDTE if s["hoehe"] > referenz["hoehe"] + 50
              and s["name"] != referenz["name"]]
    tiefer = [s for s in STAEDTE if s["hoehe"] < referenz["hoehe"] - 50
              and s["name"] != referenz["name"]]
    if len(hoeher) >= 1 and len(tiefer) >= 3:
        richtig = random.choice(hoeher)
        falsch3 = random.sample(tiefer, 3)
        fragen.append({
            "id": fid(), "kat": "hoehe",
        "sw":     "?",
            "stadt": referenz["name"], "bl": referenz["bundesland"],
            "frage": f"Welche dieser Städte liegt höher als {referenz['name']}?",
            "richtig": richtig["name"],
            "falsch": [s["name"] for s in falsch3],
            "erkl": (f"{richtig['name']} liegt auf {richtig['hoehe']} m — "
                     f"höher als {referenz['name']} mit {referenz['hoehe']} m.")
        })
    if len(tiefer) >= 1 and len(hoeher) >= 3:
        richtig = random.choice(tiefer)
        falsch3 = random.sample(hoeher, 3)
        fragen.append({
            "id": fid(), "kat": "hoehe",
        "sw":     "?",
            "stadt": referenz["name"], "bl": referenz["bundesland"],
            "frage": f"Welche dieser Städte liegt tiefer als {referenz['name']}?",
            "richtig": richtig["name"],
            "falsch": [s["name"] for s in falsch3],
            "erkl": (f"{richtig['name']} liegt auf {richtig['hoehe']} m — "
                     f"tiefer als {referenz['name']} mit {referenz['hoehe']} m.")
        })

# ── Typ 3: In welchem Höhenbereich liegt X? ────────────────────────────────
for stadt in STAEDTE:
    bereich = hoehenbereich(stadt["hoehe"])
    if not bereich: continue
    alle_bereiche = [b[2] for b in HOEHENB]
    falsch_b = [b for b in alle_bereiche if b != bereich]
    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": stadt["name"], "bl": stadt["bundesland"],
        "frage": f"In welchem Höhenbereich liegt {stadt['name']}?",
        "richtig": bereich,
        "falsch": falsch_b,
        "erkl": f"{stadt['name']} liegt auf {stadt['hoehe']} m — also {bereich}."
    })

# ── Typ 4: Höhenunterschied zwischen zwei Städten (Schätzfrage) ────────────
paare_h = list(combinations(STAEDTE, 2))
random.shuffle(paare_h)
for a, b in paare_h[:40]:
    diff = abs(a["hoehe"] - b["hoehe"])
    if diff < 80: continue  # zu gering
    r_diff = runde_hoehe(diff)
    falsch_d = hoehen_optionen(diff)
    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": a["name"], "bl": a["bundesland"],
        "frage": f"Wie groß ist der Höhenunterschied zwischen {a['name']} und {b['name']}?",
        "richtig": f"ca. {r_diff} m",
        "falsch": falsch_d,
        "erkl": (f"{a['name']} liegt auf {a['hoehe']} m, {b['name']} auf {b['hoehe']} m — "
                 f"Unterschied: ca. {r_diff} m.")
    })

# ── Typ 5: Höchste/Tiefste Stadt eines Bundeslands ────────────────────────
from collections import defaultdict as _dd
bl_staedte = _dd(list)
for s in STAEDTE:
    bl_staedte[s["bundesland"]].append(s)

for bl_name, gruppe in bl_staedte.items():
    if len(gruppe) < 3: continue
    hoechste = max(gruppe, key=lambda s: s["hoehe"])
    tiefste  = min(gruppe, key=lambda s: s["hoehe"])
    if hoechste["name"] == tiefste["name"]: continue
    # Falsche: andere Städte aus dem BL oder anderen BLs
    falsch_pool = [s["name"] for s in gruppe if s["name"] != hoechste["name"]]
    if len(falsch_pool) < 3:
        falsch_pool += [s["name"] for s in pool_fuer(hoechste)
                        if s["bundesland"] != bl_name]
    falsch3 = random.sample(falsch_pool, 3)
    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": hoechste["name"], "bl": bl_name,
        "frage": f"Welche Stadt in {bl_name} liegt am höchsten?",
        "richtig": hoechste["name"],
        "falsch": falsch3,
        "erkl": f"{hoechste['name']} liegt auf {hoechste['hoehe']} m — die höchste Stadt in {bl_name}."
    })

# ── Typ 6: Liegt über/unter Schwelle? ─────────────────────────────────────
for schwelle in [100, 200, 300]:
    ueber = [s for s in STAEDTE if s["hoehe"] > schwelle]
    unter = [s for s in STAEDTE if s["hoehe"] <= schwelle]
    if len(ueber) < 1 or len(unter) < 3: continue
    for richtig in random.sample(ueber, min(5, len(ueber))):
        falsch3 = random.sample([s["name"] for s in unter], 3)
        fragen.append({
            "id": fid(), "kat": "hoehe",
        "sw":     "?",
            "stadt": richtig["name"], "bl": richtig["bundesland"],
            "frage": f"Welche dieser Städte liegt über {schwelle} m?",
            "richtig": richtig["name"],
            "falsch": falsch3,
            "erkl": f"{richtig['name']} liegt auf {richtig['hoehe']} m — also über {schwelle} m."
        })

# ── Typ 7: Welche Kombination hat den größten Höhenunterschied? ────────────
tripel = list(combinations(STAEDTE, 2))
random.shuffle(tripel)
for _ in range(30):
    vier_paare = random.sample(tripel, 4)
    diffs = [(abs(a["hoehe"] - b["hoehe"]), a, b) for a, b in vier_paare]
    diffs.sort(key=lambda x: x[0], reverse=True)
    if diffs[0][0] - diffs[1][0] < 50: continue  # kein klarer Sieger
    richtig_diff, ra, rb = diffs[0]
    richtig_label = f"{ra['name']} – {rb['name']}"
    falsch_labels  = [f"{a['name']} – {b['name']}" for _, a, b in diffs[1:]]
    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": ra["name"], "bl": ra["bundesland"],
        "frage": "Welche Kombination hat den größten Höhenunterschied?",
        "richtig": richtig_label,
        "falsch": falsch_labels,
        "erkl": (f"{richtig_label}: {ra['hoehe']} m vs. {rb['hoehe']} m — "
                 f"Unterschied {richtig_diff} m.")
    })

# ── Typ 8: Auf Route A→B — welche Zwischenstadt liegt am höchsten? ─────────
random.shuffle(staedte_h)
for i in range(0, len(staedte_h) - 1, 3):
    if i + 1 >= len(staedte_h): break
    start = staedte_h[i]
    ziel  = staedte_h[i+1]
    # Zwischenstädte: grob auf der Route (Haversine-Nähe zur Verbindungslinie)
    kandidaten = [s for s in STAEDTE
                  if s["name"] not in (start["name"], ziel["name"])]
    if len(kandidaten) < 4: continue
    vier = random.sample(kandidaten, 4)
    hoechste = max(vier, key=lambda s: s["hoehe"])
    falsch3  = [s["name"] for s in vier if s["name"] != hoechste["name"]]
    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": hoechste["name"], "bl": hoechste["bundesland"],
        "frage": (f"Du fährst von {start['name']} nach {ziel['name']}. "
                  f"Welche dieser Städte liegt am höchsten?"),
        "richtig": hoechste["name"],
        "falsch": falsch3,
        "erkl": (f"{hoechste['name']} liegt auf {hoechste['hoehe']} m — "
                 f"am höchsten der vier Optionen auf dieser Route.")
    })



# ── Typ 8: Route steigt oder fällt? ────────────────────────────────────────
# Frageform: "Auf dem Weg von Hamburg nach München — zwischen welchen zwei
# Städten STEIGT / FÄLLT die Route am stärksten?"
# Antworten: immer Stadtpaare "A → B" (Richtung der Route)

STEIG_ROUTEN = [
    ("Hamburg",   "München"),
    ("Berlin",    "Köln"),
    ("Dresden",   "Frankfurt am Main"),
    ("Rostock",   "Freiburg im Breisgau"),
    ("Flensburg", "Nürnberg"),
    ("Bremen",    "Augsburg"),
    ("Hannover",  "München"),
]
random.shuffle(STEIG_ROUTEN)
steig_fragen_count = 0

for start_name, ziel_name in STEIG_ROUTEN:
    start = S.get(start_name)
    ziel  = S.get(ziel_name)
    if not start or not ziel: continue

    auf_route = staedte_auf_route(start, ziel, STAEDTE, ausschliessen=(start_name, ziel_name))
    if len(auf_route) < 5: continue

    # Konsekutive Paare mit ihrem Höhendelta
    paare = []
    for i in range(len(auf_route) - 1):
        a, b = auf_route[i], auf_route[i+1]
        delta = b["hoehe"] - a["hoehe"]
        paare.append((a, b, delta))

    # mind. 4 Paare für eine sinnvolle Auswahl
    if len(paare) < 4: continue

    # Frage 1: Wo steigt die Route am stärksten?
    steigend = sorted(paare, key=lambda x: x[2], reverse=True)
    richtig_s = steigend[0]
    if richtig_s[2] < 50: continue  # zu wenig Unterschied

    # 3 Falsche: andere Paare, bevorzugt fallende
    falsch_pool_s = [p for p in paare
                     if p[0]["name"] != richtig_s[0]["name"]
                     and p[1]["name"] != richtig_s[1]["name"]]
    if len(falsch_pool_s) < 3: continue
    # Wähle gut verteilte Falschantworten (auch fallende dabei)
    falsch_pool_s.sort(key=lambda x: x[2])  # aufsteigend = fallende zuerst
    falsch3_s = falsch_pool_s[:3]

    label_r  = f"{richtig_s[0]['name']} → {richtig_s[1]['name']}"
    label_f  = [f"{p[0]['name']} → {p[1]['name']}" for p in falsch3_s]

    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": richtig_s[0]["name"], "bl": richtig_s[0]["bundesland"],
        "frage": (f"Du fährst von {start_name} nach {ziel_name}. "
                  f"Zwischen welchen zwei Städten steigt die Route am stärksten?"),
        "richtig": label_r,
        "falsch":  label_f,
        "erkl": (f"{richtig_s[0]['name']} liegt auf {richtig_s[0]['hoehe']} m, "
                 f"{richtig_s[1]['name']} auf {richtig_s[1]['hoehe']} m — "
                 f"ein Anstieg von +{richtig_s[2]} m.")
    })
    steig_fragen_count += 1

    # Frage 2: Wo fällt die Route am stärksten?
    fallend = sorted(paare, key=lambda x: x[2])
    richtig_f = fallend[0]
    if richtig_f[2] > -50: continue

    falsch_pool_f = [p for p in paare
                     if p[0]["name"] != richtig_f[0]["name"]
                     and p[1]["name"] != richtig_f[1]["name"]]
    if len(falsch_pool_f) < 3: continue
    falsch_pool_f.sort(key=lambda x: x[2], reverse=True)  # steigende zuerst
    falsch3_f = falsch_pool_f[:3]

    label_rf = f"{richtig_f[0]['name']} → {richtig_f[1]['name']}"
    label_ff = [f"{p[0]['name']} → {p[1]['name']}" for p in falsch3_f]

    fragen.append({
        "id": fid(), "kat": "hoehe",
        "sw":     "?",
        "stadt": richtig_f[0]["name"], "bl": richtig_f[0]["bundesland"],
        "frage": (f"Du fährst von {start_name} nach {ziel_name}. "
                  f"Zwischen welchen zwei Städten fällt die Route am stärksten?"),
        "richtig": label_rf,
        "falsch":  label_ff,
        "erkl": (f"{richtig_f[0]['name']} liegt auf {richtig_f[0]['hoehe']} m, "
                 f"{richtig_f[1]['name']} auf {richtig_f[1]['hoehe']} m — "
                 f"ein Gefälle von {richtig_f[2]} m.")
    })
    steig_fragen_count += 1
    if steig_fragen_count >= 12: break  # max 12 Fragen dieses Typs


# ── Nächste Nachbarstadt ───────────────────────────────────────────────────
# "Welche Stadt liegt am nächsten an X?"
random.shuffle(STAEDTE)
for referenz in STAEDTE[:40]:
    # Alle anderen nach Distanz sortieren (aus gleichem sw-Pool)
    andere = sorted(
        [s for s in pool_fuer(referenz) if s["name"] != referenz["name"]],
        key=lambda s: haversine(referenz["lat"], referenz["lon"], s["lat"], s["lon"])
    )
    naechste  = andere[0]   # richtige Antwort
    weiter    = andere[5:8] # klar weiter weg
    if len(weiter) < 3: continue
    falsch3 = random.sample(weiter, 3)
    dist_km = int(haversine(referenz["lat"], referenz["lon"],
                            naechste["lat"], naechste["lon"]))
    fragen.append({
        "id": fid(), "kat": "dist",
        "id": fid(), "kat": "dist",
        "sw":     sw_stufe(stadt),
        "stadt": referenz["name"], "bl": referenz["bundesland"],
        "frage": f"Welche Stadt liegt am nächsten an {referenz['name']}?",
        "richtig": naechste["name"],
        "falsch": [s["name"] for s in falsch3],
        "erkl": (f"{naechste['name']} liegt nur ca. {dist_km} km von "
                 f"{referenz['name']} entfernt — näher als alle anderen Optionen.")
    })

# ── Reihenfolge auf Route ──────────────────────────────────────────────────
# "Welche Stadt kommt nach X, wenn du von A nach B fährst?"
routen = [
    ("Hamburg",  "München"),
    ("Berlin",   "Köln"),
    ("Dresden",  "Frankfurt am Main"),
    ("Kiel",     "Stuttgart"),
    ("Rostock",  "Freiburg im Breisgau"),
    ("Flensburg","Nürnberg"),
    ("Bremen",   "Augsburg"),
    ("Hannover", "München"),
]
for start_name, ziel_name in routen:
    start = S.get(start_name)
    ziel  = S.get(ziel_name)
    if not start or not ziel: continue

    # Städte auf der Route: nur Städte nahe der Luftlinie
    auf_route = staedte_auf_route(start, ziel, STAEDTE, ausschliessen=(start_name, ziel_name))
    if len(auf_route) < 6: continue
    # Referenzstadt: ca. in der Mitte der Route
    mitte_idx = len(auf_route) // 2
    referenz  = auf_route[mitte_idx]

    # Richtige Antwort: nächste Stadt nach Referenz Richtung Ziel
    nach_referenz = [s for s in auf_route
                     if haversine(start["lat"], start["lon"], s["lat"], s["lon"])
                     > haversine(start["lat"], start["lon"],
                                 referenz["lat"], referenz["lon"])
                     and s["name"] != referenz["name"]]
    if not nach_referenz: continue
    richtig = nach_referenz[0]

    # Falsche: Städte vor der Referenz
    vor_referenz = [s for s in auf_route if s["name"] != referenz["name"]
                    and s["name"] != richtig["name"]]
    if len(vor_referenz) < 3: continue
    falsch3 = random.sample(vor_referenz, 3)

    fragen.append({
        "id": fid(), "kat": "dist",
        "id": fid(), "kat": "dist",
        "sw":     sw_stufe(stadt),
        "stadt": referenz["name"], "bl": referenz["bundesland"],
        "frage": (f"Du fährst von {start_name} nach {ziel_name}. "
                  f"Welche Stadt kommt nach {referenz['name']}?"),
        "richtig": richtig["name"],
        "falsch": [s["name"] for s in falsch3],
        "erkl": (f"Auf der Route {start_name} → {ziel_name} folgt nach "
                 f"{referenz['name']} als nächstes {richtig['name']}.")
    })


# ══════════════════════════════════════════════════════════════════════════
# KATEGORIE: bahn — Deutsche Bahn (aus bahnhof.json)
# ══════════════════════════════════════════════════════════════════════════

import os as _os
BAHN_FILE = "bahnhof.json"
if not _os.path.exists(BAHN_FILE):
    BAHN_FILE = args.staedte.replace("staedte.json", "bahnhof.json")

if _os.path.exists(BAHN_FILE):
    with open(BAHN_FILE, encoding="utf-8") as f:
        BAHN = json.load(f)

    BK  = BAHN["bahnhof_kategorien"]   # {stadtname: {kategorie, ice_halt, ...}}
    ICE = BAHN["ice_strecken"]         # {streckenname: {halte, halte_quiz, ...}}

    # Städte nach Kategorie
    ice_staedte    = [s for s in STAEDTE if BK.get(s["name"], {}).get("ice_halt")]
    kein_ice       = [s for s in STAEDTE if not BK.get(s["name"], {}).get("ice_halt")
                      and BK.get(s["name"], {}).get("kategorie")]
    kat1_2         = [s for s in STAEDTE if BK.get(s["name"], {}).get("kategorie") in (1, 2)]
    kat3plus       = [s for s in STAEDTE if (BK.get(s["name"], {}).get("kategorie") or 9) >= 3]

    # ── Typ 1: Hat diese Stadt einen ICE-Halt? ─────────────────────────────
    # Kontraintuitive Fälle: überraschende ICE-Halte & überraschende Nicht-Halte
    ueberraschend_ja  = ["Montabaur", "Wolfsburg", "Kassel"]   # klein aber ICE
    ueberraschend_nein = ["Wiesbaden", "Heidelberg", "Regensburg", "Mainz"]  # groß aber kein ICE

    for stadtname in ueberraschend_ja:
        stadt = S.get(stadtname)
        if not stadt or not BK.get(stadtname): continue
        bk = BK[stadtname]
        _kein_ice_pool = [s["name"] for s in kein_ice if s["name"] != stadtname
                          and sw_stufe(s) == sw_stufe(stadt)]
        if len(_kein_ice_pool) < 3:
            _kein_ice_pool = [s["name"] for s in kein_ice if s["name"] != stadtname]
        falsch3 = random.sample(_kein_ice_pool, min(3, len(_kein_ice_pool)))
        if len(falsch3) < 3: continue
        hinweis = bk.get("hinweis", "")
        fragen.append({
            "id": fid(), "kat": "bahn",
        "sw":     "?",
            "stadt": stadtname, "bl": stadt["bundesland"],
            "frage": f"Welche dieser Städte hat trotz ihrer Größe einen ICE-Halt?",
            "richtig": stadtname,
            "falsch": falsch3,
            "erkl": (f"{stadtname} hat tatsächlich einen ICE-Halt ({bk['bahnhof_name']})! "
                     + (hinweis or f"Kategorie {bk['kategorie']} — Fernverkehrsbahnhof."))
        })

    for stadtname in ueberraschend_nein:
        stadt = S.get(stadtname)
        if not stadt or not BK.get(stadtname): continue
        bk = BK[stadtname]
        # Frage: Welche dieser Städte hat KEINEN ICE-Halt?
        drei_ice = random.sample([s["name"] for s in ice_staedte
                                  if s["name"] != stadtname], 3)
        fragen.append({
            "id": fid(), "kat": "bahn",
        "sw":     "?",
            "stadt": stadtname, "bl": stadt["bundesland"],
            "frage": f"Welche dieser Städte hat keinen direkten ICE-Halt?",
            "richtig": stadtname,
            "falsch": drei_ice,
            "erkl": (f"{stadtname} hat trotz seiner Größe keinen eigenen ICE-Halt — "
                     f"Bahnhofskategorie {bk['kategorie']}.")
        })

    # ── Typ 2: Welcher Bahnhof hat die höchste Kategorie? (4 Städte) ──────────
    random.shuffle(STAEDTE)
    staedte_mit_kat = [s for s in STAEDTE if BK.get(s["name"], {}).get("kategorie")]
    for i in range(0, len(staedte_mit_kat) - 3, 2):
        gruppe = staedte_mit_kat[i:i+4]
        if len(gruppe) < 4: continue
        kats = [BK[s["name"]]["kategorie"] for s in gruppe]
        if max(kats) - min(kats) < 2: continue  # zu ähnlich
        bester = min(gruppe, key=lambda s: BK[s["name"]]["kategorie"])  # niedrigste Kat = größter Bhf
        falsch3 = [s["name"] for s in gruppe if s["name"] != bester["name"]]
        kat_b = BK[bester["name"]]["kategorie"]
        fragen.append({
            "id": fid(), "kat": "bahn",
        "sw":     "?",
            "stadt": bester["name"], "bl": bester["bundesland"],
            "frage": "Welche dieser Städte hat den bedeutendsten Bahnhof?",
            "richtig": bester["name"],
            "falsch": falsch3,
            "erkl": (f"{bester['name']} hat einen Bahnhof der Kategorie {kat_b} "
                     f"({BK[bester['name']]['bahnhof_name']}) — "
                     f"{'Fernverkehr mit ICE.' if BK[bester['name']]['ice_halt'] else 'Regionaler Knotenbahnhof.'}")
        })

    # ── Typ 3: Liegt diese Stadt an der ICE-Strecke X? ────────────────────
    for strecke_name, strecke in ICE.items():
        halte_quiz = strecke["halte_quiz"]
        alle_halte = set(strecke["halte"]) | set(halte_quiz)
        nicht_halte = [s["name"] for s in STAEDTE if s["name"] not in alle_halte]
        quiz_halte = halte_quiz[1:-1] if len(halte_quiz) > 2 else []  # nur 2 Halte = nur Endpunkte → überspringen

        for halt_name in quiz_halte:
            halt_stadt = S.get(halt_name)
            if not halt_stadt: continue
            # Falschantworten aus gleichem sw-Pool wie halt_stadt
            _nh_pool = [n for n in nicht_halte if S.get(n) and sw_stufe(S[n]) == sw_stufe(halt_stadt)]
            if len(_nh_pool) < 3: _nh_pool = nicht_halte  # Fallback
            falsch3 = random.sample(_nh_pool, min(3, len(_nh_pool)))
            if len(falsch3) < 3: continue
            fragen.append({
                "id": fid(), "kat": "bahn",
        "sw":     "?",
                "stadt": halt_name, "bl": halt_stadt["bundesland"],
                "frage": f"Welche dieser Städte liegt an der ICE-Strecke {strecke_name}?",
                "richtig": halt_name,
                "falsch": falsch3,
                "erkl": (f"{halt_name} ist ein Halt auf der Strecke {strecke_name}. "
                         f"{strecke['beschreibung']}")
            })

    # ── Typ 4: Welche Stadt kommt nach X? (Reihenfolge auf Strecke) ────────
    for strecke_name, strecke in ICE.items():
        halte = strecke["halte"]
        if len(halte) < 3: continue
        # Jede Zwischenposition als Frage
        for i in range(1, len(halte) - 1):
            referenz = halte[i]
            naechster = halte[i+1]
            ref_stadt = S.get(referenz)
            nae_stadt = S.get(naechster)
            if not ref_stadt or not nae_stadt: continue
            start, end = halte[0], halte[-1]
            # Überspringe wenn naechster der Endpunkt ist (Endpunkt steht im Fragentext)
            if naechster == end or naechster == start: continue
            # Falsche: weder Referenzstadt, noch nächster Halt, noch Start/Ende der Strecke
            falsch_pool = [h for h in halte
                           if h != naechster and h != referenz and h != start and h != end]
            # extra_pool: nur Städte aus gleichem sw-Pool wie ref_stadt
            _ref_pool = pool_fuer(ref_stadt)
            extra_pool  = [s["name"] for s in _ref_pool
                           if s["name"] not in halte and s["name"] != referenz
                           and s["name"] != start and s["name"] != end]
            alle_falsch = falsch_pool + extra_pool
            if len(alle_falsch) < 3: continue
            falsch3 = random.sample(alle_falsch, 3)
            fragen.append({
                "id": fid(), "kat": "bahn",
        "sw":     "?",
                "stadt": referenz, "bl": ref_stadt["bundesland"],
                "frage": (f"Du fährst mit dem ICE von {halte[0]} nach {halte[-1]}. "
                          f"Welche Stadt kommt nach {referenz}?"),
                "richtig": naechster,
                "falsch": falsch3,
                "erkl": (f"Auf der Strecke {strecke_name} folgt nach {referenz} "
                         f"der Halt {naechster}.")
            })

    # ── Typ 5: Bahnhofskategorie direkt ───────────────────────────────────
    kat_labels = {
        1: "Kategorie 1 (Großstadtknoten)",
        2: "Kategorie 2 (Fernverkehr)",
        3: "Kategorie 3 (Regionalzentrum)",
        4: "Kategorie 4 (Regionalbahnhof)",
        5: "Kategorie 5 (kleiner Bahnhof)",
    }
    random.shuffle(STAEDTE)
    for stadt in STAEDTE[:25]:
        bk = BK.get(stadt["name"])
        if not bk or not bk.get("kategorie"): continue
        kat = bk["kategorie"]
        richtig_label = kat_labels.get(kat)
        if not richtig_label: continue
        falsch_labels = [v for k, v in kat_labels.items() if k != kat]
        falsch3 = random.sample(falsch_labels, 3)
        fragen.append({
            "id": fid(), "kat": "bahn",
        "sw":     "?",
            "stadt": stadt["name"], "bl": stadt["bundesland"],
            "frage": f"Welche Bahnhofskategorie hat {bk['bahnhof_name']}?",
            "richtig": richtig_label,
            "falsch": falsch3,
            "erkl": (f"{bk['bahnhof_name']} ist ein Bahnhof der {richtig_label}. "
                     f"{'Fernverkehr inklusive ICE.' if bk['ice_halt'] else 'Kein Fernverkehrshalt.'}")
        })

else:
    print("ℹ️   bahnhof.json nicht gefunden — bahn-Fragen übersprungen.")
    print("    Bitte zuerst: python fetch_bahnhof.py")


# ══════════════════════════════════════════════════════════════════════════
# KATEGORIE: gesch — Geschichte (aus geschichte.json)
# ══════════════════════════════════════════════════════════════════════════

import os
GESCH_FILE = args.staedte.replace("staedte.json", "geschichte.json")
if not os.path.exists(GESCH_FILE):
    GESCH_FILE = "geschichte.json"

if os.path.exists(GESCH_FILE):
    with open(GESCH_FILE, encoding="utf-8") as f:
        GESCHICHTE = json.load(f)

    # Nur Städte mit bekanntem Jahr
    hist_staedte = [
        s for s in STAEDTE
        if GESCHICHTE.get(s["name"], {}).get("jahr")
    ]

    # Typ 1: Welche Stadt wurde früher gegründet? (4 Städte)
    random.shuffle(hist_staedte)
    for i in range(0, len(hist_staedte) - 3, 2):
        gruppe = hist_staedte[i:i+4]
        if len(gruppe) < 4:
            continue
        aelteste = min(gruppe, key=lambda s: GESCHICHTE[s["name"]]["jahr"])
        falsch   = [s["name"] for s in gruppe if s["name"] != aelteste["name"]]
        jahr     = GESCHICHTE[aelteste["name"]]["jahr"]
        fragen.append({
            "id": fid(),
            "kat": "gesch",
        "sw":     "?",
            "stadt": aelteste["name"],
            "bl": aelteste["bundesland"],
            "frage": "Welche dieser Städte hat die längste Geschichte?",
            "richtig": aelteste["name"],
            "falsch": falsch,
            "erkl": f"{aelteste['name']} wurde bereits {jahr} erstmals urkundlich erwähnt."
        })

    # Typ 2: Direktvergleich zwei Städte — wer ist älter?
    hist_paare = list(combinations(hist_staedte, 2))
    random.shuffle(hist_paare)
    for a, b in hist_paare[:40]:
        ja = GESCHICHTE[a["name"]]["jahr"]
        jb = GESCHICHTE[b["name"]]["jahr"]
        if abs(ja - jb) < 50:
            continue  # zu knapp — überspringen
        aelter   = a if ja < jb else b
        juenger  = b if aelter == a else a
        ja2 = GESCHICHTE[aelter["name"]]["jahr"]
        jb2 = GESCHICHTE[juenger["name"]]["jahr"]
        # 3 falsche: andere Städte mit bekanntem Jahr
        falsch_pool = [s["name"] for s in hist_staedte
                       if s["name"] not in (a["name"], b["name"])]
        falsch = random.sample(falsch_pool, min(3, len(falsch_pool)))
        if len(falsch) < 3:
            continue
        fragen.append({
            "id": fid(),
            "kat": "gesch",
        "sw":     "?",
            "stadt": aelter["name"],
            "bl": aelter["bundesland"],
            "frage": f"Welche Stadt ist älter — {a['name']} oder {b['name']}?",
            "richtig": aelter["name"],
            "falsch": [juenger["name"]] + falsch[:2],
            "erkl": (f"{aelter['name']} wurde {ja2} erstmals erwähnt, "
                     f"{juenger['name']} erst {jb2} — "
                     f"ein Unterschied von {jb2 - ja2} Jahren.")
        })

    # Typ 3: Zeitepoche — aus welchem Jahrhundert stammt diese Stadt?
    epochen = {
        (0,   500):  "der Römerzeit (vor 500)",
        (500, 900):  "dem Frühmittelalter (500–900)",
        (900, 1200): "dem Hochmittelalter (900–1200)",
        (1200,1500): "dem Spätmittelalter (1200–1500)",
        (1500,1800): "der Frühen Neuzeit (1500–1800)",
        (1800,2000): "der Neuzeit (nach 1800)",
    }
    def epoche(jahr):
        for (von, bis), label in epochen.items():
            if von <= jahr < bis:
                return label
        return None

    for stadt in hist_staedte:
        jahr = GESCHICHTE[stadt["name"]]["jahr"]
        ep   = epoche(jahr)
        if not ep:
            continue
        alle_epochen = list(epochen.values())
        falsch_ep = random.sample([e for e in alle_epochen if e != ep], 3)
        fragen.append({
            "id": fid(),
            "kat": "gesch",
        "sw":     "?",
            "stadt": stadt["name"],
            "bl": stadt["bundesland"],
            "frage": f"Aus welcher Epoche stammt {stadt['name']} (erste Erwähnung {jahr})?",
            "richtig": ep,
            "falsch": falsch_ep,
            "erkl": f"{stadt['name']} wurde {jahr} erstmals erwähnt — das ist {ep}."
        })

else:
    print("ℹ️   geschichte.json nicht gefunden — gesch-Fragen übersprungen.")
    print("    Bitte zuerst: python fetch_wikidata.py")


# ══════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════
# Ausgabe — pro Kategorie UND Schwierigkeitsstufe begrenzen
# ══════════════════════════════════════════════════════════════════════════

MAX_PRO_KAT_SW = {"L": 30, "M": 50, "S": 50}
MAX_HOEHE_SW   = {"L": 30, "M": 56, "S": 56}

from collections import defaultdict

# sw nachträglich normieren (ew/bahn/gesch haben keine direkte stadt-Variable)
ew_lookup = {s["name"]: sw_stufe(s) for s in STAEDTE}
for fq in fragen:
    if fq.get("sw") not in ("L", "M", "S"):
        fq["sw"] = ew_lookup.get(fq.get("stadt", ""), "S")

# Gruppieren nach kat + sw
nach_kat_sw = defaultdict(list)
for fq in fragen:
    nach_kat_sw[(fq["kat"], fq["sw"])].append(fq)

# Fehlende M/S-Stufen mit L-Fragen auffüllen (bahn/gesch haben kaum M/S-Daten)
MIN_PRO_STUFE = 20
for kat in set(fq["kat"] for fq in fragen):
    l_fragen = nach_kat_sw.get((kat, "L"), [])
    for sw in ("M", "S"):
        vorh = len(nach_kat_sw.get((kat, sw), []))
        if vorh < MIN_PRO_STUFE and l_fragen:
            import copy as _copy
            fehlend = MIN_PRO_STUFE - vorh
            ergaenzung = [_copy.copy(fq) for fq in random.sample(
                l_fragen, min(fehlend, len(l_fragen)))]
            for fq in ergaenzung:
                fq["sw"] = sw
            nach_kat_sw[(kat, sw)].extend(ergaenzung)

fragen_final = []
for (kat, sw), pool in nach_kat_sw.items():
    prio = [fq for fq in pool if "steigt" in fq["frage"] or "fällt" in fq["frage"]]
    rest = [fq for fq in pool if fq not in prio]
    random.shuffle(rest)
    pool_sorted = prio + rest
    gesehen = set()
    pool_dedup = []
    for fq in pool_sorted:
        key = fq["frage"][:80]
        if key not in gesehen:
            gesehen.add(key)
            pool_dedup.append(fq)
    limit_map = MAX_HOEHE_SW if kat == "hoehe" else MAX_PRO_KAT_SW
    fragen_final.extend(pool_dedup[:limit_map.get(sw, 50)])

random.shuffle(fragen_final)

for i, fq in enumerate(fragen_final):
    fq["id"] = f"q{i+1:04d}"

with open(args.out, "w", encoding="utf-8") as f:
    json.dump(fragen_final, f, ensure_ascii=False, indent=2)

from collections import Counter
kat_sw_count = Counter((fq["kat"], fq.get("sw","S")) for fq in fragen_final)
print(f"✅  {len(fragen_final)} Fragen generiert → {args.out}")
print()
print(f"   {'Kat':<8} {'L':>5} {'M':>5} {'S':>5} {'Σ':>6}")
print(f"   {'-'*30}")
for kat in sorted({k for k,_ in kat_sw_count}):
    l = kat_sw_count.get((kat,"L"),0)
    m = kat_sw_count.get((kat,"M"),0)
    s = kat_sw_count.get((kat,"S"),0)
    warn = " ⚠️" if l < 20 or m < 20 else ""
    print(f"   {kat:<8} {l:>5} {m:>5} {s:>5} {l+m+s:>6}{warn}")
print()
print(f"   Pool-Größen: L={len(POOL_L)} Städte (≥{EW_GRENZE_L//1000}k EW), "
      f"M={len(POOL_M)} Städte (≥{EW_GRENZE_M//1000}k EW), S={len(POOL_S)} Städte")
