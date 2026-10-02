import copy,json,unittest,tempfile,shutil,subprocess,sys
from pathlib import Path
from atlas import Engine,SpecError,check_compatible
from atlas.engine import number
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'dictionary/atlas-A1-0.1.0.json'
def node(fields,groups=None):return {'fields':fields,**({'groups':groups} if groups is not None else {})}
class EngineTests(unittest.TestCase):
 def setUp(self):self.e=Engine(D)
 def assertCode(self,facts,expected):
  self.assertEqual(self.e.encode(facts),expected)
  self.assertEqual(self.e.encode(self.e.decode(expected)),expected)
  self.assertTrue(self.e.describe(expected)['complete'])
 def test_W01_independent_diameters(self):
  f=node({'MA':'APTX','AR':'CUB','CA':{'value':'0.5','unit':'L'},'FI':{'value':'9.8','unit':'cm'}})
  self.assertCode(f,'A1!APTX.CUB.XXX.M500.R98');f['fields']['FI']={'value':'98.125','unit':'mm'}
  self.assertCode(f,'A1!APTX.CUB.XXX.M500.R98_125')
 def test_W02_W03_printing_context_separate(self):
  self.assertCode(node({'MA':'APPX','AR':'CUB','CA':'M500'}),'A1!APPX.CUB.XXX.M500.X')
  for key,value in [('PN','YES'),('PC',2),('PS',1),('PM','FLEXO'),('IC','50'),('SK','SKU'),('vendor','A'),('price','12'),('approval','YES'),('kit',[])]:
   with self.subTest(key=key),self.assertRaises(SpecError):self.e.encode(node({'MA':'APPX',key:value}))
  for context in [{'customization':{'logo':'A'}},{'sampling':'V2'},{'supplier':'B'}]:
   with self.assertRaises(SpecError):self.e.encode({**node({'MA':'APPX'}),**context})
 def test_W04_scopes_and_layers(self):
  for colour in ['BROWN','WHITE']:
   self.assertCode(node({'MA':'BKRX','AR':'BGX','CF':'XXT'},[{'scope':'INSIDE','node':node({'MA':'BKRX','CL':colour})}]),f'A1!BKRX.BGX.XXT.X.X~S(INSIDE){{CL:{colour}.MA:BKRX}}')
  for direction,expected in [('O','MA:BKRX;MA:APTX'),('X','MA:APTX;MA:BKRX')]:
   self.assertCode(node({'MA':'BKRX','AR':'BGX','CF':'XLX'},[{'direction':direction,'layers':[node({'MA':'BKRX'}),node({'MA':'APTX'})]}]),f'A1!BKRX.BGX.XLX.X.X~L({direction}){{{expected}}}')
 def test_W05_clarification_descriptions_differ(self):
  for ma in ['BKWX','BKWP']:self.assertCode(node({'MA':ma,'AR':'CUB','CA':'M500'}),f'A1!{ma}.CUB.XXX.M500.X')
  self.assertFalse(self.e.compare('A1!BKWX.CUB.XXX.M500.X','A1!BKWP.CUB.XXX.M500.X')['equal_description'])
 def test_W06_additive_dictionary_and_old_meanings(self):
  old=copy.deepcopy(self.e.d);new=copy.deepcopy(old);new['release']='0.2.0-test-only';new['tables']['GRADE']['A']['ZZ']='Illustrative new polymer'
  self.assertTrue(check_compatible(old,new));e2=Engine(new)
  self.assertEqual(self.e.decode('A1!APTX.CUB.XXX.M500.R98'),e2.decode('A1!APTX.CUB.XXX.M500.R98'))
  with self.assertRaises(SpecError):self.e.decode('A1!AZZX.CUX.XXX.X.X')
  self.assertTrue(e2.describe('A1!AZZX.CUX.XXX.X.X')['complete'])
  new['tables']['GRADE']['A']['PT']='Changed meaning'
  with self.assertRaises(SpecError):check_compatible(old,new)
 def test_retired_entry_still_decodes(self):
  d=copy.deepcopy(self.e.d)
  for e in d['entry_metadata']:
   if e['registry']=='GRADE' and e['token']=='PT':e['retired']=True
  self.assertTrue(check_compatible(self.e.d,d));self.assertTrue(Engine(d).describe('A1!APTX.CUX.XXX.X.X')['complete'])
 def test_W07_separate_components(self):
  for feature in ['S','F','N']:self.assertCode(node({'MA':'ACPX','AR':'CYX','CF':'XX'+feature}),f'A1!ACPX.CYX.XX{feature}.X.X')
  self.assertCode(node({'MA':'BTSX','AR':'NPX'}),'A1!BTSX.NPX.XXX.X.X')
  for role in ['K','C']:
   with self.assertRaises(SpecError):self.e.encode(node({'MA':'ACPX','AR':'CY'+role}))
  with self.assertRaises(SpecError):self.e.encode(node({'AR':'CYX','CF':'XXM'}))
 def test_W08_unresolved_ounces(self):self.assertCode(node({'AR':'CUX','UT':[['CA','16 oz']]}),'A1!XXXX.CUX.XXX.X.X+UT:CA=16%20oz')
 def test_exact_numbers(self):
  for a,b in [('00098.5000','98_5'),('2/6','1/3'),('125/1000','0_125'),('-0','0'),('1/40','0_025')]:self.assertEqual(number(a),b)
  for v in ['1e3','+1','1/0',1.5,True]:
   with self.assertRaises(SpecError):number(v)
 def test_exact_units_and_thickness(self):
  self.assertCode(node({'MA':'APTX','TH':{'value':'30','unit':'um'},'GW':{'value':'0.01','unit':'kg'},'FI':{'value':'3','unit':'in'}}),'A1!APTX.XXX.XXX.X.R76_2+GW:10.TH:0_03')
  self.assertCode(node({'AR':'CUX','CA':{'value':'1','unit':'US_fl_oz'}}),'A1!XXXX.CUX.XXX.M29_5735295625.X')
  self.assertCode(node({'AR':'CUX','CA':{'value':'1','unit':'IMP_fl_oz'}}),'A1!XXXX.CUX.XXX.M28_4130625.X')
  self.assertCode(node({'AR':'BGX','CA':{'value':'1','unit':'kg'}}),'A1!XXXX.BGX.XXX.G1000.X')
 def test_unresolved_units_fail(self):
  for u in ['oz','floz','gauge','']:
   with self.assertRaises(SpecError):self.e.encode(node({'AR':'CUX','CA':{'value':'16','unit':u}}))
 def test_intervals_fraction_count(self):
  self.assertCode(node({'AR':'CUX','CA':'M1/3','FI':'R098_0-99_00'}),'A1!XXXX.CUX.XXX.M1/3.R98-99')
  self.assertCode(node({'AR':'BGX','CA':'N2-2'}),'A1!XXXX.BGX.XXX.N2.X')
  for bad in ['N1_5','N1-2_5','M0','M2-1','M-1','R98']:
   with self.assertRaises(SpecError):self.e.encode(node({'AR':'CUX','CA':bad}))
 def test_tolerance_qualification(self):
  self.assertCode(node({'AR':'CUX','CA':'M500','QC':[['CA','TARGET','FILL','20 °C']],'TO':[['CA','5','10']]}),'A1!XXXX.CUX.XXX.M500.X+QC:[CA,TARGET,FILL,20%20%C2%B0C].TO:[CA,5,10]')
  self.assertCode(node({'AR':'CUX','CA':'M500','QC':[['CA','REPORTED','UNKNOWN','-']]}),'A1!XXXX.CUX.XXX.M500.X')
  for fields in [{'CA':'M490-510','TO':[['CA','1','1']]},{'CA':'M500','TO':[['CA','-1','1']]},{'TO':[['GW','1','1']]},{'GW':'2','QC':[['GW','TARGET','BRIM','-']]},{'CA':'X','QC':[['CA','TARGET','FILL','-']]},{'CA':'N3','TO':[['CA','0_5','1']]}]:
   with self.subTest(fields=fields),self.assertRaises(SpecError):self.e.encode(node({'AR':'CUX',**fields}))
 def test_dimensions_and_targets(self):
  self.assertCode(node({'AR':'BGX','DM':{'WIDTH':'20','HEIGHT':{'value':'2','unit':'in'}},'TO':[['DM_HEIGHT','1','2']]}),'A1!XXXX.BGX.XXX.X.X+DM:HEIGHT=50_8,WIDTH=20.TO:[DM_HEIGHT,1,2]')
  with self.assertRaises(SpecError):self.e.encode(node({'AR':'BGX','DM':{'WIDTH':'20'},'QC':[['DM_HEIGHT','TARGET','NA','-']]}))
 def test_unknown_na_other(self):
  self.assertCode(node({'AR':'BGX','CA':'0','FI':'0'}),'A1!XXXX.BGX.XXX.0.0')
  self.assertCode(node({'MA':'A99X','OT':[['MA_GRADE','novel polymer']]}),'A1!A99X.XXX.XXX.X.X+OT:MA_GRADE=novel%20polymer')
  for f in [{'MA':'A99X'},{'MA':'APTX','OT':[['MA_GRADE','PET']]},{'AR':'BG0'},{'MA':'A00X'},{'MA':'XPTX'},{}]:
   with self.assertRaises(SpecError):self.e.encode(node(f))
 def test_nested_no_inheritance_and_merge(self):
  f=node({'MA':'BKRX','AR':'BGX'},[{'scope':'INSIDE','node':node({'CL':'WHITE'})},{'scope':'INSIDE','node':node({'OP':'OPAQUE'})}])
  expected='A1!BKRX.BGX.XXX.X.X~S(INSIDE){CL:WHITE.OP:OPAQUE}'
  self.assertCode(f,expected);self.assertNotIn('MA',self.e.decode(expected)['groups'][0]['node']['fields'])
  f['groups'][1]['node']['fields']['CL']='BROWN'
  with self.assertRaises(SpecError):self.e.encode(f)
  self.assertCode(node({'MA':'APTX'},[{'scope':'BODY','node':node({},[{'scope':'OUTSIDE','node':node({'CL':'RED'})}])}]),'A1!APTX.XXX.XXX.X.X~S(BODY){-~S(OUTSIDE){CL:RED}}')
 def test_layer_repeats_reverse(self):
  base={'MA':'BKRX','AR':'BGX'}
  self.assertCode(node(base,[{'direction':'X','layers':[node({'MA':'BKRX'}),node({'MA':'APEX'}),node({'MA':'APEX'})]}]),'A1!BKRX.BGX.XXX.X.X~L(X){MA:APEX;MA:APEX;MA:BKRX}')
  self.assertCode(node(base,[{'direction':'I','layers':[node({'MA':'APEX'}),node({'MA':'BKRX'})]}]),'A1!BKRX.BGX.XXX.X.X~L(O){MA:BKRX;MA:APEX}')
 def test_utf8_structural_escaping(self):
  self.assertCode(node({'AR':'BGX','UT':[['DM','é .,:;{}[]()%+~|/=中文']]}),'A1!XXXX.BGX.XXX.X.X+UT:DM=%C3%A9%20%2E%2C%3A%3B%7B%7D%5B%5D%28%29%25%2B%7E%7C%2F%3D%E4%B8%AD%E6%96%87')
 def test_multiple_features(self):
  self.assertCode(node({'AR':'BGX','CF':'XXZ','FX':['W','T']}),'A1!XXXX.BGX.XXT.X.X+FX:W,Z')
  # No handle and a window are compatible; no handle and twisted handle are not.
  self.assertCode(node({'AR':'BGX','CF':'XXN','FX':['W']}),'A1!XXXX.BGX.XXN.X.X+FX:W')
  for cf,fx in [('XXN',['T']),('XXT',['F']),('XXT',['T'])]:
   with self.assertRaises(SpecError):self.e.encode(node({'AR':'BGX','CF':cf,'FX':fx}))
 def test_lid_function_without_saleability(self):
  self.assertCode(node({'AR':'CUX','FR':'CLOSURE','LP':'D','AP':'STRAW_HOLE'}),'A1!XXXX.CUX.XXX.X.X+AP:STRAW_HOLE.FR:CLOSURE.LP:D')
  self.assertCode(node({'AR':'CUL','CF':'XXD','FR':'CLOSURE'}),'A1!XXXX.CUL.XXD.X.X')
  for f in [{'AR':'BGL'},{'AR':'BGX','FR':'CLOSURE'},{'AR':'CUX','AP':'NONE'},{'AR':'CUL','LP':'D'},{'AR':'CUB','FR':'CLOSURE'}]:
   with self.assertRaises(SpecError):self.e.encode(node(f))
 def test_consistency_and_applicability(self):
  for f in [{'MA':'BKWX','BL':'UNBLEACHED'},{'MA':'APTX','BL':'BLEACHED'},{'MA':'APTX','GS':'40'},{'AR':'CYX','TT':'tin tie'},{'MA':'APTX','FS':'VIRGIN','PR':'20'},{'MA':'APTX','PF':'UNTESTED'},{'MA':'APTX','CL':'PRINTED'},{'MA':'APTX','CO':['NONE','BPI']},{'AR':'BGX','CF':'XXN','HL':'twisted'}]:
   with self.subTest(f=f),self.assertRaises(SpecError):self.e.encode(node(f))
 def test_malformed_unsupported_duplicates(self):
  prefix='A1!APTX.CUX.XXX.X.X'
  bad=['A2!APTX.CUX.XXX.X.X',prefix+'.NEW',prefix+'+ZZ:foo',prefix+'+CL:WHITE.CL:BLACK',prefix+'+MA:APTX',prefix+'+UT:CA=%FF',prefix+'+UT:CA=%2',prefix+'~S(INSIDE){CL:WHITE',prefix+'~K(KIT){MA:APTX}',prefix+'~S(UNKNOWN){CL:WHITE}',prefix+'+DM:HEIGHT=1,HEIGHT=2',prefix+'+QC:[CA,TARGET,FILL,-;CA,TARGET,FILL,-]',prefix+'~L(X){}',prefix+'~L(X){-}',prefix+'~S(INSIDE){-}',prefix+'~L(O){MA:APTX}|L(X){MA:APTX}']
  for code in bad:
   with self.subTest(code=code),self.assertRaises(SpecError):self.e.decode(code)
 def test_canonical_and_complete_extensions(self):
  non='A1!APTX.CUX.XXX.M0500_00.R98_0+OP:CLEAR.CL:WHITE'
  canonical='A1!APTX.CUX.XXX.M500.R98+CL:WHITE.OP:CLEAR'
  self.assertEqual(self.e.canonicalize(non),canonical)
  with self.assertRaises(SpecError):self.e.decode(non)
  self.assertFalse(self.e.compare(canonical,canonical.replace('WHITE','BLACK'))['equal_description'])
 def test_measurement_comparison(self):
  def f(cap,**extra):return node({'AR':'CUX','CA':cap,**extra})
  self.assertEqual(self.e.compare_measurement(f('M490-510'),f('M495-505'),'CA')['result'],'satisfies')
  self.assertEqual(self.e.compare_measurement(f('M490-510'),f('M500-520'),'CA')['result'],'contradiction')
  self.assertEqual(self.e.compare_measurement(f('M500'),f('X'),'CA')['result'],'information_gap')
  self.assertEqual(self.e.compare_measurement(f('M500'),f('M500',QC=[['CA','APPROXIMATE','UNKNOWN','-']]),'CA')['result'],'incompatible_context')
  self.assertFalse(self.e.compare_measurement(f('M500',TO=[['CA','10','10']]),f('M500',TO=[['CA','5','5']]),'CA')['equal_measurement_description'])
 def test_dictionary_only_subprocess(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td);shutil.copytree(ROOT/'atlas',path/'atlas',ignore=shutil.ignore_patterns('__pycache__'));shutil.copy(D,path/'dictionary.json')
   p=subprocess.run([sys.executable,'-m','atlas','--dictionary','dictionary.json','decode','A1!BKRX.BGX.XLX.X.X~L(X){MA:APTX;MA:BKRX}'],cwd=path,text=True,capture_output=True)
   self.assertEqual(p.returncode,0,p.stderr);self.assertTrue(json.loads(p.stdout)['complete'])
 def test_resource_refusal(self):
  with self.assertRaises(SpecError):self.e.decode('A1!'+'X'*100001)
 def test_workbook_expected_codes(self):
  data=json.loads((ROOT/'fixtures/verified-batch.json').read_text())
  self.assertEqual(len(data['records']),12)
  for r in data['records']:
   with self.subTest(record=r['id']):
    if r['facts']:self.assertCode(r['facts'],r['expected_code'])
    else:self.assertIsNone(r['expected_code']);self.assertTrue(r['uncertainty'])
 def test_workbook_mapping_independent(self):
  rs={r['id']:r for r in json.loads((ROOT/'fixtures/verified-batch.json').read_text())['records']}
  self.assertEqual(rs['V4']['cells']['D4']['value'],'Plastic - PS');self.assertEqual(rs['V4']['facts']['fields']['MA'],'APSX')
  self.assertEqual(rs['V4']['cells']['E4']['value'],'Bowl Lid');self.assertEqual(rs['V4']['facts']['fields']['AR'],'BWX')
  self.assertEqual(rs['V7']['supplier_context']['A']['source'],'A4');self.assertEqual(rs['V18']['supplier_context']['A']['source'],'A18')
  self.assertEqual(rs['V18']['cells']['O18']['value'],'=P18/H18');self.assertEqual(rs['V18']['cells']['O18']['kind'],'formula')
  self.assertEqual(rs['V961']['cells']['F961']['value'],'7.5 (H) x 5.75 (W) x 1.375 (G) inches')
  self.assertEqual(rs['V961']['facts']['fields']['DM']['GUSSET'],{'value':'1.375','unit':'in'})
  self.assertEqual(rs['V962']['expected_code'],rs['V963']['expected_code']);self.assertNotEqual(rs['V962']['outside']['customization'],rs['V963']['outside']['customization'])
  self.assertEqual(rs['V993']['rows'],[993,997]);self.assertIn('D996',rs['V993']['cells']);self.assertIsNone(rs['V993']['facts'])
  self.assertEqual(rs['V1088']['facts']['fields']['MA'],'BKRX');self.assertNotIn('FI',rs['V1141']['facts']['fields'])
  self.assertEqual(len(rs['V1141']['facts']['groups'][0]['layers']),3);self.assertEqual(rs['V1141']['facts']['groups'][0]['direction'],'X')
  self.assertIsNone(rs['V1143']['facts']);self.assertTrue(rs['V1143']['cells']['C1143']['value'].startswith('Example:'))

