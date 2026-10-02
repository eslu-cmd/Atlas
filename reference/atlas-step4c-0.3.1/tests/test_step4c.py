"""Step 4C independent expected outcomes against on-disk persistent operations.
All fixtures are illustrative except the preserved reviewed batch test.
"""
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from atlas.records import Store, ROOT, RecordError
from atlas.engine import Engine
from atlas.demo import illustrative
from atlas.batch import import_batch
from atlas.intake import Intake
from atlas.search import Search
from atlas.phrases import Phrases

class Step4CTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'store.sqlite'
        self.s=Store(self.path); self.f=illustrative(self.s); self.a=self.f['A']; self.b=self.f['B']
        self.meta=dict(actor='Illustrative reviewer',reason='Synthetic acceptance evidence',provenance='illustrative')
        self.ev=[self.f['evidence']]; self.i=Intake(self.s); self.search=Search(self.s)
    def tearDown(self): self.s.close(); self.tmp.cleanup()
    def add(self,k,d,**refs): return self.s.add(k,d,refs,**self.meta)
    def spec(self,facts):
        code=facts if isinstance(facts,str) else Engine(ROOT/'dictionary/atlas-A1-0.1.0.json').encode(facts)
        return self.s.issue(code,self.f['dictionary'],**self.meta)
    def query(self,criteria,**kwargs):
        out=self.search.search({'criteria':criteria,**kwargs}); self.assertEqual(out['status'],'ok',out); return out['results']
    def row(self,id,criteria,**kwargs): return next(r for r in self.query(criteria,**kwargs) if r['id']==id)
    def c(self,f,v,**kwargs): return dict(field=f,value=v,**kwargs)
    def capture(self,facts=None,kind='supplier_statement',uncertainty=None):
        return self.i.capture({'label':'ILLUSTRATIVE intake','kind':kind,'source':{'title':'ILLUSTRATIVE quotation','uri':'illustrative://source'},'locator':{'worksheet':'Sheet','cells':['F2']},'statements':[{'statement':'Original supplied words','uncertainty':'stated','supplied':{'value':'=P2/H2','unit':'mL','formula':'=P2/H2','cached':None}}],'attachments':[{'uri':'illustrative://photo','media_type':'image/png'}],'facts':facts,'uncertainty_facts':uncertainty or []},**self.meta)
    def preview(self,id,**kwargs): return self.i.preview(id,**kwargs,**self.meta)['preview']
    def commit(self,p,action='specification',**kwargs): return self.i.commit(p,{'action':action,'confirmed':True,'evidence':self.ev,**kwargs},**self.meta)
    def counts(self): return {k:len(self.s.all(k)) for k in ('specification','product','version','association','intake_decision')}
    def offering_row(self,product,criteria,**kwargs): return next(r for r in self.query(criteria,types=['offering'],**kwargs) if r['product']==product)
    def context(self,side=None,**refs): return self.add('context',{},**{**self.s.get((side or self.a)['context'])['links'],**refs})

    def test_01_source_review_commit_search_history_reopen(self):
        """AT-02/11/20: source → preview → exact reuse → offering → search → reopen."""
        intake=self.capture({'fields':{'MA':'APTX','AR':'CUB','CA':'M500','FI':'R98'}})
        before=self.counts(); p=self.preview(intake); self.assertEqual(before,self.counts())
        out=self.commit(p,'offering',supplier=self.a['supplier'],reference='REVIEWED-NEW')
        self.assertEqual(out['specification'],self.f['specification']); self.assertEqual(len(self.s.all('specification')),1)
        row=self.offering_row(out['product'],[self.c('CA',{'value':'0.5','unit':'L'})]); self.assertEqual(row['classification'],'match')
        self.assertEqual(self.offering_row(out['product'],[],evidence={'quotation':True})['classification'],'potential')
        self.s.close(); self.s=Store(self.path); self.i=Intake(self.s)
        h=self.i.history(intake); self.assertEqual(len(h['decisions']),1)
        snapshot=h['record']['data']['snapshot']; self.assertEqual(snapshot['statements'][0]['supplied']['cached'],None)
        self.assertEqual(snapshot['statements'][0]['supplied']['formula'],'=P2/H2')
        self.assertEqual(snapshot['locator']['cells'],['F2']); self.assertEqual(len(snapshot['attachments']),1)

    def test_02_broad_match_not_equality_or_silent_association(self):
        """AT-02: broad matching cannot assert candidate's missing material and rim."""
        t=self.capture({'fields':{'AR':'CUB','CA':'M500'}}); p=self.preview(t)
        candidates=self.s.get(p)['data']['candidates']; self.assertEqual(candidates[0]['classification'],'match'); self.assertFalse(candidates[0]['equal_description'])
        before=self.counts()
        with self.assertRaises(RecordError): self.commit(p,'offering',supplier=self.a['supplier'],reference='BROAD',selected_specification=self.f['specification'])
        self.assertEqual(before,self.counts())
        out=self.commit(p,'offering',supplier=self.a['supplier'],reference='BROAD',selected_specification=self.f['specification'],supported_code='A1!APTX.CUB.XXX.M500.R98')
        self.assertEqual(out['specification'],self.f['specification'])

    def test_03_new_difference_and_close_values_remain_distinct(self):
        t=self.capture({'fields':{'AR':'CUB','CA':'M500','FI':'R98_125'}}); p=self.preview(t)
        with self.assertRaises(RecordError): self.commit(p)
        out=self.commit(p,distinguishing_reason='Source explicitly states 98.125 mm rim')
        self.assertNotEqual(out['specification'],self.f['specification'])
        self.assertEqual(len(self.s.all('specification')),2)

    def test_04_rejected_commit_is_atomic(self):
        t=self.capture({'fields':{'AR':'BGX','CL':'WHITE'}}); p=self.preview(t); before=self.counts()
        with self.assertRaises((RecordError,sqlite3.Error)): self.commit(p,'offering',supplier=self.a['supplier'],reference='ILLUSTRATIVE-A',distinguishing_reason='Bag, white')
        self.assertEqual(before,self.counts())

    def test_05_repeat_submission_after_reopen_no_duplicates(self):
        t=self.capture({'fields':{'AR':'BGX'}}); p=self.preview(t)
        first=self.commit(p,distinguishing_reason='Bag'); before=self.counts()
        self.s.close(); self.s=Store(self.path); self.i=Intake(self.s)
        second=self.commit(p,distinguishing_reason='Bag'); self.assertEqual(first['decision'],second['decision']); self.assertTrue(second['repeated']); self.assertEqual(before,self.counts())
        with self.assertRaises(RecordError): self.commit(p,distinguishing_reason='Changed reason payload')

    def test_06_client_requirement_never_supplier_claim(self):
        t=self.capture({'fields':{'AR':'CUB','CA':'M500'}},kind='client_requirement'); p=self.preview(t)
        with self.assertRaises(RecordError): self.commit(p,'offering',supplier=self.a['supplier'],reference='NO',distinguishing_reason='Request')
        out=self.commit(p,'request',client=self.f['client']); self.assertEqual(self.s.get(out['request'])['kind'],'request'); self.assertEqual(len(self.s.all('product')),2)
        with self.assertRaises(RecordError): self.commit(self.preview(t),'add_information',subject=self.a['product'])

    def test_07_triage_resolution_append_and_original_preserved(self):
        t=self.capture({'fields':{'AR':'BGX'}},uncertainty=[{'field':'MA_GRADE','state':'conflicting','wording':'virgin/recycled'}]); original=self.s.get(t)
        p=self.preview(t); self.commit(p,'triage')
        with self.assertRaises(RecordError): self.commit(self.preview(t),distinguishing_reason='Bag')
        r=self.row(t,[self.c('AR_CLASS','BG'),self.c('MA_GRADE','BKV')],types=['triage']); self.assertEqual(r['classification'],'potential')
        p2=self.preview(t,facts={'fields':{'MA':'BKVX','AR':'BGX'}},uncertainty_facts=[])
        out=self.commit(p2,distinguishing_reason='Supported virgin kraft resolution')
        self.assertEqual(original,self.s.get(t)); self.assertEqual(len(self.i.history(t)['decisions']),2)
        self.assertEqual(self.row(t,[],types=['triage'])['resolution'],'resolved_with_original_retained')
        self.assertEqual(self.row(out['specification'],[self.c('MA_GRADE','BKV')],types=['specification'])['classification'],'match')

    def test_08_explicit_narrowing_only_selected_fields(self):
        ids=[self.spec('A1!APPX.CUB.XXX.M500.R90'),self.spec('A1!APTX.CUB.XXX.M600.R98')]
        broad=[self.c('AR_CLASS','CU')]; narrowed=broad+[self.c('CA','M500')]
        self.assertEqual(self.row(ids[1],broad,types=['specification'])['classification'],'match')
        self.assertEqual(self.row(ids[1],narrowed,types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(ids[0],narrowed,types=['specification'])['classification'],'match')

    def test_09_missing_negative_na_contradictory(self):
        unknown=self.spec('A1!BKRX.BGX.XXX.X.X'); negative=self.spec('A1!BKR N.BGX.XXX.0.X'.replace(' ',''))
        q=[self.c('MA_TREATMENT','P')]
        self.assertEqual(self.row(unknown,q,types=['specification'])['classification'],'potential')
        self.assertEqual(self.row(negative,q,types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(negative,[self.c('CA','M500')],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(negative,[self.c('CA','0')],types=['specification'])['classification'],'match')

    def test_10_exact_units_quantity_roles_and_dimensions(self):
        sid=self.spec({'fields':{'AR':'CUB','CA':'M500','DM':{'TOP_DIA':{'value':'1','unit':'in'}}}})
        self.assertEqual(self.row(sid,[self.c('CA',{'value':'0.5','unit':'L'}),self.c('DM_TOP_DIA','25.4')],types=['specification'])['classification'],'match')
        self.assertEqual(self.row(sid,[self.c('CA','G500')],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(sid,[self.c('FI','R25_4')],types=['specification'])['classification'],'potential')
        self.assertEqual(self.s.all('compatibility'),[])

    def test_11_interval_containment_not_overlap(self):
        sid=self.spec('A1!APTX.CUB.XXX.M480-520.X')
        for want,expected in [('M470-530','match'),('M500-550','contradiction'),('M500','contradiction')]:
            self.assertEqual(self.row(sid,[self.c('CA',want)],types=['specification'])['classification'],expected)

    def test_12_tolerance_and_approximate(self):
        sid=self.spec({'fields':{'AR':'CUB','CA':'M500','TO':[['CA','10','10']]}})
        self.assertEqual(self.row(sid,[self.c('CA','M490-510')],types=['specification'])['classification'],'match')
        self.assertEqual(self.row(sid,[self.c('CA','M495-505')],types=['specification'])['classification'],'contradiction')
        approx=self.spec({'fields':{'AR':'CUB','CA':'M500','QC':[['CA','APPROXIMATE','UNKNOWN','-']]}})
        self.assertEqual(self.row(approx,[self.c('CA','M500')],types=['specification'])['classification'],'potential')

    def test_13_measurement_basis_and_conditions(self):
        sid=self.spec({'fields':{'AR':'CUB','CA':'M500','QC':[['CA','REPORTED','BRIM','20 C']]}})
        self.assertEqual(self.row(sid,[self.c('CA','M500',qualifier=['REPORTED','FILL','20 C'])],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(sid,[self.c('CA','M500',qualifier=['REPORTED','BRIM','40 C'])],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(sid,[self.c('CA','M500',qualifier=['REPORTED','BRIM','20 C'])],types=['specification'])['classification'],'match')

    def test_14_inside_does_not_satisfy_outside(self):
        sid=self.spec({'fields':{'MA':'BKRX','AR':'BGX'},'groups':[{'scope':'INSIDE','node':{'fields':{'MA':'XXXG'}}}]})
        self.assertEqual(self.row(sid,[self.c('MA_TREATMENT','G',scope=['INSIDE'])],types=['specification'])['classification'],'match')
        self.assertEqual(self.row(sid,[self.c('MA_TREATMENT','G',scope=['OUTSIDE'])],types=['specification'])['classification'],'potential')

    def test_15_layers_never_fictional_combination(self):
        sid=self.spec({'fields':{'AR':'BGX'},'groups':[{'direction':'O','layers':[{'fields':{'MA':'BKRX','CL':'WHITE'}},{'fields':{'MA':'APTX','CL':'BROWN'}}]}]})
        r=self.row(sid,[{'layer':[self.c('MA_GRADE','APT'),self.c('CL','WHITE')]}],types=['specification']); self.assertNotEqual(r['classification'],'match')
        self.assertEqual(self.row(sid,[{'layer':[self.c('MA_GRADE','APT'),self.c('CL','BROWN')]}],types=['specification'])['classification'],'match')
        r=self.row(sid,[self.c('laminate',True)],types=['specification']); self.assertEqual(r['classification'],'match'); self.assertEqual(len(r['facts']['groups'][0]['layers']),2)
        self.assertEqual(self.search.search({'criteria':[{'layer':[self.c('TH','10')]}]})['status'],'unsupported')

    def test_16_capability_contains_target_not_product_semantics(self):
        cap=self.add('capability',{'alternatives':[{'fields':{'AR':'CUB','CA':'M300-700'}}],'conditions':[]},supplier=self.a['supplier'])
        r=self.row(cap,[self.c('CA','M500')],types=['capability']); self.assertEqual(r['classification'],'match'); self.assertFalse(r['availability_established'])
        self.assertEqual(self.row(cap,[self.c('CA','M800')],types=['capability'])['classification'],'contradiction')

    def test_17_capability_alternatives_cannot_be_combined(self):
        cap=self.add('capability',{'alternatives':[{'fields':{'MA':'APTX','CA':'M300'}},{'fields':{'MA':'APPX','CA':'M500'}}],'conditions':[]},supplier=self.a['supplier'])
        r=self.row(cap,[self.c('MA_GRADE','APT'),self.c('CA','M500')],types=['capability']); self.assertEqual(r['classification'],'contradiction')
        conditional=self.add('capability',{'alternatives':[{'fields':{'CA':'M300-700'}}],'conditions':['requires tooling review']},supplier=self.a['supplier'])
        self.assertEqual(self.row(conditional,[self.c('CA','M500')],types=['capability'])['classification'],'potential')

    def test_18_two_suppliers_no_cross_evidence_join(self):
        # Withdraw A approval; B has an approval but only a quote in a different context.
        self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)
        new=self.s.change_association(self.b['association'],self.spec('A1!APTX.CUB.XXX.M500.R98_1'),event_type='H01',evidence=self.ev,**self.meta)
        context=self.context(self.b,association=new['record'])
        self.add('approval',{'type':'client_approval','decision':'approved','actor_name':'B client'},context=context,evidence=self.ev)
        rows=self.query([self.c('CA','M500')],types=['offering'],evidence={'quotation':True,'approval':'client_approval'})
        self.assertFalse(any(r['classification']=='match' for r in rows))
        spec=self.row(self.f['specification'],[],types=['specification'],evidence={'quotation':True,'approval':'client_approval'}); self.assertEqual(spec['classification'],'potential')

    def test_19_client_customization_sample_scope(self):
        other=self.add('client',{'name':'Other'})
        self.assertEqual(self.offering_row(self.a['product'],[],scope={'client':other},evidence={'approval':'client_approval'})['classification'],'potential')
        c=self.s.revise(self.a['customization'],{'details':{'printing':'two colour'}},evidence=self.ev,**self.meta)['record']
        self.context(customization=c)
        self.assertEqual(self.offering_row(self.a['product'],[],scope={'customization':c},evidence={'approval':'client_approval'})['classification'],'potential')
        sample=self.s.revise(self.a['sample'],{'label':'V2'},evidence=self.ev,**self.meta)['record']
        self.assertEqual(self.offering_row(self.a['product'],[],scope={'sample':sample},evidence={'approval':'client_approval'})['classification'],'potential')
        self.assertEqual(len(self.s.all('version')),2)

    def test_20_approval_forms_withdrawn_and_rejected(self):
        r=self.offering_row(self.a['product'],[],evidence={'approval':'proof_agreement'}); self.assertEqual(r['classification'],'potential')
        self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'contradiction')
        self.add('approval',{'type':'source_one_acceptance','decision':'rejected','actor_name':'Reviewer'},context=self.a['context'],sample=self.a['sample'],evidence=self.ev)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'source_one_acceptance'})['classification'],'contradiction')

    def test_21_quotation_sampling_photos_selected_only(self):
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'photos':True})['classification'],'potential')
        attachment=self.add('attachment',{'uri':'illustrative://photo','media_type':'image/png'})
        self.add('sample_note',{'type':'photo','text':'Received photo'},sample=self.a['sample'],attachments=[attachment])
        r=self.offering_row(self.a['product'],[],evidence={'quotation':True,'sampling':True,'photos':True}); self.assertEqual(r['classification'],'match')
        self.assertEqual(self.offering_row(self.b['product'],[],evidence={'photos':True})['classification'],'potential')

    def kit(self):
        component=self.add('component',{'quantity':None,'quantity_state':'not_supplied','saleability':'not_supplied'},association=self.a['association'])
        kit=self.add('kit',{'reference':'ILLUSTRATIVE kit'},supplier=self.a['supplier'])
        rev=self.add('kit_revision',{'label':'1'},kit=kit,components=[component]); context=self.add('context',{},kit_revision=rev,client=self.f['client'])
        return kit,rev,context

    def test_22_kit_browsing_membership_no_component_approval_inheritance(self):
        kit,rev,context=self.kit()
        r=self.row(rev,[self.c('kind','kit'),{'component':[self.c('CA','M500')]}],types=['kit']); self.assertEqual(r['classification'],'match'); self.assertIsNone(r['code'])
        self.assertEqual(self.row(rev,[],types=['kit'],evidence={'approval':'client_approval'})['classification'],'potential')
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'kit_membership':True})['classification'],'match')
        self.assertEqual(r['components'][0]['record']['data']['quantity'],None)

    def test_23_kit_revision_evidence_scope(self):
        kit,rev,context=self.kit()
        self.add('approval',{'type':'client_approval','decision':'approved','actor_name':'Client'},context=context,evidence=self.ev)
        new=self.s.revise(rev,{'label':'2'},evidence=self.ev,**self.meta)['record']
        self.add('context',{},kit_revision=new,client=self.f['client'])
        self.assertEqual(self.row(new,[],types=['kit'],evidence={'approval':'client_approval'})['classification'],'potential')
        self.assertFalse(any(r['id']==rev for r in self.query([],types=['kit'])))
        self.assertEqual(self.row(rev,[],types=['kit'],historical=True,evidence={'approval':'client_approval'})['classification'],'match')

    def test_24_clarification_changes_current_retains_original_quote(self):
        t=self.capture({'fields':{'MA':'APTX','AR':'CUB','CA':'M500','FI':'R98_125'}}); p=self.preview(t)
        out=self.commit(p,'clarification',association=self.a['association'],distinguishing_reason='Exact rim clarified')
        self.assertEqual(out['version'],self.a['version'])
        self.assertEqual(self.offering_row(self.a['product'],[self.c('FI','R98_125')])['classification'],'match')
        self.assertEqual(self.offering_row(self.a['product'],[self.c('FI','R98')])['classification'],'contradiction')
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'potential')
        old=self.s.history(self.a['quote']); self.assertIn(self.a['association'],old['original_context']); self.assertNotIn(out['association'],old['original_context']); self.assertEqual(old['later_corrections'][0]['data']['type'],'H01')

    def test_25_correction_and_physical_change(self):
        t=self.capture({'fields':{'MA':'APPX','AR':'CUB','CA':'M500','FI':'R98'}})
        out=self.commit(self.preview(t),'correction',association=self.a['association'],distinguishing_reason='PET claim disproved; PP supported')
        self.assertEqual(out['version'],self.a['version']); self.assertFalse(self.s.is_active(self.a['association']))
        t2=self.capture({'fields':{'MA':'APPX','AR':'CUB','CA':'M600','FI':'R98'}})
        out2=self.commit(self.preview(t2),'physical_change',association=out['association'],version_label='Physical 2',distinguishing_reason='Changed capacity')
        self.assertNotEqual(out2['version'],self.a['version']); self.assertEqual(self.s.one(out2['version'],'product'),self.a['product'])
        self.assertEqual(self.offering_row(self.a['product'],[self.c('CA','M500')])['classification'],'contradiction')
        self.assertIn(self.a['version'],self.s.history(self.a['approval'])['original_context'])

    def test_26_add_information_does_not_create_physical_version(self):
        t=self.capture(); p=self.preview(t); before=self.counts(); out=self.commit(p,'add_information',subject=self.a['product'])
        self.assertEqual(self.counts()['version'],before['version']); self.assertEqual(self.s.one(out['assertions'][0],'subject'),self.a['product'])
        self.assertEqual(self.offering_row(self.a['product'],[])['additional_assertions'][0]['id'],out['assertions'][0])

    def test_27_phrase_requires_confirmation_and_preserves_unrecognized(self):
        ph=Phrases(self.s); review=ph.propose('PET cups 500 ml cheap 16 oz',**self.meta)
        self.assertFalse(review['executed']); self.assertTrue(review['unsupported']); self.assertIn('oz',[x['text'] for x in review['unsupported']])
        with self.assertRaises(RecordError): ph.execute(review['review'])
        with self.assertRaises(RecordError): ph.confirm(review['review'],review['proposed'],confirmed=False,acknowledged=review['unsupported'],**self.meta)
        with self.assertRaises(RecordError): ph.confirm(review['review'],review['proposed'],confirmed=True,acknowledged=[],**self.meta)
        confirmation=ph.confirm(review['review'],review['proposed'],confirmed=True,acknowledged=review['unsupported'],**self.meta)
        self.s.close(); self.s=Store(self.path); result=Phrases(self.s).execute(confirmation)
        self.assertEqual(result['search']['status'],'ok'); self.assertEqual(result['interpretation']['data']['phrase'],'PET cups 500 ml cheap 16 oz')

    def test_28_phrase_edit_explicit_narrowing_no_unit_guess(self):
        ph=Phrases(self.s); r=ph.propose('bags height 2 in white',**self.meta)
        self.assertEqual(r['unsupported'],[]); self.assertIn(self.c('DM_HEIGHT',{'value':'2','unit':'in'}),r['proposed']['criteria'])
        ambiguous=ph.propose('cups 16 oz',**self.meta)
        self.assertFalse(any(c['field']=='CA' for c in ambiguous['proposed']['criteria']))
        edited={'criteria':[self.c('AR_CLASS','CU'),self.c('CA','M500')],'types':['offering']}
        confirm=ph.confirm(ambiguous['review'],edited,confirmed=True,acknowledged=ambiguous['unsupported'],**self.meta)
        self.assertEqual(ph.execute(confirm)['search']['counts']['match'],2)

    def test_29_empty_unsupported_and_failed_are_distinct(self):
        with Store(Path(self.tmp.name)/'empty.db') as s:
            self.assertEqual(Search(s).search({'criteria':[]})['results'],[])
            self.assertEqual(Search(s).search({'criteria':[]})['status'],'ok')
        self.assertEqual(self.search.search({'criteria':[self.c('magic','x')]})['status'],'unsupported')
        self.assertEqual(self.search.search({'criteria':[],'scope':{'client':'nonexistent'}})['status'],'error')

    def test_30_preserved_batch_no_promotion_and_structured_triage(self):
        with Store(Path(self.tmp.name)/'batch.db') as s:
            ids=import_batch(s); self.assertEqual(len(s.all('triage')),12); self.assertEqual(len(s.all('specification')),9)
            self.assertEqual(s.all('product'),[]); self.assertEqual(s.all('quote'),[])
            by={r['source_record']:r for r in ids['records']}; self.assertEqual(by['V962']['specification'],by['V963']['specification'])
            r=Search(s).search({'criteria':[self.c('AR_CLASS','BG')],'types':['triage']})
            found=next(x for x in r['results'] if x['label']=='V993'); self.assertEqual(found['classification'],'match')
            self.assertEqual(s.get(by['V18']['triage'])['data']['snapshot']['cells']['O18']['value'],'=P18/H18')
            for label in ('V993','V1143'): self.assertIsNone(by[label]['specification'])
            self.assertTrue(all(x['resolution']=='unresolved' for x in r['results']))
            conflict=Search(s).search({'criteria':[self.c('FS','VIRGIN')],'types':['triage']})
            row=next(x for x in conflict['results'] if x['label']=='V993')
            self.assertEqual(row['classification'],'potential'); self.assertIn('conflicting',row['explanations'][0]['reason'])

    def test_31_cli_visible_errors_and_structured_search(self):
        path=Path(self.tmp.name)/'query.json'; path.write_text(json.dumps({'criteria':[self.c('CA','M500')],'types':['offering']}))
        proc=subprocess.run([sys.executable,'-m','atlas.workflow_cli','--db',str(self.path),'search',str(path)],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr); self.assertEqual(json.loads(proc.stdout)['counts']['match'],2)
        path.write_text('{"criteria":[{"field":"unsupported","value":"x"}]}')
        proc=subprocess.run([sys.executable,'-m','atlas.workflow_cli','--db',str(self.path),'search',str(path)],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(proc.returncode,3); self.assertEqual(json.loads(proc.stdout)['status'],'unsupported')

    def test_32_equivalent_business_context_evidence_join(self):
        req=self.add('request',{'requirements':{}},client=self.f['client']); job=self.add('job',{'reference':'J'},request=req)
        c1=self.add('context',{},version=self.a['version'],association=self.a['association'],job=job)
        c2=self.add('context',{},version=self.a['version'],association=self.a['association'],job=job,request=req,client=self.f['client'])
        self.add('quote',{'supplied':{'price':'1'}},context=c1)
        self.add('approval',{'type':'client_approval','decision':'approved','actor_name':'Client'},context=c2,evidence=self.ev)
        r=self.offering_row(self.a['product'],[],scope={'job':job},evidence={'quotation':True,'approval':'client_approval'})
        self.assertEqual(r['classification'],'match')

    def test_33_photos_and_approval_cannot_cross_sample_iterations(self):
        photo=self.add('attachment',{'uri':'illustrative://v2','media_type':'image/png'})
        v2=self.s.revise(self.a['sample'],{'label':'V2'},evidence=self.ev,**self.meta)['record']
        self.add('sample_note',{'type':'photo','text':'V2 only'},sample=v2,attachments=[photo])
        r=self.offering_row(self.a['product'],[],evidence={'photos':True,'approval':'client_approval'})
        self.assertNotEqual(r['classification'],'match')
        self.add('approval',{'type':'client_approval','decision':'approved','actor_name':'Client'},context=self.a['context'],sample=v2,evidence=self.ev)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'photos':True,'approval':'client_approval'})['classification'],'match')

    def test_34_membership_search_needs_no_commercial_context(self):
        t=self.capture({'fields':{'AR':'BGX'}})
        out=self.commit(self.preview(t),'offering',supplier=self.a['supplier'],reference='UNPRICED',distinguishing_reason='Bag')
        component=self.add('component',{'quantity':None,'quantity_state':'not_supplied','saleability':'not_supplied'},association=out['association'])
        kit=self.add('kit',{'reference':'UNPRICED KIT'},supplier=self.a['supplier'])
        self.add('kit_revision',{'label':'1'},kit=kit,components=[component])
        self.assertEqual(self.offering_row(out['product'],[],evidence={'kit_membership':True})['classification'],'match')
        self.assertEqual(self.offering_row(out['product'],[],evidence={'quotation':True,'kit_membership':True})['classification'],'potential')

    def test_35_unresolved_raw_assertion_blocks_commit(self):
        doc={'label':'Conflict','kind':'supplier_statement','source':{'title':'Conflicting source','uri':'illustrative://conflict'},'locator':'line 1','statements':[{'statement':'PET or PP','uncertainty':'conflicting'}],'facts':{'fields':{'AR':'CUB'}}}
        t=self.i.capture(doc,**self.meta); p=self.preview(t)
        with self.assertRaises(RecordError): self.commit(p,distinguishing_reason='Cup')
        self.assertEqual(self.row(t,[self.c('AR_CLASS','CU')],types=['triage'])['classification'],'potential')
        self.assertEqual(len(self.i.history(t)['reviews']),1)

    def test_36_explicit_no_handle_and_surface_negative(self):
        sid=self.spec('A1!BKRX.BGX.XXN.X.X')
        q=[self.c('CF_FEATURE',{'article':'BG','closure':False,'token':'T'})]
        self.assertEqual(self.row(sid,q,types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(sid,[self.c('CF_FEATURE',{'article':'BG','closure':False,'token':'N'})],types=['specification'])['classification'],'match')
        negative=self.spec({'fields':{'AR':'BGX','MW':'NO'}})
        self.assertEqual(self.row(negative,[self.c('MW','YES')],types=['specification'])['classification'],'contradiction')

    def test_37_unknown_states_remain_explicit_and_not_matches(self):
        for state in ('not_supplied','explicitly_unknown','ambiguous','conflicting','unsupported'):
            t=self.capture({'fields':{'AR':'BGX'}},uncertainty=[{'field':'CL','state':state,'wording':'Original'}])
            r=self.row(t,[self.c('CL','WHITE')],types=['triage'])
            self.assertEqual(r['classification'],'potential'); self.assertIn(state,r['explanations'][0]['reason'])
        t=self.capture({'fields':{'AR':'BGX'}},uncertainty=[{'field':'CA','state':'not_applicable'}])
        self.assertEqual(self.row(t,[self.c('CA','M500')],types=['triage'])['classification'],'contradiction')

    def test_38_current_withdrawal_and_historical_search(self):
        self.add('event',{'type':'H06','resolution':'withdrawn'},old=self.a['association'],evidence=self.ev)
        current=self.offering_row(self.a['product'],[self.c('MA_GRADE','APT')]); self.assertEqual(current['classification'],'potential'); self.assertIsNone(current['code'])
        old=[r for r in self.query([self.c('MA_GRADE','APT')],types=['offering'],historical=True) if r['product']==self.a['product']][0]
        self.assertEqual(old['classification'],'match'); self.assertFalse(old['current'])
        self.assertIn(self.a['association'],self.s.history(self.a['approval'])['original_context'])

    def test_39_lids_bags_and_complete_code_inspection(self):
        lid=self.spec('A1!APSX.BWX.XXX.X.X+FR:CLOSURE.LP:D')
        self.assertEqual(self.row(lid,[self.c('kind','lid')],types=['specification'])['classification'],'match')
        self.assertEqual(self.row(lid,[self.c('kind','cup')],types=['specification'])['classification'],'contradiction')
        r=self.row(lid,[self.c('LP','D')],types=['specification']); self.assertTrue(r['code'].endswith('LP:D')); self.assertTrue(r['readable'])

    def test_40_broad_selection_cannot_override_known_conflict(self):
        t=self.capture({'fields':{'MA':'APPX','AR':'CUB','CA':'M500'}}); p=self.preview(t)
        with self.assertRaises(RecordError): self.commit(p,'offering',supplier=self.a['supplier'],reference='CONFLICT',selected_specification=self.f['specification'],supported_code='A1!APTX.CUB.XXX.M500.R98')
        self.assertEqual(len(self.s.all('product')),2)

    def test_41_capability_legacy_unstructured_remains_visible(self):
        cap=self.add('capability',{'alternatives':[{'material':'PP','range':'300-700 mL'}],'conditions':[]},supplier=self.a['supplier'])
        r=self.row(cap,[self.c('CA','M500')],types=['capability']); self.assertEqual(r['classification'],'potential'); self.assertEqual(r['alternatives'][0]['range'],'300-700 mL')

    def test_42_contradiction_not_hidden_by_another_missing_field(self):
        sid=self.spec('A1!APPX.CUB.XXX.X.X')
        r=self.row(sid,[self.c('MA_GRADE','APT'),self.c('FI','R90')],types=['specification']); self.assertEqual(r['classification'],'contradiction')
        self.assertEqual([x['state'] for x in r['explanations']],['contradiction','gap'])

if __name__=='__main__': unittest.main()
