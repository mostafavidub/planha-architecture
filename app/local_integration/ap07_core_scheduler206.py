"""AP07 two-core request orchestration study, not programme selection or qualification.
No private artifacts. Historical child function is reused read-only; its main is not run.
Full reports exist only inside one temporary request lifecycle, never public uploads.
"""
import copy,hashlib,inspect,json,math,os,re,signal,subprocess,sys,tempfile,time,uuid
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import core_choice_pair_study as corestudy
from same_version_front_rear_contract import digest
from current_entry_boundary_x03 import public_request
from program_profile_registry import lookup
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
CHOICES=('FRONT_REAR_COMPACT118','FRONT_REAR_FULL_BAND114')
RAW={'W':'18','L':'20','n':2,'requested_count':1}
BODY=b'{"W":"18","L":"20","n":2}'
LIMIT=480
TASK_END=datetime(2026,11,19,17,33,40,tzinfo=timezone.utc)
OLD_PATHS=['app/local_integration/'+n for n in ('core_choice_pair_study.py','one_bed_pair_source_study.py','program_profile_registry.py','front_rear_runtime_adapter.py','same_version_front_rear_contract.py')]
OLD_PATHS+=['app/reconstruction357/planha_general150_runtime_work/'+n for n in ('contract114.py','assemble114.py','search114.py','constructor127.py','construction_replay127.py','evaluate_pair127.py','core_wall_audit118.py','entry117.py')]
EXTRA_PATHS=['app/local_integration/'+n for n in ('ap07_core_scheduler206.py','current_entry_boundary_x03.py','public_wln_contract.py','dimension_contract.py')]
REPORTS={'independent_replay','original_replay','physical','core_partition','core_concept','opening_hosts','core_assessment','actual_detached_negatives'}
OUTCOMES={'VERIFIED_CORE_STUDY','NO_PROPOSAL','EXECUTION_ERROR','TIMED_OUT','RECEIPT_ERROR','REPEATED_MODEL'}
def need(ok,code):
 if not ok:raise ValueError(code)
def finite(v):return type(v)in(int,float)and math.isfinite(v)and v>=0
def hash_ok(v):return type(v)is str and re.fullmatch('[0-9a-f]{64}',v)is not None
def save(path,value):
 p=Path(str(path)+'.tmp');p.write_text(json.dumps(value,sort_keys=True,allow_nan=False));p.replace(path)
def read(path):return json.loads(path.read_text())
def snapshot(paths):
 return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in paths}
def sources():
 need(Path(inspect.getsourcefile(corestudy.child)).resolve()==ROOT/'app/local_integration/core_choice_pair_study.py','CHILD_IMPORT_PATH')
 data=(ROOT/'app/local_integration/core_choice_pair_study.py').read_bytes()
 need(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()=='4ed751238583d63ec2d9bb570bccbb9b0802cd3c','CHILD_SOURCE_PIN')
 return snapshot(OLD_PATHS+EXTRA_PATHS)
def make_request(body,started,seconds):
 env,raw=public_request(body)
 need(digest(raw)==digest(RAW),'UNSUPPORTED_AP07_STUDY_INPUT')
 need(finite(started)and finite(seconds)and 0<seconds<=LIMIT,'REQUEST_BUDGET')
 profile=lookup('PROGRAM_2BED_V1');corestudy.bind_profile(profile)
 return {'schema':'AP07_TWO_CORE_REQUEST206_V1','account_id':uuid.uuid4().hex,'nonce':uuid.uuid4().hex,
 'body_hex':body.hex(),'raw':raw,'profile':profile,'choices':list(CHOICES),'source_snapshot':sources(),
 'started':started,'allocated_seconds':seconds,'deadline':started+seconds,'solver_seconds_per_attempt':30,
 'max_attempts':2,'task_deadline':'2026-11-19T17:33:40Z',**{k:False for k in AUTH}}
