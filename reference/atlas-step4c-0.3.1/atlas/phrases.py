"""Bounded deterministic vocabulary. Every unconsumed span remains visible."""
import re
from .records import need
from .search import Search

WORDS={
 'cup':('AR_CLASS','CU'),'cups':('AR_CLASS','CU'),
 'lid':('FR','CLOSURE'),'lids':('FR','CLOSURE'),
 'bag':('AR_CLASS','BG'),'bags':('AR_CLASS','BG'),
 'pet':('MA_GRADE','APT'),'pp':('MA_GRADE','APP'),'ps':('MA_GRADE','APS'),
 'kraft':('MA_GRADE','BKR'),'paper':('MA_FAMILY','B'),
 'clear':('OP','CLEAR'),'white':('CL','WHITE'),'uncoated':('MA_TREATMENT','N'),
 'laminate':('laminate',True),'laminates':('laminate',True),
 'kit':('kind','kit'),'kits':('kind','kit')}

class Phrases:
    def __init__(self,store): self.s=store
    def propose(self,phrase,*,actor,reason,provenance='operational'):
        need(isinstance(phrase,str) and phrase.strip(),'Phrase required')
        criteria=[]; evidence={}; unsupported=[]
        # Ordered scanner consumes complete known patterns only; punctuation and
        # unsupported words are never silently stripped.
        pattern=r'\s+|(?:rim|height|width|depth)\s+\d+(?:\.\d+)?\s*(?:mm|cm|in)\b|\d+(?:\.\d+)?\s*(?:ml|litres?|liters?|l)\b|[A-Za-z]+|[^\sA-Za-z]+'
        for m in re.finditer(pattern,phrase,re.I):
            text=m.group(); token=text.lower()
            if token.isspace(): continue
            dim=re.fullmatch(r'(rim|height|width|depth)\s+(\d+(?:\.\d+)?)\s*(mm|cm|in)',token)
            volume=re.fullmatch(r'(\d+(?:\.\d+)?)\s*(ml|litres?|liters?|l)',token)
            if dim:
                name,value,unit=dim.groups(); criteria.append({'field':'FI' if name=='rim' else 'DM_'+name.upper(),'value':{'value':value,'unit':unit}})
            elif volume:
                value,unit=volume.groups(); criteria.append({'field':'CA','value':{'value':value,'unit':'mL' if unit=='ml' else 'L'}})
            elif token in WORDS:
                field,value=WORDS[token]; criteria.append({'field':field,'value':value})
            elif token in ('quoted','sampled','photos'):
                evidence[{'quoted':'quotation','sampled':'sampling','photos':'photos'}[token]]=True
            else: unsupported.append({'text':text,'start':m.start(),'end':m.end(),'reason':'Unsupported or ambiguous wording; review explicitly'})
        seen={}
        for c in criteria:
            f=c['field']
            if f in seen and seen[f]!=c['value']: unsupported.append({'text':phrase,'reason':'Conflicting alternatives for '+f+'; edit criteria'})
            seen[f]=c['value']
        query={'criteria':criteria,**({'evidence':evidence} if evidence else {})}
        rid=self.s.add('phrase_review',{'phrase':phrase,'proposed':query,'unsupported':unsupported},actor=actor,reason=reason,provenance=provenance)
        return {'review':rid,'phrase':phrase,'proposed':query,'unsupported':unsupported,'executed':False}

    def confirm(self,review,query,*,confirmed,acknowledged,actor,reason,provenance='operational'):
        r=self.s.get(review,'phrase_review')
        need(confirmed is True,'Explicit confirmation required before interpreted search')
        need(acknowledged==r['data']['unsupported'],'Acknowledge every unsupported/ambiguous span; edit criteria to express the intended supported subset')
        Search(self.s).validate(query)
        return self.s.add('phrase_confirmation',{'query':query,'acknowledged':acknowledged},{'review':review},actor=actor,reason=reason,provenance=provenance)

    def execute(self,confirmation):
        r=self.s.get(confirmation,'phrase_confirmation'); review=self.s.get(self.s.one(confirmation,'review'))
        return {'interpretation':review,'confirmation':r,'search':Search(self.s).search(r['data']['query'])}
