import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from database import init_db, add_task, get_tasks, complete_task, delete_task, update_task

STATIC = Path(__file__).parent / "static"
PORT = 8080


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # tylus serveris

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, ValueError):
            return None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self._serve_file(STATIC / "index.html", "text/html")
        elif parsed.path == "/api/tasks":
            show_done = "all" in parse_qs(parsed.query)
            self.send_json(get_tasks(show_done=show_done))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        data = self.read_body()
        if data is None:
            self.send_json({"error": "Blogas JSON"}, 400)
            return
        if parsed.path == "/api/tasks":
            if not data.get("title"):
                self.send_json({"error": "Trūksta pavadinimo"}, 400)
                return
            task_id = add_task(
                title=data["title"],
                priority=data.get("priority", "vidutinis"),
                deadline=data.get("deadline") or None,
                category=data.get("category") or None,
                notes=data.get("notes") or None,
            )
            self.send_json({"id": task_id})
        elif parsed.path.startswith("/api/tasks/") and parsed.path.endswith("/done"):
            try:
                task_id = int(parsed.path.split("/")[3])
            except (ValueError, IndexError):
                self.send_json({"error": "Blogas ID"}, 400)
                return
            ok = complete_task(task_id)
            self.send_json({"ok": ok})
        else:
            self.send_response(404)
            self.end_headers()

    def do_PATCH(self):
        parsed = urlparse(self.path)
        data = self.read_body()
        if data is None:
            self.send_json({"error": "Blogas JSON"}, 400)
            return
        if parsed.path.startswith("/api/tasks/"):
            try:
                task_id = int(parsed.path.split("/")[3])
            except (ValueError, IndexError):
                self.send_json({"error": "Blogas ID"}, 400)
                return
            allowed = {"title", "priority", "deadline", "category", "notes"}
            kwargs = {k: v for k, v in data.items() if k in allowed}
            ok = update_task(task_id, **kwargs)
            self.send_json({"ok": ok})
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/tasks/"):
            try:
                task_id = int(parsed.path.split("/")[3])
            except (ValueError, IndexError):
                self.send_json({"error": "Blogas ID"}, 400)
                return
            ok = delete_task(task_id)
            self.send_json({"ok": ok})
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, path: Path, content_type: str):
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)


def main():
    init_db()
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"✅ SmartTask veikia: http://localhost:{PORT}")
    print("   Spausk Ctrl+C norėdamas sustabdyti\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Serveris sustabdytas.")


if __name__ == "__main__":
    main()
