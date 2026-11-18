"""Independent conservative local-seat study. Never replaces whole acceptance."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
from contract114 import BODY,S,digest
from shared_geometry137 import rect,overlaps,local_polyline_clear
IDS=('sofa1','sofa2','armchair1','armchair2','armchair3','armchair4')
SCENARIO='SHARED137_ALL_OTHER_ACTIVITIES_RESERVED'
# Extra conservative study: other activities remain obstacles, no concurrency exemptions.
SOURCE_PINS={'contract114.py': '8fa52a9d992cd078e7dd3356bab61de7b9687d60a4ae52fc403a3e0b2203dbcf', 'assemble114.py': 'b12cf81eb0acdfd5c696445fe7821235012f589cac9477b865da89093c0b095e', 'fixture_catalog114.json': 'fdfd29e5aa90f263ede216f7102d3bc2d242c0dc93058600ec2340f0f8c241e4'} # Frozen136 source snapshot; independent review still required.

def source_check():
 for name,h in SOURCE_PINS.items():
  if hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_CHANGED:'+name)
 if len(SOURCE_PINS)!=3 or BODY!=F('.7'):raise ValueError('BODY_SOURCE_CONTRACT_CHANGED')

def reconstruct(model,uid,proposal):
 source_check()
 if F(model['profile']['body_m'])!=BODY or F(model['source_geometry_contract']['body_m'])!=BODY:raise ValueError('MODEL_BODY_CHANGED')
 units=[u for u in model['units']if u['id']==uid]
 if len(units)!=1:raise ValueError('UNIQUE_UNIT_REQUIRED')
 u=units[0];L=F(model['inputs'][1]);uses={}
 def tr(q):
  a,b,c,d=map(F,q);return (a,b,c,d)if uid=='A'else(a,L-d,c,L-b)
 for ident in IDS:
  key=ident+'_use'if ident.startswith('sofa')else 'chair'+ident[-1]+'_use'
  a,b,c,d=rect(proposal['rectangles'][key]);w,h=c-a,d-b
  if ident.startswith('sofa'):
   if(w,h)==(F('2.2'),F('1.6')):fx=(a,b,c,b+F('.9'));ac=(a,b+F('.9'),c,d);rot=0
   elif(w,h)==(F('1.6'),F('2.2')):fx=(a+BODY,b,c,d);ac=(a,b,a+BODY,d);rot=90
   else:raise ValueError('SOURCE_SIZE:'+ident)
   size=(F('2.2'),F('.9'))
  else:
   if(w,h)!=(F('.8'),F('1.5')):raise ValueError('SOURCE_SIZE:'+ident)
   fx=(a,b+BODY,c,d);ac=(a,b,c,b+BODY);rot=0;size=(F('.8'),F('.8'))
  if rect(u['fixtures'][ident])!=tr(fx) or rect(u['activities'][ident+'_front'])!=tr(ac):raise ValueError('SOURCE_GEOMETRY:'+ident)
  md=u['fixture_metadata'][ident]
  expected_kind=ident if ident.startswith('sofa')else('armchair1'if ident in('armchair1','armchair3')else'armchair2')
  if md.get('kind')!=expected_kind:raise ValueError('SOURCE_KIND:'+ident)
  if tuple(F(str(v))for v in md['source_size_m'])!=size or md['rotation_deg']!=rot or md.get('walkable'):raise ValueError('SOURCE_METADATA:'+ident)
  aa,bb,cc,dd=tr(ac);target=((aa+cc)/2,(bb+dd)/2)
  if tuple(map(F,u['route_targets'][ident+'_front']))!=target:raise ValueError('REAL_ACTIVITY_TARGET:'+ident)
  uses[ident]=tr((a,b,c,d))
 group=(min(q[0]for q in uses.values()),min(q[1]for q in uses.values()),max(q[2]for q in uses.values()),max(q[3]for q in uses.values()))
 return u,uses,group

def obstacles(model,u,target):
 # Derived internally; callers cannot erase blockers. All walls, panels, fixtures,
 # other activities and private circulation remain conservative local obstacles.
 return list(model['walls'].values())+[o['open_panel']for o in model.get('operations',{}).get('doors',[])]+[q for unit in model['units']for q in unit['fixtures'].values()]+[q for unit in model['units']for k,q in unit['activities'].items()if not(unit['id']==u['id']and k==target)]+u['rooms'].get('private_circulation',[])

def check(model,uid,proposal,packet):
 try:
  u,uses,g=reconstruct(model,uid,proposal)
  if packet['scenario']!=SCENARIO or set(packet['paths'])!=set(IDS):raise ValueError('SIX_UNIQUE_PATHS_AND_SCENARIO_REQUIRED')
  w=rect(packet['witness']);a,b,c,d=w
  if(c-a,d-b)!=(BODY,BODY) or not(g[0]<=a<c<=g[2]and g[1]<=b<d<=g[3]):raise ValueError('WITNESS_BODY_OR_TIGHT_GROUP')
  if any(overlaps(w,rect(q))for q in list(uses.values())+obstacles(model,u,None)):raise ValueError('WITNESS_NOT_ADDITIONAL_FREE_SPACE')
  start=((a+c)/2,(b+d)/2);lengths={}
  for ident in IDS:
   path=[tuple(map(F,p))for p in packet['paths'][ident]];target=tuple(map(F,u['route_targets'][ident+'_front']))
   if not path or path[0]!=start or path[-1]!=target:raise ValueError('PATH_ENDPOINT:'+ident)
   if not local_polyline_clear(path,BODY,g,obstacles(model,u,ident+'_front')):raise ValueError('LOCAL_BODY_SWEEP:'+ident)
   lengths[ident]=S(sum(abs(x-u)+abs(y-v)for(x,y),(u,v)in zip(path,path[1:])))
  return {'status':'LOCAL_STUDY_PASS_NOT_FULL_GATE','source_pins':SOURCE_PINS,'model_hash':digest(model),'packet_hash':digest(packet),'lengths_m':lengths,'scope':'One extra body position and conservative local routes; not comfort, spaciousness or complete quality.'}
 except(KeyError,TypeError,ValueError)as exc:return {'status':'LOCAL_STUDY_FAIL','reason':str(exc)}
