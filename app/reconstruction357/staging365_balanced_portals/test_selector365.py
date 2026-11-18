import unittest,sys,json,copy
from pathlib import Path
from fractions import Fraction as F
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'planha_general150_runtime_work'))
from selector365 import select
from core_variant365 import core
class Tests(unittest.TestCase):
 def setUp(self):self.r=json.loads((B/'staging362_core_notch/actual362.json').read_text())
 def test_actual_domain_midpoint(self):
  x=select(self.r);self.assertEqual(list(map(F,x['selected_interval'])),[F('15.025'),F('15.075')]);self.assertEqual(F(x['entry_x']['A']),F('15.05'));self.assertFalse(x['accepted'])
 def test_not_hardcoded_obstacle_boundary(self):
  # Synthetic geometry seam only: a wider actual service-wall obstacle shifts midpoint.
  self.r['candidate']['model']['walls']['A.bath.A.service_right'][2]='13.1';x=select(self.r);self.assertEqual(F(x['entry_x']['A']),F('15.0625'))
 def test_empty_domain(self):
  self.r['candidate']['model']['walls']['testblocking']=['13.1','12.35','14','12.46'];self.assertRaises(ValueError,select,self.r)
 def test_unsupported_width(self):
  o=next(o for o in self.r['candidate']['model']['openings']if o['id']=='A.entry');o['rect'][2]='14.5';self.assertRaises(ValueError,select,self.r)
 def test_wrong_body_profile(self):
  self.r['candidate']['model']['profile']['body_m']='.8';self.assertRaises(ValueError,select,self.r)
 def test_source_geometry_preservation(self):
  c=core(F(26),F(28));old=self.r['candidate']['packet']['core']
  for k in('stair','lift','lobby','unit_ownership','units','notch362'):self.assertEqual(c[k],old[k])
 def test_actual_input_immutable(self):
  before=copy.deepcopy(self.r);select(self.r);self.assertEqual(self.r,before)
 def test_fixed_lineage_other_request_rejected(self):self.assertRaises(ValueError,core,F(25),F(28))
if __name__=='__main__':unittest.main()
