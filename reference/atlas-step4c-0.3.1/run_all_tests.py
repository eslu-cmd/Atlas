"""Reproduce baseline, known-answer stability, integrity and persistence tests."""
import hashlib
import json
import platform
import sqlite3
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
from atlas.records import RECORD_VERSION
import test_records
import test_repairs_021

class Results(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs); self.rows=[]
    def addSuccess(self,test):
        super().addSuccess(test)
        self.rows.append({'test':test.id(),'fixture':'ILLUSTRATIVE, except test_12 uses preserved Step 4A workbook batch',
            'expected':test.shortDescription() or 'All named scenario assertions and prohibited-outcome checks hold',
            'actual':'All assertions held through on-disk SQLite','status':'pass'})
    def addFailure(self,test,error):
        super().addFailure(test,error); self.rows.append({'test':test.id(),'status':'fail','actual':self._exc_info_to_string(error,test)})
    def addError(self,test,error):
        super().addError(test,error); self.rows.append({'test':test.id(),'status':'error','actual':self._exc_info_to_string(error,test)})

baseline=subprocess.run([sys.executable,'run_tests.py'],cwd=ROOT,capture_output=True,text=True)
(ROOT/'Engine-Test-Run.txt').write_text(baseline.stdout+baseline.stderr)
engine=json.loads((ROOT/'test-results.json').read_text())
frozen=json.loads((ROOT/'fixtures/engine-known-answers-0.1.1.json').read_text())
known_stable=engine['known_answers']==frozen
integrity=json.loads((ROOT/'reference/baseline-integrity.json').read_text())
hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==value for f,value in integrity['sha256'].items()}
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(module)
                          for module in (test_records,test_repairs_021)])
result=unittest.TextTestRunner(verbosity=2,resultclass=Results).run(suite)
success=baseline.returncode==0 and result.wasSuccessful() and known_stable and all(hashes.values()) and engine['tests_run']==47 and len(frozen)==44
report={'time_utc':datetime.now(timezone.utc).isoformat(),'implementation':RECORD_VERSION,'engine_version':engine['implementation'],
    'dictionary_release':engine['dictionary_release'],'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,
    'storage':'on-disk SQLite; Supabase/Postgres not executed','engine_tests':engine['tests_run'],'record_tests':result.testsRun,'original_record_tests':25,'repair_regression_tests':12,
    'total_tests':engine['tests_run']+result.testsRun,'failures':len(result.failures)+engine['failures'],'errors':len(result.errors)+engine['errors'],
    'known_answers':len(frozen),'known_answers_unchanged':known_stable,'baseline_files_unchanged':hashes,
    'record_results':result.rows,'success':success,'boundary':'Record-layer evidence, not completion of all 24 acceptance workflows, shared editing, deployment or recovery.'}
(ROOT/'record-test-results.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Step 4B reproducible test execution','',f"{report['total_tests']} tests: {report['engine_tests']} baseline + {report['record_tests']} persistent-record tests. {report['failures']} failures; {report['errors']} errors.",
    '',f"Python {report['python']}; SQLite {report['sqlite']}. {report['time_utc']}.",'',report['boundary'],'',
    f"44 known answers unchanged: {known_stable}. Baseline file hashes unchanged: {all(hashes.values())}.",'',
    'Run `python3 run_all_tests.py`. Full expected/actual assertions are in `tests/test_records.py` and `tests/test_repairs_021.py`; machine-readable execution is in `record-test-results.json`. Baseline known answers remain in `test-results.json`.','',
    '| Persistent test | Result |','|---|---|']
lines.extend('| '+r['test'].split('.')[-1]+' | '+r['status']+' |' for r in result.rows)
(ROOT/'Record-Test-Results.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('record_results','baseline_files_unchanged')},indent=2))
sys.exit(0 if success else 1)
