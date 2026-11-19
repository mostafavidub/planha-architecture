import copy,unittest
from unittest.mock import patch
from live_program_scheduler import *
BODY=b'{"W":"18","L":"20","n":2}'
def fixture():
 pf=preflight(BODY);q={'schema':'LIVE_PROGRAM_ATTEMPT_V1','nonce':'test','body_hex':BODY.hex(),'preflight_digest':digest(pf),'budget':budgets()}
 runtime={'binding':pf['binding'],'model_digest':'synthetic-model-only'}
 decision={'model_digest':'synthetic-model-only','decision':{'state':'BLOCKED'}}
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
if __name__=='__main__':unittest.main()
