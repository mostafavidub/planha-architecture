"""One bounded source-repair attempt, invoked only after current physical FAIL.
No public endpoint, no review mutation, no cached PASS and no semantic authority.
"""
from collections import Counter
from parametric_repair import propose,verify_child,digest

def attempt(raw,family,proposal,packet,context,review,source_revision,*,test_only=False):
    from current_entry_boundary_x03 import check_raw_domain
    check_raw_domain(raw)
    from constructor129 import build,context as make_context
    from evaluate_hierarchical129 import evaluate
    from engine114 import revision
    if revision()!=source_revision:raise ValueError('REPAIR_SOURCE_REVISION_CHANGED')
    base={'schema':'MAC_PARAMETRIC_REPAIR_RECEIPT_V1','test_only':test_only,'natural_failure':not test_only,
      'parent_model_digest':digest(packet['world_model']),'parent_review_digest':digest(review),
      'source_revision':source_revision,'repair_attempted':False,'operator_invoked':False,
      'accepted':False,'delivery_allowed':False}
    try:plan=propose(raw,family,proposal,packet,context,review,source_revision,test_only=test_only)
    except ValueError as e:
        if str(e) in ('UNSUPPORTED_REPAIR_FRAME','DIRECT_COLLISION_REQUIRED') and not test_only:
            from parametric_route_repair import propose_route
            try:plan=propose_route(raw,family,proposal,packet,context,review,source_revision)
            except ValueError as route_error:
                return {'receipt':{**base,'state':'UNSUPPORTED_OR_INVALID_REPAIR_PRECONDITION','reason':str(route_error)},'replacement':None}
        else:return {'receipt':{**base,'state':'UNSUPPORTED_OR_INVALID_REPAIR_PRECONDITION','reason':str(e)},'replacement':None}
    if plan['state']!='RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED':return {'receipt':{**base,'state':plan['state']},'replacement':None}
    base.update(repair_attempted=True,operator_invoked=True,plan_digest=plan['plan_digest'],operator=plan['operator'])
    child=build(raw,family,plan['proposal']);ctx=make_context(raw,plan['proposal'],child);fresh=evaluate(child,ctx)
    lineage=verify_child(raw,packet,plan,child,fresh,ctx)
    delta={k:list((Counter(map(digest,fresh.get(k,[])))-Counter(map(digest,review.get(k,[])))).elements())for k in('errors','pending','original_pending','not_evaluated')}
    success=fresh.get('status')=='PASS_CONCEPT_SCOPED_REVIEW' and not fresh['errors'] and not fresh['pending'] and not any(delta.values())
    if revision()!=source_revision:raise ValueError('REPAIR_SOURCE_CHANGED_DURING_REVIEW')
    receipt={**base,**lineage,'state':'REPAIRED_PHYSICAL_SEMANTIC_UNKNOWN'if success else'REPAIR_REJECTED_OR_UNKNOWN','mechanics_success':success,'new_witness_digests':delta,'before_errors':len(review['errors']),'after_errors':len(fresh['errors']),'semantic_qualification':'UNKNOWN_NOT_EXECUTED'}
    # Preserve parent source/review and attempted child even if replacement rejected.
    evidence={'raw':raw,'family':family,'parent_proposal':proposal,'parent_model_digest':base['parent_model_digest'],'parent_review':review,'plan':plan,'child_context':ctx,'child_review':fresh,'lineage':lineage,'test_only':test_only}
    return {'receipt':receipt,'replacement':{'packet':child,'context':ctx,'review':fresh}if success else None,'evidence':evidence}