def validate_request(r,expected):
 need(digest(r)==expected,'REQUEST_DIGEST')
 need(r['schema']=='AP07_TWO_CORE_REQUEST206_V1'and all(r.get(k)is False for k in AUTH),'REQUEST_SCHEMA_AUTHORITY')
 need(all(type(r[k])is str and re.fullmatch('[0-9a-f]{32}',r[k])for k in ('account_id','nonce')),'REQUEST_IDENTITIES')
 env,raw=public_request(bytes.fromhex(r['body_hex']))
 need(digest(raw)==digest(RAW)==digest(r['raw']),'REQUEST_RAW_BINDING')
 need(digest(r['profile'])==digest(lookup('PROGRAM_2BED_V1')),'REQUEST_PROGRAM')
 need(digest(r['choices'])==digest(list(CHOICES))and type(r['max_attempts'])is int and r['max_attempts']==2,'SERVER_CHOICES')
 need(type(r['solver_seconds_per_attempt'])is int and r['solver_seconds_per_attempt']==30,'SOLVER_LIMIT')
 need(finite(r['started'])and finite(r['allocated_seconds'])and 0<r['allocated_seconds']<=LIMIT and r['deadline']==r['started']+r['allocated_seconds'],'REQUEST_TIME')
 need(r['task_deadline']=='2026-11-19T17:33:40Z','TASK_DEADLINE')
 need(digest(sources())==digest(r['source_snapshot']),'SOURCE_CHANGED')
def new_ledger(r):
 return {'schema':'AP07_SHARED_ACCOUNT206_V1','request_digest':digest(r),'account_id':r['account_id'],'limit_seconds':r['allocated_seconds'],
 'used_attempts':0,'used_seconds':0,'active':None,'history':[],**{k:False for k in AUTH}}
def check_ledger(s,r):
 need(s['schema']=='AP07_SHARED_ACCOUNT206_V1'and s['request_digest']==digest(r)and s['account_id']==r['account_id'],'ACCOUNT_BINDING')
 need(digest(s['limit_seconds'])==digest(r['allocated_seconds'])and all(s.get(k)is False for k in AUTH),'ACCOUNT_LIMIT_AUTHORITY')
 need(type(s['used_attempts'])is int and 0<=s['used_attempts']<=2 and finite(s['used_seconds']),'ACCOUNT_COUNTS')
 need(type(s['history'])is list and len(s['history'])+(s['active']is not None)==s['used_attempts'],'ACCOUNT_HISTORY_COUNT')
 last=0;seen=[]
 for i,row in enumerate(s['history']):
  need(row['token']==r['account_id']+':'+str(i+1)and row['choice']==CHOICES[i],'ACCOUNT_TOKEN_CHOICE')
  need(row['request_digest']==digest(r)and finite(row['reserved_at'])and finite(row['finished_at'])and row['reserved_at']>=last and row['finished_at']>=row['reserved_at'],'ACCOUNT_TIME_ORDER')
  need(finite(row['allocated_seconds'])and 0<row['allocated_seconds']<=min(240,r['allocated_seconds']-row['reserved_at']-5),'ACCOUNT_ALLOCATION')
  need(row['outcome']in OUTCOMES and type(row['receipt_verified'])is bool,'ACCOUNT_OUTCOME')
  need(row['model_digest']is None or hash_ok(row['model_digest']),'ACCOUNT_MODEL')
  if row['receipt_verified']:
   need(row['finished_at']<min(r['allocated_seconds'],row['reserved_at']+row['allocated_seconds']),'VERIFIED_AFTER_ATTEMPT_DEADLINE')
   need(row['model_digest']is None or row['model_digest']not in seen,'VERIFIED_DUPLICATE_MODEL')
   need(row['outcome']in('VERIFIED_CORE_STUDY','NO_PROPOSAL'),'ACCOUNT_VERIFIED_STATE')
   need((hash_ok(row['model_digest'])if row['outcome']=='VERIFIED_CORE_STUDY'else row['model_digest']is None),'ACCOUNT_VERIFIED_MODEL')
  if row['model_digest']is not None:seen.append(row['model_digest'])
  last=row['finished_at']
 if s['active']is not None:
  a=s['active'];i=len(s['history'])
  need(a['token']==r['account_id']+':'+str(i+1)and a['choice']==CHOICES[i]and a['request_digest']==digest(r),'ACTIVE_TOKEN')
  need(finite(a['reserved_at'])and a['reserved_at']>=last and a['allocated_seconds']==min(240,r['allocated_seconds']-a['reserved_at']-5)and a['allocated_seconds']>0,'ACTIVE_ALLOCATION')
  last=a['reserved_at']
 need(s['used_seconds']>=last,'ACCOUNT_ELAPSED_REWIND')
