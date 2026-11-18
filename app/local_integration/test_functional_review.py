import unittest,json,copy
from pathlib import Path
from functional_review import assess,ROOT
from review_cycle import digest,decide
class Functional(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  r=json.loads((ROOT/'app/local_integration/evidence/requests/ff64fcb1-0e5f-499c-8f69-079f792473a6/result.json').read_text());cls.r=r;cls.c=r['candidates'][0]
 def evaluate(self,model):
  review=copy.deepcopy(self.c['physical_review']);review['model_hash']=digest(model);return assess(model,review,self.r['engine_source_revision'])
 def test_source_profile_places_not_full_quality(self):
  a=self.evaluate(self.c['model']);self.assertEqual(a['internal_capacity']['evidence']['status'],'PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY');self.assertEqual(len(a['internal_capacity']['evidence']['units']),2);self.assertTrue(all(r['actual_places']=={'sleeping_places':6,'dining_seats':6,'living_seats':6}for r in a['internal_capacity']['evidence']['units']));self.assertFalse(a['display_allowed']);self.assertEqual(a['state'],'UNKNOWN_REQUIRED_FUNCTIONAL_PROOF')
 def test_inflated_places_fail(self):
  m=copy.deepcopy(self.c['model']);m['units'][0]['public_program']['capacity']['living_seats'][0]['places']=3;self.assertEqual(self.evaluate(m)['state'],'REJECTED_FUNCTIONAL')
 def test_reused_seat_fails(self):
  m=copy.deepcopy(self.c['model']);seats=m['units'][0]['public_program']['capacity']['living_seats'];seats[1]=copy.deepcopy(seats[0]);self.assertEqual(self.evaluate(m)['state'],'REJECTED_FUNCTIONAL')
 def test_wrong_model_binding(self):
  with self.assertRaises(ValueError):assess(self.c['model'],{'model_hash':'wrong'},self.r['engine_source_revision'])
 def test_decision_binds_report(self):
  c=copy.deepcopy(self.c);c['functional_review']=self.evaluate(c['model']);d=decide(c,self.r['envelope']['canonical_request_digest'],self.r['engine_source_revision']);self.assertEqual(d['functional_review_digest'],digest(c['functional_review']));self.assertFalse(d['design_display_allowed'])
 def test_attempted_promotion_rejected(self):
  c=copy.deepcopy(self.c);c['functional_review']=self.evaluate(c['model']);c['functional_review']['display_allowed']=True
  with self.assertRaises(ValueError):decide(c,self.r['envelope']['canonical_request_digest'],self.r['engine_source_revision'])
if __name__=='__main__':unittest.main()
