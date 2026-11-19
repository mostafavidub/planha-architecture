"""Source planned-witness cause contract, resumed R4-1.08.
Not a claim of global route infeasibility, natural failure reproduction or admission.
"""
import copy,inspect
from pathlib import Path
from fractions import Fraction as F
from same_version_front_rear_contract import digest
from front_rear_runtime_adapter import ROOT,ENGINE
from protected_repair_contract import protected
from cause_directed_contract108 import need,dimensions,validate_parent_contract,CAUSES,ROLES
from core_wall_audit118 import q,hit,covered,sweep
CAUSES=CAUSES|{'PLANNED_GUEST_DINING_MOTION'}

def missing_count(value,uid):
 if type(value)is dict:
  own=0
  if value.get('code')=='MISSING_REQUIRED_ACTIVITY_ROUTES':
   own=sum(type(v)is dict and v.get('unit')==uid and v.get('route')=='guest_dining'for v in value.get('failures',[]))
  return own+sum(missing_count(v,uid)for v in value.values())
 if type(value)is list:return sum(missing_count(v,uid)for v in value)
 return 0

def world_path(proposal,uid,L):
 need(uid in('A','B'),'PLANNED_UNIT')
 path=proposal.get('network_paths',{}).get('dining_east')
 need(type(path)is list and len(path)>=2,'PLANNED_PATH_MISSING')
 out=[]
 for p in path:
  need(type(p)is list and len(p)==2 and all(type(v)in(str,int,float)for v in p),'PLANNED_POINT_TYPE')
  a,b=(F(str(v))for v in p);out.append([str(a),str(b if uid=='A'else F(L)-b)])
 return out

def isolated_motion(path,start,end,scene):
 from source_guest_route_evaluator import route_check
 body=F(scene['body']);need(body==F('.7'),'PLANNED_BODY')
 need(len(scene['obstacles'])==len(scene['labels']),'PLANNED_LABEL_COUNT')
 other=[r for r,label in zip(scene['obstacles'],scene['labels'])if not label.startswith('kitchen_motion:')]
 route_check(path,start,end,body,scene['parts'],other)
 need(all(covered(z,list(map(q,scene['owner'])))for z in sweep(path,body)),'PLANNED_OWNER')
 labels=sorted({label for band in sweep(path,body)for r,label in zip(scene['obstacles'],scene['labels'])if hit(band,q(r))})
 need(bool(labels)and all(label.startswith('kitchen_motion:')for label in labels),'PLANNED_NOT_EXCLUSIVE_MOTION')
 try:route_check(path,start,end,body,scene['parts'],scene['obstacles'])
 except ValueError as ex:need(str(ex)=='ROUTE_OBSTACLE_COLLISION','PLANNED_DIFFERENT_REJECTION')
 else:raise ValueError('PLANNED_COLLISION_NOT_REJECTED')
 return labels


def original_guest_scene(model,u):
 """Exact public_witness118 guest base; ownership[0] box, whole kitchen exclusion.
This is not the newer typed-floor scene: both profiles are tested separately.
"""
 uid=u['id']
 obstacles=list(model['walls'].values())+[o['open_panel']for o in model['operations'].get('doors',[])]
 labels=['wall:'+k for k in model['walls']]+['open_panel:'+str(i)for i,_ in enumerate(model['operations'].get('doors',[]))]
 obstacles+=list(u['fixtures'].values());labels+=['fixture:'+k for k in u['fixtures']]
 for role,rects in u['rooms'].items():
  if role.startswith('bed')or role in('bath','private_circulation'):
   obstacles+=rects;labels+=['private:'+role+':'+str(i)for i,_ in enumerate(rects)]
 for o in model['operations']['dining_chairs']:
  if o['unit']!=uid:continue
  a,b=q(o['closed_rect']),q(o['open_rect'])
  obstacles += [[str(min(a[0],b[0])),str(min(a[1],b[1])),str(max(a[2],b[2])),str(max(a[3],b[3]))],o['occupied_body']]
  labels+=['chair_swept:'+o['fixture_id'],'chair_occupied:'+o['fixture_id']]
 obstacles+=u['rooms']['kitchen'];labels+=['whole_kitchen:'+str(i)for i,_ in enumerate(u['rooms']['kitchen'])]
 for op in model['operations']['kitchen']:
  if op['unit']==uid:
   obstacles+=op['motion_envelopes'];labels+=['kitchen_motion:'+str(i)for i,_ in enumerate(op['motion_envelopes'])]
 return {'body':model['profile']['body_m'],'parts':[u['ownership'][0]],'owner':[u['ownership'][0]],'obstacles':obstacles,'labels':labels}

