import unittest,copy
from unittest.mock import patch
from rule_contract118 import evaluate_rule_contract as run,load_contract,result,digest
M={'inputs':['15','21',2],'units':[{'id':'A','ownership':[[0,0,1,1]],'rooms':{'bed1':[[0,0,1,1]]},'fixtures':{},'activities':{},'fixture_metadata':{}}],'walls':{}}
def positive(m):return result('PASS_LIMITED',{'measured_model_hash':digest(m)},'Synthetic callback plumbing only, not architectural proof')
def mutating(m):m['inputs'][0]='5';return positive(m)
class Tests(unittest.TestCase):
 def test_registry89(self):self.assertEqual(len(load_contract()['registry']),89)
 def test_missing_named(self):
  r=run(M);self.assertIn('RULE_NOT_EVALUATED:q11_functional_boundary',r['pending']);self.assertFalse(r['accepted'])
 def test_receipt_never_pass(self):self.assertTrue(run(M,evidence_by_rule={'q11_functional_boundary':{'status':'PASS'}})['errors'])
 def test_actual_domain_reject(self):
  m=copy.deepcopy(M);m['inputs'][2]='2.5';self.assertTrue(run(m)['errors'])
 def test_malformed_rectangle(self):
  m=copy.deepcopy(M);m['walls']['x']=[0,0,0,2];self.assertTrue(run(m)['errors'])
 def test_named_callback_scope(self):
  r=run(M,trusted_evaluators={'q11_functional_boundary':positive});self.assertNotIn('RULE_NOT_EVALUATED:q11_functional_boundary',r['pending']);self.assertIn('RULE_NOT_EVALUATED:guest_dining_route',r['pending']);self.assertFalse(r['eligible_for_draft_export'])
 def test_callback_mutation_reject(self):self.assertTrue(run(M,trusted_evaluators={'q11_functional_boundary':mutating})['errors'])
 def test_single_batch_not_fake_distinct(self):
  r=run(M,context={'stage':'concept_internal','batch_models':[M]});x=next(x for x in r['requirements']if x['requirement_id']=='geometric_diversity');self.assertEqual(x['status'],'NOT_APPLICABLE_TO_STAGE_OR_MODEL');self.assertFalse(r['all_rules_approved'])
 def test_attach_does_not_inherit_pass(self):
  from rule_contract118 import attach_rule_contract
  report={'checker_version':'GENERAL117_TEST','model_hash':digest(M),'status':'PASS_CONCEPT_SCOPED_REVIEW','errors':[],'pending':[],'eligible_for_draft_export':True}
  r=attach_rule_contract(M,report,context={'stage':'concept_internal','batch_models':[M]});self.assertFalse(r['eligible_for_draft_export']);self.assertIn('RULE_NOT_EVALUATED:guest_dining_route',r['pending'])
 def test_stage_is_not_approval(self):
  r=run(M,context={'stage':'concept_internal','batch_models':[M]});x=next(x for x in r['requirements']if x['requirement_id']=='export_parity');self.assertEqual(x['status'],'NOT_APPLICABLE_TO_STAGE_OR_MODEL');self.assertFalse(r['accepted'])
 def test_laundry(self):
  m=copy.deepcopy(M);m['units'][0]['rooms']['laundry']=[[0,0,.1,.1]];self.assertTrue(run(m)['errors'])
 def test_contract_tamper(self):
  with patch('pathlib.Path.read_bytes',return_value=b'{}'):
   with self.assertRaises(ValueError):load_contract()
if __name__=='__main__':unittest.main()
