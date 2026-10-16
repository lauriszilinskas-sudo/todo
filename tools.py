from database import add_task, get_tasks, complete_task, delete_task, update_task

TOOLS = [
    {
        "name": "add_task",
        "description": "Pridėti naują užduotį į sąrašą",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Užduoties pavadinimas"},
                "priority": {
                    "type": "string",
                    "enum": ["aukštas", "vidutinis", "žemas"],
                    "description": "Prioritetas",
                },
                "deadline": {"type": "string", "description": "Terminas YYYY-MM-DD formatu"},
                "category": {"type": "string", "description": "Kategorija, pvz. darbas, asmeninis"},
            },
            "required": ["title"],
        },
    },
    {
        "name": "list_tasks",
        "description": "Rodyti užduočių sąrašą",
        "input_schema": {
            "type": "object",
            "properties": {
                "show_done": {"type": "boolean", "description": "Rodyti ir atliktas užduotis"},
            },
        },
    },
    {
        "name": "complete_task",
        "description": "Pažymėti užduotį kaip atliktą",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Užduoties ID numeris"},
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "delete_task",
        "description": "Ištrinti užduotį",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Užduoties ID numeris"},
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "update_task",
        "description": "Atnaujinti užduoties informaciją",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Užduoties ID numeris"},
                "title": {"type": "string", "description": "Naujas pavadinimas"},
                "priority": {"type": "string", "enum": ["aukštas", "vidutinis", "žemas"]},
                "deadline": {"type": "string", "description": "Terminas YYYY-MM-DD formatu"},
                "category": {"type": "string"},
            },
            "required": ["task_id"],
        },
    },
]


def run_tool(name: str, inputs: dict) -> str:
    if name == "add_task":
        task_id = add_task(**inputs)
        return f"✅ Užduotis sukurta (ID: {task_id}): {inputs['title']}"

    elif name == "list_tasks":
        tasks = get_tasks(show_done=inputs.get("show_done", False))
        if not tasks:
            return "📭 Užduočių sąrašas tuščias."
        lines = []
        for t in tasks:
            status = "✅" if t["done"] else _priority_icon(t["priority"])
            deadline = f" | ⏰ {t['deadline']}" if t["deadline"] else ""
            category = f" | 📁 {t['category']}" if t["category"] else ""
            lines.append(f"[{t['id']}] {status} {t['title']}{deadline}{category}")
        return "\n".join(lines)

    elif name == "complete_task":
        ok = complete_task(inputs["task_id"])
        return f"✅ Atlikta!" if ok else f"⚠️ Užduotis ID {inputs['task_id']} nerasta arba jau atlikta."

    elif name == "delete_task":
        ok = delete_task(inputs["task_id"])
        return f"🗑️ Ištrinta." if ok else f"⚠️ Užduotis ID {inputs['task_id']} nerasta."

    elif name == "update_task":
        ok = update_task(**inputs)
        return f"📝 Atnaujinta." if ok else f"⚠️ Nepavyko atnaujinti."

    return f"⚠️ Nežinomas įrankis: {name}"


def _priority_icon(priority: str) -> str:
    return {"aukštas": "🔴", "vidutinis": "🟡", "žemas": "🟢"}.get(priority, "⚪")
