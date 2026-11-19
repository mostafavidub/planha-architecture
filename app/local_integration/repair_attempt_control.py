"""Task4.4 bounded attempt ledger and no-progress stops; no quality ranking or admission."""
import copy,hashlib,json,math,os,signal,subprocess,time,uuid
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def require(ok,why):
 if not ok:raise ValueError(why)
def finite(x):return type(x) in (int,float) and math.isfinite(x)
def new_account(parent_model_digest,*,max_attempts=3,seconds=240):
 require(type(max_attempts) is int and 1<=max_attempts<=3,'ATTEMPT_LIMIT')
 require(finite(seconds) and 0<seconds<=240,'TIME_LIMIT')
 require(type(parent_model_digest) is str and len(parent_model_digest)==64,'PARENT_DIGEST')
 return {'schema':'BOUNDED_REPAIR_ACCOUNT_V1','account_id':uuid.uuid4().hex,'max_attempts':max_attempts,'seconds':seconds,
  'parent_model_digest':parent_model_digest,'used_attempts':0,'used_seconds':0,'active':None,'seen_model_digests':[parent_model_digest],'history':[],'stop_reason':None,
  'budget_policy':'Engineering study cap, not an architectural rule; no budget reset for retries or lower programmes',
  **{k:False for k in AUTH}}
def check(s,expected):
 require(digest(s)==expected,'ACCOUNT_RECEIPT')
 require(type(s['max_attempts']) is int and 1<=s['max_attempts']<=3 and finite(s['seconds']) and 0<s['seconds']<=240,'ACCOUNT_LIMITS')
 require(s['schema']=='BOUNDED_REPAIR_ACCOUNT_V1' and all(s.get(k) is False for k in AUTH),'ACCOUNT_SCHEMA_AUTHORITY')
 require(type(s['used_attempts']) is int and 0<=s['used_attempts']<=s['max_attempts'],'ACCOUNT_ATTEMPTS')
 require(finite(s['used_seconds']) and s['used_seconds']>=0,'ACCOUNT_TIME')
 require(type(s['account_id']) is str and len(s['account_id'])==32,'ACCOUNT_ID')
 require(type(s['history']) is list and s['active'] is None or type(s['history']) is list and type(s['active']) is dict,'ACCOUNT_HISTORY_ACTIVE')
 require(len(s['history'])+(1 if s['active'] is not None else 0)==s['used_attempts'],'ACCOUNT_HISTORY_COUNT')
 require(type(s['parent_model_digest']) is str and len(s['parent_model_digest'])==64,'ACCOUNT_PARENT')
 elapsed=0;seen=[s['parent_model_digest']];stop=None
 for i,row in enumerate(s['history'],1):
  require(stop is None,'ATTEMPT_AFTER_STOP')
  require(row['token']==s['account_id']+':'+str(i),'HISTORY_TOKEN')
  require(finite(row['elapsed_seconds']) and row['elapsed_seconds']>=0,'HISTORY_TIME')
  elapsed+=row['elapsed_seconds'];outcome=row['outcome'];model=row['observed_model_digest']
  require(outcome in ('CANDIDATE','NO_WITNESS','TIMED_OUT','ERROR'),'HISTORY_OUTCOME')
  require(model is None or type(model) is str and len(model)==64,'HISTORY_MODEL')
  require(row['counts_as_quality_improvement'] is False,'NO_QUALITY_CLAIM')
  if outcome=='TIMED_OUT' or elapsed>=s['seconds']:stop='TIME_BUDGET_EXHAUSTED_NOT_INFEASIBLE'
  elif outcome=='ERROR':stop='EXECUTION_ERROR_NOT_GEOMETRIC_FAILURE'
  elif outcome=='NO_WITNESS' or model is None:stop='NO_VERIFIED_CANDIDATE_IN_ATTEMPT_NOT_INFEASIBLE'
  elif model in seen:stop='REPEATED_MODEL_NO_GEOMETRIC_PROGRESS'
  else:
   seen.append(model)
   if i>=s['max_attempts']:stop='ATTEMPT_BUDGET_EXHAUSTED'
 require(elapsed==s['used_seconds'] and seen==s['seen_model_digests'] and stop==s['stop_reason'],'ACCOUNT_HISTORY_REPLAY')
 if s['active'] is not None:
  require(stop is None and s['active']['token']==s['account_id']+':'+str(s['used_attempts']),'ACTIVE_TOKEN')
  require(s['active']['allocated_seconds']==s['seconds']-elapsed and finite(s['active']['allocated_seconds']) and s['active']['allocated_seconds']>0,'ACTIVE_ALLOCATION')
