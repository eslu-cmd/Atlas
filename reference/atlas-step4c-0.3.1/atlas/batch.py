"""Import only the reviewed Step 4A batch, without inventing supplier identities."""
import json
from pathlib import Path
from .records import ROOT, need

def import_batch(store, path=None):
    path=Path(path or ROOT/'fixtures/verified-batch.json')
    batch=json.loads(path.read_text())
    meta={'actor':'Step 4B batch loader','reason':'Preserve reviewed Step 4A mapping without resolving product identity','provenance':'source'}
    with store.transaction():
        dictionary=store.register_dictionary(ROOT/'dictionary/atlas-A1-0.1.0.json',**meta)
        source=store.add('source',{'title':'verified list.xlsx — selected Step 4A batch','uri':batch['records'][0]['source'],
            'sha256':batch['metadata']['workbook_sha256'],'metadata':batch['metadata']},**meta)
        result=[]
        for record in batch['records']:
            loc=store.add('location',{'locator':{'worksheet':record['worksheet'],'rows':record['rows'],
                'cells':list(record['cells']),'supplier_context':record['supplier_context']}},{'source':source},**meta)
            assertions=[]
            for cell,value in record['cells'].items():
                cell_loc=store.add('location',{'locator':{'worksheet':record['worksheet'],'cell':cell}},{'source':source},**meta)
                assertions.append(store.add('assertion',{'statement':str(value['value']),'supplied':value,
                    'uncertainty':'stated','interpretation':'Transcription only; no product truth or approval inferred'}, {'location':cell_loc},**meta))
            specification=None
            if record['expected_code']:
                specification=store.issue(record['expected_code'],dictionary,**meta)
            triage=store.add('triage',{'label':record['id'],'status':'description_encoded_identity_unresolved' if specification else 'description_and_identity_unresolved',
                'snapshot':record}, {'location':loc,'assertions':assertions,**({'specification':specification} if specification else {})},**meta)
            result.append({'source_record':record['id'],'triage':triage,'specification':specification})
        need(len(result)==12, 'Only the reviewed 12-record batch is supported')
        return {'source':source,'records':result}
