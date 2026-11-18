"""Conservative full-report comparison; never grants semantic qualification."""
from collections import Counter
from operator371 import digest,protected,rect,overlap

def witness_delta(old,new):
    differences={}
    for field in ('errors','pending','original_pending','not_evaluated'):
        a=Counter(map(digest,old.get(field,[])));b=Counter(map(digest,new.get(field,[])))
        differences[field]=list((b-a).elements())
    return differences

def compare(parent,before,plan,child,after,lineage):
    if plan['before_raw_digest']!=digest(before['raw_report']) or plan['before_raw_report']!=before['raw_report']:
        raise ValueError('BEFORE_EVIDENCE_CHANGED')
    if (after.get('fresh_checker_executed') is not True or not after.get('source_unchanged')
        or after['input_record_digest']!=digest(child) or after['model_digest']!=digest(child['candidate']['model'])
        or after['raw_report']['model_hash']!=after['model_digest']
        or after['review_id']==before['review_id'] or after['model_digest']==before['model_digest']
        or not after['expected_method_registry']['built_before_evaluate'] or not after['provenance']['verified']
        or after['provenance']['input_record_digest']!=digest(child)
        or after['provenance']['model_hash']!=after['model_digest']):
        raise ValueError('FRESH_CHILD_BINDING')
    if (child.get('test_only') is not True or after.get('test_only') is not True
        or lineage.get('parent_fresh_digest')!=digest(before)
        or lineage.get('parent_review_id')!=before['review_id']):
        raise ValueError('PARENT_REVIEW_OR_TEST_SCOPE')
    if protected(parent)!=protected(child) or lineage['record_digest']!=digest(child) or lineage['model_digest']!=after['model_digest']:
        raise ValueError('CHILD_PRESERVATION_OR_LINEAGE')
    pair=plan['operator']['pair'];m=child['candidate']['model'];still=[]
    for i,u in enumerate(m['units']):
        if overlap(rect(u['fixtures'][pair[0]]),rect(u['fixtures'][pair[1]])):still.append(u['id'])
        for v in m['units'][i+1:]:
            for a,b in (pair,pair[::-1]):
                if overlap(rect(u['fixtures'][a]),rect(v['fixtures'][b])):still.append(u['id']+'/'+v['id'])
    # Exact error objects, including nested witnesses. Changed witnesses count as
    # unproven regression, even if a future specialized comparison might show improvement.
    old=before['raw_report'];new=after['raw_report'];differences=witness_delta(old,new)
    no_regression=not any(differences.values())
    return {'schema':'371_CONSERVATIVE_REPAIR_COMPARISON','collision_resolved':not still,
      'remaining_collision_units':still,'no_new_or_changed_error_or_unknown_witness':no_regression,
      'new_or_changed_witness_digests':differences,'before_report_digest':digest(old),'after_report_digest':digest(new),
      'before_errors':old['errors'],'before_pending':old['pending'],
      'before_original_pending':old.get('original_pending',[]),'before_not_evaluated':old.get('not_evaluated',[]),
      'after_raw_status':new['status'],'mechanics_success':not still and no_regression,
      'semantic_qualification':'UNKNOWN_NEW_GEOMETRY_NOT_REPROVEN','test_only':True,
      'accepted':False,'delivery_allowed':False}
