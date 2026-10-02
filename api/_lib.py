"""Shared helpers for Vercel Python serverless handlers."""
from __future__ import annotations

import json
import pathlib
import sys
import traceback
from http.server import BaseHTTPRequestHandler
from typing import Any


# Make the sibling `service/` package importable from each api/*.py handler.
_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


class JsonHandler(BaseHTTPRequestHandler):
    """BaseHTTPRequestHandler subclass that encodes JSON responses and parses JSON bodies."""

    def _write(self, status: int, body: dict[str, Any]) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON body: {exc}") from exc
        if not isinstance(parsed, dict):
            raise ValueError("JSON body must be an object")
        return parsed

    def do_OPTIONS(self) -> None:  # noqa: N802  (BaseHTTPRequestHandler API)
        self._write(204, {})

    # Subclasses implement handle_get / handle_post.
    def handle_get(self) -> tuple[int, dict[str, Any]]:
        return 405, {"error": "method not allowed"}

    def handle_post(self, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        return 405, {"error": "method not allowed"}

    def do_GET(self) -> None:  # noqa: N802
        try:
            status, body = self.handle_get()
        except Exception as exc:  # noqa: BLE001
            status, body = 500, {"error": str(exc), "trace": traceback.format_exc()}
        self._write(status, body)

    def do_POST(self) -> None:  # noqa: N802
        try:
            body = self._read_json()
        except ValueError as exc:
            self._write(400, {"error": str(exc)})
            return
        try:
            status, response = self.handle_post(body)
        except Exception as exc:  # noqa: BLE001
            status, response = 500, {"error": str(exc), "trace": traceback.format_exc()}
        self._write(status, response)
