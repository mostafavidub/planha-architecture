import copy,json,unittest
from pathlib import Path
import named_checks118 as named
from circulation_integrity119 import evaluate
from rule_contract118 import evaluate_rule_contract
class Registration(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads(Path('evidence/alternative119/case5_diningports_variant2_whole.json').read_text())['model']
 def audit(self,m,adapters):return evaluate_rule_contract(m,trusted_evaluators=adapters,context={'stage':'concept_internal','batch_models':[m]})
 def test_binding_actual(self):
  from final_route_ledger120 import evaluate as final_ledger
  wrapper=named.circulation_functional_integrity120
  self.assertIs(named.adapters_for_workflow(None)['circulation_functional_integrity'],wrapper)
  m=json.loads(Path('evidence/correction120/case2_final_floor_only.json').read_text())['after']
  report=wrapper(m)
  self.assertEqual(report['witness']['actual_functional_integrity'],evaluate(m))
  self.assertEqual(report['witness']['final_route_classification'],final_ledger(m))
  self.assertEqual(report['status'],'PASS_LIMITED')
  r=self.audit(m,{'circulation_functional_integrity':wrapper});row=next(v for v in r['requirements']if v['requirement_id']=='circulation_functional_integrity');self.assertEqual(row['status'],'PASS_LIMITED')
 def test_missing_hard(self):
  r=self.audit(self.m,{});self.assertIn('RULE_NOT_EVALUATED:circulation_functional_integrity',r['pending']);self.assertNotIn('RULE_NOT_EVALUATED:long_corridor_necessity',r['pending']);self.assertTrue(any(x['requirement_id']=='long_corridor_necessity'for x in r['review_findings']))
 def test_actual_collision_hard(self):
  m=copy.deepcopy(self.m);m['units'][0]['routes']['dining_east']=[['0','0'],['1','0']];r=self.audit(m,{'circulation_functional_integrity':named.circulation_functional_integrity120});self.assertTrue(any(x.get('requirement_id')=='circulation_functional_integrity'for x in r['errors']))
if __name__=='__main__':unittest.main()
