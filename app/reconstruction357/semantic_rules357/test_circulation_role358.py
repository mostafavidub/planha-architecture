import unittest,json,copy
from fractions import Fraction as F
from circulation_role358 import evaluate,component_accounting,transverse_source_margin,ROOT
from modules_spatial import rect
class Circulation(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text());cls.review=json.loads((ROOT/'review358_source_validation/result.json').read_text());cls.o=evaluate(cls.record,cls.review)
 def test_empty_target_rejected(self):
  with self.assertRaises(ValueError):component_accounting([rect(['0','0','1','1'])],{},'.7')
 def test_deadend_not_hidden_by_transverse_margin(self):
  d=[rect(['0','0','10','1'])];p={'target':[['.5','.5'],['2','.5']]};margin=transverse_source_margin(d,p,'.7','1');r=component_accounting(d,p,'.7',margin)[0];self.assertGreater(F(r['unsupported_margin_area_m2']),7);self.assertTrue(r['verdict'].startswith('UNKNOWN'))
 def test_actual_entry_component_proof(self):
  for u in self.o['units']:self.assertTrue(all(c['verdict']=='PASS_EXACT_REQUIRED_PATH_USE_COMPONENT'for c in u['entry_circulation_components']))
 def test_real_terminal_extension_not_hardfail(self):
  for u in self.o['units']:
   self.assertEqual(len(u['untargeted_terminal_extensions']),2);self.assertEqual(sum(F(r['area_m2'])for r in u['untargeted_terminal_extensions']),F('11.9'));self.assertTrue(all(r['verdict']=='UNKNOWN_NOT_PROVEN_USELESS'for r in u['untargeted_terminal_extensions']))
 def test_service_not_assumed_zero_or_exclusive(self):
  for u in self.o['units']:
   self.assertEqual(len(u['service_inventory']),2);self.assertTrue(all(F(r['route_only_after_actual_fixture_activity_deduction_m2'])>0 for r in u['service_inventory']));self.assertTrue(all(r['exclusive_service_circulation_status'].startswith('UNKNOWN')for r in u['service_inventory']))
 def test_tampered_target_binding_rejected(self):
  r=copy.deepcopy(self.record);r['candidate']['model']['units'][0]['route_targets']['WC_front']=['0','0']
  with self.assertRaises(ValueError):evaluate(r,self.review)
 def test_no_parent_or_newfresh(self):
  for k in('parent_complete','fresh_execution','admission_allowed'):self.assertFalse(self.o[k])
if __name__=='__main__':unittest.main()
