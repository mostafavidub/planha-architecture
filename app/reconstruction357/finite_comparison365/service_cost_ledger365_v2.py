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

def evaluate(record,review):
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
if __name__=='__main__':
 r,f=[json.loads((ROOT/p).read_text())for p in ['staging365_service_grammar/candidate365.json','review365_service_source_validation/result.json']];o=evaluate(r,f);p=Path(__file__).with_name('service_cost_ledger_actual365_v2.json');assert not p.exists();p.write_text(json.dumps(o,indent=2));print(o['verdict'])
