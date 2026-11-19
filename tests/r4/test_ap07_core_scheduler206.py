"""Synthetic receipts and real controlled processes; no geometry solver."""
import copy,json,os,subprocess,sys,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'app/local_integration'))
import ap07_core_scheduler206 as s
def request():return s.make_request(s.BODY,time.monotonic(),480)
def fixture(r,index=0):
 choice=s.CHOICES[index];nonce=s.attempt_nonce(r,index);core,_=s.corestudy.selected_core(r['raw'],choice)
 model=s.digest(['SYNTHETIC_NOT_MODEL',index]);receipt=s.digest(['receipt',index]);program=s.digest('synthetic-program')
 old={p:r['source_snapshot'][p]for p in s.OLD_PATHS}
 preds={'core_partition':{'status':'PASS_SOURCE_CORE_PARTITION_ONLY','errors':[],'pending':[]},'core_concept':{'status':'PASS_LIMITED','errors':[],'pending':[]},'opening_hosts':{'status':'PASS_LIMITED','errors':[],'pending':[]}}
 ca={'choice':choice,'run_nonce':nonce,'model_hash':model,'raw_hash':s.digest(r['raw']),'profile_hash':s.digest(r['profile']),'core_hash':s.digest(core),'source_hash':s.digest(old),'origin_receipt_hash':receipt,
 'predicates':copy.deepcopy(preds),'core_scoped_verified':True,'state':'PASS_CORE_SCOPE_ONLY','program_hash':program,**{k:False for k in s.AUTH}}
 reports={**preds,'independent_replay':{'verified':True,'authority':False,'model_hash':model,'receipt_digest':receipt},
 'original_replay':{'verified':False,'model_hash':model,'errors':['SYNTHETIC_LEGACY_FAILURE']},
 'physical':{'status':'FAIL','model_hash':model,'errors':[],'pending':[]},'core_assessment':ca,
 'actual_detached_negatives':{'model_hash':model,'original_unchanged':True,'all_expected_rejected':True,'rows':[{'base_model_hash':model,'binding_rejected':True,'direct_geometry_rejected':True}for _ in range(6)]}}
 summary={'run_nonce':nonce,'choice':choice,'completed':True,'integrity_verified':True,'current_four':'NOT_EVALUATED_CORE_CHOICE_ADAPTER_MISSING','raw_digest':s.digest(r['raw']),'profile_digest':s.digest(r['profile']),
 'core_digest':s.digest(core),'source_digest':s.digest(old),'report_digests':{k:s.digest(v)for k,v in reports.items()},'state':'FULL_REPORTS_RETAINED_NOT_QUALIFIED','model_digest':model,'receipt_digest':receipt,
 'independent_origin_verified':True,'core_scoped_verified':True,'physical_status':'FAIL','physical_error_counts':{},'physical_pending_counts':{},'legacy_replay_verified':False,'program_digest':program,**{k:False for k in s.AUTH}}
 return summary,reports
