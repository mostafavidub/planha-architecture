import unittest,copy,sys
from source_guest_route_evaluator import living_destination,route_check,ENGINE
from fractions import Fraction as F
sys.path.insert(0,str(ENGINE))
class GuestSourceHelpers(unittest.TestCase):
 def fixture(self):
  return {'public_program':{'destinations':{'guest_living':{'fixture_id':'sofa1','activity_id':'sofa1_front'}},'capacity':{'living_seats':[{'fixture_id':'sofa1','access_activity_id':'sofa1_front'}]}},'fixtures':{'sofa1':['0','0','2','.9']},'activities':{'sofa1_front':['0','.9','2','1.6']}}
 def test_no_old_route_required(self):
  u=self.fixture();target,_=living_destination(u);self.assertEqual(target,['1','5/4']);self.assertNotIn('scenario_routes',u)
 def test_activity_misbinding(self):
  u=self.fixture();u['public_program']['capacity']['living_seats'][0]['access_activity_id']='other'
  with self.assertRaises(ValueError):living_destination(u)
 def test_nonadjacent(self):
  u=self.fixture();u['activities']['sofa1_front']=['4','4','5','5']
  with self.assertRaises(ValueError):living_destination(u)
 def test_duplicate_source_seat(self):
  u=self.fixture();u['public_program']['capacity']['living_seats']*=2
  with self.assertRaises(ValueError):living_destination(u)
 def test_valid_width_route(self):
  self.assertEqual(route_check([['1','1'],['3','1']],['1','1'],['3','1'],F('.7'),[['0','0','4','2']],[]),1)
 def test_floor_hole(self):
  with self.assertRaises(ValueError):route_check([['1','1'],['3','1']],['1','1'],['3','1'],F('.7'),[['0','0','1.5','2'],['2','0','4','2']],[])
 def test_obstacle_centerline_clear_body_collision(self):
  with self.assertRaises(ValueError):route_check([['1','1'],['3','1']],['1','1'],['3','1'],F('.7'),[['0','0','4','2']],[['1.5','1.1','2','1.3']])
 def test_endpoint_or_body_invalid(self):
  for body,end in ((F(0),['3','1']),(F('.7'),['2','1'])):
   with self.assertRaises(ValueError):route_check([['1','1'],['3','1']],['1','1'],end,body,[['0','0','4','2']],[])
if __name__=='__main__':unittest.main()
