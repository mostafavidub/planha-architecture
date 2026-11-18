import unittest,copy,json
from pathlib import Path
from service_closure362 import ownership_nondecrease,reconcile_scope,assess,ROOT
class Tests(unittest.TestCase):
 def test_ownership_growth_not_identity(self):self.assertTrue(ownership_nondecrease([[0,0,1,1]],[[0,0,2,1]]))
 def test_ownership_loss_blocks(self):self.assertFalse(ownership_nondecrease([[0,0,2,1]],[[0,0,1,1]]))
 def test_outside_entry_residual_blocks(self):self.assertFalse(reconcile_scope({'complete':True},{'unassigned_after_source_clearance_m2':'1/100'}))
 def test_actual(self):
  paths=['staging362_core_notch/actual362.json','review362_source_validation/result.json','staging359_hall_clamp/actual359.json','review359_source_validation/result.json'];args=[json.loads((ROOT/p).read_text())for p in paths];out=assess(*args);self.assertEqual(out['verdict'],'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS');self.assertEqual(len(out['units']),2);self.assertFalse(out['all_parent_acceptance'])
 def test_tampered_current_blocks(self):
  paths=['staging362_core_notch/actual362.json','review362_source_validation/result.json','staging359_hall_clamp/actual359.json','review359_source_validation/result.json'];args=[json.loads((ROOT/p).read_text())for p in paths];args[1]['raw_report']['errors']=['injected']
  with self.assertRaises(ValueError):assess(*args)
if __name__=='__main__':unittest.main()
