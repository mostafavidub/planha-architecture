import unittest,json,copy
from pathlib import Path
from whole_circulation_compare119 import compare,digest
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.m=json.loads(Path('evidence/compact118_reassembled_actual.json').read_text())['model']
 def evaluator(self,m):return {'model_hash':digest(m),'excluded_requirements':['long_corridor_necessity'],'errors':[],'pending':['RULE_NOT_EVALUATED:long_corridor_necessity'],'noncomparison_pending':[],'status':'PASS_NONCIRCULAR_PHYSICAL_SCOPED'}
 def test_identical_not_alternative(self):self.assertIn('ALTERNATIVE_IDENTICAL_TO_CURRENT',compare(self.m,self.m,self.evaluator)['pending'])
 def test_program_change(self):
  a=copy.deepcopy(self.m);a['program']['bedrooms_per_unit']=1
  self.assertIn('ALTERNATIVE_INPUT_PROGRAM_CORE_OR_FURNITURE_MISMATCH',compare(self.m,a,self.evaluator)['errors'])
 def test_actual_failure_retained(self):
  def bad(m):r=self.evaluator(m);r['errors']=['ACTUAL_COLLISION'];return r
  self.assertEqual(compare(self.m,self.m,bad)['status'],'FAIL')
 def test_other_pending_retained(self):
  def bad(m):r=self.evaluator(m);r['noncomparison_pending']=['RULE_NOT_EVALUATED:private_grouping'];return r
  self.assertIn('alternative:OTHER_NAMED_REQUIREMENTS_UNRESOLVED',compare(self.m,self.m,bad)['pending'])
 def test_wrong_exclusion(self):
  def bad(m):r=self.evaluator(m);r['excluded_requirements']+=['private_grouping'];return r
  self.assertEqual(compare(self.m,self.m,bad)['status'],'FAIL')
 def test_wrong_hash(self):
  def bad(m):r=self.evaluator(m);r['model_hash']='fake';return r
  self.assertEqual(compare(self.m,self.m,bad)['status'],'FAIL')
if __name__=='__main__':unittest.main()