def diagnose(model,proposals,L,physical,context):
 from cause_directed_contract108 import diagnose as original
 from guest_route_certificate_study import scene
 from public_program_audit118 import bind_operation_destination
 from guest_four_route_diagnostic import center
 from source_guest_route_evaluator import route_check
 for fn,path in ((original,ROOT/'app/local_integration/cause_directed_contract108.py'),(scene,ROOT/'app/local_integration/guest_route_certificate_study.py'),(route_check,ROOT/'app/local_integration/source_guest_route_evaluator.py'),(bind_operation_destination,ENGINE/'public_program_audit118.py')):
  need(Path(inspect.getsourcefile(fn)).resolve()==path,'PLANNED_IMPORT_PATH')
 pin=digest([model,proposals,physical,context])
 trace=context['construction_trace']
 need(trace['model_hash']==digest(model)and digest(trace['proposals'])==digest(proposals),'PLANNED_CONTEXT_BINDING')
 need(F(trace['raw']['L'])==F(L)and digest(model['inputs'])==digest([trace['raw']['W'],trace['raw']['L'],2]),'PLANNED_INPUT_FRAME')
 out=original(model,proposals,L,physical)
 out.update(schema='SOURCE_PLANNED_CAUSE_SELECTION108_V2',context_digest=digest(context),proposal_digest=digest(proposals),
  scope='Stored-path causes unchanged. Missing guest_dining plus source planned witness exclusive motion collision is a planner-witness defect, not the unique cause of route search failure or global infeasibility.')
 for u in model['units']:
  uid=u['id'];row={'unit':uid,'cause':'PLANNED_GUEST_DINING_MOTION','route':'guest_dining','established':False,'state':'NOT_ESTABLISHED'}
  out['rows'].append(row)
  count=missing_count(physical.get('errors',[]),uid);row['original_missing_route_count']=count
  if u.get('scenario_routes',{}).get('guest_dining'):
   if True:
    from guest_four_route_diagnostic import center
    end=center(u['activities'][u['public_program']['destinations']['guest_dining']['activity_id']])
    os=original_guest_scene(model,u)
    try:route_check(u['scenario_routes']['guest_dining'],u['entry_point'],end,F('.7'),os['parts'],os['obstacles'])
    except ValueError:row['state']='ACTUAL_STORED_PATH_NOT_CLEAR_IN_ORIGINAL_PROFILE'
    else:row['state']='ACTUAL_STORED_PATH_CLEAR_ORIGINAL_PROFILE'
   continue
  row['cause']='PLANNED_GUEST_DINING_MOTION'
  row['planned_witness_scope']='SOURCE_PROPOSAL_NETWORK_NOT_STORED_ACTUAL_ROUTE'
  if count==0:row['state']='NO_ORIGINAL_MISSING_ROUTE_CODE';continue
  failures=[f for f in model.get('route_failures',[])if f.get('unit')==uid and f.get('route')=='guest_dining'and f.get('profile')=='public_all_seat_motion_occupied_and_kitchen_exclusion']
  if not failures:row['state']='NO_SOURCE_ROUTE_FAILURE_PROFILE';continue
  path=world_path(proposals[uid],uid,L);s=original_guest_scene(model,u)
  d=u['public_program']['destinations']['guest_dining']
  need(d['activity_id']=='dining_east'and d['fixture_id']=='dining_chair_east','PLANNED_DESTINATION_SOURCE')
  end=center(u['activities'][d['activity_id']]);bind_operation_destination(u,d,tuple(map(F,end)))
  row.update(path_digest=digest(path),scene_digest=digest(s),proposal_digest=digest(proposals[uid]),endpoint_digest=digest([u['entry_point'],end]),
   transform={'matrix':[[1,0],[0,1 if uid=='A'else-1]],'translation':['0','0'if uid=='A'else str(F(L))]})
  try:
   labels=isolated_motion(path,u['entry_point'],end,s)
   row['original_profile_exclusive_motion_verified']=True
   row.update(established=True,state='DIRECT_PLANNED_WITNESS_MOTION_COLLISION',collision_labels=labels)
  except ValueError as ex:
   allowed={'ROUTE_ENDPOINT','ROUTE_DOMAIN_COVERAGE','ROUTE_OBSTACLE_COLLISION','PLANNED_OWNER','PLANNED_NOT_EXCLUSIVE_MOTION','PLANNED_COLLISION_NOT_REJECTED','NON_ORTHOGONAL_SEGMENT','EMPTY_SWEEPS'}
   row.update(state='NO_SUPPORTED_EXCLUSIVE_PLANNED_MOTION',rejection_code=str(ex)if str(ex)in allowed else'OTHER_GEOMETRY_REJECTION')
 out['selected_causes']=sorted({r['cause']for r in out['rows']if r['established']})
 need(digest([model,proposals,physical,context])==pin,'PLANNED_INPUT_MUTATION')
 return out
