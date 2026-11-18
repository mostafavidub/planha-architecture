import unittest
from fractions import Fraction as F
from supporting_floor import analyze
class Support(unittest.TestCase):
 def test_room(self):self.assertTrue(analyze([[0,0,4,4]],[],[[1,1],[3,3]],'.7')['verdict'].startswith('PASS'))
 def test_narrow_neck(self):self.assertEqual(analyze([[0,0,2,2],[2,'.8',3,'1.2'],[3,0,5,2]],[],[[1,1],[4,1]],'.7')['verdict'],'FAIL_SOURCE_ACTIVITIES_DISCONNECTED')
 def test_exact_body_neck(self):self.assertTrue(analyze([[0,0,2,2],[2,'.65',3,'1.35'],[3,0,5,2]],[],[[1,1],[4,1]],'.7')['verdict'].startswith('PASS'))
 def test_blind_appendage(self):
  r=analyze([[0,0,2,2],[2,'.8',5,'1.2']],[],[[1,1]],'.7');self.assertTrue(all(F(q[2])<5 for q in r['support_regions']))
 def test_small(self):self.assertEqual(analyze([[0,0,'.5',3]],[],[['.25',1]],'.7')['verdict'],'FAIL_BODY_CANNOT_FIT_DOMAIN')
 def test_missing_anchor(self):
  with self.assertRaises(ValueError):analyze([[0,0,4,4]],[],[],'.7')
 def test_obstacle_at_anchor(self):self.assertEqual(analyze([[0,0,4,4]],[[0,0,2,2]],[[1,1]],'.7')['verdict'],'FAIL_SOURCE_ACTIVITY_ANCHOR_NOT_BODY_USABLE')
 def test_no_parent_pass(self):self.assertFalse(analyze([[0,0,4,4]],[],[[1,1]],'.7')['parent_complete'])
if __name__=='__main__':unittest.main()
