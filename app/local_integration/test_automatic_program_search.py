import copy,unittest
import automatic_program_search as s
BODY=b'{"W":"18","L":"20","n":2}'
def receipt(q):
 return {'schema':'SCHEDULER_SYNTHETIC_RESULT_V1','kind':'SYNTHETIC_TEST_ONLY',
  **{k:q[k] for k in ('attempt_id','request_digest','programme_digest','contract_digest')},
  'state':'SIMULATED_WITNESS',**{k:False for k in s.AUTHORITY}}
class SchedulerTests(unittest.TestCase):
 def test_default_never_executes(self):
  r=s.run(BODY,clock=lambda:0)
  self.assertEqual([x['state'] for x in r['attempts']],['LIVE_ADAPTER_NOT_CONNECTED','UNSUPPORTED_ADAPTER'])
  self.assertEqual(r['used_attempts'],0);self.assertFalse(r['fresh_model_executed'])
 def test_registry_and_contract(self):
  r=s.run(BODY,clock=lambda:0)
  self.assertEqual(r['binding']['program_registry_digest'],r['alternatives'][0]['registry_digest'])
  self.assertEqual(r['binding']['raw'],{'W':'18','L':'20','n':2,'requested_count':1})
  self.assertIsNone(r['alternatives'][1]['selected_contract'])
 def test_synthetic_receipt(self):
  r=s.run(BODY,test_adapter=receipt,clock=lambda:0)
  self.assertEqual(r['attempts'][0]['state'],'SIMULATED_WITNESS')
  self.assertEqual(r['used_attempts'],1);self.assertTrue(r['test_mode'])
  self.assertIsNone(r['selected_alternative']);self.assertFalse(r['qualified'])
 def test_budget_invalid(self):
  for key,vals in {'max_attempts':[True,1.0,-1,2,'1'],'wall_seconds':[True,float('nan'),float('inf'),-1,91,'3'],'seconds_per_attempt':[False,float('nan'),float('inf'),-1,4]}.items():
   for v in vals:
    b=dict(s.DEFAULT_BUDGET);b[key]=v
    with self.assertRaises(ValueError):s.run(BODY,budget=b)
  for b in ({},dict(s.DEFAULT_BUDGET,extra=1),[]):
   with self.assertRaises(ValueError):s.run(BODY,budget=b)
 def test_zero_budget_no_calls(self):
  for key in s.DEFAULT_BUDGET:
   b=dict(s.DEFAULT_BUDGET);b[key]=0
   calls=[];r=s.run(BODY,test_adapter=lambda q:calls.append(q),clock=lambda:0,budget=b)
   self.assertEqual(calls,[]);self.assertEqual(r['attempts'][0]['state'],'BUDGET_EXHAUSTED')
 def test_allocation_capped_remaining(self):
  times=iter([0,89,89,89,89])
  r=s.run(BODY,test_adapter=receipt,clock=lambda:next(times))
  self.assertEqual(r['allocated_seconds'],1)
 def test_overrun_rejects_receipt(self):
  times=iter([0,0,4,4,4])
  r=s.run(BODY,test_adapter=receipt,clock=lambda:next(times))
  self.assertEqual(r['attempts'][0]['state'],'BUDGET_OVERRUN')
  self.assertNotIn('synthetic_receipt',r['attempts'][0])
 def test_clock_types(self):
  for v in (True,float('nan'),float('inf'),'1'):
   with self.assertRaises(ValueError):s.run(BODY,clock=lambda:v)
  times=iter([1,0])
  with self.assertRaises(ValueError):s.run(BODY,clock=lambda:next(times))
 def test_mutation(self):
  def bad(q):q['raw']['n']=1;return receipt(q)
  r=s.run(BODY,test_adapter=bad,clock=lambda:0)
  self.assertEqual(r['attempts'][0]['error']['detail'],'ADAPTER_MUTATED_INPUT')
  self.assertEqual(r['binding']['raw']['n'],2)
 def test_receipt_mismatch(self):
  for key in ('attempt_id','request_digest','programme_digest','contract_digest'):
   def bad(q):r=receipt(q);r[key]='wrong';return r
   r=s.run(BODY,test_adapter=bad,clock=lambda:0)
   self.assertEqual(r['attempts'][0]['state'],'ATTEMPT_FAILED_CLOSED')
   self.assertNotIn('synthetic_receipt',r['attempts'][0])
 def test_no_authority(self):
  for key in s.AUTHORITY:
   for value in (True,0,None):
    def bad(q):r=receipt(q);r[key]=value;return r
    r=s.run(BODY,test_adapter=bad,clock=lambda:0)
    self.assertEqual(r['attempts'][0]['state'],'ATTEMPT_FAILED_CLOSED')
    self.assertTrue(all(r[k] is False for k in s.AUTHORITY))
 def test_no_live_model_payload(self):
  for key,value in [('model',{}),('state','PASS'),('kind','LIVE')]:
   def bad(q):r=receipt(q);r[key]=value;return r
   r=s.run(BODY,test_adapter=bad,clock=lambda:0)
   self.assertEqual(r['attempts'][0]['state'],'ATTEMPT_FAILED_CLOSED')
 def test_public_no_hidden_or_other_case(self):
  for b in (b'{"W":18,"L":20,"n":2,"bedrooms":2}',b'{"W":20,"L":18,"n":2}',b'{"W":18,"L":20,"n":1}'):
   with self.assertRaises(ValueError):s.run(b)
 def test_no_exhaustive_or_selection_claim(self):
  r=s.run(BODY,test_adapter=receipt,clock=lambda:0)
  self.assertEqual(r['transitions'],[])
  self.assertFalse(r['ap07_complete']);self.assertFalse(r['global_infeasibility_proven'])
  self.assertIn('NOT_EXHAUSTIVENESS',r['transition_policy_status'])
 def test_independent_copies(self):
  a=s.alternatives();a[0]['registry']['sleep_roles'].clear()
  self.assertEqual(s.alternatives()[0]['registry']['sleep_roles'],['double','twin'])
 def test_adapter_exception(self):
  def bad(q):raise RuntimeError('test')
  r=s.run(BODY,test_adapter=bad,clock=lambda:0)
  self.assertEqual(r['attempts'][0]['error']['type'],'RuntimeError')
if __name__=='__main__':unittest.main()
