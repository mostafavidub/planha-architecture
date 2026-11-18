"""Only fixed-record, isolated callable qualification; no caller receipt API."""
import hashlib,json,subprocess,sys,os,signal
from pathlib import Path
from common import digest
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='2a990390d0219ae92ae2efd2f1c1926e4e60f09b4bfdf3e13494beae6cb2bea2'
def evaluate(record,fresh):
 p=ROOT/'semantic_rules357/balanced365_qualification367_v3_manifest.json'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('QUALIFICATION_MANIFEST_CHANGED')
 m=json.loads(p.read_text())
 if digest(record)!=m['record_digest'] or digest(fresh)!=m['fresh_digest']:raise ValueError('QUALIFICATION_FIXED_INPUTS')
 def check():
  for n,h in m['files'].items():
   if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('QUALIFICATION_SOURCE_CHANGED:'+n)
 check();before=digest([record,fresh])
 script='''import json,sys,hashlib
from pathlib import Path
R=Path(sys.argv[1]);p=R/'semantic_rules357/balanced365_qualification367_v3_manifest.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()==sys.argv[2]
m=json.loads(p.read_text())
for n,h in m['files'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
sys.path.insert(0,str(R/'semantic_rules357'))
from balanced365_qualification367_core_v3 import evaluate
r=json.loads((R/'staging365_balanced_portals/actual365.json').read_text());f=json.loads((R/'review365_balanced_source_validation/result.json').read_text())
print(json.dumps(evaluate(r,f),sort_keys=True))
'''
 worker=subprocess.Popen([sys.executable,'-B','-c',script,str(ROOT),MANIFEST_SHA],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:
  stdout,stderr=worker.communicate(timeout=150)
  if worker.returncode!=0:raise ValueError('QUALIFICATION_WORKER_FAILED:'+stderr[-1000:])
 finally:
  # Kill the isolated session group, including nested fixed-runner children.
  try:os.killpg(worker.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  worker.communicate()
 out=json.loads(stdout);check()
 if before!=digest([record,fresh]) or out['record_digest']!=digest(record)or out['fresh_result_digest']!=digest(fresh):raise ValueError('QUALIFICATION_OUTPUT_BINDING')
 out['invocation_manifest_sha256']=MANIFEST_SHA
 return out
