"""Fixed runner: external manifest SHA, all dependencies checked before import."""
import json,hashlib,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def verify(expected):
 p=HERE/'q04_manifest362_v2.json'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('MANIFEST_PIN')
 m=json.loads(p.read_text())
 for name,h in m['files'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('DEPENDENCY_CHANGED:'+name)
 return m

def main(expected):
 m=verify(expected)
 from q04_closure362_v2 import evaluate
 r=json.loads((ROOT/'staging362_core_notch/actual362.json').read_text());f=json.loads((ROOT/'review362_source_validation/result.json').read_text());x=evaluate(r,f)
 verify(expected);x['runner_manifest_sha256']=expected;x['transitive_pre_post_verified']=True
 p=HERE/'q04_closure_actual362_v2.json'
 if p.exists():raise ValueError('WRITE_ONCE')
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2));print(x['remaining'])
if __name__=='__main__':main(sys.argv[1])
