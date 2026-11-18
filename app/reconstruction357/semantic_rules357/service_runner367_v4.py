"""Fixed source367 intrinsic cost evaluation; no arbitrary caller receipt authority."""
import json,hashlib,subprocess,sys,os,signal,time
from pathlib import Path
from common import digest
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='955cf133c78d7c01f112dfc9de1f675b2e5b94d715fa0642f682535e124a1e21'
def verify_receipts(out):
 receipts=out['invocation_receipts']
 for name,field in [('cost','cost_receipt_digest'),('necessity','necessity_receipt_digest'),('functional_partition','functional_partition_digest')]:
  if digest(receipts[name])!=out[field]:raise ValueError('SAME_INVOCATION_RECEIPT_CHANGED:'+name)
  for key in ('record_digest','fresh_result_digest','model_digest'):
   if receipts[name][key]!=out[key]:raise ValueError('NESTED_CURRENT_BINDING:'+name+':'+key)
 return True

def contained_run(argv,timeout=90):
 process=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:
  stdout,stderr=process.communicate(timeout=timeout)
  if process.returncode:raise subprocess.CalledProcessError(process.returncode,argv,stdout,stderr)
  return stdout
 finally:
  # Every fixed nested callback uses ordinary subprocess.run and inherits this group.
  # Kill any remaining descendants on success, timeout, parse-independent error, or exception.
  try:os.killpg(process.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:process.wait(timeout=.2)
  except subprocess.TimeoutExpired:pass
  try:os.killpg(process.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  process.wait()
  if process.stdout:process.stdout.close()
  if process.stderr:process.stderr.close()

def evaluate(record,result):
 manifest=ROOT/'finite_comparison367/service_manifest367_v4.json'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('SERVICE367_MANIFEST_CHANGED')
 files=json.loads(manifest.read_text())['files']
 def check():
  for name,h in files.items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('SERVICE367_DEPENDENCY_CHANGED:'+name)
 check();before=digest([record,result])
 script='''import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]);manifest=root/'finite_comparison367/service_manifest367_v4.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==sys.argv[2]
for path,h in json.loads(manifest.read_text())['files'].items():
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==h,path
sys.path[:0]=[str(root/'finite_comparison367'),str(root/'semantic_rules357')]
from service_criterion367_v4 import evaluate
r=json.loads((root/'review367_joint_attempt2/actual367.json').read_text());f=json.loads((root/'review367_joint_source_validation_attempt2/result.json').read_text())
print(json.dumps(evaluate(r,f),sort_keys=True))
'''
 stdout=contained_run([sys.executable,'-B','-c',script,str(ROOT),MANIFEST_SHA],timeout=90);out=json.loads(stdout);check();verify_receipts(out)
 if before!=digest([record,result])or out['record_digest']!=digest(record)or out['fresh_result_digest']!=digest(result):raise ValueError('SERVICE367_INPUT_RECORD_RESULT_BINDING')
 if out['model_digest']!=digest(record['candidate']['model']):raise ValueError('SERVICE367_MODEL_BINDING')
 out['invocation_manifest_sha256']=MANIFEST_SHA;out['invocation_scope']='ISOLATED_FIXED_STORED_ARTIFACT_SOURCE_JOINT367_REASSESSMENT_NOT_LIVE_AUTHORITY';return out
