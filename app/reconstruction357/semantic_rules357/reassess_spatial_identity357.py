"""Registered artifact reassessment; no fresh checker or solver execution."""
import json
from pathlib import Path
import common
from common import digest
from group_readsets357 import build
from support_review import evaluate as support
from wall_purpose import evaluate as walls
ROOT=Path(__file__).resolve().parents[1]
def evaluate(record,review):
 before=digest([record,review]);views=build(record,review,source_profile='SOURCE_IDENTITY357');old=common.REGISTRY_NAME
 try:
  common.REGISTRY_NAME='method_registry_identity357.json'
  s=support(views['envelope'],views['result'],views['groups']);w=walls(views['envelope'],views['result'],record)
 finally:common.REGISTRY_NAME=old
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'schema':'SPATIAL_IDENTITY357_ARTIFACT_REASSESSMENT','record_digest':digest(record),'raw_review_digest':digest(review),'model_hash':digest(record['candidate']['model']),'support':s,'wall_purpose':w,'new_fresh_execution':False,'live_authority':False,'parent_complete':False,'admission_allowed':False}
if __name__=='__main__':
 record=json.loads((ROOT/'staging357_comparative/attached_service_final357.json').read_text());review=json.loads((ROOT/'review357_source_identity/result.json').read_text());o=evaluate(record,review);Path(__file__).with_name('spatial_identity_reassessment_actual357.json').write_text(json.dumps(o,indent=2));print(o['model_hash'],[(r['unit'],r['unresolved_area_m2'])for r in o['support']['rows']],o['wall_purpose'].get('counts'))
