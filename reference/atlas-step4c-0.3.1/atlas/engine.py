"""Atlas A1 local dictionary/identifier engine. Standard library only."""
import copy,json,re
from fractions import Fraction
from pathlib import Path
from urllib.parse import unquote_to_bytes

VERSION='0.1.1'
class SpecError(ValueError): pass

def require(ok,message):
    if not ok: raise SpecError(message)

def exact(value):
    require(not isinstance(value,(float,bool)), 'Use exact strings or integers, not floating point/bool')
    if isinstance(value,Fraction): return value
    require(isinstance(value,(str,int)), 'Expected exact number')
    s=str(value).replace('_','.')
    require(bool(re.fullmatch(r'-?\d+(?:\.\d+|/\d+)?',s)),f'Malformed exact number: {value}')
    try: return Fraction(s)
    except (ValueError,ZeroDivisionError): raise SpecError('Invalid fraction')

def number(value):
    n=exact(value); sign='-' if n<0 else '';n=abs(n);d=n.denominator
    a=b=0
    while d%2==0:d//=2;a+=1
    while d%5==0:d//=5;b+=1
    if d!=1:return sign+str(n.numerator)+'/'+str(n.denominator)
    places=max(a,b); v=n.numerator*(10**places//n.denominator)
    if not places:return sign+str(v)
    s=str(v).zfill(places+1);return sign+(s[:-places]+'_'+s[-places:]).rstrip('0').rstrip('_')

def escape(s):
    require(isinstance(s,str) and bool(s),'Expected nonempty exact text')
    return ''.join(chr(b) if 65<=b<=90 or 97<=b<=122 or 48<=b<=57 or b in (45,95) else f'%{b:02X}' for b in s.encode('utf-8'))

def unescape(s):
    require(bool(re.fullmatch(r'(?:[A-Za-z0-9_-]|%[0-9A-Fa-f]{2})+',s)),'Malformed escaped text')
    try:return unquote_to_bytes(s).decode('utf-8','strict')
    except UnicodeError:raise SpecError('Invalid UTF-8')

def split(s,delimiter):
    stack=[];start=0;parts=[];pairs={')':'(',']':'[','}':'{'}
    for i,c in enumerate(s):
        if c in '([{':stack.append(c)
        elif c in ')]}':
            require(stack and stack.pop()==pairs[c],'Unbalanced delimiters')
        elif c==delimiter and not stack:parts.append(s[start:i]);start=i+1
    require(not stack,'Unbalanced delimiters');parts.append(s[start:]);return parts

class Engine:
    def __init__(self,dictionary):
        self.d=json.loads(Path(dictionary).read_text()) if isinstance(dictionary,(str,Path)) else copy.deepcopy(dictionary)
        require(self.d.get('namespace')=='A1','Unsupported dictionary namespace')
        self.t=self.d['tables'];self.f=self.d['fields']
    def unit(self,v,canonical):
        if isinstance(v,dict):
            require(set(v)=={'value','unit'},'Quantity requires exactly value and unit')
            u=self.d['units'].get(v['unit']);require(u is not None,f"Unsupported unit {v['unit']}")
            require(u['canonical']==canonical,f'Incompatible quantity role/unit, expected {canonical}')
            raw=v['value'];factor=exact(u['factor'])
        else:raw=v;factor=Fraction(1)
        if isinstance(raw,str) and re.fullmatch(r'\d+(?:[._]\d+|/\d+)?-\d+(?:[._]\d+|/\d+)?',raw):raw=raw.split('-')
        vals=raw if isinstance(raw,list) else [raw]
        require(len(vals) in [1,2],'Expected scalar or two interval endpoints')
        return [exact(x)*factor for x in vals]
    def amount(self,v,unit,positive=True,integer=False,maximum=None):
        vals=self.unit(v,unit)
        require(all(x>0 if positive else x>=0 for x in vals),'Quantity outside domain')
        require(not integer or all(x.denominator==1 for x in vals),'Count endpoints must be integers')
        require(maximum is None or all(x<=exact(maximum) for x in vals),'Quantity above maximum')
        require(len(vals)==1 or vals[0]<=vals[1],'Reversed interval')
        if len(vals)==2 and vals[0]==vals[1]:vals=vals[:1]
        return '-'.join(number(x) for x in vals)
    def quantity(self,k,v):
        if v in ('X','0') if isinstance(v,str) else False:return v
        if isinstance(v,str):
            require(v and v[0] in ('MGN' if k=='CA' else 'R'),f'Unsupported {k} prefix')
            p=v[0];raw=v[1:].split('-');require(len(raw)<=2,'Malformed interval')
            unit={'M':'mL','G':'g','N':'count','R':'mm'}[p]
            return p+self.amount(raw if len(raw)>1 else raw[0],unit,integer=p=='N')
        require(isinstance(v,dict),'Quantity must be explicit object or encoded block')
        require(set(v)=={'value','unit'},'Quantity requires value and unit; qualifiers use QC')
        u=self.d['units'].get(v['unit']);require(u is not None,'Unsupported or unresolved unit')
        p={'mL':'M','g':'G','count':'N'}.get(u['canonical']) if k=='CA' else ('R' if u['canonical']=='mm' else None)
        require(p is not None,'Incompatible quantity role')
        return p+self.amount(v,u['canonical'],integer=p=='N')
    def token(self,table,v,label):
        require(isinstance(v,str) and v in table,f'Unsupported {label}: {v}');return v
    def blocks(self,fields):
        ma=fields.get('MA','XXXX');ar=fields.get('AR','XXX');cf=fields.get('CF','XXX')
        require(isinstance(ma,str) and len(ma)==4,'MA requires four characters')
        require(isinstance(ar,str) and len(ar)==3,'AR requires three characters')
        require(isinstance(cf,str) and len(cf)==3,'CF requires three characters')
        fam,grade,trt=ma[0],ma[1:3],ma[3];art,role=ar[:2],ar[2]
        self.token(self.t['FAMILY'],fam,'family');self.token(self.t['GRADE'].get(fam,{}),grade,'grade');self.token(self.t['TREATMENT'],trt,'treatment')
        self.token(self.t['ARTICLE'],art,'article');self.token(self.t['ROLE'],role,'role')
        require(role not in self.d['reference_only_roles'],'Supplier kits need separate component IDs')
        require(role!='L' or art in self.d['lid_bearing'],'Closure role incompatible with article')
        self.token(self.t['SHAPE'],cf[0],'shape');self.token(self.t['CONSTRUCTION'],cf[1],'construction')
        ft=self.t['FEATURE_LID'] if role=='L' else self.t['FEATURE'].get(art,self.t['FEATURE']['_DEFAULT'])
        self.token(ft,cf[2],'feature')
        require(not (art=='XX' and cf[2] not in ['X','0','9']),'Feature needs local article scope')
        require(not (art=='CY' and cf[2]=='M'),'Mixed kit cannot be a base specification')
        return ma,ar,cf,ft
    def target(self,target,fields,other=False):
        require(isinstance(target,str),'Target must be string')
        valid=set(self.d['slot_targets'])|set(self.d.get('unresolved_targets',[]))|set(self.f)|{'CA','FI'}|{'DM_'+x for x in self.d['dimensions']}
        require(target in valid,f'Unsupported target {target}')
        if other:require(target in self.d['slot_targets'],'OT explains a registered core slot')
    def numeric_target(self,target,fields):
        if target.startswith('DM_'):
            require(target[3:] in fields.get('DM',{}),'Qualifier/tolerance target missing dimension');return fields['DM'][target[3:]],'mm',False
        require(target in fields,'Qualifier/tolerance target missing')
        if target in ['CA','FI']:
            s=fields[target];require(s not in ['X','0'],'Unknown/NA target cannot be qualified');return s[1:],{'M':'mL','G':'g','N':'count','R':'mm'}[s[0]],s[0]=='N'
        require(self.f.get(target,{}).get('type') in ['num','int'],'Target is not numeric')
        return fields[target],self.f[target]['unit'],self.f[target]['type']=='int'
    def normalize_fields(self,raw,root=False):
        require(isinstance(raw,dict),'Fields must be object; duplicates are forbidden')
        fields=copy.deepcopy(raw)
        unknown=set(fields)-set(self.f);require(not unknown,f'Unsupported/misplaced fields: {sorted(unknown)}')
        ma,ar,cf,ft=self.blocks(fields)
        for k in ['CA','FI']:
            if k in fields:fields[k]=self.quantity(k,fields[k])
        for k,v in list(fields.items()):
            spec=self.f[k];kind=spec['type'];app=spec['applicability']
            for axis,value in [('families',ma[0]),('articles',ar[:2]),('constructions',cf[1])]:
                if axis in app:require(value in app[axis],f'{k} needs explicit local {axis}: {app[axis]}')
            if kind=='enum':self.token(spec['domain'],v,k)
            elif kind=='list':
                require(isinstance(v,list) and v,'Expected nonempty list')
                require(all(x in spec['domain'] for x in v),f'Unsupported {k} list token')
                require(not ('NONE' in v and len(set(v))>1),'Contradictory NONE claim');fields[k]=sorted(set(v))
            elif kind in ['num','int']:fields[k]=self.amount(v,spec['unit'],positive=spec.get('minimum')!='0',integer=kind=='int',maximum=spec.get('maximum'))
            elif kind=='str':
                escape(v)
                if k=='FF':require(v in self.d['registered_fitments'],'Unsupported registered fitment; preserve targeted UT instead')
            elif kind=='dimensions':
                require(isinstance(v,dict) and v,'DM needs named dimensions')
                require(set(v)<=set(self.d['dimensions']),'Unsupported dimension name')
                fields[k]={name:self.amount(val,'mm') for name,val in sorted(v.items())}
            elif kind=='profile':self.token(self.t['FEATURE_LID'],v,k);require(v not in ['X','0','9'],'LP needs known profile')
            elif kind=='features':
                require(isinstance(v,list) and v,'FX needs token list')
                for x in v:self.token(ft,x,'additional feature');require(x not in ['X','0','9'],'FX requires positive known features')
            elif kind=='statements':
                require(isinstance(v,list) and v,'Statements require list of [target,text]')
                for entry in v:
                    require(isinstance(entry,list) and len(entry)==2,'Statement requires target and text');self.target(entry[0],fields,k=='OT');escape(entry[1])
                require(len({tuple(x) for x in v})==len(v),'Duplicate statement')
                if k=='OT':require(len({x[0] for x in v})==len(v),'Duplicate OT target')
                fields[k]=sorted(v)
        if 'FX' in fields:
            fs=fields.pop('FX')+[cf[2]] if cf[2] not in ['X'] else fields.pop('FX')
            require(len(set(fs))==len(fs),'Duplicate feature');require(not any(x in ['0','9'] for x in fs),'Reserved feature mixed with positive')
            fs=sorted(fs);cf=cf[:2]+fs[0];fields['CF']=cf
            if len(fs)>1:fields['FX']=fs[1:]
        fs=[cf[2]]+fields.get('FX',[])
        rules=self.d['feature_rules'].get('LID' if ar[2]=='L' else ar[:2],self.d['feature_rules']['_DEFAULT'])
        for group in rules['exclusive_sets']:require(len(set(fs)&set(group))<=1,'Mutually exclusive features')
        require(not (set(fs)&set(rules['negative']) and len(fs)>1),'Plain feature contradicts positive features')
        function={'B':'BODY','L':'CLOSURE','A':'ACCESSORY'}.get(ar[2])
        if 'FR' in fields and function:
            require(fields['FR']==function,'Role/function contradiction');fields.pop('FR')
        closure=function=='CLOSURE' or fields.get('FR')=='CLOSURE'
        if closure:require(ar[:2] in self.d['lid_bearing'],'Closure function incompatible with article')
        if 'AP' in fields:require(closure,'AP requires explicit local closure function')
        if 'LP' in fields:require(closure and ar[2]!='L','LP requires closure function and role other than L')
        for rule in self.d.get('construction_rules',[]):
            if cf[1]==rule['construction'] and ma[0] not in ['X','9']:
                require(ma[0] in rule['families'], 'Construction contradicts known material family')
        if ma[:3]=='BKW':require(fields.get('BL','BLEACHED')=='BLEACHED','KW/bleach contradiction')
        if ma[:3]=='BKB':require(fields.get('BL','UNBLEACHED')=='UNBLEACHED','KB/bleach contradiction')
        if fields.get('FS')=='VIRGIN' and 'PR' in fields:require(all(exact(x)==0 for x in fields['PR'].split('-')),'Virgin contradicts recycled content')
        if ma[:3] in ['BKC','ARP']:
            require(fields.get('FS')!='VIRGIN','Recycled grade contradicts virgin feedstock')
        if ma[:3]=='BKV':require(fields.get('FS') not in ['RECYCLED','PCR'],'Virgin grade contradicts recycled feedstock')
        if 'FF' in fields:require(fields.get('FI','X') in ['X','0'],'Non-circular footprint contradicts circular fitment')
        if ar[:2]=='BG':
            require(not(cf[2]=='N' and 'HL' in fields),'No handle contradicts handle detail')
        vals=[ma[0],ma[1:3],ma[3],ar[:2],ar[2],cf[0],cf[1],cf[2]]
        needed={k for k,v in zip(self.d['slot_targets'],vals) if set(v)=={'9'}}
        explanations={x[0] for x in fields.get('OT',[])}
        require(needed==explanations,f'OT targets must exactly explain OTHER slots: {sorted(needed)}')
        for k in ['QC','TO']:
            if k not in fields:continue
            rows=fields[k];require(isinstance(rows,list) and rows,f'{k} requires nonempty entries');seen=set();out=[]
            for row in rows:
                require(isinstance(row,list) and len(row)==(4 if k=='QC' else 3),f'Malformed {k}')
                target=row[0];require(target not in seen,f'Duplicate {k} target');seen.add(target)
                value,unit,integer=self.numeric_target(target,fields)
                if k=='QC':
                    _,mode,basis,condition=row;require(mode in self.d['qualifiers']['modes'] and basis in self.d['qualifiers']['bases'],'Invalid qualifier')
                    require(basis not in ['FILL','BRIM'] or target=='CA' and unit=='mL','Basis requires volume capacity')
                    require(basis!='NA' or unit!='mL','NA basis incompatible with volume')
                    require(isinstance(condition,str) and bool(condition),'Condition must be text or -')
                    if row[1:]!=['REPORTED','UNKNOWN','-']:out.append(row)
                else:
                    require('-' not in value,'Tolerance cannot duplicate interval')
                    offsets=[self.amount(x,unit,positive=False,integer=integer) for x in row[1:]]
                    require(all('-' not in x for x in offsets),'Tolerance offsets must be scalar')
                    lower=exact(value)-exact(offsets[0]); upper=exact(value)+exact(offsets[1])
                    minimum=self.f.get(target,{}).get('minimum','positive')
                    require(lower>=0 if minimum=='0' else lower>0,'Tolerance lower bound outside quantity domain')
                    maximum=self.f.get(target,{}).get('maximum')
                    require(maximum is None or upper<=exact(maximum),'Tolerance upper bound outside quantity domain')
                    out.append([target]+offsets)
            if out:fields[k]=sorted(out)
            else:fields.pop(k)
        for k,v in list(fields.items()):
            if k in ['MA','AR','CF','CA','FI'] and v in ['XXXX','XXX','X'] and not root:fields.pop(k)
        return fields
    def field_text(self,k,v):
        kind=self.f[k]['type']
        if kind=='str':return escape(v)
        if kind in ['enum','profile','block','quantity','num','int']:return v
        if kind in ['list','features']:return ','.join(v)
        if kind=='dimensions':return ','.join(n+'='+x for n,x in sorted(v.items()))
        if kind=='statements':return ','.join(t+'='+escape(x) for t,x in v)
        if kind=='qualifiers':return '['+';'.join(','.join(row[:3]+[escape(row[3]) if row[3]!='-' else '-']) for row in v)+']'
        if kind=='tolerances':return '['+';'.join(','.join(row) for row in v)+']'
        raise SpecError('Unsupported field type')
    def merge_local(self,left,right):
        """Merge facts in the same explicitly named scope; never across scopes."""
        result=copy.deepcopy(left)
        for key,value in right.items():
            if key not in result:result[key]=copy.deepcopy(value);continue
            old=result[key]
            if old==value:continue
            if key in ['MA','AR','CF']:
                widths={'MA':[1,2,1],'AR':[2,1],'CF':[1,1,1]}[key]
                require(isinstance(old,str) and isinstance(value,str) and len(old)==sum(widths) and len(value)==sum(widths),'Malformed repeated block')
                parts=[];offset=0
                for width in widths:
                    a,b=old[offset:offset+width],value[offset:offset+width]
                    if a==b:parts.append(a)
                    elif a=='X'*width:parts.append(b)
                    elif b=='X'*width:parts.append(a)
                    elif key=='CF' and offset==2 and a not in ['0','9'] and b not in ['0','9']:
                        parts.append(min(a,b));result['FX']=sorted(set(result.get('FX',[])+[max(a,b)]))
                    else:raise SpecError('Conflicting repeated scope block')
                    offset+=width
                result[key]=''.join(parts)
            elif key=='DM':
                require(isinstance(old,dict) and isinstance(value,dict),'Malformed dimensions')
                for target,x in value.items():
                    require(target not in old or self.amount(old[target],'mm')==self.amount(x,'mm'),'Conflicting repeated dimension')
                    old[target]=x
            elif key in ['CA','FI']:
                require(old=='X' or value=='X' or self.quantity(key,old)==self.quantity(key,value),'Conflicting repeated quantity')
                result[key]=value if old=='X' else old
            elif self.f.get(key,{}).get('type') in ['num','int']:
                spec=self.f[key]
                require(self.amount(old,spec['unit'])==self.amount(value,spec['unit']),'Conflicting repeated measurement')
            elif key in ['OT','QC','TO']:
                combined={r[0]:r for r in old}
                for row in value:
                    require(row[0] not in combined or combined[row[0]]==row,'Conflicting repeated target')
                    combined[row[0]]=row
                result[key]=list(combined.values())
            elif key=='UT':result[key]=[list(x) for x in sorted(set(tuple(x) for x in old+value))]
            elif self.f.get(key,{}).get('type') in ['list','features']:result[key]=sorted(set(old+value))
            else:raise SpecError('Conflicting repeated scope field '+key)
        return result
    @staticmethod
    def validate_node_structure(node):
        """Check raw containers before merging; defer meaning to the merged node."""
        require(isinstance(node,dict) and set(node)<={'fields','groups'},'Node accepts only fields and groups; separate context explicitly')
        require(isinstance(node.get('fields',{}),dict),'Fields must be object; duplicates are forbidden')
        require(isinstance(node.get('groups',[]),list),'Groups must be list')
    def fragment(self,node,root=False,depth=0):
        require(depth<=self.d['policy']['limits']['depth'],'Resource limit exceeded; retained input requires review')
        self.validate_node_structure(node)
        fields=self.normalize_fields(node.get('fields',{}),root)
        groups=node.get('groups',[]);require(isinstance(groups,list),'Groups must be list')
        scopes={};layers=[]
        for group in groups:
            require(isinstance(group,dict),'Group must be object')
            if 'scope' in group:
                require(set(group)=={'scope','node'},'Scope group requires scope and node');name=group['scope'];require(name in self.d['scopes'],'Unsupported scope')
                self.validate_node_structure(group['node'])
                child=copy.deepcopy(group['node'])
                if name not in scopes:scopes[name]=child
                else:
                    a=self.merge_local(scopes[name].get('fields',{}),child.get('fields',{}))
                    scopes[name]={'fields':a,'groups':scopes[name].get('groups',[])+child.get('groups',[])}
            else:
                require(set(group)=={'direction','layers'},'Unsupported group; kits are separate')
                require(group['direction'] in ['O','X','I'],'Unsupported layer direction');require(isinstance(group['layers'],list) and group['layers'],'Empty layer stack')
                require(not layers,'Conflicting layer stacks')
                items=[self.fragment(x,depth=depth+1) for x in group['layers']]
                require(all(x!='-' for x in items),'Empty layer has no supported facts')
                if group['direction']=='I':items.reverse()
                if group['direction']=='X':items.sort()
                layers=['L('+('X' if group['direction']=='X' else 'O')+'){'+ ';'.join(items)+'}']
        encoded=layers+['S('+s+'){'+self.fragment(n,depth=depth+1)+'}' for s,n in scopes.items()]
        require(all(not x.endswith('{-}') for x in encoded),'Empty scope has no facts')
        if root:
            head='.'.join(fields.pop(k,default) for k,default in [('MA','XXXX'),('AR','XXX'),('CF','XXX'),('CA','X'),('FI','X')])
            tail='.'.join(k+':'+self.field_text(k,v) for k,v in sorted(fields.items()))
            result=head+('+'+tail if tail else '')
        else:result='.'.join(k+':'+self.field_text(k,v) for k,v in sorted(fields.items())) or '-'
        return result+('~'+'|'.join(sorted(encoded)) if encoded else '')
    def encode(self,facts):
        require(isinstance(facts,dict),'Expected structured node')
        body=self.fragment(copy.deepcopy(facts),root=True)
        require(body!='XXXX.XXX.XXX.X.X','Unknown-only root is not meaningful')
        code='A1!'+body;require(len(code)<=self.d['policy']['limits']['characters'],'Resource limit exceeded; no truncation');return code
    def parse_fields(self,s):
        result={}
        for part in split(s,'.'):
            require(':' in part,'Malformed field');k,v=part.split(':',1)
            require(k in self.f,f'Unsupported/misplaced field {k}');require(k not in result,f'Duplicate field {k}');require(v!='','Empty field')
            kind=self.f[k]['type']
            if kind=='str':value=unescape(v)
            elif kind in ['list','features']:value=v.split(',')
            elif kind=='dimensions':
                value={}
                for item in v.split(','):
                    require('=' in item,'Malformed dimension');n,x=item.split('=',1);require(n not in value,'Duplicate dimension');value[n]=self.parse_amount(x)
            elif kind=='statements':
                value=[]
                for item in v.split(','):
                    require('=' in item,'Malformed statement');t,x=item.split('=',1);value.append([t,unescape(x)])
            elif kind in ['qualifiers','tolerances']:
                require(v.startswith('[') and v.endswith(']'),'Malformed bracketed field');value=[x.split(',') for x in v[1:-1].split(';')]
                if kind=='qualifiers':
                    for row in value:
                        require(len(row)==4,'Malformed QC');row[3]=unescape(row[3]) if row[3]!='-' else '-'
            elif kind in ['num','int']:value=self.parse_amount(v)
            else:value=v
            result[k]=value
        return result
    @staticmethod
    def parse_amount(s):
        parts=s.split('-');require(len(parts)<=2 and all(parts),'Malformed positive amount');return parts if len(parts)==2 else s
    def parse_node(self,s,root=False,depth=0):
        require(depth<=self.d['policy']['limits']['depth'],'Resource nesting limit exceeded')
        chunks=split(s,'~');require(len(chunks)<=2,'Multiple group separators');head=chunks[0]
        if root:
            bits=split(head,'+');require(len(bits)<=2,'Multiple field separators');core=bits[0].split('.')
            require(len(core)==5,'Core needs five blocks');fields=dict(zip(['MA','AR','CF','CA','FI'],core))
            if len(bits)>1:
                more=self.parse_fields(bits[1]);require(not(set(more)&set(fields)),'Duplicate root block field');fields.update(more)
        else:fields={} if head=='-' else self.parse_fields(head)
        groups=[]
        if len(chunks)==2:
            for g in split(chunks[1],'|'):
                m=re.fullmatch(r'([SL])\(([A-Z_]+)\)\{(.*)\}',g,re.S);require(m is not None,'Malformed group')
                kind,name,content=m.groups()
                if kind=='S':groups.append({'scope':name,'node':self.parse_node(content,depth=depth+1)})
                else:
                    require(name in ['O','X'],'Encoded layer direction must be O or X')
                    groups.append({'direction':name,'layers':[self.parse_node(x,depth=depth+1) for x in split(content,';')]})
        return {'fields':fields,**({'groups':groups} if groups else {})}
    def decode(self,code):
        require(isinstance(code,str) and code.startswith('A1!'),'Unsupported namespace')
        require(len(code)<=self.d['policy']['limits']['characters'],'Resource size limit exceeded')
        node=self.parse_node(code[3:],root=True);canonical=self.encode(node)
        require(canonical==code,f'Noncanonical input; canonical form: {canonical}')
        return node
    def canonicalize(self,value):
        if isinstance(value,str):
            require(value.startswith('A1!'),'Unsupported namespace');require(len(value)<=self.d['policy']['limits']['characters'],'Resource limit')
            return self.encode(self.parse_node(value[3:],root=True))
        return self.encode(value)
    def describe(self,code):
        node=self.decode(code)
        def walk(n,path):
            fs=n['fields'];out=[]
            if 'MA' in fs:
                m=fs['MA'];out.append(f"{path}: material = {self.t['FAMILY'][m[0]]}; {self.t['GRADE'][m[0]][m[1:3]]}; {self.t['TREATMENT'][m[3]]}")
            if 'AR' in fs:
                a=fs['AR'];out.append(f"{path}: article = {self.t['ARTICLE'][a[:2]]}; {self.t['ROLE'][a[2]]}")
            if 'CF' in fs:
                c=fs['CF'];a=fs.get('AR','XXX');ft=self.t['FEATURE_LID'] if a[2]=='L' else self.t['FEATURE'].get(a[:2],self.t['FEATURE']['_DEFAULT'])
                out.append(f"{path}: configuration = {self.t['SHAPE'][c[0]]}; {self.t['CONSTRUCTION'][c[1]]}; {ft[c[2]]}")
            for k,v in fs.items():
                if k in ['MA','AR','CF']:continue
                if k in ['CA','FI']:
                    text={'X':'unknown','0':'explicitly not applicable'}.get(v)
                    if text is None:text=v[1:].replace('_','.')+' '+{'M':'mL capacity','G':'g mass-based capacity/load','N':'count capacity','R':'mm circular rim/opening diameter'}[v[0]]
                elif k=='LP':text=self.t['FEATURE_LID'][v]
                elif k=='FX':
                    a=fs.get('AR','XXX');ft=self.t['FEATURE_LID'] if a[2]=='L' else self.t['FEATURE'].get(a[:2],self.t['FEATURE']['_DEFAULT']);text=', '.join(ft[x] for x in v)
                else:text=json.dumps(v,ensure_ascii=False)+((' '+self.f[k]['unit']) if self.f[k].get('unit') else '')
                out.append(f"{path}: {self.f[k]['description']} = {text}")
            for i,g in enumerate(n.get('groups',[])):
                if 'scope' in g:out+=walk(g['node'],path+'/'+g['scope'])
                else:
                    order='outside-to-inside' if g['direction']=='O' else 'unknown order (display sorted; repeats retained)';out.append(path+': layers '+order)
                    for j,child in enumerate(g['layers']):out+=walk(child,path+f'/layer[{j+1}]')
            return out
        return {'dictionary_release':self.d['release'],'complete':True,'facts':node,'description':walk(node,'product'),'boundary':'Description equality does not establish product identity, fit, or approval.'}
    def compare(self,left,right):
        a=self.canonicalize(left);b=self.canonicalize(right)
        return {'equal_description':a==b,'left':a,'right':b,'supplier_identity_or_fit_or_approval_established':False}
    def compare_measurement(self,request,candidate,target):
        a=self.decode(self.canonicalize(request))['fields'];b=self.decode(self.canonicalize(candidate))['fields']
        try:av,au,_=self.numeric_target(target,a);bv,bu,_=self.numeric_target(target,b)
        except SpecError:return {'result':'information_gap'}
        def qual(fs):return next((r[1:] for r in fs.get('QC',[]) if r[0]==target),['REPORTED','UNKNOWN','-'])
        aq,bq=qual(a),qual(b)
        if au!=bu or aq!=bq or 'APPROXIMATE' in aq:return {'result':'incompatible_context'}
        def interval(s,fs):
            vals=[exact(x) for x in s.split('-')];lo,hi=vals[0],vals[-1]
            for row in fs.get('TO',[]):
                if row[0]==target:lo-=exact(row[1]);hi+=exact(row[2])
            return lo,hi
        al,ah=interval(av,a);bl,bh=interval(bv,b)
        return {'result':'satisfies' if al<=bl and bh<=ah else 'contradiction','equal_measurement_description':av==bv and [r for r in a.get('TO',[]) if r[0]==target]==[r for r in b.get('TO',[]) if r[0]==target],'interchangeability_established':False}

def check_compatible(old,new):
    require(old['namespace']==new['namespace'],'Namespace differs')
    for entry in old['entry_metadata']:
        match=next((x for x in new['entry_metadata'] if (x['registry'],x['scope'],x['token'])==(entry['registry'],entry['scope'],entry['token'])),None)
        require(match and match['meaning']==entry['meaning'],'Old token removed or redefined')
    def subset(a,b,path=''):
        for k,v in a.items():
            require(k in b,f'Removed meaning {path}/{k}')
            if isinstance(v,dict):subset(v,b[k],path+'/'+k)
            else:require(v==b[k],f'Redefined meaning {path}/{k}')
    subset(old['tables'],new['tables']);subset(old['units'],new['units'])
    for k,v in old['fields'].items():
        require(k in new['fields'],'Removed field');w=new['fields'][k]
        # Preserve every field rule, including bounds and newly introduced
        # constraints. Only lifecycle/editorial metadata may change freely.
        metadata={'description','source','introduced','retired','replacement'}
        for key in (set(v)|set(w))-metadata-{'domain'}:
            require(key in v and key in w and v[key]==w[key],f'Redefined field {k}.{key}')
        old_domain,new_domain=v.get('domain'),w.get('domain')
        if isinstance(old_domain,list):
            require(isinstance(new_domain,list) and set(old_domain)<=set(new_domain),f'Removed field value {k}')
        else:require(old_domain==new_domain,f'Redefined field domain {k}')
    for key in ['grammar','policy','qualifiers','construction_rules','validation_rules','feature_rules','reference_only_roles','excluded_fields']:
        require(old[key]==new[key],f'Changed semantic rules {key}; requires namespace review')
    for key in ['scopes','dimensions','lid_bearing','slot_targets','unresolved_targets']:
        require(set(old[key])<=set(new[key]),f'Removed vocabulary {key}')
    subset(old.get('registered_fitments',{}),new.get('registered_fitments',{}))
    return True
