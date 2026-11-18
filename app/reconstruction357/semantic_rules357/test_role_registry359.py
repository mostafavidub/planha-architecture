import unittest,json,copy
from role_registry359 import evaluate,ordered_dag,DAG,room_inventory,ROOT
import common
class Registry(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text());cls.review=json.loads((ROOT/'review358_source_validation/result.json').read_text());cls.o=evaluate(cls.record,cls.review)
  from pathlib import Path
  Path(__file__).with_name('role_registry_on358.json').write_text(json.dumps(cls.o,indent=2))
 def test_acyclic_no_self_verdict_filter(self):
  o=ordered_dag();self.assertEqual(set(o),set(DAG));self.assertNotIn('Q12_PER_UNIT',DAG['Q12_PER_UNIT']);self.assertNotIn('Q11_WHOLE_ROLE',DAG['Q04_COMPARISON'])
 def test_cycle_rejected(self):
  with self.assertRaises(ValueError):ordered_dag({'A':['B'],'B':['A']})
 def test_new359_not_old_evidence(self):
  with self.assertRaises(ValueError):evaluate(self.record,self.review,source_profile='SOURCE359')
 def test_whole_room_source_roles_not_footprint_tiling(self):self.assertEqual(len(self.o['nodes']['SOURCE_ROOM_USE']['evidence']),12)
 def test_missing_comparison_and_lobby_propagate(self):
  q=self.o['nodes']['Q11_WHOLE_ROLE'];self.assertIn('Q04_COMPARISON',q['blocking_dependencies']);self.assertIn('COMMON_ROLE',q['blocking_dependencies']);self.assertFalse(self.o['whole_parent_complete'])
 def test_each_unit_pending_and_missing_set(self):
  n=self.o['nodes'];self.assertEqual(len(n['Q12_PER_UNIT']['evidence']),2);self.assertTrue(all(r['exact_pending']for r in n['Q12_PER_UNIT']['evidence']));self.assertEqual(n['Q14_SELECTION_SET']['status'],'UNKNOWN_SELECTION_SET_NOT_SUPPLIED')
 def test_stale_record_rejected(self):
  r=copy.deepcopy(self.record);r['candidate']['model']['units'][0]['rooms']['bed1'][0][0]='0'
  with self.assertRaises(ValueError):evaluate(r,self.review)
if __name__=='__main__':unittest.main()
