import unittest,json,copy
from entry_role_joint367 import *
class Entry(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());c.v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());c.o=evaluate(c.r,c.v)
 def test_actual_nonzero_cost_not_zero_guard(self):
  for u in self.o['units']:self.assertGreater(F(u['service_only_outside_source_approach_m2']),0);self.assertTrue(u['verdict'].startswith('PASS_SCOPED_INTRINSIC'));self.assertTrue(u['necessity_verdict'].startswith('NOT_ASSESSED'))
 def test_gap_cannot_launder(self):
  with self.assertRaises(ValueError):partition([rect(['0','0','3','1'])],[rect(['0','0','1','1'])],[],[])
 def test_shared_route_not_exclusive(self):
  q=[rect(['0','0','1','1'])];x=partition(q,q,q,[]);self.assertEqual(x['current_source_shared_route_area_m2'],'1');self.assertEqual(x['current_source_service_only_route_area_m2'],'0')
 def test_no_necessity_or_admission(self):self.assertFalse(self.o['admission_allowed']);self.assertTrue(self.o['compactness_verdict'].startswith('UNKNOWN'))
 def test_extra_room_or_route_tamper_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['units'][0]['rooms']['entry_circulation'].append(['0','0','2','2'])
  with self.assertRaises(ValueError):evaluate(r,self.v)
 def test_stale_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text()))
if __name__=='__main__':unittest.main()
