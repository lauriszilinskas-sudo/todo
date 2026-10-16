# SmartTask — Rizikos Cesija To-Do

Lengvas užduočių valdymo įrankis su kalendoriaus rodinio sąsaja. Sukurtas naudojant tik Python standartinę biblioteką — nereikia pip install.

![Python](https://img.shields.io/badge/Python-3.13-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![No dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

---

## Funkcijos

- **Kalendoriaus rodinys** — mėnesinis kalendorius kairėje, dienos užduotys dešinėje
- **Prioritetai** — 🔴 Aukštas / 🟡 Vidutinis / 🟢 Žemas su spalvotais taškeliais kalendoriuje
- **Paieška** — realaus laiko filtravimas pagal pavadinimą ir kategoriją
- **Pastabos** — papildoma informacija prie kiekvienos užduoties
- **Inline redagavimas** — spustelėti pavadinimą ir redaguoti vietoje
- **Užduotys be datos** — inbox principas, „Be datos" skyrius
- **Savaitinė statistika** — 7 dienų grafikas ir prioritetų suvestinė
- **Mobilusis rodinys** — prisitaikantis dizainas iki 700px
- **Rizikos Cesija spalvos** — žalia `#143D34`, aukso `#CBA052`, tamsiai mėlyna `#19395B`

---

## Paleidimas

**Reikalavimai:** Python 3.10+

```bash
python server.py
```

Atidaryti naršyklėje: [http://localhost:8080](http://localhost:8080)

Sustabdyti: `Ctrl+C`

---

## Struktūra

```
todo-agent/
├── server.py          # HTTP serveris (stdlib: http.server)
├── database.py        # SQLite CRUD operacijos
├── agent.py           # CLI REPL (alternatyva web UI)
├── tools.py           # Įrankių dispečeris (agent loopui)
├── static/
│   └── index.html     # Vienalapis SPA (vanilla JS + CSS)
├── BEST_PRACTICES.md  # To-do programų geriausios praktikos 2026
└── requirements.txt   # Tuščias — naudojama tik stdlib
```

---

## API

| Metodas | Kelias | Aprašas |
|---------|--------|---------|
| `GET` | `/api/tasks` | Gauti aktyvias užduotis |
| `GET` | `/api/tasks?all` | Gauti visas užduotis (įskaitant atliktas) |
| `POST` | `/api/tasks` | Sukurti užduotį |
| `PATCH` | `/api/tasks/<id>` | Atnaujinti užduotį |
| `POST` | `/api/tasks/<id>/done` | Pažymėti kaip atliktą |
| `DELETE` | `/api/tasks/<id>` | Ištrinti užduotį |

**POST /api/tasks body:**
```json
{
  "title": "Užduoties pavadinimas",
  "priority": "aukštas | vidutinis | žemas",
  "deadline": "2026-10-20",
  "category": "Darbas",
  "notes": "Papildoma informacija"
}
```

---

## CLI naudojimas

```bash
python agent.py
```

```
> add Paskambinti klientui --p aukštas --d 2026-10-20 --c Darbas
> list
> done 1
> delete 2
> help
```

---

## Duomenų bazė

SQLite failas `tasks.db` kuriamas automatiškai pirmojo paleidimo metu.

```sql
CREATE TABLE tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    priority   TEXT DEFAULT 'vidutinis',
    deadline   TEXT,
    category   TEXT,
    notes      TEXT,
    done       INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
)
```

---

## Technologijos

- **Backend:** Python 3.13, `http.server`, `sqlite3`, `json`, `urllib.parse`
- **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3
- **Duomenų bazė:** SQLite
- **Priklausomybės:** nėra

---

*Rizikos Cesija, UAB — 2026*
