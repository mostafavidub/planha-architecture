"""Saved explicit two-bedroom redirection; never accepts default or constructor129."""
import json,sys,re,uuid
from run_history import summary,BASE
from dimension_contract import verify
from parametric_worker import ROOT,SCHEMA,prepare
from review_cycle import digest,decide
from producer_provenance import require_unchanged,snapshot
def load_source(run_id,candidate_id):
    summary(run_id)
    if type(candidate_id)is not str or re.fullmatch('[0-9a-f]{64}',candidate_id)is None:raise ValueError('CANDIDATE_ID')
    folder=BASE/run_id;body=(folder/'request.json').read_bytes();old=json.loads((folder/'result.json').read_text())
    envelope,raw=prepare(body);verify(body,old['envelope'])
    if envelope['canonical_request'].get('program')!={'bedrooms_per_unit':2}:raise ValueError('EXPLICIT_TWO_BEDROOM_PROGRAM_REQUIRED')
    matches=[c for c in old['candidates'] if c['candidate_id']==candidate_id]
    if len(matches)!=1:raise ValueError('UNIQUE_PARENT_REQUIRED')
    c=matches[0];ctx=c['generation_context'];trace=ctx['construction_trace']
    if trace.get('schema')!='CONSTRUCTION_TRACE127_PAIR_V1' or trace.get('raw')!=raw or c['review_decision']['state']!='REJECTED_PHYSICAL':raise ValueError('EXPLICIT_REJECTED_PAIR_REQUIRED')
    if c.get('repair_receipt') or c.get('exploratory_redirection_receipt'):raise ValueError('INITIAL_PAIR_PARENT_ONLY')
    initial=c.get('initial_producer_receipt',{})
    payload={k:v for k,v in initial.items() if k!='receipt_digest'}
    if initial.get('schema')!='V25_EXPLICIT_PROGRAM_PRODUCER_V1' or initial.get('receipt_digest')!=digest(payload):raise ValueError('PARENT_PRODUCER_RECEIPT_REQUIRED')
    bindings={'request_digest':envelope['canonical_request_digest'],'initial_model_digest':digest(c['model']),'proposal_digest':digest(trace['proposals']),'context_digest':digest(ctx),'initial_review_digest':digest(c['physical_review']),'historical_engine_revision':old['engine_source_revision']}
    if any(initial.get(k)!=v for k,v in bindings.items()):raise ValueError('PARENT_PRODUCER_BINDING')
    require_unchanged(ROOT,initial['source_files'])
    return body,old,c
def run(source_run,candidate_id,output_id):
    if str(uuid.UUID(output_id))!=output_id:raise ValueError('OUTPUT_ID')
    body,old,parent=load_source(source_run,candidate_id)
    sources=snapshot(ROOT,['app/local_integration/explicit_pair_saved_worker.py','app/local_integration/functional_review.py','app/local_integration/guest_four_route_diagnostic.py','app/local_integration/living_connectivity_diagnostic.py'])
    from explicit_pair_redirection import redirect
    result=redirect(body,parent['model'],parent['generation_context'])
    (BASE/output_id/'exploratory_evidence.json').write_text(json.dumps(result,ensure_ascii=False))
    child=result['child']
    if child:
        model=child['packet']['world_model'];ctx=child['context'];review=child['review']
    else:model=parent['model'];ctx=parent['generation_context'];review=result['fresh_parent_review']
    receipt={'schema':'V25_SAVED_PAIR_REDIRECTION_RECEIPT_V1','scope':result['scope'],'parent_run_id':source_run,'parent_candidate_id':candidate_id,'parent_model_digest':result['parent_model_digest'],'request_digest':result['request_digest'],'source_revision':result['source_revision'],'operator_receipt_digest':result['receipt_digest'],'integration_sources':sources,'child_created':child is not None,'final_model_digest':digest(model),'fresh_parent_review_digest':digest(result['fresh_parent_review']),'fresh_final_review_digest':digest(review),'parent_pending_preserved':result['parent_pending_preserved'],'state':result['state'],'accepted':False,'display_allowed':False,'delivery_allowed':False,'qualified':False,'production_repair_registered':False}
    receipt['receipt_digest']=digest(receipt)
    candidate={'family':'FRONT_REAR','organization':'EXPLICIT_TWO_BEDROOM_EXPLORATORY_REDIRECTION','model':model,'model_digest':digest(model),'model_json':json.dumps(model,ensure_ascii=False,sort_keys=True,separators=(',',':')),'generation_context':ctx,'physical_review':review,'exploratory_redirection_receipt':receipt,'parent_initial_producer_receipt':parent['initial_producer_receipt'],'accepted':False,'delivery_allowed':False,'qualified':False,'repair_capability':{'supported':False,'reason':'PRODUCTION_PAIR_REPAIR_NOT_REGISTERED'}}
    candidate['candidate_id']=digest({'request_digest':result['request_digest'],'model_digest':digest(model),'exploratory_receipt_digest':digest(receipt)})
    from functional_review import assess
    candidate['functional_review']=assess(model,review,result['source_revision'])
    candidate['review_decision']=decide(candidate,result['request_digest'],result['source_revision'])
    candidate['producer_lineage']={'initial_model_digest':result['parent_model_digest'],'final_model_digest':digest(model),'exploratory_receipt_digest':digest(receipt),'accepted':False,'delivery_allowed':False}
    require_unchanged(ROOT,sources);require_unchanged(ROOT,parent['initial_producer_receipt']['source_files'])
    from guard400 import guard
    from explicit_pair_redirection import FREEZE
    from engine114 import revision
    if guard(FREEZE)!=12991 or revision()!=result['source_revision']:raise ValueError('SOURCE_CHANGED')
    _,raw=prepare(body)
    return {'schema':SCHEMA,'outcome':'EXPERIMENT_COMPLETED','run_id':output_id,'parent_run_id':source_run,'envelope':old['envelope'],'engine_raw_request':raw,'engine_source_revision':result['source_revision'],'candidates':[candidate],'generated_count':int(child is not None),'reviewed_candidate_count':1,'reused_parent':child is None,'qualified_count':0,'requested_count':raw['requested_count'],'qualified_shortfall':raw['requested_count'],'request_fulfilled':False,'accepted':False,'delivery_allowed':False,'attempts':[{'state':result['state'],'exploratory_receipt':receipt}],'scope':result['scope']}
if __name__=='__main__':print(json.dumps(run(*sys.argv[1:]),ensure_ascii=False,allow_nan=False))
