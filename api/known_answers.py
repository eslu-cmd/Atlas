"""GET /api/known-answers — representative preserved-engine results via the deployed service.

Returns the Document 2 worked examples re-encoded by the deployed engine plus
the result of running the full preserved engine unittest suite.
"""
from __future__ import annotations

from typing import Any

from _lib import JsonHandler
from service.known_answers import canonical_examples, run_engine_suite


class handler(JsonHandler):  # noqa: N801
    def handle_get(self) -> tuple[int, dict[str, Any]]:
        examples = canonical_examples()
        suite = run_engine_suite()
        combined_pass = examples["all_pass"] and suite["all_pass"]
        return (200 if combined_pass else 500), {
            "all_pass": combined_pass,
            "canonical_examples": examples,
            "engine_suite": suite,
        }
