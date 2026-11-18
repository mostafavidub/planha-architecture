"""Local fixed-capability UI. No authority from caller receipts; no cached plan route."""
import json,threading,uuid,copy
from pathlib import Path
from wsgiref.simple_server import make_server
import pipeline_bridge
from public_report import public_result
from state_machine import valid_run_id,event_view,final_view
HERE=Path(__file__).resolve().parent
class Application:
 def __init__(self,*,_test_parser=None,_test_invoke=None,_test_root=None,_test_synchronous=False):
  self.parse=_test_parser or pipeline_bridge.parse;self.invoke=_test_invoke or pipeline_bridge.invoke;self.root=_test_root or HERE/'runs';self.sync=_test_synchronous;self.jobs={};self.lock=threading.Lock();self.active=False;self.source_guard=(lambda:None)if _test_parser is not None else None
 def work(self,job,folder):
  try:
   if self.source_guard is None:raise ValueError('VERIFIED_BOOTSTRAP_REQUIRED')
   self.source_guard()
   result=self.invoke(job['request'],job['generation_run_id'],folder)
   self.source_guard()
   job.update(final_view(result,job['request'],job['generation_run_id']))
  except Exception as e:job.update(state='UNKNOWN',error_type=type(e).__name__,reason='PIPELINE_EXECUTION_OR_BINDING_NOT_VERIFIED',delivery_allowed=False)
  finally:
   with self.lock:self.active=False
 def __call__(self,env,start):
  def respond(code,data):
   b=json.dumps(data,ensure_ascii=False,allow_nan=False).encode();start(code,[('Content-Type','application/json; charset=utf-8'),('Cache-Control','no-store')]);return[b]
  path=env['PATH_INFO'];method=env['REQUEST_METHOD']
  if env.get('HTTP_HOST')not in (None,'127.0.0.1:8368'):return respond('403 Forbidden',{'state':'INPUT_INVALID','reason':'LOOPBACK_HOST_REQUIRED','generation_started':False})
  if path=='/api/health'and method=='GET':
   verified=False
   try:
    if self.source_guard is not None:self.source_guard();pipeline_bridge.registry();verified=True
   except Exception:pass
   return respond('200 OK',{'state':'READY_CHECK_ONLY'if verified else'SOURCE_NOT_VERIFIED','pipeline_registered':not pipeline_bridge.REGISTRY_SHA.startswith('PENDING'),'semantic_bridge_registered':True,'source_closure_verified':verified,'ready_for_qualified_generation':verified,'scope':'FIXED26X28_TWO_UNITS_TWO_PLANS','active':self.active,'generation_started':False,'qualification_executed':False})
  if path=='/'and method=='GET':start('200 OK',[('Content-Type','text/html; charset=utf-8'),('Cache-Control','no-store')]);return[(HERE/'index.html').read_bytes()]
  if path=='/api/runs'and method=='POST':
   if env.get('CONTENT_TYPE','').split(';',1)[0].strip().lower()!='application/json'or env.get('HTTP_ORIGIN')not in (None,'http://127.0.0.1:8368'):return respond('403 Forbidden',{'state':'INPUT_INVALID','reason':'LOCAL_JSON_ORIGIN_REQUIRED','generation_started':False})
   try:
    if self.source_guard is None:raise ValueError('VERIFIED_BOOTSTRAP_REQUIRED')
    self.source_guard()
    n=int(env.get('CONTENT_LENGTH','0'))
    if not 0<n<=16384:return respond('413 Payload Too Large',{'state':'INPUT_INVALID','reason':'BODY_SIZE_LIMIT'})
    request=self.parse(env['wsgi.input'].read(n).decode('utf-8'))
   except Exception as e:
    reason=str(e);state='CAPABILITY_UNAVAILABLE'if reason in {'UNSUPPORTED_EXACT_FIXED_DIMENSION:W','UNSUPPORTED_EXACT_FIXED_DIMENSION:L','UNSUPPORTED_FIXED_SCOPE_26_28_TWO_UNITS_TWO_PLANS','PIPELINE_NOT_REGISTERED'} else'INPUT_INVALID'
    public_reason=reason if reason in {'UNSUPPORTED_EXACT_FIXED_DIMENSION:W','UNSUPPORTED_EXACT_FIXED_DIMENSION:L','UNSUPPORTED_FIXED_SCOPE_26_28_TWO_UNITS_TWO_PLANS','PIPELINE_NOT_REGISTERED'} else reason.split(':',1)[0]
    return respond('422 Unprocessable Entity',{'state':state,'reason':public_reason,'generation_started':False,'delivery_allowed':False})
   with self.lock:
    if self.active:return respond('409 Conflict',{'state':'BUSY','reason':'ANOTHER_RUN_ACTIVE','generation_started':False})
    self.active=True
   run_id=str(uuid.uuid4());folder=self.root/run_id
   try:
    folder.mkdir(parents=True,exist_ok=False)
    with(folder/'request.json').open('x')as stream:json.dump(request,stream,ensure_ascii=False)
   except Exception:
    with self.lock:self.active=False
    raise
   job={'state':'RUNNING','generation_run_id':run_id,'canonical_request_digest':request['canonical_request_digest'],'raw_digest':request['raw_digest'],'request':copy.deepcopy(request),'delivery_allowed':False};self.jobs[run_id]=job
   if self.sync:self.work(job,folder)
   else:threading.Thread(target=self.work,args=(job,folder),daemon=True).start()
   return respond('202 Accepted',{'state':'RUNNING','generation_run_id':run_id,'status_url':'/api/runs/'+run_id,'canonical_request_digest':request['canonical_request_digest'],'raw_digest':request['raw_digest'],'delivery_allowed':False})
  if path.startswith('/api/runs/')and method=='GET':
   run_id=path.removeprefix('/api/runs/')
   if not valid_run_id(run_id)or run_id not in self.jobs:return respond('404 Not Found',{'state':'NOT_FOUND'})
   job=copy.deepcopy(self.jobs[run_id]);events=self.root/run_id/'events.jsonl';job['events']=[]
   if events.exists():
    for line in events.read_text().splitlines():
     try:job['events'].append(event_view(json.loads(line),run_id))
     except(ValueError,KeyError,TypeError,json.JSONDecodeError):job['event_warning']='UNVERIFIED_OR_INCOMPLETE_EVENT_NOT_DISPLAYED'
   if 'result'in job:job['result']=public_result(job['result'])
   return respond('200 OK',job)
  return respond('404 Not Found',{'state':'NOT_FOUND'})
app=Application()
if __name__=='__main__':raise SystemExit('Use the source-verified launch_server.py; direct server startup is disabled.')
