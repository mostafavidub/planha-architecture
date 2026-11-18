import json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;P=Path(sys.argv[1]);sys.path.insert(0,str(HERE.parent/'staging368_final_pipeline'))
from supervisor import supervise
start=time.monotonic();deadline=start+190;phases=[]
result={'schema':'371_CONTROLLED_CONTINUATION','test_only':True,'natural_failure':False,'first_review_reused_from_actual369':True,'retry':False,'accepted':False,'delivery_allowed':False,'semantic_qualification':'UNKNOWN_NEW_GEOMETRY_NOT_REPROVEN'}
try:
 for name,cap in [('propose',3),('construct',90),('fresh',90),('compare',3)]:
  remaining=deadline-time.monotonic()
  if remaining<=0:raise ValueError('SHARED190_DEADLINE')
  budget=min(cap,remaining);e=P/(name+'_supervision_evidence');e.mkdir()
  with(P/'events.jsonl').open('a')as f:f.write(json.dumps({'phase':name,'budget':budget,'status':'STARTED'})+'\n')
  s=supervise([sys.executable,'-B',str(HERE/'worker371.py'),name,str(P),str(budget)],budget,evidence_directory=e)
  (P/(name+'_supervision.json')).write_text(json.dumps(s,indent=2));phases.append({'phase':name,'supervision':s})
  if s['reason']!='COMPLETED'or s['worker_returncode']!=0 or not s['worker_reaped']or not s['cleanup_verified']or s['unresolved']:raise ValueError('PHASE_NOT_COMPLETED:'+name)
 comparison=json.loads((P/'comparison.json').read_text())
 result.update(status='CONTROLLED_REPAIR_MECHANICS_VERIFIED'if comparison['mechanics_success']else'REPAIR_NOT_VERIFIED',comparison_summary={k:v for k,v in comparison.items()if k not in ('before_errors','before_pending','before_original_pending','before_not_evaluated')})
except Exception as e:result.update(status='STOPPED',reason=type(e).__name__+':'+str(e))
result.update(seconds=time.monotonic()-start,phases=phases)
(P/'cycle_result.json').write_text(json.dumps(result,indent=2))
