"""Model-specific SOURCE_JOINT367 role registry, using its own registered JOINT367 fresh gate.
Previous registries and evidence remain unchanged. No parent admission.
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

def selection_scope(record,review,req):
 import hashlib
 mh=digest(record['candidate']['model']);row=req['geometric_diversity']
 registry=json.loads((Path(__file__).parent/'method_registry_source367.json').read_text())
 sources={}
 for name,selector in [('checker114.py','_evaluate_impl: context stage concept_internal, batch_models=[model]'),('rule_contract118.py','evaluate_rule_contract: multiple_candidates, batch model membership and len(batch)>1')]:
  key='staging367_joint_source_validation_attempt2/runtime/'+name;path=ROOT/key;sha=hashlib.sha256(path.read_bytes()).hexdigest()
  if registry['sources'].get(key)!=sha:raise ValueError('SELECTION_CALLBACK_SOURCE_CHANGED')
  sources[key]={'sha256':sha,'selector':selector}
 singleton=(row.get('status')=='NOT_APPLICABLE_TO_STAGE_OR_MODEL' and row.get('applicability')=={'condition':'multiple_candidates','batch_model_hashes':[mh]})
 return {'status':'UNKNOWN_SELECTION_SET_NOT_SUPPLIED','evidence':{'internal_pair_test':{'status':'NOT_APPLICABLE_INTERNAL_SINGLETON_REVIEW'if singleton else'UNKNOWN_BOUND_SINGLETON_APPLICABILITY_NOT_ESTABLISHED','source_bound_requirement_row':row,'row_digest':digest(row),'model_hash':mh,'record_digest':digest(record),'fresh_result_digest':digest(review),'source_callbacks':sources,'scope':'Only this registered internal review batch; not requested selection-set fulfillment or general Q14 exemption.'},'raw_requested_count':record['candidate']['request']['requested_count'],'actual_supplied_candidate_count':1,'actual_selection_set':None,'selected_output_set_fulfillment':'NOT_PROVEN','delivery_allowed':False,'rule':'Internal single-model callback applicability is source-bound; requested_count 2 remains unfulfilled/unproven, not inferred completed from pair-test N_A.'}}

def evaluate(record,review,source_profile='SOURCE_JOINT367'):
 if source_profile!='SOURCE_JOINT367':raise ValueError('MODEL_SPECIFIC_SOURCE_GATE_NOT_REGISTERED_NO_358_REUSE')
 from group_readsets367 import build
 from reassess_spatial_joint367 import evaluate as spatial
 from private_role_joint367 import evaluate as circulation
 before=digest([record,review]);views=build(record,review,source_profile='SOURCE_JOINT367');model=record['candidate']['model'];old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source367.json';req=rows(model,review['raw_report']);rooms=room_inventory(model,req)
 finally:common.REGISTRY_NAME=old
 sp=spatial(record,review);ci=circulation(record,review);mh=digest(model)
 if any(x['model_hash']!=mh for x in (sp,ci)):raise ValueError('DEPENDENT_MODEL_BINDING')
 nodes={
  'SOURCE_GATE':{'status':'PASS_REGISTERED_MODEL_SPECIFIC_ARTIFACT_GATE','evidence':{'record_digest':digest(record),'review_digest':digest(review),'view_digest':digest(views)}},
  'PARTITION':{'status':'PASS_EXACT_GEOMETRIC_PARTITION_NOT_ROLE_ACCEPTANCE','evidence':{'source_row_digest':digest(req['partition_ledger']),'named_floor_unassigned_m2':'0','role_inventory':[(u['id'],sorted(u['rooms']))for u in model['units']]}},
  'SOURCE_ROOM_USE':{'status':'PASS_SCOPED_WHOLE_SOURCE_ROOM_ROLES','evidence':rooms},
  'PUBLIC_SUPPORT':{'status':'PASS_SCOPED_SOURCE_SUPPORT_EXTENT'if sp['support'].get('status')=='MEASURED_CURRENT_SOURCE_SUPPORT_NOT_FINAL_ROLE_APPROVAL'and all(F(r['unresolved_area_m2'])==0 for r in sp['support']['rows'])else'UNKNOWN','evidence':sp['support'],'scope':'Source-required sitting/use and reachable support plus actual operations/reservations. Not exclusive-circulation necessity.'},
  'ENTRY_CIRCULATION':{'status':'PASS_SCOPED_REQUIRED_TARGET_COMPONENTS'if all(c['verdict']=='PASS_EXACT_REQUIRED_PATH_USE_COMPONENT'for u in ci['units']for c in u['entry_circulation_components'])else'UNKNOWN','evidence':{u['unit']:u['entry_circulation_components']for u in ci['units']}},
  'PRIVATE_CIRCULATION':{'status':'PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE'if all(u['intrinsic_private_role_status']=='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE'for u in ci['units'])else'UNKNOWN_SOURCE_PRIVATE_COMPONENT_ROLE','evidence':{u['unit']:{k:u[k]for k in('private_circulation_components','private_margin_operationalization','untargeted_terminal_extensions','source_connector_margin_proof','intrinsic_private_role_status')}for u in ci['units']}},
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
  if cr['intrinsic_private_role_status']=='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE':pending.remove('PRIVATE_CIRCULATION_VALID_MARGIN_SCOPE')
  if cr['untargeted_terminal_extensions']:pending.append('UNTARGETED_TERMINAL_EXTENSIONS_REQUIRE_PURPOSE')
  if F(sr['unresolved_area_m2'])>0:pending.append('PUBLIC_FUNCTIONAL_EXTENT_GAP')
  perunit.append({'unit':uid,'whole_unit_verdict':'UNKNOWN','source_room_roles':[r for r in rooms if r['unit']==uid],'capacity_use_access_source_rows':{k:digest(req[k])for k in ('fixture_inventory_use','body_route_sweeps','chair_capacity_movement','bath_service_operation','kitchen_essential_operation','guest_living_route','guest_dining_route','serving_route')},'current_source_public_extent_unresolved_m2':sr['unresolved_area_m2'],'entry_component_targets':[c['required_targets_served']for c in cr['entry_circulation_components']],'exact_pending':pending,'not_a_parent_acceptance_filter':True})
 nodes['Q12_PER_UNIT']={'status':'UNKNOWN_PER_UNIT_ROLE_DEPENDENCIES','evidence':perunit,'scope':'Direct same-model per-unit source capacity/use/access evidence and role gaps; no all12-PASS prerequisite and no dependency on Q12 verdict.'}
 nodes['Q14_SELECTION_SET']={'status':'UNKNOWN_SELECTION_SET_NOT_SUPPLIED','evidence':{'raw_requested_count':record['candidate']['request']['requested_count'],'actual_supplied_candidate_count':1,'actual_selection_set':None,'rule':'Single internal candidate is not a demonstrated final selection set. Requested count is not generated-set evidence. No N_A inferred from absent set.'}}
 from common_role_joint367 import evaluate as common_evaluate
 common_proof=common_evaluate(record,review)
 if common_proof['model_hash']!=mh or common_proof['raw_review_digest']!=digest(review):raise ValueError('COMMON365_SOURCE_CLOSURE_BINDING')
 nodes['COMMON_ROLE']={'status':common_proof['verdict'],'evidence':common_proof}
 if common_proof['verdict']!='PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE'or common_proof['missing']:raise ValueError('CURRENT_COMMON_ROLE_UNCLOSED')
 from balanced_access_joint367 import evaluate as balance_evaluate
 balance=balance_evaluate(record,review);nodes['Q12_PER_UNIT']['balanced_common_access']=balance
 for unit in perunit:
  if balance['verdict']!='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS':unit['exact_pending'].append('IR_P07_BALANCED_COMMON_ACCESS_UNRESOLVED')
 from entry_role_joint367 import evaluate as entry_evaluate
 entry=entry_evaluate(record,review)
 if entry['model_digest']!=mh or entry['record_digest']!=digest(record)or entry['fresh_result_digest']!=digest(review):raise ValueError('CURRENT_ENTRY_ROLE_BINDING')
 if entry['verdict']!='PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE':raise ValueError('CURRENT_ENTRY_ROLE_UNCLOSED')
 nodes['ENTRY_CIRCULATION']={'status':entry['verdict'],'evidence':entry,'scope':'Whole source entry function independently checked; path cost and comparative necessity are separate.'}
 bath_roles=[r for r in rooms if r['role']=='bath']
 if {r['unit']for r in bath_roles}!={u['id']for u in model['units']}:raise ValueError('SOURCE_BATH_ROLE_INVENTORY')
 nodes['SERVICE_CIRCULATION']={'status':'PASS_SCOPED_INTRINSIC_SOURCE_BATH_ACCESS_AND_ROUTE_USE_ACCOUNTING','evidence':{'source_bath_whole_roles':bath_roles,'current_entry_role_and_route_use_cost':entry},'scope':'Actual fixed source bath/WC room use and required access plus explicit current-source route-use classes. No global exclusive-function or compactness conclusion; final SERVICE criterion must use independent finite comparison.'}
 for unit in perunit:
  unit['exact_pending']=[p for p in unit['exact_pending']if p not in ('EXCLUSIVE_SERVICE_CIRCULATION_ACCOUNTING','WHOLE_COMMON_LOBBY_ROLE')]
  unit['intrinsic_service_role_digest']=digest(nodes['SERVICE_CIRCULATION'])
 nodes['Q14_SELECTION_SET']=selection_scope(record,review,req)
 order=ordered_dag()
 for name in order:
  nodes[name]['depends_on']=DAG[name];nodes[name]['blocking_dependencies']=[d for d in DAG[name]if nodes[d]['status'].startswith('UNKNOWN')]
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'schema':'ROLE_REGISTRY_JOINT367_INTRINSIC_DAG_WITH_FINITE_NECESSITY_PENDING','source_profile':source_profile,'model_hash':mh,'record_digest':digest(record),'review_digest':digest(review),'topological_order':order,'nodes':nodes,'fresh_execution':False,'admission_allowed':False,'whole_parent_complete':False}
if __name__=='__main__':
 r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('role_registry_joint_actual367.json').write_text(json.dumps(o,indent=2));print([(k,n['status'])for k,n in o['nodes'].items()])
