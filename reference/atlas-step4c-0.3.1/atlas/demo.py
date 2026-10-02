"""Explicitly illustrative relationship fixture, unrelated to workbook identities."""
from .records import ROOT

def illustrative(store):
    meta={'actor':'Illustrative fixture author','reason':'Synthetic Step 4B relationship scenario; not source facts','provenance':'illustrative'}
    def add(kind,data,**links): return store.add(kind,data,links,**meta)
    with store.transaction():
        d=store.register_dictionary(ROOT/'dictionary/atlas-A1-0.1.0.json',**meta)
        spec=store.issue('A1!APTX.CUB.XXX.M500.R98',d,**meta)
        source=add('source',{'title':'ILLUSTRATIVE evidence','uri':'illustrative://scenario'})
        location=add('location',{'locator':'ILLUSTRATIVE paragraph 1'},source=source)
        evidence=add('assertion',{'statement':'ILLUSTRATIVE scenario evidence; no real product claim','uncertainty':'stated'},location=location)
        client=add('client',{'name':'ILLUSTRATIVE Client'})
        ids={'dictionary':d,'specification':spec,'source':source,'evidence':evidence,'client':client}
        for label in ('A','B'):
            supplier=add('supplier',{'name':'ILLUSTRATIVE Vendor '+label})
            product=add('product',{'reference':'ILLUSTRATIVE-'+label,'sku':'DEMO-'+label},supplier=supplier)
            version=add('version',{'label':'Physical 1'},product=product)
            association=add('association',{},version=version,specification=spec,evidence=[evidence])
            customization=add('customization',{'details':{'printing':'one colour','artwork':'not supplied'}},version=version,client=client)
            packing=add('packing',{'supplied':{'units_per_case':'1000'}},version=version)
            context=add('context',{},version=version,association=association,customization=customization,packing=packing,client=client)
            quote=add('quote',{'supplied':{'unit_price':'0.01','case_price':'10.37','currency':'USD'},'discrepancies':['Supplied prices do not agree; neither value changed']},context=context,evidence=[evidence])
            sequence=add('sequence',{'label':'ILLUSTRATIVE sampling '+label},product=product,client=client)
            sample=add('sample',{'label':'V1'},sequence=sequence,context=context,evidence=[evidence])
            approval=add('approval',{'type':'client_approval','decision':'approved','actor_name':'ILLUSTRATIVE client representative'},context=context,sample=sample,evidence=[evidence])
            ids[label]=dict(supplier=supplier,product=product,version=version,association=association,customization=customization,packing=packing,context=context,quote=quote,sequence=sequence,sample=sample,approval=approval)
        return ids
