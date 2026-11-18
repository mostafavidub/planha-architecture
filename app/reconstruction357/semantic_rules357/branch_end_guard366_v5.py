"""Pure registered-source branch end preflight. No construction or acceptance.
Derives a bound from complete declared current-source approaches/motions/tasks.
Unknown or unsupported inputs STOP; a bound is not a proof of uselessness.
"""
import json,hashlib
from fractions import Fraction as F
from pathlib import Path
from common import digest
from modules_spatial import rect,intersection,difference,source_sweeps
from guest_closure import transformed_rect
from wall_origin_service365 import hall,load_origin
ROOT=Path(__file__).resolve().parents[1]
def motion(a,b):
 a,b=rect(a),rect(b)
 if a[2]-a[0]!=b[2]-b[0] or a[3]-a[1]!=b[3]-b[1] or (a[0]!=b[0] and a[1]!=b[1]):raise ValueError('UNKNOWN_NONRIGID_OR_NONORTHOGONAL_MOTION_STOP')
 return min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])
def protected_end(branch,domains):
 if not domains:raise ValueError('UNKNOWN_PROTECTED_DOMAIN_INVENTORY_STOP')
 hits=[(name,z)for name,q in domains if(z:=intersection(branch,q))]
 if not hits:raise ValueError('UNKNOWN_NO_BRANCH_FUNCTIONAL_DOMAIN_STOP')
 end=max(q[2]for _,q in hits)
 if not branch[0]<end<=branch[2]:raise ValueError('INVALID_PROTECTED_END')
 return end,hits

def assert_removed_clear(removed,domains):
 for name,q in domains:
  if intersection(q,removed):raise ValueError('PROTECTED_DOMAIN_CROSSES_PROPOSED_REMOVAL_STOP:'+name)
 return True

