"""Live single-contract scheduler. Bounded study only; no lower-program execution."""
import copy,json,math,os,signal,subprocess,sys,time,uuid,hashlib
from pathlib import Path
from fractions import Fraction as F
from public_wln_contract import parse_public,verify_public,engine_raw
from same_version_front_rear_contract import ROOT,bind_request,digest
from program_profile_registry import lookup
from program_search_order import policy,stage_record,lower_program_transition,STAGES
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
LIMITS={'max_attempts':1,'solver_seconds':30,'shared_child_seconds':180}
def budgets(value=None):
 b=copy.deepcopy(LIMITS if value is None else value)
 if type(b) is not dict or set(b)!=set(LIMITS):raise ValueError('LIVE_BUDGET_FIELDS')
 if type(b['max_attempts']) is not int or b['max_attempts']!=1:raise ValueError('LIVE_ONE_ATTEMPT_ONLY')
 for k in ('solver_seconds','shared_child_seconds'):
  if type(b[k]) not in (int,float) or not math.isfinite(b[k]) or not 0<b[k]<=LIMITS[k]:raise ValueError('LIVE_BUDGET_FINITE_LIMIT')
 if b['solver_seconds']>=b['shared_child_seconds']:raise ValueError('LIVE_SOLVER_OUTER_ORDER')
 return b
def preflight(body):
 e=parse_public(body);verify_public(body,e)
 base={'public_envelope':e,'input_valid':True,**{k:False for k in AUTH}}
 if e['canonical_request']['unit_count']!=2:return {**base,'state':'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT','execution_ready':False}
 raw=engine_raw(e)
 if raw!={'W':'18','L':'20','n':2,'requested_count':1}:return {**base,'state':'UNSUPPORTED_SELECTED_SAME_VERSION_CASE','execution_ready':False}
 return {**base,'state':'READY_SCOPED_CONTRACT_ONLY','execution_ready':True,'binding':bind_request(body,e,'PROGRAM_2BED_V1')}
def save(path,value):
 path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False))
def child(directory):
 request=json.loads((directory/'request.json').read_text());body=bytes.fromhex(request['body_hex'])
 pf=preflight(body)
 if digest(pf)!=request['preflight_digest']:raise ValueError('CHILD_REQUEST_BINDING')
 limits=budgets(request['budget']);nonce=request['nonce']
 out={'schema':'LIVE_SCHEDULER_CHILD_V1','nonce':nonce,'request_digest':digest(request),'preflight_digest':digest(pf),
  'programme_digest':pf['binding']['program_registry_digest'],'contract_digest':pf['binding']['contract_digest'],
  'stages':[],'state':'STARTED','assessments':{},**{k:False for k in AUTH}}
 save(directory/'child-progress.json',out)
 from front_rear_runtime_adapter import run
 runtime=run(body,solver_seconds=limits['solver_seconds'])
 save(directory/'runtime-bundle.json',runtime)
 out['runtime_digest']=digest(runtime);out['model_digest']=runtime.get('model_digest')
 out['runtime_status']=runtime['status'];out['stages'].append('ORIGINAL_RUNTIME_RETURNED')
 out['constructor_called']=runtime['constructor_called'];out['model_binding_verified']=runtime['model_binding_verified']
 save(directory/'child-progress.json',out)
 if not runtime['completed'] or not runtime['model_binding_verified']:
  out['state']='ORIGINAL_RUNTIME_INCOMPLETE_NO_FOUR_REPORT_DECISION';save(directory/'child-complete.json',out);return
 from current_programme_evaluator import assess as programme
 from source_guest_route_evaluator import assess as guest
 from source_living_evaluator import assess as living
 from source_wall_function_evaluator import assess as walls
 for cid,fn in [('CURRENT_PROGRAM_SUITABILITY',programme),('KITCHEN_GUEST_PATH_SEPARATION',guest),('CONTINUOUS_USEFUL_LIVING',living),('NONFUNCTIONAL_WALL_EXCLUSION',walls)]:
  result=fn(runtime);out['assessments'][cid]=result
  if digest(runtime)!=out['runtime_digest']:raise ValueError('CHILD_RUNTIME_MUTATION')
  save(directory/(cid+'.json'),result);out['stages'].append(cid);save(directory/'child-progress.json',out)
 from current_four_decision import assemble
 decision=assemble(runtime,out['assessments'],{k:digest(v) for k,v in out['assessments'].items()})
 save(directory/'decision.json',decision)
 out['decision']=decision['decision'];out['decision_digest']=digest(decision)
 out['state']='LIVE_ORIGINAL_CHAIN_AND_CURRENT_DECISION_COMPLETED_NOT_QUALIFIED';save(directory/'child-complete.json',out)
