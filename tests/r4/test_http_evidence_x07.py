"""Synthetic file writer only; real HTTP, consumer, bind_completed and assemble.
No solver, constructor, physical evaluator or geometry authenticity is exercised.
"""
import copy,hashlib,http.client,json,shutil,sys,threading,time,unittest,uuid
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'app/local_integration'))
import public_wln_server as server
import http_evidence_x07 as x
import live_program_scheduler as live
import current_four_decision as dec
from test_current_four_decision import fixture
BODY=b'{"W":"18","L":"20","n":2}'
def write(p,v):p.write_text(json.dumps(v,sort_keys=True,ensure_ascii=False,allow_nan=False))
class HTTP(unittest.TestCase):
 def setUp(self):
  self.folders=[];self.raw=None
  self.s=server.server();self.thread=threading.Thread(target=self.s.serve_forever,daemon=True);self.thread.start()
 def tearDown(self):
  self.s.shutdown();self.s.server_close();self.thread.join()
  for p in self.folders:shutil.rmtree(p,ignore_errors=True)
  self.assertFalse(server.LOCK.locked())
 def request(self):
  c=http.client.HTTPConnection('127.0.0.1',self.s.server_port,timeout=10)
  c.request('POST','/api/public/plan',BODY,{'Content-Type':'application/json'})
  r=c.getresponse();status=r.status;out=json.loads(r.read());c.close();return status,out
 def make(self,body,change=None,nonce=None):
  nonce=nonce or uuid.uuid4().hex;folder=x.EVIDENCE_ROOT/nonce;folder.mkdir(parents=True,exist_ok=True);self.folders.append(folder)
  pf=live.preflight(body);b,reports,pins=fixture()
  b.update(binding=pf['binding'],completed=True,model_binding_verified=True,constructor_called=True,construction_returned=True,**{k:False for k in live.AUTH})
  decision=dec.assemble(b,reports,pins)
  req={'schema':'LIVE_PROGRAM_ATTEMPT_V1','nonce':nonce,'body_hex':body.hex(),'preflight_digest':x.digest(pf),'budget':live.budgets()}
  child={'schema':'LIVE_SCHEDULER_CHILD_V1','nonce':nonce,'request_digest':x.digest(req),'preflight_digest':x.digest(pf),
   'programme_digest':pf['binding']['program_registry_digest'],'contract_digest':pf['binding']['contract_digest'],
   'runtime_digest':x.digest(b),'model_digest':b['model_digest'],'decision_digest':x.digest(decision),
   'decision':copy.deepcopy(decision['decision']),'assessments':copy.deepcopy(reports),'state':x.COMPLETE,**{k:False for k in live.AUTH}}
  row={'state':x.COMPLETE,'nonce':nonce,'attempt_id':'PROGRAM_2BED_V1:'+nonce,'budget_account_id':nonce,
   'receipt_verified':True,**{k:child[k] for k in ('model_digest','runtime_digest','decision_digest')}}
  raw={'schema':'AUTOMATIC_PROGRAM_LIVE_SINGLE_CASE_V1','preflight':pf,'budget':live.budgets(),'attempts':[row],
   'state':'LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED','source_integrity_verified':True,
   'fresh_model_executed':True,'current_decision':copy.deepcopy(decision['decision']),
   'evidence_directory':'live-program-evidence/'+nonce,**{k:False for k in live.AUTH}}
  docs={'request.json':req,'runtime-bundle.json':b,'child-complete.json':child,'decision.json':decision,'scheduler.json':copy.deepcopy(raw),
   **{k+'.json':r for k,r in reports.items()}}
  if change:change(raw,docs)
  for name,obj in docs.items():write(folder/name,obj)
  self.raw=copy.deepcopy(raw);self.before={p.name:p.read_bytes() for p in folder.iterdir()};self.folder=folder
  return raw
 def assert_files_unchanged(self):
  self.assertEqual(self.before,{p.name:p.read_bytes() for p in self.folder.iterdir()})
 def http_case(self,change=None):
  with patch.object(server,'run_live',side_effect=lambda b:self.make(b,change)) as run:
   result=self.request();run.assert_called_once_with(BODY)
  self.assert_files_unchanged();return result
 def test_healthy_real_consumer_unknown_and_fail_retained(self):
  status,out=self.http_case();self.assertEqual(status,200)
  self.assertEqual(out['decision']['state'],'BLOCKED')
  self.assertIn('CURRENT_UNKNOWN',out['decision']['blockers']);self.assertIn('PHYSICAL_FAIL',out['decision']['blockers'])
  self.assertTrue(out['full_evidence_binding']['binding_verified'])
  self.assertFalse(out['full_evidence_binding']['producer_authenticity_verified'])
  self.assertFalse(out['http_lifecycle']['receipt_verified'])
  self.assertTrue(all(out[k]is False for k in live.AUTH))
  self.assertNotIn('original_reports',out);self.assertNotIn('file_bytes',out)
 def test_changed_summary_no_raw_rewrite(self):
  def change(raw,docs):raw['current_decision']={'state':'FORGED'}
  status,out=self.http_case(change);self.assertEqual(status,500);self.assertNotIn('decision',out)
 def test_rehashed_false_decision(self):
  def change(raw,d):
   d['decision.json']['decision']['blockers']=[]
   d['child-complete.json']['decision']=copy.deepcopy(d['decision.json']['decision'])
   d['child-complete.json']['decision_digest']=x.digest(d['decision.json'])
   raw['current_decision']=copy.deepcopy(d['decision.json']['decision'])
   raw['attempts'][0]['decision_digest']=d['child-complete.json']['decision_digest'];d['scheduler.json']=copy.deepcopy(raw)
  self.assertEqual(self.http_case(change)[0],500)
 def test_other_request_nonce(self):
  def change(raw,d):d['request.json']['nonce']='f'*32
  self.assertEqual(self.http_case(change)[0],500)
 def test_other_model_even_rehashed(self):
  def change(raw,d):
   d['runtime-bundle.json']['packet']['world_model']['other']=True
   d['child-complete.json']['runtime_digest']=x.digest(d['runtime-bundle.json'])
   raw['attempts'][0]['runtime_digest']=d['child-complete.json']['runtime_digest'];d['scheduler.json']=copy.deepcopy(raw)
  self.assertEqual(self.http_case(change)[0],500)
 def test_source_snapshot_mismatch(self):
  def change(raw,d):
   key='CONTINUOUS_USEFUL_LIVING';r=d[key+'.json'];r['source_snapshot'][next(iter(r['source_snapshot']))]='0'*64
   d['child-complete.json']['assessments'][key]=copy.deepcopy(r)
  self.assertEqual(self.http_case(change)[0],500)
 def test_missing_report(self):
  def change(raw,d):del d['CONTINUOUS_USEFUL_LIVING.json']
  self.assertEqual(self.http_case(change)[0],500)
 def test_source_false_withheld(self):
  def change(raw,d):raw['source_integrity_verified']=False
  self.assertEqual(self.http_case(change)[0],500)
 def test_reused_directory_not_new_request(self):
  raw=self.make(BODY)
  with patch.object(server,'run_live',return_value=raw):status,out=self.request()
  self.assertEqual(status,500);self.assertNotIn('decision',out);self.assert_files_unchanged()
 def test_symlink_file(self):
  def writer(body):
   raw=self.make(body);p=self.folder/'decision.json';p.unlink();p.symlink_to(self.folder/'scheduler.json');return raw
  with patch.object(server,'run_live',side_effect=writer):self.assertEqual(self.request()[0],500)
 def test_path_from_return_cannot_escape(self):
  def change(raw,d):raw['evidence_directory']='../other';d['scheduler.json']=copy.deepcopy(raw)
  self.assertEqual(self.http_case(change)[0],500)
 def test_direct_failure_keeps_original_json_and_bytes(self):
  before=x.existing_nonces();sources=x.guard();raw=self.make(BODY)
  path=self.folder/'request.json';path.write_bytes(b'{')
  with self.assertRaises(x.EvidenceFailure) as caught:x.consume(BODY,raw,before,sources)
  e=caught.exception.private_evidence
  self.assertEqual(e['file_bytes']['request.json'],b'{');self.assertFalse(e['verified'])
  self.assertEqual(e['parsed']['runtime-bundle.json']['reports']['physical']['status'],'FAIL')
  self.assertEqual(len(e['file_hashes']),9)
 def test_mid_read_replacement(self):
  before=x.existing_nonces();sources=x.guard();raw=self.make(BODY);real=x.read_file;count={}
  def changed(path):
   data,identity=real(path);count[path.name]=count.get(path.name,0)+1
   if path.name=='decision.json' and count[path.name]>1:return data+b' ',identity
   return data,identity
  with patch.object(x,'read_file',side_effect=changed):
   with self.assertRaises(x.EvidenceFailure) as caught:x.consume(BODY,raw,before,sources)
  self.assertEqual(caught.exception.reason_code,'X07_FILES_CHANGED')
 def test_callable_swapped_after_writer_rejected_before_call(self):
  original=dec.assemble;called=[]
  def shadow(*a):called.append(True);raise AssertionError('MUST_NOT_CALL')
  def writer(body):
   raw=self.make(body);dec.assemble=shadow;return raw
  try:
   with patch.object(server,'run_live',side_effect=writer):self.assertEqual(self.request()[0],500)
   self.assertEqual(called,[])
  finally:dec.assemble=original
 def test_consumer_late_result_withheld_and_lock_held(self):
  import http_withholding_x04 as boundary
  release=threading.Event();entered=threading.Event();real=x.read_file
  def slow(path):
   if path.name=='request.json':entered.set();release.wait(4)
   return real(path)
  try:
   with patch.object(server,'run_live',side_effect=lambda b:self.make(b)),patch.object(x,'read_file',side_effect=slow),patch.object(boundary,'LIMIT_SECONDS',.15):
    status,out=self.request();self.assertEqual(status,504);self.assertTrue(entered.is_set())
    self.assertTrue(server.LOCK.locked());self.assertNotIn('decision',out)
    release.set()
    end=time.monotonic()+4
    while server.LOCK.locked() and time.monotonic()<end:time.sleep(.005)
    self.assertFalse(server.LOCK.locked())
  finally:
   release.set()
   end=time.monotonic()+4
   while server.LOCK.locked() and time.monotonic()<end:time.sleep(.005)
 def test_strict_types_duplicates_and_nonfinite(self):
  for value in (b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}'):
   with self.assertRaises(ValueError):x.decode(value)
  with self.assertRaises(ValueError):x.digest((1,2))
  self.assertNotEqual(x.digest(True),x.digest(1));self.assertNotEqual(x.digest(1),x.digest(1.0))
if __name__=='__main__':unittest.main()
