"""Isolated fixed-source SERVICE invocation, not caller-supplied receipt authority."""
import json,hashlib,subprocess,sys
from pathlib import Path
from common import digest
ROOT=Path(__file__).resolve().parents[1]
MANIFEST_SHA='7f0ae85e2fd5165f775292277261a66ad073ad9add3dd66a09b2cf465682a49b'
def evaluate(record,result):
 from group_readsets359 import build
 build(record,result,source_profile='SOURCE359')
 manifest=ROOT/'finite_comparison358/service_closure359_manifest.json'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA:raise ValueError('SERVICE_MANIFEST_CHANGED')
 pins=json.loads(manifest.read_text())['files']
 def check():
  for name,sha in pins.items():
   if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('SERVICE_SOURCE_CHANGED:'+name)
 check();before=digest([record,result])
 script="""import sys,json
from pathlib import Path
r=Path(sys.argv[1]);sys.path[:0]=[str(r/'finite_comparison358'),str(r/'semantic_rules357')]
from service_closure359 import assess
paths=['staging359_hall_clamp/actual359.json','review359_source_validation/result.json','staging358_comparative/row_candidate358.json','review358_source_validation/result.json']
print(json.dumps(assess(*[json.loads((r/p).read_text())for p in paths]),sort_keys=True))
"""
 run=subprocess.run([sys.executable,'-B','-c',script,str(ROOT)],capture_output=True,text=True,timeout=20,check=True)
 out=json.loads(run.stdout);check()
 if before!=digest([record,result]):raise ValueError('SERVICE_INPUT_MUTATION')
 if out['evidence'][1]['model_digest']!=digest(record['candidate']['model']):raise ValueError('SERVICE_MODEL_MISMATCH')
 out['invocation_source_manifest_sha256']=MANIFEST_SHA
 out['current_record_digest']=digest(record);out['current_fresh_result_digest']=digest(result)
 out['invocation_scope']='ISOLATED_FIXED_SOURCE_STORED_ARTIFACT_REASSESSMENT; NO_LIVE_AUTHORITY'
 return out
