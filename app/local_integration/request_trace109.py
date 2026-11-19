"""Server-owned request/receipt contract for a blocked-path integration study.
Not authentication, admission or a replacement for the historical repair controller.
"""
import copy,hashlib,json,math,re,uuid
from datetime import datetime,timezone
from pathlib import Path
from public_wln_contract import parse_public,verify_public,engine_raw
from same_version_front_rear_contract import digest
from program_profile_registry import lookup
ROOT=Path(__file__).resolve().parents[2]
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
FILES=('report_lifecycle112.py','current_report_adapter111.py','obligation_admission111.py','request_budget110.py','request_trace109.html','request_trace109.js','request_trace109.py','request_trace_server109.py','cause_directed_chain108.py','cause_directed_contract108.py','cause_directed_candidate108.py','public_wln_contract.py','dimension_contract.py','program_profile_registry.py','repair_attempt_control.py')
DEADLINE=datetime(2026,11,19,15,59,9,tzinfo=timezone.utc)
def need(ok,code):
 if not ok:raise ValueError(code)
def stamp():return datetime.now(timezone.utc).isoformat()
def sources():return {n:hashlib.sha256((ROOT/'app/local_integration'/n).read_bytes()).hexdigest()for n in FILES}
def preflight(body):
 e=parse_public(body);verify_public(body,e);raw=engine_raw(e)
 ready=digest(raw)==digest({'W':'18','L':'22','n':2,'requested_count':1})
 return {'schema':'REQUEST_TRACE_PREFLIGHT109_V1','execution_ready':ready,'state':'READY_STUDY_ONLY'if ready else'UNSUPPORTED_TRACE_STUDY_CONTRACT','raw':raw,'envelope_digest':digest(e),'body_digest':hashlib.sha256(body).hexdigest(),**{k:False for k in AUTH}}
def make_request(body,*,seconds=240):
 pf=preflight(body);need(pf['execution_ready'],'UNSUPPORTED_TRACE_STUDY_CONTRACT')
 need(type(seconds)in(int,float)and math.isfinite(seconds)and 0<seconds<=240,'REQUEST_BUDGET')
 seconds=min(seconds,(DEADLINE-datetime.now(timezone.utc)).total_seconds()-5)
 need(seconds>0,'TASK_TIMEBOX_EXPIRED')
 nonce=uuid.uuid4().hex
 return {'schema':'REQUEST_TRACE_JOB109_V1','body_hex':body.hex(),'preflight':pf,'nonce':nonce,'account_id':uuid.uuid4().hex,
  'programme_id':'PROGRAM_2BED_V1','programme_digest':digest(lookup('PROGRAM_2BED_V1')),'runtime':'CAUSE108_PARENT_ONLY',
  'source_snapshot':sources(),'allocated_seconds':seconds,'created_utc':stamp(),'deadline_utc':DEADLINE.isoformat(),
  'parent_only':True,**{k:False for k in AUTH}}
def validate_request(r,expected):
 need(type(r)is dict and digest(r)==expected,'REQUEST_DIGEST')
 need(set(r)=={'schema','body_hex','preflight','nonce','account_id','programme_id','programme_digest','runtime','source_snapshot','allocated_seconds','created_utc','deadline_utc','parent_only',*AUTH},'REQUEST_FIELDS')
 need(r['schema']=='REQUEST_TRACE_JOB109_V1'and r['runtime']=='CAUSE108_PARENT_ONLY'and r['parent_only']is True,'REQUEST_RUNTIME')
 for k in ('nonce','account_id'):need(type(r[k])is str and re.fullmatch('[0-9a-f]{32}',r[k])is not None,'REQUEST_ID')
 need(r['nonce']!=r['account_id'],'REQUEST_DISTINCT_IDS')
 need(type(r['body_hex'])is str,'REQUEST_BODY')
 pf=preflight(bytes.fromhex(r['body_hex']))
 need(pf['execution_ready']and digest(pf)==digest(r['preflight']),'REQUEST_PREFLIGHT')
 need(r['programme_id']=='PROGRAM_2BED_V1'and r['programme_digest']==digest(lookup(r['programme_id'])),'REQUEST_PROGRAMME')
 need(type(r['allocated_seconds'])in(int,float)and math.isfinite(r['allocated_seconds'])and 0<r['allocated_seconds']<=240,'REQUEST_BUDGET')
 need(r['deadline_utc']==DEADLINE.isoformat()and datetime.fromisoformat(r['created_utc'])<=DEADLINE,'REQUEST_TIME')
 need(digest(r['source_snapshot'])==digest(sources()),'REQUEST_SOURCE')
 need(all(r.get(k)is False for k in AUTH),'REQUEST_AUTHORITY')
 return pf
