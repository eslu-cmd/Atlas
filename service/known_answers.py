"""Reproduce representative preserved-engine results via the production service.

Two complementary checks:

1. `canonical_examples()` — runs the Document 2 worked examples W01–W08 with
   fresh inputs and compares the deployed engine's canonical codes to the
   expected strings documented in `reference/.../Step-3.md`. This is the
   explicit, auditable "representative known-answer results" check.

2. `run_engine_suite()` — invokes the preserved `test_engine.EngineTests`
   unittest suite programmatically and reports counts. This matches what the
   full baseline runner does for the 47 engine tests.

The 44-entry `engine-known-answers-0.1.1.json` fixture captures (test, input,
expected, actual) tuples at each assertion. Because several engine tests mutate
the input dict in place between assertions, re-encoding a captured `input`
cannot by itself reproduce the paired `expected`/`actual`. The lossy capture is
why we prefer explicit canonical examples here and the full unittest suite for
drift detection.
"""
from __future__ import annotations

import io
import unittest
from typing import Any

from . import atlas_reference


def _node(fields: dict[str, Any], groups=None) -> dict[str, Any]:
    out = {"fields": fields}
    if groups is not None:
        out["groups"] = groups
    return out


# Document 2 worked examples W01–W08 — explicit canonical codes.
CANONICAL_EXAMPLES: list[dict[str, Any]] = [
    {
        "id": "W01a",
        "description": "PET cup body, 500 mL, rim 98 mm (9.8 cm)",
        "input": _node({"MA": "APTX", "AR": "CUB", "CA": {"value": "0.5", "unit": "L"}, "FI": {"value": "9.8", "unit": "cm"}}),
        "expected": "A1!APTX.CUB.XXX.M500.R98",
    },
    {
        "id": "W01b",
        "description": "Same cup, rim stated more precisely as 98.125 mm",
        "input": _node({"MA": "APTX", "AR": "CUB", "CA": {"value": "0.5", "unit": "L"}, "FI": {"value": "98.125", "unit": "mm"}}),
        "expected": "A1!APTX.CUB.XXX.M500.R98_125",
    },
    {
        "id": "W02",
        "description": "PP cup body, 500 mL, no printing on base spec",
        "input": _node({"MA": "APPX", "AR": "CUB", "CA": "M500"}),
        "expected": "A1!APPX.CUB.XXX.M500.X",
    },
    {
        "id": "W04-inside-white",
        "description": "Kraft bag with twisted handle, white interior",
        "input": _node({"MA": "BKRX", "AR": "BGX", "CF": "XXT"}, [{"scope": "INSIDE", "node": _node({"MA": "BKRX", "CL": "WHITE"})}]),
        "expected": "A1!BKRX.BGX.XXT.X.X~S(INSIDE){CL:WHITE.MA:BKRX}",
    },
    {
        "id": "W04-layers-outside-in",
        "description": "Kraft/PET laminate, outside-to-inside",
        "input": _node({"MA": "BKRX", "AR": "BGX", "CF": "XLX"}, [{"direction": "O", "layers": [_node({"MA": "BKRX"}), _node({"MA": "APTX"})]}]),
        "expected": "A1!BKRX.BGX.XLX.X.X~L(O){MA:BKRX;MA:APTX}",
    },
    {
        "id": "W05-before",
        "description": "White bleached kraft cup, treatment unknown",
        "input": _node({"MA": "BKWX", "AR": "CUB", "CA": "M500"}),
        "expected": "A1!BKWX.CUB.XXX.M500.X",
    },
    {
        "id": "W05-after",
        "description": "Same cup after learning one-sided PE coating",
        "input": _node({"MA": "BKWP", "AR": "CUB", "CA": "M500"}),
        "expected": "A1!BKWP.CUB.XXX.M500.X",
    },
    {
        "id": "W07-spoon",
        "description": "CPLA spoon component",
        "input": _node({"MA": "ACPX", "AR": "CYX", "CF": "XXS"}),
        "expected": "A1!ACPX.CYX.XXS.X.X",
    },
    {
        "id": "W07-fork",
        "description": "CPLA fork component",
        "input": _node({"MA": "ACPX", "AR": "CYX", "CF": "XXF"}),
        "expected": "A1!ACPX.CYX.XXF.X.X",
    },
    {
        "id": "W07-knife",
        "description": "CPLA knife component",
        "input": _node({"MA": "ACPX", "AR": "CYX", "CF": "XXN"}),
        "expected": "A1!ACPX.CYX.XXN.X.X",
    },
    {
        "id": "W07-napkin",
        "description": "Paper tissue napkin component",
        "input": _node({"MA": "BTSX", "AR": "NPX"}),
        "expected": "A1!BTSX.NPX.XXX.X.X",
    },
    {
        "id": "W08",
        "description": "16 oz cup with unresolved capacity statement",
        "input": _node({"AR": "CUX", "UT": [["CA", "16 oz"]]}),
        "expected": "A1!XXXX.CUX.XXX.X.X+UT:CA=16%20oz",
    },
]


def canonical_examples() -> dict[str, Any]:
    """Encode each Document 2 worked example and compare to its documented code."""
    e = atlas_reference.engine()
    results: list[dict[str, Any]] = []
    failures = 0
    for ex in CANONICAL_EXAMPLES:
        try:
            actual = e.encode(ex["input"])
            ok = actual == ex["expected"]
        except Exception as exc:  # noqa: BLE001
            actual = f"<error: {type(exc).__name__}: {exc}>"
            ok = False
        if not ok:
            failures += 1
        results.append({
            "id": ex["id"],
            "description": ex["description"],
            "expected": ex["expected"],
            "actual": actual,
            "pass": ok,
        })
    return {
        "total": len(results),
        "passed": len(results) - failures,
        "failures": failures,
        "all_pass": failures == 0,
        "versions": atlas_reference.BASELINE_VERSIONS,
        "results": results,
    }


def run_engine_suite() -> dict[str, Any]:
    """Run the preserved test_engine.EngineTests programmatically.

    Returns counts and the IDs of any failures. This is the same engine suite
    the full baseline runner invokes (47 tests). Running it in the deployed
    service is the strongest no-drift check at runtime.
    """
    # Importing after atlas_reference.engine() has set up sys.path.
    atlas_reference.engine()
    import sys as _sys  # noqa: PLC0415

    _tests_root = str(atlas_reference.REFERENCE_ROOT / "tests")
    if _tests_root not in _sys.path:
        _sys.path.insert(0, _tests_root)
    import test_engine  # type: ignore[import-not-found]

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_engine)
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=0)
    result = runner.run(suite)
    failures = [t.id() for t, _ in result.failures]
    errors = [t.id() for t, _ in result.errors]
    return {
        "run": result.testsRun,
        "passed": result.testsRun - len(failures) - len(errors),
        "failures": failures,
        "errors": errors,
        "all_pass": result.wasSuccessful(),
        "versions": atlas_reference.BASELINE_VERSIONS,
    }
