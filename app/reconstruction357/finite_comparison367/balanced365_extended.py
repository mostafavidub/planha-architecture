"""New receipt for expanded cohort; old balanced365 evidence remains immutable."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'semantic_rules357'),str(ROOT/'finite_comparison365')]
from common import digest
from q04_runner365 import evaluate as original
from q04_closure365_v7 import compare
from group_readsets367 import build
from eligibility_intrinsic367 import evaluate as eligibility

def evaluate(record,review):
 old=original(record,review);r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());f=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());gate=build(r,f,source_profile='SOURCE_JOINT367');own=eligibility(r,f,source_profile='SOURCE_JOINT367');pair=compare(record['candidate']['model'],r['candidate']['model'])
 remaining=[]
 if not old['verdict'].startswith('PASS_')or old['remaining']:remaining.append('ORIGINAL_FIXED_COHORT_NOT_CLOSED')
 if not own['eligible']or own['verdict']!='PASS':remaining.append('ADDED367_OWN_INTRINSIC_NOT_PASS')
 if pair['dominance']!='FALSE':remaining.append('ADDED367_COMPARATIVE_UNRESOLVED')
 from source_property366 import evaluate as property366
 from comparison_metrics import rectangle_union_area
 draft=property366(r)
 current_area=rectangle_union_area(record['candidate']['model']['common_spaces']['lobby'])
 if current_area!=rectangle_union_area(r['candidate']['model']['common_spaces']['lobby']):raise ValueError('BALANCED_COMMON_AREA_PROPERTY_REBIND')
 draft={**draft,'current_model_digest':digest(record['candidate']['model']),'current':str(current_area),'binding_note':'Same exact measured common area as proof current367, so strictly larger fixed366 lobby coordinate refutes dominance of this balanced model too.'}
 return {'schema':'BALANCED365_EXPANDED_COHORT367','record_digest':digest(record),'fresh_result_digest':digest(review),'model_digest':digest(record['candidate']['model']),'original_bound_receipt':old,'new367_record_digest':digest(r),'new367_fresh_digest':digest(f),'new367_group_digest':digest(gate),'new367_intrinsic':own,'new367_comparison':pair,'draft366_property':draft,'remaining':remaining,'verdict':'UNKNOWN'if remaining else'PASS_SCOPED_FINITE_Q04_BALANCED365_EXPANDED367','accepted':False,'new_fresh_execution':False,'scope':'New versioned receipt, not retroactive alteration of old domain. Both models have common-route tradeoffs.'}
