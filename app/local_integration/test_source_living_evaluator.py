import unittest,sys
from source_living_evaluator import union_area,box_of,ENGINE
from living_connectivity_diagnostic import direction_changes
from fixed_route_clearance_diagnostic import fixed_polyline_capacity
sys.path.insert(0,str(ENGINE))
class LivingHelpers(unittest.TestCase):
 def test_overlap_union_not_bbox(self):
  self.assertEqual(union_area([['0','0','2','1'],['1','0','3','1']]),3)
 def test_disconnected_area_not_connectivity(self):
  q=[['0','0','1','1'],['2','0','3','1']]
  self.assertEqual(union_area(q),2);self.assertEqual(box_of(q),['0','0','3','1'])
 def test_zero_and_collinear_directions(self):
  self.assertEqual(direction_changes([['0','0'],['0','0'],['1','0'],['2','0'],['2','1']]),1)
 def test_reversal_explicit(self):
  self.assertEqual(direction_changes([['0','0'],['1','0'],['0','0']]),1)
 def test_bad_diagonal(self):
  with self.assertRaises(ValueError):direction_changes([['0','0'],['1','1']])
 def test_fixed_width_not_door_claim(self):
  r=fixed_polyline_capacity([['1','1'],['3','1']],['0','0','4','2'],[])
  self.assertEqual(r['maximum_uniform_axis_aligned_square_width_m'],'2')
  self.assertIn('Not corridor/door width',r['scope'])
 def test_zero_route_rejected(self):
  with self.assertRaises(ValueError):fixed_polyline_capacity([['1','1'],['1','1']],['0','0','4','2'],[])
if __name__=='__main__':unittest.main()
