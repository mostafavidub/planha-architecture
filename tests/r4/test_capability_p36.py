"""Controlled on-wire P36 response disclosure; no generation, no replay."""
import hashlib,http.client,json,sys,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import capability_p36 as c
import current_entry_launch_x03 as launcher
import public_wln_server as server
import http_withholding_x04 as x04

N2=b'{"W":"18.1","L":"22.2","n":2}'
N1=b'{"W":"18","L":"20","n":1}'
AUTH={k:False for k in c.AUTH}
def sh(b):return hashlib.sha256(b).hexdigest()
def controlled(body,_,*,deadline):
 pf=server.preflight(body);e=pf.get('envelope',pf.get('public_envelope'));n=e['canonical_request']['unit_count']
 row={'receipt_verified':True,'nonce':'f'*32,'model_digest':'e'*64,'decision_digest':'d'*64}
 r={'fresh_model_executed':True,'source_integrity_verified':True,'preflight':pf,'attempts':[row],
    'current_decision':{'state':'BLOCKED','blockers':['CURRENT_UNKNOWN'],**AUTH},**AUTH}
 if n==2:
  row['state']=c.COMPLETED
  r.update(schema='AUTOMATIC_PROGRAM_LIVE_SINGLE_CASE_V1',state=c.PAIR_STATE,
   http_full_evidence={'schema':c.PAIR,'binding_verified':True,'state':'SAME_REQUEST_FULL_REPORT_CONSISTENCY_VERIFIED_SCOPED',
     'request_digest':sh(body),'file_count':9,'nonce_digest':sh(json.dumps(row['nonce']).encode()),'model_digest':'e'*64,
     'decision_digest':'d'*64,'source_digest':'a'*64,'file_hashes_digest':'b'*64,**AUTH})
 else:
  obs={'model':'e'*64,'summary':'c'*64,'decision':'d'*64}
  row.update(state='FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED',timed_out=False,returncode=0,wait_completed=True,
    observed_model_digest='e'*64,runtime_digest='c'*64,observed_file_hashes=obs,physical_status='PASS_CONCEPT_SCOPED_REVIEW',physical_errors=0,physical_pending=0,current_states=dict.fromkeys(c.CURRENT,'UNKNOWN'))
  r.update(schema='SINGLE_HTTP_RESULT_P17_V1',state='BLOCKED',http_full_evidence={'schema':c.SINGLE,'binding_verified':True},
    http_diagnostic={'schema':'P17_PRIVATE_DIAGNOSTIC_V1','request_digest':sh(body),'runtime_nonce':row['nonce'],
      'source_integrity_observed':True,'within_budget_observed':True,'observed_model_digest':'e'*64,'observed_file_hashes':obs})
 return r
class CapTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=launcher.server('PUBLIC_WLN_18X20');cls.t=threading.Thread(target=cls.s.serve_forever);cls.t.start()
 @classmethod
 def tearDownClass(cls):cls.s.shutdown();cls.t.join(5);cls.s.server_close()
 def post(self,b):
  cn=http.client.HTTPConnection('127.0.0.1',self.s.server_port,timeout=10)
  try:
   cn.request('POST','/api/public/plan',b,{'Content-Type':'application/json'});r=cn.getresponse()
   return r.status,json.loads(r.read())
  finally:cn.close()
 def cap(self,row,kind,b):
  v=row['capability'];self.assertEqual(v['schema'],c.SCHEMA);self.assertEqual(v['capability_state'],kind)
  self.assertEqual(v['request_digest'],sh(b));self.assertFalse(v['product_available'])
  self.assertTrue(all(v[k]is False for k in c.AUTH));return v
 def test_wire_invalid_and_valid_unsupported_no_worker(self):
  rows=[(b'{"W":"20","L":"25","n":3}',422,'INVALID_INPUT'),(b'{"W":20.0,"L":"25","n":2}',409,'WIRE_UNSUPPORTED'),
        (b'{"W":"20","L":"25","n":2}',409,'VALID_UNSUPPORTED'),(b'{"W":"17","L":"20","n":1}',409,'VALID_UNSUPPORTED')]
  with patch.object(server,'run_bound',side_effect=AssertionError('NO_DISPATCH'))as no:
   for body,status,kind in rows:
    h,r=self.post(body);self.assertEqual(h,status);d=self.cap(r,kind,body)
    self.assertIsNone(d['selected_study']);self.assertEqual(d['evidence_state'],'NOT_VERIFIED')
    self.assertEqual(d['input_state']=='VALID',kind=='VALID_UNSUPPORTED')
    self.assertEqual(d['canonical_case'] is not None,kind=='VALID_UNSUPPORTED')
   no.assert_not_called()
 def test_permitted_and_verified_each_control_family(self):
  for b,contract,family in ((N1,c.SINGLE,'SINGLE_FRONT_TOP_CORE_P15_V1'),(N2,c.PAIR,'FRONT_REAR')):
   with patch.object(server,'run_bound',side_effect=controlled):
    h,r=self.post(b);self.assertEqual(h,200);d=self.cap(r,'STUDY_PERMITTED',b)
   self.assertEqual(d['selected_study']['family'],family);self.assertEqual(d['evidence_contract'],contract)
   self.assertEqual(d['evidence_state'],'SAME_REQUEST_STUDY_REPORTS_VERIFIED')
   self.assertFalse(r['http_lifecycle']['receipt_verified'])
   self.assertEqual(x04.digest({k:v for k,v in r.items()if k!='http_lifecycle'}),r['http_lifecycle']['summary_digest'])
   self.assertFalse(r['accepted']);self.assertFalse(r['delivery_allowed']);self.assertEqual(r['decision']['state'],'BLOCKED')
  self.assertEqual(d['canonical_case']['dimensions_m']['W'],{'numerator':'181','denominator':'10'})
 def test_stale_missing_or_contradictory_cannot_promote(self):
  for body,key,value in ((N1,'http_diagnostic',{}),(N2,'http_full_evidence',{}),(N2,'fresh_model_executed',False),(N1,'http_diagnostic',{'request_digest':'0'*64})):
   def invalid(b,fn,*,deadline):return {**controlled(b,fn,deadline=deadline),key:value}
   with patch.object(server,'run_bound',side_effect=invalid):
    h,r=self.post(body)
   self.assertEqual(h,200);self.assertEqual(self.cap(r,'STUDY_PERMITTED',body)['evidence_state'],'NOT_VERIFIED')
 def test_single_wrong_semantic_state_and_pair_wrong_version(self):
  for b,fault in ((N1,'state_type'),(N1,'pending_conflict'),(N1,'model_drift'),(N2,'wrong_version'),(N2,'source_unverified')):
   def malformed(body,fn,*,deadline):
    v=controlled(body,fn,deadline=deadline);row=v['attempts'][0]
    if fault=='state_type':row['current_states'][c.CURRENT[0]]=True
    elif fault=='pending_conflict':row['physical_pending']=1
    elif fault=='model_drift':row['observed_file_hashes']['model']='0'*64
    elif fault=='wrong_version':v['preflight']['binding']['schema']='OTHER'
    else:v['source_integrity_verified']=False
    return v
   with patch.object(server,'run_bound',side_effect=malformed):
    status,r=self.post(b)
   if fault=='source_unverified':
    self.assertEqual(status,500);self.assertEqual(self.cap(r,'SERVER_RESULT_UNAVAILABLE',b)['evidence_state'],'NOT_VERIFIED')
   else:
    self.assertEqual(status,200);self.assertEqual(self.cap(r,'STUDY_PERMITTED',b)['evidence_state'],'NOT_VERIFIED')
 def test_busy_withheld_and_changed_projection_cannot_promote(self):
  with server.LOCK,patch.object(server,'run_bound',side_effect=AssertionError('NO_DISPATCH'))as no:
   h,r=self.post(N1);self.assertEqual(h,409);self.assertEqual(self.cap(r,'STUDY_BUSY',N1)['evidence_state'],'NOT_VERIFIED');no.assert_not_called()
  release=threading.Event()
  def slow(b,fn,*,deadline):release.wait(5);return controlled(b,fn,deadline=deadline)
  with patch.object(x04,'LIMIT_SECONDS',.35),patch.object(server,'run_bound',side_effect=slow):
   try:
    h,r=self.post(N1);self.assertEqual(h,504);self.assertEqual(self.cap(r,'STUDY_RESULT_WITHHELD',N1)['evidence_state'],'NOT_VERIFIED')
    self.assertIsNone(r['capability']['evidence_contract'])
   finally:release.set()
   stop=time.monotonic()+5
   while server.LOCK.locked() and time.monotonic()<stop:time.sleep(.02)
  self.assertFalse(server.LOCK.locked())
 def test_non_capability_fields_and_preflight_unchanged(self):
  v=controlled(N1,None,deadline=0);pf=json.loads(json.dumps(v['preflight']))
  a=server.public_summary(v,N1);b=server.with_capability(a,'STUDY_PERMITTED',N1,pf['envelope'],pf,v)
  self.assertEqual(a,{k:z for k,z in b.items()if k!='capability'});self.assertEqual(pf,v['preflight'])
if __name__=='__main__':unittest.main()