def propose(record):
 c,m,t=load_origin(record);origin=hall(record);L=F(c['request']['L']);ox,oy=map(F,t['proposal']['ordered_macro']['origin']);out=[]
 # Branch146 construction constants are pinned by executed origin; dimensions
 # below are re-derived from actual walls, not a tuning threshold.
 for u in m['units']:
  uid=u['id'];norm=lambda q:tuple(map(F,q)) if uid=='A' else (F(q[0]),L-F(q[3]),F(q[2]),L-F(q[1]))
  world=lambda q:q if uid=='A'else(q[0],L-q[3],q[2],L-q[1])
  endid=uid+'.private_branch146.branch_end';topid=uid+'.private_branch146.branch_top';ew=norm(m['walls'][endid]);tw=norm(m['walls'][topid]);thickness=ew[2]-ew[0]
  if thickness<=0 or tw[3]-tw[1]!=thickness:raise ValueError('UNKNOWN_SOURCE_WALL_THICKNESS_STOP')
  branch=(ox+F('5.75'),ew[1]+thickness,ew[0],tw[1]);private=[norm(q)for q in u['rooms']['private_circulation']]
  if difference([branch],private):raise ValueError('SOURCE_BRANCH_FLOOR_BINDING_STOP')
  domains=[];portids=[]
  for p in m['module_placements']:
   if p['unit_id']!=uid:continue
   if digest(p['module'])!=p['module_hash']:raise ValueError('SOURCE_MODULE_HASH_STOP')
   for sp in p['module'].get('external_ports',[]):
    oid=p['id_map'][sp['opening_id']];a=[x for x in m['module_ports']if x['opening_id']==oid]
    if len(a)!=1 or transformed_rect(sp['rect'],p['transform'])!=rect(a[0]['rect']):raise ValueError('SOURCE_PORT_BINDING_STOP')
    domains.append(('source_port:'+oid,norm(a[0]['rect'])));portids.append(oid)
  expected={uid+'.bed'+str(i)+'.entry'for i in (1,2,3)}
  if not expected<=set(portids):raise ValueError('UNKNOWN_REQUIRED_BEDROOM_PORT_STOP')
  for k,q in u['activities'].items():
   if k not in u['routes']:raise ValueError('UNKNOWN_TASK_WITHOUT_ROUTE_STOP')
   domains.append(('actual_task:'+k,norm(q)))
  for k,path in {**u['routes'],**u['scenario_routes']}.items():
   for i,q in enumerate(source_sweeps(path,m['profile']['body_m'])):domains.append(('actual_route:'+k+':'+str(i),norm(q)))
  domains += [('actual_fixture:'+k,norm(q))for k,q in u['fixtures'].items()]
  pd=[x for x in m['private_domains']if x['unit']==uid]
  if len(pd)!=1 or pd[0]['route_failures'] or set(pd[0]['paths'])!={uid+'.bed'+str(i)for i in(1,2,3)}:raise ValueError('UNKNOWN_PRIVATE_SOURCE_PATH_INVENTORY_STOP')
  for name,path in pd[0]['paths'].items():
   port=next(x for x in m['module_ports']if x['opening_id']==name+'.entry')
   if list(map(F,path[-1]))!=list(map(F,port['center'])):raise ValueError('PRIVATE_SOURCE_PATH_ENDPOINT_STOP')
   domains += [('source_private_path:'+name+':'+str(i),norm(q))for i,q in enumerate(source_sweeps(path,m['profile']['body_m']))]
  for op in m['operations']['closets']:
   if op['unit']!=uid:continue
   domains += [('closet_shell:'+op['fixture_id'],norm(q))for q in op['shell_rects']]
   for pan in op['panels']:
    domains.append(('closet_full_linear_sweep:'+op['fixture_id'],norm(motion(pan['closed_panel'],pan['open_panel']))))
    domains.append(('closet_rail:'+op['fixture_id'],norm(pan['rail_envelope'])))
    domains += [('closet_actor:'+op['fixture_id'],norm(s['actor_rect']))for s in pan['states']]
    domains += [('closet_actor_continuous:'+op['fixture_id'],norm(motion(s['actor_start'],s['actor_end'])))for s in pan['continuous_actor_segments']]
  for op in m['operations']['kitchen']:
   if op['unit']==uid:
    if not op.get('motion_envelopes'):raise ValueError('UNKNOWN_KITCHEN_MOTION_INVENTORY_STOP')
    domains += [('kitchen_motion_envelope',norm(q))for q in op['motion_envelopes']]
  for op in m['operations']['dining_chairs']:
   if op['unit']==uid:
    domains += [('dining_chair_full_motion',norm(motion(op['closed_rect'],op['open_rect']))),('dining_occupied_body',norm(op['occupied_body']))]
    domains += [('dining_egress',norm(q))for q in source_sweeps(op['egress_route'],m['profile']['body_m'])]
  domains += [('source_living_seat_body',norm(seat['occupied_body']))for seat in u['public_program']['capacity']['living_seats']]
  seen=set()
  for op in m['operations']['doors']:
   if not op['opening_id'].startswith(uid+'.'):continue
   if any(k not in op for k in ('closed_panel','open_panel','translation','pocket','states','continuous_actor_segments')):raise ValueError('UNKNOWN_CONTINUOUS_DOOR_INVENTORY_STOP')
   a,b=rect(op['closed_panel']),rect(op['open_panel']);dx,dy=map(F,op['translation'])
   if (a[0]+dx,a[1]+dy,a[2]+dx,a[3]+dy)!=b:raise ValueError('SOURCE_PANEL_TRANSLATION_STOP')
   domains.append(('panel_full_linear_sweep:'+op['opening_id'],norm(motion(op['closed_panel'],op['open_panel']))));domains.append(('source_rail:'+op['opening_id'],norm(op.get('rail_envelope',op['pocket']))));seen.add(op['opening_id'])
   for i,s in enumerate(op['states']):domains.append(('door_actor:'+op['opening_id']+':'+str(i),norm(s['actor_rect'])))
   for i,s in enumerate(op['continuous_actor_segments']):domains.append(('continuous_actor:'+op['opening_id']+':'+str(i),norm(motion(s['actor_start'],s['actor_end']))))
  if not expected<=seen:raise ValueError('UNKNOWN_REQUIRED_DOOR_OPERATION_STOP')
  bound,hits=protected_end(branch,domains);newend=(bound,ew[1],bound+thickness,ew[3]);newtop=(tw[0],tw[1],bound+thickness,tw[3]);removed=(bound,branch[1],branch[2],branch[3])
  if newtop[2]<=newtop[0]:raise ValueError('SOURCE_BRANCH_JUNCTION_REMOVAL_STOP')
  assert_removed_clear(removed,domains)
  for name,q in domains:
   if intersection(q,newend):raise ValueError('PROTECTED_DOMAIN_CROSSES_NEW_END_WALL_STOP:'+name)
  out.append({'unit':uid,'source_end_before':str(branch[2]),'derived_end':str(bound),'wall_thickness_m':str(thickness),'old_branch_floor':list(map(str,world(branch))),'removed_floor_candidate':list(map(str,world(removed)))if bound<branch[2]else None,'wall_replacements':{endid:list(map(str,world(newend))),topid:list(map(str,world(newtop)))},'bound_witnesses':[{'source_id':n,'intersection':list(map(str,world(q)))}for n,q in hits if q[2]==bound],'complete_declared_protected_domain_digest':digest([(n,list(map(str,q)))for n,q in domains]),'declared_protected_domain_count':len(domains)})
 return {'schema':'SOURCE_BRANCH146_END_PREFLIGHT366_V5_SOURCE_REROUTE_ORACLE','model_digest':digest(m),'record_digest':digest(record),'source_origin':origin[1],'units':out,'status':'PROPOSAL_ONLY_REBUILD_AND_FRESH_REQUIRED','scope':'Registered source146 declared ports/tasks and complete linear door actor/panel motions only. No claim all conceivable activities, uselessness, or post-construction validity.','admission_allowed':False,'fresh_execution':False}

