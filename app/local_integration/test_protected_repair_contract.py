import unittest,copy
from protected_repair_contract import protected,digest
def packet():
 u=lambda uid:{'id':uid,'fixtures':{uid+'.bed':['0','0','2','1']},'fixture_metadata':{uid+'.bed':{'kind':'bed','source_size_m':['2','1']}}}
 return {'core':{'x':2},'world_model':{'inputs':{'n':2},'program':{'units':2},'profile':{'body_m':'.7'},'units':[u('A'),u('B')],'accepted':False,'release_allowed':False}}
class Tests(unittest.TestCase):
 def test_actual_dimensions(self):
  p=packet();self.assertEqual(protected(p)['fixture_inventory']['A']['A.bed']['actual_dimensions_m'],['1','2'])
 def test_translation_preserves(self):
  p=packet();q=copy.deepcopy(p);q['world_model']['units'][0]['fixtures']['A.bed']=['3','4','5','5'];self.assertEqual(digest(protected(p)),digest(protected(q)))
 def test_program_int_float_differs(self):
  p=packet();q=copy.deepcopy(p);q['world_model']['program']['units']=2.0;self.assertNotEqual(digest(protected(p)),digest(protected(q)))
 def test_core_bool_zero_differs(self):
  p=packet();p['core']['x']=0;q=copy.deepcopy(p);q['core']['x']=False;self.assertNotEqual(digest(protected(p)),digest(protected(q)))
 def test_dimension_differs(self):
  p=packet();q=copy.deepcopy(p);q['world_model']['units'][0]['fixtures']['A.bed'][2]='2.01';self.assertNotEqual(digest(protected(p)),digest(protected(q)))
 def test_duplicate_unit_rejected(self):
  p=packet();p['world_model']['units'][1]['id']='A'
  with self.assertRaises(ValueError):protected(p)
 def test_metadata_missing_rejected(self):
  p=packet();p['world_model']['units'][0]['fixture_metadata']={}
  with self.assertRaises(ValueError):protected(p)
 def test_boolean_coordinate_rejected(self):
  p=packet();p['world_model']['units'][0]['fixtures']['A.bed'][0]=False
  with self.assertRaises(ValueError):protected(p)
 def test_source_size_type_differs(self):
  p=packet();q=copy.deepcopy(p);q['world_model']['units'][0]['fixture_metadata']['A.bed']['source_size_m']=[2,1];self.assertNotEqual(digest(protected(p)),digest(protected(q)))
 def test_authority_rejected(self):
  p=packet();p['world_model']['accepted']=True
  with self.assertRaises(ValueError):protected(p)
if __name__=='__main__':unittest.main()
