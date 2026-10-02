#!/usr/bin/env python3
"""Run the preserved reference test suite without modifying the preserved package.

Copies `reference/atlas-step4c-0.3.1/` to a scratch directory, runs
`verify_package.py` and `run_step4c_tests.py` there, prints the results, then
re-verifies that the preserved reference is still pristine.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PRESERVED = REPO_ROOT / "reference" / "atlas-step4c-0.3.1"


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def main() -> int:
    if not PRESERVED.is_dir():
        print(f"preserved reference missing at {PRESERVED}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="atlas-ref-") as tmp:
        scratch = Path(tmp) / "atlas-step4c"
        shutil.copytree(PRESERVED, scratch)

        rc, out, err = run([sys.executable, "verify_package.py"], scratch)
        verify = json.loads(out) if out.strip() else {}
        print("preserved manifest:", json.dumps(verify, indent=2))
        if verify.get("mismatches"):
            print("preserved reference manifest FAILED", file=sys.stderr)
            print(err, file=sys.stderr)
            return 1

        rc, out, err = run([sys.executable, "run_step4c_tests.py"], scratch)
        tail = out.strip().splitlines()[-30:]
        suite_json_line = None
        for line in tail:
            if line.startswith("{"):
                suite_json_line = "\n".join(tail[tail.index(line):])
                break
        print("baseline run:")
        print(suite_json_line or out)
        if rc != 0:
            print(err, file=sys.stderr)
            return 1
        suite = {}
        if suite_json_line:
            try:
                suite = json.loads(suite_json_line)
            except json.JSONDecodeError:
                pass
        if not suite.get("success"):
            print("baseline suite reported !success", file=sys.stderr)
            return 1

    # Re-verify preserved reference wasn't touched
    rc, out, err = run([sys.executable, "verify_package.py"], PRESERVED)
    verify = json.loads(out) if out.strip() else {}
    if verify.get("mismatches"):
        print("preserved reference drifted after scratch run:", verify, file=sys.stderr)
        return 1

    print("\nreference pristine; baseline 146/146 ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
