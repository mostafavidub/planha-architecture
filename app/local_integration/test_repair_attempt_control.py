import unittest,sys,copy
from repair_attempt_control import *
class Tests(unittest.TestCase):
 def test_reserve_counts_before_work(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s));self.assertEqual(s['used_attempts'],1);self.assertEqual(t['allocated_seconds'],240)
 def test_repeat_parent_stops(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=2,outcome='CANDIDATE',model_digest='a'*64);self.assertEqual(s['stop_reason'],'REPEATED_MODEL_NO_GEOMETRIC_PROGRESS')
 def test_shared_budget_no_reset(self):
  s=new_account('a'*64,seconds=10);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=3,outcome='CANDIDATE',model_digest='b'*64);s,t=reserve(s,digest(s));self.assertEqual(t['allocated_seconds'],7)
 def test_repeat_new_digest_stops(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=1,outcome='CANDIDATE',model_digest='b'*64)
  s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=1,outcome='CANDIDATE',model_digest='b'*64);self.assertEqual(s['stop_reason'],'REPEATED_MODEL_NO_GEOMETRIC_PROGRESS')
 def test_attempt_cap(self):
  s=new_account('a'*64,max_attempts=1);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=1,outcome='CANDIDATE',model_digest='b'*64);self.assertEqual(s['stop_reason'],'ATTEMPT_BUDGET_EXHAUSTED')
 def test_timeout_not_infeasible(self):
  s=new_account('a'*64,seconds=1);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=1.1,outcome='TIMED_OUT');self.assertIn('NOT_INFEASIBLE',s['stop_reason'])
 def test_no_witness_not_infeasible(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=1,outcome='NO_WITNESS');self.assertIn('NOT_INFEASIBLE',s['stop_reason'])
 def test_wrong_receipt(self):
  s=new_account('a'*64)
  with self.assertRaises(ValueError):reserve(s,'0'*64)
 def test_double_reserve(self):
  s=new_account('a'*64);s,_=reserve(s,digest(s))
  with self.assertRaises(ValueError):reserve(s,digest(s))
 def test_wrong_token(self):
  s=new_account('a'*64);s,_=reserve(s,digest(s))
  with self.assertRaises(ValueError):finish(s,digest(s),'wrong',elapsed_seconds=0,outcome='ERROR')
 def test_bad_budgets(self):
  for x in (True,float('nan'),float('inf'),0,-1,241):
   with self.assertRaises(ValueError):new_account('a'*64,seconds=x)
 def test_bool_attempts(self):
  with self.assertRaises(ValueError):new_account('a'*64,max_attempts=True)
 def test_bad_elapsed(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s))
  for x in (True,-1,float('nan')):
   with self.assertRaises(ValueError):finish(s,digest(s),t['token'],elapsed_seconds=x,outcome='ERROR')
 def test_rehashed_history_elapsed_tampering(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=3,outcome='CANDIDATE',model_digest='b'*64);s['used_seconds']=0
  with self.assertRaises(ValueError):reserve(s,digest(s))
 def test_rehashed_active_allocation_tampering(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s));s['active']['allocated_seconds']=241
  with self.assertRaises(ValueError):finish(s,digest(s),t['token'],elapsed_seconds=1,outcome='ERROR')
 def test_rehashed_active_token_tampering(self):
  s=new_account('a'*64);s,_=reserve(s,digest(s));s['active']['token']='wrong'
  with self.assertRaises(ValueError):finish(s,digest(s),'wrong',elapsed_seconds=1,outcome='ERROR')
 def test_rehashed_no_progress_stop_cannot_reset(self):
  s=new_account('a'*64);s,t=reserve(s,digest(s));s=finish(s,digest(s),t['token'],elapsed_seconds=1,outcome='CANDIDATE',model_digest='a'*64);s['stop_reason']=None
  with self.assertRaises(ValueError):reserve(s,digest(s))
 def test_actual_controlled_timeout(self):
  r=run_bounded([sys.executable,'-u','-c','import time;print("started",flush=True);time.sleep(10)'],.3)
  self.assertTrue(r['timed_out'] and r['kill_sent'] and r['wait_completed']);self.assertNotEqual(r['returncode'],0);self.assertIn('started',r['stdout'])
 def test_actual_controlled_success(self):
  r=run_bounded([sys.executable,'-c','print("done")'],2);self.assertFalse(r['timed_out']);self.assertEqual(r['returncode'],0)
 def test_actual_controlled_error(self):
  r=run_bounded([sys.executable,'-c','raise SystemExit(7)'],2);self.assertFalse(r['timed_out']);self.assertEqual(r['returncode'],7)
if __name__=='__main__':unittest.main()
