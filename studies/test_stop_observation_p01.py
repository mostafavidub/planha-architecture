"""P01 synthetic source-shaped observations and real HTTP, NEVER a solver run.
Controlled Popen writes existing worker file formats; actual parser, dispatcher,
runtime readback, helper, X04 and HTTP projection execute. No authenticity claim.
"""
import copy,hashlib,http.client,json,subprocess,sys,tempfile,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import stop_observation_p01 as s
import single_runtime_p17 as r
import public_wln_server as server
import http_withholding_x04 as boundary
BODY=b'{"W":"18","L":"20","n":1}'
NONCE='a'*32
MH='b'*64
def save(folder,name,value):(folder/name).write_text(json.dumps(value,ensure_ascii=False,sort_keys=True),encoding='utf-8')
def proposal(code,status):
 return {'status':status,'solver_status':code,'solver_seconds':.01,'budget_seconds':30,'solver_message':'PRIVATE FREE TEXT'}
def fixture(folder,q=None,stage='PROPOSE',failed=False):
 request=json.loads((folder/'request.json').read_text())
 save(folder,'summary.json',{'nonce':request['nonce'],'stage':stage,'state':'FAILED_CLOSED'if failed else'NO_MODEL_IN_THIS_ATTEMPT','attempts':1,'source_integrity_verified':True,'within_budget':True,'error_type':'ValueError'if failed else None})
 if q is not None:save(folder,'proposal.json',q)
 save(folder,'originals.json',{'physical':{'model_hash':MH,'status':'FAIL','errors':[{'code':'BODY_WALL_COLLISION','detail':'PRIVATE FREE TEXT'},{'code':'PRIVATE_UPPERCASE_SECRET'}],'pending':[]}})
