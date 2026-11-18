"""Experimental multi-dimensional comparison. Not architectural quality/admission.
Uses preserved whole-gate bindings + source geometry descriptor; no solver.
Exact rational spatial relations; no arbitrary owner distance threshold.
"""
import sys,json,itertools
from pathlib import Path
from fractions import Fraction as F
import diversity124 as base
EPS=F(0)
D4=[[[a,0],[0,b]]for a in (-1,1)for b in (-1,1)]+[[[0,a],[b,0]]for a in (-1,1)for b in (-1,1)]
def box(rs):
 rs=[base.q(r)for r in rs];return(min(r[0]for r in rs),min(r[1]for r in rs),max(r[2]for r in rs),max(r[3]for r in rs))
def tr(r,M):return base.transform({'transform':{'matrix':M,'translation':[0,0]}})(r)
def relation(a,b):
 out=[]
 for axis in (0,1):
  gap=b[axis]-a[axis+2];reverse=a[axis]-b[axis+2]
  if gap>EPS:out.append('BEFORE')
  elif reverse>EPS:out.append('AFTER')
  elif min(a[axis+2],b[axis+2])-max(a[axis],b[axis])>EPS:out.append('OVERLAP')
  else:out.append('UNCERTAIN_CONTACT')
 return out

def spatial_variants(m):
 # Each source-bound functional role is retained. Repeated compatible bedrooms
 # are merged conservatively, never assigned artificial diversity by their IDs.
 labels={p['unit_id']+'.'+p['room_id']:('bedroom:twin'if p['module']['schema']=='PRIVATE_TWIN_ROOM_MODULE118'else 'bedroom:double'if p['module']['schema']=='PRIVATE_ROOM_MODULE116'else p['room_id'])for p in m['module_placements']}
 variants=[]
 for M in D4:
  unitrows=[]
  for u in m['units']:
   regions={}
   for role,rs in u['rooms'].items():
    key=labels.get(u['id']+'.'+role)
    if key:regions.setdefault(key,[]).extend(rs)
   # Dining is bound through immutable source fixtures in base descriptor.
   dp=u['dining_module_placement'];dt=base.transform(dp)
   regions['dining_activity']=[dt(r)for r in dp['module']['fixtures'].values()]
   regions['common_stair']=[m['common_spaces']['stair']]
   regions['common_lift']=[m['common_spaces']['lift']]
   boxes={k:tr(box(v),M)for k,v in regions.items()}
   unitrows.append({a+'|'+b:{'relation':relation(boxes[a],boxes[b]),'bounds':[list(map(str,boxes[a])),list(map(str,boxes[b]))]}for a,b in itertools.combinations(sorted(boxes),2)})
  variants.append(unitrows)
 return variants

def route_facts(m):
 rows=[]
 for u in m['units']:
  facts={}
  for key,path in {**u['routes'],**u.get('scenario_routes',{})}.items():
   ps=[tuple(F(str(v))for v in p)for p in path];segments=[(b[0]-a[0],b[1]-a[1])for a,b in zip(ps,ps[1:])];segments=[d for d in segments if d!=(0,0)]
   headings=[(int(x>0)-int(x<0),int(y>0)-int(y<0))for x,y in segments]
   facts[key]={'length_m':str(sum(abs(x)+abs(y)for x,y in segments)),'turns':sum(a!=b for a,b in zip(headings,headings[1:])),'endpoints':[list(map(str,ps[0])),list(map(str,ps[-1]))]}
  rows.append({'unit':u['id'],'paths':facts})
 return {'units':rows,'meaning':'Current stored functional path geometry, bound to preserved admitted model. Metrics are NOT a separate diversity proof; operations/route validity not rerun by this study.'}

def describe(c):
 d=base.describe_candidate(c);m=c['model']
 p=json.loads(d['program_key']);p['frame']=[sorted(p['frame'][:2],key=F),p['frame'][2]]
 return {'program_key':base.canonical(p),'access_signature':d['access_signature'],'spatial':spatial_variants(m),'model_hash':base.digest(m),'source_witness':d['witness'],'path_facts':route_facts(m),'whole_gate_reexecuted':False}

def compare(a,b):
 if a['program_key']!=b['program_key']:return {'status':'INCOMPARABLE_PROGRAM','distinct':False}
 if a['access_signature']!=b['access_signature']:return {'status':'DISTINCT_SOURCE_ACCESS_RELATION','distinct':True,'dimensions':['access_graph']}
 # Compare against every whole isometry and unit permutation. A robust mismatch
 # must survive all matches; uncertain contact never establishes a difference.
 left=a['spatial'][0];alternatives=[]
 for right in b['spatial']:
  for perm in itertools.permutations(right):
   proof=[];unknown=[]
   for i,(x,y)in enumerate(zip(left,perm)):
    if set(x)!=set(y):return {'status':'UNRESOLVED_ROLE_INVENTORY','distinct':False}
    for k in x:
     for ax,(v,w)in enumerate(zip(x[k]['relation'],y[k]['relation'])):
      if v==w:continue
      if 'UNCERTAIN_CONTACT'in(v,w):unknown.append([i,k,ax,v,w])
      elif {v,w}=={'BEFORE','AFTER'} and 'dining_activity' not in k:
       proof.append({'unit_match':i,'roles':k,'axis':ax,'relation':[v,w],'actual_bounds':[x[k]['bounds'],y[k]['bounds']]})
      else:unknown.append([i,k,ax,v,w,'NOT_SUFFICIENT_ALONE'])
   alternatives.append({'robust_differences':proof,'uncertain':unknown})
 if alternatives and all(v['robust_differences']for v in alternatives):
  return {'status':'DISTINCT_SPATIAL_ROLE_ORDER_SCOPED','distinct':True,'dimensions':['strict_order_reversal_of_source_bound_rooms_or_core'],'isometry_permutation_comparisons':len(alternatives),'least_difference_witness':min(alternatives,key=lambda x:len(x['robust_differences']))}
 return {'status':'UNRESOLVED_NO_ROBUST_MULTIDIMENSIONAL_DIFFERENCE','distinct':False,'reason':'Same spatial/access abstraction or changes only at uncertain boundaries; not proof of identical architecture.'}