def _expected_branch_projection(before_record,proposal):
 """Internal comparison oracle only, never an emitted/accepted constructor model."""
 import copy,sys,importlib.util
 before=before_record['candidate']['model']
 if proposal['record_digest']!=digest(before_record)or proposal['model_digest']!=digest(before):raise ValueError('PROPOSAL_STALE_STOP')
 # Recompute proposal, not arbitrary caller-provided replacement geometry.
 if digest(propose(before_record))!=digest(proposal):raise ValueError('PROPOSAL_NOT_DERIVED_BY_FIXED_GUARD_STOP')
 expected=copy.deepcopy(before);source=ROOT/'planha_general150_runtime_work';sys.path.insert(0,str(source))
 def module(name):
  path=source/(name+'.py');sha=hashlib.sha256(path.read_bytes()).hexdigest()
  if before_record['trace']['source_inventory'].get(str(path.relative_to(ROOT)))!=sha:raise ValueError('DERIVED_FIELD_SOURCE_PIN_STOP:'+name)
  spec=importlib.util.spec_from_file_location('_branch_guard_'+name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
 cells=module('geometry114').cells;source_S=module('contract114').S
 for row in proposal['units']:
  uid=row['unit'];u=next(u for u in expected['units']if u['id']==uid)
  for key in ('walls','wall_hosts','source_wall_hosts'):expected[key].update({wid:[source_S(F(x)) for x in q] for wid,q in row['wall_replacements'].items()})
  u['rooms']['private_circulation']=cells(u['rooms']['private_circulation'],[row['removed_floor_candidate']]if row['removed_floor_candidate']else[])
  pd=next(p for p in expected['private_domains']if p['unit']==uid);pd['parts']=copy.deepcopy(u['rooms']['private_circulation'])
  expected['logical_regions'][uid+'.private_access']['parts']=copy.deepcopy(u['rooms']['private_circulation'])
 # Re-run ONLY the pinned source routing/public witness phase. This is an
 # independent allowed-delta oracle over changed wall geometry, not acceptance
 # of caller routes or a new full model construction.
 import ast,types
 source_path=source/'assemble146.py';source_bytes=source_path.read_bytes()
 if before_record['trace']['source_inventory'].get(str(source_path.relative_to(ROOT)))!=hashlib.sha256(source_bytes).hexdigest():raise ValueError('SOURCE_ROUTE_PHASE_PIN_STOP')
 tree=ast.parse(source_bytes);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='assemble')
 start=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='allwalls'for x in n.targets))
 stop=next(i for i,n in enumerate(fn.body)if isinstance(n,ast.Assign)and any(isinstance(x,ast.Subscript)and isinstance(x.value,ast.Name)and x.value.id=='m'and isinstance(x.slice,ast.Constant)and x.slice.value=='quality_unverified'for x in n.targets))
 imports=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))]
 body=ast.parse('from nonseating144 import route_obstacles').body+fn.body[start:stop]
 env={'m':expected,'core':before_record['candidate']['packet']['core'],'entry_cx':F(before_record['candidate']['packet']['core']['entry_centers']['A'][0])}
 expected['route_failures']=[]
 exec(compile(ast.fix_missing_locations(ast.Module(body=imports+body,type_ignores=[])),str(source_path)+'#source_route_phase','exec'),env,env)
 for u in expected['units']:
  if 'kitchen_work'in u['routes']:u['routes']['kitchen']=u['routes']['kitchen_work']
 expected=module('public_witness144').install(expected)
 if expected['route_failures']:raise ValueError('SOURCE_REROUTE_FAILED_STOP')
 # Every protected task and operation must survive recomputation unchanged;
 # path geometry may change ONLY as reproduced by this fixed source phase.
 for a,b in zip(before['units'],expected['units']):
  for key in ('id','ownership','fixtures','fixture_metadata','activities','public_program','dining_module_placement'):
   if digest(a[key])!=digest(b[key]):raise ValueError('SOURCE_REROUTE_PROTECTED_FUNCTION_CHANGED_STOP:'+key)
  if set(a['routes'])!=set(b['routes'])or set(a['scenario_routes'])!=set(b['scenario_routes']):raise ValueError('SOURCE_REROUTE_TASK_INVENTORY_CHANGED_STOP')
  for k in a['routes']:
   if a['routes'][k][0]!=b['routes'][k][0]or a['routes'][k][-1]!=b['routes'][k][-1]:raise ValueError('SOURCE_REROUTE_TASK_ENDPOINT_CHANGED_STOP')
 if digest(before['operations'])!=digest(expected['operations']):raise ValueError('SOURCE_REROUTE_OPERATION_CHANGED_STOP')
 expected=module('final_public_floor120').rebuild(expected)
 expected=module('wall_union118').bind_physical_wall_union(expected)
 expected=module('face_threshold118').attach(expected)
 # spatial_roles118 hashes its pre-attach model. Remove only its prior
 # generated fields to reproduce the constructor's first attachment state.
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn.body[stop]],type_ignores=[])),str(source_path)+'#source_pre_role_quality','exec'),env,env)
 expected.pop('spatial_accounting',None)
 for u in expected['units']:
  u.pop('spatial_role_bindings',None)
  expected['room_metadata'].pop(u['id']+'.living',None)
 expected=module('spatial_roles118').attach(expected)
 return expected

