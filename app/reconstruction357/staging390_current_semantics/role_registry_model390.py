"""Model-specific SOURCE_BALANCED365 role registry, using independent fresh359 gate.
Previous SOURCE358 registry/evidence remain unchanged. No parent admission.
"""
import json
from pathlib import Path
from fractions import Fraction as F
import common
from common import digest,rows
from modules_spatial import rect,union_area,difference,intersection
from guest_closure import transformed_rect
ROOT=Path(__file__).resolve().parents[1]
DAG={
 'SOURCE_GATE':[], 'PARTITION':['SOURCE_GATE'], 'SOURCE_ROOM_USE':['SOURCE_GATE'],
 'PUBLIC_SUPPORT':['SOURCE_ROOM_USE','SOURCE_GATE'], 'ENTRY_CIRCULATION':['SOURCE_GATE'],
 'PRIVATE_CIRCULATION':['SOURCE_GATE'], 'SERVICE_CIRCULATION':['SOURCE_ROOM_USE'],
 'COMMON_ROLE':['SOURCE_GATE'], 'WALL_PURPOSE':['SOURCE_ROOM_USE','PRIVATE_CIRCULATION'],
 'Q04_COMPARISON':['ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE'],
 'Q11_WHOLE_ROLE':['PARTITION','SOURCE_ROOM_USE','PUBLIC_SUPPORT','ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON'],
 'Q05_PRIVACY':['SOURCE_GATE','WALL_PURPOSE','Q11_WHOLE_ROLE'],
 'Q12_PER_UNIT':['SOURCE_ROOM_USE','PUBLIC_SUPPORT','ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE','WALL_PURPOSE'],
 'Q14_SELECTION_SET':['SOURCE_GATE']}
def ordered_dag(dag=DAG):
 out=[];pending=set(dag)
 while pending:
  ready=sorted(k for k in pending if all(d in out for d in dag[k]))
  if not ready:raise ValueError('DEPENDENCY_CYCLE_OR_UNKNOWN_NODE')
  out+=ready;pending-=set(ready)
 return out

def room_inventory(model,req):
 out=[]
 for u in model['units']:
  floor=next(r['regions']for r in model['spatial_accounting']['plot_partition']if r['role']=='unit_'+u['id']+'_floor');named=[rect(q)for rs in u['rooms'].values()for q in rs]
  unassigned=difference(list(map(rect,floor)),named);outside=difference(named,list(map(rect,floor)))
  if unassigned or outside:raise ValueError('NAMED_ROLE_FLOOR_PARTITION_MISMATCH')
  for p in model['module_placements']:
   if p['unit_id']!=u['id']:continue
   source=p['module'];room=p['room_id'];schema=source['schema']
   if schema not in ('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118','BATHROOM_MODULE117','KITCHEN_MODULE117'):raise ValueError('UNSUPPORTED_SOURCE_ROOM_SCHEMA')
   if digest(source)!=p['module_hash']:raise ValueError('SOURCE_ROOM_MODULE_HASH')
   expected=[transformed_rect(q,p['transform'])for k,rs in source['unit']['rooms'].items()if k!='public_access'for q in rs];actual=list(map(rect,u['rooms'][room]))
   if difference(expected,actual)or difference(actual,expected):raise ValueError('WHOLE_SOURCE_ROOM_REGION_BINDING')
   ids=[p['id_map'][k]for k in source['unit']['fixtures']];activities=[p['id_map'][k]for k in source['unit']['activities']]
   for k,q in source['unit']['fixtures'].items():
    if transformed_rect(q,p['transform'])!=rect(u['fixtures'][p['id_map'][k]]):raise ValueError('SOURCE_ROOM_FIXTURE_BINDING')
   for k,q in source['unit']['activities'].items():
    if transformed_rect(q,p['transform'])!=rect(u['activities'][p['id_map'][k]]):raise ValueError('SOURCE_ROOM_ACTIVITY_BINDING')
   deps=['fixture_inventory_use','body_route_sweeps','door_operation']+(['bath_service_operation']if room=='bath'else['kitchen_essential_operation']if room=='kitchen'else['closet_operation'])
   if any(req[d]['status']!='PASS_LIMITED'for d in deps):raise ValueError('SOURCE_ROOM_FUNCTION_UNVERIFIED')
   out.append({'unit':u['id'],'role':room,'verdict':'PASS_SCOPED_SOURCE_WHOLE_ROOM_ROLE','regions':u['rooms'][room],'area_m2':str(union_area(actual)),'source_module_hash':p['module_hash'],'transform':p['transform'],'actual_fixture_ids':ids,'actual_activity_ids':activities,'source_row_digests':{d:digest(req[d])for d in deps},'scope':'Whole exact source-defined operational room, including source margins; no requirement to tile room floor with fixture footprints. Independent exclusive service-circulation accounting remains a separate dependency.'})
  p=u['dining_module_placement'];source=p['module']
  if digest(source)!=p['module_hash']:raise ValueError('DINING_MODULE_HASH')
  expected=[transformed_rect(['0','0',source['width'],source['depth']],p['transform'])];actual=list(map(rect,u['rooms']['dining']))
  if difference(expected,actual)or difference(actual,expected):raise ValueError('WHOLE_DINING_REGION_BINDING')
  for k,q in source['fixtures'].items():
   if transformed_rect(q,p['transform'])!=rect(u['fixtures'][p['id_map'][k]]):raise ValueError('DINING_FIXTURE_BINDING')
  deps=['fixture_inventory_use','chair_capacity_movement','guest_dining_route','serving_route']
  if any(req[d]['status']!='PASS_LIMITED'for d in deps):raise ValueError('DINING_FUNCTION_UNVERIFIED')
  out.append({'unit':u['id'],'role':'dining','verdict':'PASS_SCOPED_SOURCE_WHOLE_ROOM_ROLE','regions':u['rooms']['dining'],'area_m2':str(union_area(actual)),'source_module_hash':p['module_hash'],'source_row_digests':{d:digest(req[d])for d in deps},'scope':'Source full dining envelope including required chair operation and transfer/access margins, not fixture tiling.'})
 return out