def bind_result(r,expected,out,reports,process):
 validate_request(r,expected)
 need(type(out)is dict and out.get('completed')is True and out.get('integrity_verified')is True,'RESULT_INTEGRITY')
 need(type(process['returncode'])is int and process['returncode']==0 and process['wait_completed']is True and process['timed_out']is False,'RESULT_PROCESS')
 need(out.get('state')in('BLOCKED_NO_SUPPORTED_CAUSE','BLOCKED_REPAIR_CONTROLLER_ADAPTER','BLOCKED_NO_PARENT_PROPOSAL'),'RESULT_STATE')
 need(out.get('request_digest')==expected and out.get('run_nonce')==r['nonce']and out.get('request_account_id')==r['account_id'],'RESULT_REQUEST_ID')
 need(out.get('raw_digest')==digest(r['preflight']['raw'])and out.get('profile_digest')==r['programme_digest'],'RESULT_INPUT_PROGRAMME')
 need(out.get('request_source_digest')==digest(r['source_snapshot']),'RESULT_SOURCE')
 need(type(out.get('attempt_count'))is int and out['attempt_count']==1 and out.get('child_observed')is False and out.get('cause_repair_verified')is False,'RESULT_PARENT_ONLY')
 need(all(out.get(k)is False for k in AUTH),'RESULT_AUTHORITY')
 pins=out.get('report_digests');need(type(pins)is dict and pins and type(reports)is dict,'RESULT_REPORTS')
 need(set(reports)==set(pins)and all(digest(reports[k])==v for k,v in pins.items()),'RESULT_REPORT_DIGEST')
 if out['state']=='BLOCKED_NO_PARENT_PROPOSAL':
  need(out.get('parent_observed')is False and 'parent_no_witness'in reports,'RESULT_NO_PARENT')
 else:
  need(out.get('parent_observed')is True,'RESULT_PARENT')
  mh=out.get('parent_model_digest')
  need(reports['parent_physical']['model_hash']==mh and reports['parent_replay']['model_hash']==mh and reports['parent_replay']['verified']is True,'RESULT_MODEL_REPORT')
  physical=reports['parent_physical']
  from one_bed_pair_source_study import code_counts
  physical_summary={'status':physical.get('status'),'errors':code_counts(physical.get('errors',[])),'pending':code_counts(physical.get('pending',[])),'not_evaluated_count':len(physical.get('not_evaluated',[])),'out_of_scope_count':len(physical.get('out_of_scope',[]))}
  need(digest(out.get('parent_physical'))==digest(physical_summary),'RESULT_PHYSICAL_SUMMARY')
  cause=reports['parent_cause'];need(cause['model_digest']==mh,'RESULT_CAUSE_MODEL')
  need(digest(cause['selected_causes'])==digest(out.get('selected_causes')),'RESULT_CAUSE')
  need((not cause['selected_causes'])==(out['state']=='BLOCKED_NO_SUPPORTED_CAUSE'),'RESULT_CAUSE_STATE')
  mods=('current_programme_evaluator','source_guest_route_evaluator','source_living_evaluator','source_wall_function_evaluator')
  need(set(out['parent_current'])==set(mods),'RESULT_CURRENT_SET')
  for mod in mods:
   v=reports['parent_current_'+mod]
   need(v['model_digest']==mh and v['integrity_verified']is True and v['state']in('PASS','FAIL','UNKNOWN','NOT_EVALUATED')and all(v.get(k)is False for k in AUTH),'RESULT_CURRENT')
   errors=sum(x.get('kind')in('EVALUATOR_OR_SOURCE_BINDING_ERROR','INTEGRITY_ERROR')for x in v.get('findings',[]))
   errors+=sum(x.get('state')in('UNKNOWN_EVALUATOR_OR_BINDING_ERROR','EVALUATOR_ERROR')for u in v.get('units',[])for x in u.get('routes',[]))
   errors+=sum(x.get('state')=='EVALUATOR_ERROR'for u in v.get('units',[])for st in u.get('studies',[])for x in st.get('routes',[]))
   actual={'state':v['state'],'integrity_verified':v.get('integrity_verified')is True,'missing_count':len(v.get('missing',[])),'evaluator_error_count':errors}
   need(digest(out['parent_current'][mod])==digest(actual)and not actual['missing_count']and not errors,'RESULT_CURRENT_SUMMARY')
 return True
