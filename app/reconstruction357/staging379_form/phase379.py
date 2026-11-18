import json,sys,time,traceback
from pathlib import Path
from guard379 import guard
start=time.monotonic();name,folder,budget,run_id,expected=sys.argv[1:];P=Path(folder);budget=float(budget)
def write(name,value):
 with (P/name).open('x')as f:json.dump(value,f,indent=2)
def read(name):return json.loads((P/name).read_text())
try:
 guard(expected)
 from contract379 import ROOT,verify,bind
 env=read('request.json');verify(env)
 sys.path.insert(0,str(ROOT/'staging378_finite_portals'))
 if name=='construct':
  from source378 import construct
  write('record.json',construct(env['normalized_raw'],run_id))
 elif name=='fresh':
  from evaluate378 import evaluate378
  remaining=budget-(time.monotonic()-start)
  if remaining<=0:raise ValueError('FRESH_BUDGET_EXHAUSTED')
  write('fresh.json',evaluate378(read('record.json'),min(90,remaining)))
 elif name=='bind':write('binding.json',bind(env,read('record.json'),read('fresh.json'),run_id))
 else:raise ValueError('UNKNOWN_PHASE')
 guard(expected);write(name+'_worker_receipt.json',{'run_id':run_id,'phase':name,'source_guard_before_after':True,'seconds':time.monotonic()-start})
except Exception as e:
 write(name+'_error.json',{'phase':name,'error':type(e).__name__+':'+str(e),'traceback':traceback.format_exc()});raise
