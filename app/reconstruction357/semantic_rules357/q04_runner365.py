"""Repeatable isolated fixed invocation; no supplied verdict accepted."""
import json,hashlib,subprocess,sys
from pathlib import Path
from common import digest
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='0eb1110d9dd9fa599718203904cb84881ad9f026be4209712d46741825b6201c'
def evaluate(record,review):
 manifest=ROOT/'finite_comparison365/q04_manifest365_v7.json'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('Q04_MANIFEST_CHANGED')
 files=json.loads(manifest.read_text())['files']
 def check():
  for name,h in files.items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('Q04_SOURCE_CHANGED:'+name)
 check();before=digest([record,review])
 script='''import sys,json,hashlib
from pathlib import Path
r=Path(sys.argv[1]);m=r/'finite_comparison365/q04_manifest365_v7.json'
assert hashlib.sha256(m.read_bytes()).hexdigest()==sys.argv[2]
for p,h in json.loads(m.read_text())['files'].items():
 assert hashlib.sha256((r/p).read_bytes()).hexdigest()==h,p
sys.path[:0]=[str(r/'finite_comparison365'),str(r/'semantic_rules357')]
from q04_closure365_v7 import evaluate
record=json.loads((r/'staging365_balanced_portals/actual365.json').read_text());review=json.loads((r/'review365_balanced_source_validation/result.json').read_text())
print(json.dumps(evaluate(record,review),sort_keys=True))
'''
 run=subprocess.run([sys.executable,'-B','-c',script,str(ROOT),MANIFEST_SHA],capture_output=True,text=True,timeout=20,check=True)
 out=json.loads(run.stdout);check()
 if before!=digest([record,review]):raise ValueError('Q04_INPUT_MUTATION')
 if out['record_digest']!=digest(record)or out['fresh_result_digest']!=digest(review)or out['model_digest']!=digest(record['candidate']['model']):raise ValueError('Q04_CALLER_FIXED_ARTIFACT_BINDING')
 out['invocation_manifest_sha256']=MANIFEST_SHA;out['invocation_scope']='FIXED_SOURCE_STORED_ARTIFACT_REASSESSMENT_NOT_LIVE_AUTHORITY'
 return out
