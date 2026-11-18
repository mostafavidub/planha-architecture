import unittest,json,copy
from spatial_preflight367 import *
class Preflight(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());c.o=evaluate(c.r)
 def test_own_geometry_not_role(self):
  self.assertFalse(self.o['parent_complete']);self.assertFalse(self.o['fresh_execution']);self.assertFalse(self.o['admission_allowed']);self.assertEqual(self.o['common_lobby_area_m2'],'583/80')
 def test_protected_assets(self):
  for u in self.o['units']:self.assertTrue(u['protected_program_assets_equal']);self.assertTrue(all(u['fixed_room_geometry_equal'].values()));self.assertEqual(u['private_floor_m2'],'117/10')
 def test_stale_model_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['inputs'][0]='25'
  with self.assertRaises(ValueError):evaluate(r)
 def test_wrong_source_schema(self):
  r=copy.deepcopy(self.r);r['trace']['schema']='SOURCE_SERVICE_ANCHOR365_TRACE_V1'
  with self.assertRaises(ValueError):evaluate(r)
if __name__=='__main__':unittest.main()
