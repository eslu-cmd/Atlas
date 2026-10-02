"""GET /api/health — baseline versions + runtime info."""
from __future__ import annotations

import os
import platform
import sys
from typing import Any

from _lib import JsonHandler
from service.atlas_reference import BASELINE_VERSIONS


class handler(JsonHandler):  # noqa: N801 — Vercel discovers lowercase `handler`
    def handle_get(self) -> tuple[int, dict[str, Any]]:
        return 200, {
            "status": "ok",
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "versions": BASELINE_VERSIONS,
            "vercel_env": os.environ.get("VERCEL_ENV", "local"),
            "has_db_url": bool(os.environ.get("SUPABASE_DB_URL")),
        }
