"""Final current-source role dependency integration; no engine reentry/delivery.
Fixed callable closures recompute evidence. No caller proof flags are accepted.
Q14 output selection-set parent remains UNKNOWN despite internal singleton N_A.
"""
import copy,json,hashlib
from pathlib import Path
from common import digest
from role_registry_joint367 import evaluate as base_evaluate
from role_registry_joint367 import DAG,ordered_dag

ROOT=Path(__file__).resolve().parents[1]
def evaluate(record,review):
 runner_path=Path(__file__).parent/'q04_runner367_v3.py'
 runner_sha='81097e13bcecdbf260d6bb648b49d4cf7cb6c742764adaa2e3209b9ef2469f4c'
 service_path=Path(__file__).parent/'service_runner367.py'
 service_sha='aebd4991be9a1521577374fc3c21d53c37886906fde0c92019e9773f6ab9e6ee'
 if runner_sha.startswith('PENDING') or service_sha.startswith('PENDING'):raise ValueError('AUDITED_CURRENT_CALLBACK_FREEZE_PENDING')
 if hashlib.sha256(service_path.read_bytes()).hexdigest()!=service_sha:raise ValueError('SERVICE_RUNNER_SOURCE_PIN')
 from q04_runner367_v3 import evaluate as q04_evaluate
 from service_runner367 import evaluate as service_evaluate
 if hashlib.sha256(runner_path.read_bytes()).hexdigest()!=runner_sha:raise ValueError('Q04_RUNNER_SOURCE_PIN')
 before=digest([record,review]);out=base_evaluate(record,review);q04=q04_evaluate(record,review);service=service_evaluate(record,review);mh=digest(record['candidate']['model']);n=out['nodes']
 if q04['model_digest']!=mh or q04['record_digest']!=digest(record) or q04['fresh_result_digest']!=digest(review):raise ValueError('Q04_BOUND_CURRENT_ARTIFACT')
 if any(service[k]!=v for k,v in [('model_digest',mh),('record_digest',digest(record)),('fresh_result_digest',digest(review))]):raise ValueError('SERVICE_BOUND_CURRENT_ARTIFACT')
 if service['verdict']!='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'or service['remaining']:raise ValueError('SERVICE_NOT_CLOSED')
 common=q04['current_common_role']
 if common['model_hash']!=mh or common['record_digest']!=digest(record)or common['raw_review_digest']!=digest(review):raise ValueError('COMMON_BOUND_CURRENT_ARTIFACT')
 if common['verdict']!='PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE'or common['missing']:raise ValueError('COMMON_ROLE_NOT_CLOSED')
 if q04['verdict']!='PASS_SCOPED_FINITE_Q04_SOURCE_JOINT367'or q04['remaining']:raise ValueError('Q04_NOT_CLOSED')
 n['COMMON_ROLE']={'status':'PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE','evidence':common,'scope':'Actual checked conceptual arrival/transfer and entry operation with clear source junction; legitimate margins. Not technical core certification or standalone optimality.'}
 n['Q04_COMPARISON']={'status':q04['verdict'],'evidence':q04,'scope':q04['invocation_scope']}
 walls=n['WALL_PURPOSE']['evidence'];private=n['PRIVATE_CIRCULATION']
 if private['status']!='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE' or walls.get('unjoined_host_ids'):raise ValueError('WALL_INTRINSIC_SOURCE_ROLE_INCOMPLETE')
 closed=[]
 for row in walls['rows']:
  if row['verdict']=='UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY':
   if row['kind']!='EXECUTED_SOURCE_PRIVATE_ACCESS_BOUNDARY':raise ValueError('UNSUPPORTED_PENDING_WALL_KIND')
   closed.append({'wall_id':row['wall_id'],'source_row_digest':digest(row),'intrinsic_private_role_digest':digest(private),'finite_q04_digest':digest(q04),'verdict':'PASS_SCOPED_SOURCE_PRIVATE_ACCESS_BOUNDARY_WITH_FINITE_NECESSITY'})
  elif not row['verdict'].startswith('PASS_'):raise ValueError('UNRESOLVED_WALL_ROLE')
 if len(closed)!=8:raise ValueError('EXPECTED_REGISTERED_HALL_WALL_INVENTORY')
 n['WALL_PURPOSE']={'status':'PASS_SCOPED_ALL_CURRENT_SOURCE_WALL_ROLES','evidence':{'immutable_constructive_wall_evidence':walls,'closed_hall_dependency_rows':closed,'source_model_hash':mh,'counterfactual_scope':'No wall removal/relocation alternative executed in this role proof; source role constructive claims plus actual finite Q04 prerequisites, not fabricated per-wall removal tests.'}}
 # Explicit non-circular role dependencies; no all-12 acceptance predicate.
 for key in DAG['Q11_WHOLE_ROLE']:
  if not n[key]['status'].startswith('PASS_'):raise ValueError('WHOLE_ROLE_DEPENDENCY:'+key)
 n['Q11_WHOLE_ROLE']={'status':'PASS_SCOPED_CURRENT_SOURCE_WHOLE_FUNCTIONAL_ROLE_ACCOUNTING','evidence':{'model_hash':mh,'dependency_digests':{k:digest(n[k])for k in DAG['Q11_WHOLE_ROLE']},'scope':'Exact accounted floor, whole operational source rooms and legitimate margins, source-supported public extent, actual private/entry/common function and bounded finite circulation comparison. Not global optimum.'}}
 privacy=next(r for r in review['raw_report']['rule_contract_evidence']['requirements']if r['requirement_id']=='privacy_scenarios')
 if privacy.get('model_hash')!=mh or privacy['status']!='PASS_LIMITED':raise ValueError('PRIVACY_CURRENT_SOURCE_PREREQUISITE')
 n['Q05_PRIVACY']={'status':'PASS_SCOPED_CURRENT_SOURCE_PRIVACY_AND_FUNCTIONAL_WALL_ROLES','evidence':{'model_hash':mh,'same_model_privacy_row':privacy,'wall_role_digest':digest(n['WALL_PURPOSE']),'whole_role_digest':digest(n['Q11_WHOLE_ROLE'])},'scope':'Actual source privacy scenarios plus source-functional wall roles; not arbitrary future occupancy/scenarios or technical certification.'}
 balance=n['Q12_PER_UNIT']['balanced_common_access']
 if balance['model_hash']!=mh or balance['record_digest']!=digest(record) or balance['fresh_result_digest']!=digest(review):raise ValueError('BALANCE_CURRENT_BINDING')
 if balance['verdict']!='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS' or not all(c['equal_fixed_source_metrics'] for c in balance['comparisons']):raise ValueError('BALANCE_UNCLOSED')
 perunit=n['Q12_PER_UNIT']['evidence']
 removable={'WHOLE_COMMON_LOBBY_ROLE','HALL_WALL_PURPOSE_Q04_DEPENDENCY','Q04_CLOSED_FINITE_ELIGIBLE_COMPARISON'}
 for unit in perunit:
  if set(unit['exact_pending'])-removable:raise ValueError('UNRESOLVED_PER_UNIT_ROLE')
  unit['resolved_dependency_digests']={k:digest(n[k]) for k in ('COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON')}
  unit['balanced_access_digest']=digest(balance);unit['finite_service_criterion_digest']=digest(service);unit['exact_pending']=[];unit['whole_unit_verdict']='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW'
 n['Q12_PER_UNIT']['status']='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW'
 # Output-set fulfillment is not waived by the singleton applicability callback.
 if n['Q14_SELECTION_SET']['evidence']['internal_pair_test']['status']!='NOT_APPLICABLE_INTERNAL_SINGLETON_REVIEW':raise ValueError('INTERNAL_PAIR_APPLICABILITY_UNESTABLISHED')
 n['Q14_SELECTION_SET']['status']='UNKNOWN_SELECTION_SET_NOT_SUPPLIED'
 for key in ordered_dag():
  n[key]['depends_on']=DAG[key];n[key]['blocking_dependencies']=[k for k in DAG[key]if not n[k]['status'].startswith('PASS_')]
 out.update(schema='ROLE_REGISTRY_FINAL_JOINT367_CURRENT_SOURCE_ROLES',fresh_execution=False,admission_allowed=False,whole_parent_complete=False,output_set_parent_verdict='UNKNOWN',selected_output_set_fulfillment='NOT_PROVEN',internal_q12_and_singleton_pair_subclaim='PASS_SCOPED_INTERNAL_Q12_WITH_INTERNAL_PAIR_N_A')
 parent_specs={'SPACE_ACCOUNTING':('Q11_WHOLE_ROLE',DAG['Q11_WHOLE_ROLE']),'CIRCULATION_NECESSITY':('Q04_COMPARISON',['ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE']),'PRIVACY_WITHOUT_FAKE_BAFFLE':('Q05_PRIVACY',DAG['Q05_PRIVACY'])}
 out['parent_evidence']={}
 for rid,(node,deps)in parent_specs.items():
  out['parent_evidence'][rid]={'verdict':'PASS_SCOPED_INTERNAL_CURRENT_SOURCE','missing':[],'required_dependency_nodes':deps,'dependency_evidence_digests':{d:digest(n[d])for d in deps},'closure_node':node,'closure_evidence_digest':digest(n[node]),'model_hash':mh,'fresh_result_digest':digest(review),'record_digest':digest(record),'explicit_complete_predicate':{'current_artifact_gate':True,'all_required_source_roles_closed':True,'same_model_comparative_runner_checked':True,'no_pending_required_dependency':not n[node]['blocking_dependencies']},'scope':'Current registered joint367 internal Concept review only; no all-domain or output-set admission.','source_assumptions':[common['engineering_assumption'],q04['invocation_scope']]}
 out['parent_evidence']['COMMON_CORE_COMPACTNESS']={'verdict':'PASS_SCOPED_INTERNAL_CURRENT_SOURCE','missing':[],'required_dependency_nodes':['COMMON_ROLE','Q11_WHOLE_ROLE','Q04_COMPARISON','Q12_PER_UNIT'],'dependency_evidence_digests':{k:digest(n[k]) for k in ('COMMON_ROLE','Q11_WHOLE_ROLE','Q04_COMPARISON','Q12_PER_UNIT')},'closure_node':'COMMON_ROLE','closure_evidence_digest':digest(n['COMMON_ROLE']),'model_hash':mh,'record_digest':digest(record),'fresh_result_digest':digest(review),'explicit_complete_predicate':{'current_artifact_gate':True,'whole_common_function_closed':True,'finite_comparison_closed':True,'source_access_metrics_exactly_balanced':True,'no_pending_required_dependency':True},'balance_evidence':balance,'scope':'Actual common functional role, finite registered-source comparison and exact equality of source route length/turn/fixed-square capacity; not all-state or technical-core certification.','source_assumptions':[common['engineering_assumption'],balance['scope']]}
 out['parent_evidence']['DISTINCTNESS_AND_FAIRNESS']={'verdict':'UNKNOWN','missing':['ACTUAL_REQUESTED_SELECTION_SET_NOT_SUPPLIED'],'model_hash':mh,'record_digest':digest(record),'fresh_result_digest':digest(review),'internal_per_unit_and_singleton_review':'PASS_SCOPED_INTERNAL_Q12; SINGLETON_PAIR_N_A_ONLY','per_unit_evidence_digest':digest(n['Q12_PER_UNIT']),'scope':'Requested count2 remains unproven, no delivery approval.'}
 out['service_compactness_evidence']=service
 out['parent_evidence']['SERVICE_COMPACTNESS']={'verdict':'PASS_SCOPED_INTERNAL_CURRENT_SOURCE','missing':[],'model_hash':mh,'record_digest':digest(record),'fresh_result_digest':digest(review),'closure_evidence_digest':digest(service),'explicit_complete_predicate':{'current_source_function_bound':True,'same_program_room_comparison_checked':True,'independent_finite_q04_checked':True,'no_pending_required_dependency':not service['remaining']},'scope':service['definition']}
 out['internal_per_unit_review']={'model_hash':mh,'record_digest':digest(record),'fresh_result_digest':digest(review),'verdict':n['Q12_PER_UNIT']['status'],'missing':[],'units':perunit,'dependency_evidence_digests':{k:digest(n[k])for k in DAG['Q12_PER_UNIT']},'explicit_complete_predicate':{'same_model_source_capacity_use_access':True,'all_unit_required_role_gaps_closed':all(not u['exact_pending']for u in perunit),'own_source_common_balance_closed':True,'same_model_finite_service_criterion_closed':not service['remaining'],'no_dependency_on_selected_set':True},'scope':'Internal current candidate units only. Pair distinctness and requested-count fulfillment are separate.'}
 if hashlib.sha256(service_path.read_bytes()).hexdigest()!=service_sha:raise ValueError('SERVICE_RUNNER_SOURCE_CHANGED')
 if hashlib.sha256(runner_path.read_bytes()).hexdigest()!=runner_sha:raise ValueError('Q04_RUNNER_SOURCE_CHANGED')
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return out
if __name__=='__main__':
 r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('role_registry_final_joint_actual367.json').write_text(json.dumps(o,indent=2));print({k:v['status']for k,v in o['nodes'].items()})
