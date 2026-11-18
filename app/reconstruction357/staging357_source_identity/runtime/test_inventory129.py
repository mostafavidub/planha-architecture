import unittest,json,copy
from pathlib import Path
from world_inventory125 import examine
class T(unittest.TestCase):
 def setUp(self):self.p=json.loads((Path(__file__).parent/'evidence129/case4_first_assembly.json').read_text())['packet']
 def result(self):return examine(self.p['local_model'],self.p['world_model'],self.p['core'])
 def reject(self):r=self.result();self.assertTrue(r['errors']or r['pending'])
 def test_actual(self):r=self.result();self.assertEqual(r['errors']+r['pending'],[])
 def test_joint_unknown_scalar(self):
  for k in ('local_model','world_model'):self.p[k]['private_domains'][0]['invented_width']=.7
  self.reject()
 def test_joint_unknown_struct(self):
  for k in ('local_model','world_model'):self.p[k]['operations']['doors'][0]['new_geometry']={'offset':.3}
  self.reject()
 def test_missing_path(self):self.p['world_model']['private_domains'][0]['paths'].pop('A.bed3');self.reject()
 def test_joint_missing_path(self):
  for k in ('local_model','world_model'):self.p[k]['private_domains'][0]['paths'].pop('A.bed3')
  self.reject()
 def test_false_side(self):self.p['world_model']['private_domains'][0]['public_interface']['open_side']='top';self.reject()
 def test_false_coordinate(self):self.p['world_model']['private_domains'][0]['parts'][0][0]='.123';self.reject()
 def test_missing_instance(self):self.p['world_model']['units'][0]['fixtures'].pop('bed3.bedA');self.reject()
 def test_added_fixture(self):
  for k in ('local_model','world_model'):self.p[k]['units'][0]['fixtures']['fake_bed']=['1','1','2','2']
  self.reject()
if __name__=='__main__':unittest.main()
