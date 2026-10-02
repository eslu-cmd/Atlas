"""Run fresh tests; write execution evidence, including independent known answers."""
import unittest,json,sys,platform,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
import test_engine
from atlas import VERSION
vectors=[]
original=test_engine.EngineTests.assertCode
def record(self,facts,expected):
    actual=None
    try:
        actual=self.e.encode(facts)
        original(self,facts,expected)
    finally:
        vectors.append({'test':self.id(),'input':facts,'expected':expected,'actual':actual,'pass':expected==actual})
test_engine.EngineTests.assertCode=record
class Result(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.rows=[]
    def addSuccess(self,test):super().addSuccess(test);self.rows.append({'test':test.id(),'expected':'All independently specified assertions in named test hold','actual':'All assertions held','status':'pass'})
    def addFailure(self,test,err):super().addFailure(test,err);self.rows.append({'test':test.id(),'status':'fail','actual':self._exc_info_to_string(err,test)})
    def addError(self,test,err):super().addError(test,err);self.rows.append({'test':test.id(),'status':'error','actual':self._exc_info_to_string(err,test)})
suite=unittest.defaultTestLoader.loadTestsFromModule(test_engine)
r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
report={'time_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'implementation':VERSION,'dictionary_release':'0.1.0-local-candidate','dictionary_sha256':hashlib.sha256((ROOT/'dictionary/atlas-A1-0.1.0.json').read_bytes()).hexdigest(),'tests_run':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'test_results':r.rows,'known_answers':vectors,'scope':'Local identifier/dictionary only. No application, history, concurrency, approval, recovery or production validation.'}
(ROOT/'test-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Step 4A test execution','',f"{r.testsRun} test methods; {len(r.failures)} failures; {len(r.errors)} errors.",'',report['scope'],'','Fresh run: `python3 run_tests.py`. Full inputs and expected versus actual codes: `test-results.json`.','', '| Test | Result |','|---|---|']
lines += ['| '+x['test'].split('.')[-1]+' | '+x['status']+' |' for x in r.rows]
lines += ['','## Independent code answers','', '| Test | Expected | Actual |','|---|---|']
lines += [f"| {v['test'].split('.')[-1]} | `{v['expected']}` | `{v['actual']}` |" for v in vectors]
(ROOT/'Test-Results.md').write_text('\n'.join(lines)+'\n')
sys.exit(0 if r.wasSuccessful() else 1)
