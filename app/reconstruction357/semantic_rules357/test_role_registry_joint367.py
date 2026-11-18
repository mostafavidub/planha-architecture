import unittest,json,copy
from role_registry_joint367 import evaluate,ROOT,ordered_dag,DAG
from common import digest
class Roles(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());c.v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());c.o=evaluate(c.r,c.v)
 def test_current_binding(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(self.o['source_profile'],'SOURCE_JOINT367')
 def test_public_own_source_no_gap(self):self.assertEqual([u['unresolved_area_m2']for u in self.o['nodes']['PUBLIC_SUPPORT']['evidence']['rows']],['0','0'])
 def test_private_common_intrinsic(self):
  for k in ('PRIVATE_CIRCULATION','COMMON_ROLE','ENTRY_CIRCULATION'):self.assertTrue(self.o['nodes'][k]['status'].startswith('PASS_SCOPED'))
 def test_no_final_service_cycle(self):
  self.assertEqual(DAG['SERVICE_CIRCULATION'],['SOURCE_ROOM_USE']);self.assertIn('SOURCE_GATE',DAG['SOURCE_ROOM_USE']);self.assertIn('SERVICE_CIRCULATION',DAG['Q04_COMPARISON']);self.assertEqual(len(ordered_dag()),len(DAG));self.assertIn('No global exclusive-function or compactness',self.o['nodes']['SERVICE_CIRCULATION']['scope'])
 def test_hall_and_necessity_pending(self):
  for k in ('WALL_PURPOSE','Q04_COMPARISON','Q11_WHOLE_ROLE','Q05_PRIVACY'):self.assertTrue(self.o['nodes'][k]['status'].startswith('UNKNOWN'))
  for u in self.o['nodes']['Q12_PER_UNIT']['evidence']:self.assertEqual(set(u['exact_pending']),{'Q04_CLOSED_FINITE_ELIGIBLE_COMPARISON','HALL_WALL_PURPOSE_Q04_DEPENDENCY'})
 def test_not_selected_set_qualified(self):
  x=self.o['nodes']['Q14_SELECTION_SET'];self.assertEqual(x['evidence']['internal_pair_test']['status'],'NOT_APPLICABLE_INTERNAL_SINGLETON_REVIEW');self.assertEqual(x['evidence']['selected_output_set_fulfillment'],'NOT_PROVEN');self.assertFalse(self.o['admission_allowed'])
 def test_old_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review365_service_source_validation/result.json').read_text()))
 def test_changed_model_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['units'][0]['ownership']=[]
  with self.assertRaises(ValueError):evaluate(r,self.v)
if __name__=='__main__':unittest.main()
