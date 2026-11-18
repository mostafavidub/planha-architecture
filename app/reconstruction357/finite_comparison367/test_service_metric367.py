import unittest
from service_criterion367_v2 import scoped_metric
class Tests(unittest.TestCase):
 def example(self):return {'current_source_service_only_route_area_m2':'3','current_source_nonservice_only_route_area_m2':'4','current_source_shared_route_area_m2':'2','whole_entry_area_m2':'9','all_cells_required_traversal_bound':True,'classification_scope':'CURRENT_SOURCE_DECLARED_ROUTE_USE_CLASSES_NOT_EXCLUSIVITY_OF_ALL_POSSIBLE_FUNCTIONS','service_only_outside_source_approach_m2':'2'}
 def test_nonzero_exact_scope_not_global(self):
  x=scoped_metric(self.example());self.assertEqual(x['A_exclusive_service_circulation_m2'],'3');self.assertIsNone(x['global_exclusive_function_m2'])
 def test_missing_partition(self):
  x=self.example();x['whole_entry_area_m2']='10'
  with self.assertRaises(ValueError):scoped_metric(x)
 def test_unknown_inventory(self):
  x=self.example();x['all_cells_required_traversal_bound']=False
  with self.assertRaises(ValueError):scoped_metric(x)
 def test_wrong_scope(self):
  x=self.example();x['classification_scope']='ANY POSSIBLE USE'
  with self.assertRaises(ValueError):scoped_metric(x)
 def test_approach_not_doublecounted(self):
  x=self.example();x['service_only_outside_source_approach_m2']='4'
  with self.assertRaises(ValueError):scoped_metric(x)
if __name__=='__main__':unittest.main()
