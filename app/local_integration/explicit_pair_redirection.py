"""Bounded explicit-pair exploratory redirection, never constructor129 repair.
Only a freshly reconstructed, narrowly classified natural route rejection permits search.
Pending rules remain evidence, never authority. No display/delivery/qualification.
"""
import copy,inspect,time
from pathlib import Path
from review_cycle import digest
FREEZE='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
PENDING={'RULE_NOT_EVALUATED:'+x for x in ('circulation_functional_integrity','guest_dining_route','guest_living_route','private_grouping','program_functional_roles','serving_route')}
def require_rejection(review):
    errors=review.get('errors');pending=review.get('pending')
    if review.get('status')!='FAIL' or type(errors)is not list or len(errors)!=1 or type(pending)is not list:
        raise ValueError('FRESH_NATURAL_ROUTE_REJECTION_REQUIRED')
    e=errors[0]
    if e.get('code')!='MISSING_REQUIRED_ACTIVITY_ROUTES' or set(e)!={'code','failures'}:
        raise ValueError('REJECTION_OUTSIDE_EXPLORATORY_SCOPE')
    failures=e['failures']
    expected=[{'unit':u,'route':'guest_dining','reason':'NO_CONNECTED_BODY_ROUTE','profile':'public_all_seat_motion_occupied_and_kitchen_exclusion'} for u in ('A','B')]
    if failures!=expected or any(type(p)is not str for p in pending) or not set(pending)<=PENDING:
        raise ValueError('REJECTION_OUTSIDE_EXPLORATORY_SCOPE')
def inventory(model):
    # Protect exact fixture IDs as well as types and source sizes, not only counts.
    from fractions import Fraction as F
    inventory={}
    for u in model['units']:
        records={}
        if set(u['fixtures'])!=set(u['fixture_metadata']):raise ValueError('FIXTURE_METADATA_INVENTORY')
        for k,v in u['fixture_metadata'].items():
            q=list(map(lambda x:F(str(x)),u['fixtures'][k]))
            dims=sorted((q[2]-q[0],q[3]-q[1]))
            if dims[0]<=0:raise ValueError('FIXTURE_GEOMETRY')
            records[k]={'kind':v.get('kind'),'source_size_m':v.get('source_size_m'),'actual_dimensions_m':list(map(str,dims))}
        inventory[u['id']]=records
    return inventory
