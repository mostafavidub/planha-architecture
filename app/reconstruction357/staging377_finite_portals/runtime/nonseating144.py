"""No-through-route study for seating group. Additional constraint, not relaxation."""
from fractions import Fraction as F
from contract114 import BODY,S,digest
from shared_geometry137 import overlaps,rect
POLICY='NONSEATING_WHOLE_GROUP_EXCLUSION144'
SEATING=tuple(x+'_front'for x in('sofa1','sofa2','armchair1','armchair2','armchair3','armchair4'))
def envelope(unit):
 names=('sofa1','sofa2','armchair1','armchair2','armchair3','armchair4')
 qs=[rect(unit['fixtures'][k])for k in names]+[rect(unit['activities'][k+'_front'])for k in names]
 return(min(q[0]for q in qs),min(q[1]for q in qs),max(q[2]for q in qs),max(q[3]for q in qs))
def route_obstacles(unit,name):
 return []if name in SEATING or name=='guest_living'else[envelope(unit)]
def require(p):
 if p.get('nonseating_protection144')!=POLICY:raise ValueError('NONSEATING144_POLICY_REQUIRED')
 from seating_source142 import validate_proposal
 validate_proposal(p)
def check_model(model):
 errors=[];out={};h=BODY/2
 if F(model['profile']['body_m'])!=BODY:raise ValueError('BODY_CONTRACT')
 if sorted(u['id']for u in model['units'])!=['A','B']:raise ValueError('TWO_UNIQUE_UNITS_REQUIRED')
 for u in model['units']:
  group=envelope(u);count=0
  if set(u['activities'])!=set(u['route_targets'])or not set(u['route_targets'])<=set(u['routes']):errors.append(u['id']+':INCOMPLETE_ACTIVITY_ROUTE_INVENTORY')
  if not {'guest_living','guest_dining','kitchen_to_dining_floor'}<=set(u['scenario_routes']):errors.append(u['id']+':INCOMPLETE_PUBLIC_SCENARIOS')
  for field in('routes','scenario_routes'):
   for name,path in u[field].items():
    if not route_obstacles(u,name):
     target='sofa1_front'if name=='guest_living'else name
     if not path or tuple(map(F,path[-1]))!=tuple(map(F,u['route_targets'][target])):errors.append(u['id']+':'+name+':EXEMPT_SOURCE_ENDPOINT')
     continue
    count+=1;points=[tuple(map(F,p))for p in path]
    if not points:errors.append(u['id']+':'+name+':EMPTY');continue
    segments=list(zip(points,points[1:]))or[(points[0],points[0])]
    for (x,y),(X,Y)in segments:
     if x!=X and y!=Y:errors.append(u['id']+':'+name+':NON_ORTHOGONAL');break
     swept=(min(x,X)-h,min(y,Y)-h,max(x,X)+h,max(y,Y)+h)
     if overlaps(swept,group):errors.append(u['id']+':'+name+':BODY_SWEEP_THROUGH_GROUP');break
  out[u['id']]={'nonseating_paths_checked':count,'group':list(map(S,group))}
 return {'status':'PASS_NONSEATING_ZERO_GROUP_CROSS144'if not errors else'FAIL','errors':errors,'model_hash':digest(model),'units':out,'scope':'All recorded nonseating route body sweeps excluded from group; completeness/physical legality still require unchanged whole gate.'}

def check_packet(packet):
 if packet['family']!='LEFT_RIGHT'or packet['core']['world_from_local']!={'matrix':[[0,1],[1,0]],'translation':['0','0']}:raise ValueError('NONSEATING144_FRAME')
 local=packet['local_model'];world=packet['world_model'];audits={k:check_model(packet[k])for k in('local_model','world_model')}
 if any(a['status']!='PASS_NONSEATING_ZERO_GROUP_CROSS144'for a in audits.values()):raise ValueError('NONSEATING144_BODY_SWEEP:'+str(audits))
 wu={u['id']:u for u in world['units']}
 if len(wu)!=2 or set(wu)!={'A','B'}or sorted(u['id']for u in local['units'])!=['A','B']:raise ValueError('NONSEATING144_UNITS')
 for u in local['units']:
  v=wu[u['id']]
  for field in('routes','scenario_routes'):
   if set(u[field])!=set(v[field]):raise ValueError('NONSEATING144_ROUTE_INVENTORY')
   for name,path in u[field].items():
    if route_obstacles(u,name) and [tuple(map(F,p))for p in v[field][name]]!=[(F(p[1]),F(p[0]))for p in path]:raise ValueError('NONSEATING144_WORLD_ROUTE_TRANSFORM:'+name)
 return audits
