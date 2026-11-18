import unittest,copy
from service_cost_ledger365_v3 import join_intrinsic
class Tests(unittest.TestCase):
 def fixtures(self):
  m={'record_digest':'r','fresh_result_digest':'f','model_digest':'m','units':[{'unit':'A','cost_inventory':{'unclassified_route_only_m2':'1911/200'}}]}
  e={**{k:m[k]for k in ('record_digest','fresh_result_digest','model_digest')},'verdict':'PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE','units':[{'unit':'A','verdict':'PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE','all_cells_required_traversal_bound':True,'service_only_outside_source_approach_m2':'1911/200','classification_scope':'CURRENT_SOURCE_ROUTE_USE_ONLY'}]};return m,e
 def test_nonzero_retained_not_acceptance(self):
  m,e=self.fixtures();x=join_intrinsic(m,e);self.assertEqual(x['units'][0]['cost_inventory']['actual_source_service_route_only_m2'],'1911/200');self.assertEqual(x['verdict'],'UNKNOWN')
 def test_unknown_role_rejected(self):
  m,e=self.fixtures();e['verdict']='UNKNOWN'
  with self.assertRaises(ValueError):join_intrinsic(m,e)
 def test_unchecked_unit_rejected(self):
  m,e=self.fixtures();e['units'][0]['all_cells_required_traversal_bound']=False
  with self.assertRaises(ValueError):join_intrinsic(m,e)
 def test_wrong_model_rejected(self):
  m,e=self.fixtures();e['model_digest']='other'
  with self.assertRaises(ValueError):join_intrinsic(m,e)
 def test_missing_unit_rejected(self):
  m,e=self.fixtures();e['units']=[]
  with self.assertRaises(ValueError):join_intrinsic(m,e)
 def test_cost_disagreement_rejected(self):
  m,e=self.fixtures();e['units'][0]['service_only_outside_source_approach_m2']='0'
  with self.assertRaises(ValueError):join_intrinsic(m,e)
if __name__=='__main__':unittest.main()
