import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
import request_budget110 as l
import request_trace109 as bridge
from repair_attempt_control import run_bounded
B=b'{"W":"18","L":"22","n":2}'
class Ledger(unittest.TestCase):
 def fixture(self,seconds=10,prior=()):
  # Request metadata is synthetic; no geometry or solver runs.
  r=bridge.make_request(B,seconds=seconds);h=l.digest(r);a=l.anchor(r,h,prior);s=l.create(a);s,alloc=l.reserve(s,l.digest(s),a)
  return r,h,a,s,alloc
 def finish(self,a,s,alloc,**kw):
  args={'elapsed_seconds':1,'reported_outcome':'BLOCKED_NO_SUPPORTED_CAUSE','model_digest':'a'*64,'receipt_verified':True,'internal_attempt_count':1,'internal_count_verified':True};args.update(kw)
  return l.finish(s,l.digest(s),a,alloc['token'],**args)
 def test_roundtrip_replays_exact_history(self):
  r,h,a,s,alloc=self.fixture();out=self.finish(a,s,alloc)
  with tempfile.TemporaryDirectory()as td:
   p=Path(td)/'ledger.json';p.write_text(json.dumps(out,allow_nan=False));again=json.loads(p.read_text());self.assertEqual(l.digest(again),l.digest(out));l.check(again,l.digest(out),a)
  self.assertEqual(out['used_seconds'],sum(x['elapsed_seconds']for x in out['history']));self.assertEqual(out['used_attempts'],1)
 def test_rehashed_history_semantic_mutations(self):
  r,h,a,s,alloc=self.fixture();out=self.finish(a,s,alloc)
  mutants=[]
  for key,value in [('used_attempts',True),('used_seconds',0),('state','NEW'),('unique_observed_models',[])]:
   bad=copy.deepcopy(out);bad[key]=value;mutants.append(bad)
  for key,value in [('token','wrong'),('request_digest','0'*64),('elapsed_seconds',True),('reported_outcome','INFEASIBLE'),('internal_attempt_count',True),('receipt_verified',False)]:
   bad=copy.deepcopy(out);bad['history'][0][key]=value;mutants.append(bad)
  for bad in mutants:
   with self.subTest(bad_keys=list(bad)),self.assertRaises(ValueError):l.check(bad,l.digest(bad),a)
 def test_reservation_and_token_no_reset(self):
  r,h,a,s,alloc=self.fixture()
  with self.assertRaises(ValueError):l.reserve(s,l.digest(s),a)
  with self.assertRaises(ValueError):l.finish(s,l.digest(s),a,'bad',elapsed_seconds=1,reported_outcome='FAILED_CLOSED')
  out=self.finish(a,s,alloc)
  with self.assertRaises(ValueError):l.reserve(out,l.digest(out),a)
  with self.assertRaises(ValueError):l.finish(out,l.digest(out),a,alloc['token'],elapsed_seconds=1,reported_outcome='FAILED_CLOSED')
  reset=l.create(a)
  with self.assertRaises(ValueError):l.check(reset,l.digest(out),a)
  # No claim of persistent anti-replay if an external trusted anchor is replaced.
 def test_rehashed_active_allocation_and_anchor(self):
  r,h,a,s,alloc=self.fixture()
  for key,value in [('allocated_seconds',20),('token','0'*32+':1')]:
   bad=copy.deepcopy(s);bad['active'][key]=value
   with self.assertRaises(ValueError):l.check(bad,l.digest(bad),a)
  bad=copy.deepcopy(s);bad['anchor']['request_digest']='0'*64
  with self.assertRaises(ValueError):l.check(bad,l.digest(bad),a)
 def test_verified_parent_presence_matches_reported_outcome(self):
  r,h,a,s,alloc=self.fixture()
  with self.assertRaisesRegex(ValueError,'LEDGER_VERIFIED_PARENT_MODEL'):self.finish(a,s,alloc,model_digest=None)
  with self.assertRaisesRegex(ValueError,'LEDGER_NO_PARENT_MODEL'):self.finish(a,s,alloc,reported_outcome='BLOCKED_NO_PARENT_PROPOSAL')
  out=self.finish(a,s,alloc,reported_outcome='BLOCKED_NO_PARENT_PROPOSAL',model_digest=None)
  self.assertEqual(out['state'],'BLOCKED_NO_PARENT_PROPOSAL')
  bad=self.finish(a,s,alloc);bad['history'][0]['observed_model_digest']=None;bad['unique_observed_models']=[]
  with self.assertRaisesRegex(ValueError,'LEDGER_VERIFIED_PARENT_MODEL'):l.check(bad,l.digest(bad),a)
 def test_duplicate_model_no_quality_progress(self):
  r,h,a,s,alloc=self.fixture(prior=('a'*64,));out=self.finish(a,s,alloc)
  self.assertEqual(out['state'],'REPEATED_MODEL_NO_PROGRESS');self.assertFalse(out['history'][0]['receipt_verified']);self.assertFalse(out['history'][0]['quality_improvement'])
 def test_budget_boundary_invalidates_observed_receipt(self):
  for elapsed in (10,11):
   r,h,a,s,alloc=self.fixture();out=self.finish(a,s,alloc,elapsed_seconds=elapsed)
   self.assertEqual(out['state'],'BUDGET_EXHAUSTED');self.assertFalse(out['history'][0]['receipt_verified']);self.assertTrue(out['history'][0]['observed_receipt_verified'])
 def test_error_and_no_parent_not_infeasibility(self):
  for state in('FAILED_CLOSED','SOURCE_INTEGRITY_ERROR','TIMED_OUT','BLOCKED_NO_PARENT_PROPOSAL'):
   r,h,a,s,alloc=self.fixture();out=self.finish(a,s,alloc,reported_outcome=state,receipt_verified=False,internal_count_verified=False,internal_attempt_count=None,model_digest=None)
   self.assertEqual(out['state'],state);self.assertFalse(out['accepted']);self.assertNotIn('INFEASIBLE',out['state'])
 def base(self,r,h,s,process=None):
  return {'state':'BLOCKED_NO_SUPPORTED_CAUSE','receipt_verified':True,'account':s,'account_reserved_digest':l.digest(s),'trace':[],'attempt_count':1,'parent_model_digest':'a'*64,'current_states':{'x':'UNKNOWN'},'full_report_digests':{'x':'b'*64},**({}if process is None else{'process':process})}
 def test_wrapper_deadline_moves_evidence_to_observed(self):
  r,h,a,s,alloc=self.fixture();base=self.base(r,h,s);bridge.finalize_result(base,r,h,10,True)
  self.assertEqual(base['state'],'BUDGET_EXHAUSTED');self.assertFalse(base['receipt_verified']);self.assertFalse(base['evidence_usable'])
  self.assertNotIn('current_states',base);self.assertIn('observed_unverified_evidence',base)
  self.assertEqual(base['account']['history'][0]['outcome'],base['state']);self.assertEqual(base['account_digest'],l.digest(base['account']))
 def test_final_cutoff_includes_ledger_validation_time(self):
  r,h,a,s,alloc=self.fixture();base=self.base(r,h,s)
  with patch('time.monotonic',side_effect=[100,100.001,111]):bridge.finalize_result(base,r,h,0,True)
  self.assertEqual(base['state'],'BUDGET_EXHAUSTED');self.assertEqual(base['elapsed_seconds'],11)
  self.assertEqual(base['account']['history'][0]['elapsed_seconds'],11);l.check(base['account'],base['account_digest'],a)
  self.assertFalse(base['evidence_usable']);self.assertNotIn('current_states',base)
 def test_finalize_exception_preserves_reservation_process(self):
  r,h,a,s,alloc=self.fixture();process={'returncode':0,'wait_completed':True,'timed_out':False,'elapsed_seconds':.1};base=self.base(r,h,s,process)
  before=l.digest(s)
  with patch.object(l,'finish',side_effect=ValueError('CONTROLLED_FINALIZE_FAILURE')):bridge.finalize_result(base,r,h,1,True)
  self.assertEqual(base['state'],'ACCOUNT_FINALIZATION_FAILED');self.assertFalse(base['receipt_verified'])
  self.assertEqual(l.digest(base['account_reserved']),before);self.assertEqual(l.digest(base['account']),before);self.assertIsNotNone(base['account']['active'])
  self.assertEqual(base['process'],process);self.assertFalse(base['account_finalization_verified'])
 def test_wrong_reserved_digest_fails_closed(self):
  r,h,a,s,alloc=self.fixture();base=self.base(r,h,s);base['account_reserved_digest']='0'*64
  bridge.finalize_result(base,r,h,1,True);self.assertEqual(base['state'],'ACCOUNT_FINALIZATION_FAILED');self.assertIn('account_reserved',base)
 def test_controlled_real_timeout_wait_and_partial(self):
  proc=run_bounded([sys.executable,'-u','-c',"import time; print('CONTROLLED_PARTIAL',flush=True); time.sleep(20)"],.5)
  self.assertTrue(proc['timed_out']);self.assertTrue(proc['wait_completed']);self.assertTrue(proc['kill_sent']);self.assertNotEqual(proc['returncode'],0);self.assertIn('CONTROLLED_PARTIAL',proc['stdout'])
  r,h,a,s,alloc=self.fixture();base=self.base(r,h,s,proc);base['receipt_verified']=False;base.pop('attempt_count')
  bridge.finalize_result(base,r,h,proc['elapsed_seconds'],True)
  self.assertEqual(base['state'],'TIMED_OUT');self.assertIsNone(base['account']['history'][0]['internal_attempt_count']);self.assertFalse(base['receipt_verified'])
  self.assertEqual(base['process']['stdout'],proc['stdout'])
 def test_controlled_nonzero_exit_not_geometry_failure(self):
  proc=run_bounded([sys.executable,'-u','-c',"print('CONTROLLED_FAILURE',flush=True); raise SystemExit(7)"],2)
  self.assertEqual(proc['returncode'],7);self.assertTrue(proc['wait_completed']);self.assertFalse(proc['timed_out'])
  r,h,a,s,alloc=self.fixture();base=self.base(r,h,s,proc);base.update(state='FAILED_CLOSED',receipt_verified=False);base.pop('attempt_count')
  bridge.finalize_result(base,r,h,proc['elapsed_seconds'],True);self.assertEqual(base['state'],'FAILED_CLOSED');self.assertFalse(base['receipt_verified'])
if __name__=='__main__':unittest.main()
