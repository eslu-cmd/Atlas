"""Reproduce inherited suite, then Step 4C persistent workflow scenarios."""
import hashlib
import json
import platform
import sqlite3
import subprocess
import sys
import unittest
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
import test_step4c
import test_repairs_031

class Result(unittest.TextTestResult):
    def __init__(self,*a,**kw): super().__init__(*a,**kw); self.rows=[]
    def addSuccess(self,test):
        super().addSuccess(test); self.rows.append({'test':test.id(),'status':'pass','expected':test.shortDescription() or test.id().split('.')[-1],'actual':'All explicit expected and prohibited-outcome assertions passed on persistent SQLite'})
    def addFailure(self,test,err):
        super().addFailure(test,err); self.rows.append({'test':test.id(),'status':'fail','actual':self._exc_info_to_string(err,test)})
    def addError(self,test,err):
        super().addError(test,err); self.rows.append({'test':test.id(),'status':'error','actual':self._exc_info_to_string(err,test)})

baseline=subprocess.run([sys.executable,'run_all_tests.py'],cwd=ROOT,capture_output=True,text=True)
(ROOT/'Step-4C-Inherited-Test-Run.txt').write_text(baseline.stdout+baseline.stderr)
b=json.loads((ROOT/'record-test-results.json').read_text())
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(m) for m in (test_step4c,test_repairs_031)])
with (ROOT/'Step-4C-Test-Run.txt').open('w') as log:
    result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=Result).run(suite)
pinned=json.loads((ROOT/'reference/Step-4C-inherited-integrity.json').read_text())
integrity={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in pinned['sha256'].items()}
repair_pinned=json.loads((ROOT/'reference/Repair-0.3.1-protected-integrity.json').read_text())
repair_integrity={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in repair_pinned['sha256'].items()}
report={'version':'0.3.1','records_baseline':'0.2.1','engine':'0.1.1','dictionary':'A1 / 0.1.0-local-candidate','time_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,'inherited_tests':b['total_tests'],'previous_baseline_tests':126,'original_step4c_tests':42,'repair_regression_tests':20,'new_tests':result.testsRun,'total_tests':b['total_tests']+result.testsRun,'failures':b['failures']+len(result.failures),'errors':b['errors']+len(result.errors),'known_answers_unchanged':b['known_answers_unchanged'],'known_answers':b['known_answers'],'integrity':integrity,'repair_protected_integrity':repair_integrity,'scenarios':result.rows,'source_fixture':'test_30 uses the preserved batch; other tests are illustrative','success':baseline.returncode==0 and result.wasSuccessful() and all(integrity.values()) and all(repair_integrity.values()),'boundary':'Local intake/search evidence only; not all AT-01–24 workflows, shared editing, cloud deployment or recovery.'}
(ROOT/'step4c-test-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('integrity','repair_protected_integrity','scenarios')},indent=2))
sys.exit(0 if report['success'] else 1)