def redirect(body,parent_model,parent_context):
    from parametric_worker import ROOT,ENGINE,prepare
    envelope,raw=prepare(body)
    if envelope['canonical_request'].get('program')!={'bedrooms_per_unit':2}:raise ValueError('EXPLICIT_TWO_BEDROOM_PROGRAM_REQUIRED')
    from producer_provenance import snapshot,require_unchanged
    import sys
    sys.path[:0]=[str(ROOT/'frontend'),str(ENGINE)]
    from guard400 import guard
    from engine114 import revision
    from constructor127 import frame,build,context
    from evaluate_pair127 import evaluate
    sys.path.insert(0,str(ROOT/'app/local_integration/candidate'))
    from four_seat_group_candidate import propose
    for fn,name in [(frame,'constructor127.py'),(build,'constructor127.py'),(context,'constructor127.py'),(evaluate,'evaluate_pair127.py')]:
        if Path(inspect.getsourcefile(fn)).resolve()!=(ENGINE/name).resolve():raise ValueError('EXPLORATORY_IMPORT_PATH')
    if Path(inspect.getsourcefile(propose)).resolve()!=(ROOT/'app/local_integration/candidate/four_seat_group_candidate.py').resolve():raise ValueError('GROUPED_PRODUCER_IMPORT_PATH')
    sources=snapshot(ROOT,['app/local_integration/candidate/four_seat_group_candidate.py','app/local_integration/explicit_pair_redirection.py','app/local_integration/parametric_worker.py','app/local_integration/dimension_contract.py','app/local_integration/review_cycle.py'])
    before=revision();pins=guard(FREEZE)
    if pins!=12991:raise ValueError('HISTORICAL_GUARD_COUNT')
    trace=parent_context.get('construction_trace',{})
    if trace.get('schema')!='CONSTRUCTION_TRACE127_PAIR_V1' or trace.get('raw')!=raw or trace.get('source_revision')!=before or trace.get('model_hash')!=digest(parent_model):
        raise ValueError('EXPLORATORY_PARENT_BINDING')
    ps=trace.get('proposals',{})
    if set(ps)!={'A','B'} or any(p.get('bedrooms')!=2 or p.get('sleep_roles')!=['double','twin'] for p in ps.values()):raise ValueError('EXPLICIT_PROGRAM_CHANGED')
    family='FRONT_REAR'
    packet=build(raw,family,copy.deepcopy(ps['A']),copy.deepcopy(ps['B']))
    fresh_context=context(raw,packet,copy.deepcopy(ps))
    if digest(packet['world_model'])!=digest(parent_model) or digest(fresh_context)!=digest(parent_context):raise ValueError('EXPLORATORY_PARENT_REPLAY')
    fresh=evaluate(packet,fresh_context)
    origin=fresh.get('multiproposal_provenance127',{})
    if origin.get('verified')is not True or origin.get('model_hash')!=digest(parent_model) or origin.get('source_revision')!=before or origin.get('errors')!=[] or origin.get('pending')!=[]:raise ValueError('EXPLORATORY_PARENT_PROVENANCE')
    require_rejection(fresh)
    started=time.monotonic();core,_=frame(raw,family);protected=inventory(parent_model)
    result={'schema':'V25_EXPLICIT_PAIR_REDIRECTION_V1','scope':'EXPLORATORY_ONLY_NOT_PRODUCTION_REPAIR','request_digest':envelope['canonical_request_digest'],'source_revision':before,'source_files':sources,'parent_model_digest':digest(parent_model),'parent_context_digest':digest(parent_context),'fresh_parent_review':fresh,'parent_pending_preserved':copy.deepcopy(fresh['pending']),'search_strategy':'SOURCE_BOUND_GROUPED_GUEST_MOTION_V1','attempts':[],'child':None,'accepted':False,'delivery_allowed':False,'qualified':False,'display_allowed':False,'production_repair_registered':False}
    for variant in (0,1,2):
        if time.monotonic()-started>100:break
        p=propose(core,2,time_limit=12,variant=variant,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES')
        attempt={'variant':variant,'proposal':p};result['attempts'].append(attempt)
        if p.get('status')!='PROPOSAL_ONLY':continue
        child_packet=build(raw,family,p,p);child_context=context(raw,child_packet,{'A':p,'B':p});model=child_packet['world_model']
        if inventory(model)!=protected or model['inputs']!=parent_model['inputs'] or model.get('profile')!=parent_model.get('profile') or digest(child_packet['core'])!=digest(packet['core']):raise ValueError('EXPLORATORY_PROTECTED_PROGRAM_CHANGED')
        review=evaluate(child_packet,child_context)
        attempt.update(model_digest=digest(model),review=review)
        if review.get('status')=='PASS_CONCEPT_SCOPED_REVIEW' and review.get('errors')==[] and review.get('pending')==[] and digest(model)!=digest(parent_model):
            origin=review.get('multiproposal_provenance127',{})
            if origin.get('verified')is not True or origin.get('model_hash')!=digest(model) or origin.get('source_revision')!=before or origin.get('errors')!=[] or origin.get('pending')!=[]:raise ValueError('EXPLORATORY_CHILD_PROVENANCE')
            result['child']={'packet':child_packet,'context':child_context,'review':review,'model_digest':digest(model),'variant':variant}
            break
    require_unchanged(ROOT,sources)
    if revision()!=before or guard(FREEZE)!=pins:raise ValueError('EXPLORATORY_SOURCE_CHANGED')
    result['state']='FRESH_PHYSICAL_PASS_FUNCTIONAL_UNKNOWN' if result['child'] else 'BOUNDED_SEARCH_NO_FRESH_PASS'
    result['elapsed_seconds']=time.monotonic()-started
    result['receipt_digest']=digest(result)
    return result
