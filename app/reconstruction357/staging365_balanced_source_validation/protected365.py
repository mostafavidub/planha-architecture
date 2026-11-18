"""Exact declared core variant and ownership nondecrease, not functional proof."""
from fractions import Fraction as F

def difference(a,b):
 a=[tuple(map(F,r))for r in a];b=[tuple(map(F,r))for r in b];rr=a+b
 xs=sorted({r[i]for r in rr for i in(0,2)});ys=sorted({r[i]for r in rr for i in(1,3)})
 def inside(x,y,r):return any(l<x<h and t<y<d for l,t,h,d in r)
 return sum(((h-l)*(d-t)for l,h in zip(xs,xs[1:])for t,d in zip(ys,ys[1:])if inside((l+h)/2,(t+d)/2,a)and not inside((l+h)/2,(t+d)/2,b)),F(0))
def check(old,new):
 from core_variant365 import core
 from contract114 import digest
 expected=core(F(new['request']['W']),F(new['request']['L']));actual=new['packet']['core']
 if digest(actual)!=digest(expected):raise ValueError('EXPLICIT_CORE_VARIANT_MISMATCH')
 if digest(actual['entry_centers'])!=digest(expected['entry_centers']):raise ValueError('SOURCE_SELECTED_ENTRIES_CHANGED')
 units=new['model']['units'];prior=old['model']['units']
 if [u['id']for u in units]!=[u['id']for u in prior]:raise ValueError('UNIT_IDENTITIES_CHANGED')
 rows=[]
 for u,v in zip(units,prior):
  if digest(u['ownership'])!=digest(expected['unit_ownership'][u['id']]):raise ValueError('MODEL_CORE_OWNERSHIP_MISMATCH')
  if digest(v['ownership'])!=digest(u['ownership']):raise ValueError('OWNERSHIP_CHANGED')
  floor=[r for rr in u['rooms'].values()for r in rr]
  if difference(floor,u['ownership']):raise ValueError('ROOM_FLOOR_OUTSIDE_OWNERSHIP')
  rows.append({'unit':u['id'],'lost_area':'0','added_area':str(difference(u['ownership'],v['ownership']))})
 return {'scope':'EXACT_SOURCE_VARIANT_OWNERSHIP_NONDECREASE_NOT_FUNCTIONAL','rows':rows,'accepted':False}
