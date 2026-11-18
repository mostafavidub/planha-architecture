import unittest,copy
from private_l3_primitive131 import build
from private_domain121 import examine
from geometry114 import Q,hit,cells
from fractions import Fraction as F
class L3(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.model=build()
 def test_real_three_room_private_domain(self):
  m=self.model;r=examine(m);self.assertEqual(r['errors'],[]);self.assertEqual(r['pending'],[])
  self.assertEqual(len(m['module_placements']),3);self.assertEqual(len(m['operations']['doors']),3)
  self.assertEqual(len(m['operations']['closets']),3)
  self.assertEqual(F(m['private_primitive_scope']['actual_room_floor_area_m2']),F('68.67'))
 def test_missing_quadrant_not_claimed_floor(self):
  q=Q(['6.9','3.9','12.35','9.3']);floor=self.model['units'][0]['ownership']
  self.assertFalse(any(hit(q,Q(r))for r in floor))
 def test_shared_walls_have_alias_not_duplicate_solid(self):
  m=self.model;solids=list(m['physical_wall_network']['solids'].values())
  self.assertTrue(all(not hit(Q(a),Q(b))for i,a in enumerate(solids)for b in solids[i+1:]))
  self.assertEqual(cells(solids,[]),cells(list(m['walls'].values()),[]))
 def test_missing_functional_boundary_rejected(self):
  m=copy.deepcopy(self.model);del m['walls']['A.private_l3.right_exposed'];r=examine(m)
  self.assertTrue(r['pending']or r['errors'])
 def test_intruding_obstacle_rejected(self):
  m=copy.deepcopy(self.model);m['walls']['test.blocker']=['5.75','2','6.75','2.1'];r=examine(m)
  self.assertTrue(r['errors'])
 def test_foreign_route_through_private_rejected(self):
  m=copy.deepcopy(self.model);m['units'][0]['routes']['kitchen_guest']=[['6.25','.15'],['6.25','5']];r=examine(m)
  self.assertIn('A:NONPRIVATE_FUNCTION_THROUGH_PRIVATE_DOMAIN',r['errors'])
 def test_port_and_interface_binding(self):
  for target in('port','interface'):
   m=copy.deepcopy(self.model)
   if target=='port':m['module_ports'][0]['center']=['6.15','1']
   else:m['private_domains'][0]['paths']['A.bed1'][0]=['6.25','.2']
   self.assertTrue(examine(m)['errors'])
if __name__=='__main__':unittest.main()
