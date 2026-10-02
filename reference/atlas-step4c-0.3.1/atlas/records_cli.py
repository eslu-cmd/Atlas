"""Small local CLI. JSON plans are explicit record operations, never inferred text."""
import argparse
import json
import sqlite3
import sys
from .records import Store, RecordError, RECORD_VERSION
from .engine import SpecError
from .batch import import_batch
from .demo import illustrative

def main(argv=None):
    p=argparse.ArgumentParser(description=f'Atlas persistent records {RECORD_VERSION} (local SQLite)')
    p.add_argument('--db',required=True)
    sub=p.add_subparsers(dest='action',required=True)
    sub.add_parser('init'); sub.add_parser('import-reviewed'); sub.add_parser('demo')
    for action in ('get','history','product-history','memberships','current-association','sampling-history'):
        sub.add_parser(action).add_argument('id')
    sub.add_parser('list').add_argument('kind')
    sub.add_parser('apply').add_argument('file',help='JSON array of explicit operations; atomic')
    args=p.parse_args(argv)
    try:
        with Store(args.db) as store:
            if args.action=='init': result={'schema':1,'implementation':RECORD_VERSION}
            elif args.action=='import-reviewed': result=import_batch(store)
            elif args.action=='demo': result=illustrative(store)
            elif args.action=='list': result=store.all(args.kind)
            elif args.action=='apply':
                allowed={'add','register_dictionary','issue','change_association','revise','correct_approval','resolve_identity'}
                def unique(pairs):
                    d={}
                    for k,v in pairs:
                        if k in d: raise RecordError('Duplicate JSON key '+k)
                        d[k]=v
                    return d
                with open(args.file) as f: plan=json.load(f,object_pairs_hook=unique)
                if not isinstance(plan,list): raise RecordError('Plan must be an array')
                result={}
                def resolve(value):
                    if isinstance(value,str) and value.startswith('$'): return result[value[1:]]
                    if isinstance(value,list): return [resolve(x) for x in value]
                    if isinstance(value,dict): return {k:resolve(v) for k,v in value.items()}
                    return value
                with store.transaction():
                    for step in plan:
                        if set(step)!={'name','operation','arguments'} or step['operation'] not in allowed:
                            raise RecordError('Unsupported plan operation')
                        if step['name'] in result: raise RecordError('Duplicate result name')
                        result[step['name']]=getattr(store,step['operation'])(**resolve(step['arguments']))
            else: result=getattr(store,args.action.replace('-','_'))(args.id)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (RecordError,SpecError,sqlite3.Error,OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({'complete':False,'error':str(error)}),file=sys.stderr)
        return 2

if __name__=='__main__': sys.exit(main())
