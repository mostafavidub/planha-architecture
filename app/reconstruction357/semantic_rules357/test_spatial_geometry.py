import unittest
from fractions import Fraction as F
from modules_spatial import *
class Spatial(unittest.TestCase):
 def test_union_not_sum(self):self.assertEqual(union_area([rect([0,0,2,2]),rect([1,0,3,2])]),6)
 def test_touch(self):self.assertIsNone(intersection(rect([0,0,1,1]),rect([1,0,2,1])))
 def test_subtraction(self):self.assertEqual(union_area(difference([rect([0,0,10,10])],[rect([0,0,1,1])])),99)
 def test_subtract_duplicate(self):self.assertEqual(union_area(difference([rect([0,0,10,10])],[rect([0,0,1,1])]*2)),99)
 def test_float_reject(self):
  with self.assertRaises(ValueError):rect([0.,0,1,1])
 def test_diagonal_reject(self):
  with self.assertRaises(ValueError):source_sweeps([[0,0],[1,1]],'.7')
 def test_overlap(self):
  m={'units':[{'id':'A','ownership':[[0,0,2,2]]},{'id':'B','ownership':[[1,0,3,2]]}]};self.assertEqual(ownership_overlap(m)[0]['intersection_area_m2'],'2')
 def test_no_source_no_pass(self):self.assertTrue(all(v['verdict']=='UNKNOWN'for v in evaluate({'units':[]},{}).values()))
if __name__=='__main__':unittest.main()
