"""Controlled process/helper tests only; no original solver invocation."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import controlled_repair_entrypoint as e
from repair_attempt_control import new_account,digest,check
class Tests(unittest.TestCase):
 def run_case(self,script,seconds=2):
  a=new_account('a'*64,seconds=seconds)
  with tempfile.TemporaryDirectory() as d:
   r=e._execute(Path(d),Path(d),a,digest(a),controlled_worker=[sys.executable,'-u','-c',script])
   p=list(Path(d).rglob('controller-receipt.json'));self.assertEqual(len(p),1)
   self.assertEqual(json.loads(p[0].read_text()),r)
  self.assertTrue(r['source_integrity_verified'])
  self.assertFalse(r['fresh_geometry_verified']);self.assertFalse(r['child_receipt_verified'])
  check(r['account'],r['account_digest'])
  for key in e.AUTH:self.assertIs(r[key],False)
  self.assertEqual(a['used_attempts'],0)
  return r
 def test_controlled_exit_not_geometry(self):
  r=self.run_case('print("done")')
  self.assertEqual(r['outcome'],'NO_WITNESS')
  self.assertEqual(r['account']['used_attempts'],1)
 def test_controlled_exit_error(self):
  r=self.run_case('raise SystemExit(7)')
  self.assertEqual(r['outcome'],'ERROR')
 def test_real_controlled_timeout(self):
  r=self.run_case('import time; print("started",flush=True);time.sleep(10)',.2)
  self.assertEqual(r['outcome'],'TIMED_OUT')
  self.assertTrue(r['process']['kill_sent']);self.assertTrue(r['process']['wait_completed'])
  self.assertIn('NOT_INFEASIBLE',r['account']['stop_reason'])
 def test_forged_stdout_not_child_receipt(self):
  r=self.run_case('print(\'{"qualified":true,"generated_count":1}\')')
  self.assertFalse(r['child_receipt_verified']);self.assertNotIn('decision',r)
 def test_used_account_not_reset(self):
  r=self.run_case('pass')
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'ACCOUNT_STOPPED'):
    e._execute(d,d,r['account'],r['account_digest'],controlled_worker=[sys.executable,'-c','pass'])
 def test_rehashed_ledger_mutation(self):
  a=new_account('a'*64);a['used_seconds']=1
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'ACCOUNT_HISTORY_REPLAY'):
    e._execute(d,d,a,digest(a),controlled_worker=[sys.executable,'-c','pass'])
 def test_source_mutation_fail_closed(self):
  a=new_account('a'*64)
  with tempfile.TemporaryDirectory() as d,patch.object(e,'snapshot',side_effect=[{'x':'a'},{'x':'b'}]):
   r=e._execute(d,d,a,digest(a),controlled_worker=[sys.executable,'-c','pass'])
  self.assertFalse(r['source_integrity_verified']);self.assertEqual(r['outcome'],'ERROR')
 def test_account_finalization_error_retains_process(self):
  a=new_account('a'*64)
  with tempfile.TemporaryDirectory() as d,patch.object(e.control,'finish',side_effect=ValueError('CONTROLLED_LEDGER_FAILURE')):
   r=e._execute(d,d,a,digest(a),controlled_worker=[sys.executable,'-c','pass'])
   saved=json.loads(next(Path(d).rglob('controller-receipt.json')).read_text())
  self.assertEqual(saved,r);self.assertEqual(r['state'],'ACCOUNT_FINALIZATION_FAILED')
  self.assertFalse(r['account_finalization_verified']);self.assertFalse(r['child_receipt_verified'])
  self.assertEqual(r['account_reserved']['used_attempts'],1);self.assertIsNotNone(r['account_reserved']['active'])
  self.assertTrue(r['process']['wait_completed']);self.assertFalse(r['fresh_geometry_verified'])
 def test_account_digest_required(self):
  a=new_account('a'*64)
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'ACCOUNT_RECEIPT'):
    e._execute(d,d,a,'bad',controlled_worker=[sys.executable,'-c','pass'])
if __name__=='__main__':unittest.main()
