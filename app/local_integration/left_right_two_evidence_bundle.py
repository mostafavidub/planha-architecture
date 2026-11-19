"""Evidence bundle only; does not replace any production/historical admission.
Source-derived shape and D4 are not a declarative independent semantic schema.
Historical pair evaluator remains authoritative about its own incompatibility.
"""
import copy,hashlib,inspect,json,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ENGINE)]
from left_right_two_source_binding import verify as source_binding,digest,exact,source_state,ENGINE_PIN
from producer_provenance import snapshot,require_unchanged
from guard400 import guard
FREEZE='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
CURRENT_UNKNOWN={'CURRENT_PROGRAM_SUITABILITY','KITCHEN_GUEST_PATH_SEPARATION','CONTINUOUS_USEFUL_LIVING','NONFUNCTIONAL_WALL_EXCLUSION'}
LOCAL_FILES=['left_right_two_evidence_bundle.py','left_right_two_source_binding.py','functional_review.py','guest_four_route_diagnostic.py','kitchen_guest_review.py','living_connectivity_diagnostic.py','review_cycle.py','producer_provenance.py']

def ensure(ok,reason):
    if not ok:raise ValueError(reason)

def evaluate(packet,ctx):
    result={'schema':'V25_LEFT_RIGHT_TWO_EVIDENCE_BUNDLE_V1','status':'EVIDENCE_BUNDLE_ONLY','accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'whole_physical_verified':False,'whole_functional_verified':False,'production_supported':False,'historical_compatibility':'NOT_EVALUATED','errors':[],'pending_obligations':[],
      'scope':'Independent orchestration of original physical/named and current diagnostics. Source-derived shape/D4 only, not independent declarative semantic schema, not a replacement admission contract; historical incompatibility and all pending retained.',
      'stages':[]}
    paths=['app/local_integration/'+name for name in LOCAL_FILES]
    sources=snapshot(ROOT,paths);engine_before=source_state();immutable=digest([packet,ctx])
    def unchanged():
        ensure(digest([packet,ctx])==immutable,'BUNDLE_INPUT_MUTATION')
        require_unchanged(ROOT,sources);ensure(source_state()==engine_before,'BUNDLE_ENGINE_CHANGED')
        ensure(guard(FREEZE)==12991,'FROZEN_GUARD_CHANGED')
    def record_pending(section,report):
        for field in ('pending','original_pending','not_evaluated'):
            for value in report.get(field,[]):result['pending_obligations'].append({'section':section,'field':field,'value':copy.deepcopy(value)})
        for row in report.get('out_of_scope',[]):result['pending_obligations'].append({'section':section,'field':'out_of_scope','value':copy.deepcopy(row)})
    try:
        ensure(guard(FREEZE)==12991,'FROZEN_GUARD_CHANGED')
        shape=source_binding(packet,ctx);result['source_derived_shape_d4']=shape
        result['stages'].append('source_derived_shape_d4')
        unchanged()
        ensure(shape['scoped_verified'],'SOURCE_DERIVED_BINDING_FAILED')
        model=packet['world_model'];mh=digest(model);result['model_hash']=mh
        import checker114,frame_audit125,evaluate_pair127,functional_review,rule_contract118
        for fn,path in [(checker114.evaluate,ENGINE/'checker114.py'),(frame_audit125.evaluate_core,ENGINE/'frame_audit125.py'),(evaluate_pair127.evaluate,ENGINE/'evaluate_pair127.py'),(functional_review.assess,ROOT/'app/local_integration/functional_review.py'),(rule_contract118.load_contract,ENGINE/'rule_contract118.py')]:
            ensure(Path(inspect.getsourcefile(fn)).resolve()==path.resolve(),'BUNDLE_IMPORTED_CALLABLE_PATH')
        bound_context=copy.deepcopy(ctx)
        bound_context['frame_core125']=copy.deepcopy(packet['core'])
        bound_context['frame_local129']=copy.deepcopy(packet['local_model'])
        bound_context_hash=digest(bound_context)
        result['bound_workflow_context_hash']=bound_context_hash
        result['frame_report']=frame_audit125.evaluate_core(packet['core'])
        result['stages'].append('original_frame_audit125');unchanged()
        physical=checker114.evaluate(model,workflow_context=bound_context)
        ensure(digest(bound_context)==bound_context_hash,'CHECKER_CONTEXT_MUTATION')
        ensure(physical.get('model_hash')==mh,'PHYSICAL_MODEL_BINDING')
        result['physical_and_named_original_checker']=physical
        result['stages'].append('original_checker114_with_original_named_checks');unchanged()
        contract=rule_contract118.load_contract();audit=physical['rule_contract_evidence']
        actual=[r['requirement_id'] for r in audit['requirements']]
        wanted=[r['id'] for r in contract['requirements']]
        ensure(actual==wanted and len(actual)==len(set(actual)),'NAMED_REQUIREMENT_INVENTORY')
        ensure(audit['model_hash']==mh and audit['all_rules_approved']is False,'NAMED_MODEL_AUTHORITY')
        result['named_requirement_inventory']={'ids':actual,'count':len(actual),'contract_hash':audit['contract_hash'],'model_hash':mh}
        current=functional_review.assess(model,physical,ENGINE_PIN)
        ensure(current['model_digest']==mh and current['physical_review_digest']==digest(physical) and current['source_revision']==ENGINE_PIN,'CURRENT_FUNCTIONAL_BINDING')
        rows=current['requirements'];ids=[r['id'] for r in rows]
        ensure(set(ids)==CURRENT_UNKNOWN|{'INTERNAL_INSTANCE_CAPACITY'} and len(ids)==5,'CURRENT_REQUIREMENT_INVENTORY')
        ensure(all(r['state']=='UNKNOWN' for r in rows if r['id'] in CURRENT_UNKNOWN),'CURRENT_UNKNOWN_REQUIRED')
        ensure(all(current[k]is False for k in ('accepted','qualified','display_allowed','delivery_allowed')),'CURRENT_AUTHORITY')
        result['current_functional_report']=current
        result['stages'].append('original_current_functional_assess');unchanged()
        historical=evaluate_pair127.evaluate(packet,ctx)
        ensure(historical.get('model_hash')==mh,'HISTORICAL_MODEL_BINDING')
        result['historical_full_report']=historical
        result['stages'].append('original_evaluate_pair127_unfiltered');unchanged()
        record_pending('source_derived_shape_d4',shape)
        record_pending('original_frame_audit125',result['frame_report'])
        record_pending('original_checker114',physical)
        record_pending('original_evaluate_pair127',historical)
        for row in rows:
            if row['state']!='PASS_SCOPED':result['pending_obligations'].append({'section':'current_functional','field':'requirement','value':copy.deepcopy(row)})
        # Reports themselves are preserved in full. Error rows are merely indexed,
        # never removed/classified away or used to manufacture admission.
        for section,report in [('original_frame_audit125',result['frame_report']),('original_checker114',physical),('original_evaluate_pair127',historical)]:
            for error in report.get('errors',[]):result['errors'].append({'section':section,'error':copy.deepcopy(error)})
        result['historical_compatibility']='BLOCKED' if historical['errors'] or historical['pending'] else 'NO_ERRORS_OBSERVED_NOT_ADMISSION'
        result['status']='HISTORICAL_COMPATIBILITY_BLOCKED' if result['historical_compatibility']=='BLOCKED' else 'EVIDENCE_BUNDLE_ONLY'
        result['completed']=True
    except Exception as ex:
        result['status']='EVIDENCE_BUNDLE_FAILED_CLOSED';result['completed']=False
        result['errors'].append({'section':'orchestration','type':type(ex).__name__,'detail':str(ex),'traceback':traceback.format_exc()})
    finally:
        try:unchanged()
        except Exception as ex:
            result.update(status='EVIDENCE_BUNDLE_FAILED_CLOSED',completed=False)
            result['errors'].append({'section':'final_immutability','type':type(ex).__name__,'detail':str(ex)})
        result.update(source_snapshot=sources,engine_revision=ENGINE_PIN,input_bundle_digest=immutable,output_bundle_digest=digest([packet,ctx]),guard_expected=12991)
    return result
