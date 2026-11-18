import json,sys,time
from pathlib import Path
from guard377 import guard,clean
HERE=Path(__file__).resolve().parent;P=Path(sys.argv[1]);expected=sys.argv[2]
guard(expected)
sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
start=time.monotonic();deadline=start+145;phases=[]
result={'schema':'FINITE377_SINGLE_SOURCE_CANDIDATE_RUN','accepted':False,'delivery_allowed':False,'request_fulfilled':False,'branch_count':1,'requested_count':2,'semantic_qualification':'UNKNOWN_NOT_EXECUTED','browser_executed':False,'repair_attempted':False,'retry':False}
failed=False
try:
 for name,cap in [('construct',45),('fresh',90),('audit',5)]:
  guard(expected);remaining=deadline-time.monotonic()
  if remaining<=0:raise ValueError('SHARED145_DEADLINE')
  budget=min(cap,remaining);e=P/(name+'_supervision_evidence');e.mkdir()
  with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'phase':name,'status':'STARTED','budget':budget})+'\n')
  receipt=supervise([sys.executable,'-B',str(HERE/'worker377.py'),name,str(P),str(budget),expected],budget,evidence_directory=e)
  (P/(name+'_supervision.json')).write_text(json.dumps(receipt,indent=2));phases.append({'phase':name,'receipt':receipt})
  guard(expected)
  if not clean(receipt):raise ValueError('PHASE_OR_CLEANUP_FAILED:'+name)
  with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'phase':name,'status':'COMPLETED'})+'\n')
 dispatch=json.loads((P/'dispatch.json').read_text());result.update(status=dispatch['reason'],dispatch=dispatch)
except Exception as e:
 failed=True;result.update(status='INTEGRATION_STOPPED_NOT_A_CANDIDATE_VERDICT',reason=type(e).__name__+':'+str(e))
result.update(seconds=time.monotonic()-start,phases=phases)
(P/'cycle_result.json').write_text(json.dumps(result,indent=2))
if failed:raise SystemExit(1)
