"""Audited current-source margin/balance integration; unresolved dependencies stay.
No SOURCE362 verdict reuse, caller flags, or admission. Old365 registry retained.
"""
import json
from pathlib import Path
from common import digest
from role_registry_model365 import evaluate as base_evaluate,DAG,ordered_dag
from entry_separation365 import evaluate as reserve_evaluate
from support_reservation365 import reconcile
from balanced_access365 import evaluate as balance_evaluate
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record,review):
 before=digest([record,review]);out=base_evaluate(record,review);n=out['nodes'];reserve=reserve_evaluate(record,review);balance=balance_evaluate(record,review);mh=digest(record['candidate']['model'])
 for proof in (reserve,balance):
  if proof['model_hash']!=mh or proof['record_digest']!=digest(record)or proof['fresh_result_digest']!=digest(review):raise ValueError('CURRENT_COMPONENT_BINDING')
 original=n['PUBLIC_SUPPORT']['evidence'];accounting=reconcile(original,reserve)
 n['PUBLIC_SUPPORT']={'status':'PASS_SCOPED_FUNCTIONAL_EXTENT_WITH_SEPARATE_NONUSABLE_OPERATIONAL_RESERVATION'if not accounting['unresolved_positive_extent']else'UNKNOWN_UNRESOLVED_FUNCTIONAL_EXTENT','evidence':{'original_source_function_support':original,'source_operational_reservation':reserve,'reconciled_role_ledger':accounting},'scope':'Exact functional floor role accounting with separately nonusable source separation reserve. No seating/useful-floor increment and no small-area waiver.'}
 ledger={r['unit']:r for r in accounting['rows']}
 for unit in n['Q12_PER_UNIT']['evidence']:
  unit['source_public_extent_before_operational_reservation_m2']=unit['current_source_public_extent_unresolved_m2'];unit['current_source_public_extent_unresolved_m2']=ledger[unit['unit']]['remaining_unresolved_area_m2'];unit['nonusable_operational_reservation_m2']=ledger[unit['unit']]['nonusable_operational_reservation_area_m2'];unit['usable_capacity_increment_from_reservation']=0
  if ledger[unit['unit']]['remaining_unresolved_area_m2']=='0'and'PUBLIC_FUNCTIONAL_EXTENT_GAP'in unit['exact_pending']:unit['exact_pending'].remove('PUBLIC_FUNCTIONAL_EXTENT_GAP')
  if balance['verdict']!='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS':unit['exact_pending'].append('IR_P07_CURRENT_SOURCE_BALANCED_ACCESS_UNRESOLVED')
  unit['current_balanced_access_evidence_digest']=digest(balance)
 n['Q12_PER_UNIT']['balanced_common_access']=balance
 rawrow=next(r for r in review['raw_report']['rule_contract_evidence']['requirements']if r['requirement_id']=='geometric_diversity')
 singleton=rawrow['status']=='NOT_APPLICABLE_TO_STAGE_OR_MODEL'and rawrow.get('applicability')=={'condition':'multiple_candidates','batch_model_hashes':[mh]}
 n['Q14_SELECTION_SET']['evidence']['internal_pair_test']={'status':'NOT_APPLICABLE_INTERNAL_SINGLETON_REVIEW'if singleton else'UNKNOWN_CURRENT_BATCH_APPLICABILITY','source_row':rawrow,'row_digest':digest(rawrow),'gate':'SOURCE_BALANCED365_CALLBACKS_PINNED_BY_REGISTERED_ARTIFACT_GATE','model_hash':mh}
 n['Q14_SELECTION_SET']['evidence']['selected_output_set_fulfillment']='NOT_PROVEN'
 out['common_core_subclaims']={'whole_junction_function':n['COMMON_ROLE'],'actual_balanced_access':balance,'finite_compact_comparison_status':n['Q04_COMPARISON']['status'],'parent_verdict':'UNKNOWN_REQUIRED_FINITE_CURRENT_SOURCE_COMPARISON'}
 for key in ordered_dag():n[key]['depends_on']=DAG[key];n[key]['blocking_dependencies']=[d for d in DAG[key]if n[d]['status'].startswith('UNKNOWN')]
 out.update(schema='ROLE_REGISTRY_BALANCED365_V2_AUDITED_NONUSABLE_RESERVATION_AND_BALANCE',model_hash=mh,fresh_execution=False,admission_allowed=False,whole_parent_complete=False)
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return out
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());v=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('role_registry_on365_v2.json').write_text(json.dumps(o,indent=2));print({k:v['status']for k,v in o['nodes'].items()})
