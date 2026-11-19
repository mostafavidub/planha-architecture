"""Real source-built modules installed into a synthetic shell, not a generated plan."""
import copy,hashlib,inspect,pathlib,sys,unittest
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parents[2];ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ENGINE),str(ROOT/'frontend')]
from source_module_floor_reference_study import assess,transformed,digest,EXPECTED
from source_wall_record_contract_study import ROOT_KEYS
PINS={"bedroom_module116.py":"289b23f25bafaa05281015b521affad5ab5a415d","twin_module118.py":"0da5c7b24a614d22f7ab9f9a4d2d68bcdb6ede15","bathroom_module117.py":"db08bc7558db9be37ec8ac10839b1173d56555e6","kitchen_module117.py":"8ec837d51e724076d8b479763b132756137de61b","place_module116.py":"8dab53d28173052c6b106bf91fd7d2585d9e3da6","place_bathroom117.py":"982bbb6dc584641b1a4894751e0f13e252da10ea","place_kitchen117.py":"8d4048d922f8c1052028e0c2e3172f2b8e75c3ce","final_public_floor120.py":"e91c70d8c308240e2cb7e7784634cecfb036240b"}
def build_fixture():
 import bedroom_module116,twin_module118,bathroom_module117,kitchen_module117
 import place_module116,place_bathroom117,place_kitchen117
 specs=[('bed1',bedroom_module116,'5.45','3.6'),('bed2',twin_module118,'5.45','4.5'),('bath',bathroom_module117,'4.3','3.1'),('kitchen',kitchen_module117,'3.6','4.2')]
 modules={name:mod.build(w,d) for name,mod,w,d in specs}
 for name,mod,w,d in specs:
  assert pathlib.Path(inspect.getsourcefile(mod.build)).resolve()==(ENGINE/(mod.__name__+'.py')).resolve()
 m=dict.fromkeys(ROOT_KEYS)
 m.update(schema='GENERAL125_WORLD_FRAME_STUDY',inputs=['20','25',2],accepted=False,release_allowed=False,units=[],program={'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin']},walls={},wall_hosts={},source_wall_hosts={},openings=[],operations={},logical_regions={},room_metadata={},module_ports=[],module_aprons={},module_placements=[])
 for uid in ('A','B'):
  u={'id':uid,'rooms':{k:[['0','0','1','1']] for k in ('bed1','bed2','bath','kitchen','dining','living','entry_circulation')},'fixtures':{},'fixture_metadata':{},'activities':{}}
  for name,mod,w,d in specs:
   q=[F(1),F(1),F(1)+F(w),F(1)+F(d)]
   if name in ('bed1','bed2'):place_module116.install(modules[name],m,u,uid,name,q,F(25),'left' if name=='bed1' else 'right')
   elif name=='bath':place_bathroom117.install(modules[name],m,u,uid,q,F(25))
   else:place_kitchen117.install(modules[name],m,u,uid,q,F(25))
  m['units'].append(u)
 return m
class ModuleFloors(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.original=build_fixture()
 def model(self):return copy.deepcopy(self.original)
 def reject(self,fn):
  m=self.model();fn(m);r=assess(m,digest(m));self.assertEqual(r['state'],'INVALID_MODULE_FLOOR_CONTRACT');return r
 def test_source_pins(self):
  for name,pin in PINS.items():
   b=(ENGINE/name).read_bytes();self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin)
 def test_eight_real_module_installations_synthetic_shell(self):
  m=self.model();r=assess(m,digest(m));self.assertEqual(r['state'],'SOURCE_MODULE_FLOORS_AND_APRONS_BOUND_ONLY')
  self.assertEqual(len(r['bindings']),8)
  self.assertEqual({(x['unit'],x['room']) for x in r['bindings']},{(u,k) for u in ('A','B') for k in EXPECTED})
  for k in ('origin_verified','whole_schema_verified','physical_verified','accepted','qualified','display_allowed','delivery_allowed','source_content_authenticated'):self.assertIs(r[k],False)
 def test_missing_duplicate_and_foreign_placement(self):
  self.reject(lambda m:m['module_placements'].pop())
  self.reject(lambda m:m['module_placements'].__setitem__(1,copy.deepcopy(m['module_placements'][0])))
  self.reject(lambda m:m['module_placements'][0].update(unit_id='C'))
 def test_room_floor_mutation(self):
  self.reject(lambda m:m['units'][0]['rooms']['bed1'][0].__setitem__(0,'999'))
 def test_apron_missing_extra_and_geometry(self):
  self.reject(lambda m:m['module_aprons'].pop('A.bed1'))
  self.reject(lambda m:m['module_aprons'].update({'A.bed3':[['0','0','1','1']]}))
  self.reject(lambda m:m['module_aprons']['A.bed1'].__setitem__(0,['100','100','101','101']))
 def test_transform_type_matrix_translation(self):
  self.reject(lambda m:m['module_placements'][0]['transform'].__setitem__('matrix',[[True,0],[0,1]]))
  self.reject(lambda m:m['module_placements'][0]['transform']['translation'].__setitem__(0,1.0))
 def test_source_module_hash_and_role(self):
  self.reject(lambda m:m['module_placements'][0].update(module_hash='0'*64))
  def mutate(m):
   p=m['module_placements'][0];p['module']['schema']='UNDECLARED';p['module_hash']=digest(p['module'])
  self.reject(mutate)
 def test_source_floor_rehashed_tamper_still_rejected(self):
  def mutate(m):
   p=m['module_placements'][0];p['module']['unit']['rooms']['public_access']=[['100','100','101','101']];p['module_hash']=digest(p['module'])
  self.reject(mutate)
 def test_unknown_fields_and_room_role(self):
  self.reject(lambda m:m['module_placements'][0].update(extra=True))
  self.reject(lambda m:m['units'][0]['rooms'].update(bed3=[]))
 def test_fixed_nonzero_signed_permutation_rectangle(self):
  got=transformed(['0.125','1.375','12.625','20.875'],{'matrix':[[0,-1],[1,0]],'translation':['30','-5']})
  self.assertEqual(got,[F('9.125'),F('-4.875'),F('28.625'),F('7.625')])
 def test_model_digest_and_no_mutation(self):
  m=self.model();h=digest(m);self.assertEqual(assess(m,'0'*64)['state'],'INVALID_MODULE_FLOOR_CONTRACT')
  assess(m,h);self.assertEqual(digest(m),h)
if __name__=='__main__':unittest.main()
