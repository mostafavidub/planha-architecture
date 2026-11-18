"""Final finite SERVICE criterion using independent roles and Q04 necessity.
Current-source route-only cost is not asserted to be global exclusive-use floor.
"""
from cost_runner367 import evaluate as costs
from q04_runner367_v3 import evaluate as necessity
from common import digest
from fractions import Fraction as F

def scoped_metric(entry):
 keys=['current_source_service_only_route_area_m2','current_source_nonservice_only_route_area_m2','current_source_shared_route_area_m2']
 vals=[F(entry[k])for k in keys]
 if any(v<0 for v in vals)or sum(vals)!=F(entry['whole_entry_area_m2']):raise ValueError('INCOMPLETE_SOURCE_FUNCTION_PARTITION')
 if not entry['all_cells_required_traversal_bound']or entry['classification_scope']!='CURRENT_SOURCE_DECLARED_ROUTE_USE_CLASSES_NOT_EXCLUSIVITY_OF_ALL_POSSIBLE_FUNCTIONS':raise ValueError('FUNCTION_INVENTORY_SCOPE_UNBOUND')
 if F(entry['service_only_outside_source_approach_m2'])>vals[0]:raise ValueError('SERVICE_APPROACH_ACCOUNTING')
 return {'A_exclusive_service_circulation_m2':str(vals[0]),'operational_definition':'Exclusive within the complete required activity/scenario route-use inventory of this sourceprofile: current bath/WC-only access atoms, excluding shared and nonservice atoms; not exclusivity over all possible future uses.','includes':'Source bath approach/threshold atoms outside the bath room when only bath-required routes use them; source bath room itself counted once separately.','source_function_partition_m2':dict(zip(keys,map(str,vals))),'global_exclusive_function_m2':None}

def reduce_bound(record,review,ledger,q04,partition):
 for x in (ledger,q04,partition):
  if x['record_digest']!=digest(record)or x['fresh_result_digest']!=digest(review)or x['model_digest']!=digest(record['candidate']['model']):raise ValueError('OWN_CURRENT_BINDING')
 remaining=[];units=[]
 if partition['verdict']!='PASS_SCOPED_CURRENT_SOURCE_ROLE_PARTITION'or partition['remaining']:remaining.append('CURRENT_FUNCTIONAL_PARTITION_NOT_CLOSED')
 if partition['global_exclusive_function_m2']is not None:raise ValueError('UNSUPPORTED_GLOBAL_EXCLUSIVE_CLAIM')
 if {u['unit']for u in partition['units']}!={u['unit']for u in ledger['units']}:raise ValueError('PARTITION_UNIT_INVENTORY')
 for u in ledger['units']:
  b=u['against359'];entry=u['intrinsic_entry']if 'intrinsic_entry'in u else next(e for e in q04['entry_role']['units']if e['unit']==u['unit'])
  route_metric=scoped_metric(entry)
  part=next(x for x in partition['units']if x['unit']==u['unit'])
  if F(part['unclassified_m2'])!=0 or sum(F(part[k])for k in ('exclusive_current_profile_m2','shared_current_profile_m2','nonservice_current_profile_m2'))!=F(part['whole_entry_area_m2']):raise ValueError('FUNCTIONAL_PARTITION_INCOMPLETE')
  if F(part['route_only_measurement_m2'])!=F(route_metric['A_exclusive_service_circulation_m2']):raise ValueError('ROUTE_MEASUREMENT_BINDING')
  metric={'A_exclusive_service_circulation_m2':part['exclusive_current_profile_m2'],'definition':'Exclusive within complete current source functional room/task/scenario/operation inventory, with independent whole-role and motion joins, including bath approach outside bathroom.','global_exclusive_function_m2':None,'functional_partition':part}
  if not b['same_validated_service_program']:remaining.append(u['unit']+':SAME_PROGRAM_OWNERSHIP_BASELINE')
  if F(b['current_room_excess_m2'])!=0:remaining.append(u['unit']+':ROOM_EXCESS_FUNCTIONAL_REASON_NOT_IMPLEMENTED')
  if entry['verdict']!='PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE':remaining.append(u['unit']+':SOURCE_ACCESS_FUNCTION')
  units.append({'unit':u['unit'],'bath_WC_union_m2':u['bath_WC_union_m2'],'R_service_percent':b['R_service_percent'],'A_unit_net_m2':b['A_unit_net_m2'],'smallest_actually_validated_same_source_room_m2':b['tested_cohort_min_room_m2'],'actual_source_service_route_only_m2':u['actual_source_service_route_only_m2'],'scoped_exclusive_metric':metric,'global_exclusive_function_m2':None,'functional_reason':'Actual source-required bath activity routes, exact source-derived whole entry access domain, own fresh actor/scenario checks. Not route optimality.','excess_comparison':'Full vector finite Q04: all unit routes/circulation, all common transfers, common area; all registered alternatives have known-worse coordinate under componentwise noncompensation. Not service-area-only global minimization.'})
 if q04['verdict']!='PASS_SCOPED_FINITE_Q04_SOURCE_JOINT367'or q04['remaining']:remaining.append('FINITE_NECESSITY_NOT_CLOSED')
 return {'schema':'SOURCE_JOINT367_FINITE_SERVICE_CRITERION','record_digest':digest(record),'fresh_result_digest':digest(review),'model_digest':digest(record['candidate']['model']),'units':units,'verdict':'UNKNOWN'if remaining else'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS','remaining':remaining,'cost_receipt_digest':digest(ledger),'necessity_receipt_digest':digest(q04),'comparison_scope':'Roomminimum compares homogeneous bath/WC union and identical sourceprogram against359. No baseline exclusive-metric equality or minimum is claimed. Nonzero current scoped-exclusive circulation is separately justified by source access role plus finite full-vector Q04; global exclusiveuse remains unknown.','functional_partition_digest':digest(partition),'definition':'Nonzero source-route cost retained and justified by independent intrinsic access function plus finite noncompensatory comparison. Global service exclusivity and global minimum not claimed.','accepted':False,'new_fresh_execution':False,'all_parent_acceptance':False}
def evaluate(record,review):
 from service_role_inventory_joint367 import evaluate as roles
 c=costs(record,review);q=necessity(record,review);p=roles(record,review)
 out=reduce_bound(record,review,c,q,p)
 out['invocation_receipts']={'cost':c,'necessity':q,'functional_partition':p}
 if out['cost_receipt_digest']!=digest(c)or out['necessity_receipt_digest']!=digest(q)or out['functional_partition_digest']!=digest(p):raise ValueError('SAME_INVOCATION_RECEIPT_DIGEST')
 out['receipt_scope']='Exact callback return objects from this invocation, not archived standalone receipts; list ordering and other witness differences are preserved.'
 return out