def reserve(s,r,elapsed):
 check_ledger(s,r);need(s['active']is None and s['used_attempts']<2,'ACCOUNT_NO_DUPLICATE')
 need(finite(elapsed)and elapsed>=s['used_seconds'],'CLOCK_REWIND')
 if s['history']:need(s['history'][-1]['outcome']in('VERIFIED_CORE_STUDY','NO_PROPOSAL'),'STOP_AFTER_ERROR')
 allocation=min(240,r['allocated_seconds']-elapsed-5);need(allocation>0,'BUDGET_EXHAUSTED')
 out=copy.deepcopy(s);i=out['used_attempts'];out.update(used_attempts=i+1,used_seconds=elapsed,
 active={'token':r['account_id']+':'+str(i+1),'choice':CHOICES[i],'request_digest':digest(r),'reserved_at':elapsed,'allocated_seconds':allocation})
 check_ledger(out,r);return out
def finish(s,r,elapsed,outcome,verified=False,model=None):
 check_ledger(s,r);need(s['active']is not None,'FINISH_WITHOUT_RESERVATION')
 out=copy.deepcopy(s);row=out['active'];row.update(finished_at=elapsed,outcome=outcome,receipt_verified=verified,model_digest=model)
 if model is not None and any(x['model_digest']==model for x in out['history']):row.update(outcome='REPEATED_MODEL',receipt_verified=False)
 if elapsed>=min(r['allocated_seconds'],row['reserved_at']+row['allocated_seconds']):row.update(outcome='TIMED_OUT',receipt_verified=False)
 out.update(active=None,used_seconds=elapsed);out['history'].append(row);check_ledger(out,r);return out
def invalidate(ledger,observations,reason):
 for row in ledger['history']:
  row.setdefault('observed_receipt_verified',row['receipt_verified'])
  row.setdefault('observed_outcome',row['outcome'])
  row.update(receipt_verified=False,outcome='TIMED_OUT'if reason=='BUDGET_EXHAUSTED'else'RECEIPT_ERROR')
 for row in observations:
  row.setdefault('observed_receipt_verified',row.get('receipt_verified',False))
  row.update(receipt_verified=False,evidence_usable=False)
def wait_process(proc,seconds,group=False):
 need(finite(seconds)and seconds>0,'WAIT_BUDGET')
 timed=False;killed=False
 try:proc.wait(timeout=seconds)
 except subprocess.TimeoutExpired:
  timed=True
  try:
   if group:os.killpg(proc.pid,signal.SIGKILL)
   else:proc.kill()
   killed=True
  except ProcessLookupError:pass
  finally:proc.wait()
 return {'timed_out':timed,'kill_sent':killed,'wait_completed':proc.poll()is not None,'returncode':proc.returncode}
def attempt_nonce(r,index):
 need(type(index)is int and index in(0,1),'ATTEMPT_INDEX')
 return digest([r['nonce'],r['account_id'],index,CHOICES[index]])[:32]
