"""JSON CLI for persisted review, explicit search and confirmed phrase search."""
import argparse
import json
import sqlite3
import sys
from .records import Store, RecordError
from .engine import SpecError
from .search import Search, UnsupportedQuery, VERSION
from .intake import Intake
from .phrases import Phrases

def read(path):
    def unique(pairs):
        result={}
        for k,v in pairs:
            if k in result: raise ValueError('Duplicate JSON key '+k)
            result[k]=v
        return result
    with open(path) as f: return json.load(f,object_pairs_hook=unique)

def main(argv=None):
    p=argparse.ArgumentParser(description='Atlas intake/search '+VERSION)
    p.add_argument('--db',required=True)
    sub=p.add_subparsers(dest='command',required=True)
    for name in ('capture','preview','commit','search','phrase','confirm-phrase'):
        sub.add_parser(name).add_argument('file',help='JSON arguments file')
    for name in ('intake-history','execute-phrase','inspect'):
        sub.add_parser(name).add_argument('id')
    args=p.parse_args(argv)
    try:
        with Store(args.db) as s:
            i=Intake(s); phrases=Phrases(s)
            if args.command=='search': result=Search(s).search(read(args.file))
            elif args.command in ('capture','preview','commit'): result=getattr(i,args.command)(**read(args.file))
            elif args.command=='phrase': result=phrases.propose(**read(args.file))
            elif args.command=='confirm-phrase': result=phrases.confirm(**read(args.file))
            elif args.command=='execute-phrase': result=phrases.execute(args.id)
            elif args.command=='intake-history': result=i.history(args.id)
            else: result=s.history(args.id)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        status=result.get('status') if isinstance(result,dict) else None
        return 3 if status=='unsupported' else 2 if status=='error' else 0
    except (RecordError,SpecError,UnsupportedQuery,sqlite3.Error,OSError,ValueError,KeyError,TypeError) as e:
        print(json.dumps({'status':'error','error':str(e)}),file=sys.stderr)
        return 2

if __name__=='__main__': sys.exit(main())
