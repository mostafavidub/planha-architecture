"""Fixed-source JOINT367 final-role actual/tests; isolated group and deadline180.
No arbitrary script, path or timeout accepted. Nested callbacks inherit the group.
"""
import hashlib,json,subprocess,sys,os,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='1f25e4193e8f4d228a29c7dc7a4afee047535b0aebbbfe055b435b7f9504a93f'
DEADLINE_SECONDS=180
PREFIX='''import json,sys,hashlib,unittest
from pathlib import Path
R=Path(sys.argv[1]);p=R/'semantic_rules357/role_registry_final_joint367_source_freeze.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()==sys.argv[2]
m=json.loads(p.read_text())
for n,h in m['files'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
sys.path.insert(0,str(R/'semantic_rules357'))
'''
SCRIPTS={'actual':PREFIX+'''from role_registry_final_joint367 import evaluate
r=json.loads((R/'review367_joint_attempt2/actual367.json').read_text());f=json.loads((R/'review367_joint_source_validation_attempt2/result.json').read_text())
print(json.dumps(evaluate(r,f),sort_keys=True))
''','tests':PREFIX+'''suite=unittest.defaultTestLoader.loadTestsFromName('test_role_registry_final_joint367')
result=unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():raise SystemExit(1)
print(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'successful':result.wasSuccessful()}))
'''}
def run(mode):
 if mode not in SCRIPTS:raise ValueError('FIXED_MODE_ONLY')
 manifest=ROOT/'semantic_rules357/role_registry_final_joint367_source_freeze.json'
 def check():
  if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('FINALROLE_MANIFEST_CHANGED')
  for n,h in json.loads(manifest.read_text())['files'].items():
   if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('FINALROLE_SOURCE_CHANGED:'+n)
 check();worker=subprocess.Popen([sys.executable,'-B','-c',SCRIPTS[mode],str(ROOT),MANIFEST_SHA],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:
  stdout,stderr=worker.communicate(timeout=DEADLINE_SECONDS)
  if worker.returncode!=0:raise ValueError('FINALROLE_WORKER_FAILED:'+stderr[-2000:])
 finally:
  try:os.killpg(worker.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  worker.communicate()
 check();out=json.loads(stdout)
 return {'mode':mode,'result':out,'stderr':stderr,'deadline_seconds':DEADLINE_SECONDS,'isolated_group_cleanup_attempted':True,'invocation_manifest_sha256':MANIFEST_SHA}
if __name__=='__main__':
 mode=sys.argv[1]if len(sys.argv)==2 else'';print(json.dumps(run(mode),sort_keys=True))
