import argparse,json,sys
from . import Engine,SpecError
p=argparse.ArgumentParser(description='Atlas A1 local candidate')
p.add_argument('--dictionary',required=True)
p.add_argument('action',choices=['encode','decode','validate','canonicalize','compare'])
p.add_argument('input',help='JSON file for encode; complete code otherwise')
p.add_argument('other',nargs='?')
a=p.parse_args()
try:
 e=Engine(a.dictionary)
 if a.action=='encode':
  def unique(pairs):
   d={}
   for k,v in pairs:
    if k in d:raise SpecError('Duplicate JSON key '+k)
    d[k]=v
   return d
  result=e.encode(json.load(open(a.input),object_pairs_hook=unique))
 elif a.action=='decode':result=e.describe(a.input)
 elif a.action=='validate':e.decode(a.input);result={'valid':True,'dictionary_release':e.d['release']}
 elif a.action=='compare':result=e.compare(a.input,a.other)
 else:result=e.canonicalize(a.input)
 print(json.dumps(result,ensure_ascii=False,indent=2) if not isinstance(result,str) else result)
except (SpecError,OSError,json.JSONDecodeError) as ex:
 print(json.dumps({'error':str(ex),'complete':False}),file=sys.stderr);sys.exit(2)
