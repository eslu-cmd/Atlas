"""POST /api/encode — run the preserved engine on an arbitrary facts payload.

Body: {"facts": {...}}  →  {"code": "A1!...", "describe": {...}}
"""
from __future__ import annotations

from typing import Any

from _lib import JsonHandler
from service.atlas_reference import engine


class handler(JsonHandler):  # noqa: N801
    def handle_post(self, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        if "facts" not in body:
            return 400, {"error": "missing 'facts' in body"}
        e = engine()
        try:
            code = e.encode(body["facts"])
        except Exception as exc:  # noqa: BLE001
            return 400, {"error": f"{type(exc).__name__}: {exc}"}
        try:
            describe = e.describe(code)
        except Exception as exc:  # noqa: BLE001
            describe = {"error": f"{type(exc).__name__}: {exc}"}
        return 200, {"code": code, "describe": describe}
