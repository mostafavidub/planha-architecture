"""Conservative exact readset equivalence, not fresh execution authority.
Public pipeline boundary must independently bind real supervised execution.
No raw timing fields are discarded; only outer elapsed seconds may differ.
"""
import json,hashlib,copy,math
from fractions import Fraction

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def rows(raw):
 r=raw['rule_contract_evidence']['requirements']
 if type(r)is not list or len(r)!=38 or any(type(x)is not dict for x in r):raise ValueError('EXACT_38_REQUIREMENT_ROWS')
 ids=[x['requirement_id']for x in r]
 if len(set(ids))!=38:raise ValueError('DUPLICATE_REQUIREMENT')
 return{q['requirement_id']:q for q in r}
def compare(reference_record,reference_fresh,current_record,current_fresh):
 before=digest([reference_record,reference_fresh,current_record,current_fresh])
 # Full record equality deliberately includes all constructor trace/source/cohort
 # metadata, not just geometry. Run identity belongs in the external envelope.
 if digest(reference_record)!=digest(current_record):raise ValueError('FULL_CONSTRUCTOR_RECORD_READSET_CHANGED')
 c=current_record['candidate'];mh=digest(c['model'])
 for fresh in (reference_fresh,current_fresh):
  if fresh.get('fresh_checker_executed')is not True or fresh.get('source_unchanged')is not True:raise ValueError('CHECKER_EXECUTION_OR_SOURCE_PREREQUISITE')
  if fresh.get('input_record_digest')!=digest(current_record)or fresh.get('outer_trace_digest')!=digest(current_record['trace'])or fresh.get('model_digest')!=mh:raise ValueError('FRESH_RECORD_MODEL_TRACE')
  p=fresh['provenance']
  if p.get('verified')is not True or p['candidate_digest']!=digest(c)or p['packet_digest']!=digest(c['packet'])or p['model_hash']!=mh:raise ValueError('FRESH_PROVENANCE')
  if digest(p['raw'])!=digest(c['request'])or c['request_digest']!=digest(c['request']):raise ValueError('RAW_REQUEST_BINDING')
 if set(reference_fresh)!=set(current_fresh):raise ValueError('UNSUPPORTED_FRESH_SCHEMA_FIELD')
 for key in reference_fresh:
  if key=='seconds':
   for fresh in (reference_fresh,current_fresh):
    if type(fresh[key])not in(int,float)or not math.isfinite(fresh[key])or fresh[key]<0:raise ValueError('OUTER_SECONDS_INVALID')
  elif digest(reference_fresh[key])!=digest(current_fresh[key]):raise ValueError('FULL_FRESH_SEMANTIC_READSET_CHANGED:'+key)
 old=rows(reference_fresh['raw_report']);new=rows(current_fresh['raw_report'])
 if set(old)!=set(new):raise ValueError('REQUIREMENT_INVENTORY_CHANGED')
 proofs=[]
 for rid in sorted(old):
  if digest(old[rid])!=digest(new[rid]):raise ValueError('REQUIREMENT_READSET_CHANGED:'+rid)
  proofs.append({'requirement_id':rid,'reference_row_digest':digest(old[rid]),'current_row_digest':digest(new[rid]),'status':new[rid]['status'],'applicability_present':'applicability'in new[rid],'applicability_digest':digest(new[rid].get('applicability')),'method_present':'method'in new[rid],'method_digest':digest(new[rid].get('method')),'evidence_present':'evidence'in new[rid],'evidence_digest':digest(new[rid].get('evidence'))})
 if digest([reference_record,reference_fresh,current_record,current_fresh])!=before:raise ValueError('INPUT_MUTATION')
 return{'schema':'EXACT368_FULL_READSET_EQUIVALENCE','model_digest':mh,'packet_digest':digest(c['packet']),'record_digest':digest(current_record),'reference_fresh_digest':digest(reference_fresh),'current_fresh_digest':digest(current_fresh),'raw_report_digest':digest(current_fresh['raw_report']),'expected_method_registry_digest':digest(current_fresh['expected_method_registry']),'requirements':proofs,'raw_timing_allowlist':[],'outer_nonsemantic_difference_allowlist':['/seconds'],'evidence_equivalent':True,'execution_authority':False,'scope':'Full record and all semantic fresh fields identical; outer elapsed seconds separately retained. This comparison itself does not prove a new execution.'}