def freeze(raw,packet,context,proposals,physical,diagnostic,sources,nonce):
 need(digest(proposals['A'])==digest(proposals['B']),'PAIR_EQUAL_PROPOSAL_SCOPE')
 need(context['construction_trace']['model_hash']==digest(packet['world_model']),'PARENT_CONTEXT')
 need(digest(context['construction_trace']['raw'])==digest(raw)and digest(context['construction_trace']['proposals'])==digest(proposals),'PARENT_RAW_PROPOSAL')
 need(diagnostic['model_digest']==digest(packet['world_model'])and diagnostic['physical_digest']==digest(physical),'PARENT_CAUSE_BINDING')
 actual=diagnose(packet['world_model'],proposals,raw['L'],physical,context)
 need(digest(actual)==digest(diagnostic),'PARENT_CAUSE_RECOMPUTE')
 out={'schema':'PLANNED_WITNESS_FIXED_SIZE_CONTRACT108_V2','raw':copy.deepcopy(raw),'parent_model_digest':digest(packet['world_model']),
  'parent_packet_digest':digest(packet),'parent_context_digest':digest(context),'parent_physical_digest':digest(physical),
  'parent_proposal_digest':digest(proposals),'cause_digest':digest(actual),'enabled_causes':actual['selected_causes'],
  'rectangle_dimensions':dimensions(proposals['A']),'bed_door_sides':copy.deepcopy(proposals['A']['bed_door_sides']),
  'protected':protected(packet),'source_snapshot':copy.deepcopy(sources),'run_nonce':nonce,
  'diagnostic_scope':'SOURCE_PLANNED_WITNESS_NOT_UNIQUE_ROUTE_FAILURE_CAUSE',
  'movement_scope':'Positions and routes may change; all proposal rectangle dimensions and bedroom door sides fixed. Cause-directed resynthesis, not minimal geometric repair.',
  'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
 validate_parent_contract(out,out['enabled_causes'])
 return out
def validate_parent_contract(contract,enabled):
 need(type(contract)is dict and contract.get('schema')=='PLANNED_WITNESS_FIXED_SIZE_CONTRACT108_V2','PARENT_CONTRACT_SCHEMA')
 need(type(enabled)is list and enabled==sorted(set(enabled))and bool(enabled)and set(enabled)<=CAUSES,'SUPPORTED_CAUSE_REQUIRED')
 need(digest(contract['enabled_causes'])==digest(enabled),'ENABLED_CAUSE_BINDING')
 need(set(contract['rectangle_dimensions'])==ROLES,'PARENT_DIMENSION_ROLE_SET')
 for v in contract['rectangle_dimensions'].values():
  need(type(v)is dict and set(v)=={'width','height'}and all(type(x)is str and F(x)>0 for x in v.values()),'PARENT_DIMENSION_VALUE')
 need(type(contract['bed_door_sides'])is dict and set(contract['bed_door_sides'])=={'bed1','bed2'}and all(type(v)is str and v in('left','right')for v in contract['bed_door_sides'].values()),'PARENT_DOOR_SIDES')
 need(all(contract.get(k)is False for k in('accepted','qualified','display_allowed','delivery_allowed')),'PARENT_AUTHORITY')
def bind_parent(contract,raw,packet,context,proposals,physical,diagnostic,sources,nonce):
 need(digest(contract)==digest(freeze(raw,packet,context,proposals,physical,diagnostic,sources,nonce)),'PARENT_CONTRACT_BINDING')
def check_child(contract,packet,proposals):
 validate_parent_contract(contract,contract['enabled_causes'])
 need(digest(protected(packet))==digest(contract['protected']),'CHILD_PROTECTED_STATE_CHANGED')
 for p in proposals.values():
  need(digest(dimensions(p))==digest(contract['rectangle_dimensions']),'CHILD_RECTANGLE_DIMENSIONS_CHANGED')
  need(digest(p['bed_door_sides'])==digest(contract['bed_door_sides']),'CHILD_BED_DOOR_SIDE_CHANGED')
 need(digest(packet['world_model'])!=contract['parent_model_digest'],'CHILD_NOT_DISTINCT')
 return {'protected_verified':True,'parent_model_digest':contract['parent_model_digest'],'child_model_digest':digest(packet['world_model']),'contract_digest':digest(contract),'authority':False}

def resolution(parent,child):
 need(parent['selected_causes'],'NO_TARGET_CAUSE')
 rows=[]
 for p in parent['rows']:
  if not p['established']:continue
  matches=[c for c in child['rows']if c['unit']==p['unit']and c['cause']==p['cause']and c.get('route')==p.get('route')]
  ok=False
  if len(matches)==1:
   c=matches[0]
   ok=(not c['geometry']['overlap_piece_pairs']and not c['geometry']['outside_piece_indices']and c['direct_target_error_count']==0 and c['original_target_error_count']==0)if p['cause']=='BATH_APRON_DINING'else (c['state']=='ACTUAL_STORED_PATH_CLEAR_ORIGINAL_PROFILE'and c.get('original_missing_route_count')==0)if p['cause']=='PLANNED_GUEST_DINING_MOTION'else c['state']=='ACTUAL_STORED_PATH_CLEAR'
  rows.append({'unit':p['unit'],'cause':p['cause'],'route':p.get('route'),'resolved':ok})
 return {'schema':'PLANNED_WITNESS_RESOLUTION108_V2','parent_model_digest':parent['model_digest'],'child_model_digest':child['model_digest'],
  'rows':rows,'all_target_causes_resolved':all(r['resolved']for r in rows)and bool(rows),'new_supported_causes':child['selected_causes'],'authority':False}

def validate_current_report(report,model_digest):
 need(type(report)is dict and report.get('state')in('PASS','FAIL','UNKNOWN','NOT_EVALUATED'),'CURRENT_STATE_NOT_ALLOWED')
 need(report.get('model_digest')==model_digest,'CURRENT_REPORT_MODEL')
 need(all(report.get(k)is False for k in('accepted','qualified','display_allowed','delivery_allowed')),'CURRENT_REPORT_AUTHORITY')

def candidate_contract(contract):
 """Explicit operator adapter; evidence cause is not renamed into a stored-route cause."""
 validate_parent_contract(contract,contract['enabled_causes'])
 need('PLANNED_GUEST_DINING_MOTION'in contract['enabled_causes'],'PLANNED_CAUSE_REQUIRED')
 translated=copy.deepcopy(contract)
 translated['schema']='CAUSE_DIRECTED_FIXED_SIZE_CONTRACT108_V1'
 translated['enabled_causes']=sorted({'KITCHEN_GUEST_MOTION'if c=='PLANNED_GUEST_DINING_MOTION'else c for c in contract['enabled_causes']})
 translated['operator_adapter']={'schema':'PLANNED_TO_SOURCE_MOTION_RESERVATION108_V1','source_contract_digest':digest(contract),
  'mapping':{'PLANNED_GUEST_DINING_MOTION':'KITCHEN_GUEST_MOTION'},'scope':'Same source motion reservation operator; does not relabel diagnostic evidence as stored-path failure.'}
 from cause_directed_contract108 import validate_parent_contract as old_validate
 old_validate(translated,translated['enabled_causes'])
 return translated
