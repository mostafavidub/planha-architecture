import json,sys,time,traceback,uuid
from pathlib import Path
from guard390 import guard
start=time.monotonic();phase,folder,budget,run_id,expected,kind=sys.argv[1:];P=Path(folder);budget=float(budget)
def write(name,value):
 with(P/name).open('x')as f:json.dump(value,f,indent=2)
def read(name):return json.loads((P/name).read_text())
try:
 guard(expected)
 from contract390 import ROOT,verify,digest,bind_member
 envelope=json.loads((P.parent/'request.json').read_text());verify(envelope)
 if kind not in('balanced','joint'):raise ValueError('KIND')
 if phase=='construct':
  if kind=='balanced':
   sys.path.insert(0,str(ROOT/'staging378_finite_portals'));from source378 import construct
   record=construct(envelope['normalized_raw'],run_id)
  else:
   sys.path.insert(0,str(ROOT/'staging367_service_joint_attempt2'));import joint367
   if joint367.original()['candidate']['request']!=envelope['normalized_raw']:raise ValueError('JOINT_CURRENT_INPUT')
   record=joint367.construct()
  write('record.json',record)
 elif phase=='fresh':
  record=read('record.json')
  if kind=='balanced':
   sys.path.insert(0,str(ROOT/'staging378_finite_portals'));from evaluate378 import evaluate378 as evaluate
  else:
   sys.path.insert(0,str(ROOT/'staging367_joint_source_validation_attempt2'));from evaluate367 import evaluate367 as evaluate
  remaining=budget-(time.monotonic()-start)
  if remaining<=0:raise ValueError('FRESH_BUDGET_EXHAUSTED')
  fresh=evaluate(record,min(90,remaining));write('fresh.json',fresh)
  write('review_identity.json',{'run_id':run_id,'kind':kind,'review_id':fresh['review_id']if kind=='balanced'else str(uuid.uuid4()),'record_digest':digest(record),'fresh_digest':digest(fresh)})
 elif phase=='bind':write('binding.json',bind_member(envelope,read('record.json'),read('fresh.json'),run_id,kind,read('review_identity.json')['review_id']))
 elif phase=='semantics':
  from contract390 import validate_member_folder
  inputs=validate_member_folder(P,expected,require_physical_pass=False);raw=inputs['fresh']['raw_report']
  if raw['status']!='PASS_CONCEPT_SCOPED_REVIEW'or raw['errors']or raw['pending']:
   out={'binding':inputs['binding'],'qualified':False,'state':'CURRENT_PHYSICAL_REJECTED_OR_UNKNOWN','errors':raw['errors'],'pending':raw['pending'],'semantic_kernels_executed':False}
  elif kind=='balanced':
   sys.path.insert(0,str(ROOT/'staging390_current_semantics'))
   from integration390 import run_member
   out=run_member(P,expected)
  else:
   from joint_semantics390 import run_member
   out=run_member(P,expected)
  write('semantic.json',out)
 else:raise ValueError('UNKNOWN_PHASE')
 guard(expected)
 receipt={'run_id':run_id,'kind':kind,'phase':phase,'source_guard_before_after':True,'seconds':time.monotonic()-start}
 for name,key in [('record.json','record_digest'),('fresh.json','fresh_digest')]:
  if(P/name).is_file():receipt[key]=digest(read(name))
 if(P/'semantic.json').is_file():receipt['semantic_digest']=digest(read('semantic.json'))
 write(phase+'_worker_receipt.json',receipt)
except Exception as e:
 write(phase+'_error.json',{'error':type(e).__name__+':'+str(e),'traceback':traceback.format_exc()});raise
