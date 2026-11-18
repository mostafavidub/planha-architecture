import unittest
from service_cost_ledger365_v2 import cost_bounds
class Tests(unittest.TestCase):
 def test_nonzero_not_discarded(self):
  x=cost_bounds('3189/250','1911/200');self.assertEqual(x['service_room_plus_unclassified_cost_interval_m2'],['3189/250','22311/1000']);self.assertIsNone(x['exclusive_service_circulation_m2'])
 def test_unknown_not_pass(self):self.assertFalse(cost_bounds('1','1')['role_classification_complete'])
 def test_zero_measurement_not_final_acceptance(self):self.assertNotIn('verdict',cost_bounds('1','0'))
 def test_negative_rejected(self):
  with self.assertRaises(ValueError):cost_bounds('1','-1')
if __name__=='__main__':unittest.main()
