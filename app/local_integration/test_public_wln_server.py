import unittest,threading,http.client,json
from unittest.mock import patch
import public_wln_server as S
class HTTP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.spawn_patch=patch('subprocess.Popen',side_effect=AssertionError('REGRESSION_NO_PROCESS'))
  cls.spawn=cls.spawn_patch.start()
  cls.server=S.server(0);cls.port=cls.server.server_address[1]
  cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
 @classmethod
 def tearDownClass(cls):
  cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.spawn_patch.stop()
 def tearDown(self):self.spawn.assert_not_called()
 def request(self,body=None,path='/api/public/plan',headers=None,method='POST'):
  c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=10)
  h={'Content-Type':'application/json',**(headers or {})};c.request(method,path,body=body,headers=h);r=c.getresponse();raw=r.read();status=r.status;c.close();return status,raw
 def test_three_fields_assets(self):
  status,raw=self.request(path='/',method='GET');self.assertEqual(status,200)
  text=raw.decode();self.assertEqual(text.count('<input '),3);self.assertNotIn('name="bedrooms"',text);self.assertNotIn('requested_count',text)
 def test_health(self):
  status,raw=self.request(path='/health',method='GET');self.assertEqual(json.loads(raw)['public_fields'],['W','L','n'])
 def test_diagnostic_not_exposed(self):self.assertEqual(self.request(b'{}',path='/generate')[0],404)
 def test_export_not_exposed(self):self.assertEqual(self.request(path='/download/model',method='GET')[0],404)
 def test_extra_hidden_field(self):self.assertEqual(self.request(b'{"W":18,"L":20,"n":2,"bedrooms":2}')[0],422)
 def test_duplicate(self):self.assertEqual(self.request(b'{"W":18,"W":20,"L":20,"n":2}')[0],422)
 def test_dimension_above25(self):self.assertEqual(self.request(b'{"W":26,"L":20,"n":2}')[0],422)
 def test_valid_unsupported_no_worker(self):
  with patch('public_wln_server.run_live',side_effect=AssertionError('must not run')) as p:
   status,raw=self.request(b'{"W":20,"L":20,"n":2}');self.assertEqual(status,409);self.assertTrue(json.loads(raw)['input_valid']);p.assert_not_called()
 def test_n3_n4_invalid_brief_no_dispatch(self):
  with patch('public_wln_server.run_live',side_effect=AssertionError('must not run')) as p:
   for n in (3,4,'3','4'):
    status,raw=self.request(json.dumps({'W':'18','L':'20','n':n}).encode())
    out=json.loads(raw);self.assertEqual(status,422);self.assertEqual(out['code'],'INVALID_BRIEF');self.assertEqual(out['field'],'n')
    for key in S.AUTH:self.assertIs(out[key],False)
   p.assert_not_called()
 def test_unit_one_other_dimensions_unsupported(self):
  with patch.object(S,'run_bound',side_effect=AssertionError('NO_WORKER'))as call:
   status,raw=self.request(b'{"W":17,"L":20,"n":1}')
   self.assertEqual(status,409);self.assertTrue(json.loads(raw)['input_valid']);call.assert_not_called()
 def test_unit_one_selected_family_ready_without_execution(self):
  with patch.object(S,'run_bound',side_effect=AssertionError('NO_WORKER'))as call:
   self.assertTrue(S.preflight(b'{"W":18,"L":20,"n":1}')['execution_ready'])
   call.assert_not_called()
 def test_foreign_origin(self):self.assertEqual(self.request(b'{}',headers={'Origin':'https://evil.invalid'})[0],403)
 def test_foreign_host(self):self.assertEqual(self.request(b'{}',headers={'Host':'evil.invalid'})[0],403)
 def test_content_type(self):self.assertEqual(self.request(b'{}',headers={'Content-Type':'text/plain'})[0],415)
 def test_busy_no_queue(self):
  S.LOCK.acquire()
  try:self.assertEqual(json.loads(self.request(b'{"W":18,"L":20,"n":2}')[1])['code'],'STUDY_BUSY_NO_QUEUE')
  finally:S.LOCK.release()
 def test_synthetic_wiring_not_fresh_solver(self):
  body=b'{"W":18,"L":20,"n":2}'
  fake={'preflight':S.preflight(body),'state':'SYNTHETIC_HTTP_TEST_ONLY','attempts':[{'state':'SYNTHETIC'}],'source_integrity_verified':True,'fresh_model_executed':False,'current_decision':{'state':'BLOCKED','blockers':['SYNTHETIC']},'secret_internal_model':{'not_public':True}}
  with patch('public_wln_server.run_live',return_value=fake) as p:
   status,raw=self.request(body);out=json.loads(raw);self.assertEqual(status,200);p.assert_called_once_with(body)
   self.assertEqual(out['plan_count_available'],0);self.assertIsNone(out['plan_payload']);self.assertNotIn('secret_internal_model',out)
 def test_error_releases_lock(self):
  with patch('public_wln_server.run_live',side_effect=ValueError('synthetic')):
   self.assertEqual(self.request(b'{"W":18,"L":20,"n":2}')[0],500)
  self.assertFalse(S.LOCK.locked())
if __name__=='__main__':unittest.main()
