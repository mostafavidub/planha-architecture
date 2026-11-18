"""Producer regression only. Not independent acceptance."""
import unittest,copy,json
from pathlib import Path
from fractions import Fraction as F
from bathroom_module117 import build
class Test(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=build()
 def test_inventory(self):
  self.assertEqual(len(self.m['operations']['doors']),3);self.assertEqual(set(self.m['unit']['fixtures']),{'WC_iranian','shower_floor','basin'})
 def test_fixed_source_dimensions(self):
  expected={'WC_iranian':(F('.7'),F('.7')),'shower_floor':(F('.9'),F('.9')),'basin':(F('.45'),F('.45'))}
  for k,q in self.m['unit']['fixtures'].items():
   q=list(map(F,q));self.assertEqual((q[2]-q[0],q[3]-q[1]),expected[k])
 def test_three_panel_rigid_translations(self):
  for o in self.m['operations']['doors']:
   c=list(map(F,o['closed_panel']));d=list(map(F,o['translation']));self.assertEqual([c[i]+d[i%2]for i in range(4)],list(map(F,o['open_panel'])))
 def test_negative_forged_panel(self):
  o=copy.deepcopy(self.m['operations']['doors'][0]);o['open_panel'][0]=str(F(o['open_panel'][0])+F('.1'));c=list(map(F,o['closed_panel']));d=list(map(F,o['translation']));self.assertNotEqual([c[i]+d[i%2]for i in range(4)],list(map(F,o['open_panel'])))
 def test_actual_tasks_have_routes(self):
  self.assertFalse(self.m['route_failures']);self.assertEqual(set(self.m['unit']['routes']),set(self.m['unit']['activities']))
 def test_decimal_rigid_basin_anchor(self):
  q=build('3.4','2.5');self.assertFalse(q['route_failures']);self.assertEqual(F(q['unit']['fixtures']['basin'][3]),F('2.5'))
  for key in self.m['unit']['fixtures']:
   a=list(map(F,self.m['unit']['fixtures'][key]));b=list(map(F,q['unit']['fixtures'][key]));self.assertEqual((a[2]-a[0],a[3]-a[1]),(b[2]-b[0],b[3]-b[1]))
 def test_bounds_not_global_proof(self):
  with self.assertRaises(ValueError):build('3.1499','2.25')
if __name__=='__main__':unittest.main()
