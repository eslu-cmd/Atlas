"""Bounded 0.2.1 regressions; all records are explicitly illustrative."""
import sqlite3
import unittest
import test_records
from atlas.records import Store, RecordError

class RepairTests(unittest.TestCase):
    setUp = test_records.RecordTests.setUp
    tearDown = test_records.RecordTests.tearDown
    add = test_records.RecordTests.add
    context = test_records.RecordTests.context
    approval = test_records.RecordTests.approval
    spec = test_records.RecordTests.spec

    def document(self, name):
        source=self.add('source',{'title':'ILLUSTRATIVE '+name,'uri':'illustrative://'+name})
        attachment=self.add('attachment',{'uri':'illustrative://'+name+'.pdf','media_type':'application/pdf'},source=source)
        location=self.add('location',{'locator':'signed page 1'},source=source)
        assertion=self.add('assertion',{'statement':'ILLUSTRATIVE '+name,'uncertainty':'stated'},location=location,attachments=[attachment])
        return dict(source=source,attachment=attachment,location=location,assertion=assertion)

    def signed_approval(self):
        signed=self.document('signed-approval')
        old=self.add('approval',{'type':'client_approval','decision':'approved','actor_name':'ILLUSTRATIVE signer','decision_at':'2026-09-01'},context=self.a['context'],sample=self.a['sample'],evidence=[signed['assertion']])
        note=self.document('reassociation-note')
        return old,signed,note

    def correct(self, old, note, side):
        return self.s.correct_approval(old,destination=side['context'],sample=side['sample'],evidence=[note['assertion']],**self.meta)

    def test_R1_approval_evidence_is_not_replaced_by_correction_note(self):
        """H07: preserve signed approval evidence; reassociation evidence stays on event."""
        old,signed,note=self.signed_approval()
        before=self.s.get(old)
        replacement=self.correct(old,note,self.b)
        self.assertEqual(self.s.get(replacement['record'])['links']['evidence'],[signed['assertion']])
        self.assertEqual(self.s.get(replacement['event'])['links']['evidence'],[note['assertion']])
        self.assertEqual(self.s.get(replacement['record'])['data'],before['data'])
        self.assertEqual(self.s.get(old),before)
        self.assertFalse(self.s.is_active(old))
        self.assertTrue(self.s.is_active(replacement['record']))

    def test_R1_replacement_retrieval_exposes_incoming_correction_provenance(self):
        """Replacement opens the approval document and explicitly withdrawn predecessor."""
        old,signed,note=self.signed_approval()
        new=self.correct(old,note,self.b)
        history=self.s.history(new['record'])
        provenance=history['correction_provenance']
        for rid in (old,new['event'],*signed.values(),*note.values()):
            self.assertIn(rid,provenance['records'])
        self.assertEqual(provenance['approval_status'][old],False)
        self.assertEqual(provenance['approval_status'][new['record']],True)
        self.assertNotIn(old,history['original_context'])
        self.assertIn(signed['attachment'],history['original_context'])
        self.assertNotIn(note['assertion'],history['original_context'])
        self.assertNotIn(old,{r['record']['id'] for r in self.s.product_history(self.b['product'])['approvals']})
        self.assertEqual(self.s.history(self.b['approval'])['correction_provenance']['events'],[])

    def test_R1_successive_corrections_and_handoff_provenance_survive_reopen(self):
        """Successive explicit corrections keep both notes and the original signed evidence."""
        old,signed,note=self.signed_approval()
        first=self.correct(old,note,self.b)
        second_note=self.document('second-correction-note')
        second=self.correct(first['record'],second_note,self.a)
        handoff=self.add('handoff',{'qualifications':[]},context=self.a['context'],approvals=[second['record']])
        snapshots={rid:self.s.history(rid) for rid in (second['record'],handoff)}
        self.s.close(); self.s=Store(self.path)
        for rid,expected in snapshots.items():
            actual=self.s.history(rid)
            self.assertEqual(actual,expected)
            provenance=actual['correction_provenance']
            self.assertEqual({r['id'] for r in provenance['events']},{first['event'],second['event']})
            for entry in (old,first['record'],signed['assertion'],signed['attachment'],note['assertion'],second_note['assertion']):
                self.assertIn(entry,provenance['records'])
            self.assertFalse(provenance['approval_status'][old])
            self.assertFalse(provenance['approval_status'][first['record']])
        self.assertEqual(self.s.get(second['record'])['links']['evidence'],[signed['assertion']])
        with self.assertRaises(RecordError): self.add('handoff',{'qualifications':[]},context=self.b['context'],approvals=[first['record']])

    def test_R1_failed_reassociation_preserves_evidence_and_active_state(self):
        old,signed,note=self.signed_approval()
        counts={k:len(self.s.all(k)) for k in ('approval','event')}
        with self.assertRaises(RecordError):
            self.s.correct_approval(old,destination=self.b['context'],sample=self.a['sample'],evidence=[note['assertion']],**self.meta)
        self.assertEqual(counts,{k:len(self.s.all(k)) for k in counts})
        self.assertTrue(self.s.is_active(old))
        self.assertEqual(self.s.get(old)['links']['evidence'],[signed['assertion']])

    def business_contexts(self):
        request=self.add('request',{'requirements':{}},client=self.f['client'])
        job=self.add('job',{'reference':'ILLUSTRATIVE inherited scope'},request=request)
        customization=self.add('customization',{'details':{}},version=self.a['version'],job=job)
        links=dict(version=self.a['version'],association=self.a['association'],customization=customization,packing=self.a['packing'],job=job)
        first=self.add('context',{},**links)
        redundant=self.add('context',{},**links,client=self.f['client'],request=request)
        sequence=self.add('sequence',{'label':'ILLUSTRATIVE job sampling'},product=self.a['product'],job=job)
        sample=self.add('sample',{'label':'V1'},sequence=sequence,context=first)
        return first,redundant,sample,links,request,job

    def test_R2_sample_approval_accepts_redundant_resolved_scope(self):
        """Same job/request/client via inheritance or explicit links is equivalent."""
        first,redundant,sample,*_=self.business_contexts()
        approval=self.approval(context=redundant,sample=sample)
        self.assertTrue(self.s.same_context(first,redundant))
        self.assertTrue(self.s.same_context(redundant,first))
        self.assertEqual(self.s.one(approval,'sample'),sample)
        self.s.close(); self.s=Store(self.path)
        self.assertTrue(self.s.same_context(first,redundant))

    def test_R2_handoff_accepts_equivalent_quote_and_approval_context(self):
        first,redundant,sample,*_=self.business_contexts()
        approval=self.approval(context=first,sample=sample)
        quote=self.add('quote',{'supplied':{'price':'ILLUSTRATIVE'}},context=first)
        handoff=self.add('handoff',{'qualifications':[]},context=redundant,quote=quote,approvals=[approval])
        self.assertIn(approval,self.s.history(handoff)['original_context'])

    def test_R2_exact_product_and_business_distinctions_are_not_erased(self):
        """Missing scope and different job/request/client or snapshot links stay distinct."""
        first,_,sample,links,request,job=self.business_contexts()
        # Valid alternate contexts, not contradictory inputs that fail before comparison.
        base=dict(version=self.a['version'],association=self.a['association'],client=self.f['client'])
        plain=self.add('context',{},**base)
        other_client=self.add('client',{'name':'ILLUSTRATIVE other client'})
        request2=self.add('request',{'requirements':{}},client=self.f['client'])
        job2=self.add('job',{'reference':'ILLUSTRATIVE job2'},request=request)
        association2=self.s.change_association(self.a['association'],self.f['specification'],event_type='H01',evidence=self.ev,**self.meta)['record']
        version2=self.s.revise(self.a['version'],{'label':'2'},evidence=self.ev,**self.meta)['record']
        version_association=self.add('association',{},version=version2,specification=self.f['specification'])
        custom2=self.add('customization',{'details':{}},version=self.a['version'],job=job)
        packing2=self.add('packing',{'supplied':{}},version=self.a['version'])
        pairs=[
            (plain,self.add('context',{},version=self.a['version'],association=self.a['association'])),
            (plain,self.add('context',{},**{**base,'client':other_client})),
            (self.add('context',{},**base,request=request),self.add('context',{},**base,request=request2)),
            (self.add('context',{},**base,job=job),self.add('context',{},**base,job=job2)),
            (plain,self.add('context',{},**{**base,'association':association2})),
            (plain,self.add('context',{},version=version2,association=version_association,client=self.f['client'])),
            (first,self.add('context',{},**{**links,'customization':custom2})),
            (first,self.add('context',{},**{**links,'packing':packing2})),
        ]
        for left,right in pairs:
            with self.subTest(left=left,right=right):
                self.assertFalse(self.s.same_context(left,right))
                quote=self.add('quote',{'supplied':{}},context=left)
                with self.assertRaises(RecordError): self.add('handoff',{'qualifications':[]},context=right,quote=quote)
        with self.assertRaises(RecordError): self.approval(context=plain,sample=sample)

    def test_R2_explicit_inherited_contradictions_remain_rejected(self):
        _,_,_,links,request,job=self.business_contexts()
        other=self.add('client',{'name':'ILLUSTRATIVE contradiction'})
        request2=self.add('request',{'requirements':{}},client=other)
        for extra in ({'client':other},{'request':request2}):
            with self.subTest(extra=extra),self.assertRaises(RecordError): self.add('context',{},**{**links,**extra})

    def kit_fixture(self,label='KIT',side=None):
        side=side or self.a
        component=self.add('component',{'quantity':None,'quantity_state':'not_supplied','saleability':'not_supplied'},association=side['association'])
        kit=self.add('kit',{'reference':'ILLUSTRATIVE '+label},supplier=side['supplier'])
        revision=self.add('kit_revision',{'label':'1'},kit=kit,components=[component])
        request=self.add('request',{'requirements':{}},client=self.f['client'])
        job=self.add('job',{'reference':'ILLUSTRATIVE '+label+' job'},request=request)
        custom=self.add('customization',{'details':{'printing':'ILLUSTRATIVE logo'}},kit_revision=revision,job=job)
        context=self.add('context',{},kit_revision=revision,customization=custom,job=job)
        return dict(kit=kit,revision=revision,component=component,request=request,job=job,custom=custom,context=context)

    def kit_sequence(self,k,label='sampling'):
        return self.add('sequence',{'label':label},kit=k['kit'],job=k['job'])

    def test_R3_kit_samples_notes_acceptance_and_client_approval_persist(self):
        """Kit sampling owns a permanent kit; samples/decisions retain the exact composition."""
        k=self.kit_fixture(); sequence=self.kit_sequence(k)
        sample=self.add('sample',{'label':'V1'},sequence=sequence,context=k['context'],evidence=self.ev)
        photo=self.add('attachment',{'uri':'illustrative://kit-photo','media_type':'image/png'})
        for kind in ('photo','comment','revision_request','evidence'):
            self.add('sample_note',{'type':kind,'text':'ILLUSTRATIVE kit note'},sample=sample,attachments=[photo],evidence=self.ev)
        acceptance=self.approval(context=k['context'],kind='source_one_acceptance',sample=sample)
        approval=self.approval(context=k['context'],sample=sample)
        self.assertEqual(self.s.referring(k['context'],'context','approval')[0]['id'],acceptance)
        counts={kind:len(self.s.all(kind)) for kind in ('kit_revision','version','specification','product')}
        second=self.s.revise(sample,{'label':'V2'},evidence=self.ev,**self.meta)['record']
        self.assertEqual(counts,{kind:len(self.s.all(kind)) for kind in counts})
        self.assertEqual(self.s.one(second,'context'),k['context'])
        history=self.s.sampling_history(sequence)
        self.s.close(); self.s=Store(self.path)
        self.assertEqual(self.s.sampling_history(sequence),history)
        self.assertEqual(len(history['iterations'][0]['notes']),4)
        self.assertEqual({r['record']['id'] for r in history['iterations'][0]['approvals']},{acceptance,approval})
        self.assertIn(k['component'],self.s.history(approval)['original_context'])
        self.assertNotIn(self.a['approval'],self.s.history(approval)['original_context'])

    def test_R3_sequence_has_exactly_one_permanent_owner(self):
        k=self.kit_fixture()
        valid=self.kit_sequence(k)
        self.assertEqual(self.s.one(valid,'kit'),k['kit'])
        self.assertIsNone(self.s.one(valid,'product'))
        for refs in ({},{'product':self.a['product'],'kit':k['kit']},{'kit':self.a['product']}):
            with self.subTest(refs=refs),self.assertRaises(RecordError): self.add('sequence',{'label':'invalid'},**refs)
        with self.assertRaises(RecordError): self.add('sample',{'label':'V1'},sequence=valid,context=self.a['context'])
        with self.assertRaises(RecordError): self.add('sample',{'label':'kit'},sequence=self.a['sequence'],context=k['context'])

    def test_R3_changed_composition_does_not_inherit_approval(self):
        k=self.kit_fixture(); sequence=self.kit_sequence(k)
        sample=self.add('sample',{'label':'V1'},sequence=sequence,context=k['context'])
        approval=self.approval(context=k['context'],sample=sample)
        component2=self.add('component',{'quantity':{'value':'2','unit':'pieces'},'quantity_state':'stated','saleability':'not_supplied'},association=self.a['association'])
        revision2=self.s.revise(k['revision'],{'label':'2'},links={'components':[component2]},evidence=self.ev,**self.meta)['record']
        custom2=self.add('customization',{'details':{}},kit_revision=revision2,job=k['job'])
        context2=self.add('context',{},kit_revision=revision2,customization=custom2,job=k['job'])
        self.assertFalse(self.s.same_context(k['context'],context2))
        with self.assertRaises(RecordError): self.approval(context=context2,sample=sample)
        with self.assertRaises(RecordError): self.add('handoff',{'qualifications':[]},context=context2,approvals=[approval])
        with self.assertRaises(RecordError): self.add('context',{},kit_revision=revision2,customization=k['custom'],job=k['job'])
        second=self.s.revise(sample,{'label':'V2'},links={'context':context2},evidence=self.ev,**self.meta)['record']
        self.assertEqual(self.s.one(second,'sequence'),sequence)
        self.assertEqual(self.s.referring(context2,'context','approval'),[])
        expected=self.s.history(approval)
        self.s.close(); self.s=Store(self.path)
        self.assertEqual(self.s.history(approval),expected)
        original=self.s.history(approval)['original_context']
        self.assertIn(k['component'],original); self.assertNotIn(component2,original)
        with self.assertRaises(RecordError): self.add('handoff',{'qualifications':[]},context=k['context'],approvals=[self.a['approval']])

    def test_R3_wrong_kit_client_customization_and_sequence_labels(self):
        k=self.kit_fixture(); sequence=self.kit_sequence(k)
        other=self.kit_fixture('OTHER',self.b)
        with self.assertRaises(RecordError): self.add('sample',{'label':'wrong kit'},sequence=sequence,context=other['context'])
        client=self.add('client',{'name':'ILLUSTRATIVE wrong kit client'})
        bad_context=self.add('context',{},kit_revision=k['revision'],client=client)
        with self.assertRaises(RecordError): self.add('sample',{'label':'wrong client'},sequence=sequence,context=bad_context)
        with self.assertRaises(RecordError): self.add('context',{},kit_revision=k['revision'],customization=k['custom'],job=k['job'],client=client)
        sample=self.add('sample',{'label':'V1'},sequence=sequence,context=k['context'])
        other_custom=self.add('customization',{'details':{}},kit_revision=k['revision'],job=k['job'])
        changed=self.add('context',{},kit_revision=k['revision'],customization=other_custom,job=k['job'])
        with self.assertRaises(RecordError): self.approval(context=changed,sample=sample)
        with self.assertRaises(sqlite3.IntegrityError): self.add('sample',{'label':'V1'},sequence=sequence,context=k['context'])
        sequence2=self.kit_sequence(k,'separate effort')
        self.add('sample',{'label':'V1'},sequence=sequence2,context=k['context'])
        with self.assertRaises(RecordError): self.add('sample',{'label':'V2'},sequence=sequence2,context=k['context'],previous=sample)

if __name__=='__main__': unittest.main()
