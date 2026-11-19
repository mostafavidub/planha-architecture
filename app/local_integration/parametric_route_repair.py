"""Finite source translations for a witnessed missing seating body route.
Search checkpoints are engineering budgets, never architectural standards.
Works in constructor129 local coordinates before LEFT_RIGHT world transform.
"""
import copy,time
from parametric_repair import rect,moved,contains,overlap,source_key,protected,PUBLIC,F,digest

def propose_route(raw,family,proposal,packet,context,review,source_revision):
    from current_entry_boundary_x03 import check_raw_domain
    check_raw_domain(raw)
    from constructor129 import build
    if family not in ('FRONT_REAR','LEFT_RIGHT') or packet['family']!=family:raise ValueError('ROUTE_REPAIR_FRAME')
    if proposal.get('generation_method')!='COARSE_BUNDLE_MILP_NOT_FULL_NETWORK_SOLVER':raise ValueError('ROUTE_REPAIR_SOURCE_FAMILY')
    model=packet['world_model'];mh=digest(model);trace=context['construction_trace'];proof=review.get('hierarchical_provenance129',{})
    if trace['raw']!=raw or trace['proposal']!=proposal or trace['model_hash']!=mh or trace['core_hash']!=digest(packet['core']) or trace['local_model_hash']!=digest(packet['local_model']) or review.get('model_hash')!=mh:raise ValueError('ROUTE_PARENT_BINDING')
    if proof.get('verified')is not True or proof.get('model_hash')!=mh or proof.get('source_revision')!=source_revision:raise ValueError('ROUTE_FRESH_PROOF_REQUIRED')
    if review.get('status')!='FAIL' or review.get('pending')!=[]:raise ValueError('ROUTE_UNAMBIGUOUS_FAIL_REQUIRED')
    errors=review.get('errors',[])
    if any(isinstance(e,dict)and e.get('code')=='FIXTURE_COLLISION'for e in errors):raise ValueError('COLLISION_NOT_ROUTE_ONLY')
    reports=[e for e in errors if isinstance(e,dict)and e.get('code')=='MISSING_REQUIRED_ACTIVITY_ROUTES']
    targets={f.get('route','')[:-6]for e in reports for f in e.get('failures',[])if f.get('route','').endswith('_front')and f.get('reason')=='NO_CONNECTED_BODY_ROUTE'}
    if len(targets)!=1 or not targets<=PUBLIC:raise ValueError('SINGLE_SEATING_ROUTE_REQUIRED')
    fid=next(iter(targets));target=fid+'_front';key=source_key(fid)
    if not any(f.get('route')==target and f.get('reason')=='NO_CONNECTED_BODY_ROUTE'for f in model.get('route_failures',[])):raise ValueError('ACTUAL_ROUTE_FAILURE_REQUIRED')
    unit=next(u for u in packet['local_model']['units']if u['id']=='A');q=rect(proposal['rectangles'][key]);fx=rect(unit['fixtures'][fid]);ac=rect(unit['activities'][target])
    if q!=(min(fx[0],ac[0]),min(fx[1],ac[1]),max(fx[2],ac[2]),max(fx[3],ac[3])):raise ValueError('LOCAL_SOURCE_COMPOUND_BINDING')
    owners=list(map(rect,unit['ownership']));options=set()
    for k,v in proposal['rectangles'].items():
        if k==key:continue
        o=rect(v)
        for dx,dy in ((o[0]-q[2],F(0)),(o[2]-q[0],F(0)),(F(0),o[1]-q[3]),(F(0),o[3]-q[1])):
            t=moved(q,dx,dy)
            if not(dx or dy)or abs(dx)+abs(dy)>4 or not contains(t,owners):continue
            if any(overlap(t,rect(w))for n,w in proposal['rectangles'].items()if n!=key):continue
            options.add((abs(dx)+abs(dy),dx,dy,t))
    tried=[];started=time.monotonic();snapshot=digest([raw,proposal,packet,context,review]);protect=digest(protected(packet,fid))
    for _,dx,dy,t in sorted(options)[:8]:
        if time.monotonic()-started>60:break
        p=copy.deepcopy(proposal);p['rectangles'][key]=list(map(str,t))
        for name in ('solver_status','solver_message','variables','constraints','seconds'):p.pop(name,None)
        p.update(status='PROPOSAL_ONLY',generation_method='EXACT_PARAMETRIC_ROUTE_ESCAPE_V1',solver_used=False)
        child=build(raw,family,p)
        failures=[f for f in child['world_model'].get('route_failures',[])if f.get('route')in(target,'guest_living')]
        same=protected(child,fid)==protected(packet,fid)
        tried.append({'dx':str(dx),'dy':str(dy),'producer_route_failures':len(failures),'protected_unchanged':same})
        if not failures and same:
            plan={'state':'RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED','proposal':p,'parent_proposal_digest':digest(proposal),'parent_model_digest':mh,'parent_review_digest':digest(review),'source_revision':source_revision,'raw_digest':digest(raw),'protected_digest':protect,'operator':{'name':'FINITE_SOURCE_SEATING_ROUTE_ESCAPE_V1','fixture_id':fid,'source_key':key,'dx':str(dx),'dy':str(dy),'coordinate_frame':'CONSTRUCTOR129_LOCAL_BEFORE_WORLD_TRANSFORM','family':family,'search_budget_not_physical_rule_m':4},'producer_prefilter_only':True,'tried':tried,'candidate_limit':8,'start_checkpoint_seconds':60,'accepted':False,'delivery_allowed':False}
            plan['plan_digest']=digest(plan)
            if digest([raw,proposal,packet,context,review])!=snapshot:raise ValueError('ROUTE_PARENT_MUTATED')
            return plan
    return {'state':'UNSUPPORTED_ROUTE_REPAIR_FINITE_SEARCH_EXHAUSTED','repair_attempted':False,'tried':tried,'accepted':False,'delivery_allowed':False}
