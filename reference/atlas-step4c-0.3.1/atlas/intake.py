"""Persistent source capture, review previews, and atomic reviewed commits."""
import copy
import hashlib
from .records import ROOT, UNCERTAINTY, need, dump
from .engine import Engine
from .search import Search, SLOTS, outcome, classification

class Intake:
    def __init__(self,store):
        self.s=store
        self.e=Engine(ROOT/'dictionary/atlas-A1-0.1.0.json')

    def capture(self,document,*,actor,reason,provenance='operational'):
        """Capture only source/triage records. No supplier identity is inferred."""
        d=copy.deepcopy(document); meta=dict(actor=actor,reason=reason,provenance=provenance)
        need(set(d)<={'label','kind','source','locator','statements','attachments','facts','uncertainty_facts','context'},'Unsupported intake fields')
        need(d.get('kind') in ('client_requirement','supplier_statement'), 'Separate client requirements from supplier statements')
        need(isinstance(d.get('statements'),list) and bool(d['statements']), 'Original statements required')
        need(bool(d.get('locator')), 'Precise source location required')
        self.validate_uncertainty(d.get('uncertainty_facts',[]))
        # Validate supported facts before storing; unresolved raw wording needs no encoding.
        if d.get('facts'): self.e.encode(d['facts'])
        with self.s.transaction():
            source=self.s.add('source',d['source'],**meta)
            location=self.s.add('location',{'locator':d['locator']},{'source':source},**meta)
            attachments=[self.s.add('attachment',x,{'source':source},**meta) for x in d.get('attachments',[])]
            assertions=[]
            for st in d['statements']:
                need(isinstance(st,dict) and set(st)<={'statement','uncertainty','supplied','interpretation','evidence_kind','locator'}, 'Unsupported source statement')
                st=copy.deepcopy(st); loc=location
                if 'locator' in st: loc=self.s.add('location',{'locator':st.pop('locator')},{'source':source},**meta)
                assertions.append(self.s.add('assertion',st,{'location':loc,'attachments':attachments},**meta))
            return self.s.add('triage',{'label':d['label'],'status':'unresolved','snapshot':d},{'location':location,'assertions':assertions},**meta)

    def validate_uncertainty(self,rows):
        need(isinstance(rows,list),'Uncertainty facts must be an array')
        for row in rows:
            need(isinstance(row,dict) and set(row)<={'field','scope','state','wording'} and row.get('state') in UNCERTAINTY,'Invalid uncertainty fact')
            need(isinstance(row.get('field'),str) and row['field'],'Uncertainty target required')
            need(isinstance(row.get('scope',[]),list) and all(x in self.e.d['scopes'] for x in row.get('scope',[])),'Invalid uncertainty scope')

    def criteria(self,node):
        result=[]
        def walk(n,path):
            fs=n.get('fields',{})
            for field,(block,start,end,_) in SLOTS.items():
                value=fs.get(block,{'MA':'XXXX','AR':'XXX','CF':'XXX'}[block])[start:end]
                if field=='MA_GRADE': value=fs.get('MA','XXXX')[:3]
                if 'X' not in value and '9' not in value: result.append({'field':field,'value':value,'scope':path})
            ar=fs.get('AR','XXX'); feature=fs.get('CF','XXX')[2]
            if feature not in ('X','9') and ar[:2]!='XX':
                result.append({'field':'CF_FEATURE','value':{'article':ar[:2],'closure':ar[2]=='L','token':feature},'scope':path})
            for feature in fs.get('FX',[]):
                result.append({'field':'CF_FEATURE','value':{'article':ar[:2],'closure':ar[2]=='L','token':feature},'scope':path})
            for k,v in fs.items():
                if k in ('MA','AR','CF','QC','TO','UT','OT','FX'): continue
                rows=[('DM_'+name,value) for name,value in v.items()] if k=='DM' else [(k,v)]
                for target,value in rows:
                    if value=='X': continue
                    values=value if self.e.f.get(k,{}).get('type')=='list' else [value]
                    for item in values:
                        c={'field':target,'value':item,'scope':path}
                        if Search(self.s).is_numeric(target):
                            for q in fs.get('QC',[]):
                                if q[0]==target: c['qualifier']=q[1:]
                            for t in fs.get('TO',[]):
                                if t[0]==target: c['tolerance']=t[1:]
                        result.append(c)
            for g in n.get('groups',[]):
                if 'scope' in g: walk(g['node'],path+[g['scope']])
        walk(node,[])
        return result

    def other_comparisons(self, original, candidate):
        """OTHER is a known slot plus its exact explanation, not an unknown wildcard.

        Scoped/layer groups already require unchanged recorded groups at selection.
        This handles root OT, including CF_FEATURE which has no scalar search slot.
        """
        checks=[]
        fields=candidate.get('fields',{})
        slots={**SLOTS,'CF_FEATURE':('CF',2,3,'FEATURE')}
        for target,wording in original.get('fields',{}).get('OT',[]):
            block,start,end,_=slots[target]
            default={'MA':'XXXX','AR':'XXX','CF':'XXX'}[block]
            token=fields.get(block,default)[start:end]
            preserved=[target,wording] in fields.get('OT',[])
            state='satisfies' if preserved else 'gap' if set(token)=={'X'} else 'contradiction'
            checks.append(outcome(state,'Known OTHER slot and exact explanation must be retained; reinterpretation needs an amended preview',criterion={'field':target,'other':wording},recorded_token=token,recorded_other=fields.get('OT',[])))
        return checks

    def preview(self,intake,*,facts=None,uncertainty_facts=None,actor,reason,provenance='operational'):
        record=self.s.get(intake,'triage'); snap=record['data']['snapshot']
        node=copy.deepcopy(facts if facts is not None else snap.get('facts'))
        uncertainty=copy.deepcopy(uncertainty_facts if uncertainty_facts is not None else snap.get('uncertainty_facts',[]))
        if uncertainty_facts is None:
            if not snap.get('facts') and snap.get('uncertainty'):
                uncertainty.extend({'field':'UNCLASSIFIED','state':'ambiguous','wording':x} for x in snap['uncertainty'])
            for assertion in record['links'].get('assertions',[]):
                a=self.s.get(assertion)['data']
                if a['uncertainty'] in ('ambiguous','conflicting','unsupported'):
                    uncertainty.append({'field':'UNCLASSIFIED','state':a['uncertainty'],'wording':a['statement']})
        self.validate_uncertainty(uncertainty)
        code=self.e.encode(node) if node else None
        node=self.e.decode(code) if code else {'fields':{}}
        query={'criteria':self.criteria(node),'types':['specification']}
        candidates=Search(self.s).search(query)
        need(candidates['status']=='ok','Preview criteria failed: '+str(candidates.get('error')))
        entries=[]
        for row in candidates['results']:
            # Include contradicted candidates, with explicit differences, for review.
            entries.append({k:row[k] for k in ('id','code','readable','facts','classification','explanations')})
            entries[-1]['explanations']=entries[-1]['explanations']+self.other_comparisons(node,row['facts'])
            entries[-1]['classification']=classification(entries[-1]['explanations'])
            entries[-1]['equal_description']=row['code']==code
        differences=[{'specification':r['id'],'equal_description':r['equal_description'],
                      'intake_facts':node,'candidate_facts':r['facts'],
                      'selected_criteria':r['explanations']} for r in entries]
        meta=dict(actor=actor,reason=reason,provenance=provenance)
        with self.s.transaction():
            d=self.s.register_dictionary(ROOT/'dictionary/atlas-A1-0.1.0.json',**meta)
            rid=self.s.add('intake_preview',{'facts':node,'uncertainty_facts':uncertainty,'code':code,'candidates':entries,'differences':differences},{'intake':intake,'dictionary':d},**meta)
        return {'preview':rid,'source':record,'code':code,'readable':self.e.describe(code)['description'] if code else [],'candidates':entries,'differences':differences,'uncertainty_facts':uncertainty,'boundary':'Matching is not equality. A broader intake cannot establish an additional candidate characteristic.'}

    def commit(self,preview,decision,*,actor,reason,provenance='operational'):
        p=self.s.get(preview,'intake_preview'); intake=self.s.one(preview,'intake')
        snap=self.s.get(intake)['data']['snapshot']; d=copy.deepcopy(decision)
        allowed={'action','confirmed','evidence','selected_specification','distinguishing_reason','supplier','reference','sku','version','association','version_label','subject','client','supported_code'}
        need(set(d)<=allowed,'Unsupported decision fields')
        need(d.get('confirmed') is True,'Explicit review confirmation required')
        action=d.get('action'); evidence=d.get('evidence',[])
        if snap.get('kind')=='client_requirement':
            need(action in ('triage','request'),'Client requirements stay separate from supplier offering assertions')
        need(action in ('triage','specification','offering','clarification','correction','physical_change','add_information','request'),'Unsupported intake decision')
        need(isinstance(evidence,list) and evidence,'Review needs source/evidence')
        for e in evidence: self.s.get(e,'assertion')
        payload={'decision':d,'actor':actor,'reason':reason,'provenance':provenance}
        # Both retry identity and terminal resolution are enforced inside one transaction.
        with self.s.transaction():
            previous=self.s.referring(preview,'preview','intake_decision')
            if previous:
                need(previous[0]['data']['payload']==payload,'Preview already decided differently; create another preview')
                return {'decision':previous[0]['id'],**previous[0]['data']['result'],'repeated':True}
            terminal=[x for x in self.s.referring(intake,'intake','intake_decision') if x['data']['action']!='triage']
            need(not terminal,'Intake already resolved; capture a new source for later changes')
            meta=dict(actor=actor,reason=reason,provenance=provenance)
            result={}; code=p['data']['code']; records=[]
            if action not in ('triage','request','add_information'):
                need(snap.get('kind','supplier_statement')=='supplier_statement','Client requirements cannot become supplier statements')
                need(code,'Resolved description required')
                need(not any(u['state'] in ('ambiguous','conflicting','unsupported') for u in p['data']['uncertainty_facts']), 'Resolve conflicting/unsupported facts in a new supported preview before committing')
                selected=d.get('selected_specification')
                if selected:
                    chosen=self.s.get(selected,'specification')['data']['code']
                    if chosen!=code:
                        # Reviewer must supply a complete supported description, not just click a broad match.
                        need(d.get('supported_code')==chosen,'Broad matching does not assert extra characteristics; supply reviewed complete supported_code and evidence')
                        current=self.e.decode(chosen)
                        need(all(g in current.get('groups',[]) for g in p['data']['facts'].get('groups',[])), 'Scoped/layer construction differs; create a fully supported revised preview')
                        need(all(x in current['fields'].get('UT',[]) for x in p['data']['facts']['fields'].get('UT',[])), 'Unresolved wording changes require an explicitly amended preview')
                        checks=[Search(self.s).evaluate(current,c) for c in self.criteria(p['data']['facts'])]+self.other_comparisons(p['data']['facts'],current)
                        need(all(x['state']=='satisfies' for x in checks),'Selected description contradicts or cannot support interpreted facts; amend preview with evidence')
                    code=chosen
                equal=[r for r in self.s.all('specification') if r['data']['code']==code]
                if not equal: need(bool(d.get('distinguishing_reason')),'Explain the supported distinguishing difference before issuing a new description')
                spec=self.s.issue(code,self.s.one(preview,'dictionary'),**meta)
                result['specification']=spec; records.append(spec)
            if action=='offering':
                need(bool(d.get('supplier')) and bool(d.get('reference')), 'Explicit supplier identity and offering reference required')
                product=self.s.add('product',{'reference':d['reference'],**({'sku':d['sku']} if d.get('sku') else {})},{'supplier':d['supplier']},**meta)
                version=self.s.add('version',{'label':d.get('version_label','Initial')},{'product':product},**meta)
                association=self.s.add('association',{}, {'version':version,'specification':spec,'evidence':evidence},**meta)
                result.update(product=product,version=version,association=association); records.extend([product,version,association])
            elif action in ('clarification','correction','physical_change'):
                old=d.get('association'); a=self.s.get(old,'association'); version=self.s.one(old,'version')
                need(self.s.current_association(version)['id']==old,'Stale association requires a fresh review')
                need(not self.s.referring(version,'previous','version'),'Physical version is historical; review the current offering')
                if action=='physical_change':
                    need(bool(d.get('version_label')),'Actual physical change requires supplied version label')
                    changed=self.s.revise(version,{'label':d['version_label']},evidence=evidence,**meta)
                    association=self.s.add('association',{}, {'version':changed['record'],'specification':spec,'evidence':evidence},**meta)
                    result.update(version=changed['record'],event=changed['event'],association=association)
                else:
                    changed=self.s.change_association(old,spec,event_type='H01' if action=='clarification' else 'H06',evidence=evidence,**meta)
                    result.update(version=version,association=changed['record'],event=changed['event'])
                records.extend(result.values())
            elif action=='add_information':
                subject=d.get('subject'); need(self.s.get(subject)['kind'] in ('product','version','association','kit','kit_revision'),'Existing offering context required')
                notes=[]
                for e in evidence:
                    prior=self.s.get(e); refs={**prior['links'],'subject':subject}
                    notes.append(self.s.add('assertion',prior['data'],refs,**meta))
                result.update(subject=subject,assertions=notes); records.extend([subject]+notes)
            elif action=='request':
                need(snap.get('kind')=='client_requirement','Request decision requires client intake')
                location=self.s.one(intake,'location'); source=self.s.one(location,'source')
                req=self.s.add('request',{'requirements':{'facts':p['data']['facts'],'original':snap},'qualifications':p['data']['uncertainty_facts']},{'source':source,**({'client':d['client']} if d.get('client') else {})},**meta)
                result['request']=req; records.append(req)
            rid=self.s.add('intake_decision',{'action':action,'payload':payload,'result':result},{'intake':intake,'preview':preview,'evidence':evidence,'records':list(dict.fromkeys(records))},**meta)
            self.s._key('intake_preview_decision',preview,rid)
            if action!='triage': self.s._key('intake_resolution',intake,rid)
            return {'decision':rid,**result,'repeated':False}

    def history(self,intake):
        record=self.s.history(intake)
        record['reviews']=[self.s.history(r['id']) for r in self.s.referring(intake,'intake','intake_preview')]
        record['decisions']=[self.s.history(r['id']) for r in self.s.referring(intake,'intake','intake_decision')]
        return record
