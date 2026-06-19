from __future__ import annotations

import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4


HOST = "127.0.0.1"
PORT = 8000
APPLICATIONS_PATH = Path(__file__).with_name("registration_applications.json")


def read_applications() -> list[dict[str, str]]:
    if not APPLICATIONS_PATH.exists():
        return []

    try:
        data = json.loads(APPLICATIONS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        return data
    return []


def write_applications(applications: list[dict[str, str]]) -> None:
    APPLICATIONS_PATH.write_text(
        json.dumps(applications, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


class RegistrationRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        if self.path != "/api/registration-applications":
            self.respond_json({"detail": "Not found"}, status=404)
            return

        self.respond_json({"applications": read_applications()})

    def do_POST(self) -> None:
        if self.path != "/api/registration-applications":
            self.respond_json({"detail": "Not found"}, status=404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self.respond_json({"detail": "Invalid JSON"}, status=400)
            return

        name = str(payload.get("name", "")).strip()
        email = str(payload.get("email", "")).strip()

        if len(name) < 2 or "@" not in email:
            self.respond_json({"detail": "Invalid name or email"}, status=422)
            return

        application = {
            "unique_id": str(uuid4()),
            "name": name,
            "email": email,
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        applications = read_applications()
        applications.append(application)
        write_applications(applications)
        self.respond_json(application)

    def respond_json(self, payload: dict | list, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), RegistrationRequestHandler)
    print(f"Registration server is running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