def invalidate(result):
 result['receipt_verified']=False
 prior={}
 for k in ('parent_model_digest','full_report_digests','current_states','parent_physical','runtime_trace','lifecycle_admission'):
  if k in result:prior[k]=result.pop(k)
 if prior:result['observed_unverified_evidence']=prior
 result['evidence_usable']=False
 return result
def finalize_result(base,request,expected,elapsed,process_started):
 import time
 import request_budget110 as ledger
 began=time.monotonic();initial_elapsed=elapsed
 base['result_state_before_finalization']=base.get('state','FAILED_CLOSED')
 reserved=copy.deepcopy(base['account']);reserved_digest=base['account_reserved_digest']
 try:validate_request(request,expected);base['source_integrity_verified']=True
 except Exception:base.update(state='SOURCE_INTEGRITY_ERROR',source_integrity_verified=False,receipt_verified=False)
 elapsed+=time.monotonic()-began
 observed_state=base.get('state','FAILED_CLOSED')
 if observed_state not in ledger.REPORTED:observed_state='FAILED_CLOSED'
 process=base.get('process')
 if process is not None and process.get('timed_out')is True:observed_state='TIMED_OUT';base['receipt_verified']=False
 observed_verified=base['receipt_verified']
 try:
  a=ledger.anchor(request,expected)
  account=ledger.finish(reserved,reserved_digest,a,reserved['active']['token'],elapsed_seconds=elapsed,
   reported_outcome=observed_state,model_digest=base.get('parent_model_digest'),receipt_verified=observed_verified,
   process_digest=None if process is None else digest(process),internal_attempt_count=base.get('attempt_count'),
   internal_count_verified=observed_verified)
  ledger.check(account,digest(account),a)
  base.update(account=account,account_digest=digest(account),account_finalization_verified=True,state=account['state'],receipt_verified=account['history'][-1]['receipt_verified'])
 except Exception as ex:
  base.update(state='ACCOUNT_FINALIZATION_FAILED',account_finalization_verified=False,receipt_verified=False,
   account_reserved=reserved,account_reserved_digest=reserved_digest,account_error_type=type(ex).__name__)
  # Do not release or reset a reservation whose finalization failed.
  base['account']=reserved; base['account_digest']=digest(reserved)
 # Final monotonic eligibility cutoff follows source verification and ledger validation.
 # The following fixed-shape record/JSON encoding is not a preempted runtime phase.
 elapsed=initial_elapsed+time.monotonic()-began
 if base.get('account_finalization_verified')is True:
  account=base['account'];row=account['history'][0]
  account['used_seconds']=elapsed;row['elapsed_seconds']=elapsed
  row['outcome'],row['receipt_verified']=ledger.terminal(row,account['anchor'])
  account['state']=row['outcome']
  base.update(state=account['state'],receipt_verified=row['receipt_verified'],account_digest=digest(account))
 if not base['receipt_verified']:invalidate(base)
 else:base['evidence_usable']=True
 base.update(elapsed_seconds=elapsed,durable_full_reports=False,
  budget_scope='Process group is preempted; wrapper/source/receipt verification and provisional ledger validation are measured until final eligibility cutoff and invalidated at deadline, not preempted. Fixed-shape final record/JSON encoding and HTTP body read/network delivery excluded.',
  original_outcome_observed=observed_state,process_started_observed=process_started)
 base['trace'].append({'stage':'REQUEST_FINALIZED','utc':stamp(),'state':base['state']})
 return base
