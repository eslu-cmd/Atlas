"""Explicit structured criteria over immutable Store records. No ID-text matching."""
import copy
import sqlite3
from .engine import Engine, SpecError, exact
from .records import ROOT, RecordError

VERSION = '0.3.1'
SLOTS = {'MA_FAMILY':('MA',0,1,'FAMILY'), 'MA_GRADE':('MA',1,3,'GRADE'),
         'MA_TREATMENT':('MA',3,4,'TREATMENT'), 'AR_CLASS':('AR',0,2,'ARTICLE'),
         'AR_ROLE':('AR',2,3,'ROLE'), 'CF_SHAPE':('CF',0,1,'SHAPE'),
         'CF_CONSTRUCTION':('CF',1,2,'CONSTRUCTION')}
TYPES = {'specification','offering','kit','capability','triage'}
APPROVALS = {'proof_agreement':'agreed','source_one_acceptance':'accepted','client_approval':'approved'}

class UnsupportedQuery(ValueError): pass

def supported(ok, message):
    if not ok: raise UnsupportedQuery(message)

def outcome(state, reason, **extra):
    return dict(state=state, reason=reason, **extra)

def classification(explanations):
    states = [e['state'] for e in explanations]
    return 'contradiction' if 'contradiction' in states else 'potential' if 'gap' in states else 'match'

