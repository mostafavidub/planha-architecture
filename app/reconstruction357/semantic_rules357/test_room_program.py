import unittest,json,copy
from pathlib import Path
from closure_room_program import evaluate,bundle_inventory,digest
from intrinsic_access import bound_rows
BASE=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.x=json.loads((BASE/'actual_run/actual_response.json').read_text());cls.m=cls.x['selected'][0]['model'];cls.raw=cls.x['central_fresh_reviews'][0]['central_fresh_review']['raw_fresh_report'];cls.rs=bound_rows(cls.m,cls.raw,'BASE351')
 def synthetic_rows(self,m):
  # Isolated helper test seam, never passed to the profile-bound public evaluator.
  r=copy.deepcopy(self.rs);r['fixture_inventory_use']['evidence']['witness']['capacity']['evidence']['model_hash']=digest(m);return r
 def test_baseline(self):
  r=evaluate(self.x['selected'][0],self.x['central_fresh_reviews'][0]);self.assertTrue(r['proofscopecomplete']);self.assertFalse(r['parent_complete'])
 def test_identity_profile(self):
  c=json.loads((BASE/'staging357_comparative/attached_service_final357.json').read_text());r=json.loads((BASE/'review357_source_identity/result.json').read_text());v=evaluate(c,r,'SOURCE_IDENTITY357');self.assertTrue(v['proofscopecomplete']);self.assertFalse(v['fresh_executed'])
 def test_capacity_without_role(self):
  m=copy.deepcopy(self.m);m['program']['sleep_roles']=['double']*3;self.assertRaises(ValueError,bundle_inventory,m,self.synthetic_rows(m))
 def test_missing_closet_operation(self):
  m=copy.deepcopy(self.m);m['operations']['closets'].pop();self.assertRaises(ValueError,bundle_inventory,m,self.synthetic_rows(m))
 def test_unmapped_extra_bed_fixture(self):
  m=copy.deepcopy(self.m);m['units'][0]['fixtures']['bed1.fake']=['1','1','2','2'];self.assertRaises(ValueError,bundle_inventory,m,self.synthetic_rows(m))
 def test_source_scaled_fixture(self):
  m=copy.deepcopy(self.m);m['units'][0]['fixtures']['bed1.bed'][0]='0';self.assertRaises(ValueError,bundle_inventory,m,self.synthetic_rows(m))
 def test_modified_receipt_blocked(self):
  r=copy.deepcopy(self.x['central_fresh_reviews'][0]);r['made_up']=True;self.assertFalse(evaluate(self.x['selected'][0],r)['proofscopecomplete'])
if __name__=='__main__':unittest.main()
