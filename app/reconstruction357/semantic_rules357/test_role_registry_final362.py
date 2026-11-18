import unittest,json,copy
from role_registry_final362 import evaluate,ROOT
from common import digest
class FinalRole362(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging362_core_notch/actual362.json').read_text());cls.v=json.loads((ROOT/'review362_source_validation/result.json').read_text());cls.o=evaluate(cls.r,cls.v)
 def test_current_binding(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(self.o['review_digest'],digest(self.v))
 def test_no_pending_role_parents(self):
  for k in ('Q11_WHOLE_ROLE','Q05_PRIVACY','Q12_PER_UNIT'):self.assertEqual(self.o['nodes'][k]['blocking_dependencies'],[])
 def test_hall_exact_eight_closed(self):
  e=self.o['nodes']['WALL_PURPOSE']['evidence'];self.assertEqual(len(e['closed_hall_dependency_rows']),8);self.assertEqual(e['immutable_constructive_wall_evidence']['counts']['UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY'],8)
 def test_q12_internal_only(self):
  for u in self.o['nodes']['Q12_PER_UNIT']['evidence']:self.assertEqual(u['exact_pending'],[]);self.assertTrue(u['not_a_parent_acceptance_filter'])
 def test_q10_not_inferred(self):self.assertEqual(self.o['parent_evidence']['COMMON_CORE_COMPACTNESS']['verdict'],'UNKNOWN')
 def test_outputset_not_waived(self):
  self.assertEqual(self.o['parent_evidence']['DISTINCTNESS_AND_FAIRNESS']['verdict'],'UNKNOWN');self.assertEqual(self.o['selected_output_set_fulfillment'],'NOT_PROVEN');self.assertFalse(self.o['admission_allowed'])
 def test_explicit_parent_bindings(self):
  for k in ('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','PRIVACY_WITHOUT_FAKE_BAFFLE'):
   e=self.o['parent_evidence'][k];self.assertEqual(e['fresh_result_digest'],digest(self.v));self.assertTrue(all(e['explicit_complete_predicate'].values()));self.assertEqual(e['missing'],[])
 def test_stale_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review359_source_validation/result.json').read_text()))
 def test_changed_model_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['common_routes']={}
  with self.assertRaises(ValueError):evaluate(r,self.v)
if __name__=='__main__':unittest.main()
