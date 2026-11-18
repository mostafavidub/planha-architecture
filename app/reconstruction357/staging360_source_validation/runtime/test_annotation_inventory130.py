import unittest,json,copy
from pathlib import Path
from world_inventory125 import examine
class T(unittest.TestCase):
 def setUp(self):self.p=json.loads((Path(__file__).parent/'evidence130/case1_saved_rebuilt.json').read_text())['packet']
 def r(self):return examine(self.p['local_model'],self.p['world_model'],self.p['core'])
 def fail(self):r=self.r();self.assertTrue(r['errors']or r['pending'])
 def test_onebed_actual(self):self.assertEqual(self.r()['errors']+self.r()['pending'],[])
 def test_unknown_both(self):
  for k in ('local_model','world_model'):self.p[k]['unknown_geometry_scalar']=.4
  self.fail()
 def test_null_annotation_forbidden(self):self.p['world_model']['ordered_macro_coordinate_frame']=None;self.fail()
 def test_forged_nonnull_macro(self):
  for k in ('local_model','world_model'):self.p[k]['ordered_macro']={'kind':'fake','width':3}
  self.p['world_model']['ordered_macro_coordinate_frame']='IMMUTABLE_LOCAL_CONSTRUCTION_PROPOSAL';self.fail()
 def test_fake_annotation(self):self.p['world_model']['ordered_macro_coordinate_frame']='IMMUTABLE_LOCAL_CONSTRUCTION_PROPOSAL';self.fail()
 def test_retained_threebed(self):
  self.p=json.loads((Path(__file__).parent/'evidence129/case4_first_assembly.json').read_text())['packet'];self.assertEqual(self.r()['errors']+self.r()['pending'],[])
if __name__=='__main__':unittest.main()
