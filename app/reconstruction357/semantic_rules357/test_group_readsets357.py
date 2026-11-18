import json,copy,unittest
from pathlib import Path
from group_readsets357 import build,digest
ROOT=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging357_comparative/attached_service_final357.json').read_text());cls.f=json.loads((ROOT/'review357_source_validation/result.json').read_text())
 def test_actual(self):
  before=digest([self.r,self.f]);x=build(self.r,self.f);self.assertEqual(len(x['groups']['rows']),9);self.assertTrue(all(r['verdict']=='SCOPED_PASS'for r in x['groups']['rows']));self.assertEqual(x['envelope']['raw'],self.r['trace']['raw']);self.assertFalse(x['live_authority']);self.assertFalse(x['new_fresh_execution']);self.assertEqual(x['envelope']['schema'],'REGISTERED_SOURCE357_VIEW');self.assertEqual(digest(x['result']['raw_fresh_report']),digest(self.f['raw_report']));self.assertEqual(digest([self.r,self.f]),before)
 def test_tampered_raw(self):
  f=copy.deepcopy(self.f);f['raw_report']['errors']=['new']
  with self.assertRaises(ValueError):build(self.r,f)
 def test_tampered_outertrace(self):
  r=copy.deepcopy(self.r);r['trace']['accepted']=True
  with self.assertRaises(ValueError):build(r,self.f)
 def test_fake_methods(self):
  f=copy.deepcopy(self.f);f['expected_method_registry']['methods']={}
  with self.assertRaises(ValueError):build(self.r,f)
 def test_unregistered_profile(self):
  with self.assertRaises(ValueError):build(self.r,self.f,source_profile='UNKNOWN')
 def test_identity_profile(self):
  f=json.loads((ROOT/'review357_source_identity/result.json').read_text());x=build(self.r,f,source_profile='SOURCE_IDENTITY357');self.assertEqual(x['groups']['review_verdict'],'SCOPED_PASS');self.assertFalse(x['new_fresh_execution']);self.assertEqual(digest(x['result']['raw_fresh_report']),digest(f['raw_report']))
 def test_profile_not_interchangeable(self):
  f=json.loads((ROOT/'review357_source_identity/result.json').read_text())
  with self.assertRaises(ValueError):build(self.r,f,source_profile='SOURCE357')
 def test_zero_budget(self):
  with self.assertRaises(ValueError):build(self.r,self.f,seconds=0)
if __name__=='__main__':unittest.main()
