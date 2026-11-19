"""Source-cited automatic program SEARCH study, never public design admission.
No production worker, UI, historical schema or frozen engine is modified.
"""
import copy,json,sys,time,hashlib,inspect
from pathlib import Path
from public_wln_contract import parse_public,engine_raw
from dimension_contract import digest
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
DOC='https://docs.google.com/document/d/17X8Q5nsiFBmJqAodCQpIfewsDIUeP5eosc3D72ALi3s/edit'
FREEZE='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
ENGINE_PIN='faada6a8a1106adfe8a24a5f18dfdf6b550f20a6ecc93d81df6ec07d47a20d6a279'
# Internal runtime limits only. They are not architectural bounds or quality rules.
BUDGET={'solver_seconds_per_attempt':3,'max_attempts':4,'wall_seconds':90}
OPTIONS=(('FRONT_REAR','SIDE_ROOTED_SERVICES'),('FRONT_REAR','FRAME125_SERVICE_SIDE'),
         ('LEFT_RIGHT','SIDE_ROOTED_SERVICES'),('LEFT_RIGHT','FRAME125_SERVICE_SIDE'))
UNREADY=('UNENUMERATED_CORE_VARIANTS','UNENUMERATED_SPLIT_VARIANTS',
         'OPTIONAL_NONBED_MERGE_NOT_IMPLEMENTED','UNENUMERATED_PLACEMENT_VARIANTS')
def alternative(bedrooms):
    if bedrooms not in (1,2): raise ValueError('UNAPPROVED_PROGRAM_PROFILE')
    roles=['double'] if bedrooms==1 else ['double','twin']
    return {'alternative_id':'MVP_APPROVED_'+str(bedrooms)+'BED_'+str(2*bedrooms)+'DESIGN_PERSONS_V1',
      'bedrooms_per_unit':bedrooms,'sleep_roles':roles,'design_persons_per_unit':2*bedrooms,
      'capacity_is_actual_population':False,'unit_count':2,
      'bundle_required':['sleep','living_seating','dining','clothes_storage','activities','access'],
      'relations_required':['same_design_capacity_across_bundle','programme_locked_after_geometry'],
      'approval_source':{'url':DOC+'?tab=t.jgj9urck6sd','section':'A9','range':'41570-42072;43973-44545'},
      'limits_source':{'section':'AP05/AP06/A7','range':'38709-39357;40544-40834'},
      'numeric_quality_thresholds':None,'profile_status':'PROFILE_NOT_READY',
      'profile_missing':['SOURCE_BOUND_NET_CAPACITY_PREFILTER','CALIBRATED_ROOM_AND_UNIT_QUALITY_FLOORS','PARETO_QUALITY_ANCHORS'],
      'search_order_reason':'Two before one is bounded study enumeration, not quality preference or maximum-bedroom rule.'}

def reduction_transition(previous,next_alt,attempts):
    """No incomplete AP07 search or timeout is a reduction authorization."""
    if next_alt['bedrooms_per_unit']!=previous['bedrooms_per_unit']-1 or next_alt['bedrooms_per_unit']<1:
        raise ValueError('INVALID_PROGRAM_TRANSITION')
    return {'from_alternative':previous['alternative_id'],'to_alternative':next_alt['alternative_id'],
      'state':'BLOCKED_AP07_INCOMPLETE','authorized':False,'programme_repair':False,
      'attempted_ids':[a['attempt_id'] for a in attempts],
      'unattempted':list(UNREADY),'budget_is_infeasibility':False,
      'reason':'Available bounded core/split/placement sample is not exhaustive AP07; no automatic lower-bedroom fallback.'}

def _actual_inventory(model,alt):
    """Bind the observed bundle without claiming capacity suitability."""
    p=model['program']
    assert p['bedrooms_per_unit']==alt['bedrooms_per_unit'] and p['sleep_roles']==alt['sleep_roles']
    assert type(p['units']) is int and p['units']==alt['unit_count']
    assert p['design_occupants_per_unit']==alt['design_persons_per_unit']
    assert [u['id'] for u in model['units']]==['A','B']
    evidence=[]
    for u in model['units']:
        fx=u['fixtures'];ac=u['activities']
        expected_sleep=['bed1.bed','bed2.single1','bed2.single2']
        # Exact source names verified against source module below; no guessed new fixture.
        sleeping={k:v for k,v in fx.items() if k.startswith('bed')}
        evidence.append({'unit':u['id'],'sleep_and_clothes':sleeping,
          'living_fixture_ids':[k for k in fx if k.startswith(('sofa','armchair'))],
          'dining_fixture_ids':[k for k in fx if k.startswith('dining')],
          'activity_ids':sorted(ac),'fixture_digest':digest(fx),'activity_digest':digest(ac),
          'bundle_suitability':'NOT_VERIFIED'})
    return evidence

