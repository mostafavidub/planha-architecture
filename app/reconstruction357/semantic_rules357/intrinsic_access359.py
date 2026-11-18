"""New357 exact intrinsic access closures; no solver, no fresh or parent approval.
Stored paths are witnesses only: a blocked path is UNKNOWN, not impossibility.
"""
from pathlib import Path
from fractions import Fraction as F
import types,time
from common import digest
from modules_spatial import rect,intersection,union_area,source_sweeps
from guest_closure import transformed_rect
HERE=Path(__file__).resolve().parent
PROFILES={'SOURCE359':'method_registry_source359.json'}
def need(x,c):
 if not x:raise ValueError(c)
def bound_rows(m,raw,profile):
 need(profile in PROFILES,'UNREGISTERED_PROFILE')
 cm=types.ModuleType('_intrinsic_access_bound_common');cm.__file__=str(HERE/'common.py');exec(compile((HERE/'common.py').read_bytes(),cm.__file__,'exec'),cm.__dict__);cm.REGISTRY_NAME=PROFILES[profile]
 return cm.rows(m,raw)
def point(p):
 need(type(p)is list and len(p)==2 and all(type(v)in(str,int)for v in p),'EXACT_POINT');return tuple(map(F,p))
def contains(r,parts):return union_area([x for p in parts if(x:=intersection(r,p))])==union_area([r])
def private_parts(m,u):
 """Union sources are intentionally overlapping, never area-counted twice."""
 uid=u['id'];ds=[d for d in m['private_domains']if d['unit']==uid];need(ds,'PRIVATE_DOMAINS_MISSING')
 beds={uid+'.'+k for k in u['rooms']if k.startswith('bed')};need(set().union(*(set(d['bedrooms'])for d in ds))==beds,'PRIVATE_BED_INVENTORY')
 parts=[rect(p)for d in ds for p in d['parts']]
 for name,rs in u['rooms'].items():
  md=u.get('room_metadata',{}).get(name,{})
  globalmd=m.get('room_metadata',{}).get(uid+'.'+name,{})
  if name.startswith('bed')or 'private' in name.lower()or 'vestibule' in name.lower()or md.get('private')is True or globalmd.get('private')is True:parts.extend(map(rect,rs))
 for key,value in m.get('logical_regions',{}).items():
  if value.get('unit')==uid and ('PRIVATE' in value.get('kind','').upper()or'VESTIBULE'in value.get('kind','').upper()):
   need(type(value.get('parts'))is list,'PRIVATE_LOGICAL_PARTS_MISSING');parts.extend(map(rect,value['parts']))
 return parts

def pathcheck(path,body,floor,obstacles):
 collisions=[];uncovered=[]
 for i,s in enumerate(source_sweeps(path,body)):
  if not contains(s,floor):uncovered.append(i)
  for label,r in obstacles:
   x=intersection(s,r)
   if x:collisions.append({'segment':i,'obstacle':label,'intersection':list(map(str,x))})
 return {'verdict':'PASS_SCOPED_PATH'if not collisions and not uncovered else'UNKNOWN_STORED_PATH_BLOCKED','collisions':collisions,'uncovered_segments':uncovered,'sweep_profile_m':str(body)}
def require_row(rs,key):
 r=rs[key];need(r['status']=='PASS_LIMITED','SOURCE_PREREQUISITE:'+key);w=r['evidence']['witness'];need(not w.get('errors')and not w.get('pending'),'SOURCE_PENDING:'+key);return w

