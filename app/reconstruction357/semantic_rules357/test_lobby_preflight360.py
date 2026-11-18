import unittest,json,copy
from pathlib import Path
from lobby_preflight360 import evaluate,ROOT
from common import digest
class Lobby360(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging360_core_notch/actual360.json').read_text());cls.o=evaluate(cls.r)
 def test_actual_junction_geometry(self):
  self.assertEqual(self.o['lobby']['geometry_unsupported_area_m2'],'0');self.assertEqual(len(self.o['lobby']['source_portals']),4)
 def test_not_functional_pass(self):
  self.assertFalse(self.o['source_use_verified']);self.assertFalse(self.o['admission_allowed']);self.assertTrue(self.o['whole_role_status'].startswith('UNKNOWN'))
 def test_transfer_no_label_acceptance(self):
  self.assertEqual(self.o['transferred_floor']['area_m2'],'627/400');self.assertTrue(self.o['transferred_floor']['functional_role'].startswith('UNKNOWN'))
 def test_missing_portal(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['openings']=[o for o in r['candidate']['model']['openings']if o['id']!='lift.entry'];r['candidate']['model_digest']=digest(r['candidate']['model'])
  with self.assertRaisesRegex(ValueError,'FOUR_REQUIRED'):evaluate(r)
 def test_stale_geometry(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['common_spaces']['lobby'][0][0]='0'
  with self.assertRaisesRegex(ValueError,'MODEL_DIGEST'):evaluate(r)
 def test_physical_wall_union(self):self.assertEqual(self.o['physical_wall_union_difference_m2'],{'missing':'0','extra':'0'})
if __name__=='__main__':unittest.main()
