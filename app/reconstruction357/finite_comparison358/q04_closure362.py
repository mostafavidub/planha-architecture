"""Current-source362 bound Q04 evidence; admission awaits domain audit.
Engineering policy v362 adds actual common-lobby floor cost explicitly. This
extension is declared after seeing the core-notch result, not preregistered or
recovered from a missing helper. It follows Q04 common-circulation cost scope.
It is not a functional-purpose test or global optimization certificate.
"""
from q04_measurement362 import *
import eligibility_intrinsic362 as eligibility
from circulation_role362 import evaluate as role_review
from q04_closure359 import purpose_complete
import hashlib

def evaluate(record,review):
 before=digest([record,review]);measurement=build()
 if digest(record)!=measurement['record_digest'] or digest(record['candidate']['model'])!=review['model_digest']:raise ValueError('CURRENT362_RECORD_REVIEW')
 gate=eligibility.evaluate(record,review,seconds=30)
 role=role_review(record,review)
 if role['model_hash']!=review['model_digest']or role['review_digest']!=digest(review):raise ValueError('CURRENT362_ROLE_BINDING')
 roleok=purpose_complete(role)
 objectives=all(r['comparison']['dominance']=='FALSE'for r in measurement['comparisons'])
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATED')
 reasons=[]
 if gate.get('verdict')!='PASS'or not gate.get('eligible'):reasons.append('CURRENT362_INTRINSIC_NOT_PASS')
 if not roleok:reasons.append('CURRENT362_CIRCULATION_PURPOSE_NOT_COMPLETE')
 if not objectives:reasons.append('UNRESOLVED_CONSTRUCTED_ALTERNATIVE')
 if not measurement['branches']['branch_enumeration_closed']:reasons.append('UNRESOLVED_ACTIVE_SOURCE_BRANCH')
 reasons.append('CURRENT362_COMMON_CIRCULATION_WHOLE_FUNCTION_PROOF_NOT_BOUND')
 reasons.append('INDEPENDENT_FINITE_DOMAIN_AND_COMMON_COST_POLICY_AUDIT_PENDING')
 return {'schema':'Q04_CURRENT362_BOUND_CLOSURE_AUDIT_PENDING','model_digest':review['model_digest'],'record_digest':digest(record),'fresh_result_digest':digest(review),'current_gate':gate,'current_gate_evaluator_sha256':hashlib.sha256((ROOT/'semantic_rules357/eligibility_intrinsic362.py').read_bytes()).hexdigest(),'purpose':role,'current_private_and_entry_purpose_complete':roleok,'negative_objectives_complete':objectives,'measurement':measurement,'verdict':'UNKNOWN','remaining':reasons,'engineering_policy_version':'Q04_COMPONENTWISE_REQUIRED_PATH_UNIT_CIRCULATION_PLUS_COMMON_LOBBY_V362','policy_change_timing':'Explicit new engineering scope after current core-notch outcome; not pre-registered and not claimed recovered authoritative helper','common_purpose_not_inferred_from_area':True,'global_optimum':False,'accepted':False,'delivery_allowed':False,'new_fresh_execution':False}
if __name__=='__main__':
 r=json.loads((ROOT/'staging362_core_notch/actual362.json').read_text());f=json.loads((ROOT/'review362_source_validation/result.json').read_text());x=evaluate(r,f);Path(__file__).with_name('q04_closure_actual362.json').write_text(json.dumps(x,ensure_ascii=False,indent=2));print(x['remaining'])
