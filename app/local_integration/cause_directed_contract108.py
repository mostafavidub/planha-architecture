"""Cause-directed study contract. No provenance from a self-hash and no admission.
Actual original reports remain separate; scoped obstruction is not global infeasibility.
"""
import copy,inspect
from pathlib import Path
from fractions import Fraction as F
from same_version_front_rear_contract import digest
from front_rear_runtime_adapter import ROOT,ENGINE
from protected_repair_contract import protected
from source_fit_profile207 import source_check,installation_expectations,verify_installed_subset
from core_wall_audit118 import q,hit,covered,sweep
CAUSES={'BATH_APRON_DINING','KITCHEN_GUEST_MOTION'}
ROLES={'bed1','bed2','bath','kitchen','dining','sofa1_use','sofa2_use','chair1_use','chair2_use','entry_apron'}
def need(ok,code):
 if not ok:raise ValueError(code)
def dimensions(proposal):
 need(type(proposal)is dict and set(proposal['rectangles'])==ROLES,'RECTANGLE_ROLE_SET')
 out={}
 for k,r in proposal['rectangles'].items():
  need(type(r)is list and len(r)==4 and all(type(x)in(str,int,float)for x in r),'RECTANGLE_TYPED_COORDINATES')
  a,b,c,d=map(lambda v:F(str(v)),r);need(c>a and d>b,'RECTANGLE_POSITIVE')
  out[k]={'width':str(c-a),'height':str(d-b)}
 return out
def target_error_count(value,uid):
 if type(value)is dict:
  own=int(value.get('code')=='MODULE_APRON_NOT_REAL_PUBLIC_FLOOR'and value.get('unit')==uid and value.get('room')=='bath')
  return own+sum(target_error_count(v,uid)for v in value.values())
 if type(value)is list:return sum(target_error_count(v,uid)for v in value)
 return 0
def bath_geometry(aprons,dining,public):
 overlap=[(i,j)for i,a in enumerate(aprons)for j,b in enumerate(dining)if hit(q(a),q(b))]
 outside=[i for i,a in enumerate(aprons)if not covered(q(a),list(map(q,public)))]
 return {'overlap_piece_pairs':overlap,'outside_piece_indices':outside,'direct_geometry_failure':bool(overlap and outside)}
def diagnose(model,proposals,L,physical):
 from checker114 import check_module_placements
 from typed_public_access120 import parts
 from source_guest_route_evaluator import route_check,living_destination
 from guest_route_certificate_study import scene
 from public_program_audit118 import bind_operation_destination
 from guest_four_route_diagnostic import center
 source_check()
 for fn,path in ((check_module_placements,ENGINE/'checker114.py'),(parts,ENGINE/'typed_public_access120.py'),(route_check,ROOT/'app/local_integration/source_guest_route_evaluator.py'),(scene,ROOT/'app/local_integration/guest_route_certificate_study.py')):
  need(Path(inspect.getsourcefile(fn)).resolve()==path,'CAUSE_IMPORT_PATH')
 pin=digest([model,proposals,physical]);mh=digest(model)
 need(physical['model_hash']==mh,'CAUSE_PHYSICAL_MODEL')
 expected=installation_expectations(proposals,F(L))
 binding=verify_installed_subset(model,expected)
 need(binding['state']=='PASS_SOURCE_SUBSET_ONLY','CAUSE_SOURCE_SUBSET_BINDING')
 direct=check_module_placements(model);rows=[];selected=set()
 for u in model['units']:
  uid=u['id'];public=parts(model,u,uid+'.public_access')
  geometry=bath_geometry(model['module_aprons'][uid+'.bath'],u['rooms']['dining'],public)
  original_count=target_error_count(physical.get('errors',[]),uid);direct_count=target_error_count(direct['errors'],uid)
  established=geometry['direct_geometry_failure']and original_count>0 and direct_count>0
  rows.append({'unit':uid,'cause':'BATH_APRON_DINING','established':established,'original_target_error_count':original_count,'direct_target_error_count':direct_count,
   'geometry':geometry,'typed_public_digest':digest([[str(v)for v in r]for r in public]),'apron_digest':digest(model['module_aprons'][uid+'.bath'])})
  if established:selected.add('BATH_APRON_DINING')
  for old,new in (('guest_living','entry_living'),('guest_dining','entry_dining')):
   path=u.get('scenario_routes',{}).get(old)
   row={'unit':uid,'cause':'KITCHEN_GUEST_MOTION','route':old,'established':False,'state':'NO_STORED_ACTUAL_PATH_NO_CAUSE_CLAIM'}
   if path:
    s=scene(model,u,new);body=F(model['profile']['body_m']);need(body==F('.7'),'CAUSE_BODY')
    if old=='guest_living':end,_=living_destination(u)
    else:
     d=u['public_program']['destinations']['guest_dining'];end=center(u['activities'][d['activity_id']]);bind_operation_destination(u,d,tuple(map(F,end)))
    start=u['entry_point'];other=[r for r,label in zip(s['obstacles'],s['labels'])if not label.startswith('kitchen_motion:')]
    try:
     route_check(path,start,end,body,s['parts'],other)
     need(all(covered(z,list(map(q,s['owner'])))for z in sweep(path,body)),'CAUSE_OWNER')
     labels=sorted({label for band in sweep(path,body)for r,label in zip(s['obstacles'],s['labels'])if hit(band,q(r))})
     if not labels:
      route_check(path,start,end,body,s['parts'],s['obstacles']);row['state']='ACTUAL_STORED_PATH_CLEAR'
     else:need(all(v.startswith('kitchen_motion:')for v in labels),'CAUSE_NOT_EXCLUSIVE_SOURCE_MOTION')
     try:route_check(path,start,end,body,s['parts'],s['obstacles'])
     except ValueError as ex:
      if str(ex)=='ROUTE_OBSTACLE_COLLISION':row.update(established=True,state='DIRECT_STORED_ROUTE_MOTION_COLLISION',collision_labels=labels,path_digest=digest(path))
     if row['established']:selected.add('KITCHEN_GUEST_MOTION')
    except ValueError:row['state']='NO_SUPPORTED_EXCLUSIVE_MOTION_CAUSE'
   rows.append(row)
 need(digest([model,proposals,physical])==pin,'CAUSE_INPUT_MUTATION')
 return {'schema':'ACTUAL_CAUSE_SELECTION108_V1','model_digest':mh,'physical_digest':digest(physical),
  'selected_causes':sorted(selected),'rows':rows,'module_check_digest':digest(direct),'installed_binding_digest':digest(binding),
  'scope':'Bath requires original and direct code plus actual apron/dining/outside geometry. Motion requires stored actual route with source-bound endpoints and isolated motion collision; missing route alone is not evidence.',
  'accepted':False,'qualified':False}
