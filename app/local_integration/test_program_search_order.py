import copy,unittest
import program_search_order as p
def rows(state='NOT_ENUMERATED'):
 return [p.stage_record(s,state,'Limited framework; remaining branch explicit.') for s in p.STAGES]
def ledger():return {'account_id':'same-project','limit_attempts':2,'used_attempts':1,'limit_seconds':90,'used_seconds':3}
def transition(r=None,b=None,**kw):
 return p.lower_program_transition('PROGRAM_2BED_V1','PROGRAM_1BED_V1',rows() if r is None else r,unit_count=kw.get('n',2),budget_ledger=ledger() if b is None else b)
class OrderTests(unittest.TestCase):
 def test_unenumerated_not_exhaustive_block(self):
  r=transition();self.assertTrue(r['new_programme_alternative'])
  self.assertFalse(r['programme_repair']);self.assertFalse(r['prior_programme_infeasible'])
  self.assertFalse(r['execute_lower_program']);self.assertFalse(r['execution_ready'])
 def test_order(self):
  r=rows();r.reverse()
  with self.assertRaises(ValueError):transition(r)
  with self.assertRaises(ValueError):transition(rows()[:-1])
 def test_reason_and_state(self):
  for args in [('CORE','NOT_ENUMERATED',''),('CORE','PASS','x'),('UNKNOWN','NOT_IMPLEMENTED','x')]:
   with self.assertRaises(ValueError):p.stage_record(*args)
 def test_attempt_proof(self):
  with self.assertRaises(ValueError):p.stage_record('CORE','TIMED_OUT','time')
  r=rows();r[0]=p.stage_record('CORE','TIMED_OUT','time',['a'])
  out=transition(r);self.assertFalse(out['prior_programme_infeasible'])
 def test_duplicate_attempts(self):
  r=rows();r[0]=p.stage_record('CORE','ATTEMPTED_NO_WITNESS','x',['a']);r[1]=p.stage_record('SPLIT','TIMED_OUT','y',['a'])
  with self.assertRaises(ValueError):transition(r)
 def test_budget_not_reset(self):
  b=ledger();b['used_attempts']=2;b['used_seconds']=90
  out=transition(b=b)
  self.assertEqual(out['budget_ledger'],b);self.assertFalse(out['budget_remaining_for_study']);self.assertFalse(out['budget_reset'])
 def test_budget_adversarial(self):
  for k,vs in {'used_attempts':[True,1.0,-1,3],'used_seconds':[False,float('nan'),float('inf'),91],'limit_seconds':[float('nan'),True]}.items():
   for v in vs:
    b=ledger();b[k]=v
    with self.assertRaises(ValueError):transition(b=b)
 def test_attempt_budget_match(self):
  r=rows();r[0]=p.stage_record('CORE','ATTEMPTED_NO_WITNESS','x',['a']);b=ledger();b['used_attempts']=0
  with self.assertRaises(ValueError):transition(r,b)
 def test_program_and_n_locked(self):
  for a,b in [('PROGRAM_1BED_V1','PROGRAM_2BED_V1'),('PROGRAM_3BED_V1','PROGRAM_2BED_V1'),('PROGRAM_2BED_V1','PROGRAM_2BED_V1')]:
   with self.assertRaises(ValueError):p.lower_program_transition(a,b,rows(),unit_count=2,budget_ledger=ledger())
  for n in (True,2.0,1,3):
   with self.assertRaises(ValueError):transition(n=n)
 def test_no_authority_or_winner(self):
  r=transition()
  for k in ('accepted','qualified','display_allowed','delivery_allowed','quality_winner'):self.assertIs(r[k],False)
 def test_immutable_copies(self):
  b=ledger();r=rows();before=copy.deepcopy([b,r]);out=transition(r,b)
  self.assertEqual([b,r],before);out['budget_ledger']['used_seconds']=0
  self.assertEqual(b['used_seconds'],3)
 def test_scheduler_dispositions_not_synthetic_evidence(self):
  import automatic_program_search as s
  out=s.run(b'{"W":"18","L":"20","n":2}',clock=lambda:0)
  self.assertEqual([r['stage'] for r in out['ordered_stage_dispositions']],list(p.STAGES))
  self.assertTrue(all(r['state']=='NOT_IMPLEMENTED' and r['attempt_ids']==[] for r in out['ordered_stage_dispositions']))
if __name__=='__main__':unittest.main()
