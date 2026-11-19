"""Task4.4 versioned outer controller; historical child/guards unchanged.
One outer attempt includes all internal existing-operator variants and fresh gates.
Controlled tests do not establish a fresh geometric integration run.
"""
import copy,hashlib,inspect,json,os,sys,uuid
from pathlib import Path
import repair_attempt_control as control
AUTH=control.AUTH
ROOT=Path(__file__).resolve().parents[2]
def require(ok,why):
 if not ok:raise ValueError(why)
def snapshot():
 paths=['app/local_integration/'+x for x in ('controlled_repair_entrypoint.py','repair_attempt_control.py','bounded_repair_chain.py')]
 return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
def save(p,v):p.write_text(json.dumps(v,sort_keys=True,indent=2,allow_nan=False))
def _execute(input_root,output_root,account,expected,*,controlled_worker=None):
 """Internal controlled-worker seam is explicitly unverified and never runs real binder."""
 control.check(account,expected)
 before=snapshot()
 state,allocation=control.reserve(account,expected)
 require(allocation is not None,'NO_ATTEMPT_ALLOCATED')
 nonce=uuid.uuid4().hex;directory=Path(output_root)/nonce
 directory.mkdir(parents=True,exist_ok=False)
 simulated=controlled_worker is not None
 out={'schema':'CONTROLLED_REPAIR_ENTRYPOINT_V1','nonce':nonce,'mode':'CONTROLLED_WORKER_TEST' if simulated else 'ORIGINAL_CHILD_WIRING',
      'account_before_digest':expected,'account_after_reserve':copy.deepcopy(state),'source_snapshot':before,
      'head_sha':os.environ.get('GITHUB_SHA'),'child_receipt_verified':False,'fresh_geometry_verified':False,
      'scope':'One outer attempt includes existing internal variants; no per-variant stop callback or quality claim.',
      **{k:False for k in AUTH}}
 save(directory/'controller-start.json',out)
 outcome='ERROR';model=None;elapsed=0;process=None;audit=None;child_sources=None;child_filepins={}
 try:
  if simulated:
   argv=controlled_worker
  else:
   import bounded_repair_chain as child
   require(Path(inspect.getsourcefile(child.bind_result)).resolve()==ROOT/'app/local_integration/bounded_repair_chain.py','CHILD_BINDER_IMPORT')
   audit=child.source_audit()
   argv=[sys.executable,'-B',str(ROOT/'app/local_integration/bounded_repair_chain.py'),'--child',str(directory.resolve()),str(Path(input_root).resolve()),nonce]
  process=control.run_bounded(argv,allocation['allocated_seconds']);elapsed=process['elapsed_seconds']
  out['process']=process
  if process['timed_out']:outcome='TIMED_OUT'
  elif type(process['returncode']) is not int or process['returncode']!=0 or process['wait_completed'] is not True:outcome='ERROR'
  elif simulated:
   outcome='NO_WITNESS'
   out['controlled_result']='EXIT_OBSERVED_NO_GEOMETRY_AUTHORITY'
  else:
   def read(name):
    data=(directory/name).read_bytes();child_filepins[name]=hashlib.sha256(data).hexdigest()
    return json.loads(data)
   result=read('repair-complete.json')
   out['observed_result_digest']=control.digest(result)
   operator=read('operator-result.json')
   bundle=read('child-runtime-bundle.json') if (directory/'child-runtime-bundle.json').exists() else None
   decision=read('child-current-decision.json') if (directory/'child-current-decision.json').exists() else None
   require(result['parent_model_digest']==account['parent_model_digest'],'ACCOUNT_PARENT_BINDING')
   child.bind_result(result,nonce,operator,bundle,decision)
   child_sources=copy.deepcopy(result['source_snapshot'])
   require(type(child_sources) is dict and child_sources,'CHILD_SOURCE_SNAPSHOT')
   for path,value in child_sources.items():
    require(type(path) is str and path.startswith('app/local_integration/') and '..' not in Path(path).parts,'CHILD_SOURCE_PATH')
    require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==value,'CHILD_SOURCE_SNAPSHOT_CHANGED')
   out['child_receipt_verified']=True
   if result['state']=='FRESH_CHILD_ALL_GATES_RECORDED_NOT_QUALIFIED':
    outcome='CANDIDATE';model=result['child_model_digest']
    out['fresh_geometry_verified']=True
    out['decision']=copy.deepcopy(result['current_decision'])
   else:outcome='NO_WITNESS'
 except Exception as ex:
  out['error']={'type':type(ex).__name__,'message':str(ex)}
  outcome='ERROR'
 finally:
  try:
   require(snapshot()==before,'CONTROLLER_SOURCE_CHANGED')
   if not simulated:
    require(audit is not None,'SOURCE_AUDIT_NOT_ESTABLISHED')
    require(child.source_audit()==audit,'CHILD_SOURCE_CHANGED')
    for name,value in child_filepins.items():
     require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==value,'CHILD_EVIDENCE_FILE_CHANGED')
    if child_sources is not None:
     for path,value in child_sources.items():
      require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==value,'CHILD_SOURCE_SNAPSHOT_CHANGED')
   out['source_integrity_verified']=True
  except Exception as ex:
   out['source_integrity_verified']=False
   out['integrity_error']={'type':type(ex).__name__,'message':str(ex)}
   outcome='ERROR';model=None;out['child_receipt_verified']=False;out['fresh_geometry_verified']=False
   if 'decision' in out:out['observed_unverified_decision']=out.pop('decision')
  reserved=copy.deepcopy(state)
  try:
   state=control.finish(state,control.digest(state),allocation['token'],elapsed_seconds=elapsed,outcome=outcome,model_digest=model)
   control.check(state,control.digest(state))
   out.update(account=state,account_digest=control.digest(state),account_finalization_verified=True)
  except Exception as ex:
   out.update(account_finalization_verified=False,account_reserved=reserved,account_reserved_digest=control.digest(reserved),
     account_error={'type':type(ex).__name__,'message':str(ex)},state='ACCOUNT_FINALIZATION_FAILED',
     child_receipt_verified=False,fresh_geometry_verified=False)
   if 'decision' in out:out['observed_unverified_decision']=out.pop('decision')
  out.update(outcome=outcome,
    process_budget_scope='Child process only; source audit and setup excluded, not measured separately.',
    actual_geometry_execution_claim='NONE_CONTROLLED_TEST' if simulated else 'See verified receipt; errors/timeouts may have partial unverified construction.',
    fresh_geometry_verified_meaning='Source-bound child/replay/full-report chain, not architectural qualification',
    current_test_scope='CONTROLLED_WORKER_NO_GEOMETRY' if simulated else 'ORIGINAL_CHILD_ATTEMPT')
  save(directory/'controller-receipt.json',out)
 return out
def execute(input_root,output_root,account,expected_digest):
 return _execute(input_root,output_root,account,expected_digest)
if __name__=='__main__':
 require(len(sys.argv)==5,'USAGE input_root output_root account_json expected_digest')
 result=execute(Path(sys.argv[1]),Path(sys.argv[2]),json.loads(Path(sys.argv[3]).read_text()),sys.argv[4])
 print(json.dumps(result,sort_keys=True))
 if not result['child_receipt_verified']:raise SystemExit(1)
