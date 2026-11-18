"""Private worker only; browser cannot submit model, review, or proof objects."""
import json,sys,hashlib,traceback,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
EXPECTED_REGISTRY_SHA='1fc86e2d0aa8fa5ff6cab41d8f5dfdfcbf273200feac1e65fba3fb15b86a5f8f'
run_id=sys.argv[1];p=HERE/'pipeline_registry.json'
if hashlib.sha256(p.read_bytes()).hexdigest()!=EXPECTED_REGISTRY_SHA:raise ValueError('REGISTRY_PREIMPORT')
registry=json.loads(p.read_text())
for n,h in registry['files'].items():
 if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('FULL_SOURCE_PREIMPORT:'+n)
sys.path[:0]=[str(ROOT/'staging368_final_pipeline'),str(HERE)]
from state_machine import valid_run_id,event_view
if not valid_run_id(run_id):raise ValueError('RUN_ID')
folder=HERE/'runs'/run_id
try:
 from request_contract368 import verify
 from pipeline import execute
 envelope=json.loads((folder/'request.json').read_text());verify(envelope)
 def event(e):
  view=event_view(e,run_id)
  with (folder/'events.jsonl').open('a')as stream:stream.write(json.dumps(view,ensure_ascii=False)+'\n');stream.flush()
 result=execute(envelope,deadline_seconds=440,generation_run_id=run_id,on_event=event)
 for n,h in registry['files'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('FULL_SOURCE_POSTRUN:'+n)
 with (folder/'raw_pipeline_result.json').open('x')as stream:json.dump(result,stream,ensure_ascii=False)
 # Separate source-frozen bridge process. No upstream timeout kills its owner.
 bridge=ROOT/'staging368_bridge_runtime/launch_bridge.py'
 if 'staging368_bridge_runtime/launch_bridge.py'not in registry['files']:raise ValueError('BRIDGE_NOT_REGISTERED')
 event({'generation_run_id':run_id,'phase':'semantic_current_run','status':'STARTED'})
 subprocess.run([sys.executable,'-B',str(bridge),run_id],check=True)
 # Launcher is responsible for fixed source preimport, deadline and full reap.
 bridgefolder=ROOT/'review368_runs'/run_id
 final=json.loads((bridgefolder/'final_result.json').read_text())
 receipt=json.loads((bridgefolder/'bridge_result.json').read_text())
 supervision=json.loads((bridgefolder/'bridge_supervision.json').read_text())
 from derived_report import derive,unwrap_bridge
 semantic=unwrap_bridge(final,receipt,supervision,result,envelope,run_id)
 derived=derive(result,semantic,envelope,run_id)
 for n,h in registry['files'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('FULL_SOURCE_POSTBRIDGE:'+n)
 event({'generation_run_id':run_id,'phase':'semantic_current_run','status':'COMPLETED'})
 with (folder/'result.json').open('x')as stream:json.dump(derived,stream,ensure_ascii=False)
except BaseException:
 with (folder/'error.txt').open('x')as stream:stream.write(traceback.format_exc())
 raise
