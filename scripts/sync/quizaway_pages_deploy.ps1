# QuizAway Reise-Prototyp nach Cloudflare Pages (https://quizaway.pages.dev) – die Adresse für die echte Fahrt.
# Grund (2026-10-19): Der Artifact-Dienst bettet die Seite in einen iframe ohne geolocation ein; GPS geht dort nie.
# Nur die drei Dateien, ohne das artifact/-Duplikat. Läuft in Mikes PowerShell (wrangler-Login liegt dort;
# nach Ablauf: npx wrangler@latest login). Aufruf:  .\scripts\sync\quizaway_pages_deploy.ps1
$quelle = Join-Path $PSScriptRoot "..\..\apps\quizaway-reise"
$ziel = Join-Path $env:TEMP "quizaway-pages"
if (Test-Path $ziel) { Remove-Item -Recurse -Force $ziel }
New-Item -ItemType Directory -Force $ziel | Out-Null
foreach ($f in "index.html", "daten.js", "grund-de.js") { Copy-Item (Join-Path $quelle $f) $ziel }
npx wrangler@latest pages deploy $ziel --project-name quizaway --branch main --commit-dirty=true