def validate_current_paths(before_record,m):
 import sys,importlib.util
 src=ROOT/'planha_general150_runtime_work';sys.path.insert(0,str(src));p=src/'named_checks118.py'
 if before_record['trace']['source_inventory'].get(str(p.relative_to(ROOT)))!=hashlib.sha256(p.read_bytes()).hexdigest():raise ValueError('SOURCE_PATH_CHECKER_PIN_STOP')
 spec=importlib.util.spec_from_file_location('_branch_path_checker',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 checks={'actual_body_owner_wall_fixture':mod.body_route_sweeps(m),'actual_public_required_scenarios':mod.public_named_scenarios(m)}
 for name,result in checks.items():
  if result['status']!='PASS_LIMITED'or result['witness'].get('errors')or result['witness'].get('pending'):raise ValueError('ACTUAL_PATH_CHECK_STOP:'+name)
 private_checks=[]
 for u in m['units']:
  private=list(map(rect,u['rooms']['private_circulation']))
  for name,path in {**u['routes'],**{'scenario:'+k:v for k,v in u['scenario_routes'].items()}}.items():
   if name.startswith('bed'):continue
   if any(intersection(q,b)for q in source_sweeps(path,m['profile']['body_m'])for b in private):raise ValueError('NONPRIVATE_TASK_CROSSES_PRIVATE_DOMAIN_STOP')
  pd=next(x for x in m['private_domains']if x['unit']==u['id']);floor=private+[rect(pd['public_interface']['rect'])]
  obstacles=list(map(rect,m['walls'].values()))+[rect(op['open_panel'])for op in m['operations']['doors']]+[rect(q)for v in m['units']for q in v['fixtures'].values()]
  for name,path in pd['paths'].items():
   port=next(x for x in m['module_ports']if x['opening_id']==name+'.entry')
   if list(map(F,path[-1]))!=list(map(F,port['center'])):raise ValueError('PRIVATE_PATH_ENDPOINT_STOP')
   swept=source_sweeps(path,m['profile']['body_m'])
   if difference(swept,floor)or any(intersection(q,b)for q in swept for b in obstacles):raise ValueError('PRIVATE_PATH_BODY_CLEARANCE_STOP')
   private_checks.append({'target':name,'path_digest':digest(path)})
 return {'source_primitives':checks,'private_domain_paths':private_checks,'scope':'Stored model static/body and source public-scenario rechecks only; no whole fresh review or all-rule acceptance.'}

def compare_constructed(before_record,proposal,after_model):
 expected=_expected_branch_projection(before_record,proposal)
 # Source cell decomposition can split identical floor differently; permit
 # representation changes ONLY for private region cells after exact set equality.
 import copy
 actual=copy.deepcopy(after_model)
 if set(actual)!=set(expected):raise ValueError('COMPLETE_MODEL_KEY_INVENTORY_STOP')
 if [u.get('id')for u in actual['units']]!=[u['id']for u in expected['units']]:raise ValueError('UNIT_ID_INVENTORY_STOP')
 for eu,au in zip(expected['units'],actual['units']):
  eq=list(map(rect,eu['rooms']['private_circulation']));aq=list(map(rect,au['rooms']['private_circulation']))
  if difference(eq,aq)or difference(aq,eq):raise ValueError('CONSTRUCTOR_PRIVATE_FLOOR_PREDICTION_MISMATCH_STOP')
  # No other room is normalized or waived, including living computed above.
  au['rooms']['private_circulation']=copy.deepcopy(eu['rooms']['private_circulation'])
 for key in expected:
  if digest(actual[key])!=digest(expected[key]):raise ValueError('UNAUTHORIZED_BRANCH_ONLY_MODEL_DELTA_STOP:'+key)
 path_evidence=validate_current_paths(before_record,after_model)
 return {'path_evidence':path_evidence,'status':'PASS_EXACT_BRANCH_ONLY_ALLOWED_DELTA_PREFLIGHT','new_model_digest':digest(after_model),'proposal_digest':digest(proposal),'expected_projection_digest':digest(expected),'fixed_parent_record_file_sha256':'8807b7f2e8ba841d8e1a38ba6787f72161c9d04f64d69e71112859be92976ad9','scope':'Complete model comparison; only source-derived branch wall/private domain and independently recomputed floor/window/network/threshold/accounting fields may differ. Wrapper must verify fixed parent file SHA before propose. No entry/core changes in this stage.','fresh_required':True,'all_quality_unknown':True,'admission_allowed':False}
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());print(json.dumps(propose(r),indent=2))
