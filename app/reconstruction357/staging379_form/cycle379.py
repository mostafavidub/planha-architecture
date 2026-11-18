import json,sys,time
from pathlib import Path
from guard379 import guard
P=Path(sys.argv[1]);rid=sys.argv[2];expected=sys.argv[3];HERE=Path(__file__).resolve().parent
guard(expected)
from contract379 import ROOT,partial
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from supervisor import supervise
start=time.monotonic();deadline=start+145;failed=False
try:
 for name,cap in [('construct',45),('fresh',90),('bind',5)]:
  guard(expected);remaining=deadline-time.monotonic()
  if remaining<=0:raise ValueError('SHARED145_DEADLINE')
  budget=min(remaining,cap);e=P/(name+'_supervision_evidence');e.mkdir()
  with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'transport_run_id':rid,'phase':name,'status':'STARTED','budget':budget})+'\n')
  s=supervise([sys.executable,'-B',str(HERE/'phase379.py'),name,str(P),str(budget),rid,expected],budget,evidence_directory=e)
  (P/(name+'_supervision.json')).write_text(json.dumps(s,indent=2));guard(expected)
  if s['reason']!='COMPLETED'or s['worker_returncode']!=0 or not s['cleanup_verified']or not s['worker_reaped']or s['unresolved']:raise ValueError('PHASE_FAILED:'+name)
  with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'transport_run_id':rid,'phase':name,'status':'COMPLETED'})+'\n')
 binding=json.loads((P/'binding.json').read_text());fresh=json.loads((P/'fresh.json').read_text())
 out=partial('COMPLETED_PENDING_SEMANTICS',rid);out.update(binding=binding,physical_review_status=fresh['raw_report']['status'],dispatch=binding['dispatch'],errors=fresh['raw_report']['errors'],pending=fresh['raw_report']['pending'],original_pending=fresh['raw_report'].get('original_pending',[]),natural_generator_failure=bool(fresh['raw_report']['errors']))
except Exception as e:
 failed=True;out=partial('INTEGRATION_STOPPED',rid);out.update(reason=type(e).__name__+':'+str(e),semantic_state='UNKNOWN_STAGE_FAILURE')
with(P/'result.json').open('x')as f:json.dump(out,f,indent=2)
(P/'cycle_timing.json').write_text(json.dumps({'seconds':time.monotonic()-start,'shared_budget':145}))
if failed:raise SystemExit(1)
