import unittest,json,copy
from service_public_role_join365 import evaluate,classify_cells,ROOT
from modules_spatial import rect
class Join(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());c.v=json.loads((ROOT/'review365_service_source_validation/result.json').read_text());c.o=evaluate(c.r,c.v)
 def test_actual_not_in_living_role(self):
  for u in self.o['units']:
   self.assertEqual(u['route_only_residual_area_m2'],'1911/200');self.assertEqual(u['whole_actual_living_region_intersection_m2'],'0');self.assertEqual(u['remaining_without_independent_nonservice_use_m2'],'1911/200')
 def test_body_connection_not_multifunction(self):
  q=[rect(['0','0','2','1'])];x=classify_cells(q,[],q,q,[],[]);self.assertEqual(x['body_connected_support_intersection_m2'],'2');self.assertTrue(x['verdict'].startswith('UNKNOWN'));self.assertFalse(x['exclusive_function_proven'])
 def test_living_label_not_function(self):
  q=[rect(['0','0','2','1'])];x=classify_cells(q,q,q,q,[],[]);self.assertEqual(x['remaining_without_independent_nonservice_use_m2'],'2');self.assertTrue(x['verdict'].startswith('UNKNOWN'))
 def test_outside_entry_rejected(self):
  with self.assertRaises(ValueError):classify_cells([rect(['0','0','2','1'])],[],[],[],[],[])
 def test_stale_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text()))
 def test_module_tamper_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['module_placements'][0]['module_hash']='bad'
  with self.assertRaises(ValueError):evaluate(r,self.v)
if __name__=='__main__':unittest.main()
