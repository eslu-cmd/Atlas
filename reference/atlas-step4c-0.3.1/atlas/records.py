"""Persistent, append-only Atlas relationships. All writes go through Store.

The local database enforces references and immutability; this module additionally
validates typed edges, revision lineage and exact evidence scope. It is not an
untrusted-client SQL API. No network, ORM or nonstandard dependency is required.
"""
import hashlib
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from .engine import Engine, exact, check_compatible

RECORD_VERSION = '0.2.1'
ROOT = Path(__file__).resolve().parents[1]
UNCERTAINTY = {'not_supplied', 'explicitly_unknown', 'not_applicable', 'ambiguous', 'conflicting', 'unsupported', 'stated'}

class RecordError(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise RecordError(message)

def dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)

# Required data fields; optional fields; edges (kind, cardinality).
# ! exactly one, ? optional, * ordered collection, + nonempty collection.
CONTRACTS = {}
def contract(kind, required='', optional='', **edges):
    CONTRACTS[kind] = (set(required.split()), set(optional.split()), edges)

contract('dictionary', 'namespace release document sha256')
contract('specification', 'code', dictionary=('dictionary','!'))
contract('supplier', 'name')
contract('product', 'reference', 'sku', supplier=('supplier','!'))
contract('sku', 'value', product=('product','!'), previous=('sku','?'))
contract('version', 'label', product=('product','!'), previous=('version','?'))
contract('association', '', '', version=('version','!'), specification=('specification','!'), previous=('association','?'), evidence=('assertion','*'))
contract('source', 'title uri', 'sha256 metadata')
contract('location', 'locator', source=('source','!'))
contract('attachment', 'uri media_type', 'sha256 caption', source=('source','?'))
contract('assertion', 'statement uncertainty', 'interpretation supplied evidence_kind', location=('location','!'), subject=('*','?'), attachments=('attachment','*'))
contract('finding', 'statement uncertainty', assertion=('assertion','!'), evidence=('assertion','*'))
contract('triage', 'label status snapshot', location=('location','!'), specification=('specification','?'), assertions=('assertion','*'))
contract('client', 'name')
contract('request', 'requirements', 'usage distribution qualifications', client=('client','?'), source=('source','?'), attachments=('attachment','*'))
contract('job', 'reference', client=('client','?'), request=('request','?'))
contract('customization', 'details', version=('version','?'), kit_revision=('kit_revision','?'), client=('client','?'), request=('request','?'), job=('job','?'), previous=('customization','?'), artwork=('attachment','*'), proofs=('attachment','*'))
contract('kit', 'reference', supplier=('supplier','!'))
contract('component', 'quantity quantity_state saleability', association=('association','!'), evidence=('assertion','*'))
contract('kit_revision', 'label', kit=('kit','!'), previous=('kit_revision','?'), components=('component','+'))
contract('packing', 'supplied', version=('version','?'), kit_revision=('kit_revision','?'), previous=('packing','?'), evidence=('assertion','*'))
contract('context', '', '', version=('version','?'), association=('association','?'), kit_revision=('kit_revision','?'), customization=('customization','?'), packing=('packing','?'), client=('client','?'), request=('request','?'), job=('job','?'))
contract('quote', 'supplied', 'discrepancies', context=('context','!'), previous=('quote','?'), evidence=('assertion','*'))
contract('sequence', 'label', product=('product','?'), kit=('kit','?'), client=('client','?'), request=('request','?'), job=('job','?'))
contract('sample', 'label', 'received_at', sequence=('sequence','!'), context=('context','!'), previous=('sample','?'), evidence=('assertion','*'))
contract('sample_note', 'type text', sample=('sample','!'), attachments=('attachment','*'), evidence=('assertion','*'))
contract('approval', 'type decision actor_name', 'decision_at conditions', context=('context','!'), sample=('sample','?'), evidence=('assertion','+'))
contract('compatibility', 'type conditions', 'person date', left=('version','!'), right=('version','!'), evidence=('assertion','+'))
contract('capability', 'alternatives conditions', supplier=('supplier','!'), evidence=('assertion','*'))
contract('handoff', 'qualifications', context=('context','!'), quote=('quote','?'), approvals=('approval','*'), attachments=('attachment','*'))
contract('event', 'type resolution', old=('*','!'), new=('*','?'), evidence=('assertion','+'))

