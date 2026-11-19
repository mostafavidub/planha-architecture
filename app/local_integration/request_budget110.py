"""Exact single-request ledger; no durable cross-request replay protection.
Reuses the existing bounded process primitive through the request bridge.
"""
import copy,math,re
from same_version_front_rear_contract import digest
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
REPORTED={'BLOCKED_NO_SUPPORTED_CAUSE','BLOCKED_REPAIR_CONTROLLER_ADAPTER','BLOCKED_NO_PARENT_PROPOSAL','FAILED_CLOSED','SOURCE_INTEGRITY_ERROR','TIMED_OUT'}
def need(ok,code):
 if not ok:raise ValueError(code)
def finite(x):return type(x)in(int,float)and math.isfinite(x)and x>=0
def hash_ok(x):return type(x)is str and re.fullmatch('[0-9a-f]{64}',x)is not None
def anchor(request,expected,prior_models=()):
 need(digest(request)==expected,'LEDGER_REQUEST_DIGEST')
 need(type(request['account_id'])is str and re.fullmatch('[0-9a-f]{32}',request['account_id'])is not None,'LEDGER_ACCOUNT_ID')
 need(type(request['nonce'])is str and re.fullmatch('[0-9a-f]{32}',request['nonce'])is not None,'LEDGER_NONCE')
 need(finite(request['allocated_seconds'])and 0<request['allocated_seconds']<=240,'LEDGER_LIMIT')
 need(type(prior_models)in(list,tuple)and all(hash_ok(x)for x in prior_models)and len(set(prior_models))==len(prior_models),'LEDGER_PRIOR_MODELS')
 return {'account_id':request['account_id'],'nonce':request['nonce'],'request_digest':expected,'limit_seconds':request['allocated_seconds'],'max_attempts':1,'prior_model_digests':list(prior_models)}
def create(a):
 out={'schema':'REQUEST_ATTEMPT_LEDGER110_V1','anchor':copy.deepcopy(a),'used_attempts':0,'used_seconds':0,'active':None,'history':[],'state':'NEW','unique_observed_models':[],**{k:False for k in AUTH}}
 check(out,digest(out),a);return out
def terminal(row,a):
 need(type(row['observed_receipt_verified'])is bool,'LEDGER_RECEIPT_TYPE')
 outcome=row['reported_outcome'];verified=row['observed_receipt_verified']
 if row['elapsed_seconds']>=a['limit_seconds']:return 'BUDGET_EXHAUSTED',False
 if outcome in('TIMED_OUT','FAILED_CLOSED','SOURCE_INTEGRITY_ERROR'):return outcome,False
 if row['observed_model_digest']in a['prior_model_digests']:return 'REPEATED_MODEL_NO_PROGRESS',False
 return outcome,verified
