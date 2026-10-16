$env:PATH = "C:\Program Files\Git\cmd;C:\Program Files\Git\bin;" + $env:PATH
Set-Location "C:\Users\laurynas.zilinskas\OneDrive - Rizikos Cesija, Uadbb\Documents\Kodukas_claude\todo-agent"

git init
git config user.email "laurynas@rizikoscessija.lt"
git config user.name "Laurynas Zilinskas"
git remote remove origin 2>$null
git remote add origin https://github.com/lauriszilinskas-sudo/todo.git
git checkout -b main
git add .
git commit -m "Initial commit: SmartTask to-do app

- Python stdlib HTTP server (sqlite3, http.server, urllib)
- SQLite database with priority sorting (GTD-based)
- Calendar SPA: vanilla JS, Rizikos Cesija brand colors
- Search/filter, notes field, inline editing
- Weekly stats panel with 7-day chart
- Responsive mobile layout
- BEST_PRACTICES.md: GTD methodology research 2026-10-16"
git push -u origin main --force