class SharedCoreScheduler(unittest.TestCase):
 def test_actual_source_request_no_solver(self):
  r=request();s.validate_request(r,s.digest(r));self.assertEqual(r['choices'],list(s.CHOICES))
 def test_invalid_request_no_dispatch(self):
  for body in (b'{"W":"26","L":"20","n":2}',b'{"W":"18","L":"20","n":1}',b'{"W":"18","L":"20","n":2,"choice":"x"}'):
   with self.assertRaises(ValueError):s.make_request(body,1,480)
 def test_request_mutation_rehashed_rejected(self):
  for key,value in [('raw',dict(s.RAW,W='25')),('choices',[s.CHOICES[0]]*2),('max_attempts',True),('profile',{}),('solver_seconds_per_attempt',31)]:
   r=request();r[key]=value
   with self.assertRaises(ValueError):s.validate_request(r,s.digest(r))
 def test_source_rehashed_rejected(self):
  r=request();r['source_snapshot'][s.OLD_PATHS[0]]='0'*64
  with self.assertRaisesRegex(ValueError,'SOURCE_CHANGED'):s.validate_request(r,s.digest(r))
 def test_two_reservations_same_account_remaining(self):
  r=request();a=s.new_ledger(r);a=s.reserve(a,r,10);self.assertEqual(a['active']['allocated_seconds'],240)
  a=s.finish(a,r,245,'VERIFIED_CORE_STUDY',True,'1'*64);a=s.reserve(a,r,265)
  self.assertEqual(a['active']['allocated_seconds'],210);self.assertEqual(a['active']['token'],r['account_id']+':2')
  a=s.finish(a,r,300,'VERIFIED_CORE_STUDY',True,'2'*64);s.check_ledger(a,r)
  with self.assertRaises(ValueError):s.reserve(a,r,301)
 def test_token_history_reset_invalid(self):
  r=request();a=s.reserve(s.new_ledger(r),r,1);a=s.finish(a,r,4,'NO_PROPOSAL',True)
  for field,value in [('used_attempts',0),('used_seconds',0),('account_id','0'*32)]:
   bad=copy.deepcopy(a);bad[field]=value
   with self.assertRaises(ValueError):s.check_ledger(bad,r)
  a['history'][0]['token']='forged'
  with self.assertRaises(ValueError):s.check_ledger(a,r)
 def test_duplicate_model_no_progress(self):
  r=request();a=s.reserve(s.new_ledger(r),r,1);a=s.finish(a,r,3,'VERIFIED_CORE_STUDY',True,'1'*64)
  a=s.reserve(a,r,4);a=s.finish(a,r,6,'VERIFIED_CORE_STUDY',True,'1'*64)
  self.assertEqual(a['history'][-1]['outcome'],'REPEATED_MODEL');self.assertFalse(a['history'][-1]['receipt_verified'])
 def test_consumption_full_raw_fixture_not_authenticity(self):
  r=request()
  for i in range(2):
   a,b=fixture(r,i);out=s.consume(r,i,a,b)
   self.assertEqual(out['report_count'],8);self.assertFalse(out['legacy_replay_verified']);self.assertEqual(out['physical_status'],'FAIL')
 def test_missing_report_summary_only_rejected(self):
  r=request();a,b=fixture(r)
  for reports in ({},dict(b,physical=None)):
   with self.assertRaises((ValueError,TypeError)):s.consume(r,0,a,reports)
 def test_report_model_mutation_rehashed(self):
  r=request();a,b=fixture(r);b['physical']['model_hash']='9'*64;a['report_digests']['physical']=s.digest(b['physical'])
  with self.assertRaisesRegex(ValueError,'FULL_MODEL_REPORT_BINDING'):s.consume(r,0,a,b)
 def test_nonce_choice_summary_tamper(self):
  r=request()
  for key,value in [('run_nonce','0'*32),('choice',s.CHOICES[1]),('physical_status','PASS'),('core_scoped_verified',False),('current_four','PASS')]:
   a,b=fixture(r);a[key]=value
   with self.assertRaises(ValueError):s.consume(r,0,a,b)
 def test_final_source_failure_invalidation_preserves_observation(self):
  r=request();a=s.reserve(s.new_ledger(r),r,1);a=s.finish(a,r,3,'VERIFIED_CORE_STUDY',True,'1'*64)
  rows=[{'receipt_verified':True,'evidence_usable':True}];s.invalidate(a,rows,'SOURCE_ERROR')
  s.check_ledger(a,r);self.assertFalse(a['history'][0]['receipt_verified']);self.assertTrue(a['history'][0]['observed_receipt_verified']);self.assertFalse(rows[0]['evidence_usable'])
 def test_deadline_no_second_reservation(self):
  r=request();a=s.reserve(s.new_ledger(r),r,1);a=s.finish(a,r,200,'NO_PROPOSAL',True)
  with self.assertRaisesRegex(ValueError,'BUDGET_EXHAUSTED'):s.reserve(a,r,476)
 def test_controlled_timeout_group_kill_wait(self):
  p=subprocess.Popen([sys.executable,'-B','-c','import time;time.sleep(5)'],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  self.assertEqual(os.getpgid(p.pid),p.pid);out=s.wait_process(p,.05,True)
  self.assertTrue(out['timed_out']and out['wait_completed']);self.assertIsNotNone(p.returncode)
 def test_controlled_completion(self):
  p=subprocess.Popen([sys.executable,'-B','-c','pass'],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  out=s.wait_process(p,3,True);self.assertFalse(out['timed_out']);self.assertEqual(out['returncode'],0)
 def test_per_attempt_deadline_rehashed_contradiction(self):
  r=request();a=s.reserve(s.new_ledger(r),r,1);a=s.finish(a,r,242,'NO_PROPOSAL',True)
  self.assertEqual(a['history'][0]['outcome'],'TIMED_OUT');self.assertFalse(a['history'][0]['receipt_verified'])
  a['history'][0].update(outcome='NO_PROPOSAL',receipt_verified=True)
  with self.assertRaisesRegex(ValueError,'VERIFIED_AFTER_ATTEMPT_DEADLINE'):s.check_ledger(a,r)
 def test_rehashed_duplicate_receipt_rejected(self):
  r=request();a=s.reserve(s.new_ledger(r),r,1);a=s.finish(a,r,3,'VERIFIED_CORE_STUDY',True,'1'*64)
  a=s.reserve(a,r,4);a=s.finish(a,r,6,'VERIFIED_CORE_STUDY',True,'2'*64);a['history'][1]['model_digest']='1'*64
  with self.assertRaisesRegex(ValueError,'VERIFIED_DUPLICATE_MODEL'):s.check_ledger(a,r)
 def test_unknown_cli_and_index_never_launch(self):
  with patch.object(s,'run',side_effect=AssertionError('NO_SOLVER'))as run:
   for argv in (['script','--foo'],['script','--attempt','folder','-1'],['script','--worker']):
    with self.assertRaisesRegex(ValueError,'CLI_ARGUMENTS'):s.dispatch(argv)
   run.assert_not_called()
  for index in (-1,2,True,'0'):
   with self.assertRaisesRegex(ValueError,'ATTEMPT_INDEX'):s.attempt_nonce(request(),index)
if __name__=='__main__':unittest.main()

