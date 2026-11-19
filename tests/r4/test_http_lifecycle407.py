"""Actual loopback sockets and controlled nongeometry processes.
The production run boundary is replaced explicitly. No solver, admission, durable
ledger or request109 receipt is fabricated. Disconnect is NOT a cancel contract.
"""
import hashlib,http.client,inspect,json,socket,subprocess,sys,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import public_wln_server as public
import request_trace_server109 as trace
PINS={
 'public_wln_server.py':'b3cb9e9ad0ef34349d3c6740f6285f95b865371a',
 'request_trace_server109.py':'fbe215097b43c576ff3c97d44e741cea3d0de834',
 'public_input_errors403.py':'4dba239c1484c6eda7985cde0b590680ec9ed3f3',
 'public_wln_contract.py':'80fd2b2710342735dc35e484c9b0da790995d830',
 'dimension_contract.py':'058502cd97b5131908b82fdbdba34c62d3376ea3'}
RESULTS=[]
def guard():
 out={}
 for name,pin in PINS.items():
  p=ROOT/'app/local_integration'/name;b=p.read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin
  out[name]=hashlib.sha256(b).hexdigest()
 for m in (public,trace):
  assert Path(inspect.getsourcefile(m.Handler.do_POST)).resolve()==ROOT/'app/local_integration'/(m.__name__+'.py')
 return out
def until(predicate):
 end=time.monotonic()+5
 while not predicate():
  if time.monotonic()>=end:raise AssertionError('CONTROLLED_WAIT_EXPIRED')
  time.sleep(.01)
class Controlled:
 def __init__(self,module,hold=True,fail=False):
  self.module=module;self.hold=hold;self.fail=fail
  self.entered=threading.Event();self.release=threading.Event()
  self.records=[];self.processes=[]
 def __call__(self,body):
  index=len(self.records)+1
  record={'index':index,'body_sha256':hashlib.sha256(body).hexdigest(),'state':'STARTED','solver':False}
  self.records.append(record)
  p=subprocess.Popen([sys.executable,'-B','-c','import sys;sys.stdin.readline();sys.stdout.write("CONTROLLED_ONLY")'],
   stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
  self.processes.append(p);record['pid']=p.pid;self.entered.set()
  try:
   if self.hold and index==1:
    if not self.release.wait(5):raise RuntimeError('CONTROLLED_RELEASE_TIMEOUT')
   stdout,stderr=p.communicate(input='release\n',timeout=3)
   record.update(state='WAITED',returncode=p.returncode,wait_completed=p.poll()is not None)
   assert stdout=='CONTROLLED_ONLY'and not stderr and p.returncode==0
   if self.fail and index==1:raise RuntimeError('CONTROLLED_POST_WAIT_FAILURE')
   state='CONTROLLED_BOUNDARY_'+str(index)
   if self.module is public:
    return {'preflight':public.preflight(body),'state':state,'attempts':[{'state':state}],
     'fresh_model_executed':False,'source_integrity_verified':False}
   return {'schema':'CONTROLLED_RUN_BOUNDARY_ONLY','state':state,'controlled_index':index,
    'receipt_verified':False,'evidence_usable':False,**{k:False for k in public.AUTH}}
  finally:
   if p.poll()is None:p.kill();p.wait(timeout=3);record.update(state='HARNESS_CLEANUP',wait_completed=True)
 def cleanup(self):
  self.release.set()
  for p in self.processes:
   if p.poll()is None:p.kill();p.wait(timeout=3)
def request(server,body):
 c=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=5)
 try:
  c.request('POST','/api/public/plan',body,{'Content-Type':'application/json'})
  r=c.getresponse();return r.status,json.loads(r.read())
 finally:c.close()
def raw_request(server,body):
 s=socket.create_connection(('127.0.0.1',server.server_port),timeout=5)
 header=('POST /api/public/plan HTTP/1.0\r\nHost: 127.0.0.1:'+str(server.server_port)+
  '\r\nContent-Type: application/json\r\nContent-Length: '+str(len(body))+'\r\n\r\n').encode()
 s.sendall(header+body);return s
def marker(module,response):
 return response['status']if module is public else response['study_result']['state']
