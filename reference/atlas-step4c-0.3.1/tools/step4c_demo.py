"""Execute the actual CLI using clearly labelled illustrative data; save every step."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from atlas.records import Store
from atlas.demo import illustrative

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',required=True); args=parser.parse_args()
    out=Path(args.out).resolve()
    if out.exists(): parser.error('Choose a fresh output directory; existing demonstrations are preserved')
    out.mkdir(parents=True); db=out/'atlas.sqlite'
    with Store(db) as s: ids=illustrative(s)
    meta={'actor':'ILLUSTRATIVE CLI reviewer','reason':'Explicit synthetic demonstration; not workbook product facts','provenance':'illustrative'}
    def save(name,data):
        p=out/(name+'.json'); p.write_text(json.dumps(data,indent=2)+'\n'); return p
    def run(name,action,payload):
        path=save(name+'-input',payload)
        cmd=[sys.executable,'-m','atlas.workflow_cli','--db',str(db),action,str(path)]
        proc=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        if proc.returncode: raise RuntimeError(proc.stdout+proc.stderr)
        value=json.loads(proc.stdout); save(name+'-output',value); return value
    t=run('01-capture','capture',{'document':{'label':'ILLUSTRATIVE intake: 500 mL PET cup','kind':'supplier_statement','source':{'title':'ILLUSTRATIVE quotation','uri':'illustrative://step4c/quote'},'locator':{'page':1,'paragraph':2},'statements':[{'statement':'500 mL PET cup body; 98 mm rim; offering reference ILLUSTRATIVE-REVIEWED','uncertainty':'stated','supplied':{'capacity':'500 mL','rim':'98 mm','formula':None,'cached':None}}],'facts':{'fields':{'MA':'APTX','AR':'CUB','CA':'M500','FI':'R98'}}},**meta})
    p=run('02-preview','preview',{'intake':t,**meta})
    with Store(db) as s: evidence=s.get(t)['links']['assertions']
    decision={'action':'offering','confirmed':True,'evidence':evidence,'supplier':ids['A']['supplier'],'reference':'ILLUSTRATIVE-REVIEWED'}
    committed=run('03-commit','commit',{'preview':p['preview'],'decision':decision,**meta})
    repeated=run('04-repeat','commit',{'preview':p['preview'],'decision':decision,**meta})
    assert repeated['decision']==committed['decision'] and repeated['repeated']
    broad=run('05-browse','search',{'criteria':[{'field':'AR_CLASS','value':'CU'}],'types':['offering','specification','triage']})
    narrow=run('06-narrow','search',{'criteria':[{'field':'AR_CLASS','value':'CU'},{'field':'CA','value':{'value':'0.5','unit':'L'}}],'types':['offering'],'evidence':{'approval':'client_approval'}})
    phrase=run('07-phrase','phrase',{'phrase':'PET cups 500 ml',**meta})
    confirmation=run('08-confirm','confirm-phrase',{'review':phrase['review'],'query':phrase['proposed'],'confirmed':True,'acknowledged':phrase['unsupported'],**meta})
    for name,action,identity in [('09-execute','execute-phrase',confirmation),('10-intake-history','intake-history',t),('11-old-quote','inspect',ids['A']['quote'])]:
        proc=subprocess.run([sys.executable,'-m','atlas.workflow_cli','--db',str(db),action,identity],cwd=ROOT,capture_output=True,text=True,check=True)
        save(name+'-output',json.loads(proc.stdout))
    summary={'fixture':'ILLUSTRATIVE only; no workbook products promoted','database':str(db),'intake':t,'preview':p['preview'],'committed':committed,'repeated_without_duplicates':repeated['repeated'],'broad_counts':broad['counts'],'narrow_counts':narrow['counts'],'phrase_confirmation':confirmation,'old_quote':ids['A']['quote']}
    save('summary',summary); print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