def live_attempt(raw,alt,option,seconds):
    """Existing frozen producer and full original evaluator, not default worker."""
    sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ENGINE)]
    from guard400 import guard
    from engine114 import revision
    from constructor127 import frame,build,context
    from search114 import propose
    from construction_replay127 import verify
    from evaluate_pair127 import evaluate
    from functional_review import assess
    from left_right_two_source_binding import canonical_json
    from producer_provenance import snapshot,require_unchanged
    pin=guard(FREEZE);assert pin==12991
    rev=revision()
    # Pin established by earlier source binding contract rather than copied alternative hash.
    from left_right_two_source_binding import ENGINE_PIN as PIN
    assert rev==PIN
    for fn,file in ((frame,'constructor127.py'),(build,'constructor127.py'),(context,'constructor127.py'),
                    (propose,'search114.py'),(verify,'construction_replay127.py'),(evaluate,'evaluate_pair127.py')):
        assert Path(inspect.getsourcefile(fn)).resolve()==(ENGINE/file).resolve()
    paths=['app/local_integration/'+x for x in ('automatic_program_search.py','public_wln_contract.py',
        'functional_review.py','left_right_two_source_binding.py','producer_provenance.py','dimension_contract.py')]
    sources=snapshot(ROOT,paths);before=digest([raw,alt]);family,topology=option
    reports={}
    try:
        core,_=frame(raw,family)
        proposal=propose(core,alt['bedrooms_per_unit'],sleep_roles=alt['sleep_roles'],
             topology=topology,time_limit=seconds,variant=0,ordered_macro=False,organization_profile='UNRESTRICTED')
        result={'proposal':proposal,'proposal_digest':digest(proposal),'state':proposal['status'],
          'accepted':False,'qualified':False,'delivery_allowed':False}
        if proposal['status']!='PROPOSAL_ONLY':return result
        assert proposal['bedrooms']==alt['bedrooms_per_unit'] and proposal['sleep_roles']==alt['sleep_roles']
        packet=build(raw,family,proposal,proposal);ctx=context(raw,packet,{'A':proposal,'B':proposal})
        # Same artifact transport boundary: tuples become JSON arrays, values unchanged.
        value_before=digest([packet,ctx]);packet,ctx=canonical_json([packet,ctx])
        assert digest([packet,ctx])==value_before
        model=packet['world_model'];mh=digest(model)
        from fractions import Fraction as F
        assert list(map(F,model['inputs'][:2]))==[F(raw['W']),F(raw['L'])] and model['inputs'][2]==raw['n']
        inventory=_actual_inventory(model,alt);frozen=digest([packet,ctx])
        replay=verify(model,ctx);reports['replay']=digest(replay)
        physical=evaluate(packet,ctx);reports['physical']=digest(physical)
        current=assess(model,physical,rev)
        assert digest(physical)==reports['physical']
        assert current['model_digest']==mh and current['physical_review_digest']==reports['physical']
        assert all(current[k] is False for k in ('accepted','qualified','display_allowed','delivery_allowed'))
        assert digest([packet,ctx])==frozen and digest(replay)==reports['replay']
        result.update(state='FRESH_MODEL_REVIEWED_NOT_QUALIFIED',packet=packet,context=ctx,replay=replay,
            physical_report=physical,current_report=current,report_digests={**reports,'current':digest(current)},
            model_digest=mh,actual_bundle_inventory=inventory,source_snapshot=sources,engine_revision=rev,
            producer_input_digest=before,programme_lock_digest=digest(alt))
        return result
    finally:
        assert digest([raw,alt])==before
        require_unchanged(ROOT,sources);assert revision()==rev and guard(FREEZE)==pin