def bind_completed(result,request,runtime,decision):
 if result.get('state') not in ('LIVE_ORIGINAL_CHAIN_AND_CURRENT_DECISION_COMPLETED_NOT_QUALIFIED','ORIGINAL_RUNTIME_INCOMPLETE_NO_FOUR_REPORT_DECISION'):raise ValueError('LIVE_STATE_ENUM')
 if result['nonce']!=request['nonce'] or result['request_digest']!=digest(request):raise ValueError('LIVE_RECEIPT_NONCE_REQUEST')
 pf=preflight(bytes.fromhex(request['body_hex']))
 for key,value in [('preflight_digest',digest(pf)),('programme_digest',pf['binding']['program_registry_digest']),('contract_digest',pf['binding']['contract_digest'])]:
  if digest(result[key])!=digest(value):raise ValueError('LIVE_RECEIPT_BINDING:'+key)
 if any(result.get(k) is not False for k in AUTH):raise ValueError('LIVE_AUTHORITY')
 if digest(runtime['binding'])!=digest(pf['binding']):raise ValueError('LIVE_RUNTIME_REQUEST_BINDING')
 if result['runtime_digest']!=digest(runtime):raise ValueError('LIVE_RUNTIME_DIGEST')
 if result['model_digest']!=runtime.get('model_digest'):raise ValueError('LIVE_MODEL_DIGEST')
 if result['state']=='LIVE_ORIGINAL_CHAIN_AND_CURRENT_DECISION_COMPLETED_NOT_QUALIFIED':
  if runtime.get('completed') is not True or runtime.get('model_binding_verified') is not True:raise ValueError('LIVE_COMPLETED_RUNTIME_REQUIRED')
  if decision is None or decision.get('integrity_verified') is not True or any(decision.get(k) is not False for k in AUTH):raise ValueError('LIVE_DECISION_INTEGRITY_AUTHORITY')
  if any(runtime.get(k) is not False for k in AUTH):raise ValueError('LIVE_RUNTIME_AUTHORITY')
  if result['decision_digest']!=digest(decision) or decision['model_digest']!=result['model_digest']:raise ValueError('LIVE_DECISION_BINDING')
  if digest(result['decision'])!=digest(decision['decision']):raise ValueError('LIVE_DECISION_CHANGED')
 return True