def evaluate(record,review,source_profile='SOURCE_BALANCED365'):
 if source_profile!='SOURCE_BALANCED365':raise ValueError('MODEL_SPECIFIC_SOURCE_GATE_NOT_REGISTERED_NO_358_REUSE')
 from groups390 import build
 from reassess_spatial390 import evaluate as spatial
 from circulation_role390 import evaluate as circulation
 before=digest([record,review]);views=build(record,review,source_profile='SOURCE_BALANCED365');model=record['candidate']['model'];old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source365.json';req=rows(model,review['raw_report']);rooms=room_inventory(model,req)
 finally:common.REGISTRY_NAME=old
 sp=spatial(record,review);ci=circulation(record,review);mh=digest(model)
 if any(x['model_hash']!=mh for x in (sp,ci)):raise ValueError('DEPENDENT_MODEL_BINDING')
 nodes={
  'SOURCE_GATE':{'status':'PASS_REGISTERED_MODEL_SPECIFIC_ARTIFACT_GATE','evidence':{'record_digest':digest(record),'review_digest':digest(review),'view_digest':digest(views)}},
  'PARTITION':{'status':'PASS_EXACT_GEOMETRIC_PARTITION_NOT_ROLE_ACCEPTANCE','evidence':{'source_row_digest':digest(req['partition_ledger']),'named_floor_unassigned_m2':'0','role_inventory':[(u['id'],sorted(u['rooms']))for u in model['units']]}},
  'SOURCE_ROOM_USE':{'status':'PASS_SCOPED_WHOLE_SOURCE_ROOM_ROLES','evidence':rooms},
  'PUBLIC_SUPPORT':{'status':'PASS_SCOPED_SOURCE_SUPPORT_EXTENT'if sp['support'].get('status')=='MEASURED_CURRENT_SOURCE_SUPPORT_NOT_FINAL_ROLE_APPROVAL'and all(F(r['unresolved_area_m2'])==0 for r in sp['support']['rows'])else'UNKNOWN','evidence':sp['support'],'scope':'Source-required sitting/use and reachable support plus actual operations/reservations. Not exclusive-circulation necessity.'},
  'ENTRY_CIRCULATION':{'status':'PASS_SCOPED_REQUIRED_TARGET_COMPONENTS'if all(c['verdict']=='PASS_EXACT_REQUIRED_PATH_USE_COMPONENT'for u in ci['units']for c in u['entry_circulation_components'])else'UNKNOWN','evidence':{u['unit']:u['entry_circulation_components']for u in ci['units']}},
  'PRIVATE_CIRCULATION':{'status':'PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE'if all(u['intrinsic_private_role_status']=='PASS_SCOPED_SOURCE_WHOLE_CONNECTOR_ROLE'for u in ci['units'])else'UNKNOWN_SOURCE_PRIVATE_COMPONENT_ROLE','evidence':{u['unit']:{k:u[k]for k in('private_circulation_components','private_margin_operationalization','untargeted_terminal_extensions','source_connector_margin_proof','intrinsic_private_role_status')}for u in ci['units']}},
  'SERVICE_CIRCULATION':{'status':'UNKNOWN_EXCLUSIVE_SERVICE_ROLE_ACCOUNTING','evidence':{u['unit']:u['service_inventory']for u in ci['units']}},
  'COMMON_ROLE':{'status':'UNKNOWN_COMMON_ROLE_HELPER_APPROVAL_AND_FINAL_CLOSURE_PENDING','evidence':{'core_concept_row_digest':digest(req['core_concept']),'current_fresh_core_concept_status':req['core_concept']['status'],'current_model_common_routes':model['common_routes'],'current_model_lobby_regions':model['common_spaces']['lobby'],'current_model_entry_operations_digest':digest([o for o in model['operations']['doors'] if o['opening_id'] in ('A.entry','B.entry')]),'scope':'Conceptual core route/access exists; no inference that every lobby region has a proven arrival/staging role.'}},
  'WALL_PURPOSE':{'status':'UNKNOWN_HALL_Q04_DEPENDENCY','evidence':sp['wall_purpose']},
  'Q04_COMPARISON':{'status':'UNKNOWN_ELIGIBLE_CLOSED_FINITE_COMPARISON_NOT_REGISTERED','missing':['Actual evaluated alternatives or source-supported unavailability with protected-use eligibility; no parent-PASS circular filter']},
  'Q11_WHOLE_ROLE':{'status':'UNKNOWN_REQUIRED_DEPENDENCIES_UNCLOSED'},
  'Q05_PRIVACY':{'status':'UNKNOWN_WALL_PURPOSE_FINAL_AND_WHOLE_ROLE_UNCLOSED','evidence':{'same_model_privacy_row_digest':digest(req['privacy_scenarios']),'scope':'Source privacy rays are separate evidence; Q11 and Q04 are not assumed from zero visibility errors.'}}}
 perunit=[]
 for u in model['units']:
  uid=u['id'];cr=next(r for r in ci['units']if r['unit']==uid);sr=next(r for r in sp['support']['rows']if r['unit']==uid)
  pending=['PRIVATE_CIRCULATION_VALID_MARGIN_SCOPE','Q04_CLOSED_FINITE_ELIGIBLE_COMPARISON','EXCLUSIVE_SERVICE_CIRCULATION_ACCOUNTING','WHOLE_COMMON_LOBBY_ROLE','HALL_WALL_PURPOSE_Q04_DEPENDENCY']
  if cr['intrinsic_private_role_status']=='PASS_SCOPED_SOURCE_WHOLE_CONNECTOR_ROLE':pending.remove('PRIVATE_CIRCULATION_VALID_MARGIN_SCOPE')
  if cr['untargeted_terminal_extensions']:pending.append('UNTARGETED_TERMINAL_EXTENSIONS_REQUIRE_PURPOSE')
  if F(sr['unresolved_area_m2'])>0:pending.append('PUBLIC_FUNCTIONAL_EXTENT_GAP')
  perunit.append({'unit':uid,'whole_unit_verdict':'UNKNOWN','source_room_roles':[r for r in rooms if r['unit']==uid],'capacity_use_access_source_rows':{k:digest(req[k])for k in ('fixture_inventory_use','body_route_sweeps','chair_capacity_movement','bath_service_operation','kitchen_essential_operation','guest_living_route','guest_dining_route','serving_route')},'current_source_public_extent_unresolved_m2':sr['unresolved_area_m2'],'entry_component_targets':[c['required_targets_served']for c in cr['entry_circulation_components']],'exact_pending':pending,'not_a_parent_acceptance_filter':True})
 nodes['Q12_PER_UNIT']={'status':'UNKNOWN_PER_UNIT_ROLE_DEPENDENCIES','evidence':perunit,'scope':'Direct same-model per-unit source capacity/use/access evidence and role gaps; no all12-PASS prerequisite and no dependency on Q12 verdict.'}
 nodes['Q14_SELECTION_SET']={'status':'UNKNOWN_SELECTION_SET_NOT_SUPPLIED','evidence':{'raw_requested_count':record['candidate']['request']['requested_count'],'actual_supplied_candidate_count':1,'actual_selection_set':None,'rule':'Single internal candidate is not a demonstrated final selection set. Requested count is not generated-set evidence. No N_A inferred from absent set.'}}
 from common_role_closure390 import evaluate as common_evaluate
 common_proof=common_evaluate(record,review)
 if common_proof['model_hash']!=mh or common_proof['raw_review_digest']!=digest(review)or common_proof['verdict']!='PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE':raise ValueError('COMMON365_SOURCE_CLOSURE_BINDING')
 nodes['COMMON_ROLE']={'status':common_proof['verdict'],'evidence':common_proof}
 for unit in perunit:
  unit['exact_pending'].remove('WHOLE_COMMON_LOBBY_ROLE')
 order=ordered_dag()
 for name in order:
  nodes[name]['depends_on']=DAG[name];nodes[name]['blocking_dependencies']=[d for d in DAG[name]if nodes[d]['status'].startswith('UNKNOWN')]
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'schema':'ROLE_REGISTRY_BALANCED365_CODE_ON_MODEL_SPECIFIC_EVIDENCE','source_profile':source_profile,'model_hash':mh,'record_digest':digest(record),'review_digest':digest(review),'topological_order':order,'nodes':nodes,'fresh_execution':False,'admission_allowed':False,'whole_parent_complete':False}
