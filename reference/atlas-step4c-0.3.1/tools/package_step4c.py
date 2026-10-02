"""Build a self-contained release manifest, ZIP and external checksum report."""
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent

def digest(data): return hashlib.sha256(data).hexdigest()
def main():
    for cache in ROOT.rglob('__pycache__'):
        if cache.is_dir(): shutil.rmtree(cache)
    files={}
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name!='.DS_Store' and '__pycache__' not in p.parts and 'work' not in p.relative_to(ROOT).parts and p!=ROOT/'manifest.json':
            files[p.relative_to(ROOT).as_posix()]=digest(p.read_bytes())
    manifest={'version':'0.3.1','baseline_records':'0.2.1','engine':'0.1.1','dictionary':'A1 / 0.1.0-local-candidate','algorithm':'SHA-256','exclusion':'manifest.json excludes itself; generated Python caches, .DS_Store and local work/ excluded','files':files}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    archive=OUT/'Atlas-Step-4C-0.3.1.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in list(files)+['manifest.json']: z.write(ROOT/name,'atlas-step4c/'+name)
    checksum=digest(archive.read_bytes())
    archive.with_suffix('.zip.sha256').write_text(checksum+'  '+archive.name+'\n')
    with zipfile.ZipFile(archive) as z:
        bad=z.testzip()
        actual=set(z.namelist()); expected={'atlas-step4c/'+n for n in list(files)+['manifest.json']}
        mismatches=[name for name,h in files.items() if digest(z.read('atlas-step4c/'+name))!=h]
    report={'version':'0.3.1','archive':archive.name,'sha256':checksum,'manifested_files':len(files),'archive_entries':len(actual),'crc_error':bad,'missing_entries':sorted(expected-actual),'extra_entries':sorted(actual-expected),'content_mismatches':mismatches,'passed':not bad and actual==expected and not mismatches}
    (OUT/'Package-Verification-0.3.1.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2)); return 0 if report['passed'] else 1

if __name__=='__main__': sys.exit(main())
