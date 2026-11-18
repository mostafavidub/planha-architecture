"""Explicit program2 only. Default program3 is never silently replaced.
No automatic programme suitability or registered repair authority is claimed.
"""
import sys,time,json,hashlib,inspect
from pathlib import Path
from dimension_contract import InputError
from review_cycle import digest,decide
def run(body):
    from parametric_worker import ROOT,ENGINE,SCHEMA,prepare
    envelope,raw=prepare(body)
    if envelope['canonical_request'].get('program')!={'bedrooms_per_unit':2}:
        raise InputError('EXPLICIT_TWO_BEDROOM_PROGRAM_REQUIRED','program',409)
    from producer_provenance import snapshot,require_unchanged
    files=['app/local_integration/explicit_two_bedroom_worker.py','app/local_integration/parametric_worker.py','app/local_integration/review_cycle.py','app/local_integration/functional_review.py','app/local_integration/guest_four_route_diagnostic.py','app/local_integration/living_connectivity_diagnostic.py']
    sources=snapshot(ROOT,files)
    sys.path[:0]=[str(ROOT/'frontend'),str(ENGINE)]
    from guard400 import guard
    freeze='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0';pins=guard(freeze)
    from engine114 import revision
    from constructor127 import frame,build,context
    from evaluate_pair127 import evaluate
    from search114 import propose
    if Path(inspect.getsourcefile(propose)).resolve()!=(ENGINE/'search114.py').resolve():raise ValueError('EXPLICIT_PRODUCER_IMPORT_PATH')
    before=revision();started=time.monotonic();candidates=[];attempts=[]
    family='FRONT_REAR';attempt={'family':family,'organization':'EXPLICIT_TWO_BEDROOM_SOURCE','not_global_infeasibility':True}
    attempts.append(attempt)
    try:
        core,_=frame(raw,family)
        p=propose(core,2,time_limit=3,variant=0,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES')
        attempt['proposal']=p
        if p.get('status')!='PROPOSAL_ONLY':attempt['state']=p.get('status','UNKNOWN_PROPOSAL')
        else:
            packet=build(raw,family,p,p);ctx=context(raw,packet,{'A':p,'B':p});review=evaluate(packet,ctx);model=packet['world_model'];mh=digest(model)
            if model['inputs']!=[raw['W'],raw['L'],2]:
                from fractions import Fraction as F
                if list(map(F,model['inputs'][:2]))!=[F(raw['W']),F(raw['L'])] or model['inputs'][2]!=2:raise ValueError('EXPLICIT_INPUT_BINDING')
            if ctx['construction_trace']['raw']!=raw or ctx['construction_trace']['proposals']!={'A':p,'B':p}:raise ValueError('EXPLICIT_PROPOSAL_BINDING')
            receipt={'schema':'V25_EXPLICIT_PROGRAM_PRODUCER_V1','source_files':sources,'request_digest':envelope['canonical_request_digest'],'initial_model_digest':mh,'proposal_digest':digest({'A':p,'B':p}),'context_digest':digest(ctx),'initial_review_digest':digest(review),'historical_engine_revision':before,'accepted':False,'delivery_allowed':False}
            receipt['receipt_digest']=digest(receipt)
            candidate={'family':family,'organization':'EXPLICIT_TWO_BEDROOM_SOURCE','model':model,'model_digest':mh,'generation_context':ctx,'physical_review':review,'initial_producer_receipt':receipt,'producer_lineage':{'initial_model_digest':mh,'final_model_digest':mh,'repair_receipt_digest':None,'accepted':False,'delivery_allowed':False},'repair_capability':{'supported':False,'reason':'EXPLICIT_PAIR_REPAIR_NOT_REGISTERED'},'accepted':False,'delivery_allowed':False,'qualified':False}
            candidate['candidate_id']=digest({'request_digest':envelope['canonical_request_digest'],'model_digest':mh,'family':family,'explicit_program':2})
            from functional_review import assess
            candidate['functional_review']=assess(model,review,before)
            candidate['review_decision']=decide(candidate,envelope['canonical_request_digest'],before)
            candidates.append(candidate);attempt['state']='CONSTRUCTED_AND_FRESHLY_REVIEWED_EXPLICIT_PROGRAM'
    except ValueError as e:
        attempt.update(state='UNSUPPORTED_CURRENT_CORE_FIT' if str(e) in ('FRONT_REAR_SCOPE_NO_CORE','OUTSIDE_CURRENT_COMMON_INTERFACE_METHOD_NOT_GLOBAL_INFEASIBILITY') else 'EXECUTION_ERROR',reason=str(e))
    attempts.append({'family':'LEFT_RIGHT','state':'UNSUPPORTED_CURRENT_SOURCE_RECORD_SCHEMA','reason':'Known source schema mismatch; not global geometric infeasibility'})
    require_unchanged(ROOT,sources)
    if revision()!=before or guard(freeze)!=pins:raise ValueError('SOURCE_CHANGED')
    from diversity_review import audit
    diversity=audit(candidates,envelope['canonical_request_digest'],before)
    return {'schema':SCHEMA,'outcome':'EXPERIMENT_COMPLETED','envelope':envelope,'engine_raw_request':raw,'engine_source_revision':before,'historical_pins':pins,'producer_sources':sources,'attempts':attempts,'candidates':candidates,'generated_count':len(candidates),'qualified_count':0,'requested_count':raw['requested_count'],'qualified_shortfall':raw['requested_count'],'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'elapsed_seconds':time.monotonic()-started,'diversity_report':diversity,'diversity_report_digest':digest(diversity),'program_policy':{'bedrooms_per_unit':2,'sleep_roles':['double','twin'],'source':'explicit request; existing source127/114','capacity_suitability':'NOT_VERIFIED','automatic_program_selection':False,'fallback_from_three_bedrooms':False,'registered_repair':False},'scope':'One explicit two-bedroom FRONT_REAR attempt only. No n1, automatic selection, full domain coverage, natural production repair, design display or architectural qualification.'}
