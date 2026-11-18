import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
import engine362_v2 as engine362
class Integrated359(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  p=Path(__file__).resolve().parents[1];cls.a=json.loads((p/'staging362_core_notch/actual362.json').read_text());cls.b=json.loads((p/'review362_source_validation/result.json').read_text());cls.m=cls.a['candidate']['model'];cls.r=cls.b['raw_report']
 def invoke(self,a=None,b=None):return engine362.evaluate(self.m,self.r,registered_artifact={'record':self.a if a is None else a,'result':self.b if b is None else b})
 def test_exact_ten_limited_parents_two_pending(self):
  out=self.invoke();passed={x['rule_id']for x in out['quality']if x['verdict']=='PASS'}
  self.assertEqual(passed,{'GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','ROOM_PROGRAM_CAPACITY','OPENINGS_REAL','KITCHEN_PROXIMITY','SERVICE_COMPACTNESS','BEDROOM_GROUPING','SPACE_ACCOUNTING','CIRCULATION_NECESSITY','PRIVACY_WITHOUT_FAKE_BAFFLE'});self.assertEqual(len(out['quality']),12);self.assertFalse(out['accepted']);self.assertFalse(out['delivery_allowed']);self.assertFalse(out['fresh_executed']);self.assertEqual(sum(x['verdict']=='UNKNOWN'for x in out['quality']),2)
  for x in out['quality']:
   if x['verdict']=='PASS':self.assertTrue(x['scope']);self.assertEqual(x['missing'],[]);self.assertEqual(x['model_hash'],out['model_hash'])
 def test_no_parent_reentry(self):
  fn=engine362.evaluate
  with patch('engine362_v2.evaluate',side_effect=AssertionError('REENTRY')),patch('engine.evaluate',side_effect=AssertionError('LEGACY_REENTRY')):
   out=fn(self.m,self.r,registered_artifact={'record':self.a,'result':self.b});self.assertEqual(next(x for x in out['quality']if x['rule_id']=='ROOM_PROGRAM_CAPACITY')['verdict'],'PASS')
 def test_wrong_actual_result_fails_closed(self):
  b=copy.deepcopy(self.b);b['raw_report']['errors']=['fake'];out=self.invoke(b=b);self.assertTrue(all(x['verdict']=='UNKNOWN'for x in out['quality']))
 def test_raw_only_never_admits(self):
  out=engine362.evaluate(self.m,self.r);self.assertTrue(all(x['verdict']=='UNKNOWN'for x in out['quality']));self.assertFalse(out['registered_artifact_verified'])
if __name__=='__main__':unittest.main()