def run(body,*,adapter=None,clock=None,budget=None):
    """Injected adapter/clock only for explicitly labelled unit tests, never HTTP."""
    envelope=parse_public(body);raw=engine_raw(envelope)
    clock=clock or time.monotonic;started=clock()
    limits=copy.deepcopy(BUDGET if budget is None else budget)
    if set(limits)!=set(BUDGET) or type(limits['max_attempts']) is not int or not 0<=limits['max_attempts']<=4:
        raise ValueError('INVALID_EXECUTION_BUDGET')
    if any(type(limits[k]) not in (int,float) or not 0<=limits[k]<=BUDGET[k] for k in ('solver_seconds_per_attempt','wall_seconds')):
        raise ValueError('INVALID_EXECUTION_BUDGET')
    execute=adapter or live_attempt;alts=[alternative(2),alternative(1)]
    out={'schema':'V25_AUTOMATIC_PROGRAM_SEARCH_V1','status':'AUTOMATIC_PROGRAM_SEARCH_SCOPED',
      'envelope':envelope,'engine_raw':raw,'internal_requested_count_reason':'One bounded engine witness per attempt; not public output count or six-plan promise.',
      'alternatives':alts,'attempts':[],'transitions':[],'execution_budget':limits,
      'search_mode':'SOURCE_CAPABILITY_STUDY_NOT_PROGRAM_SELECTION',
      'profile_status':'PROFILE_NOT_READY','selection_status':'BLOCKED_NO_CALIBRATED_QUALITY_PROFILE',
      'selected_alternative':None,'pareto_selected':[],'accepted':False,'qualified':False,
      'display_allowed':False,'delivery_allowed':False,'production_supported':False,
      'request_fulfilled':False,'global_infeasibility_proven':False,'test_adapter':adapter is not None,
      'ap07_complete':False,'unattempted_ap07':list(UNREADY),
      'scope':'Public contract and automatic bounded study enumeration only. No approved net-capacity prefilter or quality calibration, no lower-program fallback, no production admission.'}
    alt=alts[0];lock=digest(alt);rawlock=digest(raw)
    for index,option in enumerate(OPTIONS):
        row={'attempt_id':alt['alternative_id']+':'+str(index),'alternative_id':alt['alternative_id'],
             'programme_lock_digest':lock,'family':option[0],'topology':option[1],
             'public_request_digest':envelope['canonical_request_digest'],'raw_digest':rawlock,
             'stage':'AP07_SUPPORTED_CORE_SPLIT_PLACEMENT_SAMPLE','prefilter_status':'PROFILE_NOT_READY',
             'prefilter_bypassed_for_qualification':False,'execution_scope':'EXPLORATORY_PLACEMENT_ONLY',
             'accepted':False,'qualified':False,'delivery_allowed':False}
        out['attempts'].append(row)
        if index>=limits['max_attempts'] or clock()-started>=limits['wall_seconds'] or not limits['solver_seconds_per_attempt']:
            row.update(state='SEARCH_BUDGET_EXHAUSTED',attempted=False,global_infeasibility_proven=False);continue
        row['attempted']=True
        try:
            result=execute(copy.deepcopy(raw),copy.deepcopy(alt),option,limits['solver_seconds_per_attempt'])
            # Adapter cannot promote its result into admission.
            if any(result.get(k) is True for k in ('accepted','qualified','delivery_allowed','display_allowed')):
                raise ValueError('ADAPTER_AUTHORITY_ESCALATION')
            row['evidence']=result;row['state']=result['state']
            if 'programme_lock_digest' in result and result['programme_lock_digest']!=lock:
                raise ValueError('PROGRAMME_LOCK_CHANGED')
        except Exception as ex:row.update(state='ATTEMPT_FAILED_CLOSED',error={'type':type(ex).__name__,'detail':str(ex)})
        assert digest(raw)==rawlock and digest(alt)==lock
    out['transitions'].append(reduction_transition(alts[0],alts[1],out['attempts']))
    alts[1]['adapter_status']='NOT_IMPLEMENTED_IN_THIS_AUTOMATIC_RUNNER'
    alts[1]['skip_reason']='Approval is not readiness; single-bedroom full bundle adapter has not been independently audited. AP07 reduction also remains blocked.'
    out['elapsed_seconds']=clock()-started
    return out
