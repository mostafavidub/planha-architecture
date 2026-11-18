import unittest,json
from pathlib import Path
from fractions import Fraction as F
from unsupported_extent_causes357 import boundary_openings,evaluate
from modules_spatial import rect
class Causes(unittest.TestCase):
 def test_sealed_and_gap(self):
  c=[rect(['0','0','1','1'])];walls=list(map(rect,[['-.1','-.1','0','1.1'],['1','-.1','1.1','1.1'],['0','-.1','1','0'],['0','1','1','1.1']]))
  self.assertEqual(boundary_openings(c,walls),[]);self.assertTrue(boundary_openings(c,walls[:-1]))
 def test_corner_touch_not_sealed(self):self.assertTrue(boundary_openings([rect(['0','0','1','1'])],[rect(['1','1','2','2'])]))
 def test_actual_components_sum(self):
  p=Path(__file__).resolve().parent;m=json.loads((p.parent/'staging357_comparative/attached_service_final357.json').read_text())['candidate']['model'];s=json.loads((p/'support_identity_actual357.json').read_text());o=evaluate(m,s)
  for u in o['units']:
   self.assertEqual(sum(F(c['area_m2'])for c in u['components']),F('6.595'));self.assertEqual(len(u['components']),3);self.assertEqual(sum(c['classification']=='SOLID_ENCLOSED_FLOOR_ISLAND'for c in u['components']),2)
 def test_stale_support(self):
  with self.assertRaises(ValueError):evaluate({}, {'model_hash':'wrong'})
if __name__=='__main__':unittest.main()