def consume(r,index,summary,reports):
 """Consistency of full reports from this pinned child, not independent raw-model replay."""
 nonce=attempt_nonce(r,index);choice=CHOICES[index]
 need(type(summary)is dict and type(reports)is dict,'FULL_REPORTS_REQUIRED')
 need(summary.get('run_nonce')==nonce and summary.get('choice')==choice,'CHILD_NONCE_CHOICE')
 need(all(summary.get(k)is False for k in AUTH)and summary.get('completed')is True and summary.get('integrity_verified')is True,'CHILD_COMPLETION')
 need(summary.get('current_four')=='NOT_EVALUATED_CORE_CHOICE_ADAPTER_MISSING','CURRENT_SCOPE')
 core,_=corestudy.selected_core(r['raw'],choice)
 need(summary['raw_digest']==digest(r['raw'])and summary['profile_digest']==digest(r['profile'])and summary['core_digest']==digest(core),'CHILD_INPUTS')
 old={p:r['source_snapshot'][p]for p in OLD_PATHS}
 need(summary['source_digest']==digest(old),'CHILD_SOURCE')
 need(type(summary['report_digests'])is dict and set(reports)==set(summary['report_digests']),'REPORT_SET')
 need(all(digest(reports[k])==summary['report_digests'][k]for k in reports),'REPORT_HASH')
 if summary['state']=='NO_PROPOSAL_NO_INFEASIBILITY_CLAIM':
  need(not reports and summary.get('construction_observed')is False and summary.get('model_digest')is None,'NO_PROPOSAL_CONTRADICTION')
  return {'outcome':'NO_PROPOSAL','model_digest':None,'report_count':0,'report_digests':{},'current_four':'NOT_EVALUATED'}
 need(summary['state']=='FULL_REPORTS_RETAINED_NOT_QUALIFIED'and set(reports)==REPORTS,'COMPLETE_REPORT_SET')
 model=summary['model_digest'];need(hash_ok(model),'MODEL_DIGEST')
 ir=reports['independent_replay'];ca=reports['core_assessment'];neg=reports['actual_detached_negatives'];physical=reports['physical']
 need(ir.get('verified')is True and ir.get('authority')is False and ir['model_hash']==model and ir['receipt_digest']==summary['receipt_digest'],'INDEPENDENT_REPLAY_BINDING')
 need(summary.get('independent_origin_verified')is True,'ORIGIN_OBSERVATION')
 need(ca['choice']==choice and ca['run_nonce']==nonce and ca['model_hash']==model and ca['raw_hash']==digest(r['raw'])and ca['profile_hash']==digest(r['profile'])and ca['core_hash']==digest(core)and ca['source_hash']==digest(old)and ca['origin_receipt_hash']==summary['receipt_digest'],'CORE_ASSESSMENT_BINDING')
 need(all(ca.get(k)is False for k in AUTH),'CORE_AUTHORITY')
 preds={k:reports[k]for k in ('core_partition','core_concept','opening_hosts')}
 need(digest(ca['predicates'])==digest(preds),'CORE_PREDICATES')
 verified=corestudy.predicates_verified(preds)
 need(type(ca['core_scoped_verified'])is bool and ca['core_scoped_verified']is verified and summary['core_scoped_verified']is verified and ca['state']==('PASS_CORE_SCOPE_ONLY'if verified else'BLOCKED_CORE_SCOPE'),'CORE_SUMMARY')
 need(physical['model_hash']==model and reports['original_replay']['model_hash']==model and neg['model_hash']==model,'FULL_MODEL_REPORT_BINDING')
 need(neg['original_unchanged']is True and neg['all_expected_rejected']is True and type(neg['rows'])is list and len(neg['rows'])==6,'NEGATIVE_REPORT')
 need(all(x['base_model_hash']==model and x['binding_rejected']is True and x['direct_geometry_rejected']is True for x in neg['rows']),'NEGATIVE_MODEL_BINDING')
 need(ca['program_hash']==summary['program_digest'],'PROGRAM_MODEL_REPORT')
 from one_bed_pair_source_study import code_counts
 need(summary['physical_status']==physical.get('status')and digest(summary['physical_error_counts'])==digest(code_counts(physical.get('errors',[])))and digest(summary['physical_pending_counts'])==digest(code_counts(physical.get('pending',[]))),'PHYSICAL_SUMMARY')
 need(summary['legacy_replay_verified']is(reports['original_replay'].get('verified')is True),'LEGACY_REPLAY_SUMMARY')
 return {'outcome':'VERIFIED_CORE_STUDY','model_digest':model,'report_count':len(reports),'report_digests':copy.deepcopy(summary['report_digests']),
 'core_scoped_verified':verified,'physical_status':physical.get('status'),'physical_error_counts':summary['physical_error_counts'],'physical_pending_counts':summary['physical_pending_counts'],
 'legacy_replay_verified':summary['legacy_replay_verified'],'current_four':'NOT_EVALUATED','negative_count':6}
def attempt(folder,index):
 r=read(folder/'request.json');expected=read(folder/'request-digest.json');validate_request(r,expected)
 nonce=attempt_nonce(r,index);dest=folder/('attempt-'+str(index));pgid=os.getpgrp()
 corestudy.child(dest,CHOICES[index],nonce)
 validate_request(r,expected)
 save(dest/'process-anchor.json',{'request_digest':expected,'account_id':r['account_id'],'nonce':nonce,'choice':CHOICES[index],'pid':os.getpid(),'pgid':pgid})
