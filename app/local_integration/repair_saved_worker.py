"""Fresh, bounded continuation of a specifically identified saved rejected model."""
import json,sys,re,uuid
from pathlib import Path
from run_history import summary,BASE
from dimension_contract import verify
from parametric_worker import ROOT,ENGINE,SCHEMA,prepare
from review_cycle import digest,decide

def load_source(run_id,candidate_id):
    summary(run_id)
    if type(candidate_id)is not str or re.fullmatch('[0-9a-f]{64}',candidate_id)is None:raise ValueError('CANDIDATE_ID')
    folder=BASE/run_id;body=(folder/'request.json').read_bytes();r=json.loads((folder/'result.json').read_text());verify(body,r['envelope'])
    candidates=[c for c in r['candidates']if c['candidate_id']==candidate_id]
    if len(candidates)!=1:raise ValueError('UNIQUE_CANDIDATE_REQUIRED')
    c=candidates[0]
    if c.get('generation_context',{}).get('construction_trace',{}).get('schema')!='CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1':raise ValueError('SAVED_REPAIR_CONSTRUCTOR_NOT_REGISTERED')
    if c['review_decision']['state']!='REJECTED_PHYSICAL':raise ValueError('SAVED_REJECTED_CANDIDATE_REQUIRED')
    if c.get('repair_receipt',{}).get('test_only'):raise ValueError('CONTROLLED_RECORD_NOT_NATURAL')
    return body,r,c

def validated_source_raw(body,candidate):
    # Revalidate before importing or invoking any historical construction entrypoint.
    _,raw=prepare(body)
    trace=candidate['generation_context']['construction_trace']
    if trace['raw']!=raw:raise ValueError('SAVED_TRACE_REQUEST_BINDING_MISMATCH')
    return raw

def run(source_run,candidate_id,output_id):
    if str(uuid.UUID(output_id))!=output_id:raise ValueError('OUTPUT_ID')
    body,old,c=load_source(source_run,candidate_id)
    raw=validated_source_raw(body,c)
    initial=c.get('initial_producer_receipt')
    if initial is not None:
        from producer_provenance import require_unchanged
        payload={k:v for k,v in initial.items() if k!='receipt_digest'}
        if digest(payload)!=initial.get('receipt_digest'):raise ValueError('SAVED_PRODUCER_RECEIPT_CHANGED')
        trace=c['generation_context']['construction_trace']
        if initial['request_digest']!=old['envelope']['canonical_request_digest'] or initial['initial_model_digest']!=c['model_digest'] or initial['proposal_digest']!=digest(trace['proposal']):raise ValueError('SAVED_PRODUCER_BINDING_CHANGED')
        require_unchanged(ROOT,initial['source_files'])
    sys.path.insert(0,str(ROOT/'frontend'));from guard400 import guard
    freeze='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0';pins=guard(freeze)
    sys.path.insert(0,str(ENGINE))
    from constructor129 import build,context
    from evaluate_hierarchical129 import evaluate
    from engine114 import revision
    from parametric_repair_flow import attempt
    trace=c['generation_context']['construction_trace'];source=revision()
    if source!=old['engine_source_revision']or source!=trace['source_revision']:raise ValueError('SAVED_SOURCE_REVISION_CHANGED')
    family=trace['family'];proposal=trace['proposal'];parent=build(raw,family,proposal)
    if digest(parent['world_model'])!=c['model_digest']:raise ValueError('SAVED_PARENT_EXACT_REPLAY_FAILED')
    ctx=context(raw,proposal,parent);before=evaluate(parent,ctx)
    if before['status']!='FAIL' or not before['errors'] or before['pending']:raise ValueError('NO_CURRENT_UNAMBIGUOUS_REJECTION')
    result=attempt(raw,family,proposal,parent,ctx,before,source,test_only=False)
    (BASE/output_id/'repair_evidence.json').write_text(json.dumps(result,ensure_ascii=False))
    receipt=result['receipt'];receipt['parent_run_id']=source_run;receipt['parent_candidate_id']=candidate_id
    selected=result['replacement']or{'packet':parent,'context':ctx,'review':before};model=selected['packet']['world_model']
    child={'family':family,'organization':'ROW','model':model,'model_digest':digest(model),'model_json':json.dumps(model,ensure_ascii=False,sort_keys=True,separators=(',',':')),'generation_context':selected['context'],'physical_review':selected['review'],'repair_receipt':receipt,'accepted':False,'delivery_allowed':False,'qualified':False}
    child['candidate_id']=digest({'request_digest':old['envelope']['canonical_request_digest'],'model_digest':child['model_digest'],'family':family,'repair_receipt_digest':digest(receipt)})
    from functional_review import assess
    child['functional_review']=assess(model,selected['review'],source)
    child['review_decision']=decide(child,old['envelope']['canonical_request_digest'],source,receipt)
    if initial is not None:
        require_unchanged(ROOT,initial['source_files'])
        child['parent_initial_producer_receipt']=initial
        child['producer_lineage']={'initial_model_digest':initial['initial_model_digest'],'final_model_digest':child['model_digest'],'repair_receipt_digest':digest(receipt),'accepted':False,'delivery_allowed':False}
    if revision()!=source or guard(freeze)!=pins:raise ValueError('SOURCE_CHANGED')
    return {'schema':SCHEMA,'outcome':'EXPERIMENT_COMPLETED','run_id':output_id,'parent_run_id':source_run,'envelope':old['envelope'],'engine_raw_request':raw,'engine_source_revision':source,'candidates':[child],'generated_count':1,'qualified_count':0,'requested_count':raw['requested_count'],'qualified_shortfall':raw['requested_count'],'request_fulfilled':False,'accepted':False,'delivery_allowed':False,'attempts':[{'family':family,'state':receipt['state'],'repair_receipt':receipt}],'scope':'fresh continuation of one saved rejected member, not regeneration of all requested options or semantic qualification'}

if __name__=='__main__':print(json.dumps(run(*sys.argv[1:]),ensure_ascii=False,allow_nan=False))
