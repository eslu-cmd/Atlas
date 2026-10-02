"""Illustrative scenarios executed through on-disk SQLite, never workbook facts."""
import copy
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from atlas.records import Store, RecordError, ROOT, UNCERTAINTY
from atlas.batch import import_batch
from atlas.demo import illustrative

class RecordTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'atlas.db'
        self.s=Store(self.path)
        self.f=illustrative(self.s)
        self.a,self.b=self.f['A'],self.f['B']
        self.meta={'actor':'Illustrative test reviewer','reason':'Explicit synthetic test decision','provenance':'illustrative'}
        self.ev=[self.f['evidence']]
    def tearDown(self):
        self.s.close(); self.temp.cleanup()
    def add(self,kind,data,**refs): return self.s.add(kind,data,refs,**self.meta)
    def spec(self,code): return self.s.issue(code,self.f['dictionary'],**self.meta)
    def context(self,side=None,**updates):
        side=side or self.a
        return self.add('context',{},**{**self.s.get(side['context'])['links'],**updates})
    def approval(self,context=None,kind='client_approval',sample=None):
        decision={'client_approval':'approved','source_one_acceptance':'accepted','proof_agreement':'agreed'}[kind]
        return self.add('approval',{'type':kind,'decision':decision,'actor_name':'Illustrative actor'},context=context or self.a['context'],evidence=self.ev,**({'sample':sample} if sample else {}))

    def test_01_shared_spec_separate_histories_and_cross_links_rejected(self):
        """AT-15/19, T04.1: equal descriptions never share vendor evidence."""
        self.assertEqual(self.s.one(self.a['association'],'specification'),self.s.one(self.b['association'],'specification'))
        for side in (self.a,self.b):
            history=self.s.product_history(side['product'])
            self.assertEqual([r['id'] for r in history['quotes']],[side['quote']])
            self.assertEqual([r['record']['id'] for r in history['approvals']],[side['approval']])
            self.assertEqual([r['id'] for r in history['sequences']],[side['sequence']])
        for role in ('association','customization','packing'):
            with self.subTest(role=role),self.assertRaises(RecordError): self.context(**{role:self.b[role]})
        with self.assertRaises(RecordError): self.add('sample',{'label':'V2'},sequence=self.a['sequence'],context=self.b['context'])
        with self.assertRaises(RecordError): self.approval(sample=self.b['sample'])

    def test_02_clarification_preserves_original_quote_and_other_vendor(self):
        """AT-13, T04.7: H01 keeps identity/version and old quote association."""
        code='A1!APTX.CUB.XXX.M500.R98_125'
        refined=self.spec(code)
        out=self.s.change_association(self.a['association'],refined,event_type='H01',evidence=self.ev,**self.meta)
        current=self.s.current_association(self.a['version'])
        self.assertEqual(current['id'],out['record'])
        self.assertEqual(self.s.one(out['record'],'version'),self.a['version'])
        old=self.s.history(self.a['quote'])
        self.assertIn(self.a['association'],old['original_context'])
        self.assertNotIn(out['record'],old['original_context'])
        self.assertEqual([e['id'] for e in old['later_corrections']],[out['event']])
        self.assertEqual(self.s.current_association(self.b['version'])['id'],self.b['association'])
        with self.assertRaises(RecordError): self.s.change_association(self.a['association'],refined,event_type='H01',evidence=self.ev,**self.meta)

    def test_03_physical_artwork_and_sample_changes_are_distinct(self):
        """AT-16/15; H02, H03, H09 and T04.2/3."""
        counts={k:len(self.s.all(k)) for k in ('version','specification','customization')}
        sample=self.s.revise(self.a['sample'],{'label':'V2'},evidence=self.ev,**self.meta)['record']
        self.assertEqual(self.s.one(sample,'sequence'),self.a['sequence'])
        self.assertEqual(counts,{k:len(self.s.all(k)) for k in counts})
        art=self.add('attachment',{'uri':'illustrative://artwork-v2','media_type':'image/png'})
        custom=self.s.revise(self.a['customization'],{'details':{'printing':'two colour'}},links={'artwork':[art]},evidence=self.ev,**self.meta)['record']
        self.assertEqual(self.s.one(custom,'version'),self.a['version'])
        self.assertEqual(len(self.s.all('specification')),counts['specification'])
        with self.s.transaction():
            version=self.s.revise(self.a['version'],{'label':'Physical 2'},evidence=self.ev,**self.meta)['record']
            association=self.add('association',{},version=version,specification=self.spec('A1!APTX.CUB.XXX.M600.R98'),evidence=self.ev)
        self.assertEqual(self.s.one(version,'product'),self.a['product'])
        with self.assertRaises(RecordError): self.context(version=version,association=association)
        self.assertEqual(self.s.one(self.a['approval'],'context'),self.a['context'])
        self.assertIn(self.a['version'],self.s.history(self.a['approval'])['original_context'])

    def test_04_kit_revisions_retain_membership_and_unknown_quantity(self):
        """AT-07, H10, T04.4: no combined spec, quantity or sale inference."""
        component=self.add('component',{'quantity':None,'quantity_state':'not_supplied','saleability':'not_supplied'},association=self.a['association'])
        kit=self.add('kit',{'reference':'ILLUSTRATIVE KIT'},supplier=self.a['supplier'])
        first=self.add('kit_revision',{'label':'1'},kit=kit,components=[component])
        context=self.add('context',{},kit_revision=first,client=self.f['client'])
        quote=self.add('quote',{'supplied':{'price':'20'}},context=context)
        approval=self.approval(context=context)
        second_component=self.add('component',{'quantity':{'value':'2','unit':'pieces'},'quantity_state':'stated','saleability':'explicitly_unknown'},association=self.a['association'])
        second=self.s.revise(first,{'label':'2'},links={'components':[second_component]},evidence=self.ev,**self.meta)['record']
        for historical in (quote,approval):
            graph=self.s.history(historical)['original_context']
            self.assertIn(component,graph); self.assertNotIn(second_component,graph)
        self.assertIsNone(self.s.get(component)['data']['quantity'])
        self.assertEqual({r['id'] for r in self.s.memberships(self.a['version'])},{first,second})
        self.assertEqual(len(self.s.all('specification')),1)
        foreign=self.add('component',{'quantity':None,'quantity_state':'explicitly_unknown','saleability':'not_supplied'},association=self.b['association'])
        with self.assertRaises(RecordError): self.add('kit_revision',{'label':'bad'},kit=kit,previous=second,components=[foreign])
        with self.assertRaises(RecordError): self.add('component',{'quantity':1,'quantity_state':'not_supplied','saleability':'not_supplied'},association=self.a['association'])

    def test_05_packing_and_commercial_revisions_preserve_supplied_values(self):
        """AT-17/08, H04/H05: retain discrepancies without recalculation."""
        packing=self.s.revise(self.a['packing'],{'supplied':{'units_per_case':'500'}},evidence=self.ev,**self.meta)['record']
        context=self.context(packing=packing)
        new=self.s.revise(self.a['quote'],{'supplied':{'unit_price':'0.02','case_price':'11.37','currency':'USD'},'discrepancies':['Supplied mismatch']},links={'context':context},evidence=self.ev,**self.meta)['record']
        old=self.s.history(self.a['quote'])
        self.assertEqual(old['record']['data']['supplied']['case_price'],'10.37')
        self.assertIn(self.a['packing'],old['original_context'])
        self.assertNotIn(packing,old['original_context'])
        self.assertEqual(self.s.get(new)['data']['supplied']['case_price'],'11.37')
        self.assertEqual({e['data']['type'] for e in old['later_corrections']},{'H04','H05'})

    def test_06_proof_internal_acceptance_client_approval_and_context(self):
        """AT-15/19: three evidence types; no cross-client/artwork transfer."""
        proof=self.approval(kind='proof_agreement')
        internal=self.approval(kind='source_one_acceptance',sample=self.a['sample'])
        self.assertEqual({self.s.get(i)['data']['type'] for i in (proof,internal,self.a['approval'])},{'proof_agreement','source_one_acceptance','client_approval'})
        other=self.add('client',{'name':'ILLUSTRATIVE Other Client'})
        with self.assertRaises(RecordError): self.context(client=other)
        plain=self.context(client=[],customization=[])
        with self.assertRaises(RecordError): self.approval(context=plain)
        with self.assertRaises(RecordError): self.approval(context=plain,kind='proof_agreement')
        with self.assertRaises(RecordError): self.approval(kind='source_one_acceptance')
        custom=self.s.revise(self.a['customization'],{'details':{'artwork':'ILLUSTRATIVE new logo'}},evidence=self.ev,**self.meta)['record']
        changed=self.context(customization=custom)
        with self.assertRaises(RecordError): self.approval(context=changed,sample=self.a['sample'])
        self.assertEqual(self.s.referring(changed,'context','approval'),[])

    def test_07_misplaced_evidence_corrected_or_unresolved_with_trail(self):
        """AT-18/15, H07: withdrawal, explicit reassociation and no guessed destination."""
        out=self.s.correct_approval(self.a['approval'],destination=self.b['context'],sample=self.b['sample'],evidence=self.ev,**self.meta)
        self.assertFalse(self.s.is_active(self.a['approval']))
        self.assertTrue(self.s.is_active(out['record']))
        old=self.s.history(self.a['approval'])
        self.assertEqual(old['record']['links']['context'],[self.a['context']])
        self.assertEqual(old['later_corrections'][0]['links']['new'],[out['record']])
        unresolved=self.s.correct_approval(self.b['approval'],evidence=self.ev,**self.meta)
        self.assertIsNone(unresolved['record'])
        self.assertEqual(self.s.get(unresolved['event'])['data']['resolution'],'unresolved')
        with self.assertRaises(RecordError): self.add('handoff',{'qualifications':[]},context=self.a['context'],approvals=[self.a['approval']])
        with self.assertRaises(RecordError): self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)

    def test_08_historical_retrieval_survives_reopen(self):
        """AT-13/18/21: original context and labelled corrections persist."""
        handoff=self.add('handoff',{'qualifications':['ILLUSTRATIVE unresolved fit']},context=self.a['context'],quote=self.a['quote'],approvals=[self.a['approval']])
        self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)
        expected=self.s.history(handoff)
        self.s.close(); self.s=Store(self.path)
        self.assertEqual(self.s.history(handoff),expected)
        self.assertEqual(expected['later_corrections'][0]['data']['type'],'H07')
        self.assertIn(self.a['approval'],expected['original_context'])

    def test_09_atomic_rollback_references_and_immutable_storage(self):
        """Transaction boundary; local persistence only, not AT-24 recovery."""
        before=len(self.s.all('version'))
        with self.assertRaises(RecordError):
            with self.s.transaction():
                self.add('version',{'label':'2'},product=self.a['product'],previous=self.a['version'])
                self.add('association',{},version='missing',specification=self.f['specification'])
        self.assertEqual(len(self.s.all('version')),before)
        for sql,args in [('UPDATE records SET reason=? WHERE id=?',('changed',self.a['quote'])),('DELETE FROM records WHERE id=?',(self.a['quote'],)),('DELETE FROM links WHERE owner=?',(self.a['quote'],))]:
            with self.assertRaises(sqlite3.IntegrityError): self.s.db.execute(sql,args)
        with self.assertRaises(sqlite3.IntegrityError): self.s.db.execute('INSERT INTO links VALUES (?,?,?,?)',('missing','bad',0,self.a['quote']))
        self.assertEqual(self.s.db.execute('PRAGMA foreign_key_check').fetchall(),[])

    def test_10_disproved_claim_correction_removes_current_indication(self):
        """AT-14, H06 preserves old meanings and claims, changes only association."""
        new_spec=self.spec('A1!APPX.CUB.XXX.M500.R98')
        out=self.s.change_association(self.a['association'],new_spec,event_type='H06',evidence=self.ev,**self.meta)
        self.assertFalse(self.s.is_active(self.a['association']))
        self.assertEqual(self.s.current_association(self.a['version'])['id'],out['record'])
        self.assertEqual(self.s.get(self.f['specification'])['data']['code'],'A1!APTX.CUB.XXX.M500.R98')
        self.assertEqual(self.s.history(self.a['quote'])['later_corrections'][0]['data']['type'],'H06')

    def test_11_pair_specific_compatibility_never_transfers(self):
        """AT-05/A12: exact version pair, claimed versus confirmed."""
        left,right=self.a['version'],self.b['version']
        claim=self.add('compatibility',{'type':'supplier_claim','conditions':'ILLUSTRATIVE room temperature'},left=left,right=right,evidence=self.ev)
        confirmation=self.add('compatibility',{'type':'human_confirmation','conditions':'ILLUSTRATIVE dry fit','person':'Illustrative reviewer'},left=left,right=right,evidence=self.ev)
        self.assertEqual({r['id'] for r in self.s.compatibility(left,right)},{claim,confirmation})
        version=self.s.revise(left,{'label':'2'},evidence=self.ev,**self.meta)['record']
        self.assertEqual(self.s.compatibility(version,right),[])
        with self.assertRaises(RecordError): self.add('compatibility',{'type':'human_confirmation','conditions':'unknown'},left=left,right=right,evidence=self.ev)

    def test_12_source_batch_preserved_without_product_invention(self):
        """AT-04/08/20: exact reviewed batch, 10 descriptions, two triage cases."""
        with Store(Path(self.temp.name)/'source.db') as s:
            out=import_batch(s)
            original=json.loads((ROOT/'fixtures/verified-batch.json').read_text())
            self.assertEqual(len(out['records']),12)
            self.assertEqual(sum(bool(r['specification']) for r in out['records']),10)
            self.assertEqual(len(s.all('specification')),9) # rows 962/963 share a complete description
            self.assertEqual(s.all('product'),[]); self.assertEqual(s.all('quote'),[])
            for source,stored in zip(original['records'],out['records']):
                triage=s.get(stored['triage'])
                self.assertEqual(triage['data']['snapshot'],source)
                self.assertEqual(len(triage['links']['assertions']),len(source['cells']))
            by={r['data']['label']:r for r in s.all('triage')}
            self.assertEqual(by['V18']['data']['snapshot']['cells']['O18'],{'value':'=P18/H18','kind':'formula','cached':None})
            self.assertIn('D996',by['V993']['data']['snapshot']['cells'])
            self.assertNotIn('specification',by['V993']['links'])
            self.assertNotIn('specification',by['V1143']['links'])
            self.assertEqual(by['V1000']['data']['snapshot']['cells']['P1000']['value'],10.37)

    def test_13_findings_uncertainty_attachments_and_sampling_notes(self):
        """A04–06/H09: facts retain location, uncertainty and later findings."""
        location=self.s.one(self.f['evidence'],'location')
        for state in UNCERTAINTY:
            rid=self.add('assertion',{'statement':'ILLUSTRATIVE '+state,'uncertainty':state},location=location)
            self.assertEqual(self.s.get(rid)['data']['uncertainty'],state)
        finding=self.add('finding',{'statement':'ILLUSTRATIVE disproved statement','uncertainty':'conflicting'},assertion=self.f['evidence'],evidence=self.ev)
        self.assertIn(finding,{r['id'] for r in self.s.history(self.a['quote'])['later_corrections']})
        attachment=self.add('attachment',{'uri':'illustrative://sample-photo','media_type':'image/png','caption':'Synthetic reference; no actual photo'},source=self.f['source'])
        for kind in ('photo','comment','revision_request','evidence'):
            note=self.add('sample_note',{'type':kind,'text':'ILLUSTRATIVE note'},sample=self.a['sample'],attachments=[attachment],evidence=self.ev)
            self.assertEqual(self.s.one(note,'sample'),self.a['sample'])
        self.assertEqual(len(self.s.referring(self.a['sample'],'sample','sample_note')),4)

    def test_14_request_job_handoff_and_capability_scope(self):
        """AT-01/12/21 record coverage; no search or operations execution."""
        request=self.add('request',{'requirements':{'capacity':'not supplied'},'usage':'ILLUSTRATIVE'},client=self.f['client'],source=self.f['source'])
        job=self.add('job',{'reference':'ILLUSTRATIVE JOB'},client=self.f['client'],request=request)
        context=self.context(customization=[],request=request,job=job)
        handoff=self.add('handoff',{'qualifications':['Approval not supplied']},context=context)
        self.assertIn(request,self.s.history(handoff)['original_context'])
        with self.assertRaises(RecordError): self.add('handoff',{'qualifications':[]},context=context,quote=self.b['quote'])
        cap=self.add('capability',{'alternatives':[{'material':'PET'},{'material':'PP','condition':'separate tooling'}],'conditions':'ILLUSTRATIVE possibilities'},supplier=self.a['supplier'],evidence=self.ev)
        self.assertEqual(len(self.s.get(cap)['data']['alternatives']),2)
        self.assertEqual(len(self.s.all('product')),2)
        with self.assertRaises(RecordError): self.add('association',{},version=cap,specification=self.f['specification'])

    def test_15_identity_resolution_requires_evidence_and_keeps_references(self):
        """AT-18/H08: no equal-spec merge; explicit resolution retains old IDs."""
        with self.assertRaises(RecordError): self.s.resolve_identity(self.a['product'],self.b['product'],evidence=[],**self.meta)
        with self.assertRaises(RecordError): self.s.resolve_identity(self.a['product'],self.b['product'],evidence=self.ev,**self.meta)
        identity_evidence=self.add('assertion',{'statement':'ILLUSTRATIVE identity review: keep these distinct offerings','uncertainty':'stated','evidence_kind':'identity'},location=self.s.one(self.f['evidence'],'location'))
        event=self.s.resolve_identity(self.a['product'],None,evidence=[identity_evidence],**self.meta)
        self.assertEqual(self.s.get(event)['data']['resolution'],'identity_resolution')
        self.assertEqual(len(self.s.all('product')),2)
        self.assertEqual(self.s.one(self.a['version'],'product'),self.a['product'])

    def test_16_dictionary_release_preserved_and_duplicate_meaning_rejected(self):
        """AT-22: full issued ID and supporting dictionary persist together."""
        old=self.s.get(self.f['dictionary'])['data']
        changed=copy.deepcopy(old)
        changed['document']['tables']['GRADE']['A']['PT']='changed meaning'
        with self.assertRaises(RecordError): self.add('dictionary',changed)
        self.assertEqual(self.spec('A1!APTX.CUB.XXX.M500.R98'),self.f['specification'])
        self.s.close(); self.s=Store(self.path)
        from atlas import Engine
        self.assertEqual(Engine(self.s.get(self.f['dictionary'])['data']['document']).encode(Engine(old['document']).decode('A1!APTX.CUB.XXX.M500.R98')),'A1!APTX.CUB.XXX.M500.R98')

    def test_17_failed_correction_leaves_no_partial_replacement(self):
        before=len(self.s.all('approval'))
        with self.assertRaises(RecordError): self.s.correct_approval(self.a['approval'],destination=self.b['context'],sample=self.a['sample'],evidence=self.ev,**self.meta)
        self.assertEqual(len(self.s.all('approval')),before)
        self.assertTrue(self.s.is_active(self.a['approval']))
        with self.assertRaises(RecordError): self.s.revise(self.a['version'],{'label':'2'},evidence=[],**self.meta)
        self.assertEqual(len(self.s.all('version')),2)

    def test_18_cli_persistence_and_atomic_apply(self):
        plan=Path(self.temp.name)/'plan.json'
        plan.write_text(json.dumps([
            {'name':'ok','operation':'add','arguments':{'kind':'supplier','data':{'name':'Should roll back'},**self.meta}},
            {'name':'bad','operation':'add','arguments':{'kind':'product','data':{'reference':'broken'},'links':{'supplier':'missing'},**self.meta}}
        ]))
        result=subprocess.run([sys.executable,'-m','atlas.records_cli','--db',str(self.path),'apply',str(plan)],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(len(self.s.all('supplier')),2)
        result=subprocess.run([sys.executable,'-m','atlas.records_cli','--db',str(self.path),'history',self.a['quote']],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['record']['id'],self.a['quote'])

    def test_19_revision_lineage_rejects_cross_product_and_cross_version(self):
        with self.assertRaises(RecordError): self.add('version',{'label':'bad'},product=self.b['product'],previous=self.a['version'])
        with self.assertRaises(RecordError): self.add('association',{},version=self.b['version'],specification=self.f['specification'],previous=self.a['association'])
        with self.assertRaises(RecordError): self.s.revise(self.a['quote'],{'supplied':{'price':'5'}},links={'context':self.b['context']},evidence=self.ev,**self.meta)
        with self.assertRaises(RecordError): self.add('event',{'type':'H02','resolution':'replaced'},old=self.a['version'],new=self.b['version'],evidence=self.ev)
        self.assertEqual(len(self.s.all('version')),2)

    def test_20_sku_and_sample_labels_are_locally_scoped(self):
        sku=self.add('sku',{'value':'ILLUSTRATIVE-NEW-SKU'},product=self.a['product'])
        second=self.add('sku',{'value':'ILLUSTRATIVE-NEWER-SKU'},product=self.a['product'],previous=sku)
        self.assertEqual(self.s.one(second,'previous'),sku)
        with self.assertRaises(sqlite3.IntegrityError): self.add('sku',{'value':'ILLUSTRATIVE-NEW-SKU'},product=self.a['product'])
        self.add('sku',{'value':'ILLUSTRATIVE-NEW-SKU'},product=self.b['product'])
        with self.assertRaises(sqlite3.IntegrityError): self.add('sample',{'label':'V1'},sequence=self.a['sequence'],context=self.a['context'])
        other_sequence=self.add('sequence',{'label':'Another effort'},product=self.a['product'],client=self.f['client'])
        sample=self.add('sample',{'label':'V1'},sequence=other_sequence,context=self.a['context'])
        self.assertEqual(self.s.one(sample,'sequence'),other_sequence)

    def test_21_sampling_retrieval_exposes_photos_requests_and_decisions(self):
        photo=self.add('attachment',{'uri':'illustrative://photo-reference','media_type':'image/png'})
        note=self.add('sample_note',{'type':'revision_request','text':'ILLUSTRATIVE request'},sample=self.a['sample'],attachments=[photo])
        view=self.s.sampling_history(self.a['sequence'])
        self.assertEqual(len(view['iterations']),1)
        self.assertEqual(view['iterations'][0]['notes'][0]['record']['id'],note)
        self.assertIn(photo,view['iterations'][0]['notes'][0]['original_context'])
        self.assertEqual(view['iterations'][0]['approvals'][0]['record']['id'],self.a['approval'])

    def test_22_later_dictionary_cannot_reinterpret_issued_meaning(self):
        document=copy.deepcopy(self.s.get(self.f['dictionary'])['data']['document'])
        document['release']='ILLUSTRATIVE-incompatible-release'
        document['tables']['GRADE']['A']['PT']='Different meaning'
        path=Path(self.temp.name)/'dictionary.json'; path.write_text(json.dumps(document))
        from atlas import SpecError
        with self.assertRaises(SpecError): self.s.register_dictionary(path,**self.meta)
        self.assertEqual(len(self.s.all('dictionary')),1)

    def test_23_failed_kit_revision_rolls_back_new_component(self):
        component=self.add('component',{'quantity':None,'quantity_state':'not_supplied','saleability':'not_supplied'},association=self.a['association'])
        kit=self.add('kit',{'reference':'ILLUSTRATIVE atomic kit'},supplier=self.a['supplier'])
        revision=self.add('kit_revision',{'label':'1'},kit=kit,components=[component])
        before=len(self.s.all('component'))
        with self.assertRaises(RecordError):
            with self.s.transaction():
                wrong=self.add('component',{'quantity':None,'quantity_state':'not_supplied','saleability':'not_supplied'},association=self.b['association'])
                self.s.revise(revision,{'label':'2'},links={'components':[wrong]},evidence=self.ev,**self.meta)
        self.assertEqual(len(self.s.all('component')),before)
        self.assertEqual(len(self.s.all('kit_revision')),1)

    def test_24_history_follows_multiple_corrections_without_rewriting_original(self):
        first=self.s.change_association(self.a['association'],self.spec('A1!APTX.CUB.XXX.M500.R98_125'),event_type='H01',evidence=self.ev,**self.meta)
        second=self.s.change_association(first['record'],self.spec('A1!APPX.CUB.XXX.M500.R98_125'),event_type='H06',evidence=self.ev,**self.meta)
        history=self.s.history(self.a['quote'])
        self.assertEqual({r['id'] for r in history['later_corrections']},{first['event'],second['event']})
        self.assertIn(self.a['association'],history['original_context'])
        self.assertNotIn(second['record'],history['original_context'])
        self.assertEqual(self.s.history(self.b['quote'])['later_corrections'],[])

    def test_25_retrospective_quote_still_shows_prior_correction_to_its_context(self):
        change=self.s.change_association(self.a['association'],self.spec('A1!APPX.CUB.XXX.M500.R98'),event_type='H06',evidence=self.ev,**self.meta)
        old_quote=self.add('quote',{'supplied':{'price':'historical supplied value'}},context=self.a['context'])
        self.assertEqual(self.s.history(old_quote)['later_corrections'][0]['id'],change['event'])

if __name__=='__main__': unittest.main()
