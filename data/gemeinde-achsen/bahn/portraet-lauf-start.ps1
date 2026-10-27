# Startet portraet-lauf.sh losgelöst (überlebt das Ende der Claude-Session) und hält den PC wach, bis das Log „Fertig“ meldet.
# -Skript vertiefung-lauf.sh: Vertiefung Freiburg (2026-10-27)
param([string]$Orte = "", [string]$Name = "portraet-lauf", [string]$Skript = "portraet-lauf.sh")
$log = "D:\claude-code\LernApp\data\gemeinde-achsen\bahn\$Name.log"
Start-Process -FilePath "D:\Programme\Git\usr\bin\bash.exe" -ArgumentList "-c","'export PATH=/usr/bin:`$PATH; /usr/bin/bash /d/claude-code/LernApp/data/gemeinde-achsen/bahn/$Skript $Orte > /d/claude-code/LernApp/data/gemeinde-achsen/bahn/$Name.log 2>&1'" -WindowStyle Hidden
Start-Process -FilePath "python" -ArgumentList "-X","utf8","D:\claude-code\projekte\omr\pipeline\wachhalten.py",$log,"--max-minuten","180" -WindowStyle Hidden
Write-Output "Ortsporträt-Lauf gestartet, Log: $log"
