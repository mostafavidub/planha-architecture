"""Final current-source role dependency integration; no engine reentry/delivery.
Fixed callable closures recompute evidence. No caller proof flags are accepted.
Q14 output selection-set parent remains UNKNOWN despite internal singleton N_A.
"""
import copy,json,hashlib
from pathlib import Path
from common import digest
from role_registry_model362_v2 import evaluate as base_evaluate,DAG,ordered_dag
from q04_runner362_v3 import evaluate as q04_evaluate
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record,review):
 runner_path=Path(__file__).parent/'q04_runner362_v3.py'
 runner_sha='726cb836fa5577f71d82d81200ae87b08adf4fe7315144599c7cf2b34e8dd7cf'
 if hashlib.sha256(runner_path.read_bytes()).hexdigest()!=runner_sha:raise ValueError('Q04_RUNNER_SOURCE_PIN')
 before=digest([record,review]);out=base_evaluate(record,review);q04=q04_evaluate(record,review);mh=digest(record['candidate']['model']);n=out['nodes']
 if q04['model_digest']!=mh or q04['record_digest']!=digest(record) or q04['fresh_result_digest']!=digest(review):raise ValueError('Q04_BOUND_CURRENT_ARTIFACT')
 common=q04['common_role']
 if common['model_hash']!=mh or common['record_digest']!=digest(record)or common['raw_review_digest']!=digest(review):raise ValueError('COMMON_BOUND_CURRENT_ARTIFACT')
 if common['verdict']!='PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE'or common['missing']:raise ValueError('COMMON_ROLE_NOT_CLOSED')
 if q04['verdict']!='PASS_SCOPED_FINITE_Q04_CURRENT_SOURCE_PROFILE'or q04['remaining']:raise ValueError('Q04_NOT_CLOSED')
 n['COMMON_ROLE']={'status':'PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE','evidence':common,'scope':'Actual checked conceptual arrival/transfer and entry operation with clear source junction; legitimate margins. Not technical core certification or standalone optimality.'}
 n['Q04_COMPARISON']={'status':q04['verdict'],'evidence':q04,'scope':q04['scope']}
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
 perunit=n['Q12_PER_UNIT']['evidence']
 removable={'WHOLE_COMMON_LOBBY_ROLE','HALL_WALL_PURPOSE_Q04_DEPENDENCY','Q04_CLOSED_FINITE_ELIGIBLE_COMPARISON'}
 for unit in perunit:
  if set(unit['exact_pending'])-removable:raise ValueError('UNRESOLVED_PER_UNIT_ROLE')
  unit['resolved_dependency_digests']={k:digest(n[k])for k in ('COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON')};unit['exact_pending']=['IR_P07_BALANCED_LIFT_ACCESS_REVIEW_OR_AUTHORIZED_TRADEOFF'];unit['whole_unit_verdict']='UNKNOWN_BALANCED_COMMON_ACCESS_QUALITY';unit['intrinsic_functional_role_verdict']='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_REVIEW'
 n['Q12_PER_UNIT']['status']='UNKNOWN_MANDATORY_BALANCED_COMMON_ACCESS_QUALITY'
 routes=record['candidate']['model']['common_routes'];lift=[]
 from fractions import Fraction as F
 for uid in ('A','B'):
  path=routes['lift_'+uid];length=sum(abs(F(a[0])-F(b[0]))+abs(F(a[1])-F(b[1]))for a,b in zip(path,path[1:]));lift.append({'unit':uid,'source_route':'lift_'+uid,'length_m':str(length),'path':path})
 n['Q12_PER_UNIT']['balanced_common_access']={'actual_routes':lift,'length_spread_m':str(max(F(x['length_m'])for x in lift)-min(F(x['length_m'])for x in lift)),'verdict':'UNKNOWN_NO_AUTHORIZED_BALANCE_THRESHOLD_OR_TRADEOFF','source_rule':'IR-P07','no_threshold_invented':True}
 # Output-set fulfillment is not waived by the singleton applicability callback.
 if n['Q14_SELECTION_SET']['evidence']['internal_pair_test']['status']!='NOT_APPLICABLE_INTERNAL_SINGLETON_REVIEW':raise ValueError('INTERNAL_PAIR_APPLICABILITY_UNESTABLISHED')
 n['Q14_SELECTION_SET']['status']='UNKNOWN_SELECTION_SET_NOT_SUPPLIED'
 for key in ordered_dag():
  n[key]['depends_on']=DAG[key];n[key]['blocking_dependencies']=[k for k in DAG[key]if not n[k]['status'].startswith('PASS_')]
 out.update(schema='ROLE_REGISTRY_FINAL362_V2_BALANCED_ACCESS_GAP',fresh_execution=False,admission_allowed=False,whole_parent_complete=False,output_set_parent_verdict='UNKNOWN',selected_output_set_fulfillment='NOT_PROVEN',internal_q12_and_singleton_pair_subclaim='UNKNOWN_BALANCED_ACCESS_QUALITY_WITH_INTERNAL_PAIR_N_A')
 parent_specs={'SPACE_ACCOUNTING':('Q11_WHOLE_ROLE',DAG['Q11_WHOLE_ROLE']),'CIRCULATION_NECESSITY':('Q04_COMPARISON',['ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE']),'PRIVACY_WITHOUT_FAKE_BAFFLE':('Q05_PRIVACY',DAG['Q05_PRIVACY'])}
 out['parent_evidence']={}
 for rid,(node,deps)in parent_specs.items():
  out['parent_evidence'][rid]={'verdict':'PASS_SCOPED_INTERNAL_CURRENT_SOURCE','missing':[],'required_dependency_nodes':deps,'dependency_evidence_digests':{d:digest(n[d])for d in deps},'closure_node':node,'closure_evidence_digest':digest(n[node]),'model_hash':mh,'fresh_result_digest':digest(review),'record_digest':digest(record),'explicit_complete_predicate':{'current_artifact_gate':True,'all_required_source_roles_closed':True,'same_model_comparative_runner_checked':True,'no_pending_required_dependency':not n[node]['blocking_dependencies']},'scope':'Current registered source362 internal Concept review only; no all-domain or output-set admission.','source_assumptions':[common['engineering_assumption'],q04['scope']]}
 out['parent_evidence']['COMMON_CORE_COMPACTNESS']={'verdict':'UNKNOWN','missing':['BALANCED_LIFT_ACCESS_REVIEW_OR_AUTHORIZED_TRADEOFF'],'model_hash':mh,'fresh_result_digest':digest(review),'evidence':{'common_role_digest':digest(common),'finite_q04_digest':digest(q04)},'balance_evidence':n['Q12_PER_UNIT']['balanced_common_access'],'scope':'Common functional role and bounded comparison closed; IR-P07 lift access balance remains unresolved. No arbitrary tolerance or owner tradeoff inferred.'}
 out['parent_evidence']['DISTINCTNESS_AND_FAIRNESS']={'verdict':'UNKNOWN','missing':['ACTUAL_REQUESTED_SELECTION_SET_NOT_SUPPLIED'],'model_hash':mh,'fresh_result_digest':digest(review),'internal_per_unit_and_singleton_review':'UNKNOWN_Q12_BALANCED_COMMON_ACCESS; SINGLETON_PAIR_N_A_ONLY','scope':'Requested count2 remains unproven, no delivery approval.'}
 if hashlib.sha256(runner_path.read_bytes()).hexdigest()!=runner_sha:raise ValueError('Q04_RUNNER_SOURCE_CHANGED')
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return out
if __name__=='__main__':
 r=json.loads((ROOT/'staging362_core_notch/actual362.json').read_text());v=json.loads((ROOT/'review362_source_validation/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('role_registry_final_actual362_v2.json').write_text(json.dumps(o,indent=2));print({k:v['status']for k,v in o['nodes'].items()})
