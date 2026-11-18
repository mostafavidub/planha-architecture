"""Fixed source365 SERVICE evaluation; no arbitrary caller receipt authority."""
import json,hashlib,subprocess,sys
from pathlib import Path
from common import digest
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='d8aae2829a056eb55166ee660ec58b6be1ab4522d13841f15c0b8f7186520d40'
def evaluate(record,result):
 manifest=ROOT/'finite_comparison365/service_manifest365.json'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('SERVICE365_MANIFEST_CHANGED')
 files=json.loads(manifest.read_text())['files']
 def check():
  for name,h in files.items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('SERVICE365_DEPENDENCY_CHANGED:'+name)
 check();before=digest([record,result])
 script='''import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]);manifest=root/'finite_comparison365/service_manifest365.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==sys.argv[2]
for path,h in json.loads(manifest.read_text())['files'].items():
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==h,path
sys.path[:0]=[str(root/'finite_comparison365'),str(root/'semantic_rules357')]
from service_closure365 import evaluate
r=json.loads((root/'staging365_balanced_portals/actual365.json').read_text());f=json.loads((root/'review365_balanced_source_validation/result.json').read_text())
print(json.dumps(evaluate(r,f),sort_keys=True))
'''
 run=subprocess.run([sys.executable,'-B','-c',script,str(ROOT),MANIFEST_SHA],capture_output=True,text=True,timeout=20,check=True);out=json.loads(run.stdout);check()
 if before!=digest([record,result])or out['record_digest']!=digest(record)or out['fresh_result_digest']!=digest(result):raise ValueError('SERVICE365_INPUT_RECORD_RESULT_BINDING')
 if any(out[k]['evidence'][1]['model_digest']!=digest(record['candidate']['model'])for k in ('against362','against359')):raise ValueError('SERVICE365_MODEL_BINDING')
 out['invocation_manifest_sha256']=MANIFEST_SHA;out['invocation_scope']='ISOLATED_FIXED_STORED_ARTIFACT_SOURCE365_REASSESSMENT_NOT_LIVE_AUTHORITY';return out
