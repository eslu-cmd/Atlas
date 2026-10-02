"""POST /api/txn-proof — demonstrate transactional guarantees.

Body: {idempotency_key, payload, actor, reason, mode?}
  mode: "write" (default), "rollback", "retry"

- write: insert and commit. Row must be visible on subsequent GET.
- rollback: insert then roll back. Row must NOT exist after.
- retry: write-then-write with the same idempotency_key + payload. Second call
  returns `repeated` with the original row.

GET /api/txn-proof?key=<idempotency_key> → whether that key has a committed row.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlparse

from _lib import JsonHandler
from service import db


REQUIRED = ("idempotency_key", "payload", "actor", "reason")


class handler(JsonHandler):  # noqa: N801
    def handle_get(self) -> tuple[int, dict[str, Any]]:
        qs = parse_qs(urlparse(self.path).query)
        key = (qs.get("key") or [None])[0]
        if not key:
            return 400, {"error": "missing ?key=<idempotency_key>"}
        exists = db.row_exists(key)
        return 200, {"idempotency_key": key, "exists": exists}

    def handle_post(self, body: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        missing = [k for k in REQUIRED if body.get(k) in (None, "")]
        if missing:
            return 400, {"error": "missing fields", "missing": missing}

        mode = body.get("mode", "write")
        kwargs = {
            "idempotency_key": body["idempotency_key"],
            "payload": body["payload"],
            "actor": body["actor"],
            "reason": body["reason"],
        }

        if mode == "rollback":
            result = db.write_proof(**kwargs, force_rollback=True)
            exists = db.row_exists(body["idempotency_key"])
            result["durable_after_rollback"] = exists
            return 200, result

        if mode == "retry":
            first = db.write_proof(**kwargs)
            second = db.write_proof(**kwargs)
            return 200, {"first": first, "second": second}

        if mode == "write":
            return 200, db.write_proof(**kwargs)

        return 400, {"error": f"unknown mode '{mode}'"}
