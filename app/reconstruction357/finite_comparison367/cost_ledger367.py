"""Own-source current access cost ledger; final necessity remains independent."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'semantic_rules357'),str(ROOT/'finite_comparison367')]
from common import digest

def bound_join(record,review,measurement,entry):
 for k,v in [('record_digest',digest(record)),('fresh_result_digest',digest(review)),('model_digest',digest(record['candidate']['model']))]:
  if entry[k]!=v:raise ValueError('ENTRY_BINDING:'+k)
 if entry['verdict']!='PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE':raise ValueError('ENTRY_NOT_VALIDATED')
 units=[]
 for u in measurement['against359']['evidence'][1]['units']:
  e=next(x for x in entry['units']if x['unit']==u['unit'])
  if not e['all_cells_required_traversal_bound']or e['verdict']!=entry['verdict']:raise ValueError('UNIT_ENTRY_NOT_VALIDATED')
  cost=F(e['service_only_outside_source_approach_m2'])
  if cost!=F(u['outside_entry_unassigned_m2']):raise ValueError('EXACT_ROUTE_COST_ACCOUNTING')
  units.append({'unit':u['unit'],'bath_WC_union_m2':u['bath_union_m2'],'actual_source_service_route_only_m2':str(cost),'global_exclusive_function_m2':None,'route_use_scope':e['classification_scope'],'intrinsic_entry':e,'against359':next(x for x in measurement['against359']['units']if x['unit']==u['unit']),'against362':next(x for x in measurement['against362']['units']if x['unit']==u['unit']),'final_compactness':'UNKNOWN_FUNCTIONAL_EXCESS_REASON_AND_FINITE_PROTECTION_REQUIRED'})
 if {u['unit']for u in units}!={u['unit']for u in entry['units']}:raise ValueError('UNIT_INVENTORY')
 return {'schema':'JOINT367_OWN_COST_LEDGER','record_digest':digest(record),'fresh_result_digest':digest(review),'model_digest':digest(record['candidate']['model']),'source_profile':'SOURCE_JOINT367','units':units,'entry_evidence_digest':digest(entry),'measurement_digest':digest(measurement),'verdict':'UNKNOWN','accepted':False,'new_fresh_execution':False,'final_SERVICE_required_by_intrinsic':False,'source_policy':'Nonzero route cost is retained, not an automatic failure or global exclusive-use assertion. Final necessity uses independent intrinsic roles and finite protected comparisons.'}

def evaluate(record,review):
 from legacy_service_diagnostic367 import evaluate as measure
 from entry_role_joint367 import evaluate as role
 return bound_join(record,review,measure(record,review),role(record,review))
