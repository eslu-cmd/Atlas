"""0.3.1 regressions: illustrative persistent scenarios; expected outcomes independent of matcher."""
import unittest
import test_step4c as original
from atlas.records import Store, RecordError
from atlas.intake import Intake
from atlas.search import Search

class Repair031Tests(unittest.TestCase):
    setUp=original.Step4CTests.setUp
    tearDown=original.Step4CTests.tearDown
    add=original.Step4CTests.add
    spec=original.Step4CTests.spec
    query=original.Step4CTests.query
    row=original.Step4CTests.row
    c=original.Step4CTests.c
    capture=original.Step4CTests.capture
    preview=original.Step4CTests.preview
    commit=original.Step4CTests.commit
    counts=original.Step4CTests.counts
    offering_row=original.Step4CTests.offering_row
    context=original.Step4CTests.context
    kit=original.Step4CTests.kit

    def other(self,text='Experimental Resin Q'):
        return {'fields':{'MA':'A99X','AR':'CUB','CA':'M500','OT':[['MA_GRADE',text]]}}
    def feature(self,article,closure,token): return self.c('CF_FEATURE',dict(article=article,closure=closure,token=token))
    def approval(self,sample=None,decision='approved',context=None):
        return self.add('approval',{'type':'client_approval','decision':decision,'actor_name':'Illustrative client'},context=context or self.a['context'],evidence=self.ev,**({'sample':sample} if sample else {}))
    def rejected_v1_approved_v2(self):
        self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)
        reject=self.approval(self.a['sample'],'rejected')
        v2=self.s.revise(self.a['sample'],{'label':'V2'},evidence=self.ev,**self.meta)['record']
        approve=self.approval(v2)
        return v2,reject,approve

    def test_R1_reject_other_substitution_atomic_source_retained(self):
        """Known OTHER is not unknown: reject PET substitution with no partial commit."""
        t=self.capture(self.other()); old=self.s.get(t); p=self.preview(t); before=self.counts()
        with self.assertRaises(RecordError):
            self.commit(p,'offering',supplier=self.a['supplier'],reference='OTHER-PET',selected_specification=self.f['specification'],supported_code='A1!APTX.CUB.XXX.M500.R98')
        self.assertEqual(self.counts(),before); self.assertEqual(self.s.get(t),old)
        self.s.close(); self.s=Store(self.path)
        self.assertEqual(self.s.get(t),old)
        self.assertEqual(self.s.get(p)['data']['code'],'A1!A99X.CUB.XXX.M500.X+OT:MA_GRADE=Experimental%20Resin%20Q')
        self.assertEqual(self.s.referring(p,'preview','intake_decision'),[])

    def test_R1_candidate_preview_explains_known_other_difference(self):
        p=self.preview(self.capture(self.other()))
        pet=next(x for x in self.s.get(p)['data']['candidates'] if x['id']==self.f['specification'])
        self.assertEqual(pet['classification'],'contradiction')

    def test_R1_amended_supported_preview_and_exact_reuse(self):
        t=self.capture(self.other()); first=self.preview(t)
        self.commit(first,'triage')
        p=self.preview(t,facts={'fields':{'MA':'APTX','AR':'CUB','CA':'M500','FI':'R98'}})
        out=self.commit(p,'offering',supplier=self.a['supplier'],reference='AMENDED',selected_specification=self.f['specification'])
        self.assertEqual(out['specification'],self.f['specification'])
        self.assertEqual(self.s.get(t)['data']['snapshot']['facts'],self.other())
        self.assertEqual(len(self.i.history(t)['reviews']),2)
        self.assertEqual(len(self.i.history(t)['decisions']),2)

    def test_R1_other_exact_reuse_and_unknown_enrichment(self):
        exact=self.spec(self.other())
        t=self.capture(self.other()); out=self.commit(self.preview(t),selected_specification=exact)
        self.assertEqual(out['specification'],exact)
        fuller=self.other(); fuller['fields']['FI']='R98'; target=self.spec(fuller)
        t2=self.capture(self.other())
        out=self.commit(self.preview(t2),selected_specification=target,supported_code=self.s.get(target)['data']['code'])
        self.assertEqual(out['specification'],target)
        different=self.spec(self.other('Different Resin'))
        p=self.preview(self.capture(self.other()))
        with self.assertRaises(RecordError): self.commit(p,selected_specification=different,supported_code=self.s.get(different)['data']['code'])

    def test_R2_article_stackable_is_not_sipper(self):
        sid=self.spec('A1!APTX.CUX.XXS.X.X+FR:CLOSURE.LP:F')
        self.assertEqual(self.row(sid,[self.feature('CU',True,'S')],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(sid,[self.feature('CU',True,'F')],types=['specification'])['classification'],'match')
        self.assertEqual(self.row(sid,[self.feature('CU',False,'S')],types=['specification'])['classification'],'match')

    def test_R2_explicit_lp_dome_is_searchable(self):
        sid=self.spec('A1!APSX.BWX.XXX.X.X+FR:CLOSURE.LP:D')
        self.assertEqual(self.row(sid,[self.feature('BW',True,'D')],types=['specification'])['classification'],'match')
        self.assertEqual(self.row(sid,[self.feature('BW',True,'F')],types=['specification'])['classification'],'contradiction')

    def test_R2_absent_compatible_window_is_gap(self):
        sid=self.spec('A1!BKRX.BGX.XXT.X.X')
        self.assertEqual(self.row(sid,[self.feature('BG',False,'W')],types=['specification'])['classification'],'potential')
        self.assertEqual(self.row(sid,[self.feature('BG',False,'T')],types=['specification'])['classification'],'match')

    def test_R2_explicit_negative_exclusion_na_and_valid_fx(self):
        nohandle=self.spec('A1!BKRX.BGX.XXN.X.X')
        self.assertEqual(self.row(nohandle,[self.feature('BG',False,'T')],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(nohandle,[self.feature('BG',False,'W')],types=['specification'])['classification'],'potential')
        combo=self.spec('A1!BKRX.BGX.XXT.X.X+FX:W,Z')
        for token in ('T','W','Z'): self.assertEqual(self.row(combo,[self.feature('BG',False,token)],types=['specification'])['classification'],'match')
        self.assertEqual(self.row(combo,[self.feature('BG',False,'F')],types=['specification'])['classification'],'contradiction')
        plain=self.spec('A1!APTX.CUB.XXN.X.X')
        self.assertEqual(self.row(plain,[self.feature('CU',False,'S')],types=['specification'])['classification'],'contradiction')
        na=self.spec('A1!BKRX.BGX.XX0.X.X')
        self.assertEqual(self.row(na,[self.feature('BG',False,'T')],types=['specification'])['classification'],'contradiction')

    def test_R2_core_lid_and_missing_lp_do_not_borrow_article_features(self):
        core=self.spec('A1!APSX.BWL.XXD.X.X')
        self.assertEqual(self.row(core,[self.feature('BW',True,'D')],types=['specification'])['classification'],'match')
        unknown=self.spec('A1!APTX.CUX.XXS.X.X+FR:CLOSURE')
        self.assertEqual(self.row(unknown,[self.feature('CU',True,'S')],types=['specification'])['classification'],'potential')
        self.assertEqual(self.row(core,[self.feature('CU',True,'D')],types=['specification'])['classification'],'contradiction')

    def test_R2_intake_preview_keeps_article_and_lid_features_separate(self):
        code='A1!APTX.CUX.XXS.X.X+FR:CLOSURE.LP:F'; sid=self.spec(code)
        from atlas.engine import Engine
        from atlas.records import ROOT
        facts=Engine(ROOT/'dictionary/atlas-A1-0.1.0.json').decode(code)
        p=self.preview(self.capture(facts))
        row=next(x for x in self.s.get(p)['data']['candidates'] if x['id']==sid)
        self.assertTrue(row['equal_description']); self.assertEqual(row['classification'],'match')

    def test_R3_zero_percent_is_numeric(self):
        sid=self.spec('A1!APTX.CUB.XXX.X.X+PR:0')
        r=self.row(sid,[self.c('PR','0')],types=['specification'])
        self.assertEqual(r['classification'],'match'); self.assertEqual(r['explanations'][0]['recorded_interval'],['0','0'])
        self.assertEqual(self.row(sid,[self.c('PR','1')],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(sid,[self.c('PR',{'value':['0','10'],'unit':'%'})],types=['specification'])['classification'],'match')

    def test_R3_nonzero_does_not_equal_zero(self):
        sid=self.spec('A1!APTX.CUB.XXX.X.X+PR:10')
        self.assertEqual(self.row(sid,[self.c('PR','0')],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(sid,[self.c('PR','10')],types=['specification'])['classification'],'match')

    def test_R3_ca_fi_applicability_unchanged(self):
        sid=self.spec('A1!BKRX.BGX.XXX.0.0')
        for field,value in [('CA','M500'),('FI','R98')]:
            self.assertEqual(self.row(sid,[self.c(field,'0')],types=['specification'])['classification'],'match')
            self.assertEqual(self.row(sid,[self.c(field,value)],types=['specification'])['classification'],'contradiction')
        self.assertEqual(self.row(self.f['specification'],[self.c('CA','0')],types=['specification'])['classification'],'contradiction')

    def test_R4_broad_approval_uses_approved_v2_despite_rejected_v1(self):
        v2,_,approved=self.rejected_v1_approved_v2()
        r=self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})
        self.assertEqual(r['classification'],'match')
        evidence=next(x for x in r['explanations'] if x.get('criterion')=='approval')
        self.assertEqual(evidence['records'],[approved]); self.assertEqual(evidence['sample'],v2)
        self.s.close(); self.s=Store(self.path); self.search=Search(self.s)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'match')

    def test_R4_explicit_iterations_and_sampling(self):
        v2,_,_=self.rejected_v1_approved_v2()
        for sample,expected in [(self.a['sample'],'contradiction'),(v2,'match')]:
            self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'},scope={'sample':sample})['classification'],expected)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval','sampling':True})['classification'],'match')

    def test_R4_independent_sampling_efforts_with_reused_labels(self):
        self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)
        self.approval(self.a['sample'],'rejected')
        seq=self.add('sequence',{'label':'Another effort'},product=self.a['product'],client=self.f['client'])
        sample=self.add('sample',{'label':'V1'},sequence=seq,context=self.a['context'])
        self.approval(sample)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'match')
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'},scope={'sample':self.a['sample']})['classification'],'contradiction')

    def test_R4_same_iteration_conflict_and_withdrawal_remain_negative(self):
        v2,_,approval=self.rejected_v1_approved_v2()
        self.approval(v2,'rejected')
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'contradiction')
        self.s.correct_approval(approval,evidence=self.ev,**self.meta)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'},scope={'sample':v2})['classification'],'contradiction')

    def test_R4_unsampled_decisions_have_separate_scope(self):
        self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)
        self.approval(self.a['sample'],'rejected'); self.approval()
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'match')
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval','sampling':True})['classification'],'contradiction')
        self.approval(decision='rejected')
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'contradiction')

    def test_R4_no_cross_supplier_client_or_customization_transfer(self):
        self.s.correct_approval(self.a['approval'],evidence=self.ev,**self.meta)
        self.approval(self.a['sample'],'rejected')
        other=self.add('client',{'name':'Other client'})
        ctx=self.context(customization=[],client=other)
        self.approval(context=ctx)
        newcustom=self.s.revise(self.a['customization'],{'details':{'printing':'two colors'}},evidence=self.ev,**self.meta)['record']
        otherctx=self.context(customization=newcustom); self.approval(context=otherctx)
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'},scope={'client':self.f['client'],'customization':self.a['customization']})['classification'],'contradiction')
        self.assertEqual(self.offering_row(self.b['product'],[],evidence={'approval':'client_approval'},scope={'sample':self.a['sample']})['classification'],'potential')

    def test_R4_physical_and_kit_revisions_do_not_inherit_approval(self):
        v=self.s.revise(self.a['version'],{'label':'Physical 2'},evidence=self.ev,**self.meta)['record']
        a=self.add('association',{},version=v,specification=self.f['specification'],evidence=self.ev)
        self.add('context',{},version=v,association=a,client=self.f['client'])
        self.assertEqual(self.offering_row(self.a['product'],[],evidence={'approval':'client_approval'})['classification'],'potential')
        kit,rev,ctx=self.kit(); seq=self.add('sequence',{'label':'Kit effort'},kit=kit,client=self.f['client'])
        sample=self.add('sample',{'label':'V1'},sequence=seq,context=ctx); self.approval(sample,context=ctx)
        new=self.s.revise(rev,{'label':'2'},evidence=self.ev,**self.meta)['record']
        self.add('context',{},kit_revision=new,client=self.f['client'])
        self.assertEqual(self.row(new,[],types=['kit'],evidence={'approval':'client_approval'})['classification'],'potential')

if __name__=='__main__': unittest.main()
