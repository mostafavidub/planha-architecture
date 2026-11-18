"""Bounded integration of existing parametric source constructors on this Mac.
No historical 26x28 model is loaded as a geometry template. Source modules keep
physical sizes; solver places them for the actual request. This is experimental
construction and fresh physical review, NOT semantic qualification or delivery.
"""
import hashlib
import json
from pathlib import Path
import sys
import time
from fractions import Fraction
from dimension_contract import InputError, parse

SCHEMA='PLANHA_MAC_PARAMETRIC_EXPERIMENT_V1'
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'manifests/WORKTREE_STATE.json').is_file())
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
FAMILIES=(('ROW','FRONT_REAR','coarse_master129'),('ROW','LEFT_RIGHT','coarse_master129'))


def prepare(body):
    envelope=parse(body)
    request=envelope['canonical_request']
    if request['unit_count']!=2:
        raise InputError('UNSUPPORTED_UNIT_COUNT_CURRENT_PARAMETRIC_FAMILY', 'n',409)
    if not 1<=request['requested_count']<=12:
        raise InputError('UNSUPPORTED_OPTION_COUNT_CURRENT_ENGINE','requested_count',409)
    if request.get('program_present') and request.get('program')!={'bedrooms_per_unit':3}:
        raise InputError('UNSUPPORTED_CUSTOM_PROGRAM_NO_SILENT_FALLBACK','program',409)
    def decimal(axis):
        v=request['dimensions_m'][axis]
        # exact finite decimal input; avoid float and the historical fixed parser.
        from decimal import Decimal,localcontext
        with localcontext() as ctx:
            ctx.prec=140
            return format(Decimal(v['numerator'])/Decimal(v['denominator']),'f')
    raw={'W':decimal('W'),'L':decimal('L'),'n':2,'requested_count':request['requested_count']}
    return envelope,raw


def run(body):
    envelope,raw=prepare(body)
    sys.path.insert(0,str(ROOT/'frontend'))
    from guard400 import guard
    freeze='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
    pin_count=guard(freeze)
    sys.path.insert(0,str(ENGINE))
    from constructor129 import frame,build,context
    from evaluate_hierarchical129 import evaluate
    from engine114 import revision
    from contract114 import digest
    import importlib
    before=revision();started=time.monotonic();attempts=[];candidates=[]
    for organization,family,module_name in FAMILIES:
        attempt={'organization':organization,'family':family,'not_global_infeasibility':True}
        attempts.append(attempt)
        if len(candidates)>=raw['requested_count']:
            attempt['state']='NOT_ATTEMPTED_REQUESTED_COUNT_REACHED';continue
        if time.monotonic()-started>100:
            attempt['state']='NOT_ATTEMPTED_BUDGET';continue
        try:
            try:
                core,_=frame(raw,family)
            except ValueError as error:
                if str(error)=='OUTSIDE_CURRENT_COMMON_INTERFACE_METHOD_NOT_GLOBAL_INFEASIBILITY':
                    attempt.update(state='UNSUPPORTED_CURRENT_CORE_FIT',reason=str(error));continue
                raise
            if core is None:
                attempt['state']='UNSUPPORTED_CURRENT_CORE_FIT';continue
            proposal=importlib.import_module(module_name).propose(core,time_limit=2)
            attempt['proposal']=proposal
            if proposal.get('status')!='PROPOSAL_ONLY':
                attempt['state']=proposal.get('status','UNKNOWN_PROPOSAL_STATE');continue
            packet=build(raw,family,proposal)
            model=packet['world_model']
            if list(map(Fraction,model['inputs'][:2]))!=[Fraction(raw['W']),Fraction(raw['L'])] or model['inputs'][2]!=raw['n']:
                raise ValueError('CONSTRUCTED_INPUT_BINDING_MISMATCH')
            ctx=context(raw,proposal,packet)
            review=evaluate(packet,ctx)
            repair_result=None
            if review.get('status')=='FAIL' and review.get('errors') and not review.get('pending'):
                if time.monotonic()-started<80:
                    from parametric_repair_flow import attempt as repair_once
                    repair_result=repair_once(raw,family,proposal,packet,ctx,review,before,test_only=False)
                    attempt['repair_receipt']=repair_result['receipt']
                    attempt['repair_evidence']=repair_result.get('evidence')
                    replacement=repair_result['replacement']
                    if replacement:
                        packet=replacement['packet'];ctx=replacement['context'];review=replacement['review'];model=packet['world_model']
                else:attempt['repair_state']='NOT_ATTEMPTED_SHARED_BUDGET'
            attempt['state']='CONSTRUCTED_AND_FRESHLY_REVIEWED'
            candidate={'family':family,'organization':organization,'model':model,'model_digest':digest(model),'generation_context':ctx,'physical_review':review,'accepted':False,'delivery_allowed':False,'qualified':False}
            candidate['candidate_id']=digest({'request_digest':envelope['canonical_request_digest'],'model_digest':candidate['model_digest'],'family':family})
            from review_cycle import decide
            if repair_result:candidate['repair_receipt']=repair_result['receipt']
            from functional_review import assess
            candidate['functional_review']=assess(model,review,before)
            candidate['review_decision']=decide(candidate,envelope['canonical_request_digest'],before,candidate.get('repair_receipt'))
            candidates.append(candidate)
        except Exception as error:
            attempt.update(state='EXECUTION_ERROR',reason=type(error).__name__+':'+str(error))
    if revision()!=before:raise ValueError('ENGINE_SOURCE_CHANGED')
    if guard(freeze)!=pin_count:raise ValueError('HISTORICAL_PINS_CHANGED')
    from diversity_review import audit
    diversity=audit(candidates,envelope['canonical_request_digest'],before)
    return {'diversity_report':diversity,'diversity_report_digest':digest(diversity),'schema':SCHEMA,'outcome':'EXPERIMENT_COMPLETED','envelope':envelope,'engine_raw_request':raw,'engine_source_revision':before,'historical_pins':pin_count,'attempts':attempts,'candidates':candidates,'generated_count':len(candidates),'qualified_count':0,'requested_count':raw['requested_count'],'qualified_shortfall':raw['requested_count'],'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'elapsed_seconds':time.monotonic()-started,'program_policy':{'bedrooms_per_unit':3,'source':'existing constructor129 three-bedroom experimental profile','capacity_suitability':'NOT_VERIFIED','fallback_to_lower_capacity':False},'scope':'two existing ROW ownership families; not general topology coverage, six qualified options or whole architecture validation'}


def main():
    body=sys.stdin.buffer.read(16385)
    try:
        result=run(body)
    except InputError as e:
        result={'schema':SCHEMA,'outcome':'UNSUPPORTED' if e.status==409 else 'INVALID_INPUT','code':e.code,'field':e.field,'http_status':e.status,'accepted':False,'delivery_allowed':False}
    print(json.dumps(result,ensure_ascii=False,allow_nan=False))

if __name__=='__main__':main()