class AdditionalTests(unittest.TestCase):
 def setUp(self):self.e=Engine(D)
 def test_repeated_scope_intervals(self):
  f=node({'AR':'BGX'},[{'scope':'BODY','node':node({'GW':['2','3']})},{'scope':'BODY','node':node({'CL':'WHITE'})}])
  self.assertEqual(self.e.encode(f),'A1!XXXX.BGX.XXX.X.X~S(BODY){CL:WHITE.GW:2-3}')
 def test_scope_complementary_facts(self):
  groups=[{'scope':'BODY','node':node({'MA':'BKRX','AR':'BGX','CF':'XXT','DM':{'HEIGHT':'20'}})}, {'scope':'BODY','node':node({'MA':'BKRP','CF':'XXW','DM':{'WIDTH':'30'}})}]
  self.assertEqual(self.e.encode(node({'AR':'BGX'},groups)),'A1!XXXX.BGX.XXX.X.X~S(BODY){AR:BGX.CF:XXT.DM:HEIGHT=20,WIDTH=30.FX:W.MA:BKRP}')
  groups=[{'scope':'BODY','node':node({'AR':'CUX','FR':'CLOSURE'})},{'scope':'BODY','node':node({'AP':'NONE'})}]
  self.assertIn('AP:NONE.AR:CUX.FR:CLOSURE',self.e.encode(node({'AR':'CUX'},groups)))
 def test_dictionary_rule_changes_rejected(self):
  d=copy.deepcopy(self.e.d);d['policy']['inheritance']='Yes'
  with self.assertRaises(SpecError):check_compatible(self.e.d,d)
 def test_numeric_unknown_standards_fail_explicitly(self):
  for key in ['GA','EC']:
   with self.assertRaises(SpecError):self.e.encode(node({'AR':'BXX',key:'32'}))
   sid=self.e.encode(node({'AR':'BXX','UT':[[key,'32; standard unspecified']]}));self.assertIn(key+'=32',sid)
  with self.assertRaises(SpecError):self.e.encode(node({'AR':'CTX','FF':'arbitrary-product-123'}))
 def test_no_silent_empty_or_extra_input(self):
  for f in [{'CL':''},{'UT':[]},{'DM':{}},{'MA':'APTX','GW':None},{'MA':'APTX','GW':{'value':'2','unit':'g','supplier':'A'}}]:
   with self.assertRaises(SpecError):self.e.encode(node(f))
 def test_percentage_tolerance_bounds(self):
  self.assertIn('TO:[PR,0,1]',self.e.encode(node({'MA':'APTX','PR':'0','TO':[['PR','0','1']]})))
  with self.assertRaises(SpecError):self.e.encode(node({'MA':'APTX','PR':'100','TO':[['PR','0','1']]}))
 def test_construction_and_feedstock(self):
  for f in [{'MA':'BKRX','CF':'XJX'},{'MA':'BKCX','FS':'VIRGIN'},{'MA':'BKVX','FS':'PCR'},{'MA':'APTX','FS':'VIRGIN','PR':['0','2']}]:
   with self.assertRaises(SpecError):self.e.encode(node(f))
 def test_retained_core_vocabulary_execution(self):
  # Each test input explicitly supplies the scope from the retained registry.
  count=0
  for fam,grades in self.e.t['GRADE'].items():
   for grade in grades:
    fields={'MA':fam+grade+'X','AR':'CUX'}
    targets=[]
    if fam=='9':targets.append(['MA_FAMILY','illustrative other family'])
    if grade=='99':targets.append(['MA_GRADE','illustrative other grade'])
    if targets:fields['OT']=targets
    code=self.e.encode(node(fields));self.assertEqual(self.e.decode(code)['fields']['MA'],fields['MA']);count+=1
  for article,features in self.e.t['FEATURE'].items():
   if article=='_DEFAULT':article='LN'
   for feature in features:
    if article=='CY' and feature=='M':continue
    fields={'AR':article+'X','CF':'XX'+feature}
    if feature=='9':fields['OT']=[['CF_FEATURE','illustrative other feature']]
    code=self.e.encode(node(fields));self.assertEqual(self.e.decode(code)['fields']['CF'],'XX'+feature);count+=1
  self.assertGreater(count,200)
 def test_all_legacy_rows_have_disposition(self):
  import csv
  for file in (ROOT/'reference/legacy-registries').glob('*.csv'):
   with file.open() as stream:originals=list(csv.DictReader(stream))
   recorded=[r['entry'] for r in self.e.d['legacy_disposition'] if r['file']==file.name]
   self.assertEqual(originals,recorded)
 def test_json_duplicate_cli_fails(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'duplicate.json';p.write_text('{"fields":{"MA":"APTX","MA":"APPX"}}')
   r=subprocess.run([sys.executable,'-m','atlas','--dictionary',str(D),'encode',str(p)],cwd=ROOT,capture_output=True,text=True)
   self.assertEqual(r.returncode,2);self.assertIn('Duplicate JSON key',r.stderr)

class RepairRegressionTests(unittest.TestCase):
 def setUp(self):self.e=Engine(D)
 def test_restrictive_numeric_maximum_is_incompatible(self):
  code='A1!APTX.XXX.XXX.X.X+PR:100'
  self.assertEqual(self.e.decode(code)['fields']['PR'],'100')
  changed=copy.deepcopy(self.e.d);changed['fields']['PR']['maximum']='50'
  with self.assertRaisesRegex(SpecError,'Quantity above maximum'):Engine(changed).decode(code)
  with self.assertRaises(SpecError):check_compatible(self.e.d,changed)
 def test_numeric_minimum_and_new_bound_are_incompatible(self):
  cases=[('PR','minimum','positive','A1!APTX.XXX.XXX.X.X+PR:0'),
         ('GW','maximum','1','A1!APTX.XXX.XXX.X.X+GW:2')]
  for field,key,value,code in cases:
   with self.subTest(field=field,key=key):
    self.e.decode(code);changed=copy.deepcopy(self.e.d);changed['fields'][field][key]=value
    with self.assertRaises(SpecError):Engine(changed).decode(code)
    with self.assertRaises(SpecError):check_compatible(self.e.d,changed)
 def test_other_field_semantic_properties_are_preserved(self):
  for key in ['ordering','unknown','not_applicable']:
   with self.subTest(key=key):
    changed=copy.deepcopy(self.e.d);changed['fields']['PR'][key]='changed rule'
    with self.assertRaises(SpecError):check_compatible(self.e.d,changed)
  changed=copy.deepcopy(self.e.d);del changed['fields']['PR']['maximum']
  with self.assertRaises(SpecError):check_compatible(self.e.d,changed)
 def test_new_reference_only_role_cannot_disable_existing_code(self):
  code='A1!APTX.CUB.XXX.X.X';self.e.decode(code)
  changed=copy.deepcopy(self.e.d);changed['reference_only_roles'].append('B')
  with self.assertRaises(SpecError):Engine(changed).decode(code)
  with self.assertRaises(SpecError):check_compatible(self.e.d,changed)
 def test_supported_field_additions_and_retirement_remain_compatible(self):
  changed=copy.deepcopy(self.e.d)
  changed['fields']['CL']['domain'].append('PURPLE')
  changed['fields']['ZZ']=copy.deepcopy(changed['fields']['NC'])
  changed['fields']['CL']['retired']=True
  self.assertTrue(check_compatible(self.e.d,changed))
  e2=Engine(changed)
  self.assertEqual(e2.decode('A1!APTX.XXX.XXX.X.X+CL:WHITE'),self.e.decode('A1!APTX.XXX.XXX.X.X+CL:WHITE'))
  e2.decode('A1!APTX.XXX.XXX.X.X+CL:PURPLE.ZZ:illustrative')
 def scope_groups(self):
  return [{'scope':'BODY','node':node({'CL':'WHITE'})},
          {'scope':'BODY','node':{'fields':{'OP':'OPAQUE'},'unsupported_extra':'must not disappear'}}]
 def test_repeated_scope_unsupported_child_rejected_both_orders(self):
  groups=self.scope_groups()
  for ordered in [groups,list(reversed(groups))]:
   with self.subTest(order=ordered),self.assertRaisesRegex(SpecError,'Node accepts only fields and groups'):
    self.e.encode(node({'MA':'APTX'},ordered))
 def test_standalone_unsupported_child_rejected(self):
  with self.assertRaisesRegex(SpecError,'Node accepts only fields and groups'):
   self.e.encode(node({'MA':'APTX'},self.scope_groups()[1:]))
 def test_valid_scope_merge_still_allowed_both_orders(self):
  groups=self.scope_groups();del groups[1]['node']['unsupported_extra']
  for ordered in [groups,list(reversed(groups))]:
   self.assertEqual(self.e.encode(node({'MA':'APTX'},ordered)),
                    'A1!APTX.XXX.XXX.X.X~S(BODY){CL:WHITE.OP:OPAQUE}')
 def test_raw_scope_container_types_rejected_before_merge(self):
  for bad in [{'fields':[]},{'groups':{}},[]]:
   for reverse in [False,True]:
    groups=[{'scope':'BODY','node':node({'CL':'WHITE'})},{'scope':'BODY','node':bad}]
    if reverse:groups.reverse()
    with self.subTest(bad=bad,reverse=reverse),self.assertRaises(SpecError):
     self.e.encode(node({'MA':'APTX'},groups))

if __name__=='__main__':unittest.main()
