import copy,http.client,json,sys,threading,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
import request_trace109 as c
import request_trace_server109 as s
B=b'{"W":"18","L":"22","n":2}'
class Contract(unittest.TestCase):
 def test_exact_study_and_original_scope(self):
  self.assertTrue(c.preflight(B)['execution_ready'])
  self.assertFalse(c.preflight(b'{"W":"18","L":"20","n":2}')['execution_ready'])
  from live_program_scheduler import preflight
  self.assertFalse(preflight(B)['execution_ready'])
 def test_request_identity_and_source(self):
  r=c.make_request(B);h=c.digest(r);c.validate_request(r,h)
  for key,value in [('nonce','x'),('account_id',r['nonce']),('runtime','OTHER'),('parent_only',False),('programme_digest','0'*64),('source_snapshot',{}),('qualified',True)]:
   x=copy.deepcopy(r);x[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):c.validate_request(x,c.digest(x))
  x=copy.deepcopy(r);x['nonce']='0'*32
  with self.assertRaisesRegex(ValueError,'REQUEST_DIGEST'):c.validate_request(x,h)
 def fixture(self):
  # Synthetic receipt only; no construction/architecture witness.
  r=c.make_request(B);h=c.digest(r);mh='a'*64
  reports={'parent_replay':{'verified':True,'model_hash':mh},'parent_physical':{'model_hash':mh},'parent_cause':{'model_digest':mh,'selected_causes':[]}}
  current={}
  for mod in ('current_programme_evaluator','source_guest_route_evaluator','source_living_evaluator','source_wall_function_evaluator'):
   reports['parent_current_'+mod]={'model_digest':mh,'integrity_verified':True,'state':'UNKNOWN',**{k:False for k in c.AUTH}}
   current[mod]={'state':'UNKNOWN','integrity_verified':True,'missing_count':0,'evaluator_error_count':0}
  out={'completed':True,'integrity_verified':True,'state':'BLOCKED_NO_SUPPORTED_CAUSE','request_digest':h,'run_nonce':r['nonce'],'request_account_id':r['account_id'],
   'raw_digest':c.digest(r['preflight']['raw']),'profile_digest':r['programme_digest'],'request_source_digest':c.digest(r['source_snapshot']),
   'attempt_count':1,'child_observed':False,'cause_repair_verified':False,'parent_observed':True,'parent_model_digest':mh,
   'selected_causes':[],'parent_physical':{'status':None,'errors':{},'pending':{},'not_evaluated_count':0,'out_of_scope_count':0},'parent_current':current,'report_digests':{k:c.digest(v)for k,v in reports.items()},**{k:False for k in c.AUTH}}
  p={'returncode':0,'wait_completed':True,'timed_out':False}
  return r,h,out,reports,p
 def test_synthetic_receipt_negative_identity(self):
  r,h,o,reports,p=self.fixture();self.assertTrue(c.bind_result(r,h,o,reports,p))
  for key,value in [('run_nonce','0'*32),('request_account_id','0'*32),('request_digest','0'*64),('request_source_digest','0'*64),('parent_model_digest','0'*64),('attempt_count',True),('state','NEW_STATE'),('qualified',True),('child_observed',True)]:
   x=copy.deepcopy(o);x[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):c.bind_result(r,h,x,reports,p)
 def test_rehashed_wrong_model_and_unknown_report(self):
  for field,value in [('model_hash','0'*64),('verified',False)]:
   r,h,o,reports,p=self.fixture();reports['parent_replay'][field]=value;o['report_digests']={k:c.digest(v)for k,v in reports.items()}
   with self.assertRaises(ValueError):c.bind_result(r,h,o,reports,p)
  r,h,o,reports,p=self.fixture();reports['parent_current_source_living_evaluator']['state']=None;o['report_digests']={k:c.digest(v)for k,v in reports.items()}
  with self.assertRaises(ValueError):c.bind_result(r,h,o,reports,p)
 def test_summary_forgery_with_original_reports_unchanged(self):
  r,h,o,reports,p=self.fixture();o['parent_current']['source_living_evaluator']['state']='PASS'
  with self.assertRaisesRegex(ValueError,'RESULT_CURRENT_SUMMARY'):c.bind_result(r,h,o,reports,p)
  r,h,o,reports,p=self.fixture();o['parent_physical']['status']='PASS'
  with self.assertRaisesRegex(ValueError,'RESULT_PHYSICAL_SUMMARY'):c.bind_result(r,h,o,reports,p)
 def test_final_invalidation_retains_observation_not_verified_summary(self):
  x={'receipt_verified':True,'current_states':{'x':'PASS'},'full_report_digests':{'x':'a'*64}}
  c.invalidate(x);self.assertFalse(x['receipt_verified']);self.assertNotIn('current_states',x);self.assertEqual(x['observed_unverified_evidence']['current_states']['x'],'PASS')
 def test_final_source_failure_rebuilds_account_outcome(self):
  r=c.make_request(B);h=c.digest(r)
  base={'state':'BLOCKED_NO_SUPPORTED_CAUSE','receipt_verified':True,'current_states':{'x':'UNKNOWN'},'account':{'active':True},'trace':[]}
  with patch.object(c,'validate_request',side_effect=ValueError('REQUEST_SOURCE')):c.finalize_result(base,r,h,1.25,True)
  self.assertEqual(base['state'],'SOURCE_INTEGRITY_ERROR');self.assertFalse(base['receipt_verified']);self.assertNotIn('current_states',base)
  self.assertEqual(base['account']['history'][0]['outcome'],base['state']);self.assertFalse(base['account']['history'][0]['receipt_verified'])
  self.assertEqual(c.digest(base['account']),base['account_digest']);self.assertFalse(base['account']['active'])
 def test_process_failure_no_verified_receipt(self):
  for key,value in [('returncode',True),('returncode',1),('timed_out',True),('wait_completed',False)]:
   r,h,o,reports,p=self.fixture();p[key]=value
   with self.assertRaises(ValueError):c.bind_result(r,h,o,reports,p)
 def test_source_drift_rehashed(self):
  r=c.make_request(B)
  with patch.object(c,'sources',return_value={'changed':'x'}):
   with self.assertRaisesRegex(ValueError,'REQUEST_SOURCE'):c.validate_request(r,c.digest(r))