class Observation(unittest.TestCase):
 def test_source_allowlist_not_regex(self):
  ph=s.physical_observation({'model_hash':MH,'status':'FAIL','errors':[{'code':'BODY_WALL_COLLISION'},{'code':'PRIVATE_UPPERCASE_SECRET'},'PRIVATE FREE TEXT'],'pending':[]},MH,False)
  self.assertEqual(ph['error_count'],3);self.assertEqual(ph['error_codes'],[{'code':'BODY_WALL_COLLISION','count':1},{'code':'UNKNOWN_CODE','count':2}])
  self.assertNotIn('PRIVATE',json.dumps(ph))
 def test_bad_summary_keeps_healthy_sibling_and_exact_bytes_hash(self):
  with tempfile.TemporaryDirectory()as name:
   folder=Path(name);raw=b'{"partial":'
   (folder/'summary.json').write_bytes(raw);save(folder,'originals.json',{'physical':{'status':'FAIL','errors':[{'code':'RULE_FAILED'}],'pending':[]}})
   snap=s.snapshot(folder);row=next(x for x in snap['files']if x['file']=='summary.json')
   self.assertEqual(row['bytes_digest'],hashlib.sha256(raw).hexdigest());self.assertEqual(row['state'],'PARSE_FAILED')
   self.assertIn('originals.json',snap['parsed']);self.assertEqual(snap['private_bytes']['summary.json'],raw)
   out=s.observe(BODY,NONCE,'FRONT_REAR',snap)
   self.assertEqual(out['outcome'],'EVIDENCE_READ_ERROR');self.assertFalse(out['binding_verified'])
   self.assertEqual(out['physical']['error_codes'],[{'code':'RULE_FAILED','count':1}])
 def test_timeout_no_file_is_unknown_not_false(self):
  out=s.observe(BODY,NONCE,'FRONT_REAR',{'parsed':{},'files':[]},timed_out=True)
  self.assertEqual(out['outcome'],'OUTER_TIMEOUT');self.assertIsNone(out['solver']['incumbent_observed']);self.assertEqual(out['solver']['evidence'],'UNOBSERVED')
 def test_pre_solver_and_numeric_semantics(self):
  _,_,pre=s.solver_observation({'status':'NO_PROPOSAL_IN_THIS_PROGRAM','reason':'ROOM_OR_CORE_BOUND_CONFLICT'})
  self.assertIs(pre['called'],False);self.assertIsNone(pre['incumbent_observed'])
  _,_,bad=s.solver_observation({'status':'PROPOSAL_ONLY','solver_status':True,'solver_seconds':1,'budget_seconds':30})
  self.assertIsNone(bad['called']);self.assertIsNone(bad['incumbent_observed'])
 def test_partial_nonfinite_duplicate_and_symlink(self):
  with tempfile.TemporaryDirectory()as name:
   folder=Path(name);(folder/'summary.json').write_text('{"x":NaN}')
   (folder/'proposal.json').write_text('{"x":1,"x":2}')
   (folder/'originals.json').symlink_to(folder/'summary.json')
   snap=s.snapshot(folder);states={x['file']:x['state']for x in snap['files']}
   self.assertEqual(states['summary.json'],'PARSE_FAILED');self.assertEqual(states['proposal.json'],'PARSE_FAILED');self.assertEqual(states['originals.json'],'READ_FAILED')
 def test_wrong_nonce_model_source_never_bound(self):
  snap={'parsed':{'request.json':{'nonce':'c'*32,'body_hex':BODY.hex()},'summary.json':{'model_digest':MH},'originals.json':{'physical':{'model_hash':'d'*64,'errors':[],'pending':[]}}},'files':[]}
  out=s.observe(BODY,NONCE,'FRONT_REAR',snap,bound=True,source_ok=True)
  self.assertFalse(out['binding_verified']);self.assertEqual(out['physical']['state'],'OBSERVED_UNVERIFIED')
  snap['parsed']['request.json']['nonce']=NONCE
  out=s.observe(BODY,NONCE,'FRONT_REAR',snap,bound=True,source_ok=False)
  self.assertFalse(out['binding_verified'])
 def test_safe_wrong_request_rehashed_unknown_code_and_bool(self):
  out=s.unsupported(BODY);sha=hashlib.sha256(BODY).hexdigest();self.assertIsNotNone(s.safe(out,sha));self.assertIsNone(s.safe(out,'f'*64))
  for change in ({'outcome':'PRIVATE_UPPERCASE_SECRET'},{'binding_verified':1}):
   bad=copy.deepcopy(out);bad.update(change);bad['record_digest']=s.digest({k:v for k,v in bad.items()if k!='record_digest'});self.assertIsNone(s.safe(bad,sha))
 def test_actual_source_pins(self):
  snap=s.source_snapshot();self.assertIn('single_physical_p17.py',snap);self.assertIn('search114.py',snap)
 def test_shadow_snapshot_rejected_before_call(self):
  called=[]
  def shadow(*a,**kw):called.append(True);raise AssertionError('MUST_NOT_CALL')
  with patch.object(s,'snapshot',shadow):
   with self.assertRaisesRegex(ValueError,'P01_IMPORT_PATH'):s.source_snapshot()
  self.assertEqual(called,[])
 def test_start_failure_is_retained_before_cleanup(self):
  with patch.object(r.binding,'source_audit',return_value={'controlled':True}),patch.object(r.subprocess,'Popen',side_effect=OSError('PRIVATE FREE TEXT')):
   with self.assertRaises(r.DiagnosticFailure)as caught:r.run_bound(BODY,time.monotonic()+30)
  record=caught.exception.http_diagnostic['stop_record']
  self.assertEqual(record['outcome'],'WORKER_START_FAILED');self.assertIsNone(record['solver']['incumbent_observed']);self.assertNotIn('PRIVATE',json.dumps(record))
 def test_n1_bad_summary_after_cleanup_preserves_bytes_and_codes(self):
  class Process:
   returncode=0;pid=1
   def __init__(self,args,**kw):
    folder=Path(args[-1]);fixture(folder);(folder/'summary.json').write_bytes(b'{"partial":')
   def communicate(self,timeout=None):return b'',b''
   def poll(self):return 0
  with patch.object(r.binding,'source_audit',return_value={'controlled':True}),patch.object(r.subprocess,'Popen',Process):
   with self.assertRaises(r.DiagnosticFailure)as caught:r.run_bound(BODY,time.monotonic()+30)
  record=caught.exception.http_diagnostic['stop_record']
  self.assertEqual(record['outcome'],'EVIDENCE_READ_ERROR');self.assertEqual(record['physical']['error_count'],2)
  self.assertEqual(caught.exception.private_evidence['private_bytes']['summary.json'],b'{"partial":')
 def test_x04_private_record_request_binding_and_no_response_leak(self):
  record=s.unsupported(BODY);sha=hashlib.sha256(BODY).hexdigest()
  value={'schema':'P01_PRIVATE_DIAGNOSTIC_V1','request_digest':sha,'stop_record':record}
  out=boundary.diagnostic_record(value,sha);self.assertEqual(out['stop_record'],record)
  self.assertEqual(boundary.diagnostic_record(value,'c'*64),{'state':'REQUEST_MISMATCH_REJECTED'})
  b=boundary.Boundary();lock=threading.Lock();lock.acquire()
  def failure(body):
   ex=ValueError('CONTROLLED');ex.http_diagnostic=value;raise ex
  status,payload=b.execute(BODY,accepted_at=time.monotonic(),lock=lock,run=failure,project=lambda raw:raw)
  self.assertEqual(status,500);self.assertNotIn('stop_record',payload);self.assertEqual(b.snapshot()[0]['runtime_diagnostic']['stop_record'],record)
 def test_late_diagnostic_remains_private_and_does_not_release_early(self):
  record=s.unsupported(BODY);release=threading.Event();entered=threading.Event()
  b=boundary.Boundary();lock=threading.Lock();lock.acquire()
  def failure(body):
   entered.set();release.wait(3)
   ex=ValueError('CONTROLLED');ex.http_diagnostic={'schema':'P01_PRIVATE_DIAGNOSTIC_V1','request_digest':hashlib.sha256(BODY).hexdigest(),'stop_record':record};raise ex
  try:
   with patch.object(boundary,'LIMIT_SECONDS',.05):
    status,payload=b.execute(BODY,accepted_at=time.monotonic(),lock=lock,run=failure,project=lambda raw:raw)
   self.assertEqual(status,504);self.assertTrue(entered.is_set());self.assertTrue(lock.locked());self.assertNotIn('stop_record',payload)
  finally:release.set()
  end=time.monotonic()+3
  while lock.locked()and time.monotonic()<end:time.sleep(.005)
  self.assertFalse(lock.locked());self.assertEqual(b.snapshot()[0]['runtime_diagnostic']['stop_record'],record)
