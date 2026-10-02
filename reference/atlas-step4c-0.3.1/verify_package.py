"""Verify the delivered manifest before running commands that rewrite reports."""
import hashlib
import json
import sys
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text())
bad=[]
for name,expected in manifest['files'].items():
    p=root/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        bad.append(name)
print(json.dumps({'version':manifest['version'],'files_checked':len(manifest['files']),'mismatches':bad},indent=2))
sys.exit(bool(bad))
