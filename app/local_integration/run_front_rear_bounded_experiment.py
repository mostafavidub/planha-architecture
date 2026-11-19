"""Task2.5 bounded original runtime experiment. No product admission."""
import hashlib,json,os,signal,subprocess,sys,time,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BODY=b'{"W":"18","L":"20","n":2}'
SOLVER_SECONDS=30
OUTER_SECONDS=180
def save(path,value):
 path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False))
def child(directory,nonce):
 from front_rear_runtime_adapter import run
 result=run(BODY,solver_seconds=SOLVER_SECONDS)
 result['experiment_nonce']=nonce
 save(directory/'runtime-bundle.json',result)
 print(json.dumps({'status':result['status'],'stages':result['stages'],'errors':result['errors'],
  'model_digest':result.get('model_digest'),'report_digests':result['report_digests'],
  'constructor_called':result['constructor_called'],'construction_returned':result['construction_returned']},sort_keys=True))
def main():
 if '--child' in sys.argv:
  nonce=sys.argv[sys.argv.index('--child')+1]
  child(ROOT/'task-2-5-evidence'/nonce,nonce);return
 nonce=uuid.uuid4().hex
 directory=ROOT/'task-2-5-evidence'/nonce;directory.mkdir(parents=True,exist_ok=False)
 from front_rear_runtime_adapter import source_audit
 before=source_audit();save(directory/'source-before.json',before)
 start=time.monotonic()
 receipt={'schema':'BOUNDED_ORIGINAL_RUNTIME_EXPERIMENT_V1','experiment_nonce':nonce,'public_body':BODY.decode(),
  'programme':'PROGRAM_2BED_V1','solver_seconds':SOLVER_SECONDS,'outer_seconds':OUTER_SECONDS,'timeout_scope':'Child process session runtime only; parent source audits and setup outside this cap; job cap10min',
  'budget_scope':'Engineering experiment limits, not architectural feasibility or output count',
  'head_sha':os.environ.get('GITHUB_SHA'),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'accepted':False,'qualified':False,'delivery_allowed':False,
  'display_allowed':False,'timed_out':False,'kill_sent':False,'wait_completed':False}
 proc=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'--child',nonce],
  cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:
  stdout,stderr=proc.communicate(timeout=OUTER_SECONDS)
 except subprocess.TimeoutExpired:
  receipt['timed_out']=True
  try:os.killpg(proc.pid,signal.SIGKILL);receipt['kill_sent']=True
  except ProcessLookupError:receipt['process_already_exited']=True
  stdout,stderr=proc.communicate()
 receipt.update(wait_completed=proc.poll() is not None,returncode=proc.returncode,elapsed_seconds=time.monotonic()-start)
 (directory/'stdout.txt').write_text(stdout);(directory/'stderr.txt').write_text(stderr)
 try:
  after=source_audit();save(directory/'source-after.json',after)
  receipt['source_unchanged']=before==after
 except Exception as ex:
  receipt['source_unchanged']=False;receipt['source_after_error']=type(ex).__name__
 bundle=directory/'runtime-bundle.json'
 if bundle.exists():
  data=json.loads(bundle.read_text());assert data['experiment_nonce']==nonce,'BUNDLE_NONCE'
  assert all(data[k] is False for k in ('accepted','qualified','delivery_allowed','display_allowed')),'BUNDLE_AUTHORITY'
  receipt['bundle_sha256']=hashlib.sha256(bundle.read_bytes()).hexdigest()
  receipt['runtime_status']=data['status'];receipt['model_digest']=data.get('model_digest')
  receipt['report_digests']=data.get('report_digests');receipt['runtime_errors']=data['errors']
  receipt['constructor_called']=data['constructor_called'];receipt['construction_returned']=data['construction_returned']
  receipt['model_binding_verified']=data['model_binding_verified']
 else:receipt['runtime_status']='NO_COMPLETE_CHILD_BUNDLE'
 receipt['experiment_observation_complete']=receipt['wait_completed'] and receipt['source_unchanged'] and bundle.exists() and not receipt['timed_out'] and proc.returncode==0
 receipt['notice']='CI success verifies bounded experiment/evidence collection, never model PASS or programme suitability.'
 save(directory/'outer-receipt.json',receipt);print(json.dumps(receipt,sort_keys=True))
 if not receipt['experiment_observation_complete']:raise SystemExit(1)
if __name__=='__main__':main()
