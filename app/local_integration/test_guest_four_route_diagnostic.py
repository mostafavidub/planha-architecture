import unittest
from guest_four_route_diagnostic import same_point,center
class PointBindingTests(unittest.TestCase):
 def test_equivalent_exact_notations(self):
  self.assertTrue(same_point(['12.5','0.70'],['25/2','7/10']))
 def test_nearby_not_equal(self):
  self.assertFalse(same_point(['12.500000000000000001','0.7'],['25/2','7/10']))
 def test_float_rejected(self):
  with self.assertRaisesRegex(ValueError,'EXACT_POINT_REQUIRED'):same_point([12.5,'0.7'],['25/2','7/10'])
 def test_actual_activity_center(self):
  self.assertTrue(same_point(center(['1','2','2','3']),['1.5','2.5']))
if __name__=='__main__':unittest.main()
