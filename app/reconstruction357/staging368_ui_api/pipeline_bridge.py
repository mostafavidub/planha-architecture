"""Fixed source import bridge; disabled until independent pipeline freeze exists."""
import json,hashlib,types,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
REGISTRY_SHA='1fc86e2d0aa8fa5ff6cab41d8f5dfdfcbf273200feac1e65fba3fb15b86a5f8f'
def registry():
 p=HERE/'pipeline_registry.json'
 if REGISTRY_SHA.startswith('PENDING')or not p.exists():raise ValueError('PIPELINE_NOT_REGISTERED')
 if hashlib.sha256(p.read_bytes()).hexdigest()!=REGISTRY_SHA:raise ValueError('PIPELINE_REGISTRY_CHANGED')
 r=json.loads(p.read_text())
 for name,h in r['files'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise ValueError('PIPELINE_SOURCE_CHANGED:'+name)
 return r

def parse(body):
 r=registry();p=ROOT/'staging368_final_pipeline/request_contract368.py';source=p.read_bytes()
 if hashlib.sha256(source).hexdigest()!=r['files'][str(p.relative_to(ROOT))]:raise ValueError('PARSER_SOURCE_CHANGED')
 m=types.ModuleType('_fixed_parser368');m.__file__=str(p);exec(compile(source,str(p),'exec'),m.__dict__)
 return m.parse_json(body)

def invoke(envelope,run_id,folder):
 registry()
 worker=HERE/'launch_pipeline.py'
 if hashlib.sha256(worker.read_bytes()).hexdigest()!='c0a1251218616cc639fa6430458cf65044548103defe959547eaff81bf094a50':raise ValueError('LAUNCHER_CHANGED')
 proc=subprocess.run([sys.executable,str(worker),run_id],capture_output=True,text=True,check=True)
 # No upstream timeout may kill the owner before descendant cleanup.
 # Dedicated audited supervisor owns and reaps all descendants before this returns.
 state=json.loads((folder/'supervision.json').read_text())
 if state.get('reason')!='COMPLETED'or type(state.get('worker_returncode'))is not int or type(state.get('worker_returncode'))is not int or state.get('worker_returncode')!=0 or not state['cleanup_verified']or not state['worker_reaped']or state['unresolved']:raise ValueError('PIPELINE_CLEANUP_NOT_VERIFIED')
 registry()
 return json.loads((folder/'result.json').read_text())
