# Startet nacht-2026-10-06.sh losgelöst (überlebt das Ende der Claude-Session) und hält den PC wach, bis das Log „Fertig“ meldet.
param([string]$Orte = "", [string]$Name = "nacht-2026-10-06")
$log = "D:\claude-code\LernApp\data\gemeinde-achsen\bahn\$Name.log"
Start-Process -FilePath "D:\Programme\Git\usr\bin\bash.exe" -ArgumentList "-c","'export PATH=/usr/bin:`$PATH; /usr/bin/bash /d/claude-code/LernApp/data/gemeinde-achsen/bahn/nacht-2026-10-06.sh $Orte > /d/claude-code/LernApp/data/gemeinde-achsen/bahn/$Name.log 2>&1'" -WindowStyle Hidden
Start-Process -FilePath "python" -ArgumentList "-X","utf8","D:\claude-code\projekte\omr\pipeline\wachhalten.py",$log,"--max-minuten","240" -WindowStyle Hidden
Write-Output "Nachtlauf gestartet, Log: $log"