def evaluate(model,raw,profile='SOURCE359',seconds=8):
 start=time.monotonic();out={'schema':'INTRINSIC_ACCESS359','verdict':'UNKNOWN','minima':{},'parent_complete':False,'fresh_executed':False,'missing':[]}
 original=digest([model,raw])
 try:
  need(type(seconds)in(int,float)and 0<seconds<=10,'BOUNDED_SECONDS');rs=bound_rows(model,raw,profile)
  for k in('core_concept','opening_hosts','door_operation','private_grouping','bath_nonprivate_access'):require_row(rs,k)
  body=F(model['profile']['body_m']);need(body==F('.7'),'SOURCE_BODY_PROFILE');h=body/2
  ops=model['operations']['doors'];ids=[o['opening_id']for o in ops];need(len(ids)==len(set(ids)),'DOOR_OPERATION_INVENTORY');dw=require_row(rs,'door_operation');need(set(ids)==set(dw['actual_operation_ids']),'FRESH_OPERATION_BINDING')
  panels=[('open_panel:'+o['opening_id'],rect(o['open_panel']))for o in ops]
  walls=[('wall:'+k,rect(v))for k,v in model['walls'].items()];fixtures=[(u['id']+'.fixture:'+k,rect(v))for u in model['units']for k,v in u['fixtures'].items()]
  openings=model['openings'];need(len({o['id']for o in openings})==len(openings),'OPENING_UNIQUE')
  common=model['common_spaces'];need(set(common)=={'stair','lift','lobby'},'COMMON_INVENTORY');lobby=list(map(rect,common['lobby']));expected_routes={s+'_'+u['id']for s in('stair','lift')for u in model['units']};need(set(model['common_routes'])==expected_routes,'ARRIVAL_ROUTE_INVENTORY')
  coreinterfaces={}
  for s in('stair','lift'):
   oo=[o for o in openings if set(o['connects'])=={s,'lobby'}];need(len(oo)==1,'CORE_INTERFACE_INVENTORY');o=oo[0];need(o.get('kind')=='core_access_interface'and o.get('leaf_modeled')is False,'SOURCE_NONLEAF_CORE_ONLY');coreinterfaces[s]=rect(o['rect'])
  for u in model['units']:
   need(time.monotonic()-start<seconds,'CLOSURE_DEADLINE');uid=u['id'];owner=list(map(rect,u['ownership']));root=point(u['entry_point']);private=private_parts(model,u)
   # All typed private polygons become solid obstacles, including circulation and vestibules.
   wet=[];bp=[p for p in model['module_placements']if p['unit_id']==uid and p['room_id']=='bath'];need(len(bp)==1,'BATH_SOURCE_INVENTORY');bp=bp[0];need(bp['module_hash']==digest(bp['module']),'BATH_SOURCE_HASH')
   floors=[rect(r)for v in u['rooms'].values()for r in v]+[rect(o['rect'])for o in openings if any(c.startswith(uid+'.')for c in o['connects'])]
   others=[('other_owner:'+v['id'],rect(r))for v in model['units']if v['id']!=uid for r in v['ownership']]
   for target in('WC_front','shower_use','basin_front'):
    path=u['routes'][target];need(point(path[0])==root,'WET_ROOT');need(root in {point(p[-1])for k,p in model['common_routes'].items()if k.endswith('_'+uid)},'WET_COMMON_ENDPOINT');activity=rect(u['activities'][target]);need(activity==transformed_rect(bp['module']['unit']['activities'][target],bp['transform']),'WET_SOURCE_ACTIVITY')
    end=point(path[-1]);need(end==point(u['route_targets'][target])and end==((activity[0]+activity[2])/2,(activity[1]+activity[3])/2),'WET_SOURCE_TARGET')
    wetfixtures=fixtures
    if target=='shower_use':
     # Exact task exception from checker114 source bath module routing, never a generic walkable flag.
     need(bp['module']['schema']=='BATHROOM_MODULE117','SHOWER_SOURCE_SCHEMA');sid=bp['id_map']['shower_floor'];need(u['fixture_metadata'][sid]['kind']=='shower_floor','SHOWER_SOURCE_KIND')
     need(rect(u['fixtures'][sid])==transformed_rect(bp['module']['unit']['fixtures']['shower_floor'],bp['transform']),'SHOWER_SOURCE_GEOMETRY')
     wetfixtures=[(label,r)for label,r in fixtures if label!=uid+'.fixture:'+sid]
    proof=pathcheck(path,body,floors,walls+wetfixtures+panels+others+[('private_deleted',r)for r in private]);proof.update(unit=uid,target=target,private_union_area=str(union_area(private)));wet.append(proof)
   arrival=[];eo=[o for o in openings if 'lobby'in o['connects']and any(c.startswith(uid+'.')for c in o['connects'])];need(len(eo)==1 and eo[0]['id']in ids,'ENTRY_OPERATION_JOIN');entryop=next(o for o in ops if o['opening_id']==eo[0]['id']);need(entryop.get('states')and entryop.get('continuous_actor_segments'),'ENTRY_CONTINUOUS_OPERATION')
   entry=list(map(rect,u['rooms']['entry_circulation']));public=entry+list(map(rect,u['rooms']['living']))
   for src,other in(('stair','lift'),('lift','stair')):
    region=rect(common[src]);path=model['common_routes'][src+'_'+uid];a,b=point(path[0]),point(path[-1]);need(contains((a[0]-h,a[1]-h,a[0]+h,a[1]+h),[region]),'ARRIVAL_SOURCE_POSE');need(contains((b[0]-h,b[1]-h,b[0]+h,b[1]+h),entry),'ARRIVAL_ENTRY_POSE')
    floor=[region]+lobby+public+[rect(eo[0]['rect']),coreinterfaces[src]]
    proof=pathcheck(path,body,floor,walls+fixtures+panels+others+[('opposite_core',rect(common[other]))]);need(any(intersection(s,r)for s in source_sweeps(path,body)for r in lobby),'LOBBY_TRAVERSAL');proof.update(unit=uid,source=src,entry_opening=eo[0]['id'],operation_digest=digest(entryop),scenario='SOURCE_NONLEAF_CORE_INTERFACE_PLUS_ALL_MODELED_DOORS_OPEN_TRANSIT');arrival.append(proof)
   out['minima'][uid]={'H07':{'verdict':'PASS_SCOPED_INTRINSIC'if all(p['verdict']=='PASS_SCOPED_PATH'for p in wet)else'UNKNOWN','routes':wet},'H05_H15_Q10_ARRIVAL':{'verdict':'PASS_SCOPED_INTRINSIC'if all(p['verdict']=='PASS_SCOPED_PATH'for p in arrival)else'UNKNOWN','routes':arrival}}
  need(digest([model,raw])==original,'INPUT_MUTATION');out['verdict']='PASS_SCOPED_INTRINSIC_ACCESS'if all(v['verdict']=='PASS_SCOPED_INTRINSIC'for u in out['minima'].values()for v in u.values())else'UNKNOWN';out['evidence']={'model_digest':digest(model),'raw_digest':digest(raw),'profile':profile,'bound_requirement_ids':sorted(rs)}
 except (ValueError,KeyError,TypeError,IndexError,StopIteration) as e:out['missing']=['ACCESS_CLOSURE:'+str(e)]
 out['scope']='SOURCE_0.7M_OPEN_TRANSIT_STORED_PATHS; NO_TECHNICAL_CORE_CERTIFICATION_OR_FULL_12_RULE_PASS';out['seconds']=time.monotonic()-start;return out
