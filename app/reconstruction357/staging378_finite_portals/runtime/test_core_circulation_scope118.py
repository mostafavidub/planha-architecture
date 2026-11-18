import unittest,json,copy
from pathlib import Path
from core_circulation_scope118 import evaluate,applicability
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads((Path(__file__).parent/'evidence/compact118_reassembled_actual.json').read_text())['model']
 def test_component_pass_not_whole_pass(self):
  r=evaluate(self.m);self.assertEqual(r['status'],'NOT_EVALUATED');self.assertEqual(r['witness']['common_core_subcondition_status'],'PASS_LIMITED');self.assertIn('INTERNAL_CIRCULATION_COMPARATIVE_NECESSITY_NOT_ESTABLISHED',r['witness']['pending']);self.assertFalse(r['witness']['historical_fullspan_core_component']['whole_plan_feasible'])
 def test_applicability_interface(self):self.assertIs(applicability(self.m)['witness']['applies'],True)
 def test_current_body_block(self):
  m=copy.deepcopy(self.m);m['walls']['new_block']=['9.2','11.8','10','12.5'];r=evaluate(m);self.assertNotEqual(r['witness']['common_core_subcondition_status'],'PASS_LIMITED')
 def test_renamed_private_corridor(self):
  m=copy.deepcopy(self.m);m['units'][0]['rooms']['private_access']=m['units'][0]['rooms'].pop('entry_circulation');r=evaluate(m);self.assertTrue(any('UNSUPPORTED_OR_RENAMED'in p for p in r['witness']['pending']))
 def test_unknown_extension_wall(self):
  m=copy.deepcopy(self.m);m['walls']['renamed_ordinary_wall']=['14','8','14.15','9'];r=evaluate(m);self.assertIn('UNCLASSIFIED_ENCLOSING_WALL_OR_CORRIDOR_SOURCE',r['witness']['pending'])
 def test_no_input_inflation(self):
  m=copy.deepcopy(self.m);m['inputs'][0]='44';r=evaluate(m);self.assertEqual(r['status'],'FAIL');self.assertIn('CURRENT_ACTUAL_FRAME_RAW_INPUT_BINDING',r['witness']['errors'])
 def test_strip_not_necessary(self):
  r=evaluate(self.m);strips=r['witness']['common_unprogrammed_components'];self.assertEqual(strips[0]['area_m2'],'36/25');self.assertEqual(strips[0]['classification'],'COMMON_UNPROGRAMMED_NOT_PROVEN_FUNCTIONAL')
if __name__=='__main__':unittest.main()
