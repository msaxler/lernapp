"""QuizAway Reise-Prototyp: Fassung für die Veröffentlichung als Artifact bauen.

Die Artifact-Seite bekommt Doctype, html/head/body beim Veröffentlichen; title und style stehen oben in der Datei.
Dieses Skript nimmt apps/quizaway-reise/index.html (lokal lauffähig, mit eigenem Rahmen) und schreibt
apps/quizaway-reise/artifact/quizaway-reise.html ohne den Rahmen. daten.js wird daneben mitveröffentlicht.

Aufruf:  python -X utf8 scripts/data-build/quizaway_prototyp_export.py
         python -X utf8 scripts/data-build/quizaway_prototyp_artifact.py
"""
import io
import os
import re
import shutil

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP = os.path.join(WURZEL, 'apps', 'quizaway-reise')
AUS = os.path.join(APP, 'artifact')


def main():
    with io.open(os.path.join(APP, 'index.html'), encoding='utf-8') as f:
        s = f.read()
    titel = re.search(r'<title>.*?</title>', s).group(0)
    kopf = re.search(r'<head>(.*?)</head>', s, flags=re.S).group(1)
    kopf = re.sub(r'\s*<meta[^>]*>', '', kopf).replace(titel, '').strip()
    rumpf = re.search(r'<body>(.*?)</body>', s, flags=re.S).group(1).strip()
    os.makedirs(AUS, exist_ok=True)
    with io.open(os.path.join(AUS, 'quizaway-reise.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(titel + '\n' + kopf + '\n' + rumpf + '\n')
    shutil.copyfile(os.path.join(APP, 'daten.js'), os.path.join(AUS, 'daten.js'))
    print('geschrieben:', os.path.join(AUS, 'quizaway-reise.html'))


if __name__ == '__main__':
    main()
