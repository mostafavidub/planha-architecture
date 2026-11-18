import unittest,json,copy
from balanced_access_joint367 import evaluate,ROOT
from common import digest
class Balance365(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());cls.v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());cls.o=evaluate(cls.r,cls.v)
 def test_current_binding(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(self.o['fresh_result_digest'],digest(self.v))
 def test_exact_equality_no_tolerance(self):
  self.assertEqual([c['length_A_m']for c in self.o['comparisons']],['19/5','19/5']);self.assertTrue(all(c['equal_fixed_source_metrics']for c in self.o['comparisons']));self.assertEqual([c['square_capacity_A_m']for c in self.o['comparisons']],['9/10','11/10'])
 def test_old_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review362_source_validation/result.json').read_text()))
 def test_changed_path_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['common_routes']['lift_A'][0][1]='14.4'
  with self.assertRaises(ValueError):evaluate(r,self.v)
 def test_scope_preserved(self):
  self.assertFalse(self.o['admission_allowed']);self.assertTrue(any('Other moving operation states' in s for s in self.o['source_assumptions_retained']))
if __name__=='__main__':unittest.main()