def worker(folder):
 r=read(folder/'request.json');expected=read(folder/'request-digest.json');ledger=new_ledger(r);observations=[];full={};state='STARTED';error=None
 def elapsed():return time.monotonic()-r['started']
 def checkpoint():
  save(folder/'progress.json',{'schema':'AP07_CORE_ORCHESTRATION206_V1','state':state,'request_digest':expected,'account_id':r['account_id'],'ledger':ledger,'observations':observations,
   'error_code':error,'raw_reports_retained_until_cleanup':True,'durable_archive_created':False,'quality_winner':None,'ap07_complete':False,
   'remaining_stages':{'SPLIT':'NOT_IMPLEMENTED','PLACEMENT_ALTERNATIVES':'NOT_ENUMERATED','OPTIONAL_NONBED_MERGE':'NOT_IMPLEMENTED','LOWER_PROGRAM':'BLOCKED_ADAPTER_DEPENDENCY'},
   **{k:False for k in AUTH}})
 try:
  validate_request(r,expected);checkpoint()
  for index in range(2):
   ledger=reserve(ledger,r,elapsed());state='RESERVED';checkpoint();active=copy.deepcopy(ledger['active'])
   proc=subprocess.Popen([sys.executable,'-B',__file__,'--attempt',str(folder),str(index)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   process={'pid':proc.pid,'pgid':os.getpgid(proc.pid),'worker_pgid':os.getpgrp(),'timed_out':False,'kill_sent':False}
   need(process['pgid']==process['worker_pgid'],'CHILD_PROCESS_GROUP')
   process.update(wait_process(proc,min(active['allocated_seconds'],max(.001,r['deadline']-time.monotonic()-3))))
   dest=folder/('attempt-'+str(index));row={'choice':CHOICES[index],'token':active['token'],'process':process,'receipt_verified':False,'evidence_usable':False,'outcome':'EXECUTION_ERROR','model_digest':None}
   observations.append(row);full[index]={}
   try:
    for name in ('summary','reports','process-anchor'):
     p=dest/(name+'.json')
     if p.exists():full[index][name]=read(p)
    row['observed_file_digests']={k:digest(v)for k,v in full[index].items()}
    if process['timed_out']:row['outcome']='TIMED_OUT'
    else:
     need(proc.returncode==0 and process['wait_completed'],'CHILD_PROCESS_FAILED')
     a=full[index]['process-anchor'];need(a=={'request_digest':expected,'account_id':r['account_id'],'nonce':attempt_nonce(r,index),'choice':CHOICES[index],'pid':proc.pid,'pgid':process['worker_pgid']},'PROCESS_ANCHOR')
     bound=consume(r,index,full[index]['summary'],full[index]['reports']);validate_request(r,expected)
     need(all(digest(read(dest/(k+'.json')))==digest(v)for k,v in full[index].items()),'REPORT_DISK_CHANGED')
     row.update(bound,receipt_verified=True,evidence_usable=True)
   except Exception as ex:row.update(outcome='RECEIPT_ERROR',error_type=type(ex).__name__,error_code=str(ex)if re.fullmatch('[A-Z0-9_:]+',str(ex))else'NONPUBLIC_DETAIL',receipt_verified=False,evidence_usable=False)
   ledger=finish(ledger,r,elapsed(),row['outcome'],row['receipt_verified'],row.get('model_digest'))
   row['outcome']=ledger['history'][-1]['outcome'];row['receipt_verified']=ledger['history'][-1]['receipt_verified'];row['evidence_usable']=row['receipt_verified']
   state='ATTEMPT_FINISHED';checkpoint()
   if row['outcome']not in('VERIFIED_CORE_STUDY','NO_PROPOSAL'):break
  validate_request(r,expected);check_ledger(ledger,r)
  ledger['used_seconds']=elapsed();check_ledger(ledger,r)
  if ledger['used_seconds']>=r['allocated_seconds']:state='BUDGET_EXHAUSTED'
  else:state='TWO_CORE_ATTEMPTS_RECORDED_NOT_SELECTED'if len(ledger['history'])==2 and all(x['receipt_verified']and x['outcome']in('VERIFIED_CORE_STUDY','NO_PROPOSAL')for x in ledger['history'])else'PARTIAL_ATTEMPTS_RECORDED'
 except Exception as ex:
  state='FAILED_CLOSED';error=type(ex).__name__
 finally:
  try:validate_request(r,expected);check_ledger(ledger,r)
  except Exception as ex:state='SOURCE_OR_LEDGER_ERROR';error=type(ex).__name__
  ledger['used_seconds']=max(ledger['used_seconds'],elapsed())
  if ledger['used_seconds']>=r['allocated_seconds']:state='BUDGET_EXHAUSTED'
  if state in('FAILED_CLOSED','SOURCE_OR_LEDGER_ERROR','BUDGET_EXHAUSTED'):
   invalidate(ledger,observations,state)
  checkpoint()
def run(body=BODY):
 started=time.monotonic();remaining=(TASK_END-datetime.now(timezone.utc)).total_seconds();seconds=min(LIMIT,remaining-5)
 need(seconds>0,'TASK_TIMEBOX_EXPIRED')
 r=make_request(body,started,seconds);expected=digest(r)
 with tempfile.TemporaryDirectory(prefix='ap07-two-core-')as directory:
  folder=Path(directory);save(folder/'request.json',r);save(folder/'request-digest.json',expected)
  proc=subprocess.Popen([sys.executable,'-B',__file__,'--worker',str(folder)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
  pgid=os.getpgid(proc.pid)
  receipt=wait_process(proc,max(.001,r['deadline']-time.monotonic()),True)
  timed=receipt['timed_out']
  try:out=read(folder/'progress.json')
  except Exception:out={'state':'NO_READABLE_PROGRESS','observations':[]}
  receipt.update(pid=proc.pid,pgid=pgid,elapsed_seconds=time.monotonic()-started)
  valid=False
  try:
   validate_request(r,expected);need(out['request_digest']==expected and out['account_id']==r['account_id'],'OUTER_REQUEST')
   check_ledger(out['ledger'],r);need(proc.returncode==0 and not timed and receipt['wait_completed']and out['state']=='TWO_CORE_ATTEMPTS_RECORDED_NOT_SELECTED','OUTER_COMPLETION')
   need(len(out['observations'])==2 and all(x['receipt_verified']and x['evidence_usable']for x in out['observations']),'OUTER_RECEIPT_ROWS')
   for index,row in enumerate(out['observations']):
    dest=folder/('attempt-'+str(index));summary=read(dest/'summary.json');reports=read(dest/'reports.json')
    rebound=consume(r,index,summary,reports)
    need(all(digest(row[k])==digest(v)for k,v in rebound.items()),'OUTER_OBSERVATION_BINDING')
    h=out['ledger']['history'][index]
    need(h['choice']==row['choice']and h['token']==row['token']and h['outcome']==row['outcome']and h['model_digest']==row['model_digest']and h['receipt_verified']is row['receipt_verified'],'OUTER_LEDGER_OBSERVATION')
    anchor=read(dest/'process-anchor.json')
    need(anchor=={'request_digest':expected,'account_id':r['account_id'],'nonce':attempt_nonce(r,index),'choice':CHOICES[index],'pid':row['process']['pid'],'pgid':pgid},'OUTER_PROCESS_ANCHOR')
    need(row['process']['wait_completed']is True and row['process']['returncode']==0 and row['process']['timed_out']is False,'OUTER_CHILD_PROCESS')
   validate_request(r,expected)
   receipt['elapsed_seconds']=time.monotonic()-started
   out['ledger']['used_seconds']=max(out['ledger']['used_seconds'],receipt['elapsed_seconds'])
   check_ledger(out['ledger'],r)
   need(receipt['elapsed_seconds']<seconds,'OUTER_BUDGET')
   valid=True
  except Exception:pass
  if not valid:
   if 'ledger'in out:invalidate(out['ledger'],out['observations'],'OUTER_INVALID')
   out['state']='OUTER_NOT_VERIFIED'
  out.update(ledger_digest=digest(out['ledger'])if'ledger'in out else None,process_receipt=receipt,request_digest=expected,source_digest=digest(r['source_snapshot']),raw_digest=digest(r['raw']),profile_digest=digest(r['profile']),shared_seconds=seconds,
   orchestration_verified=valid,whole_ap07_complete=False,whole_task_status='PARTIAL_BLOCKED_DEPENDENCIES_AND_QUALITY',
   report_scope='Full reports consumed in same lifecycle; raw model not independently replayed from stored artifact; no durable archive',
   budget_scope='Outer worker process cap includes setup and report consumption; final parent verification measured, not preempted; encoding/network excluded',
   historical_child_main_executed=False,model_or_fullreport_uploaded=False,**{k:False for k in AUTH})
  print(json.dumps(out,sort_keys=True,allow_nan=False),flush=True)
  need(valid,'ORCHESTRATION_NOT_VERIFIED')
  return out
def dispatch(argv):
 if len(argv)==1:return run()
 if len(argv)==3 and argv[1]=='--worker':return worker(Path(argv[2]))
 if len(argv)==4 and argv[1]=='--attempt'and argv[3]in('0','1'):return attempt(Path(argv[2]),int(argv[3]))
 raise ValueError('CLI_ARGUMENTS')
if __name__=='__main__':dispatch(sys.argv)