class RealHTTP(unittest.TestCase):
 def exercise(self,module,disconnect=False,fail=False):
  before=guard();body=json.dumps({'W':'18','L':'20'if module is public else'22','n':'2'}).encode()
  worker=Controlled(module,hold=not fail,fail=fail)
  server=module.server(0);errors=[];replies=[]
  # Record handler exceptions without dumping arbitrary request data.
  server.handle_error=lambda *args:errors.append('HANDLER_EXCEPTION')
  original=module.Handler.reply
  def reply(handler,status,value):
   replies.append({'status':status,'generation_authority':any(value.get(k)is True for k in public.AUTH)})
   return original(handler,status,value)
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  first=None
  try:
   with patch.object(module,'run_live'if module is public else'run',worker),patch.object(module.Handler,'reply',reply):
    if fail:
     status,result=request(server,body)
     self.assertEqual(status,500);self.assertEqual(result['code'],'STUDY_FAILED_CLOSED')
     until(lambda:not module.LOCK.locked())
     self.assertFalse(module.LOCK.locked());self.assertTrue(worker.records[0]['wait_completed'])
    else:
     first=raw_request(server,body);self.assertTrue(worker.entered.wait(5))
     self.assertTrue(module.LOCK.locked());self.assertEqual(len(worker.records),1)
     status,result=request(server,body)
     self.assertEqual((status,result['code']),(409,'STUDY_BUSY_NO_QUEUE'))
     self.assertFalse(result['retry_automatic']);self.assertEqual(len(worker.records),1)
     if disconnect:
      first.shutdown(socket.SHUT_RDWR);first.close();first=None
      time.sleep(.05)
      alive=worker.processes[0].poll()is None
      self.assertTrue(alive) # Observation of absent cancellation integration, NOT cancellation success.
      status,result=request(server,body)
      self.assertEqual((status,result['code']),(409,'STUDY_BUSY_NO_QUEUE'));self.assertEqual(len(worker.records),1)
     worker.release.set()
     until(lambda:not module.LOCK.locked())
     if first is not None:
      response=http.client.HTTPResponse(first);response.begin();payload=json.loads(response.read())
      self.assertEqual(response.status,200);self.assertEqual(marker(module,payload),'CONTROLLED_BOUNDARY_1')
      first.close();first=None
     self.assertTrue(worker.records[0]['wait_completed'])
    status,after=request(server,body)
    self.assertEqual(status,200);self.assertEqual(marker(module,after),'CONTROLLED_BOUNDARY_2')
    until(lambda:not module.LOCK.locked())
    self.assertEqual(len(worker.records),2);self.assertFalse(module.LOCK.locked())
    self.assertIsNone(after['plan_payload']);self.assertFalse(after['download_available'])
    self.assertTrue(all(p.poll()is not None for p in worker.processes))
    self.assertTrue(all(x['wait_completed']for x in worker.records))
    self.assertFalse(any(x['generation_authority']for x in replies))
    if not disconnect:self.assertEqual(errors,[])
    RESULTS.append({'interface':module.__name__,'scenario':'POST_WAIT_EXCEPTION'if fail else'DISCONNECT'if disconnect else'CONCURRENT',
     'worker_count':len(worker.records),'worker_returncodes':[x['returncode']for x in worker.records],
     'all_waited':True,'lock_released':True,'second_request_distinct_controlled_response':True,
     'disconnect_cancels_worker':False if disconnect else None,
     'late_reply_scope':'ATTEMPTED_AFTER_DISCONNECT_NOT_CLIENT_DELIVERY_PROOF'if disconnect else'CONNECTED_RESPONSE',
     'handler_exception_count':len(errors),'runtime_replaced_at_boundary':True,
     'production_ledger_tested':False,'restart_tested':False,'solver_calls':0})
  finally:
   worker.cleanup()
   if first is not None:first.close()
   server.shutdown();server.server_close();thread.join(timeout=5)
   self.assertFalse(thread.is_alive())
  self.assertEqual(guard(),before)
 def test_public_concurrent(self):self.exercise(public)
 def test_trace_concurrent(self):self.exercise(trace)
 def test_public_disconnect(self):self.exercise(public,disconnect=True)
 def test_trace_disconnect(self):self.exercise(trace,disconnect=True)
 def test_public_exception(self):self.exercise(public,fail=True)
 def test_trace_exception(self):self.exercise(trace,fail=True)
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(RealHTTP)
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 print(json.dumps({'schema':'HTTP_LIFECYCLE407_CONTROLLED_V1','rows':RESULTS,'source_snapshot':guard(),
  'fresh_geometry':False,'cancel_contract_implemented':False,'durable_evidence':False,
  'accepted':False,'qualified':False,'delivery_allowed':False},sort_keys=True))
 raise SystemExit(not result.wasSuccessful())
