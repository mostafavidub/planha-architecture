"""Registered artifact reassessment; no fresh checker or solver execution."""
import json
from pathlib import Path
import common
from common import digest
from group_readsets367 import build
from support_review_joint367 import evaluate as support
from wall_purpose_joint367 import evaluate as walls
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record,review):
 before=digest([record,review]);views=build(record,review,source_profile='SOURCE_JOINT367');old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_source367.json'
  s=support(views['envelope'],views['result'],views['groups']);w=walls(views['envelope'],views['result'],record)
 finally:common.REGISTRY_NAME=old
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'role_proof_scope':{'complete_source_sitting_prerequisite_recomputed':s.get('status')=='MEASURED_CURRENT_SOURCE_SUPPORT_NOT_FINAL_ROLE_APPROVAL','body_plus_source_instance_operation_extent':[{k:r[k]for k in('unit','public_domain_area_m2','body_plus_source_function_coverage_m2','unresolved_area_m2')}for r in s.get('rows',[])],'exclusive_circulation_necessity':'PENDING_Q04','wall_purpose_final':'PENDING_Q04_FOR_EIGHT_SOURCE_HALL_WALLS','whole_parent_pass':False},'schema':'SPATIAL_SOURCE_JOINT367_ARTIFACT_REASSESSMENT','record_digest':digest(record),'raw_review_digest':digest(review),'model_hash':digest(record['candidate']['model']),'support':s,'wall_purpose':w,'new_fresh_execution':False,'live_authority':False,'parent_complete':False,'admission_allowed':False}
if __name__=='__main__':
 record=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());review=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());o=evaluate(record,review);Path(__file__).with_name('spatial_reassessment_joint_actual367.json').write_text(json.dumps(o,indent=2));print(o['model_hash'],[(r['unit'],r['unresolved_area_m2'])for r in o['support']['rows']],o['wall_purpose'].get('counts'))
