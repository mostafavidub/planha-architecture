"""Audited conditional write-set invariant, not execution or eligibility of366."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from comparison_metrics import digest,rectangle_union_area
ROOT=Path(__file__).resolve().parents[1]
PROOF_SHA='952bf269832691f5ed25063ba3b9df44a2044e02dbf064a55706d8e980b7d7ae'
def evaluate(record):
 p=ROOT/'review366_common_source_lemma/result.json'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=PROOF_SHA:raise ValueError('366_PROOF_CHANGED')
 x=json.loads(p.read_text())
 for name,h in x['source_readset'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('366_SOURCE_CHANGED:'+name)
 base=ROOT/'staging365_service_grammar/candidate365.json';current=ROOT/'review367_joint_attempt2/actual367.json'
 if hashlib.sha256(base.read_bytes()).hexdigest()!=x['baseline_record_sha256']or hashlib.sha256(current.read_bytes()).hexdigest()!=x['current_record_sha256']:raise ValueError('366_PROOF_RECORD_CHANGED')
 if digest(json.loads(current.read_text()))!=digest(record):raise ValueError('366_PROOF_CURRENT_BINDING')
 a=rectangle_union_area(json.loads(base.read_text())['candidate']['model']['common_spaces']['lobby']);b=rectangle_union_area(record['candidate']['model']['common_spaces']['lobby'])
 if a<=b or a!=F(x['areas']['baseline_lobby_area_m2'])or b!=F(x['areas']['current367_lobby_area_m2']):raise ValueError('366_COUNTEREXAMPLE_NOT_VALID')
 return {'id':'balanced_only366','status':'UNASSESSED_NO_BUILD_NO_FRESH','eligibility':'UNKNOWN','conditional_dominance':'FALSE_FOR_SUCCESSFUL_FIXED_SOURCE_PATH','metric':'COMMON/lobby_floor_m2','current':str(b),'alternative_if_success':str(a),'worse_by':str(a-b),'source_proof':x,'proof_sha256':PROOF_SHA,'not_invalid_or_infeasible':True}