class HTTP(unittest.TestCase):
 def setUp(self):
  self.calls=0;self.mode=None
  owner=self
  class Process:
   returncode=0;pid=1
   def __init__(self,args,**kw):
    owner.calls+=1;folder=Path(args[-1]);mode=owner.mode
    if mode is None:raise AssertionError('UNEXPECTED_SPAWN')
    q,stage,failed=mode;fixture(folder,q,stage,failed);self.returncode=1 if failed else 0
   def communicate(self,timeout=None):return b'',b''
   def poll(self):return self.returncode
  self.spawn=patch.object(r.subprocess,'Popen',Process);self.spawn.start();self.addCleanup(self.spawn.stop)
  self.audit=patch.object(r.binding,'source_audit',return_value={'controlled_source_audit':True});self.audit.start();self.addCleanup(self.audit.stop)
  server.HTTP_BOUNDARY=boundary.Boundary()
  self.http=server.server();self.thread=threading.Thread(target=self.http.serve_forever,daemon=True);self.thread.start()
 def tearDown(self):
  self.http.shutdown();self.http.server_close();self.thread.join(3);self.assertFalse(server.LOCK.locked())
 def post(self,body=BODY):
  conn=http.client.HTTPConnection('127.0.0.1',self.http.server_port,timeout=30);conn.request('POST','/api/public/plan',body,{'Content-Type':'application/json'})
  response=conn.getresponse();data=json.loads(response.read());status=response.status;conn.close()
  end=time.monotonic()+2
  while server.LOCK.locked()and time.monotonic()<end:time.sleep(.005)
  return status,data
 def check(self,q,outcome,stage='PROPOSE',failed=False):
  self.mode=(q,stage,failed);status,data=self.post();self.assertEqual(status,200)
  record=data['stop_record'];self.assertEqual(record['outcome'],outcome);self.assertEqual(record['stage'],stage)
  self.assertIsNotNone(s.safe(record,hashlib.sha256(BODY).hexdigest()));self.assertEqual(self.calls,1)
  self.assertFalse(record['binding_verified']);self.assertFalse(data['download_available']);self.assertFalse(data['http_lifecycle']['evidence_usable'])
  self.assertNotIn('PRIVATE',json.dumps(data));return record
 def test_01_pre_program_rejection(self):
  body=b'{"W":"17","L":"20","n":1}';status,data=self.post(body)
  self.assertEqual(status,409);self.assertEqual(self.calls,0);self.assertEqual(data['stop_record']['outcome'],'VALID_UNSUPPORTED')
  self.assertEqual(data['stop_record']['programme'],'NOT_SELECTED')
 def test_02_infeasible_this_milp_not_global(self):
  self.check(proposal(2,'NO_PROPOSAL_IN_THIS_TOPOLOGY'),'SOLVER_INFEASIBLE_THIS_MILP')
 def test_03_timeout_return_without_incumbent(self):
  record=self.check(proposal(1,'SEARCH_TIMEOUT_NO_WITNESS'),'SOLVER_LIMIT_NO_INCUMBENT')
  self.assertIs(record['solver']['incumbent_observed'],False)
 def test_04_timeout_return_with_incumbent(self):
  record=self.check(proposal(1,'PROPOSAL_ONLY'),'SOLVER_LIMIT_WITH_INCUMBENT')
  self.assertIs(record['solver']['incumbent_observed'],True)
 def test_05_assembly_error_not_no_solution(self):
  self.check(proposal(0,'PROPOSAL_ONLY'),'ASSEMBLY_ERROR',stage='CONSTRUCT',failed=True)
 def test_06_successful_proposal_not_qualified_model(self):
  self.check(proposal(0,'PROPOSAL_ONLY'),'PROPOSAL_OBSERVED')
if __name__=='__main__':unittest.main(verbosity=2)
