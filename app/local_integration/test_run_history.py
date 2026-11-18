import json,tempfile,unittest,uuid,copy
from pathlib import Path
from run_history import summary,list_history,output_gate
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'manifests/WORKTREE_STATE.json').is_file())
class HistoryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
  self.result=json.loads((ROOT/'app/local_integration/evidence/review_cycle/integrated_http_result.json').read_text());self.id=self.result['run_id'];self.folder=self.base/self.id;self.folder.mkdir();self.body=json.dumps({'W':'25','L':'27','n':2,'requested_count':1}).encode();self.save()
 def tearDown(self):self.tmp.cleanup()
 def save(self):
  (self.folder/'request.json').write_bytes(self.body);(self.folder/'result.json').write_text(json.dumps(self.result));(self.folder/'lifecycle.json').write_text(json.dumps({'wait_completed':True}))
 def test_historical_only_no_model(self):
  r=summary(self.id,self.base);self.assertTrue(r['historical_only']);self.assertNotIn('model',r['candidates'][0]);self.assertFalse(r['live_model_restored'])
 def test_output_denied(self):
  status,r=output_gate(self.id,self.base);self.assertEqual(status,403);self.assertEqual(r['artifact_bytes_sent'],0)
 def test_model_tamper(self):
  self.result['candidates'][0]['model']['inputs'][0]='30';self.save()
  with self.assertRaises(ValueError):summary(self.id,self.base)
 def test_review_tamper(self):
  self.result['candidates'][0]['review_decision']['state']='OTHER';self.save()
  with self.assertRaises(ValueError):summary(self.id,self.base)
 def test_request_tamper(self):
  self.body=b'{}';self.save()
  with self.assertRaises(ValueError):summary(self.id,self.base)
 def test_flag_not_authority(self):
  self.result['delivery_allowed']=True;self.save()
  with self.assertRaises(ValueError):output_gate(self.id,self.base)
 def test_traversal(self):
  for id in ['../x',self.id+'?a=1','x']:
   with self.assertRaises(ValueError):summary(id,self.base)
 def test_repaired_history_no_authority(self):
  fixture=ROOT/'app/local_integration/evidence/parametric_repair/flow/repair_ui_response.json'
  self.result=json.loads(fixture.read_text());self.result['run_id']=self.id
  self.body=json.dumps(self.result['envelope']['received_input'],separators=(',',':')).encode();self.save()
  r=summary(self.id,self.base);self.assertEqual(r['candidates'][0]['state'],'PHYSICAL_PASS_SEMANTIC_UNKNOWN')
  self.assertFalse(r['delivery_allowed']);self.assertEqual(output_gate(self.id,self.base)[0],403)
 def test_legacy_omitted(self):
  del self.result['candidates'][0]['review_decision'];self.save();r=list_history(self.base);self.assertEqual(r['records'],[]);self.assertEqual(r['omitted_unverifiable_or_legacy'],1)
if __name__=='__main__':unittest.main()
