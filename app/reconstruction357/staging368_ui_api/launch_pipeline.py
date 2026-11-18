import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
REGISTRY_SHA='1fc86e2d0aa8fa5ff6cab41d8f5dfdfcbf273200feac1e65fba3fb15b86a5f8f'
p=HERE/'pipeline_registry.json'
if hashlib.sha256(p.read_bytes()).hexdigest()!=REGISTRY_SHA:raise ValueError('REGISTRY_PREIMPORT')
r=json.loads(p.read_text())
for n,h in r['files'].items():
 if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('FULL_SOURCE_PREIMPORT:'+n)
if hashlib.sha256((HERE/'pipeline_worker.py').read_bytes()).hexdigest()!='979e81376c2d811fe7d8520f0abd55440c48ba7abe01ccdc1fe6f7e50edd0a4d':raise ValueError('UI_BOOTSTRAP_CHANGED:pipeline_worker.py')
if hashlib.sha256((HERE/'state_machine.py').read_bytes()).hexdigest()!='e091a615eb6b1dfa6f2c2ed7b85c9a024f76d0d8c5ed45908b7252086d7171f6':raise ValueError('UI_BOOTSTRAP_CHANGED:state_machine.py')
if hashlib.sha256((HERE/'supervisor.py').read_bytes()).hexdigest()!='77053e184cea27bc860cc5e6ca520686ab0952ed6a23ecc905fb7a7fdd82f49f':raise ValueError('UI_BOOTSTRAP_CHANGED:supervisor.py')
from state_machine import valid_run_id
run_id=sys.argv[1]
if not valid_run_id(run_id):raise ValueError('RUN_ID')
folder=HERE/'runs'/run_id
with (folder/'worker_started.json').open('x')as stream:json.dump({'run_id':run_id,'outer_seconds':510,'raw_seconds':440,'bridge_seconds':60},stream)
from supervisor import supervise
x=supervise([sys.executable,str(HERE/'pipeline_worker.py'),run_id],510,evidence_directory=folder)
with (folder/'supervision.json').open('x')as stream:json.dump(x,stream)
if x.get('reason')!='COMPLETED'or type(x.get('worker_returncode'))is not int or type(x.get('worker_returncode'))is not int or x.get('worker_returncode')!=0 or not x['cleanup_verified']or not x['worker_reaped']or x['unresolved']or not(folder/'result.json').exists():raise SystemExit(1)
