import json,sys,time
from pathlib import Path
from guard376 import guard
P=Path(sys.argv[1]);rid=sys.argv[2];expected=sys.argv[3];HERE=Path(__file__).resolve().parent
from contract376 import ROOT,partial
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from supervisor import supervise
start=time.monotonic();deadline=start+240
try:
 for name,cap in [('construct',45),('fresh_first',90),('propose',3),('reconstruct',90),('fresh_second',90),('compare',10)]:
  guard(expected);remaining=deadline-time.monotonic()
  if remaining<=0:raise ValueError('SHARED240_DEADLINE')
  budget=min(remaining,cap);e=P/(name+'_supervision_evidence');e.mkdir()
  with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'transport_run_id':rid,'phase':name,'status':'STARTED','budget':budget})+'\n')
  s=supervise([sys.executable,'-B',str(HERE/'phase376.py'),name,str(P),str(budget),rid],budget,evidence_directory=e)
  (P/(name+'_supervision.json')).write_text(json.dumps(s,indent=2));guard(expected)
  if s['reason']!='COMPLETED'or s['worker_returncode']!=0 or not s['cleanup_verified']or not s['worker_reaped']or s['unresolved']:raise ValueError('PHASE_FAILED:'+name)
  with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'transport_run_id':rid,'phase':name,'status':'COMPLETED'})+'\n')
except Exception as e:
 out=partial('UNKNOWN',rid);out.update(reason=type(e).__name__+':'+str(e),semantic_state='UNKNOWN_NOT_EXECUTED_STAGE_FAILURE')
 with(P/'result.json').open('x')as f:json.dump(out,f,indent=2)
(P/'cycle_timing.json').write_text(json.dumps({'seconds':time.monotonic()-start,'shared_budget':240}))