# Step 4C appends workflow records; existing snapshot schema and contracts stay intact.
contract('intake_preview', 'facts uncertainty_facts code candidates differences', intake=('triage','!'), dictionary=('dictionary','!'))
contract('intake_decision', 'action payload result', intake=('triage','!'), preview=('intake_preview','!'), evidence=('assertion','+'), records=('*','*'))
contract('phrase_review', 'phrase proposed unsupported')
contract('phrase_confirmation', 'query acknowledged', review=('phrase_review','!'))

class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(str(path), isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        version = self.db.execute('PRAGMA user_version').fetchone()[0]
        need(version in (0,1), 'Unsupported storage schema')
        self.db.executescript((ROOT/'schema/sqlite.sql').read_text())
        self._depth = 0

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @contextmanager
    def transaction(self):
        # Savepoints make nested operations atomic even if a caller catches errors.
        name = 's' + str(self._depth)
        self.db.execute('SAVEPOINT ' + name)
        self._depth += 1
        try:
            yield self
            self.db.execute('RELEASE SAVEPOINT ' + name)
        except BaseException:
            self.db.execute('ROLLBACK TO SAVEPOINT ' + name)
            self.db.execute('RELEASE SAVEPOINT ' + name)
            raise
        finally:
            self._depth -= 1

    def get(self, identity, kind=None):
        row = self.db.execute('SELECT * FROM records WHERE id=?',(identity,)).fetchone()
        need(row is not None, 'Unknown record: ' + str(identity))
        result = dict(row)
        need(kind is None or result['kind']==kind, 'Wrong record kind: ' + str(identity))
        result['data'] = json.loads(result['data'])
        result['links'] = {}
        for link in self.db.execute('SELECT * FROM links WHERE owner=? ORDER BY role,position',(identity,)):
            result['links'].setdefault(link['role'],[]).append(link['target'])
        return result

    def one(self, identity, role):
        return self.get(identity)['links'].get(role,[None])[0]

    def all(self, kind):
        need(kind in CONTRACTS, 'Unknown kind')
        return [self.get(r[0]) for r in self.db.execute('SELECT id FROM records WHERE kind=? ORDER BY rowid',(kind,))]

    def referring(self, target, role=None, kind=None):
        self.get(target)
        sql = 'SELECT DISTINCT r.id FROM records r JOIN links l ON l.owner=r.id WHERE l.target=?'
        args = [target]
        if role is not None:
            sql += ' AND l.role=?'; args.append(role)
        if kind is not None:
            sql += ' AND r.kind=?'; args.append(kind)
        return [self.get(r[0]) for r in self.db.execute(sql,args)]

    def _key(self, namespace, value, record):
        self.db.execute('INSERT INTO unique_keys VALUES (?,?,?)',(namespace,dump(value),record))

    def add(self, kind, data, links=None, *, actor, reason, provenance='operational', effective_at=None, identity=None):
        need(kind in CONTRACTS, 'Unknown record kind')
        need(isinstance(data,dict), 'Record data must be an object')
        required, optional, edge_rules = CONTRACTS[kind]
        need(required <= data.keys() and data.keys() <= required|optional, 'Missing or unsupported data fields for '+kind)
        need(isinstance(actor,str) and actor.strip() and isinstance(reason,str) and reason.strip(), 'Actor and reason required')
        need(provenance in ('source','illustrative','operational'), 'Explicit provenance required')
        links = links or {}
        need(isinstance(links,dict) and links.keys() <= edge_rules.keys(), 'Unsupported relationship')
        refs = {}
        for role,(target_kind,cardinality) in edge_rules.items():
            values = links.get(role,[])
            if isinstance(values,str): values=[values]
            need(isinstance(values,list) and all(isinstance(v,str) for v in values), 'References must be IDs')
            need(len(values)==len(set(values)), 'Duplicate references')
            need(cardinality not in ('!','?') or len(values)<=1, 'Too many '+role+' references')
            need(cardinality not in ('!','+') or bool(values), 'Missing '+role+' reference')
            for value in values: self.get(value, None if target_kind=='*' else target_kind)
            if values: refs[role]=values
        # Round-trip detaches caller-owned data and rejects non-JSON/NaN values.
        data = json.loads(dump(data))
        with self.transaction():
            self._validate(kind,data,refs)
            rid = identity or str(uuid.uuid4())
            self.db.execute('INSERT INTO records VALUES (?,?,?,?,?,?,?,?)',
                (rid,kind,dump(data),actor,datetime.now(timezone.utc).isoformat(),reason,effective_at,provenance))
            for role,values in refs.items():
                for pos,value in enumerate(values):
                    self.db.execute('INSERT INTO links VALUES (?,?,?,?)',(rid,role,pos,value))
            self._unique(kind,data,refs,rid)
            return rid

    def _target(self, links):
        return (links.get('version') or links.get('kit_revision') or [None])[0]

    def _business_scope(self, links):
        """Resolve known client/request/job context and reject contradictions."""
        result = {k:links.get(k,[None])[0] for k in ('client','request','job')}
        if result['job']:
            job=self.get(result['job'])
            for k in ('client','request'):
                value=job['links'].get(k,[None])[0]
                need(not value or not result[k] or value==result[k], 'Job context mismatch')
                result[k]=result[k] or value
        if result['request']:
            value=self.one(result['request'],'client')
            need(not value or not result['client'] or value==result['client'], 'Request client mismatch')
            result['client']=result['client'] or value
        return result

    def _validate(self, kind, data, refs):
        one=lambda role: refs.get(role,[None])[0]
        previous=one('previous')
        for field in ('name','reference','label','code','title','uri','namespace','release','actor_name','statement'):
            if field in data and not (kind=='intake_preview' and field=='code' and data[field] is None):
                need(isinstance(data[field],str) and bool(data[field].strip()), field+' requires nonempty text')
        for field in ('supplied','details'):
            if field in data: need(isinstance(data[field],dict), field+' must preserve an object of supplied values')
        if 'uncertainty' in data:
            need(data['uncertainty'] in UNCERTAINTY, 'Unsupported uncertainty state')
        if kind in ('job','sequence','customization','context'):
            scope=self._business_scope(refs)
        if kind=='dictionary':
            document=data['document']
            need(data['namespace']==document['namespace'] and data['release']==document['release'], 'Dictionary metadata mismatch')
            need(data['sha256']==hashlib.sha256(dump(document).encode()).hexdigest(), 'Dictionary digest mismatch')
            Engine(document)
            for issued in self.all('dictionary'):
                check_compatible(issued['data']['document'],document)
        if kind=='specification':
            Engine(self.get(one('dictionary'))['data']['document']).decode(data['code'])
        if kind=='association' and previous:
            need(self.one(previous,'version')==one('version'), 'Association cannot move across versions')
        if kind in ('sku','version') and previous:
            need(self.one(previous,'product')==one('product'), 'Revision cannot move across products')
        if kind in ('customization','packing','context'):
            need(bool(one('version')) != bool(one('kit_revision')), 'Exactly one physical version or kit revision required')
        if kind in ('customization','packing') and previous:
            prior=self.get(previous)['links']
            need(self._target(prior)==self._target(refs), 'Revision target mismatch')
            if kind=='customization':
                need(self._business_scope(prior)==scope, 'Customization client/job scope mismatch')
        if kind=='component':
            need(data['quantity_state'] in UNCERTAINTY, 'Invalid quantity state')
            need(data['saleability'] in ('not_supplied','explicitly_unknown','yes','no'), 'Explicit saleability state required')
            if data['quantity_state']=='stated':
                need(isinstance(data['quantity'],dict) and set(data['quantity'])=={'value','unit'}, 'Supplied quantity needs value and unit')
                need(exact(data['quantity']['value'])>0 and bool(data['quantity']['unit']), 'Invalid supplied quantity')
            else:
                need(data['quantity'] is None, 'Unresolved quantity must remain null; retain wording in assertion')
        if kind=='kit_revision':
            if previous: need(self.one(previous,'kit')==one('kit'), 'Kit revision identity mismatch')
            supplier=self.one(one('kit'),'supplier')
            for component in refs['components']:
                association=self.one(component,'association')
                product=self.one(self.one(association,'version'),'product')
                need(self.one(product,'supplier')==supplier, 'Cross-supplier kit component')
        if kind=='context':
            if one('version'):
                need(one('association') and self.one(one('association'),'version')==one('version'), 'Exact version association required')
            else: need(not one('association'), 'Kit specifications belong to its components')
            for role in ('customization','packing'):
                if one(role):
                    other=self.get(one(role))['links']
                    need(self._target(other)==self._target(refs), role+' belongs to another version or kit revision')
                    if role=='customization': need(self._business_scope(other)==scope, 'Customization scope mismatch')
        if kind=='quote' and previous:
            old_context=self.get(self.one(previous,'context'))['links']
            new_context=self.get(one('context'))['links']
            need(self._target(old_context)==self._target(new_context), 'Commercial revision cannot move across versions or kit revisions')
            need(self._business_scope(old_context)==self._business_scope(new_context), 'Commercial revision client/job mismatch')
        if kind=='sequence':
            need(bool(one('product')) != bool(one('kit')), 'Exactly one supplier product or supplier kit required')
        if kind=='sample':
            context=self.get(one('context'))['links']
            sequence=self.get(one('sequence'))['links']
            if sequence.get('product'):
                need(context.get('version') and self.one(context['version'][0],'product')==sequence['product'][0], 'Sample sequence product mismatch')
            else:
                need(context.get('kit_revision') and self.one(context['kit_revision'][0],'kit')==sequence['kit'][0], 'Sample sequence kit mismatch')
            need(self._business_scope(context)==self._business_scope(sequence), 'Sample sequence client/job mismatch')
            if previous: need(self.one(previous,'sequence')==one('sequence'), 'Sample sequence mismatch')
        if kind=='sample_note':
            need(data['type'] in ('photo','comment','revision_request','evidence'), 'Invalid sample note type')
        if kind=='approval':
            need(data['type'] in ('proof_agreement','source_one_acceptance','client_approval'), 'Approval types must remain distinct')
            need(data['decision'] in ('agreed','accepted','approved','rejected'), 'Invalid decision')
            expected={'proof_agreement':'agreed','source_one_acceptance':'accepted','client_approval':'approved'}
            need(data['decision'] in (expected[data['type']],'rejected'), 'Decision/type mismatch')
            context=self.get(one('context'))['links']
            if data['type']=='client_approval': need(self._business_scope(context)['client'], 'Client approval needs a client')
            if data['type']=='proof_agreement': need(context.get('customization'), 'Proof agreement needs a customization revision')
            if data['type']=='source_one_acceptance': need(one('sample'), 'Sample acceptance needs its iteration')
            if one('sample'): need(self.same_context(one('context'),self.one(one('sample'),'context')), 'Approval sample context mismatch')
        if kind=='compatibility':
            need(one('left')!=one('right'), 'Compatibility needs two particular versions')
            need(data['type'] in ('supplier_claim','human_confirmation'), 'Invalid compatibility type')
            if data['type']=='human_confirmation': need(bool(data.get('person')), 'Confirmation needs a person')
        if kind=='capability':
            need(isinstance(data['alternatives'],list) and bool(data['alternatives']), 'Keep capability alternatives separate')
        if kind=='handoff':
            if one('quote'): need(self.same_context(one('context'),self.one(one('quote'),'context')), 'Handoff quote context mismatch')
            for approval in refs.get('approvals',[]):
                need(self.same_context(one('context'),self.one(approval,'context')), 'Handoff approval context mismatch')
                need(self.is_active(approval), 'Withdrawn evidence cannot support a new handoff')
        if kind=='event':
            need(data['type'] in ('H01','H02','H03','H04','H05','H06','H07','H08','H09','H10'), 'Invalid history event')
            need(data['resolution'] in ('replaced','withdrawn','unresolved','identity_resolution'), 'Invalid resolution')
            need(not one('new') or one('new')!=one('old'), 'Correction must identify a different record')
            if data['type'] in ('H01','H06'):
                self.get(one('old'),'association')
                if one('new'):
                    self.get(one('new'),'association')
                    need(self.one(one('new'),'previous')==one('old'), 'Correction association must link its predecessor')
            revision_types={'H02':'version','H03':'customization','H04':'packing','H05':'quote','H09':'sample','H10':'kit_revision'}
            if data['type'] in revision_types:
                self.get(one('old'),revision_types[data['type']])
                need(one('new'), 'Revision event requires its successor')
                self.get(one('new'),revision_types[data['type']])
                need(self.one(one('new'),'previous')==one('old'), 'Revision event lineage mismatch')
            if data['type']=='H07':
                self.get(one('old'),'approval')
                need(self.is_active(one('old')), 'Approval already withdrawn')
                if one('new'):
                    replacement=self.get(one('new'),'approval')
                    need(replacement['data']['type']==self.get(one('old'))['data']['type'], 'Correction cannot change approval type')
            if data['type']=='H08':
                self.get(one('old'),'product')
                if one('new'): self.get(one('new'),'product')
                need(data['resolution']=='identity_resolution', 'Identity resolution requires explicit evidence; no automatic merge')
                need(any(self.get(e)['data'].get('evidence_kind')=='identity' for e in refs['evidence']), 'Identity evidence must be explicitly classified; equal descriptions are insufficient')
            if data['resolution']=='unresolved': need(not one('new'), 'Uncertain destination must remain unresolved')

    def _unique(self,kind,data,refs,rid):
        one=lambda role: refs.get(role,[None])[0]
        if kind=='dictionary': self._key('dictionary',(data['namespace'],data['release']),rid)
        if kind=='specification': self._key('specification',data['code'],rid)
        if kind in ('product','kit'): self._key(kind,(one('supplier'),data['reference']),rid)
        if kind=='product' and data.get('sku'): self._key('supplier_sku',(one('supplier'),data['sku']),rid)
        if kind=='sku': self._key('supplier_sku',(self.one(one('product'),'supplier'),data['value']),rid)
        if kind in ('version','association','kit_revision'):
            parent={'version':'product','association':'version','kit_revision':'kit'}[kind]
            self._key(kind+'_successor',one('previous') or ('initial',one(parent)),rid)
        if kind=='sample': self._key('sample_label',(one('sequence'),data['label']),rid)

    def register_dictionary(self,path,**meta):
        document=json.loads(Path(path).read_text())
        existing=self.db.execute('SELECT record FROM unique_keys WHERE namespace=? AND value=?',('dictionary',dump([document['namespace'],document['release']]))).fetchone()
        if existing:
            need(self.get(existing[0])['data']['document']==document, 'Release already has different content')
            return existing[0]
        return self.add('dictionary',{'namespace':document['namespace'],'release':document['release'],'document':document,'sha256':hashlib.sha256(dump(document).encode()).hexdigest()},**meta)

    def issue(self,code,dictionary,**meta):
        Engine(self.get(dictionary,'dictionary')['data']['document']).decode(code)
        existing=self.db.execute('SELECT record FROM unique_keys WHERE namespace=? AND value=?',('specification',dump(code))).fetchone()
        if existing: return existing[0]
        return self.add('specification',{'code':code},{'dictionary':dictionary},**meta)

    def same_context(self,left,right):
        left_links=self.get(left,'context')['links']
        right_links=self.get(right,'context')['links']
        business={'client','request','job'}
        exact_links=lambda links: {k:v for k,v in links.items() if k not in business}
        return (exact_links(left_links)==exact_links(right_links)
                and self._business_scope(left_links)==self._business_scope(right_links))

    def supplier_for(self,context):
        links=self.get(context,'context')['links']
        if links.get('version'):
            return self.one(self.one(links['version'][0],'product'),'supplier')
        return self.one(self.one(links['kit_revision'][0],'kit'),'supplier')

    def is_active(self,identity):
        self.get(identity)
        return not any(e['data']['type'] in ('H06','H07') for e in self.referring(identity,'old','event'))

    def current_association(self,version):
        rows=self.referring(version,'version','association')
        prior={self.one(r['id'],'previous') for r in rows}
        heads=[r for r in rows if r['id'] not in prior and self.is_active(r['id'])]
        need(len(heads)<=1, 'Multiple current associations')
        return heads[0] if heads else None

    def change_association(self,old,specification,*,event_type,evidence,**meta):
        need(event_type in ('H01','H06'), 'Use clarification or correction')
        with self.transaction():
            version=self.one(old,'version')
            current=self.current_association(version)
            need(current and current['id']==old, 'Association is no longer current')
            new=self.add('association',{}, {'version':version,'specification':specification,'previous':old,'evidence':evidence},**meta)
            event=self.add('event',{'type':event_type,'resolution':'replaced'},{'old':old,'new':new,'evidence':evidence},**meta)
            return {'record':new,'event':event}

    def revise(self,old,data,*,evidence,links=None,**meta):
        """Create a physical/customization/packing/quote/sample/kit revision atomically."""
        prior=self.get(old)
        types={'version':'H02','customization':'H03','packing':'H04','quote':'H05','sample':'H09','kit_revision':'H10'}
        need(prior['kind'] in types, 'Unsupported revision type')
        with self.transaction():
            new_links={**prior['links'],**(links or {}),'previous':old}
            new=self.add(prior['kind'],data,new_links,**meta)
            event=self.add('event',{'type':types[prior['kind']],'resolution':'replaced'},{'old':old,'new':new,'evidence':evidence},**meta)
            return {'record':new,'event':event}

    def correct_approval(self,old,*,evidence,destination=None,sample=None,**meta):
        with self.transaction():
            prior=self.get(old,'approval')
            new=None
            if destination:
                # Retain the actual approval evidence. The H07 event separately
                # owns the evidence authorizing reassociation.
                refs={**prior['links'],'context':destination}
                refs.pop('sample',None)
                if sample: refs['sample']=sample
                new=self.add('approval',prior['data'],refs,**meta)
            event=self.add('event',{'type':'H07','resolution':'replaced' if new else 'unresolved'},
                {'old':old,**({'new':new} if new else {}),'evidence':evidence},**meta)
            return {'record':new,'event':event}

    def resolve_identity(self,old,new,*,evidence,**meta):
        # This explains identity evidence without erasing old IDs or moving evidence.
        need(bool(evidence),'Equal specifications alone do not authorize identity resolution')
        return self.add('event',{'type':'H08','resolution':'identity_resolution'},
            {'old':old,**({'new':new} if new else {}),'evidence':evidence},**meta)

    def history(self,identity):
        """Original immutable graph plus separately labelled subsequent events/findings."""
        original={}
        def visit(rid):
            if rid in original: return
            row=self.get(rid); original[rid]=row
            for role,targets in row['links'].items():
                if role=='previous': continue  # lineage remains a link, not original quote content
                for target in targets: visit(target)
        visit(identity)
        corrections={}
        revisions={}
        # Follow successive changes to affected records, without traversing a new
        # context into another offering's unrelated history. Corrections are later
        # than the referenced fact, even if an old quote was entered retrospectively.
        excluded={'specification','dictionary','supplier','client','source','location','attachment'}
        pending=[rid for rid,row in original.items() if row['kind'] not in excluded]
        seen=set()
        while pending:
            rid=pending.pop()
            if rid in seen: continue
            seen.add(rid)
            for revision in self.referring(rid,'previous'):
                revisions[revision['id']]=revision
                pending.append(revision['id'])
            for event in self.referring(rid,'old','event')+self.referring(rid,'assertion','finding'):
                corrections[event['id']]=event
                pending.extend(event['links'].get('new',[]))
        # Incoming H07 events explain why this approval is at its current
        # destination. Keep former (withdrawn) associations out of original_context.
        provenance={}
        incoming={}
        approvals=[rid for rid,row in original.items() if row['kind']=='approval']
        pending=list(approvals)
        seen=set()
        def provenance_visit(rid):
            if rid in provenance: return
            row=self.get(rid); provenance[rid]=row
            for role,targets in row['links'].items():
                if role=='previous': continue
                for target in targets: provenance_visit(target)
        while pending:
            approval=pending.pop()
            if approval in seen: continue
            seen.add(approval)
            for event in self.referring(approval,'new','event'):
                if event['data']['type']!='H07': continue
                incoming[event['id']]=event
                provenance_visit(event['id'])
                pending.extend(event['links']['old'])
        approval_status={rid:self.is_active(rid) for rid in set(approvals)|{
            rid for rid,row in provenance.items() if row['kind']=='approval'}}
        return {'record':original[identity], 'original_context':original,
                'later_corrections':sorted(corrections.values(),key=lambda x:x['recorded_at']),
                'later_revisions':sorted(revisions.values(),key=lambda x:x['recorded_at']),
                'active':self.is_active(identity),
                'correction_provenance':{'events':sorted(incoming.values(),key=lambda x:x['recorded_at']),
                    'records':provenance,'approval_status':approval_status}}

    def product_history(self,product):
        self.get(product,'product')
        versions=self.referring(product,'product','version')
        contexts=[c for v in versions for c in self.referring(v['id'],'version','context')]
        return {'product':self.get(product),'versions':versions,
                'associations':[self.current_association(v['id']) for v in versions],
                'sequences':self.referring(product,'product','sequence'),
                'quotes':[q for c in contexts for q in self.referring(c['id'],'context','quote')],
                'approvals':[{'record':a,'active':self.is_active(a['id'])} for c in contexts for a in self.referring(c['id'],'context','approval')]}

    def memberships(self,version):
        self.get(version,'version')
        return [revision for a in self.referring(version,'version','association')
                for component in self.referring(a['id'],'association','component')
                for revision in self.referring(component['id'],'components','kit_revision')]

    def compatibility(self,left,right):
        self.get(left,'version'); self.get(right,'version')
        return [r for r in self.all('compatibility') if {self.one(r['id'],'left'),self.one(r['id'],'right')}=={left,right}]

    def sampling_history(self,sequence):
        self.get(sequence,'sequence')
        return {'sequence':self.get(sequence), 'iterations':[
            {'sample':self.history(sample['id']),
             'notes':[self.history(note['id']) for note in self.referring(sample['id'],'sample','sample_note')],
             'approvals':[self.history(approval['id']) for approval in self.referring(sample['id'],'sample','approval')]}
            for sample in self.referring(sequence,'sequence','sample')]}
