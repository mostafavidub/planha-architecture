import unittest,json,copy
from fractions import Fraction as F
from service_role_inventory_joint367 import evaluate,partition,nonservice_inventory,linear,ROOT
from common import digest
class ServiceInventory(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());cls.v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());cls.o=evaluate(cls.r,cls.v)
 def test_actual_bound(self):
  self.assertEqual(self.o['verdict'],'PASS_SCOPED_CURRENT_SOURCE_ROLE_PARTITION');self.assertEqual(self.o['model_digest'],digest(self.r['candidate']['model']));self.assertEqual(self.o['remaining'],[])
 def test_current_not_global(self):self.assertIsNone(self.o['global_exclusive_function_m2']);self.assertFalse(self.o['accepted'])
 def test_includes_source_approach_not_old_outside_cost(self):
  for u in self.o['units']:self.assertGreater(F(u['exclusive_current_profile_m2']),F(u['route_only_outside_approach_m2']));self.assertEqual(u['unclassified_m2'],'0')
 def test_whole_roles_and_continuous_inventory_present(self):
  for u in self.o['units']:
   keys=u['nonservice_inventory'];self.assertIn('whole_room:living',keys);self.assertIn('whole_room:private_circulation',keys);self.assertIn('kitchen_operation',keys);self.assertTrue(any(k.startswith('closet_operation:')for k in keys));self.assertTrue(any(k.startswith('living_occupied:')for k in keys));self.assertTrue(any(k.startswith('dining_operation:')for k in keys))
 def test_unknown_inventory_stops(self):
  with self.assertRaises(ValueError):partition([(0,0,2,2)],[(0,0,2,2)],[],False)
 def test_whole_room_role_makes_shared_without_footprint(self):
  o=partition([(0,0,2,2)],[(0,0,2,2)],[(0,0,1,2)],True);self.assertEqual(o['exclusive_current_profile_m2'],'2');self.assertEqual(o['shared_current_profile_m2'],'2')
 def test_unclassified_cells_remain(self):self.assertEqual(partition([(0,0,2,2)],[(0,0,1,2)],[],True)['unclassified_m2'],'2')
 def test_continuous_middle_crossing(self):
  q=linear([-2,0,-1,1],[2,0,3,1]);o=partition([(0,0,1,1)],[(0,0,1,1)],[q],True);self.assertEqual(o['exclusive_current_profile_m2'],'0')
 def test_unsupported_motion_stops(self):
  with self.assertRaises(ValueError):linear([0,0,1,1],[1,1,2,2])
 def test_unknown_operation_stops(self):
  m=copy.deepcopy(self.r['candidate']['model']);m['operations']['other']=[]
  with self.assertRaises(ValueError):nonservice_inventory(m,m['units'][0],set())
 def test_stale_review_unknown(self):
  v=copy.deepcopy(self.v);v['raw_report']['tampered']=True;self.assertEqual(evaluate(self.r,v)['verdict'],'UNKNOWN')
 def test_missing_current_operations_unknown(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['operations'].pop('closets');self.assertEqual(evaluate(r,self.v)['verdict'],'UNKNOWN')
if __name__=='__main__':unittest.main()
