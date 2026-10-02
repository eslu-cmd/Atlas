"""POST /api/dictionary-allocate — atomically allocate a dictionary token.

Body: {namespace, scope, token, meaning, actor, reason}
"""
from __future__ import annotations

from typing import Any

from _lib import JsonHandler
from service import db


REQUIRED = ("namespace", "scope", "token", "meaning", "actor", "reason")


class handler(JsonHandler):  # noqa: N801
    def handle_get(self) -> tuple[int, dict[str, Any]]:
        return 200, {"recent": db.list_tokens()}

    def handle_post(self, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        missing = [k for k in REQUIRED if not body.get(k)]
        if missing:
            return 400, {"error": "missing fields", "missing": missing}
        result = db.allocate_token(
            namespace=body["namespace"],
            scope=body["scope"],
            token=body["token"],
            meaning=body["meaning"],
            actor=body["actor"],
            reason=body["reason"],
        )
        status = 200 if result["status"] == "allocated" else 409
        return status, result
