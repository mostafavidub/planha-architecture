import json,sys,time
from pathlib import Path
from guard385 import guard
P=Path(sys.argv[1]);rid=sys.argv[2];expected=sys.argv[3];HERE=Path(__file__).resolve().parent
guard(expected)
from contract385 import ROOT,partial,clean
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from supervisor import supervise
start=time.monotonic();deadline=start+530;failed=False
try:
 for kind in('balanced','joint'):
  d=P/kind;d.mkdir()
  for phase,cap in [('construct',45 if kind=='balanced'else 90),('fresh',90),('bind',5),('semantics',90 if kind=='balanced'else 60)]:
   guard(expected);remaining=deadline-time.monotonic()
   if remaining<=0:raise ValueError('SHARED530_DEADLINE')
   budget=min(cap,remaining);e=d/(phase+'_supervision_evidence');e.mkdir()
   with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'transport_run_id':rid,'kind':kind,'phase':phase,'status':'STARTED','budget':budget})+'\n')
   s=supervise([sys.executable,'-B',str(HERE/'phase385.py'),phase,str(d),str(budget),rid,expected,kind],budget,evidence_directory=e)
   (d/(phase+'_supervision.json')).write_text(json.dumps(s,indent=2));guard(expected)
   if not clean(s):raise ValueError('PHASE_FAILED:'+kind+':'+phase)
   with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'transport_run_id':rid,'kind':kind,'phase':phase,'status':'COMPLETED'})+'\n')
 guard(expected);remaining=deadline-time.monotonic()
 if remaining<=0:raise ValueError('SHARED530_DEADLINE')
 e=P/'seal_supervision_evidence';e.mkdir()
 s=supervise([sys.executable,'-B',str(HERE/'seal385.py'),str(P),expected],min(25,remaining),evidence_directory=e)
 (P/'seal_supervision.json').write_text(json.dumps(s,indent=2));guard(expected)
 if not clean(s):raise ValueError('SEAL_FAILED')
except Exception as e:
 failed=True;out=partial('INTEGRATION_STOPPED',rid);out.update(reason=type(e).__name__+':'+str(e),semantic_state='UNKNOWN_STAGE_FAILURE')
 with(P/'result.json').open('x')as f:json.dump(out,f,indent=2)
(P/'cycle_timing.json').write_text(json.dumps({'seconds':time.monotonic()-start,'shared_budget':530}))
if failed:raise SystemExit(1)