class HTTP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=s.server();cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
 @classmethod
 def tearDownClass(cls):
  cls.server.shutdown();cls.server.server_close();cls.thread.join()
 def post(self,payload):
  conn=http.client.HTTPConnection('127.0.0.1',self.server.server_address[1],timeout=5)
  conn.request('POST','/api/public/plan',payload,{'Content-Type':'application/json'})
  resp=conn.getresponse();out=json.loads(resp.read());conn.close();return resp.status,out
 def test_invalid_and_authority_zero_dispatch(self):
  with patch.object(s,'run',side_effect=AssertionError('NO_DISPATCH'))as run:
   for payload in (b'{"W":"25.001","L":"22","n":2}',b'{"W":"18","L":"22","n":3}',b'{"W":"18","L":"22","n":2,"accepted":true}',b'{"W":"18","L":"22","n":2,"nonce":"x"}',b'{"W":"18","L":"22","n":2,"account_id":"x"}',b'{"W":"18","L":"22","n":2,"programme_id":"x"}'):
    status,out=self.post(payload);self.assertEqual(status,422);self.assertFalse(out['accepted'])
   run.assert_not_called()
 def test_valid_unsupported_real_no_process(self):
  with patch('repair_attempt_control.run_bounded',side_effect=AssertionError('NO_PROCESS'))as launch:
   status,out=self.post(b'{"W":"18","L":"20","n":2}')
   self.assertEqual(status,409);r=out['study_result'];self.assertEqual(r['state'],'UNSUPPORTED_TRACE_STUDY_CONTRACT');self.assertEqual(r['attempt_count'],0);self.assertFalse(r['receipt_verified']);launch.assert_not_called()
 def test_static_api_has_no_product_surface(self):
  conn=http.client.HTTPConnection('127.0.0.1',self.server.server_address[1]);conn.request('GET','/')
  r=conn.getresponse();self.assertEqual(r.status,404);r.read();conn.close()
if __name__=='__main__':unittest.main()
