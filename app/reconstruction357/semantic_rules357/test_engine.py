import copy,json,unittest
from pathlib import Path
import engine
from common import digest
class Integrated(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  x=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text());cls.m=x['selected'][0]['model'];cls.r=x['central_fresh_reviews'][0]['central_fresh_review']['raw_fresh_report']
 def test_complete_dispatch_not_complete_acceptance(self):
  before=digest([self.m,self.r]);r=engine.evaluate(self.m,self.r)
  self.assertEqual({x['rule_id']for x in r['quality']},set(engine.RULE_IDS));self.assertEqual(len(r['quality']),12)
  self.assertTrue(all(x['verdict']=='UNKNOWN'for x in r['quality']));self.assertFalse(r['accepted']);self.assertFalse(r['delivery_allowed']);self.assertFalse(r['fresh_executed']);self.assertEqual(before,digest([self.m,self.r]))
 def test_stale_fails_closed_all(self):
  r=copy.deepcopy(self.r);r['model_hash']='other';out=engine.evaluate(self.m,r)
  self.assertTrue(all(x['codes'][0]=='BINDING_OR_DISPATCH_BLOCKED'for x in out['quality']))
 def test_registry_tamper_detected(self):
  from unittest.mock import patch
  original=Path.read_bytes
  def altered(p):return b'{}'if p.name=='method_registry.json'else original(p)
  with patch.object(Path,'read_bytes',altered):
   with self.assertRaisesRegex(ValueError,'REGISTRY_SOURCE_CHANGED'):engine.evaluate(self.m,self.r)
class PostFresh(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  x=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text());f=x['central_fresh_reviews'][0];cls.m=x['selected'][0]['model'];cls.r=f['central_fresh_review']['raw_fresh_report'];cls.p={'envelope':f['central_envelope'],'result':f['central_fresh_review'],'groups':f['source_groups285'],'seconds':10}
 def test_scoped_closures_do_not_promote_parent(self):
  r=engine.evaluate(self.m,self.r,post_fresh=self.p)
  self.assertEqual(r['source_closures']['guest_closure']['verdict'],'PASS_SCOPED_FOUR_SOURCE_GUEST_RELATIONS')
  self.assertTrue(all(x['verdict']=='UNKNOWN'for x in r['quality']))
 def test_wrong_packet(self):
  p=copy.deepcopy(self.p);p['envelope']['packet']['world_model']['inputs'][0]='27'
  r=engine.evaluate(self.m,self.r,post_fresh=p)
  self.assertTrue(all(x['codes']==['BINDING_OR_DISPATCH_BLOCKED','POST_FRESH_MODEL_RAW_BINDING']for x in r['quality']))
 def test_budget_bool_rejected(self):
  p=dict(self.p);p['seconds']=True;r=engine.evaluate(self.m,self.r,post_fresh=p)
  self.assertTrue(all('POST_FRESH_BUDGET'in x['codes']for x in r['quality']))
if __name__=='__main__':unittest.main()
