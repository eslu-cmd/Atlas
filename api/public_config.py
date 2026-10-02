"""GET /api/public-config — expose public Supabase URL + anon key to the browser.

Both are explicitly public (anon key is designed to be shipped to clients and is
gated by RLS). This endpoint lets the frontend attempt the unauthorized-write
rejection test without hardcoding the project URL.
"""
from __future__ import annotations

import os
from typing import Any

from _lib import JsonHandler


class handler(JsonHandler):  # noqa: N801
    def handle_get(self) -> tuple[int, dict[str, Any]]:
        return 200, {
            "SUPABASE_URL": os.environ.get("SUPABASE_URL", ""),
            "SUPABASE_ANON_KEY": os.environ.get("SUPABASE_ANON_KEY", ""),
        }
