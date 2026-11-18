"""Requires external pinned preregistration and separate explicit execution slot."""
import sys,json,hashlib,traceback,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OUT=ROOT/'review367_joint_attempt2'
def frozen():
 expected=sys.argv[sys.argv.index('--expected-prereg-sha')+1];data=(OUT/'preregistration.json').read_bytes()
 if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('PREREG_EXTERNAL_ANCHOR')
 p=json.loads(data)
 if p['execution_enabled']is not True:raise ValueError('BLOCKED_PENDING_GUARD_AND_PREAUDIT')
 for n,h in p['sources'].items():
  if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h:raise ValueError('SOURCE_DRIFT:'+n)
 return p
if __name__=='__main__':
 frozen()
 if '--worker'in sys.argv:
  try:
   from joint367 import construct,replay,inventory
   start=time.monotonic();before=inventory()
   def sink(name,data):
    if 'model'in data:
     (OUT/(name.lower()+'.json')).write_text(json.dumps(data,indent=2));return
    with (OUT/'stages.jsonl').open('a')as f:f.write(json.dumps({'stage':name,**data})+'\n')
   record=construct(stage_sink=sink);(OUT/'constructed.json').write_text(json.dumps(record,indent=2));replayed=replay(record['trace'])
   if inventory()!=before:raise ValueError('SOURCE_CHANGED_AFTER_REPLAY')
   (OUT/'actual367.json').write_text(json.dumps(record,indent=2));(OUT/'result.json').write_text(json.dumps({'status':'EXACT_SOURCE_RECONSTRUCTION_ONLY','seconds':time.monotonic()-start,'full_trace_replay':True,'fresh_executed':False,'solver_executed':False,'accepted':False,'delivery_allowed':False,'all_functional_roles':'UNKNOWN_UNTIL_OWN_CURRENT_REVIEW','source_unchanged':True},indent=2))
  except Exception as e:
   (OUT/'error.json').write_text(json.dumps({'error':str(e),'type':type(e).__name__,'traceback':traceback.format_exc(),'accepted':False},indent=2));raise
 else:
  if any((OUT/n).exists()for n in('attempt_started.json','actual367.json','error.json','supervision.json')):raise SystemExit('NO_REPEAT_ONE_DIAGNOSTIC')
  (OUT/'attempt_started.json').write_text(json.dumps({'started':time.time()}))
  from supervisor import supervise
  result=supervise([sys.executable,str(Path(__file__).resolve()),'--worker','--expected-prereg-sha',sys.argv[sys.argv.index('--expected-prereg-sha')+1]],110,evidence_directory=OUT)
  (OUT/'supervision.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
