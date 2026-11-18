import unittest,sys,copy,json
from pathlib import Path
from fractions import Fraction as F
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'planha_general150_runtime_work'));sys.path.insert(0,str(BASE/'semantic_rules357'))
from contract114 import core_first
from core_variant362 import derive
from modules_spatial import rect,union_area,intersection
class Tests(unittest.TestCase):
 def setUp(self):self.old=core_first(F(26),F(28));self.new=derive(self.old)
 def test_protected_core(self):
  for k in('stair','lift','entry_centers','units'):self.assertEqual(self.old[k],self.new[k])
 def test_gross_area_nondeterioration(self):
  for uid in('A','B'):
   a=union_area(list(map(rect,self.old['unit_ownership'][uid])));b=union_area(list(map(rect,self.new['unit_ownership'][uid])));self.assertEqual(b-a,F('1.5675')if uid=='A'else 0)
 def test_lobby_delta(self):self.assertEqual(union_area(list(map(rect,self.old['lobby'])))-union_area(list(map(rect,self.new['lobby']))),F('1.44'))
 def test_new_wall_no_floor_overlap(self):
  wall=rect(self.new['notch362']['new_separator']);floor=rect(self.new['notch362']['new_A_floor_ownership']);self.assertIsNone(intersection(wall,floor));self.assertTrue(all(intersection(wall,rect(r))is None for r in self.new['lobby']))
 def test_wall_joins_existing_lift(self):
  r=rect(self.new['notch362']['new_separator']);lift=rect(self.new['lift']);self.assertEqual(r[2],lift[0]);self.assertEqual(r[3],lift[1]-F('.15'))
 def test_wrong_core_shape(self):
  c=copy.deepcopy(self.old);c['lobby'][1][0]='0';self.assertRaises(ValueError,derive,c)
 def test_entry_rail_truncation(self):
  c=copy.deepcopy(self.old);c['entry_centers']['A'][0]='15';self.assertRaises(ValueError,derive,c)
 def test_no_input_mutation(self):
  c=copy.deepcopy(self.old);derive(c);self.assertEqual(c,self.old)
 def test_source_junction_closure(self):
  from notch_frame362 import outer_right
  r=outer_right(self.new,F('.15'));self.assertEqual(r,[F('17.575'),F('12.475'),F('17.725'),F('15.375')])
  self.assertEqual((r[2]-r[0])*(F('12.625')-r[1]),F('9/400'))
  self.assertTrue(all(intersection(rect(list(map(str,r))),rect(q))is None for q in self.new['unit_ownership']['A']))
 def test_junction_source_mismatch(self):
  from notch_frame362 import outer_right
  c=copy.deepcopy(self.new);c['lift'][2]='17.5';self.assertRaises(ValueError,outer_right,c,F('.15'))
if __name__=='__main__':unittest.main()
