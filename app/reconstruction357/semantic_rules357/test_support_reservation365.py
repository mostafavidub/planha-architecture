import unittest,json,copy
from pathlib import Path
from support_reservation365 import reconcile
ROOT=Path(__file__).resolve().parents[1]
class Reconcile365(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=json.loads((ROOT/'semantic_rules357/role_registry_on365.json').read_text())['nodes']['PUBLIC_SUPPORT']['evidence'];cls.r=json.loads((ROOT/'semantic_rules357/entry_separation_actual365.json').read_text())
 def test_current_exact_nonusable(self):
  o=reconcile(self.s,self.r);self.assertFalse(o['unresolved_positive_extent']);self.assertEqual(o['rows'][0]['nonusable_operational_reservation_area_m2'],'3/1000');self.assertEqual(o['rows'][0]['usable_floor_capacity_increment'],0)
 def test_no_epsilon_gap_removal(self):
  s=copy.deepcopy(self.s);s['rows'][0]['unresolved_regions'].append(['1','1','1.000000001','1.000000001']);self.assertTrue(reconcile(s,self.r)['unresolved_positive_extent'])
 def test_outside_reservation_rejected(self):
  r=copy.deepcopy(self.r);r['reservations'][0]['region'][0]='13'
  with self.assertRaisesRegex(ValueError,'EXTRA'):reconcile(self.s,r)
 def test_usable_laundering_rejected(self):
  r=copy.deepcopy(self.r);r['reservations'][0]['usable_floor_capacity_increment']=1
  with self.assertRaisesRegex(ValueError,'NONUSABLE'):reconcile(self.s,r)
 def test_wrong_model_rejected(self):
  r=copy.deepcopy(self.r);r['model_hash']='old362'
  with self.assertRaisesRegex(ValueError,'MODEL_BINDING'):reconcile(self.s,r)
if __name__=='__main__':unittest.main()
