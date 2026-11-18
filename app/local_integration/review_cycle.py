"""Trusted in-process fresh-review decision. Not a caller-authority verifier.
No repair is registered for constructor129. Controlled372 is not compatible.
"""
import hashlib
import json

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def decide(candidate, request_digest, source_revision, repair_receipt=None):
    model_hash=digest(candidate['model']); review=candidate['physical_review']
    origin=review.get('hierarchical_provenance129',{})
    if candidate.get('model_digest')!=model_hash or review.get('model_hash')!=model_hash or origin.get('model_hash')!=model_hash:
        raise ValueError('CURRENT_REVIEW_MODEL_BINDING')
    if origin.get('verified') is not True or origin.get('source_revision')!=source_revision or origin.get('errors')!=[] or origin.get('pending')!=[]:
        raise ValueError('CURRENT_RECONSTRUCTION_PROOF_REQUIRED')
    if any(candidate.get(k) is not False for k in ('accepted','delivery_allowed','qualified')):
        raise ValueError('UNAUTHORIZED_ACCEPTANCE')
    errors=review.get('errors'); pending=review.get('pending')
    if type(errors)is not list or type(pending)is not list:raise ValueError('REVIEW_SHAPE')
    if errors:
        if review.get('status')!='FAIL':raise ValueError('CONTRADICTORY_REVIEW_STATUS')
        state='REJECTED_PHYSICAL'; reason='NO_REGISTERED_PARAMETRIC_REPAIR_OPERATOR'
    elif pending:state='UNKNOWN_REVIEW'; reason='PENDING_NOT_REPAIR_AUTHORITY'
    elif review.get('status')=='PASS_CONCEPT_SCOPED_REVIEW':
        state='PHYSICAL_PASS_SEMANTIC_UNKNOWN'; reason='NO_CURRENT_PHYSICAL_REJECTION'
    else:state='UNKNOWN_REVIEW'; reason='UNKNOWN_REVIEW_STATUS'
    result={'schema':'MAC_FRESH_REVIEW_DECISION_V1','candidate_id':candidate['candidate_id'],
      'request_digest':request_digest,'model_digest':model_hash,'review_digest':digest(review),
      'source_revision':source_revision,'state':state,'reason':reason,
      'errors':errors,'pending':pending,'repair_attempted':False,'operator_invoked':False,
      'accepted':False,'delivery_allowed':False,'qualified':False,
      'scope':'fresh same-process physical review only; no semantic or external authority'}
    if repair_receipt is not None:
        if repair_receipt.get('schema')!='MAC_PARAMETRIC_REPAIR_RECEIPT_V1' or repair_receipt.get('source_revision')!=source_revision or repair_receipt.get('accepted')is not False or repair_receipt.get('delivery_allowed')is not False:
            raise ValueError('REPAIR_RECEIPT_CONTRACT')
        expected=repair_receipt.get('child_model_digest') if repair_receipt.get('mechanics_success') else repair_receipt.get('parent_model_digest')
        if expected!=model_hash or type(repair_receipt.get('repair_attempted'))is not bool or repair_receipt.get('operator_invoked')is not repair_receipt['repair_attempted']:raise ValueError('REPAIR_RECEIPT_BINDING')
        result.update(repair_attempted=repair_receipt['repair_attempted'],operator_invoked=repair_receipt['operator_invoked'],repair_receipt_digest=digest(repair_receipt))
        if repair_receipt['repair_attempted']:result['reason']=repair_receipt['state']
    functional=candidate.get('functional_review')
    if functional is not None:
        if functional.get('schema')!='MAC_FUNCTIONAL_REVIEW_V1' or functional.get('model_digest')!=model_hash or functional.get('physical_review_digest')!=digest(review) or functional.get('source_revision')!=source_revision or any(functional.get(k)is not False for k in ('display_allowed','accepted','delivery_allowed','qualified')):
            raise ValueError('FUNCTIONAL_REVIEW_BINDING')
        result['functional_review_digest']=digest(functional)
        result['design_display_allowed']=False
    result['decision_id']=digest(result)
    return result
