import unittest
from cost_ledger367 import bound_join,digest
class Tests(unittest.TestCase):
 def fixtures(self):
  r={'candidate':{'model':{'x':1}}};v={'review':1};entry={'record_digest':digest(r),'fresh_result_digest':digest(v),'model_digest':digest(r['candidate']['model']),'verdict':'PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE','units':[{'unit':'A','verdict':'PASS_SCOPED_INTRINSIC_CURRENT_SOURCE_REQUIRED_ACCESS_ROLE','all_cells_required_traversal_bound':True,'service_only_outside_source_approach_m2':'17/3','classification_scope':'SOURCE_CURRENT_ROUTES_ONLY'}]}
  m={'against359':{'evidence':[{}, {'units':[{'unit':'A','outside_entry_unassigned_m2':'17/3','bath_union_m2':'12'}]}],'units':[{'unit':'A'}]},'against362':{'units':[{'unit':'A'}]}}
  return r,v,m,entry
 def test_nonzero_cost_preserved(self):
  x=bound_join(*self.fixtures());self.assertEqual(x['units'][0]['actual_source_service_route_only_m2'],'17/3');self.assertEqual(x['verdict'],'UNKNOWN');self.assertIsNone(x['units'][0]['global_exclusive_function_m2'])
 def test_no_foreign_model(self):
  r,v,m,e=self.fixtures();e['model_digest']='other'
  with self.assertRaises(ValueError):bound_join(r,v,m,e)
 def test_no_unknown_role(self):
  r,v,m,e=self.fixtures();e['verdict']='UNKNOWN'
  with self.assertRaises(ValueError):bound_join(r,v,m,e)
 def test_no_cost_disagreement(self):
  r,v,m,e=self.fixtures();e['units'][0]['service_only_outside_source_approach_m2']='0'
  with self.assertRaises(ValueError):bound_join(r,v,m,e)
if __name__=='__main__':unittest.main()
