"""Exact current-source equal access comparison, not general fairness approval."""
import json,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
import common
from common import digest,rows
from groups387 import build
ROOT=Path(__file__).resolve().parents[1]
PINS = {'balance363/assessor.py': '7049854a37e0d60126744704f08079582a4eb8ff15280f3f888c4808b1265372', 'balance363/clearance_kernel.py': '8f71fdb97812226fe8c7da769097163de22794bfbfdf533fdaf3fe6761baba8c', 'semantic_rules357/comparison_metrics.py': '952dbed32324f2d48d1428293bf68c438156801c70b9008168dea041f7365524'}
def evaluate(record,review):
 before=digest([record,review]);build(record,review,source_profile='SOURCE_BALANCED365')
 for name,sha in PINS.items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('BALANCE_KERNEL_SOURCE_PIN')
 old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source365.json';req=rows(record['candidate']['model'],review['raw_report'])
 finally:common.REGISTRY_NAME=old
 for k in ('core_concept','door_operation','opening_hosts','wall_network','partition_ledger'):
  if req[k]['status']!='PASS_LIMITED':raise ValueError('BALANCE_FRESH_PREREQUISITE:'+k)
 sys.path.insert(0,str(ROOT/'balance363'));from assessor import model_route
 m=record['candidate']['model'];actual=[model_route(m,k)for k in sorted(m['common_routes'])]
 diagnostic={'model_digest':digest(m),'record_digest':digest(record),'rows':actual,'newly_recomputed_current':True,'old365_diagnostic_reused':False}
 by={r['route_id']:r for r in actual};comparisons=[]
 for origin in ('stair','lift'):
  a,b=by[origin+'_A'],by[origin+'_B'];keys=['length_m','turns'];eq=all(F(a[k])==F(b[k])for k in keys)
  wa=F(a['fully_open_entry_passage_square_capacity']['max_axis_aligned_square_width_m']);wb=F(b['fully_open_entry_passage_square_capacity']['max_axis_aligned_square_width_m']);body=F(m['profile']['body_m']);eq=eq and wa==wb and wa>=body
  comparisons.append({'origin':origin,'equal_fixed_source_metrics':eq,'length_A_m':a['length_m'],'length_B_m':b['length_m'],'turns_A':a['turns'],'turns_B':b['turns'],'square_capacity_A_m':str(wa),'square_capacity_B_m':str(wb),'body_m':str(body),'scope':'Same-source fixed actual centerline, static plus fully-open entry passage; movement operations separately fresh-checked, not all-state simultaneous traversal.'})
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'schema':'BALANCED365_CURRENT_FRESH_ACCESS_METRICS','verdict':'PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS'if all(c['equal_fixed_source_metrics']for c in comparisons)else'UNKNOWN_BALANCE_NOT_ESTABLISHED','model_hash':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'comparisons':comparisons,'recomputed_route_evidence':actual,'diagnostic_digest':digest(diagnostic),'source_pins':PINS,'fresh_prerequisite_digests':{k:digest(req[k])for k in ('core_concept','door_operation','opening_hosts','wall_network','partition_ledger')},'scope':'Equality of actual route lengths/turns and independently exact fixed-path square capacities under declared source passage profile; no tolerance invented. Not other profiles, best-route or whole-plan/fair output-set approval.','source_assumptions_retained':actual[0]['unassessed'],'admission_allowed':False,'new_fresh':False,'whole_parent_complete':False}
