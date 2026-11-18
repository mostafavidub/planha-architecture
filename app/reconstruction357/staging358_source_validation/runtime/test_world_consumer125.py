import unittest,json,copy
from pathlib import Path
from checker114 import check_module_placements,check_whole_privacy117
from dining_motion_audit118 import examine_whole
P=Path(__file__).parent/'evidence125/world125_transfer_bound39x7.07.json'
class T(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=json.loads(P.read_text())
 def test_placement_world(self):self.assertEqual(check_module_placements(self.x['world_model'])['errors'],[])
 def test_transfer_missing_transform(self):
  m=copy.deepcopy(self.x['world_model']);d=next(d for d in m['operations']['doors']if 'open_transfer_points'in d);d['open_transfer_points'][0].reverse();self.assertTrue(check_module_placements(m)['errors'])
 def test_singular(self):
  m=copy.deepcopy(self.x['world_model']);m['module_placements'][0]['transform']['matrix']=[[1,0],[1,0]];self.assertTrue(check_module_placements(m)['errors'])
 def test_missing_field(self):
  m=copy.deepcopy(self.x['world_model']);del m['operations']['doors'][0]['continuous_actor_segments'];self.assertTrue(check_module_placements(m)['errors'])
 def test_dining(self):self.assertEqual(examine_whole(self.x['world_model'])['errors'],[])
 def test_privacy(self):
  r=check_whole_privacy117(self.x['world_model']);self.assertEqual(r['errors'],[]);self.assertEqual(r['pending'],[])
if __name__=='__main__':unittest.main()