def run(body):
 """Real process wiring; no cached receipt or controlled-worker success seam."""
 import tempfile,time
 from repair_attempt_control import run_bounded
 import inspect
 need(Path(inspect.getsourcefile(run_bounded)).resolve()==ROOT/'app/local_integration/repair_attempt_control.py','PROCESS_IMPORT')
 started=time.monotonic();trace=[{'stage':'HTTP_REQUEST_ACCEPTED','utc':stamp()}]
 pf=preflight(body);trace.append({'stage':'PUBLIC_V3_PREFLIGHT','utc':stamp(),'state':pf['state']})
 base={'schema':'REQUEST_TRACE_RESULT109_V1','trace':trace,'input_valid':True,'runtime_scope':'Separate18x22/n2 study; original18x20 public runtime unchanged','model_payload':None,'download_available':False,'child_count':0,'receipt_verified':False,**{k:False for k in AUTH}}
 if not pf['execution_ready']:return {**base,'state':pf['state'],'attempt_count':0}
 request=make_request(body);expected=digest(request)
 base.update(request_digest=expected,nonce=request['nonce'],account_id=request['account_id'],source_digest=digest(request['source_snapshot']))
 import request_budget110 as ledger
 a=ledger.anchor(request,expected);account=ledger.create(a);account,allocation=ledger.reserve(account,digest(account),a)
 base['account_reserved_digest']=digest(account)
 base['account']=account;trace.append({'stage':'REQUEST_ACCOUNT_RESERVED','utc':stamp(),'account_digest':digest(account)})
 process=None;out=None;reports=None
 try:
  with tempfile.TemporaryDirectory(prefix='request-trace109-')as tmp:
   root=Path(tmp);req=root/'request.json';req.write_text(json.dumps(request,sort_keys=True,allow_nan=False));dest=root/'child'
   remaining=request['allocated_seconds']-(time.monotonic()-started);need(remaining>0,'REQUEST_BUDGET_EXHAUSTED')
   trace.append({'stage':'PARENT_RUNTIME_DISPATCHED','utc':stamp()})
   import sys
   process=run_bounded([sys.executable,'-B',str(ROOT/'app/local_integration/cause_directed_chain108.py'),'--request-child',str(dest),str(req),expected],remaining)
   trace.append({'stage':'PROCESS_WAIT_COMPLETED','utc':stamp()})
   base['process']={k:process[k]for k in ('timed_out','kill_sent','wait_completed','returncode','elapsed_seconds','allocated_seconds')}
   from report_lifecycle112 import consume
   need(Path(inspect.getsourcefile(consume)).resolve()==ROOT/'app/local_integration/report_lifecycle112.py','LIFECYCLE_IMPORT')
   # Private evidence is consumed inside this live request's temporary lifecycle,
   # never returned in HTTP or uploaded. Full reports remain nondurable.
   out,reports,lifecycle=consume(dest,request,expected,process,account,base['account_reserved_digest'])
   base['observed_summary_digest']=digest(out)
   base['lifecycle_admission']=copy.deepcopy(lifecycle['safe_summary'])
   base.update(receipt_verified=True,state=out['state'],attempt_count=out['attempt_count'],parent_model_digest=out.get('parent_model_digest'),
    full_report_digests=copy.deepcopy(out['report_digests']),current_states={k:v['state']for k,v in out.get('parent_current',{}).items()},
    parent_physical=copy.deepcopy(out.get('parent_physical')),runtime_trace=copy.deepcopy(out.get('stage_trace',[])))
   trace.append({'stage':'REAL_REPORT_BINDING_VERIFIED','utc':stamp()})
   trace.append({'stage':'REPAIR_CONTROLLER_NOT_EXECUTED','utc':stamp(),'reason':'SKIPPED_NO_SUPPORTED_CAUSE'if out['state']=='BLOCKED_NO_SUPPORTED_CAUSE'else'SKIPPED_DEPENDENCY'})
 except Exception as ex:
  # Private evidence remains handler-local; only non-content observations escape.
  observed=getattr(ex,'private_evidence',None)
  if type(observed)is dict:
   failed_adapter=observed.get('adapter',{})
   base['lifecycle_error_observation']={'state':'OBSERVED_UNVERIFIED','durable':False,
    'raw_report_count':len(observed['original_reports']) if type(observed.get('original_reports')) in (dict,list) else 0,
    'raw_reports_digest':observed.get('raw_reports_digest'),
    'adapter_error_count':len(failed_adapter.get('errors',[]))}
  base.update(state='FAILED_CLOSED',receipt_verified=False,error_type=type(ex).__name__,error_code=str(ex)if re.fullmatch('[A-Z0-9_:]+',str(ex))else'NONPUBLIC_DETAIL_RETAINED_ONLY')
 finally:
  finalize_result(base,request,expected,time.monotonic()-started,process is not None)
 return base
