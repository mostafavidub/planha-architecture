"""Controlled actual boundary and temporary-file failure; no solver/model fixture."""
import hashlib,json,sys,tempfile,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import http_withholding_x04 as x
import single_runtime_p17 as r
BODY=b'{"W":"18","L":"20","n":1}'
SHA=hashlib.sha256(BODY).hexdigest()
class Forensic(unittest.TestCase):
 def value(self,sha=SHA):
  return {'schema':'P17_PRIVATE_DIAGNOSTIC_V1','request_digest':sha,'runtime_nonce':'a'*32,'worker_state':'FAILED_CLOSED','error_code':'P17_TEST_FAILURE','error_type':'ValueError','observed_file_hashes':{'summary':'b'*64},'evidence_usable':True}
 def execute(self,run,project=lambda raw:{'state':'BLOCKED'}):
  b=x.Boundary();lock=threading.Lock();lock.acquire()
  status,out=b.execute(BODY,accepted_at=time.monotonic(),lock=lock,run=run,project=project)
  self.assertFalse(lock.locked());return status,out,b.snapshot()
 def test_exception_record_no_response_diagnostic(self):
  def fail(body):raise r.DiagnosticFailure(self.value())
  status,out,records=self.execute(fail)
  self.assertEqual(status,500);self.assertNotIn('runtime_diagnostic',out)
  self.assertEqual(records[0]['runtime_diagnostic']['error_code'],'P17_TEST_FAILURE')
  self.assertFalse(records[0]['runtime_diagnostic']['evidence_usable'])
 def test_source_false_observation_retained_without_decision(self):
  status,out,records=self.execute(lambda body:{'source_integrity_verified':False,'attempts':[],'http_diagnostic':self.value()})
  self.assertEqual(status,500);self.assertNotIn('decision',out)
  self.assertEqual(records[0]['worker_state'],'SOURCE_UNVERIFIED_OBSERVED')
  self.assertEqual(records[0]['runtime_diagnostic']['state'],'OBSERVED_UNVERIFIED')
 def test_old_request_diagnostic_not_reused(self):
  status,out,records=self.execute(lambda body:{'source_integrity_verified':False,'attempts':[],'http_diagnostic':self.value('c'*64)})
  self.assertEqual(records[0]['runtime_diagnostic'],{'state':'REQUEST_MISMATCH_REJECTED'})
  self.assertEqual(records[0]['request_digest'],SHA)
 def test_late_failure_still_withheld_and_lock_owned(self):
  b=x.Boundary();lock=threading.Lock();lock.acquire();release=threading.Event();entered=threading.Event()
  def run(body):
   entered.set();release.wait(3);raise r.DiagnosticFailure(self.value())
  try:
   with patch.object(x,'LIMIT_SECONDS',.05):
    status,out=b.execute(BODY,accepted_at=time.monotonic(),lock=lock,run=run,project=lambda raw:raw)
   self.assertTrue(entered.is_set());self.assertEqual(status,504);self.assertTrue(lock.locked())
  finally:release.set()
  end=time.monotonic()+3
  while lock.locked()and time.monotonic()<end:time.sleep(.005)
  self.assertFalse(lock.locked());record=b.snapshot()[0]
  self.assertEqual(record['response_state'],'WITHHELD');self.assertTrue(record['worker_state'].startswith('LATE_'))
  self.assertEqual(record['runtime_diagnostic']['error_code'],'P17_TEST_FAILURE')
 def test_shape_filter_not_free_text_or_arbitrary_fields(self):
  value=self.value();value.update(error_code='private free text',raw_model={'private':True},observed_file_hashes={'unknown_path':'b'*64,'summary':'not digest'})
  out=x.diagnostic_record(value,SHA)
  self.assertIsNone(out['error_code']);self.assertNotIn('raw_model',out);self.assertEqual(out['observed_file_hashes'],{})
 def test_project_error_retains_runtime_observation(self):
  def project(raw):raise ValueError('P17_PROJECT_FAILURE')
  status,out,records=self.execute(lambda body:{'http_diagnostic':self.value()},project)
  self.assertEqual(status,500);self.assertEqual(records[0]['boundary_error']['error_code'],'P17_PROJECT_FAILURE')
  self.assertEqual(records[0]['runtime_diagnostic']['error_code'],'P17_TEST_FAILURE')
 def test_file_error_before_cleanup_is_observed_not_verified(self):
  class Process:
   returncode=0;pid=1
   def __init__(self,args,**kwargs):
    folder=Path(args[-1]);(folder/'summary.json').write_text('{"incomplete":')
   def communicate(self,timeout=None):return b'',b''
   def poll(self):return 0
  with patch.object(r.binding,'source_audit',return_value={'controlled':True}),patch.object(r.p,'preflight',return_value={'execution_ready':True}),patch.object(r.subprocess,'Popen',Process):
   with self.assertRaises(r.DiagnosticFailure)as caught:r.run_bound(BODY,time.monotonic()+10)
  value=caught.exception.http_diagnostic
  self.assertEqual(value['parent_stage'],'READ_SUMMARY');self.assertEqual(value['error_type'],'JSONDecodeError')
  self.assertFalse(value['evidence_usable']);self.assertEqual(value['request_digest'],SHA)
 def test_scalar_summary_diagnostic_cannot_mask_error(self):
  out=r.diagnostic(BODY,{'nonce':'a'*32},0,{},'READ_SUMMARY',ValueError('P17_TEST'))
  self.assertEqual(out['error_code'],'P17_TEST');self.assertIsNone(out['worker_state'])
if __name__=='__main__':unittest.main(verbosity=2)
