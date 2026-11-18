import unittest,json,copy
from pathlib import Path
from world_inventory125 import examine
class T(unittest.TestCase):
 def setUp(self):self.x=json.loads((Path(__file__).parent/'evidence125/world125_annotated39x7.07.json').read_text())
 def runcheck(self):return examine(self.x['local_model'],self.x['world_model'],self.x['core'])
 def test_current(self):r=self.runcheck();self.assertEqual(r['errors'],[]);self.assertEqual(r['pending'],[])
 def test_joint_scalar(self):
  for name in ('local_model','world_model'):self.x[name]['operations']['doors'][0]['new_geometry_offset']='.2'
  self.assertTrue(self.runcheck()['errors'])
 def test_joint_struct(self):
  for name in ('local_model','world_model'):self.x[name]['operations']['doors'][0]['future_motion']={'distance':'.2'}
  self.assertTrue(self.runcheck()['errors'])
 def test_missing(self):
  del self.x['world_model']['operations']['doors'][0]['continuous_actor_segments'];self.assertTrue(self.runcheck()['errors'])
 def test_core(self):self.x['core']['units']['A'][0]='.5';self.assertTrue(self.runcheck()['errors'])
 def test_embedded(self):
  self.x['world_model']['module_placements'][0]['module']['bounds'][0][0]='99';self.assertTrue(self.runcheck()['errors'])
if __name__=='__main__':unittest.main()
