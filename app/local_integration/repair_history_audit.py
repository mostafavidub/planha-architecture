"""Task4.5 audit retained actual rejection->fresh child->all-gates history.
No solver or new geometry. Historical fresh execution remains task4.3, not simulated.
"""
import copy,hashlib,inspect
from pathlib import Path
from front_rear_runtime_adapter import ROOT,transport,ensure,source_audit,packet_binding,digest
from bounded_repair_chain import bind_result
from protected_repair_contract import freeze_parent,verify_child
from current_four_decision import assemble
from explicit_pair_redirection import require_rejection
from repair_attempt_control import classify_retained_parent
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def audit_history(parent,selection,contract,receipt,complete,operator,bundle,decision,expected):
 values=[transport(x)[0] for x in (parent,selection,contract,receipt,complete,operator,bundle,decision)]
 parent,selection,contract,receipt,complete,operator,bundle,decision=values;original=digest(values)
 keys=['parent','selection','contract','receipt','complete','operator','bundle','decision']
 ensure(set(expected)==set(keys),'HISTORY_RECEIPT_KEYS')
 for k,v in zip(keys,values):ensure(expected[k]==digest(v),'HISTORY_EXPECTED_DIGEST:'+k)
 from producer_provenance import snapshot,require_unchanged
 files=['app/local_integration/'+x for x in ('repair_history_audit.py','bounded_repair_chain.py','protected_repair_contract.py','repair_attempt_control.py','current_four_decision.py','explicit_pair_redirection.py')]
 snap=snapshot(ROOT,files);before=source_audit()
 for fn,name in ((bind_result,'bounded_repair_chain.py'),(verify_child,'protected_repair_contract.py'),(assemble,'current_four_decision.py'),(require_rejection,'explicit_pair_redirection.py')):
  ensure(Path(inspect.getsourcefile(fn)).resolve()==(ROOT/'app/local_integration'/name).resolve(),'HISTORY_IMPORT')
 for stored in (complete['source_snapshot'],receipt['source_snapshot']):require_unchanged(ROOT,stored)
 ensure(receipt['observed_result_digest']==digest(complete) and receipt['nonce']==complete['nonce'],'HISTORY_COMPLETE_RECEIPT')
 ensure(receipt['child_receipt_verified'] is True and receipt['source_integrity_verified'] is True and receipt['timed_out'] is False and receipt['wait_completed'] is True,'HISTORY_EXECUTION')
 ensure(all(receipt.get(k) is False for k in AUTH),'HISTORY_RECEIPT_AUTHORITY')
 ensure(type(receipt['returncode']) is int and receipt['returncode']==0,'HISTORY_PROCESS_RETURN_CODE')
 ensure(type(receipt['generated_count']) is int and receipt['generated_count']==complete['generated_count'],'HISTORY_SELECTED_COUNT')
 ensure(receipt['state']==complete['state'] and receipt['child_model_digest']==complete['child_model_digest'],'HISTORY_PARENT_RECEIPT_RESULT')
 bind_result(complete,receipt['nonce'],operator,bundle,decision)
 ensure(set(bundle['reports'])=={'replay','physical','functional'},'HISTORY_COMPLETE_ORIGINAL_REPORT_SET')
 functional=bundle['reports']['functional']
 ensure(functional['model_digest']==bundle['model_digest'] and functional['physical_review_digest']==bundle['report_digests']['physical'],'HISTORY_ORIGINAL_FUNCTIONAL_BINDING')
 ensure(all(functional[k] is False for k in AUTH),'HISTORY_ORIGINAL_FUNCTIONAL_AUTHORITY')
 frozen=freeze_parent(selection,parent,expected_selection_digest=digest(selection),expected_runtime_digest=digest(parent))
 ensure(digest(frozen)==digest(contract)==complete['contract_digest'],'HISTORY_PROTECTED_CONTRACT')
 preservation=verify_child(contract,digest(contract),bundle['packet'],bundle['context'])
 childmh=packet_binding(bundle['packet'],bundle['context'],parent['binding']['raw'],bundle['context']['construction_trace']['proposals']['A'])
 ensure(childmh==complete['child_model_digest'] and childmh!=parent['model_digest'],'HISTORY_DISTINCT_CHILD')
 ensure(complete['parent_model_digest']==parent['model_digest']==selection['parent_model_digest'],'HISTORY_PARENT_MODEL')
 ph=digest(parent['reports']['physical'])
 ensure(ph==selection['full_physical_digest']==complete['parent_physical_digest'] and digest(complete['parent_physical_report'])==ph,'HISTORY_PARENT_REPORT')
 require_rejection(parent['reports']['physical'])
 ensure(complete['parent_attempt_id']==contract['parent_attempt_id']==selection['parent_attempt_id'],'HISTORY_PARENT_LINEAGE')
 order=[r['criterion'] for r in decision['criteria']]
 ensure(len(order)==4 and len(set(order))==4 and set(order)==set(decision['assessments']),'HISTORY_CRITERION_SET')
 assessments={k:decision['assessments'][k] for k in order}
 rebuilt=assemble(bundle,assessments,{k:digest(v) for k,v in assessments.items()})
 ensure(digest(rebuilt)==digest(decision),'HISTORY_DECISION_REBUILD')
 ensure(digest(receipt['current_decision'])==digest(decision['decision']) and all(decision['decision'][k] is False for k in AUTH),'HISTORY_NO_DELIVERY')
 classification=classify_retained_parent(receipt)
 try:require_rejection(bundle['reports']['physical']);child_eligible=True
 except ValueError:child_eligible=False
 out={'schema':'ACTUAL_REJECTION_FRESH_CHILD_HISTORY_V1','state':'HISTORY_VERIFIED_DELIVERY_BLOCKED',
  'parent_model_digest':parent['model_digest'],'child_model_digest':childmh,'fresh_execution_nonce':receipt['nonce'],
  'parent_attempt_id':contract['parent_attempt_id'],'selected_operator_id':contract['operator_id'],
  'original_parent_physical':copy.deepcopy(parent['reports']['physical']),'original_parent_physical_digest':ph,
  'child_full_physical':copy.deepcopy(bundle['reports']['physical']),'child_full_physical_digest':bundle['report_digests']['physical'],
  'child_full_decision':copy.deepcopy(decision),'child_decision_digest':digest(decision),'protected_preservation':preservation,
  'budget_classification':classification,'rejection_matches_same_operator_scope':child_eligible,
  'repeat_execution_authorized_by_this_audit':False,'delivery_allowed':False,'display_allowed':False,'accepted':False,'qualified':False,
  'nodes':[{'kind':'ORIGINAL_REJECTED','model_digest':parent['model_digest']},{'kind':'EXISTING_OPERATOR_SELECTED','id':contract['operator_id']},{'kind':'FRESH_DISTINCT_CHILD_CONSTRUCTED','model_digest':childmh},{'kind':'ALL_FRESH_GATES_RECORDED','decision_digest':digest(decision)},{'kind':'DELIVERY_BLOCKED','reasons':decision['decision']['blockers']}],
  'source_snapshot':snap,'scope':'Read-only binding of actual task4.3 execution evidence and pure decision replay, not another fresh generation, runtime budget-controller replacement, or full product acceptance.'}
 ensure(digest(values)==original,'HISTORY_INPUT_MUTATION');require_unchanged(ROOT,snap);ensure(source_audit()==before,'HISTORY_SOURCE_CHANGED')
 out['integrity_verified']=True
 return out
