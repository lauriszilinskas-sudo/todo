from database import init_db, add_task, get_tasks, complete_task, delete_task
from tools import _priority_icon

HELP = """
Komandos:
  add <pavadinimas> [--p aukštas|vidutinis|žemas] [--d YYYY-MM-DD] [--c kategorija]
  list            — rodyti užduotis
  list all        — rodyti ir atliktas
  done <id>       — pažymėti kaip atlikta
  delete <id>     — ištrinti
  help            — pagalba
  quit            — išeiti
"""


def parse_add(parts: list) -> dict:
    kwargs = {}
    title_parts = []
    i = 0
    while i < len(parts):
        if parts[i] == "--p" and i + 1 < len(parts):
            kwargs["priority"] = parts[i + 1]; i += 2
        elif parts[i] == "--d" and i + 1 < len(parts):
            kwargs["deadline"] = parts[i + 1]; i += 2
        elif parts[i] == "--c" and i + 1 < len(parts):
            kwargs["category"] = parts[i + 1]; i += 2
        else:
            title_parts.append(parts[i]); i += 1
    kwargs["title"] = " ".join(title_parts)
    return kwargs


def print_tasks(show_done=False):
    tasks = get_tasks(show_done=show_done)
    if not tasks:
        print("  📭 Sąrašas tuščias.")
        return
    for t in tasks:
        icon = "✅" if t["done"] else _priority_icon(t["priority"])
        deadline = f"  ⏰ {t['deadline']}" if t["deadline"] else ""
        category = f"  📁 {t['category']}" if t["category"] else ""
        print(f"  [{t['id']}] {icon} {t['title']}{deadline}{category}")


def main():
    init_db()
    print("📋 SmartTask — To-Do sąrašas  (įvesk 'help' pagalbai)\n")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Viso gero!")
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ("quit", "exit", "išeiti"):
            print("👋 Viso gero!")
            break

        elif cmd == "help":
            print(HELP)

        elif cmd == "list":
            show_done = len(parts) > 1 and parts[1] == "all"
            print_tasks(show_done)

        elif cmd == "add":
            if len(parts) < 2:
                print("  ⚠️  Pvz.: add Paskambinti daktarui --p aukštas --d 2026-10-20")
                continue
            kwargs = parse_add(parts[1:])
            if not kwargs.get("title"):
                print("  ⚠️  Trūksta pavadinimo.")
                continue
            task_id = add_task(**kwargs)
            print(f"  ✅ Sukurta (ID: {task_id}): {kwargs['title']}")

        elif cmd == "done":
            if len(parts) < 2 or not parts[1].isdigit():
                print("  ⚠️  Pvz.: done 1")
                continue
            ok = complete_task(int(parts[1]))
            print("  ✅ Atlikta!" if ok else f"  ⚠️  ID {parts[1]} nerasta.")

        elif cmd == "delete":
            if len(parts) < 2 or not parts[1].isdigit():
                print("  ⚠️  Pvz.: delete 1")
                continue
            ok = delete_task(int(parts[1]))
            print("  🗑️  Ištrinta." if ok else f"  ⚠️  ID {parts[1]} nerasta.")

        else:
            print(f"  ⚠️  Nežinoma komanda: '{cmd}'. Įvesk 'help'.")


if __name__ == "__main__":
    main()
