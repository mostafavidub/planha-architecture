import unittest,json,copy
from role_registry_final_joint367 import evaluate,ROOT
from common import digest
class FinalRoleJoint367(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());cls.v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());cls.o=evaluate(cls.r,cls.v)
 def test_current_binding(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(self.o['review_digest'],digest(self.v))
 def test_no_pending_role_parents(self):
  for k in ('Q11_WHOLE_ROLE','Q05_PRIVACY'):self.assertEqual(self.o['nodes'][k]['blocking_dependencies'],[])
 def test_hall_exact_eight_closed(self):
  e=self.o['nodes']['WALL_PURPOSE']['evidence'];self.assertEqual(len(e['closed_hall_dependency_rows']),8);self.assertEqual(e['immutable_constructive_wall_evidence']['counts']['UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY'],8)
 def test_q12_internal_only(self):
  for u in self.o['nodes']['Q12_PER_UNIT']['evidence']:self.assertEqual(u['exact_pending'],[]);self.assertTrue(u['not_a_parent_acceptance_filter'])
 def test_q10_current_evidence_closed(self):self.assertEqual(self.o['parent_evidence']['COMMON_CORE_COMPACTNESS']['verdict'],'PASS_SCOPED_INTERNAL_CURRENT_SOURCE')
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
 def test_balance_exact_metrics_not_threshold(self):
  q=self.o['nodes']['Q12_PER_UNIT'];self.assertTrue(q['status'].startswith('PASS_'));self.assertTrue(all(c['equal_fixed_source_metrics'] for c in q['balanced_common_access']['comparisons']))
 def test_explicit_fairness_missing_in_parent(self):
  self.assertEqual(self.o['parent_evidence']['DISTINCTNESS_AND_FAIRNESS']['missing'],['ACTUAL_REQUESTED_SELECTION_SET_NOT_SUPPLIED'])
 def test_service_intrinsic_not_final_cycle(self):
  self.assertEqual(self.o['nodes']['SERVICE_CIRCULATION']['depends_on'],['SOURCE_ROOM_USE'])
  self.assertEqual(self.o['service_compactness_evidence']['verdict'],'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS')
 def test_q12_independent_binding_and_predicate(self):
  q=self.o['internal_per_unit_review'];self.assertEqual(q['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(q['record_digest'],digest(self.r));self.assertEqual(q['fresh_result_digest'],digest(self.v));self.assertTrue(all(q['explicit_complete_predicate'].values()));self.assertEqual(q['missing'],[])
 def test_no_foreign_reservation_transferred(self):self.assertNotIn('nonusable_operational_reservation',self.o)
 def test_current_wall_inventory(self):self.assertEqual(len(self.o['nodes']['WALL_PURPOSE']['evidence']['immutable_constructive_wall_evidence']['rows']),110)
if __name__=='__main__':unittest.main()