def run_live(body,*,budget=None):
 limits=budgets(budget);pf=preflight(body)
 out={'schema':'AUTOMATIC_PROGRAM_LIVE_SINGLE_CASE_V1','preflight':pf,'budget':limits,'attempts':[],
  'fresh_model_executed':False,'selected_alternative':None,'quality_winner':False,'production_supported':False,
  'ap07_complete':False,'global_infeasibility_proven':False,
  'scope':'Only original FRONT_REAR18x20/n2 approved two-bedroom contract. One actual attempt, not variable-dimension coverage or complete programme search.',
  **{k:False for k in AUTH}}
 if not pf['execution_ready']:out['state']=pf['state'];return out
 from front_rear_runtime_adapter import source_audit
 from producer_provenance import snapshot,require_unchanged
 paths=['app/local_integration/'+s for s in ('live_program_scheduler.py','automatic_program_search.py','program_search_order.py','current_four_decision.py','current_programme_evaluator.py','source_guest_route_evaluator.py','source_living_evaluator.py','source_wall_function_evaluator.py')]
 snap=snapshot(ROOT,paths);before=source_audit()
 nonce=uuid.uuid4().hex;directory=ROOT/'live-program-evidence'/nonce;directory.mkdir(parents=True,exist_ok=False)
 request={'schema':'LIVE_PROGRAM_ATTEMPT_V1','nonce':nonce,'body_hex':body.hex(),'preflight_digest':digest(pf),'budget':limits}
 save(directory/'request.json',request)
 attempt_id='PROGRAM_2BED_V1:'+nonce
 row={'attempt_id':attempt_id,'programme_id':'PROGRAM_2BED_V1','programme_digest':pf['binding']['program_registry_digest'],'contract_digest':pf['binding']['contract_digest'],
  'attempted':True,'state':'RUNNING','budget_account_id':nonce,'allocated_child_seconds':limits['shared_child_seconds'],'nonce':nonce}
 out['attempts'].append(row);out['source_snapshot']=snap
 out['budget_scope']='Single shared child wall limit includes original runtime and four current assessments/decision; solver limit30 is internal. Parent pre/post source audits and setup excluded and timed separately. No reset for lower programme.'
 out['head_sha']=os.environ.get('GITHUB_SHA');out['policy']=policy()
 start=time.monotonic();proc=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'--child',str(directory)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 timed=False;killed=False
 try:stdout,stderr=proc.communicate(timeout=limits['shared_child_seconds'])
 except subprocess.TimeoutExpired:
  timed=True
  try:os.killpg(proc.pid,signal.SIGKILL);killed=True
  except ProcessLookupError:pass
  stdout,stderr=proc.communicate()
 elapsed=time.monotonic()-start
 (directory/'stdout.txt').write_text(stdout);(directory/'stderr.txt').write_text(stderr)
 row.update(timed_out=timed,kill_sent=killed,wait_completed=proc.poll() is not None,returncode=proc.returncode,elapsed_seconds=elapsed)
 ledger={'account_id':nonce,'limit_attempts':1,'used_attempts':1,'limit_seconds':limits['shared_child_seconds'],'used_seconds':elapsed}
 out['budget_ledger']=ledger
 runtime=None;result=None;decision=None
 try:
  if (directory/'runtime-bundle.json').exists():runtime=json.loads((directory/'runtime-bundle.json').read_text())
  if (directory/'child-complete.json').exists():result=json.loads((directory/'child-complete.json').read_text())
  if (directory/'decision.json').exists():decision=json.loads((directory/'decision.json').read_text())
  if timed:row['state']='TIMED_OUT_NOT_INFEASIBLE'
  elif proc.returncode!=0 or result is None:row['state']='CHILD_FAILED_OR_INCOMPLETE'
  else:
   bind_completed(result,request,runtime,decision);row['state']=result['state'];row['receipt_verified']=True
   row['model_digest']=result.get('model_digest');row['runtime_digest']=result['runtime_digest']
   row['decision_digest']=result.get('decision_digest')
  if runtime:
   out['construction_observed']=runtime.get('construction_returned') is True
   out['construction_observation_verified']=row.get('receipt_verified') is True
   out['fresh_model_executed']=row.get('receipt_verified') is True and runtime.get('construction_returned') is True and runtime.get('model_binding_verified') is True
   row['constructor_called_observed']=runtime['constructor_called'];row['model_binding_verified']=row.get('receipt_verified') is True and runtime['model_binding_verified'] is True
  if decision:out['current_decision']=copy.deepcopy(decision['decision'])
 except Exception as ex:row.update(state='RECEIPT_FAILED_CLOSED',error=type(ex).__name__+':'+str(ex))
 # One fixed source core/split was used; no alternatives falsely recorded as searched.
 records=[]
 for stage in STAGES:
  if stage=='PLACEMENT' and runtime and runtime.get('model_binding_verified') is True and row.get('receipt_verified') is True:
   records.append(stage_record(stage,'ATTEMPTED_WITH_WITNESS','One source-bound geometric candidate; physical rejection/UNKNOWN retained, not a quality winner.',[attempt_id]))
  elif stage=='PLACEMENT' and timed:records.append(stage_record(stage,'TIMED_OUT','Shared budget ended; not infeasibility.',[attempt_id]))
  elif stage=='PLACEMENT':records.append(stage_record(stage,'ATTEMPTED_NO_WITNESS','No verified completed candidate receipt; retains actual failure record.',[attempt_id]))
  else:records.append(stage_record(stage,'NOT_IMPLEMENTED','Alternative '+stage.lower()+' search not implemented; fixed selected core/split use is not an alternative comparison.'))
 out['ordered_stage_dispositions']=records
 try:out['lower_program_transition']=lower_program_transition('PROGRAM_2BED_V1','PROGRAM_1BED_V1',records,unit_count=2,budget_ledger=ledger)
 except Exception as ex:out['transition_error']={'type':type(ex).__name__,'detail':str(ex),'original_ledger_retained':True}
 out['one_bed_status']='APPROVED_PROGRAM_BUT_ADAPTER_NOT_READY_NOT_EXECUTED'
 out['state']='LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED'
 try:
  require_unchanged(ROOT,snap)
  if source_audit()!=before:raise ValueError('SOURCE_AUDIT_CHANGED')
  out['source_integrity_verified']=True
 except Exception as ex:out.update(source_integrity_verified=False,source_error=type(ex).__name__+':'+str(ex),state='SOURCE_INTEGRITY_FAILED_CLOSED')
 out['evidence_directory']=str(directory.relative_to(ROOT));save(directory/'scheduler.json',out)
 return out
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--child':child(Path(sys.argv[2]))
 else:
  from automatic_program_search import run_live as scheduled
  out=scheduled(b'{"W":"18","L":"20","n":2}')
  print(json.dumps(out,sort_keys=True))
  if not out.get('source_integrity_verified') or not out['attempts'][0].get('receipt_verified'):raise SystemExit(1)