def check(s,expected,a):
 need(type(s)is dict and digest(s)==expected,'LEDGER_DIGEST')
 need(set(s)=={'schema','anchor','used_attempts','used_seconds','active','history','state','unique_observed_models',*AUTH},'LEDGER_FIELDS')
 need(s['schema']=='REQUEST_ATTEMPT_LEDGER110_V1'and digest(s['anchor'])==digest(a),'LEDGER_ANCHOR')
 need(set(a)=={'account_id','nonce','request_digest','limit_seconds','max_attempts','prior_model_digests'},'LEDGER_ANCHOR_FIELDS')
 need(type(a['max_attempts'])is int and a['max_attempts']==1 and finite(a['limit_seconds'])and 0<a['limit_seconds']<=240,'LEDGER_ANCHOR_LIMIT')
 need(hash_ok(a['request_digest'])and type(a['prior_model_digests'])is list and all(hash_ok(x)for x in a['prior_model_digests'])and len(set(a['prior_model_digests']))==len(a['prior_model_digests']),'LEDGER_ANCHOR_VALUES')
 need(all(s.get(k)is False for k in AUTH),'LEDGER_AUTHORITY')
 need(type(s['used_attempts'])is int and 0<=s['used_attempts']<=1 and finite(s['used_seconds']),'LEDGER_COUNTS')
 need(type(s['history'])is list and len(s['history'])<=1,'LEDGER_HISTORY')
 elapsed=0;models=[]
 for i,row in enumerate(s['history'],1):
  need(type(row)is dict and set(row)=={'token','request_digest','elapsed_seconds','reported_outcome','outcome','observed_model_digest','observed_receipt_verified','receipt_verified','process_digest','internal_attempt_count','internal_count_verified','quality_improvement'},'LEDGER_ROW_FIELDS')
  need(row['token']==a['account_id']+':'+str(i)and row['request_digest']==a['request_digest'],'LEDGER_ROW_ID')
  need(finite(row['elapsed_seconds'])and row['reported_outcome']in REPORTED,'LEDGER_ROW_OUTCOME')
  need(row['observed_model_digest']is None or hash_ok(row['observed_model_digest']),'LEDGER_ROW_MODEL')
  need(row['process_digest']is None or hash_ok(row['process_digest']),'LEDGER_ROW_PROCESS')
  need(type(row['internal_count_verified'])is bool and (row['internal_attempt_count']is None or type(row['internal_attempt_count'])is int and row['internal_attempt_count']>=0),'LEDGER_INTERNAL_COUNT')
  if row['internal_count_verified']:need(row['observed_receipt_verified']is True and row['internal_attempt_count']==1,'LEDGER_VERIFIED_INTERNAL_COUNT')
  need(row['quality_improvement']is False,'LEDGER_NO_QUALITY_CLAIM')
  outcome,verified=terminal(row,a)
  need(row['outcome']==outcome and row['receipt_verified']is verified,'LEDGER_REPLAY_OUTCOME')
  elapsed+=row['elapsed_seconds']
  if row['observed_model_digest']is not None and row['observed_model_digest']not in models:models.append(row['observed_model_digest'])
 need(type(s['unique_observed_models'])is list and digest(s['unique_observed_models'])==digest(models)and s['used_seconds']==elapsed,'LEDGER_HISTORY_REPLAY')
 if s['active']is not None:
  need(type(s['active'])is dict and set(s['active'])=={'token','allocated_seconds'}and not s['history']and s['used_attempts']==1,'LEDGER_ACTIVE')
  need(s['active']['token']==a['account_id']+':1'and type(s['active']['allocated_seconds'])in(int,float)and s['active']['allocated_seconds']==a['limit_seconds'],'LEDGER_ACTIVE_ALLOCATION')
  need(s['state']=='ACTIVE','LEDGER_ACTIVE_STATE')
 elif s['history']:
  need(s['used_attempts']==1 and s['state']==s['history'][-1]['outcome'],'LEDGER_TERMINAL_STATE')
 else:need(s['used_attempts']==0 and s['state']=='NEW','LEDGER_NEW_STATE')
 return True
def reserve(s,expected,a):
 check(s,expected,a);need(s['state']=='NEW'and s['active']is None,'LEDGER_NO_RESTART')
 out=copy.deepcopy(s);out.update(used_attempts=1,state='ACTIVE',active={'token':a['account_id']+':1','allocated_seconds':a['limit_seconds']})
 check(out,digest(out),a);return out,copy.deepcopy(out['active'])
def finish(s,expected,a,token,*,elapsed_seconds,reported_outcome,model_digest=None,receipt_verified=False,process_digest=None,internal_attempt_count=None,internal_count_verified=False):
 check(s,expected,a);need(s['active']is not None and token==s['active']['token'],'LEDGER_FINISH_TOKEN')
 need(finite(elapsed_seconds),'LEDGER_FINISH_TIME');need(reported_outcome in REPORTED,'LEDGER_FINISH_OUTCOME')
 row={'token':token,'request_digest':a['request_digest'],'elapsed_seconds':elapsed_seconds,'reported_outcome':reported_outcome,
  'observed_model_digest':model_digest,'observed_receipt_verified':receipt_verified,'process_digest':process_digest,
  'internal_attempt_count':internal_attempt_count,'internal_count_verified':internal_count_verified,'quality_improvement':False}
 row['outcome'],row['receipt_verified']=terminal(row,a)
 out=copy.deepcopy(s);out.update(active=None,used_seconds=elapsed_seconds,state=row['outcome'],history=[row],unique_observed_models=[]if model_digest is None else[model_digest])
 check(out,digest(out),a);return out
