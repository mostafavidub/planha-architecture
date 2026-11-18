import json,sys,time
from pathlib import Path
from guard378 import guard
start=time.monotonic();name,P,budget,expected=sys.argv[1:];P=Path(P);budget=float(budget)
def save(name,value):
 with (P/name).open('x')as f:json.dump(value,f,indent=2)
try:
 guard(expected);reg=json.loads((P/'preregistration.json').read_text())
 if name=='construct':
  from source378 import construct
  save('record.json',construct(reg['raw'],reg['run_id']))
 elif name=='fresh':
  from evaluate378 import evaluate378
  remaining=budget-(time.monotonic()-start)
  if remaining<=0:raise ValueError('FRESH_BUDGET_EXHAUSTED_BEFORE_REVIEW')
  save('fresh.json',evaluate378(json.loads((P/'record.json').read_text()),min(90,remaining)))
 elif name=='audit':
  from source378 import repair_dispatch
  record=json.loads((P/'record.json').read_text());fresh=json.loads((P/'fresh.json').read_text())
  if record['trace']['run_id']!=reg['run_id']or record['candidate']['request']!=reg['raw']:raise ValueError('PREREGISTERED_REQUEST_RUN_BINDING')
  selection=record['candidate']['generation_context']['selection']
  if record['trace']['selection_rank']!=reg['selection_rank']or selection['finite_rank378']!=reg['selection_rank']or selection['finite_policy378']!=reg['family_policy']or record['trace']['enumeration'][reg['selection_rank']]!=selection:raise ValueError('PREREGISTERED_RANK_POLICY_BINDING')
  save('dispatch.json',repair_dispatch(record,fresh))
 else:raise ValueError('UNKNOWN_PHASE')
 guard(expected);save(name+'_worker_receipt.json',{'phase':name,'run_id':reg['run_id'],'source_guard_before_after':True,'seconds':time.monotonic()-start})
except Exception as e:
 save(name+'_error.json',{'phase':name,'error':type(e).__name__+':'+str(e),'seconds':time.monotonic()-start})
 raise
