from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ALLOCATED_MEMORY: bytearray | None = None


def parse_memory_mb(raw: str | None) -> int:
    if raw is None or raw.strip() == "":
        return 0
    value = int(raw)
    if value < 0:
        raise ValueError("memory allocation must be non-negative")
    return value


def allocate_memory(memory_mb: int) -> bytearray | None:
    if memory_mb == 0:
        return None
    return bytearray(memory_mb * 1024 * 1024)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path in {"/healthz", "/readyz"}:
            self._send_json(200, {"status": "ok"})
            return
        if self.path == "/memory":
            self._send_json(
                200,
                {
                    "allocated_mb": parse_memory_mb(os.getenv("MEMORY_ALLOC_MB")),
                    "pid": os.getpid(),
                },
            )
            return
        self._send_json(404, {"error": "not found"})

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    global ALLOCATED_MEMORY
    port = int(os.getenv("PORT", "8080"))
    ALLOCATED_MEMORY = allocate_memory(parse_memory_mb(os.getenv("MEMORY_ALLOC_MB")))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
