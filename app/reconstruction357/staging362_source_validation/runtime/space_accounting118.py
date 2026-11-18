"""Exact independent floor ledger. UNACCOUNTED_DECLARED_FLOOR is never useful living by name.
This computes physical declared footprints, NOT their operational sufficiency.
"""
from fractions import Fraction as F
from collections import defaultdict
import hashlib,json

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rect(q):
 r=tuple(F(str(v))for v in q)
 if len(r)!=4 or r[0]>=r[2]or r[1]>=r[3]:raise ValueError('INVALID_RECTANGLE')
 return r

def merge(intervals):
 out=[]
 for a,b in sorted(intervals):
  if out and a<=out[-1][1]:out[-1]=(out[-1][0],max(b,out[-1][1]))
  else:out.append((a,b))
 return out

def overlap(a,b):return merge((max(x,z),min(y,w))for x,y in a for z,w in b if max(x,z)<min(y,w))
def subtract(a,b):
 out=list(a)
 for x,y in b:
  new=[]
  for z,w in out:
   if y<=z or x>=w:new.append((z,w));continue
   if z<x:new.append((z,x))
   if y<w:new.append((y,w))
  out=new
 return out

def route_rectangles(path,body):
 if len(path)<2:raise ValueError('ROUTE_HAS_NO_SEGMENT')
 h=body/2;out=[]
 for p,q in zip(path,path[1:]):
  x,y=map(lambda v:F(str(v)),p);a,b=map(lambda v:F(str(v)),q)
  if x!=a and y!=b:raise ValueError('NONORTHOGONAL_ROUTE')
  out.append((min(x,a)-h,min(y,b)-h,max(x,a)+h,max(y,b)+h))
 return out

def ledger(model):
 before=digest(model);results=[];errors=[]
 try:
  body=F(str(model['profile']['body_m']))
  if body<=0:raise ValueError('BODY_PROFILE')
  walls=[rect(q)for q in model['walls'].values()]
  for u in model['units']:
   own=[rect(q)for q in u['ownership']];fx=[rect(q)for q in u['fixtures'].values()];act=[rect(q)for q in u['activities'].values()];routes=[]
   for path in u['routes'].values():routes+=route_rectangles(path,body)
   groups={'ownership':own,'structural':walls,'fixture_footprints':fx,'declared_activity':act,'declared_route':routes}
   bounds=sorted({v for qs in groups.values()for q in qs for v in(q[1],q[3])});areas=defaultdict(F);pieces=defaultdict(list)
   for y,Y in zip(bounds,bounds[1:]):
    mid=(y+Y)/2;ints={k:merge((x,X)for x,a,X,b in qs if a<mid<b)for k,qs in groups.items()}
    owner=ints['ownership'];areas['ownership']+=sum((b-a)*(Y-y)for a,b in owner);remaining=owner
    for k in ('structural','fixture_footprints','declared_activity','declared_route'):
     assigned=overlap(remaining,ints[k]);remaining=subtract(remaining,assigned)
     for a,b in assigned:areas[k]+=(b-a)*(Y-y);pieces[k].append((a,y,b,Y))
    for a,b in remaining:areas['unaccounted_declared_floor']+=(b-a)*(Y-y);pieces['unaccounted_declared_floor'].append((a,y,b,Y))
   if areas['ownership']!=sum(areas[k]for k in('structural','fixture_footprints','declared_activity','declared_route','unaccounted_declared_floor')):raise ValueError('AREA_CONSERVATION')
   # Merge vertically adjacent identical intervals. No bbox approximation of holes.
   compact={}
   for k,qs in pieces.items():
    cols=defaultdict(list)
    for x,y,X,Y in qs:cols[(x,X)].append((y,Y))
    compact[k]=[[str(x),str(y),str(X),str(Y)]for(x,X),ys in sorted(cols.items())for y,Y in merge(ys)]
   results.append({'unit':u['id'],'areas_m2':{k:str(areas[k])for k in('ownership','structural','fixture_footprints','declared_activity','declared_route','unaccounted_declared_floor')},'regions':compact,'usefulness_not_proven_by_accounting':True,'classification_order':'walls, physical fixture footprints, declared activities, declared body routes, unprogrammed remainder; disjoint for accounting only','functional_capacity_evidence':'REQUIRES_SEPARATE_SCENARIO_GATE'})
 except(Exception)as ex:errors.append({'code':'SPACE_ACCOUNTING_FAILED','detail':str(ex)})
 if digest(model)!=before:errors.append({'code':'INPUT_MUTATED'})
 return {'status':'FAIL'if errors else'PASS_LIMITED','errors':errors,'model_hash':before,'witness':{'units':results,'all_areas_exact':True,'residual_is_not_living_or_useful_capacity':True},'scope':'Disjoint exact ownership ledger of declared wall/fixture/activity/body-route footprints and UNACCOUNTED_DECLARED_FLOOR remainder. Not full swept-operation footprint or proof the remainder is unusable/unprogrammed; not activity validation, program sufficiency, minimal circulation or architectural quality.','accepted':False}
