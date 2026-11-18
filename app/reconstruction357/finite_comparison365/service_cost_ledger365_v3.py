"""Measured cost inventory before functional classification; no zero-residual gate.
Q04 may consume these bounds without depending on final SERVICE acceptance.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from service_candidate_criterion365 import evaluate as measured,ROOT,digest
from service_public_role_join365 import evaluate as role_join

def cost_bounds(room_area,unclassified_route_atoms):
 room=F(room_area);unknown=F(unclassified_route_atoms)
 if room<0 or unknown<0:raise ValueError('NEGATIVE_MEASURED_AREA')
 return {'bath_WC_union_m2':str(room),'exclusive_service_circulation_m2':None if unknown else '0','unclassified_route_only_m2':str(unknown),'service_room_plus_unclassified_cost_interval_m2':[str(room),str(room+unknown)],'role_classification_complete':unknown==0,'nonzero_is_not_automatic_failure':True}

def evaluate_measurement(record,review):
 raw=measured(record,review);join=role_join(record,review);mh=digest(record['candidate']['model'])
 if join['model_digest']!=mh or join['record_digest']!=digest(record)or join['fresh_result_digest']!=digest(review):raise ValueError('OWN_ROLE_BINDING')
 result=[]
 for u in raw['against359']['evidence'][1]['units']:
  r=next(x for x in join['units']if x['unit']==u['unit'])
  if F(r['route_only_residual_area_m2'])!=F(u['outside_entry_unassigned_m2']):raise ValueError('RESIDUAL_ACCOUNTING_DISAGREEMENT')
  cost=cost_bounds(u['bath_union_m2'],r['route_only_residual_area_m2'])
  result.append({'unit':u['unit'],'cost_inventory':cost,'role_join':r,'baseline359':next(x for x in raw['against359']['units']if x['unit']==u['unit']),'remaining':['INDEPENDENT_WHOLE_ENTRY_ROLE_AND_EXCLUSIVE_SHARED_CLASSIFICATION','FUNCTIONAL_EXCESS_REASON_AND_PROTECTED_FINITE_COMPARISON'],'verdict':'UNKNOWN'})
 policy=Path(__file__).with_name('service_cost_policy365_v2.json')
 return {'schema':'SERVICE365_COST_LEDGER_V2','record_digest':digest(record),'fresh_result_digest':digest(review),'model_digest':mh,'policy_sha256':hashlib.sha256(policy.read_bytes()).hexdigest(),'source_contract_sha256':raw['against359']['source274_rule_sha256'],'units':result,'measurement_digest':digest(raw),'role_join_digest':digest(join),'verdict':'UNKNOWN','accepted':False,'new_fresh_execution':False,'final_service_used_as_intrinsic_gate':False,'note':'Intervals describe unresolved route-only classification, not total unknown architecture or proof of exclusive service function.'}

ENTRY_FREEZE_SHA="bc5b89e296bcf6c9816ca7045b2c733e8a9d881ac6f504c63dca818030781f16"
def check_entry_sources():
 p=ROOT/'semantic_rules357/entry_role_service365_source_freeze.json'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=ENTRY_FREEZE_SHA:raise ValueError('ENTRY_FREEZE_CHANGED')
 freeze=json.loads(p.read_text())
 for name,sha in freeze['files'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('ENTRY_SOURCE_CHANGED:'+name)
 return digest(freeze)

def join_intrinsic(measurement,entry):
 for key in ('record_digest','fresh_result_digest','model_digest'):
  if entry[key]!=measurement[key]:raise ValueError('ENTRY_'+key+'_BINDING')
 if entry['verdict']!='PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE':raise ValueError('UNTESTED_ENTRY_ROLE')
 if {u['unit']for u in entry['units']}!={u['unit']for u in measurement['units']}:raise ValueError('ENTRY_UNIT_INVENTORY')
 for u in measurement['units']:
  e=next(e for e in entry['units']if e['unit']==u['unit'])
  if e['verdict']!='PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE' or not e['all_cells_required_traversal_bound']:raise ValueError('UNTESTED_UNIT_ENTRY_ROLE')
  if F(e['service_only_outside_source_approach_m2'])!=F(u['cost_inventory']['unclassified_route_only_m2']):raise ValueError('ENTRY_COST_MISMATCH')
  u['intrinsic_entry_role']=e
  u['cost_inventory']['actual_source_service_route_only_m2']=e['service_only_outside_source_approach_m2']
  u['cost_inventory']['current_route_use_classification_complete']=True
  u['cost_inventory']['classification_scope']=e['classification_scope']
  u['remaining']=['FUNCTIONAL_EXCESS_REASON_AND_PROTECTED_FINITE_COMPARISON','OWN_PRIVATE_AND_COMMON_NECESSITY','NO_GLOBAL_EXCLUSIVE_FUNCTION_CLAIM']
 measurement.update(schema='SERVICE365_CONNECTED_COST_LEDGER_V3',intrinsic_entry_digest=digest(entry),intrinsic_entry_role='PASS_SCOPED',verdict='UNKNOWN',final_service_used_as_intrinsic_gate=False)
 return measurement

def evaluate(record,review):
 before=digest([record,review]);freeze=check_entry_sources()
 from entry_role_service365 import evaluate as intrinsic
 x=join_intrinsic(evaluate_measurement(record,review),intrinsic(record,review))
 if check_entry_sources()!=freeze or digest([record,review])!=before:raise ValueError('SOURCE_OR_INPUT_CHANGED')
 x['entry_source_freeze_digest']=freeze
 return x
if __name__=='__main__':
 r,f=[json.loads((ROOT/p).read_text())for p in ['staging365_service_grammar/candidate365.json','review365_service_source_validation/result.json']];o=evaluate(r,f);p=Path(__file__).with_name('service_cost_ledger_actual365_v3.json');assert not p.exists();p.write_text(json.dumps(o,indent=2));print(o['verdict'])
