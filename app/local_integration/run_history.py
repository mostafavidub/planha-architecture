"""Historical summaries only. Never restores a live model or export authority."""
import json
from pathlib import Path
import uuid
from dimension_contract_historical import verify
from dimension_contract import parse,InputError
from review_cycle import decide
from parametric_worker import ROOT
BASE=ROOT/'app/local_integration/evidence/requests'

def valid_id(value):
    try:return type(value)is str and str(uuid.UUID(value))==value
    except (ValueError,AttributeError):return False

def summary(run_id,base=BASE):
    if not valid_id(run_id):raise ValueError('INVALID_RUN_ID')
    folder=base/run_id
    if folder.is_symlink():raise ValueError('SYMLINK_RUN_FORBIDDEN')
    for name in ('request.json','result.json','lifecycle.json'):
        p=folder/name
        if p.is_symlink() or p.stat().st_size>16000000:raise ValueError('UNSAFE_RECORD')
    body=(folder/'request.json').read_bytes();result=json.loads((folder/'result.json').read_text());life=json.loads((folder/'lifecycle.json').read_text())
    if result.get('run_id')!=run_id or life.get('wait_completed')is not True:raise ValueError('INCOMPLETE_OR_WRONG_RUN')
    if result.get('accepted')is not False or result.get('delivery_allowed')is not False:raise ValueError('UNREGISTERED_AUTHORITY')
    current_range=True
    try:parse(body)
    except InputError as error:
        if error.code=='DIMENSION_OUT_OF_OWNER_RANGE':current_range=False
        else:raise
    rows=[]
    if result.get('outcome')=='EXPERIMENT_COMPLETED':
        verify(body,result['envelope'])
        for candidate in result['candidates']:
            decision=decide(candidate,result['envelope']['canonical_request_digest'],result['engine_source_revision'],candidate.get('repair_receipt'))
            if candidate.get('review_decision')!=decision:raise ValueError('HISTORICAL_REVIEW_DECISION_MISMATCH')
            rows.append({k:decision[k]for k in ('candidate_id','model_digest','review_digest','decision_id','state')})
        expected_generated=len(rows)
        if result.get('scope')=='EXPLORATORY_ONLY_NOT_PRODUCTION_REPAIR':
            if len(rows)!=1 or result.get('reviewed_candidate_count')!=1:raise ValueError('EXPLORATORY_REVIEW_COUNT')
            receipt=result['candidates'][0]['exploratory_redirection_receipt']
            created=receipt.get('child_created')
            if type(created)is not bool or result.get('reused_parent')is not (not created):raise ValueError('EXPLORATORY_GENERATION_COUNT')
            if (receipt['final_model_digest']!=receipt['parent_model_digest'])is not created:raise ValueError('EXPLORATORY_CHILD_IDENTITY')
            expected_generated=int(created)
        if result['generated_count']!=expected_generated or result.get('qualified_count')!=0:raise ValueError('COUNT_MISMATCH')
    return {'schema':'MAC_HISTORICAL_SUMMARY_V1','run_id':run_id,'historical_only':True,'within_current_owner_range':current_range,'current_owner_range_m':[5,25],'live_model_restored':False,'request':json.loads(body),'outcome':result['outcome'],'candidates':rows,'generated_count':result.get('generated_count',len(rows)),'reviewed_candidate_count':len(rows),'qualified_count':0,'saved_at_ns':(folder/'result.json').stat().st_mtime_ns,'accepted':False,'delivery_allowed':False,'scope':'saved record consistency, not current-source reevaluation or architecture acceptance'}

def list_history(base=BASE):
    folders=sorted((p for p in base.iterdir()if p.is_dir()and not p.is_symlink()and valid_id(p.name)),key=lambda p:p.stat().st_mtime_ns,reverse=True)[:50] if base.exists()else []
    records=[];omitted=0
    for p in folders:
        try:records.append(summary(p.name,base))
        except (ValueError,KeyError,TypeError,OSError):omitted+=1
    return {'schema':'MAC_HISTORY_LIST_V1','historical_only':True,'records':records,'omitted_unverifiable_or_legacy':omitted,'limit':50,'delivery_allowed':False}

def output_gate(run_id,base=BASE):
    # Current engine has no registered semantic acceptance or artifact issuer.
    # A saved true flag is rejected by summary, never interpreted as authority.
    record=summary(run_id,base)
    return 403,{'code':'NO_CURRENT_QUALIFIED_DELIVERY_AUTHORITY','run_id':run_id,'historical_only':True,'qualified_count':record['qualified_count'],'decision_ids':[c['decision_id']for c in record['candidates']],'accepted':False,'delivery_allowed':False,'artifact_bytes_sent':0}