def reserve(state,expected_digest):
 check(state,expected_digest);s=copy.deepcopy(state)
 require(s['active'] is None,'ATTEMPT_ALREADY_ACTIVE')
 require(s['stop_reason'] is None,'ACCOUNT_STOPPED')
 if s['used_attempts']>=s['max_attempts']:s['stop_reason']='ATTEMPT_BUDGET_EXHAUSTED';return s,None
 remaining=s['seconds']-s['used_seconds']
 if remaining<=0:s['stop_reason']='TIME_BUDGET_EXHAUSTED';return s,None
 s['used_attempts']+=1
 token=s['account_id']+':'+str(s['used_attempts']);s['active']={'token':token,'allocated_seconds':remaining}
 return s,copy.deepcopy(s['active'])
def finish(state,expected_digest,token,*,elapsed_seconds,outcome,model_digest=None):
 check(state,expected_digest);s=copy.deepcopy(state)
 require(s['active'] is not None and s['active']['token']==token,'ATTEMPT_TOKEN')
 require(finite(elapsed_seconds) and elapsed_seconds>=0,'ELAPSED_TIME')
 require(outcome in ('CANDIDATE','NO_WITNESS','TIMED_OUT','ERROR'),'OUTCOME_ENUM')
 if model_digest is not None:require(type(model_digest) is str and len(model_digest)==64,'MODEL_DIGEST')
 s['used_seconds']+=elapsed_seconds
 row={'token':token,'elapsed_seconds':elapsed_seconds,'outcome':outcome,'observed_model_digest':model_digest,'counts_as_quality_improvement':False}
 if outcome=='TIMED_OUT' or s['used_seconds']>=s['seconds']:s['stop_reason']='TIME_BUDGET_EXHAUSTED_NOT_INFEASIBLE'
 elif outcome=='ERROR':s['stop_reason']='EXECUTION_ERROR_NOT_GEOMETRIC_FAILURE'
 elif outcome=='NO_WITNESS' or model_digest is None:s['stop_reason']='NO_VERIFIED_CANDIDATE_IN_ATTEMPT_NOT_INFEASIBLE'
 elif model_digest in s['seen_model_digests']:s['stop_reason']='REPEATED_MODEL_NO_GEOMETRIC_PROGRESS'
 else:
  s['seen_model_digests'].append(model_digest)
  if s['used_attempts']>=s['max_attempts']:s['stop_reason']='ATTEMPT_BUDGET_EXHAUSTED'
 s['history'].append(row);s['active']=None
 return s
def run_bounded(argv,seconds):
 require(type(argv) is list and argv and all(type(x) is str for x in argv),'COMMAND_ARGV')
 require(finite(seconds) and 0<seconds<=240,'PROCESS_BUDGET')
 started=time.monotonic();p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 timed=False;killed=False
 try:stdout,stderr=p.communicate(timeout=seconds)
 except subprocess.TimeoutExpired:
  timed=True
  try:os.killpg(p.pid,signal.SIGKILL);killed=True
  except ProcessLookupError:pass
  stdout,stderr=p.communicate()
 return {'timed_out':timed,'kill_sent':killed,'wait_completed':p.poll() is not None,'returncode':p.returncode,
  'elapsed_seconds':time.monotonic()-started,'allocated_seconds':seconds,'stdout':stdout,'stderr':stderr,
  'scope':'Dedicated process group; no guarantee for descendants that escape with a new session',**{k:False for k in AUTH}}
def classify_retained_parent(r):
 require(r['schema']=='BOUNDED_REPAIR_PARENT_RECEIPT_V1','PARENT_RECEIPT_SCHEMA')
 require(all(r.get(k) is False for k in AUTH),'PARENT_AUTHORITY')
 require(finite(r['elapsed_seconds']) and r['elapsed_seconds']>=0 and r['shared_child_seconds']==240,'PARENT_BUDGET')
 if r['timed_out'] is True:return {'state':'TIMED_OUT_NOT_INFEASIBLE','delivery_allowed':False,'budget_reset':False}
 require(r['source_integrity_verified'] is True and r['child_receipt_verified'] is True,'PARENT_NOT_VERIFIED')
 require(r['state'] in ('BOUNDED_SEARCH_NO_CHILD_NOT_INFEASIBLE','FRESH_CHILD_ALL_GATES_RECORDED_NOT_QUALIFIED'),'PARENT_STATE')
 if r['state']=='BOUNDED_SEARCH_NO_CHILD_NOT_INFEASIBLE':
  require(type(r['generated_count']) is int and r['generated_count']==0,'PARENT_COUNT')
  state='BOUNDED_REPAIR_NO_SELECTED_CHILD_NOT_INFEASIBLE'
 else:
  require(type(r['generated_count']) is int and r['generated_count']==1,'PARENT_COUNT')
  require(r['current_decision']['state']=='BLOCKED' and all(r['current_decision'][k] is False for k in AUTH),'CURRENT_NO_ADMISSION')
  state='REPAIR_CANDIDATE_OBTAINED_BUT_DELIVERY_BLOCKED'
 return {'state':state,'used_seconds':r['elapsed_seconds'],'limit_seconds':240,'budget_reset':False,'delivery_allowed':False,
  'scope':'Classification of verified retained task4.3 parent receipt, not a re-execution or proof of quality'}
