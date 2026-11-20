import copy,unittest
from unittest.mock import patch
from live_program_scheduler import *
BODY=b'{"W":"18","L":"20","n":2}'
def fixture():
 pf=preflight(BODY);q={'schema':'LIVE_PROGRAM_ATTEMPT_V1','nonce':'test','body_hex':BODY.hex(),'preflight_digest':digest(pf),'budget':budgets()}
 runtime={'binding':pf['binding'],'model_digest':'synthetic-model-only','completed':True,'model_binding_verified':True,**{k:False for k in AUTH}}
 decision={'model_digest':'synthetic-model-only','decision':{'state':'BLOCKED'},'integrity_verified':True,**{k:False for k in AUTH}}
 r={'nonce':'test','request_digest':digest(q),'preflight_digest':digest(pf),'programme_digest':pf['binding']['program_registry_digest'],'contract_digest':pf['binding']['contract_digest'],
 'runtime_digest':digest(runtime),'model_digest':'synthetic-model-only','state':'LIVE_ORIGINAL_CHAIN_AND_CURRENT_DECISION_COMPLETED_NOT_QUALIFIED','decision':decision['decision'],'decision_digest':digest(decision),**{k:False for k in AUTH}}
 return r,q,runtime,decision
class LiveTests(unittest.TestCase):
 def test_selected_preflight(self):self.assertTrue(preflight(BODY)['execution_ready'])
 def test_valid_other_dimensions_unsupported(self):self.assertEqual(preflight(b'{"W":20,"L":20,"n":2}')['state'],'UNSUPPORTED_SELECTED_SAME_VERSION_CASE')
 def test_valid_one_unit_unsupported(self):self.assertEqual(preflight(b'{"W":18,"L":20,"n":1}')['state'],'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT')
 def test_hidden_program_rejected(self):
  with self.assertRaises(ValueError):preflight(b'{"W":18,"L":20,"n":2,"bedrooms":2}')
 def test_unsupported_never_starts_child(self):
  with patch('live_program_scheduler.subprocess.Popen',side_effect=AssertionError('not allowed')) as p:
   out=run_live(b'{"W":18,"L":20,"n":1}');self.assertFalse(out['fresh_model_executed']);p.assert_not_called()
 def test_bool_budget(self):
  b=budgets();b['solver_seconds']=True
  with self.assertRaises(ValueError):budgets(b)
 def test_nonfinite_budget(self):
  b=budgets();b['shared_child_seconds']=float('inf')
  with self.assertRaises(ValueError):budgets(b)
 def test_budget_excess(self):
  b=budgets();b['shared_child_seconds']=181
  with self.assertRaises(ValueError):budgets(b)
 def test_solver_outer_order(self):
  b=budgets();b['shared_child_seconds']=1
  with self.assertRaises(ValueError):budgets(b)
 def test_receipt_synthetic_only(self):self.assertTrue(bind_completed(*fixture()))
 def test_wrong_nonce(self):
  r,q,b,d=fixture();r['nonce']='different'
  with self.assertRaisesRegex(ValueError,'NONCE_REQUEST'):bind_completed(r,q,b,d)
 def test_wrong_program_digest(self):
  r,q,b,d=fixture();r['programme_digest']='0'*64
  with self.assertRaisesRegex(ValueError,'programme_digest'):bind_completed(r,q,b,d)
 def test_runtime_request_mutation_even_rehashed(self):
  r,q,b,d=fixture();b['binding']['raw']['requested_count']=2;r['runtime_digest']=digest(b)
  with self.assertRaisesRegex(ValueError,'LIVE_RUNTIME_REQUEST_BINDING'):bind_completed(r,q,b,d)
 def test_decision_mutation(self):
  r,q,b,d=fixture();d['decision']['state']='PASS'
  with self.assertRaisesRegex(ValueError,'LIVE_DECISION_BINDING'):bind_completed(r,q,b,d)
 def test_authority_integer_zero(self):
  r,q,b,d=fixture();r['qualified']=0
  with self.assertRaisesRegex(ValueError,'LIVE_AUTHORITY'):bind_completed(r,q,b,d)
 def test_no_budget_reset_policy(self):
  self.assertFalse(policy()['budget_reset_on_transition'])
 def test_unknown_child_state(self):
  r,q,b,d=fixture();r['state']='UNKNOWN_MAGIC'
  with self.assertRaisesRegex(ValueError,'LIVE_STATE_ENUM'):bind_completed(r,q,b,d)
 def test_completed_requires_runtime_binding(self):
  r,q,b,d=fixture();b['model_binding_verified']=False;r['runtime_digest']=digest(b)
  with self.assertRaisesRegex(ValueError,'LIVE_COMPLETED_RUNTIME_REQUIRED'):bind_completed(r,q,b,d)
 def test_completed_requires_decision_integrity(self):
  r,q,b,d=fixture();d['integrity_verified']=False;r['decision_digest']=digest(d)
  with self.assertRaisesRegex(ValueError,'LIVE_DECISION_INTEGRITY_AUTHORITY'):bind_completed(r,q,b,d)
 def test_runtime_authority(self):
  r,q,b,d=fixture();b['qualified']=True;r['runtime_digest']=digest(b)
  with self.assertRaisesRegex(ValueError,'LIVE_RUNTIME_AUTHORITY'):bind_completed(r,q,b,d)
