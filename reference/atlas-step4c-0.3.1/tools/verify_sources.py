"""Optional read-only audit of original source hashes; no workbook dependency."""
import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
errors=[]
for item in json.loads((root/'source-ledger.json').read_text()):
    path=Path(item['path'])
    if not path.exists():errors.append({'path':str(path),'status':'unavailable'});continue
    if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:errors.append({'path':str(path),'status':'changed since inspection'})
print(json.dumps({'all_inspected_sources_match':not errors,'issues':errors},indent=2))
sys.exit(bool(errors))
