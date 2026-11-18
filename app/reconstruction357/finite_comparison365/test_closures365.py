import unittest,copy,json
from pathlib import Path
import service_closure365 as service
from q04_closure365 import objective,compare,ROOT
R=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());V=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());M=R['candidate']['model']
class Tests(unittest.TestCase):
 def test_complete_common_inventory(self):
  values,b=objective(M);self.assertEqual(len(b),4);self.assertEqual(len([k for k in values if k.startswith('COMMON/')and not k.endswith('floor_m2')]),8)
 def test_missing_common_task_rejected(self):
  m=copy.deepcopy(M);del m['common_routes']['stair_B']
  with self.assertRaises(ValueError):objective(m)
 def test_anchor_change_rejected(self):
  m=copy.deepcopy(M);m['common_routes']['lift_A'][0][0]='16.4'
  with self.assertRaises(ValueError):compare(M,m)
 def test_no_service_ownership_loss(self):self.assertFalse(service.ownership_nondecrease([['0','0','2','2']],[['0','0','1','2']]))
 def test_outside_entry_residual_blocks(self):self.assertFalse(service.reconcile_scope({'complete':True},{'unassigned_after_source_clearance_m2':'1/4'}))
 def test_missing_entry_coverage_blocks(self):self.assertFalse(service.reconcile_scope({'complete':False},{'unassigned_after_source_clearance_m2':'0'}))
 def test_forged_fresh_rejected(self):
  v=copy.deepcopy(V);v['accepted']=True
  with self.assertRaises(ValueError):service.evaluate(R,v)
if __name__=='__main__':unittest.main()
