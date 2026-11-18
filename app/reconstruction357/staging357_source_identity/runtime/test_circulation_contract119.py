import unittest
from rule_contract118 import evaluate_rule_contract,load_contract
class Test(unittest.TestCase):
 def report(self,integrity=None,comparison=None):
  adapters={r['id']:(lambda m:{'status':'PASS_LIMITED','witness':{'synthetic_test_only':True},'scope':'Unit-test dispatcher only, not geometry evidence'})for r in load_contract()['requirements']}
  adapters.pop('circulation_functional_integrity');adapters.pop('long_corridor_necessity')
  if integrity:adapters['circulation_functional_integrity']=integrity
  if comparison:adapters['long_corridor_necessity']=comparison
  return evaluate_rule_contract({'inputs':['18','24',2],'walls':{},'units':[{'id':'A','ownership':[['0','0','1','1']],'rooms':{},'fixtures':{},'activities':{},'fixture_metadata':{}}]},trusted_evaluators=adapters,context={'stage':'concept_internal'},applicability_evaluators={'long_corridor_necessity':lambda m:{'status':'PASS_LIMITED','witness':{'applies':True},'scope':'test'}})
 def test_missing_integrity_hard(self):self.assertIn('RULE_NOT_EVALUATED:circulation_functional_integrity',self.report()['pending'])
 def test_missing_comparison_review(self):
  r=self.report();self.assertNotIn('RULE_NOT_EVALUATED:long_corridor_necessity',r['pending']);self.assertEqual(r['review_findings'][0]['review_disposition'],'REVIEW_REQUIRED');self.assertEqual(r['review_findings'][0]['status'],'NOT_EVALUATED')
 def test_comparison_fail_not_pass_or_hard(self):
  r=self.report(comparison=lambda m:{'status':'FAIL','witness':{'reason':'no_better_alternative'},'scope':'comparison'});self.assertEqual(r['review_findings'][0]['status'],'FAIL');self.assertFalse(any(e.get('requirement_id')=='long_corridor_necessity'for e in r['errors']))
 def test_invalid_function_hard(self):
  for reason in('body_collision','dead_end_without_function','rename_residual_as_living'):
   r=self.report(integrity=lambda m:{'status':'FAIL','witness':{'reason':reason},'scope':'independent physical callback negative dispatch'});self.assertTrue(any(e.get('requirement_id')=='circulation_functional_integrity'for e in r['errors']))
if __name__=='__main__':unittest.main()
