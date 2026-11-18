import unittest
from fractions import Fraction as F
from clearance_kernel import maximum_width,feasible
class Tests(unittest.TestCase):
 def test_narrow_interior_not_wide_portal(self):
  r=maximum_width([[1,5],[9,5]],[0,0,10,10],[{'id':'local','rect':[4,6,6,8]}]);self.assertEqual(r['max_axis_aligned_square_width_m'],'2')
 def test_corner_limits(self):
  r=maximum_width([[2,2],[5,2],[5,5]],[0,0,10,10],[{'id':'corner','rect':['5.5','2.5',7,4]}]);self.assertEqual(r['max_axis_aligned_square_width_m'],'1')
 def test_hole_limits(self):
  r=maximum_width([[2,4],[8,4]],[0,0,10,10],[{'id':'domain_hole','rect':[4,5,6,7]}]);self.assertEqual(r['max_axis_aligned_square_width_m'],'2')
 def test_touch_and_above(self):
  args=([[2,5],[8,5]],[0,0,10,10],[{'id':'wall','rect':[3,6,7,7]}]);self.assertTrue(feasible(*args,2));self.assertFalse(feasible(*args,F(2001,1000)))
 def test_diagonal_rejected(self):
  with self.assertRaises(ValueError):maximum_width([[1,1],[2,2]],[0,0,3,3],[])
 def test_collision_rejected(self):
  with self.assertRaises(ValueError):maximum_width([[1,1],[5,1]],[0,0,6,6],[{'id':'wall','rect':[3,0,4,2]}])
if __name__=='__main__':unittest.main()
