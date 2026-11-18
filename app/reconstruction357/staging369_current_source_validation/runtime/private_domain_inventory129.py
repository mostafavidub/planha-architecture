"""Exact swap-XY private-domain transport, not topology or privacy approval.
Closed versioned records: no key inferred from producer status or free metadata.
"""
from fractions import Fraction as F
from contract114 import S
from copy import deepcopy
FIELDS={'unit','bedrooms','parts','public_interface','paths','route_failures','topology_scope','functional_wall_purpose','quality_comparison'}
def point(p):
 if not isinstance(p,list)or len(p)!=2:raise ValueError('POINT_SHAPE')
 return [S(F(str(p[1]))),S(F(str(p[0])))]
def rectangle(r):
 if not isinstance(r,list)or len(r)!=4:raise ValueError('RECT_SHAPE')
 return [S(F(str(r[i])))for i in(1,0,3,2)]
def examine(local,world):
 errors=[]
 try:
  a=local['private_domains'];b=world['private_domains']
  if len(a)!=len(b)or {x['unit']for x in a}!={u['id']for u in local['units']}:raise ValueError('DOMAIN_INVENTORY')
  for i,(src,dst)in enumerate(zip(a,b)):
   if set(src)!=FIELDS or set(dst)!=FIELDS:raise ValueError('UNKNOWN_OR_MISSING_DOMAIN_FIELD')
   if set(src['public_interface'])!={'rect','open_side'}or set(dst['public_interface'])!={'rect','open_side'}:raise ValueError('UNKNOWN_OR_MISSING_INTERFACE_FIELD')
   if set(src['paths'])!=set(src['bedrooms']):raise ValueError('PATH_TARGET_INVENTORY')
   e=deepcopy(src);e['parts']=[rectangle(r)for r in src['parts']];e['public_interface']['rect']=rectangle(src['public_interface']['rect']);e['public_interface']['open_side']={'top':'right','bottom':'left','left':'bottom','right':'top'}[src['public_interface']['open_side']];e['paths']={k:[point(p)for p in ps]for k,ps in src['paths'].items()}
   if e!=dst:errors.append('PRIVATE_DOMAIN_D4_BINDING:'+str(i))
 except(KeyError,TypeError,ValueError,IndexError)as ex:errors.append('PRIVATE_DOMAIN_TRANSPORT_SCHEMA:'+str(ex))
 return {'errors':errors,'pending':[],'scope':'Closed current domain-record transport only. Fresh source placement, enclosure, body access and public-observer privacy remain mandatory.','accepted':False}
