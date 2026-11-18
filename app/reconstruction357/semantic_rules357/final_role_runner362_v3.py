"""Isolated, pinned artifact reassessment. No fresh or delivery authority."""
import hashlib,json,subprocess,sys
from pathlib import Path
from common import digest
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='440817f044fe62bc0fa987ebb09d9c83655a8e653f1391915e2a187361131a7b'
def evaluate(record,review):
 p=ROOT/'semantic_rules357/role_registry_final362_v3_source_freeze.json'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('FINAL_ROLE_MANIFEST_CHANGED')
 files=json.loads(p.read_text())['files']
 def check():
  for name,sha in files.items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('FINAL_ROLE_SOURCE_CHANGED:'+name)
 check();before=digest([record,review])
 script="""import json,hashlib,sys
from pathlib import Path
r=Path(sys.argv[1]);p=r/'semantic_rules357/role_registry_final362_v3_source_freeze.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()==sys.argv[2]
for name,sha in json.loads(p.read_text())['files'].items():
 assert hashlib.sha256((r/name).read_bytes()).hexdigest()==sha,name
sys.path.insert(0,str(r/'semantic_rules357'))
from role_registry_final362_v3 import evaluate
record=json.loads((r/'staging362_core_notch/actual362.json').read_text());review=json.loads((r/'review362_source_validation/result.json').read_text())
print(json.dumps(evaluate(record,review),sort_keys=True))
"""
 run=subprocess.run([sys.executable,'-B','-c',script,str(ROOT),MANIFEST_SHA],capture_output=True,text=True,timeout=40,check=True)
 out=json.loads(run.stdout);check()
 if before!=digest([record,review]):raise ValueError('FINAL_ROLE_INPUT_MUTATION')
 if out['record_digest']!=digest(record)or out['review_digest']!=digest(review)or out['model_hash']!=digest(record['candidate']['model']):raise ValueError('FINAL_ROLE_CALLER_BINDING')
 out['invocation_manifest_sha256']=MANIFEST_SHA
 return out
