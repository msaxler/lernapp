#!/usr/bin/env python3
"""
patch_generate_kfz.py — Verbessert KFZ-Erklärungen in generate_questions.py.
Fügt KFZ→Zulassungsbereich-Tabelle ein und passt erkl-Texte an.
Aufruf: py -3.11 patch_generate_kfz.py
"""
import sys
from pathlib import Path

GQ = Path("generate_questions.py")
if not GQ.exists():
    print(f"FEHLER: {GQ} nicht gefunden"); sys.exit(1)

c = GQ.read_text(encoding='utf-8')

# Prüfen ob bereits gepatcht
if 'KFZ_KREISSTADT' in c:
    print("Bereits gepatcht."); sys.exit(0)

# ── Die Tabelle ─────────────────────────────────────────────
# KFZ-Kennzeichen → offizieller Zulassungsbereich (Kreisstadt oder Kreis)
# Nur Einträge wo Zulassungsbereich ≠ naheliegender Stadtname
# (Städte die selbst der Namenspatron sind, stehen nicht drin)
KFZ_TABLE = '''
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
'''

# Einfügen nach den Imports / vor dem ersten Fragen-Block
# Suche nach "# KATEGORIE: kfz"
insert_before = "# KATEGORIE: kfz"
if insert_before not in c:
    print("❌ Einfügestelle nicht gefunden"); sys.exit(1)

c = c.replace(insert_before, KFZ_TABLE + "\n" + insert_before, 1)

# Patch erkl für Richtung 1: "Welches KFZ-Kennzeichen gehört zu X?"
old1 = '        "erkl": f"{kfz} ist das Kennzeichen für {name}."'
new1 = (
    '        "erkl": _kfz_erkl(kfz, name, stadt["bundesland"])'
)
c = c.replace(old1, new1, 1)

# Patch erkl für Richtung 2: "Für welche Stadt steht das Kennzeichen X?"
old2 = '        "erkl": f"\\u201e{kfz}\\u201c steht für {name} in {stadt[\'bundesland\']}."'
new2 = (
    '        "erkl": _kfz_erkl2(kfz, name, stadt["bundesland"])'
)
c = c.replace(old2, new2, 1)

# Hilfsfunktionen einfügen (direkt vor "# KATEGORIE: kfz")
helper = '''
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
        return (f"\u201e{kfz}\u201c steht für den Zulassungsbereich {bereich}. "
                f"{stadtname} liegt in diesem Bereich ({bundesland}).")
    return f"\u201e{kfz}\u201c steht für {stadtname} in {bundesland}."

'''
c = c.replace("# KATEGORIE: kfz", helper + "# KATEGORIE: kfz", 1)

GQ.write_text(c, encoding='utf-8')
print("✅ generate_questions.py gepatcht.")
print("   Jetzt ausführen:")
print("   py -3.11 generate_questions.py")
print("   py -3.11 inject_questions.py")
print("   py -3.11 check_quiz.py")
