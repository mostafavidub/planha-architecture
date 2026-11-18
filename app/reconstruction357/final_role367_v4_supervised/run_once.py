import sys,json,hashlib,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
expected=sys.argv[1]
p=HERE/'prereg.json'
if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise ValueError('EXTERNAL_PREREG_CHANGED')
x=json.loads(p.read_text())
for n,h in x['files'].items():
 if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('PRERUN_PIN_CHANGED:'+n)
with (HERE/'started.json').open('x')as f:json.dump({'started':time.time(),'prereg_sha256':expected,'hard_cap_seconds':180},f)
from supervisor import supervise
result=supervise([sys.executable,str(HERE/'worker.py'),expected],180,evidence_directory=HERE)
post=all(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h for n,h in x['files'].items())
result.update(source_unchanged=post,actual_exists=(HERE/'actual.json').exists())
with (HERE/'supervision.json').open('x')as f:json.dump(result,f,indent=2)
print(json.dumps(result))
if not result['cleanup_verified']or not post or not result['actual_exists']:raise SystemExit(1)