class ParametricP04Tests(unittest.TestCase):
 def post_body(self,w,l,n=2):return json.dumps({'W':w,'L':l,'n':n}).encode()
 def test_source_core_and_exact_decimal_and_boundary(self):
  from parametric_pair_p04 import CASES,prepare,guard
  with patch('live_program_scheduler.subprocess.Popen',side_effect=AssertionError('solver forbidden')) as spawn:
   before=guard()
   for (w,l),ratios in zip(CASES,({'W':['181','10'],'L':['111','5']},{'W':['25','1'],'L':['25','1']})):
    body=self.post_body(w,l);pf=preflight(body);binding,core=prepare(body)
    self.assertTrue(pf['execution_ready']);self.assertEqual(digest(pf['binding']),digest(binding))
    self.assertEqual(binding['contract']['raw_ratios'],ratios)
    self.assertEqual(binding['source_core_digest'],digest(core))
    self.assertEqual(binding['contract']['family'],'FRONT_REAR')
    self.assertTrue(all(binding[k] is False for k in AUTH))
   self.assertEqual(guard(),before);spawn.assert_not_called()
 def test_decimal_wire_boundary_and_near_miss_no_dispatch(self):
  from dimension_contract import InputError
  from parametric_pair_p04 import CASES
  with patch('live_program_scheduler.subprocess.Popen',side_effect=AssertionError('solver forbidden')) as spawn:
   for w,l in ((CASES[0][1],CASES[0][0]),('18.1000001','22.2'),('25','24.999'),('5','5')):
    result=run_live(self.post_body(w,l))
    self.assertEqual(result['state'],'UNSUPPORTED_SELECTED_SAME_VERSION_CASE');self.assertEqual(result['attempts'],[])
   for body in (self.post_body(18.1,'22.2'),self.post_body('25.001','25'),self.post_body('25','25',3),
                b'{"W":"25","L":"25","n":2,"family":"LEFT_RIGHT"}'):
    with self.assertRaises(InputError):run_live(body)
   spawn.assert_not_called()
 def test_native_integer_does_not_replace_fraction_and_original_wire_stays_bound(self):
  from parametric_pair_p04 import prepare
  a=prepare(self.post_body('18.1','22.2'))[0];b=prepare(self.post_body('۱۸٫۱۰','22.20'))[0]
  self.assertEqual(a['raw'],b['raw']);self.assertNotEqual(digest(a),digest(b))
 def test_child_uses_selected_runner_once_and_retains_incomplete_bundle(self):
  import tempfile
  from pathlib import Path
  import parametric_pair_p04
  body=self.post_body('25','25');pf=preflight(body);unavailable={'binding':pf['binding'],'status':'NO_PROPOSAL_IN_BOUNDED_ATTEMPT','constructor_called':False,'model_binding_verified':False,'completed':True,**{k:False for k in AUTH}}
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)
   request={'schema':'LIVE_PROGRAM_ATTEMPT_V1','nonce':'fixture','body_hex':body.hex(),'preflight_digest':digest(pf),'budget':budgets()}
   save(folder/'request.json',request)
   with patch.object(parametric_pair_p04,'run',return_value=unavailable) as controlled, patch('front_rear_runtime_adapter.run',side_effect=AssertionError('no fallback')) as legacy, patch('live_program_scheduler.subprocess.Popen',side_effect=AssertionError('solver forbidden')) as spawn:
    child(folder)
    controlled.assert_called_once_with(body,solver_seconds=30);legacy.assert_not_called();spawn.assert_not_called()
   observed=json.loads((folder/'runtime-bundle.json').read_text())
   row=json.loads((folder/'child-complete.json').read_text())
   self.assertEqual(observed,unavailable);self.assertTrue(bind_completed(row,request,observed,None))
   altered=copy.deepcopy(observed);altered['binding']['source_core_digest']='0'*64
   tampered=copy.deepcopy(row);tampered['runtime_digest']=digest(altered)
   with self.assertRaisesRegex(ValueError,'LIVE_RUNTIME_REQUEST_BINDING'):bind_completed(tampered,request,altered,None)
   self.assertFalse((folder/'decision.json').exists())
 def test_http_real_route_controlled_n2_no_solver(self):
  import http.client,threading
  import public_wln_server as server
  from parametric_pair_p04 import CASES
  s=server.server();thread=threading.Thread(target=s.serve_forever,daemon=True);thread.start()
  def post(body):
   c=http.client.HTTPConnection('127.0.0.1',s.server_port,timeout=12)
   try:
    c.request('POST','/api/public/plan',body,{'Content-Type':'application/json'})
    r=c.getresponse();return r.status,json.loads(r.read())
   finally:c.close()
  def result(body,runtime,*,deadline):
   self.assertIsInstance(deadline,float);pf=preflight(body)
   self.assertEqual(pf['binding']['schema'],'P04_PARAMETRIC_REQUEST_BINDING_V1')
   return {'preflight':pf,'state':'CONTROLLED_NO_GEOMETRY','attempts':[],**{k:False for k in AUTH}}
  try:
   with patch.object(server,'run_bound',side_effect=result) as mock,patch('subprocess.Popen',side_effect=AssertionError('solver forbidden')) as spawn:
    for w,l in CASES:
     status,data=post(self.post_body(w,l))
     self.assertEqual(status,200);self.assertEqual(data['status'],'CONTROLLED_NO_GEOMETRY')
     self.assertEqual(data['plan_count_available'],0);self.assertTrue(all(data[k] is False for k in AUTH))
    for body,expected in ((self.post_body('20','20'),409),(self.post_body('25.001','25'),422),
                         (self.post_body(18.1,'22.2'),409),(self.post_body('25','25',3),422)):
     status,data=post(body);self.assertEqual(status,expected)
    self.assertEqual(mock.call_count,2);spawn.assert_not_called()
  finally:s.shutdown();s.server_close();thread.join(timeout=5)
if __name__=='__main__':unittest.main()
