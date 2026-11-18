"""Fixed source367 intrinsic cost evaluation; no arbitrary caller receipt authority."""
import json,hashlib,subprocess,sys
from pathlib import Path
from common import digest
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='de27127a38e39d47b0e358ad159efe1d00d47c407b6b3ca37e13f13c8fe277b7'
def evaluate(record,result):
 manifest=ROOT/'finite_comparison367/q04_manifest367_v2.json'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('Q04_367_MANIFEST_CHANGED')
 files=json.loads(manifest.read_text())['files']
 def check():
  for name,h in files.items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('Q04_367_DEPENDENCY_CHANGED:'+name)
 check();before=digest([record,result])
 script='''import sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]);manifest=root/'finite_comparison367/q04_manifest367_v2.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==sys.argv[2]
for path,h in json.loads(manifest.read_text())['files'].items():
 assert hashlib.sha256((root/path).read_bytes()).hexdigest()==h,path
sys.path[:0]=[str(root/'finite_comparison367'),str(root/'semantic_rules357')]
from q04_closure367_v2 import evaluate
r=json.loads((root/'review367_joint_attempt2/actual367.json').read_text());f=json.loads((root/'review367_joint_source_validation_attempt2/result.json').read_text())
print(json.dumps(evaluate(r,f),sort_keys=True))
'''
 run=subprocess.run([sys.executable,'-B','-c',script,str(ROOT),MANIFEST_SHA],capture_output=True,text=True,timeout=30,check=True);out=json.loads(run.stdout);check()
 if before!=digest([record,result])or out['record_digest']!=digest(record)or out['fresh_result_digest']!=digest(result):raise ValueError('Q04_367_INPUT_RECORD_RESULT_BINDING')
 if out['model_digest']!=digest(record['candidate']['model']):raise ValueError('Q04_367_MODEL_BINDING')
 out['invocation_manifest_sha256']=MANIFEST_SHA;out['invocation_scope']='ISOLATED_FIXED_STORED_ARTIFACT_SOURCE_JOINT367_REASSESSMENT_NOT_LIVE_AUTHORITY';return out