def freeze(raw,packet,context,proposals,physical,diagnostic,sources,nonce):
 need(digest(proposals['A'])==digest(proposals['B']),'PAIR_EQUAL_PROPOSAL_SCOPE')
 need(context['construction_trace']['model_hash']==digest(packet['world_model']),'PARENT_CONTEXT')
 need(digest(context['construction_trace']['raw'])==digest(raw)and digest(context['construction_trace']['proposals'])==digest(proposals),'PARENT_RAW_PROPOSAL')
 need(diagnostic['model_digest']==digest(packet['world_model'])and diagnostic['physical_digest']==digest(physical),'PARENT_CAUSE_BINDING')
 actual=diagnose(packet['world_model'],proposals,raw['L'],physical)
 need(digest(actual)==digest(diagnostic),'PARENT_CAUSE_RECOMPUTE')
 out={'schema':'CAUSE_DIRECTED_FIXED_SIZE_CONTRACT108_V1','raw':copy.deepcopy(raw),'parent_model_digest':digest(packet['world_model']),
  'parent_packet_digest':digest(packet),'parent_context_digest':digest(context),'parent_physical_digest':digest(physical),
  'parent_proposal_digest':digest(proposals),'cause_digest':digest(actual),'enabled_causes':actual['selected_causes'],
  'rectangle_dimensions':dimensions(proposals['A']),'bed_door_sides':copy.deepcopy(proposals['A']['bed_door_sides']),
  'protected':protected(packet),'source_snapshot':copy.deepcopy(sources),'run_nonce':nonce,
  'movement_scope':'Positions and routes may change; all proposal rectangle dimensions and bedroom door sides fixed. Cause-directed resynthesis, not minimal geometric repair.',
  'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
 validate_parent_contract(out,out['enabled_causes'])
 return out
def validate_parent_contract(contract,enabled):
 need(type(contract)is dict and contract.get('schema')=='CAUSE_DIRECTED_FIXED_SIZE_CONTRACT108_V1','PARENT_CONTRACT_SCHEMA')
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
   ok=(not c['geometry']['overlap_piece_pairs']and not c['geometry']['outside_piece_indices']and c['direct_target_error_count']==0 and c['original_target_error_count']==0)if p['cause']=='BATH_APRON_DINING'else c['state']=='ACTUAL_STORED_PATH_CLEAR'
  rows.append({'unit':p['unit'],'cause':p['cause'],'route':p.get('route'),'resolved':ok})
 return {'schema':'CAUSE_RESOLUTION108_V1','parent_model_digest':parent['model_digest'],'child_model_digest':child['model_digest'],
  'rows':rows,'all_target_causes_resolved':all(r['resolved']for r in rows)and bool(rows),'new_supported_causes':child['selected_causes'],'authority':False}

def validate_current_report(report,model_digest):
 need(type(report)is dict and report.get('state')in('PASS','FAIL','UNKNOWN','NOT_EVALUATED'),'CURRENT_STATE_NOT_ALLOWED')
 need(report.get('model_digest')==model_digest,'CURRENT_REPORT_MODEL')
 need(all(report.get(k)is False for k in('accepted','qualified','display_allowed','delivery_allowed')),'CURRENT_REPORT_AUTHORITY')