class Search:
    def __init__(self, store):
        self.s = store
        self.e = Engine(ROOT/'dictionary/atlas-A1-0.1.0.json')

    def validate_criterion(self, c, nested=False):
        supported(isinstance(c,dict), 'Criterion must be an object')
        scope=c.get('scope',[])
        supported(isinstance(scope,list) and all(x in self.e.d['scopes'] for x in scope), 'Scope must be a path of registered names')
        if 'layer' in c or 'component' in c:
            key='layer' if 'layer' in c else 'component'
            supported(set(c)<={key,'scope'} and isinstance(c[key],list) and bool(c[key]), 'Malformed grouped criteria')
            supported(not nested, 'Nested layer/component filtering is deferred; inspect complete construction')
            for child in c[key]:
                self.validate_criterion(child,True)
                supported(not (key=='layer' and child.get('field')=='TH'), 'Specialized layer-thickness filtering is deferred')
            return
        supported(set(c)<={'field','value','scope','qualifier','tolerance'}, 'Unsupported criterion option')
        field=c.get('field')
        supported(isinstance(field,str) and 'value' in c, 'Criterion needs field and value')
        value=c['value']
        if field in SLOTS:
            table=SLOTS[field][3]
            values=set(self.e.t[table]) if table!='GRADE' else {f+g for f,gs in self.e.t['GRADE'].items() for g in gs}
            supported(isinstance(value,str) and value in values and not set(value)<={'X'}, 'Unsupported slot value; grade uses family+grade, e.g. APT')
        elif field=='CF_FEATURE':
            supported(isinstance(value,dict) and set(value)=={'article','closure','token'}, 'Feature needs article, closure boolean and token')
            supported(value['article'] in self.e.t['ARTICLE'] and type(value['closure']) is bool, 'Feature dictionary scope required')
            table=self.e.t['FEATURE_LID'] if value['closure'] else self.e.t['FEATURE'].get(value['article'],self.e.t['FEATURE']['_DEFAULT'])
            supported(value['token'] in table and value['token'] not in ('X','9'), 'Unsupported feature token')
        elif field in ('kind','laminate'):
            supported(value in ('cup','lid','bag','kit') if field=='kind' else value is True, 'Unsupported browsing value')
        elif field.startswith('DM_'):
            supported(field[3:] in self.e.d['dimensions'], 'Unsupported dimension role')
            self.numeric_request(c)
        elif field in ('CA','FI') or self.e.f.get(field,{}).get('type') in ('num','int'):
            self.numeric_request(c)
        else:
            f=self.e.f.get(field,{})
            supported(f.get('type') in ('enum','list','str','profile'), 'Unsupported field '+str(field))
            if f['type'] in ('enum','list'): supported(value in f['domain'], 'Unsupported dictionary value')
            elif field=='LP': supported(value in self.e.t['FEATURE_LID'] and value not in ('X','0','9'), 'Unsupported lid profile')
            elif field=='FF': supported(value in self.e.d['registered_fitments'], 'Unsupported registered fitment')
            else: supported(isinstance(value,str) and bool(value), 'Expected exact text value')
        if not self.is_numeric(field): supported(not ({'qualifier','tolerance'} & set(c)), 'Qualifiers only apply to quantities')

    def is_numeric(self, f):
        return f in ('CA','FI') or f.startswith('DM_') or self.e.f.get(f,{}).get('type') in ('num','int')

    def numeric_request(self,c):
        f=c['field']; value=c['value']
        if f in ('CA','FI'):
            encoded=self.e.quantity(f,value)
            if encoded in ('X','0'):
                supported(encoded=='0' and not ({'qualifier','tolerance'} & set(c)), 'Unknown is not a required quantity')
                return None
            unit={'M':'mL','G':'g','N':'count','R':'mm'}[encoded[0]]; value=encoded[1:]
        else:
            unit='mm' if f.startswith('DM_') else self.e.f[f]['unit']
            spec=self.e.f.get(f,{})
            value=self.e.amount(value,unit,positive=spec.get('minimum')!='0',integer=spec.get('type')=='int',maximum=spec.get('maximum'))
        vals=self.e.unit(value,unit); lo,hi=vals[0],vals[-1]
        q=c.get('qualifier',['REPORTED','UNKNOWN','-'])
        supported(isinstance(q,list) and len(q)==3 and q[0] in self.e.d['qualifiers']['modes'] and q[1] in self.e.d['qualifiers']['bases'] and isinstance(q[2],str) and bool(q[2]), 'Invalid quantity qualifier')
        supported(q[1] not in ('FILL','BRIM') or (f=='CA' and unit=='mL'), 'Basis incompatible with quantity role')
        supported(q[1]!='NA' or unit!='mL', 'NA basis incompatible with volume')
        if 'tolerance' in c:
            t=c['tolerance']; supported(len(vals)==1 and isinstance(t,list) and len(t)==2, 'Tolerance needs scalar and two offsets')
            offsets=[self.e.unit(x,unit) for x in t]
            supported(all(len(x)==1 and x[0]>=0 for x in offsets), 'Invalid tolerance')
            lo-=offsets[0][0]; hi+=offsets[1][0]
            supported(lo>=0, 'Tolerance outside domain')
        return lo,hi,unit,q

    def validate(self, query):
        supported(isinstance(query,dict) and set(query)<={'criteria','types','evidence','scope','historical'}, 'Unsupported query options')
        criteria=query.get('criteria',[])
        supported(isinstance(criteria,list), 'Criteria must be an array')
        for c in criteria: self.validate_criterion(c)
        types=query.get('types',sorted(TYPES))
        supported(isinstance(types,list) and bool(types) and all(x in TYPES for x in types), 'Unsupported result types')
        evidence=query.get('evidence',{})
        supported(isinstance(evidence,dict) and set(evidence)<={'quotation','photos','sampling','approval','kit_membership'}, 'Unsupported evidence filter')
        for k,v in evidence.items():
            supported(v in APPROVALS if k=='approval' else v is True, 'Evidence filter must explicitly select presence or approval type')
        scope=query.get('scope',{})
        supported(isinstance(scope,dict) and set(scope)<={'client','request','job','version','association','customization','packing','sample','kit_revision'}, 'Unsupported evidence scope')
        for k,v in scope.items(): self.s.get(v, k if k!='association' else 'association')
        supported(type(query.get('historical',False)) is bool, 'historical must be boolean')
        return query

    def local(self,node,path):
        for name in path:
            node=next((g['node'] for g in node.get('groups',[]) if g.get('scope')==name),{})
        return node

    def evaluate(self,node,c,capability=False,uncertainty=None):
        n=self.local(node,c.get('scope',[])); f=n.get('fields',{}); field=c.get('field'); want=c.get('value')
        if 'component' in c:
            return outcome('gap','Component criteria require a kit revision')
        if 'layer' in c:
            layers=[x for g in n.get('groups',[]) for x in g.get('layers',[])]
            checks=[[self.evaluate(x,cc,capability) for cc in c['layer']] for x in layers]
            if any(classification(x)=='match' for x in checks): return outcome('satisfies','One recorded layer jointly supports all selected facts',layers=checks)
            # A partial construction does not prove absence of an unrecorded layer.
            return outcome('gap','No single recorded layer supports these facts; construction may be partial',layers=checks)
        if field=='laminate':
            known=f.get('MA','X')[0]=='J' or f.get('CF','XXX')[1]=='L' or any('layers' in g for g in n.get('groups',[]))
            return outcome('satisfies' if known else 'gap','Recorded laminate/stack' if known else 'No recorded laminate construction')
        # Explicit unresolved assertions take precedence over interpreted values.
        relevant=[x for x in (uncertainty or []) if x.get('field')==field and x.get('scope',[])==c.get('scope',[])]
        if relevant:
            state=relevant[-1]['state']
            if state=='not_applicable': return outcome('satisfies' if want in ('0','NOT_APPLICABLE') else 'contradiction','Explicitly not applicable')
            if state!='stated': return outcome('gap','Unresolved assertion: '+state, assertions=relevant)
        if any(t==field or t==field.split('_')[0] for t,_ in f.get('UT',[])):
            return outcome('gap','Targeted unresolved wording retained',statements=f['UT'])
        if field=='kind':
            ar=f.get('AR','XXX'); role={'B':'BODY','L':'CLOSURE','A':'ACCESSORY'}.get(ar[2],f.get('FR'))
            if want=='lid': actual=True if role=='CLOSURE' else False if role in ('BODY','ACCESSORY') or ar[:2] not in self.e.d['lid_bearing'] and ar[:2]!='XX' else None
            elif want=='kit': actual=False if ar[:2]!='XX' else None
            else:
                cl={'cup':'CU','bag':'BG'}[want]
                actual=False if ar[:2] not in (cl,'XX') or role=='CLOSURE' else True if ar[:2]==cl and (want=='bag' or role=='BODY') else None
            return outcome('gap' if actual is None else 'satisfies' if actual else 'contradiction','Article/function classification; unknown role does not prove body or saleability')
        if field=='CF_FEATURE':
            ar=f.get('AR','XXX')
            if ar[:2]=='XX': return outcome('gap','Feature article scope is unknown')
            if ar[:2]!=want['article']: return outcome('contradiction','Feature belongs to a different article scope')
            # Core/FX dictionary is selected by the encoded role, not FR.
            # A closure with role X still has article-scoped core/FX and a separate LP.
            if want['closure']:
                if ar[2]=='L': tokens=[f.get('CF','XXX')[2]]+f.get('FX',[])
                elif f.get('FR')=='CLOSURE': tokens=[f.get('LP','X')]
                else:
                    return outcome('contradiction' if ar[2] in ('B','A') or f.get('FR') else 'gap','Closure function differs or is unknown')
                rules=self.e.d['feature_rules']['LID']
            else:
                if ar[2]=='L': return outcome('gap','Core/FX use the lid dictionary; no article-scoped feature recorded')
                tokens=[f.get('CF','XXX')[2]]+f.get('FX',[])
                rules=self.e.d['feature_rules'].get(ar[:2],self.e.d['feature_rules']['_DEFAULT'])
            requested=want['token']
            if requested in tokens: return outcome('satisfies','Feature recorded in the selected dictionary scope',recorded=tokens)
            known=set(tokens)-{'X','9'}
            exclusive=any(requested in group and known.intersection(group) for group in rules['exclusive_sets'])
            negative=set(rules['negative'])
            contradiction=bool('0' in known or requested=='0' and known or exclusive or known.intersection(negative) or requested in negative and known)
            return outcome('contradiction' if contradiction else 'gap','Explicit negative, non-applicability or mutually exclusive feature' if contradiction else 'Compatible optional feature not supplied in this dictionary scope',recorded=tokens)
        if field in SLOTS:
            block,start,end,_=SLOTS[field]; default={'MA':'XXXX','AR':'XXX','CF':'XXX'}[block]
            actual=f.get(block,default)[start:end]
            if field=='MA_GRADE': actual=f.get('MA','XXXX')[:3]
        elif field=='FR': actual={'B':'BODY','L':'CLOSURE','A':'ACCESSORY'}.get(f.get('AR','XXX')[2],f.get(field))
        elif field=='LP': actual=f.get('CF','XXX')[2] if f.get('AR','XXX')[2]=='L' else f.get(field)
        elif field=='BL': actual=f.get(field,{'BKW':'BLEACHED','BKB':'UNBLEACHED'}.get(f.get('MA','XXXX')[:3]))
        elif field.startswith('DM_'): actual=f.get('DM',{}).get(field[3:])
        else: actual=f.get(field)
        if actual is None or isinstance(actual,str) and set(actual)<={'X'}:
            return outcome('gap','Required information not supplied',recorded=actual)
        if isinstance(actual,str) and ('9' in actual and field in SLOTS): return outcome('gap','Other vocabulary requires review',recorded=actual)
        if field in SLOTS and 'X' in actual: return outcome('gap','Incomplete slot',recorded=actual)
        if self.is_numeric(field):
            request=self.numeric_request(c)
            if field in ('CA','FI') and (actual=='0' or request is None):
                return outcome('satisfies' if actual=='0' and request is None else 'contradiction','Explicit applicability comparison',recorded=actual)
            raw,unit,_=self.e.numeric_target(field,f)
            vals=self.e.unit(raw,unit); lo,hi=vals[0],vals[-1]
            for target,minus,plus in f.get('TO',[]):
                if target==field: lo-=exact(minus); hi+=exact(plus)
            q=next((r[1:] for r in f.get('QC',[]) if r[0]==field),['REPORTED','UNKNOWN','-'])
            rl,rh,ru,rq=request
            if ru!=unit: return outcome('contradiction','Incompatible quantity roles/units',recorded=actual)
            if q[1:]!=rq[1:] or q[0]!=rq[0]:
                return outcome('gap' if 'UNKNOWN' in (q[1],rq[1]) or q[0]=='APPROXIMATE' else 'contradiction','Measurement basis, mode or conditions differ',recorded_qualifier=q)
            if q[0]=='APPROXIMATE': return outcome('gap','Approximate values require review, not automatic exact satisfaction')
            ok=lo<=rl and rh<=hi if capability else rl<=lo and hi<=rh
            return outcome('satisfies' if ok else 'contradiction','Manufacturing range contains requested target/interval' if capability else 'Entire product interval must lie within requested interval',recorded_interval=[str(lo),str(hi)],required_interval=[str(rl),str(rh)],unit=unit)
        ok=want in actual if isinstance(actual,list) else actual==want
        return outcome('satisfies' if ok else 'contradiction','Recorded value comparison',recorded=actual,required=want)

    def describe(self,spec):
        if not spec: return {'fields':{}},None,None
        record=self.s.get(spec,'specification'); code=record['data']['code']
        engine=Engine(self.s.get(self.s.one(spec,'dictionary'))['data']['document'])
        desc=engine.describe(code)
        return desc['facts'],code,desc['description']

    def current(self,r):
        return self.s.is_active(r['id']) and not self.s.referring(r['id'],'previous',r['kind'])

    def contexts(self,row,scope):
        target=row.get('version') or row.get('kit_revision')
        role='version' if row.get('version') else 'kit_revision'
        if not target: return []
        found=[]
        for c in self.s.referring(target,role,'context'):
            if row.get('association') and self.s.one(c['id'],'association')!=row['association']: continue
            resolved={**{k:v[0] for k,v in c['links'].items()},**self.s._business_scope(c['links'])}
            if all(k=='sample' or resolved.get(k)==v for k,v in scope.items()): found.append(c)
        return found

    def evidence(self,row,query):
        filters=query.get('evidence',{}); scope=query.get('scope',{})
        if not filters and not scope: return []
        if row['type'] not in ('offering','kit'):
            return [outcome('gap','Supplier evidence cannot be inherited by a description, capability or triage',criterion=k) for k in list(filters)+list(scope)]
        membership=None
        if filters.get('kit_membership'):
            ids=[]
            if row.get('version'):
                ids=[r['id'] for r in self.s.memberships(row['version']) if self.current(r) and any(self.s.one(c,'association')==row['association'] for c in r['links']['components'])]
            membership=outcome('satisfies' if ids else 'gap','Current kit membership with this exact association' if ids else 'No current membership recorded',criterion='kit_membership',records=ids)
        if set(filters)<={'kit_membership'} and not scope: return [membership] if membership else []
        trials=[]
        contexts=self.contexts(row,scope)
        for context in contexts:
            cid=context['id']
            same=[c['id'] for c in contexts if self.s.same_context(c['id'],cid)]
            samples=[s for id in same for s in self.s.referring(id,'context','sample') if not scope.get('sample') or s['id']==scope['sample']]
            # Sample evidence is evaluated per iteration, never photo V1 + approval V2.
            sample_required=bool(scope.get('sample') or filters.get('sampling') or filters.get('photos'))
            sample_scoped=sample_required or 'approval' in filters
            if sample_required:
                iterations=samples or [None]
            elif 'approval' in filters:
                # Exact sample IDs also identify their sequence; repeated V1 labels
                # across independent efforts must never pool decisions.
                approvals=[a for id in same for a in self.s.referring(id,'context','approval') if a['data']['type']==filters['approval']]
                iterations=[sample for sample in samples if any(self.s.one(a['id'],'sample')==sample['id'] for a in approvals)]
                if any(self.s.one(a['id'],'sample') is None for a in approvals): iterations.append(None)
                if not iterations: iterations=[None]
            else:
                iterations=[None]
            for iteration in iterations:
                sample_id=iteration['id'] if iteration else None
                checks=[]
                if scope: checks.append(outcome('satisfies' if not scope.get('sample') or sample_id==scope['sample'] else 'gap','Selected exact context',criterion='scope',context=cid))
                for k,v in filters.items():
                    if k=='kit_membership': checks.append(membership); continue
                    ids=[]; rejected=False
                    if k=='quotation': ids=[q['id'] for id in same for q in self.s.referring(id,'context','quote') if self.current(q)]
                    elif k=='sampling': ids=[sample_id] if sample_id else []
                    elif k=='photos':
                        ids=[n['id'] for n in self.s.referring(sample_id,'sample','sample_note') if n['data']['type']=='photo' and n['links'].get('attachments')] if sample_id else []
                    elif k=='approval':
                        approvals=[a for id in same for a in self.s.referring(id,'context','approval') if a['data']['type']==v and (not sample_scoped or self.s.one(a['id'],'sample')==sample_id and (not sample_required or sample_id is not None))]
                        active_rejections=[a for a in approvals if self.s.is_active(a['id']) and a['data']['decision']=='rejected']
                        ids=[a['id'] for a in approvals if self.s.is_active(a['id']) and a['data']['decision']==APPROVALS[v]] if not active_rejections else []
                        rejected=bool(approvals) and not ids
                    checks.append(outcome('satisfies' if ids else 'contradiction' if rejected else 'gap','Evidence in this exact context/iteration' if ids else 'Rejected, withdrawn, or conflicting approval decisions recorded' if rejected else 'Required evidence not recorded in this context/iteration',criterion=k,records=ids,context=cid,sample=sample_id))
                trials.append(checks)
        if not trials:
            return ([membership] if membership else [])+[outcome('gap','No recorded context with selected scope/evidence',criterion=k) for k in list(filters)+list(scope) if k!='kit_membership']
        best=min(trials,key=lambda x:{'match':0,'potential':1,'contradiction':2}[classification(x)])
        return best+[outcome('satisfies','Evidence alternatives evaluated separately',context_alternatives=trials)]

    def rows(self,query):
        s=self.s; historical=query.get('historical',False)
        for kind in query.get('types',sorted(TYPES)):
            if kind=='specification':
                for r in s.all(kind):
                    yield {'id':r['id'],'type':kind,'specification':r['id'],'historical_description':True}
            elif kind=='offering':
                for v in s.all('version'):
                    if not historical and not self.current(v): continue
                    associations=s.referring(v['id'],'version','association') if historical else [s.current_association(v['id'])]
                    for a in associations or [None]:
                        p=s.one(v['id'],'product')
                        yield {'id':p+':'+v['id']+':'+(a['id'] if a else 'unresolved'),'type':kind,'product':p,'version':v['id'],'supplier':s.one(p,'supplier'),'association':a['id'] if a else None,'specification':s.one(a['id'],'specification') if a else None,'current':self.current(v) and bool(a) and s.current_association(v['id'])==a}
            elif kind=='kit':
                for r in s.all('kit_revision'):
                    if historical or self.current(r):
                        kit=s.one(r['id'],'kit')
                        yield {'id':r['id'],'type':kind,'kit':kit,'kit_revision':r['id'],'supplier':s.one(kit,'supplier'),'components':[s.history(c) for c in r['links']['components']],'current':self.current(r)}
            elif kind=='capability':
                for r in s.all(kind): yield {'id':r['id'],'type':kind,'supplier':s.one(r['id'],'supplier'),'alternatives':r['data']['alternatives'],'conditions':r['data']['conditions'],'availability_established':False}
            else:
                for r in s.all('triage'):
                    decisions=s.referring(r['id'],'intake','intake_decision')
                    resolved=[d for d in decisions if d['data']['action']!='triage']
                    yield {'id':r['id'],'type':kind,'specification':s.one(r['id'],'specification'),'snapshot':r['data']['snapshot'],'label':r['data']['label'],'intake_kind':r['data']['snapshot'].get('kind','supplier_statement'),'resolution':'resolved_with_original_retained' if resolved else 'unresolved','decisions':decisions}

    def _search(self,query):
        self.validate(query); result=[]
        for row in self.rows(query):
            node,code,readable=self.describe(row.get('specification'))
            uncertainty=[]
            if row['type']=='triage':
                snapshot=row['snapshot']; uncertainty=snapshot.get('uncertainty_facts',[])
                if not code and snapshot.get('facts'): node=self.e.decode(self.e.encode(snapshot['facts']))
                # Two preserved unencoded fixtures expose only their already-reviewed known facts.
                known=snapshot.get('triage_known_facts',{})
                if known.get('article')=='bag':
                    node={'fields':{'AR':'BGX',**({'CF':'XXN'} if known.get('handle')=='without handle' else {})}}
                    if known.get('original_material_statements'):
                        uncertainty=uncertainty+[{'field':f,'state':'conflicting','wording':known['original_material_statements']} for f in ('MA_GRADE','FS')]
                if known.get('material')=='bagasse': node={'fields':{'MA':'CBGX','BL':'BLEACHED','UT':[['CA',known['capacity_unresolved']]]}}
            if row['type'] in ('offering','kit'):
                subjects=[row.get(k) for k in ('product','version','association','kit','kit_revision') if row.get(k)]
                row['additional_assertions']=[a for subject in subjects for a in self.s.referring(subject,'subject','assertion')]
            checks=[]
            if row['type']=='capability':
                alternatives=[]
                for a in row['alternatives']:
                    try:
                        n=self.e.decode(self.e.encode(a.get('facts',a)))
                        cs=[dict(self.evaluate(n,c,True),criterion=c) for c in query.get('criteria',[])]
                        if row['conditions'] and query.get('criteria'): cs.append(outcome('gap','Capability has supplied feasibility conditions requiring review',conditions=row['conditions']))
                    except (SpecError,AttributeError,TypeError,KeyError): cs=[outcome('gap','Alternative is not in supported structured fact format; inspect retained original')]
                    alternatives.append(cs)
                checks=min(alternatives,key=lambda x:{'match':0,'potential':1,'contradiction':2}[classification(x)])
                row['alternative_explanations']=alternatives
                row['possibility']='custom_build_only'
            else:
                for c in query.get('criteria',[]):
                    if row['type']=='kit' and c.get('field')=='kind': check=outcome('satisfies' if c['value']=='kit' else 'contradiction','Kit identity is separate from components')
                    elif row['type']=='kit' and 'component' in c:
                        trials=[]
                        for comp in self.s.get(row['id'])['links']['components']:
                            a=self.s.one(comp,'association'); n,_,_=self.describe(self.s.one(a,'specification'))
                            trials.append([self.evaluate(n,x) for x in c['component']])
                        check=outcome('satisfies' if any(classification(t)=='match' for t in trials) else 'gap' if any(classification(t)=='potential' for t in trials) else 'contradiction','Criteria must be supported jointly by one component',components=trials)
                    else: check=self.evaluate(node,c,uncertainty=uncertainty)
                    checks.append(dict(check,criterion=c))
            checks+=self.evidence(row,query)
            if row['type']=='triage':
                raw_assertions=[self.s.get(a)['data'] for a in self.s.get(row['id'])['links'].get('assertions',[])]
                unresolved=[a for a in raw_assertions if a.get('uncertainty') in ('conflicting','ambiguous','unsupported')]
                if unresolved and query.get('criteria'): checks.append(outcome('gap','Unresolved source statements require review',statements=unresolved))
            row.update(code=code,readable=readable,facts=node,classification=classification(checks),explanations=checks)
            result.append(row)
        return {'status':'ok','query':query,'results':result,'counts':{c:sum(r['classification']==c for r in result) for c in ('match','potential','contradiction')},'boundary':'Selected criteria satisfaction is not description equality, supplier identity, fit, approval, or availability.'}

    def search(self,query):
        try: return self._search(copy.deepcopy(query))
        except UnsupportedQuery as e: return {'status':'unsupported','error':str(e)}
        except (SpecError,RecordError,sqlite3.Error,ValueError,KeyError,TypeError,IndexError) as e: return {'status':'error','error':str(e)}
