import unittest,json
from fractions import Fraction as F
from dead_end_predicate358 import evaluate,ROOT
class DeadEnd(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  r=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text());v=json.loads((ROOT/'review358_source_validation/result.json').read_text());cls.o=evaluate(r,v)
 def test_no_false_uselessness_failure(self):self.assertEqual(self.o['verdict'],'UNKNOWN_NO_CURRENT_SOURCE_PURPOSE_WITNESS');self.assertIn('not an authoritative maximum',self.o['independent_audit_limit'])
 def test_current_positive_distal_witness(self):
  self.assertEqual(len(self.o['rows']),4)
  for r in self.o['rows']:self.assertEqual(F(r['distal_no_current_witness_area_m2']),F('5.25'));self.assertEqual(r['operation_envelopes_excluded'],[])
 def test_no_execution(self):self.assertFalse(self.o['geometry_mutated']);self.assertFalse(self.o['admission_allowed']);self.assertEqual(self.o['operator_plan']['execution_state'],'PLAN_ONLY_NO_OPERATOR_EXECUTED_NO_NEW_FRESH')
if __name__=='__main__':unittest.main()
