"""Independent new-origin study evaluator, never production admission.
Runs original physical assertions, all named requirements and current functional
diagnostics afresh. Historical registry coverage is not full current PRD closure.
"""
from pathlib import Path
from copy import deepcopy
import inspect,importlib
from contract114 import digest
from open_front_kitchen_study import ROOT,ENGINE

LOCAL_MODULES=[
 'open_front_evaluator','open_front_world_origin','open_front_world_assembly',
 'open_front_kitchen_study','open_front_kitchen_check','open_front_kitchen_place',
 'open_front_placement_check','open_front_typed_public','open_front_operation_check',
 'open_front_raw_physical','open_front_rule_contract','open_front_named_checks',
 'open_front_circulation_scope','open_front_circulation_integrity','open_front_circulation_frame','open_front_q11_pending',
 'open_front_boundary_comparison','functional_review','guest_four_route_diagnostic',
 'living_connectivity_diagnostic','kitchen_guest_review','producer_provenance',
 'review_cycle']
CURRENT_REQUIRED={'CURRENT_PROGRAM_SUITABILITY','KITCHEN_GUEST_PATH_SEPARATION',
 'CONTINUOUS_USEFUL_LIVING','NONFUNCTIONAL_WALL_EXCLUSION'}

def bindings():
    from producer_provenance import snapshot
    for name in LOCAL_MODULES:
        module=importlib.import_module(name)
        if Path(module.__file__).resolve()!=Path(__file__).with_name(name+'.py').resolve():
            raise ValueError('STUDY_EVALUATOR_IMPORT_PATH:'+name)
    return snapshot(ROOT,['app/local_integration/'+n+'.py' for n in LOCAL_MODULES])

def assess(packet,trace,baseline_packet,baseline_context):
    from guard400 import guard
    from explicit_pair_redirection import FREEZE
    from engine114 import revision
    from producer_provenance import require_unchanged
    from open_front_world_origin import verify
    from open_front_raw_physical import assess as raw_assess
    from open_front_rule_contract import evaluate_rule_contract
    from open_front_named_checks import adapters_for_study,APPLICABILITY_ADAPTERS
    from open_front_boundary_comparison import assess as boundary_assess
    from functional_review import assess as functional_assess
    if guard(FREEZE)!=12991:raise ValueError('FROZEN_GUARD')
    sources=bindings();rev=revision()
    before=digest([packet,trace,baseline_packet,baseline_context])
    origin=verify(packet,trace)
    m=packet['world_model'];model_digest=digest(m)
    raw=raw_assess(deepcopy(m))
    if raw.get('model_hash')!=model_digest:raise ValueError('RAW_MODEL_BINDING')
    # Context deliberately has no historical construction trace. New replay was
    # independently established above; no constructor127/frame148 identity fake.
    named=evaluate_rule_contract(m,
        trusted_evaluators=adapters_for_study(packet,trace,baseline_packet,baseline_context),
        context={'stage':'concept_internal','batch_models':[m]},
        applicability_evaluators=APPLICABILITY_ADAPTERS)
    if named.get('model_hash')!=model_digest:raise ValueError('NAMED_MODEL_BINDING')
    boundary=boundary_assess(packet,trace,baseline_packet,baseline_context)
    if boundary.get('model_digest')!=model_digest:raise ValueError('BOUNDARY_MODEL_BINDING')
    functional=functional_assess(m,raw,rev)
    if functional.get('model_digest')!=model_digest:raise ValueError('FUNCTIONAL_MODEL_BINDING')
    current={r['id']:r for r in functional['requirements']}
    if not CURRENT_REQUIRED<=set(current):raise ValueError('CURRENT_REQUIRED_INVENTORY')
    errors=list(raw['errors'])+list(named['errors'])+list(boundary['errors'])
    pending=list(raw['pending'])+list(named['pending'])+list(boundary['pending'])
    for rid,row in current.items():
        if row['state'] in ('FAIL','REJECTED_FUNCTIONAL'):
            errors.append({'code':'CURRENT_FUNCTIONAL_FAILED','requirement_id':rid})
        elif row['state'] not in ('PASS','PASS_SCOPED'):
            pending.append('CURRENT_FUNCTIONAL_UNKNOWN:'+rid)
    # Scoped boundary comparison does not certify full current Q11.
    if boundary.get('current_Q11_complete') is not True:
        pending.append('CURRENT_Q11_FULL_FUNCTIONAL_BOUNDARY_NOT_CLOSED')
    if digest([packet,trace,baseline_packet,baseline_context])!=before:
        raise ValueError('STUDY_EVALUATOR_INPUT_MUTATED')
    if bindings()!=sources:raise ValueError('STUDY_EVALUATOR_IMPORT_OR_SOURCE_CHANGED')
    require_unchanged(ROOT,sources)
    if revision()!=rev or guard(FREEZE)!=12991:raise ValueError('FROZEN_SOURCE_CHANGED')
    return {'schema':'OPEN_FRONT_INDEPENDENT_EVALUATOR_STUDY_V1',
        'model_digest':model_digest,'input_bundle_digest':before,
        'origin':origin,'raw_physical':raw,'named_contract':named,
        'boundary_comparison':boundary,'current_functional':functional,
        'source_snapshot':sources,'frozen_revision':rev,
        'errors':errors,'pending':sorted(set(pending)),
        'status':'FAIL_STUDY' if errors else 'UNKNOWN_REQUIRED_STUDY',
        'whole_physical_verified':False,'qualified':False,'accepted':False,
        'display_allowed':False,'delivery_allowed':False,
        'eligible_for_draft_export':False,'all_rules_approved':False,
        'scope':'Independent study source and fresh physical/named/current checks. No production integration, historical identity, pending reduction, functional closure, or delivery authority.'}
