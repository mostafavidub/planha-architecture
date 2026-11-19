import copy,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
from one_bed_pair_source_study import normalize_proposal,program_bind,RECTS,TERMINALS,digest
def proposal():
 return {'bedrooms':1,'sleep_roles':['double'],'rectangles':{k:[0.,0.,1.,1.]for k in RECTS},'network_paths':{k:[[0.,0.]for _ in range(5)]for k in TERMINALS},'bed_door_sides':{'bed1':'left'}}
class OneBed(unittest.TestCase):
 def test_exact_one_bed_roles_and_no_mutation(self):
  p=proposal();h=digest(p);q,r=normalize_proposal(p);self.assertEqual(digest(q),h);self.assertEqual(digest(p),h)
 def test_no_bed2_hidden_fallback(self):
  p=proposal();p['rectangles']['bed2']=[0.,0.,1.,1.]
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_program_types_and_roles(self):
  for value in (True,1.0,2):
   p=proposal();p['bedrooms']=value
   with self.assertRaises(ValueError):normalize_proposal(p)
  p=proposal();p['sleep_roles']=['twin']
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_terminal_missing_and_wrong_dining_alias(self):
  p=proposal();p['network_paths']['dining']=p['network_paths'].pop('dining_west')
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_binary64_lossless_and_wrong_role(self):
  import numpy as np
  p=proposal();p['rectangles']['bed1'][0]=np.float64(-0.0)
  q,r=normalize_proposal(p);self.assertEqual(r['conversions'],1);self.assertEqual(q['rectangles']['bed1'][0].hex(),'-0x0.0p+0')
  p=proposal();p['metadata']=np.float64(1)
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_bad_scalar_and_path(self):
  for value in (False,float('nan'),float('inf'),'1'):
   p=proposal();p['rectangles']['bed1'][0]=value
   with self.assertRaises(ValueError):normalize_proposal(p)
  p=proposal();p['network_paths']['bed1'].pop()
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_registry_and_model_count_not_population(self):
  p={'id':'PROGRAM_1BED_V1','approval':{'status':'APPROVED_DESIGN_PROGRAM'},'bedrooms_per_unit':1,'design_persons_per_unit':2,'sleep_roles':['double'],'capacity_means_actual_population':False}
  m={'program':{'units':2,'bedrooms_per_unit':1,'sleep_roles':['double'],'design_occupants_per_unit':2,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True},'units':[{'id':'A'},{'id':'B'}],'accepted':False,'release_allowed':False}
  program_bind(m,p);m['program']['design_occupants_per_unit']=4
  with self.assertRaises(ValueError):program_bind(m,p)
 def test_side_keys_and_type(self):
  p=proposal();p['bed_door_sides']['bed2']='left'
  with self.assertRaises(ValueError):normalize_proposal(p)
if __name__=='__main__':unittest.main()
