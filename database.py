import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT DEFAULT 'vidutinis',
                deadline TEXT,
                category TEXT,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        try:
            conn.execute("ALTER TABLE tasks ADD COLUMN notes TEXT")
        except Exception:
            pass


def add_task(title: str, priority: str = "vidutinis", deadline: str = None, category: str = None, notes: str = None) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, priority, deadline, category, notes) VALUES (?, ?, ?, ?, ?)",
            (title, priority, deadline, category, notes),
        )
        return cur.lastrowid


def get_tasks(show_done: bool = False) -> list:
    with get_conn() as conn:
        priority_order = "CASE priority WHEN 'aukštas' THEN 1 WHEN 'vidutinis' THEN 2 WHEN 'žemas' THEN 3 ELSE 4 END"
        if show_done:
            rows = conn.execute(f"SELECT * FROM tasks ORDER BY done, {priority_order}, deadline").fetchall()
        else:
            rows = conn.execute(
                f"SELECT * FROM tasks WHERE done = 0 ORDER BY {priority_order}, deadline"
            ).fetchall()
        return [dict(r) for r in rows]


def complete_task(task_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ? AND done = 0", (task_id,))
        return cur.rowcount > 0


def delete_task(task_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cur.rowcount > 0


def update_task(task_id: int, **kwargs) -> bool:
    allowed = {"title", "priority", "deadline", "category", "notes"}
    fields = {k: v for k, v in kwargs.items() if k in allowed}
    if not fields:
        return False
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    with get_conn() as conn:
        cur = conn.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = ?",
            (*fields.values(), task_id),
        )
        return cur.rowcount > 0
