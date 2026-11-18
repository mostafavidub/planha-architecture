import unittest,json,copy
from pathlib import Path
from fractions import Fraction as F
import bedroom_sections358 as s
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  x=json.loads((Path(__file__).resolve().parents[1]/'staging358_comparative/row_candidate358.json').read_text());cls.m=next(p['module']for p in x['candidate']['model']['module_placements']if p['unit_id']=='A'and p['room_id']=='bed1')
 def test_actual_inventory(self):
  records,summary=s.operation_inventory(self.m);self.assertTrue(any(r['id'].startswith('door:')and r['kind']=='actor_continuous'for r in records));self.assertEqual(len(records),len({r['id']for r in records}));self.assertEqual(len(summary),3)
 def test_missing_actor(self):
  m=copy.deepcopy(self.m);m['operations']['doors'][0]['continuous_actor_segments']=[]
  with self.assertRaises(ValueError):s.operation_inventory(m)
 def test_duplicate_panel(self):
  m=copy.deepcopy(self.m);p=m['operations']['closets'][0]['panels'];p.append(copy.deepcopy(p[0]))
  with self.assertRaises(ValueError):s.operation_inventory(m)
 def test_panel_motion(self):
  m=copy.deepcopy(self.m);m['operations']['doors'][0]['translation']=['99','0']
  with self.assertRaises(ValueError):s.operation_inventory(m)
 def test_exact_hole_not_bbox(self):
  r=s.sections([(F(0),F(0),F(4),F(4))],[(F(1),F(1),F(3),F(3))]);self.assertEqual(r['free_area_m2'],'12');self.assertEqual(r['slabs']['0'][1]['component_widths_m'],['1','1'])
if __name__=='__main__':unittest.main()
