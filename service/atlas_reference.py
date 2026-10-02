"""Import shim for the preserved atlas-step4c-0.3.1 package.

Keeps the reference package pristine (no edits, no setup.py) while making
`from atlas import Engine` work from the production service and api layers.
"""
from __future__ import annotations

import pathlib
import sys

REFERENCE_ROOT = pathlib.Path(__file__).resolve().parent.parent / "reference" / "atlas-step4c-0.3.1"

if str(REFERENCE_ROOT) not in sys.path:
    sys.path.insert(0, str(REFERENCE_ROOT))

DICTIONARY_PATH = REFERENCE_ROOT / "dictionary" / "atlas-A1-0.1.0.json"
KNOWN_ANSWERS_PATH = REFERENCE_ROOT / "fixtures" / "engine-known-answers-0.1.1.json"

BASELINE_VERSIONS = {
    "workflow": "0.3.1",
    "records": "0.2.1",
    "engine": "0.1.1",
    "dictionary": "A1 / 0.1.0-local-candidate",
}


def engine():
    """Return a fresh Engine bound to the preserved dictionary."""
    from atlas import Engine  # noqa: E402  -- import after path setup

    return Engine(DICTIONARY_PATH)
