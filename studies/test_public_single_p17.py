"""Real HTTP invalid/unsupported before any worker. No geometry or parser stubs."""
import http.client,json,sys,threading,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import public_wln_server as server
import public_program_dispatch_p17 as dispatch
class HTTP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=server.server();cls.t=threading.Thread(target=cls.s.serve_forever,daemon=True);cls.t.start()
 @classmethod
 def tearDownClass(cls):cls.s.shutdown();cls.s.server_close();cls.t.join()
 def post(self,body):
  c=http.client.HTTPConnection('127.0.0.1',self.s.server_address[1],timeout=5)
  try:
   c.request('POST','/api/public/plan',body,{'Content-Type':'application/json'})
   r=c.getresponse();return r.status,json.loads(r.read())
  finally:c.close()
 def test_real_invalid_and_unsupported_zero_dispatch(self):
  matrix=[
   ('{"W":"4.999","L":"20","n":1}',422),('{"W":"25.001","L":"20","n":1}',422),
   ('{"W":"18","L":"4.999","n":1}',422),('{"W":"18","L":"25.001","n":1}',422),
   ('{"W":"18","L":"20","n":3}',422),('{"W":"18","L":"20","n":2.0}',422),
   ('{"W":"18","L":"20","n":1,"requested_count":6}',422),('{"W":"18","L":"20","n":""}',422),
   ('{"W":18.1,"L":"20","n":1}',409),('{"W":"18.1","L":"20","n":1}',409),
   ('{"W":"5","L":"5","n":1}',409),('{"W":"25","L":"25","n":1}',409)]
  with patch.object(server,'run_bound',side_effect=AssertionError('NO_WORKER'))as spy:
   for text,status in matrix:
    observed,payload=self.post(text.encode());self.assertEqual(observed,status,text)
    self.assertFalse(payload.get('qualified',False))
    if text in(matrix[-1][0],matrix[-2][0],matrix[-3][0]):self.assertIs(payload['input_valid'],True)
   spy.assert_not_called()
 def test_n1_and_n2_preflight_distinct(self):
  one=dispatch.preflight(b'{"W":"18","L":"20","n":1}')
  pair=dispatch.preflight(b'{"W":"18","L":"20","n":2}')
  self.assertTrue(one['execution_ready']);self.assertTrue(pair['execution_ready'])
  self.assertEqual(one['raw']['n'],1);self.assertIn('n1',one['case_scope'])
 def test_n1_completed_projection_has_same_family_scope(self):
  import single_runtime_p17
  body=b'{"W":"18","L":"20","n":1}'
  # Runtime is controlled only; parser, dispatcher and summary are real.
  controlled={'schema':'SINGLE_HTTP_RESULT_P17_V1','preflight':{'input_valid':True},'state':'BLOCKED','attempts':[]}
  with patch.object(single_runtime_p17,'run_bound',return_value=controlled)as worker,patch('subprocess.Popen',side_effect=AssertionError('NO_PROCESS'))as spawn:
   result=dispatch.run_bound(body,None,deadline=123)
   worker.assert_called_once_with(body,123);spawn.assert_not_called()
  summary=server.public_summary(result)
  self.assertEqual(summary['case_scope'],dispatch.preflight(body)['case_scope'])
  self.assertEqual(summary['case_scope'],dispatch.SINGLE_CASE_SCOPE)
  self.assertIn('n1/P2',summary['case_scope']);self.assertFalse(summary['qualified'])
 def test_n2_runtime_path_unmodified(self):
  body=b'{"W":"18","L":"20","n":2}'
  with patch.object(dispatch,'pair_bound',return_value={'marker':'PAIR'})as spy:
   runtime=object();self.assertEqual(dispatch.run_bound(body,runtime,deadline=123),{'marker':'PAIR'})
   spy.assert_called_once_with(body,runtime)
if __name__=='__main__':unittest.main(verbosity=2)
