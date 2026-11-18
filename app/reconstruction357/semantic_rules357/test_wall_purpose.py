import unittest,json,copy
from pathlib import Path
from wall_purpose import evaluate,module_claims,source_base,touches,material_boundary_support
from common import rows
from fractions import Fraction as F
class Walls(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0];cls.e=cls.r['central_envelope'];cls.f=cls.r['central_fresh_review'];cls.m=cls.e['packet']['world_model'];cls.req=rows(cls.m,cls.f['raw_fresh_report'])
 def test_actual_inventory(self):
  o=evaluate(self.e,self.f);self.assertEqual(len(o['rows']),len(self.m['walls']));self.assertFalse(o['parent_complete']);self.assertEqual(o['counts']['PASS_CONSTRUCTOR_BOUNDARY_WITH_ACTUAL_PROTECTED_USE'],21);self.assertEqual(o['counts']['PASS_SOURCE_FUNCTIONAL_MODULE_BOUNDARY'],72)
 def test_mutated_wall_not_accepted(self):
  m=copy.deepcopy(self.m);m['walls']['A.bed1.right'][0]='2.8'
  with self.assertRaises(ValueError):module_claims(m,self.req)
 def test_source_actual_fixture_join(self):
  m=copy.deepcopy(self.m);m['units'][0]['fixtures']['bed1.bed'][0]='7'
  with self.assertRaises(ValueError):module_claims(m,self.req)
 def test_source_method_missing(self):
  r=copy.deepcopy(self.req);r['door_operation']['status']='NOT_EVALUATED'
  with self.assertRaises(ValueError):module_claims(self.m,r)
 def test_no_corner_only_adjacency(self):self.assertFalse(touches((F(0),F(0),F(1),F(1)),(F(1),F(1),F(2),F(2))))
 def test_all_eight_material_layers_join(self):
  o=evaluate(self.e,self.f);layer=[r for r in o['rows']if r['verdict']=='PASS_SOURCE_HOST_MATERIAL_FUNCTIONAL_BOUNDARY'];self.assertEqual(len(layer),8)
  for r in layer:self.assertTrue(r['source_material_boundary_proof']['source_material_chain']);self.assertTrue(r['source_material_boundary_proof']['actual_adjacent_source_regions'])
 def test_layer_outside_host_unsupported(self):
  source={'walls':{'layer':['5','5','6','6']},'wall_hosts':{'host':['0','0','1','1']},'unit':{'rooms':{'room':[['1','0','2','1']]}}};self.assertIsNone(material_boundary_support(source,'layer'))
 def test_disconnected_material_not_cavity_fill(self):
  source={'walls':{'layer':['0','0','1','.1'],'boundary':['0','.9','1','1']},'wall_hosts':{'host':['0','0','1','1']},'unit':{'rooms':{'room':[['0','1','1','2']]}}};self.assertIsNone(material_boundary_support(source,'layer'))
 def test_tampered_actual_layer_rejected(self):
  m=copy.deepcopy(self.m);m['walls']['A.bath.A.bath_right1.assembly3'][0]='11.5'
  with self.assertRaises(ValueError):module_claims(m,self.req)
 def test_wrong_frame_not_assumed(self):
  e=copy.deepcopy(self.e);e['packet']['family']='LEFT_RIGHT'
  with self.assertRaises(ValueError):source_base(e)
if __name__=='__main__':unittest.main()