def attest_proofs(quality,proof_map,equivalence,current_groups,run_binding,pinned_policy_digest):
 if equivalence.get('evidence_equivalent')is not True:raise ValueError('EQUIVALENCE_MISSING')
 if {r.get('requirement_id')for r in current_groups.get('rows',[])}!={'partition_ledger','door_operation','fixture_inventory_use','closet_operation','kitchen_essential_operation','bath_service_operation','program_functional_roles','privacy_scenarios','stored_living_network288'}or current_groups.get('current_predicates_recomputed')is not True:raise ValueError('EXACT_CURRENT_GROUP_INVENTORY')
 if current_groups.get('review_verdict')!='SCOPED_PASS'or len(current_groups.get('rows',[]))!=9 or any(r.get('verdict')!='SCOPED_PASS'for r in current_groups['rows']):raise ValueError('CURRENT_NINE_SEMANTIC_PREDICATES_REQUIRED')
 if current_groups.get('model_hash')!=equivalence['model_digest']or current_groups.get('current_fresh_digest')!=equivalence['current_fresh_digest']or current_groups.get('current_record_digest')!=equivalence['record_digest']:raise ValueError('CURRENT_GROUP_ARTIFACT_BINDING')
 if run_binding.get('model_digest')!=equivalence['model_digest']or run_binding.get('fresh_digest')!=equivalence['current_fresh_digest']or run_binding.get('record_digest')!=equivalence['record_digest']:raise ValueError('CURRENT_ATTESTATION_RUN_BINDING')
 by={q['rule_id']:q for q in quality};out=[]
 if {p['rule_id']for p in proof_map}!=set(by)-{'DISTINCTNESS_AND_FAIRNESS'}:raise ValueError('EXACT_PARENT_PROOF_SET')
 if len(by)!=12 or len(proof_map)!=11 or len({p['rule_id']for p in proof_map})!=11:raise ValueError('PROOF_PARENT_INVENTORY')
 for p in proof_map:
  q=by[p['rule_id']]
  if q['verdict']!='PASS'or q.get('missing')!=[]or digest(q)!=p['original_parent_evidence_digest']:raise ValueError('ORIGINAL_QUALIFIED_PROOF_CHANGED')
  for key in('model_digest','packet_digest','record_digest','raw_report_digest','expected_method_registry_digest'):
   if p['exact_readset'][key]!=equivalence[key]:raise ValueError('PROOF_SPECIFIC_READSET_CHANGED:'+p['rule_id']+':'+key)
  if p['exact_readset']['required_requirement_ids']!=[r['requirement_id']for r in equivalence['requirements']]:raise ValueError('PROOF_REQUIREMENT_READSET_INCOMPLETE')
  if p['source_contract_cohort_policy_digest']!=pinned_policy_digest:raise ValueError('NON_GEOMETRIC_SOURCE_POLICY_BINDING')
  out.append({'rule_id':p['rule_id'],'verdict':'PASS_SCOPED_REUSED_PROOF_WITH_CURRENT_PREREQUISITES','original_parent_evidence_digest':p['original_parent_evidence_digest'],'original_proof_map_digest':digest(p),'current_fresh_digest':equivalence['current_fresh_digest'],'reference_fresh_digest':equivalence['reference_fresh_digest'],'current_groups_digest':digest(current_groups),'run_binding_digest':digest(run_binding),'scope':'Explicit reuse of identical fixed-model/source/cohort/contract proof after current fresh and current semantic prerequisite validation; not recomputation of every original proof.'})
 return out
