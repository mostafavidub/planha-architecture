import hashlib,http.client,json,socket,sys,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'app/local_integration'))
import public_wln_server as s
import http_withholding_x04 as w
BODY=b'{"W":"18","L":"20","n":2}'
def fake(body):
 return {'preflight':{'input_valid':True},'state':'CONTROLLED_ONLY','attempts':[{'state':'CONTROLLED_ONLY','nonce':'synthetic-child','receipt_verified':False}],
 'source_integrity_verified':True,'fresh_model_executed':False,'current_decision':{'state':'BLOCKED','blockers':['CONTROLLED_ONLY']}}
def until(fn):
 end=time.monotonic()+4
 while not fn():
  if time.monotonic()>end:raise AssertionError('WAIT_EXPIRED')
  time.sleep(.005)
class HTTP(unittest.TestCase):
 def setUp(self):
  self.server=s.server();self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
  self.port=self.server.server_port;self.before=len(s.HTTP_BOUNDARY.snapshot())
 def tearDown(self):
  self.server.shutdown();self.server.server_close();self.thread.join()
  self.assertFalse(s.LOCK.locked())
 def request(self,body=BODY):
  c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5);c.request('POST','/api/public/plan',body,{'Content-Type':'application/json'})
  r=c.getresponse();status=r.status;data=json.loads(r.read());c.close();return status,data
 def test_ontime_same_public_path(self):
  with patch.object(s,'run_live',side_effect=fake) as run:
   status,data=self.request()
  self.assertEqual(status,200);self.assertEqual(data['http_lifecycle']['response_state'],'ON_TIME_OBSERVED')
  self.assertFalse(data['http_lifecycle']['evidence_usable']);run.assert_called_once_with(BODY)
  record=s.HTTP_BOUNDARY.snapshot()[-1]
  self.assertEqual(record['request_id'],data['http_lifecycle']['request_id'])
  self.assertEqual(record['request_digest'],hashlib.sha256(BODY).hexdigest())
  self.assertEqual(record['summary_digest'],data['http_lifecycle']['summary_digest'])
 def test_timeout_busy_late_then_new_identity(self):
  entered=threading.Event();release=threading.Event()
  def slow(body):
   entered.set()
   if not release.wait(4):raise AssertionError('CONTROL')
   return fake(body)
  try:
   with patch.object(w,'LIMIT_SECONDS',.15),patch.object(s,'run_live',side_effect=slow) as run:
    status,data=self.request();self.assertEqual(status,504);self.assertTrue(entered.is_set())
    self.assertEqual(data['code'],'DEADLINE_EXCEEDED_RESULT_WITHHELD')
    self.assertFalse(data['evidence_usable']);self.assertTrue(s.LOCK.locked())
    self.assertEqual(self.request()[1]['code'],'STUDY_BUSY_NO_QUEUE');self.assertEqual(run.call_count,1)
    release.set();until(lambda:not s.LOCK.locked())
    old=s.HTTP_BOUNDARY.snapshot()[-1];self.assertEqual(old['response_state'],'WITHHELD');self.assertTrue(old['worker_state'].startswith('LATE_'))
    status,new=self.request();self.assertEqual(status,200);self.assertNotEqual(new['http_lifecycle']['request_id'],data['request_id'])
    self.assertEqual(run.call_count,2);self.assertEqual(s.HTTP_BOUNDARY.snapshot()[-2]['response_state'],'WITHHELD')
  finally:release.set();until(lambda:not s.LOCK.locked())
 def test_worker_exception_releases(self):
  with patch.object(s,'run_live',side_effect=ValueError('PRIVATE_NEVER_PRINT')):
   status,data=self.request()
  self.assertEqual(status,500);self.assertNotIn('PRIVATE',json.dumps(data));self.assertFalse(s.LOCK.locked())
 def test_finalization_overrun(self):
  original=s.public_summary
  def slow(raw):time.sleep(.12);return original(raw)
  with patch.object(w,'LIMIT_SECONDS',.05),patch.object(s,'run_live',side_effect=fake),patch.object(s,'public_summary',side_effect=slow):
   status,data=self.request();self.assertEqual(status,504)
   self.assertTrue(s.LOCK.locked());until(lambda:not s.LOCK.locked())
  self.assertTrue(s.HTTP_BOUNDARY.snapshot()[-1]['worker_state'].startswith('LATE_'))
 def test_preflight_overrun_no_dispatch(self):
  original=s.preflight
  def slow(body):time.sleep(.08);return original(body)
  with patch.object(w,'LIMIT_SECONDS',.03),patch.object(s,'preflight',side_effect=slow),patch.object(s,'run_live',side_effect=AssertionError('NO_DISPATCH')) as run:
   status,data=self.request();self.assertEqual(status,504);self.assertEqual(data['code'],'DEADLINE_EXCEEDED_BEFORE_DISPATCH');run.assert_not_called()
  self.assertFalse(data['generation_started'])
 def test_disconnect_does_not_unlock(self):
  entered=threading.Event();release=threading.Event()
  def slow(body):entered.set();release.wait(4);return fake(body)
  sock=socket.create_connection(('127.0.0.1',self.port))
  try:
   with patch.object(w,'LIMIT_SECONDS',.1),patch.object(s,'run_live',side_effect=slow) as run:
    header=('POST /api/public/plan HTTP/1.0\r\nHost: 127.0.0.1:'+str(self.port)+'\r\nContent-Type: application/json\r\nContent-Length: '+str(len(BODY))+'\r\n\r\n').encode()
    sock.sendall(header+BODY);until(entered.is_set);sock.close();time.sleep(.15)
    self.assertTrue(s.LOCK.locked());self.assertEqual(self.request()[1]['code'],'STUDY_BUSY_NO_QUEUE');self.assertEqual(run.call_count,1)
    release.set();until(lambda:not s.LOCK.locked())
  finally:sock.close();release.set();until(lambda:not s.LOCK.locked())
 def test_source_failure_never_verified(self):
  data=fake(BODY);data['source_integrity_verified']=False
  with patch.object(s,'run_live',return_value=data):
   status,out=self.request()
  self.assertEqual(status,200);self.assertFalse(out['source_integrity_verified']);self.assertFalse(out['http_lifecycle']['receipt_verified'])
  self.assertEqual(s.HTTP_BOUNDARY.snapshot()[-1]['worker_state'],'SOURCE_UNVERIFIED_OBSERVED')
 def test_invalid_unsupported_no_boundary(self):
  with patch.object(s,'run_live',side_effect=AssertionError('NO_RUN')) as run:
   self.assertEqual(self.request(b'{"W":"26","L":"20","n":2}')[0],422)
   self.assertEqual(self.request(b'{"W":"18","L":"20","n":1}')[0],409);run.assert_not_called()
  self.assertEqual(len(s.HTTP_BOUNDARY.snapshot()),self.before)
if __name__=='__main__':unittest.main()
