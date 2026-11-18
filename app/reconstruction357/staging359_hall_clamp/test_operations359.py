import unittest,json
from pathlib import Path
from operation_reservations359 import *
from clamp_geometry359 import clamp
class Tests(unittest.TestCase):
 def test_continuous_crossing_not_just_endpoints(self):
  swept=bbox([['0','0','1','1'],['0','8','1','9']]);x=clamp(['0','4','10','5'],[['3','0','4','4']],['4','4','5','6'],{'x':[['4','5'],['4','1']]},{'moving_actor':swept},'.8');self.assertEqual(x['hall'][0],'0')
 def test_invalid_rectangle_stops(self):
  with self.assertRaises(ValueError):bbox([['0','0','0','1']])
 def test_unknown_group_stops(self):
  with self.assertRaises(ValueError):extract({'invented':[]},'.7')
 def test_current358_operation_schema_readonly(self):
  m=json.loads((Path(__file__).resolve().parents[1]/'staging358_comparative/row_candidate358.json').read_text())['candidate']['model'];r=extract(m['operations'],m['profile']['body_m']);self.assertGreater(len(r),100)
if __name__=='__main__':unittest.main()
