"""Source attach on synthetic hosts. No model generation or technical approval."""
import copy,hashlib,inspect,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2];ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ENGINE),str(ROOT/'frontend')]
from source_finish_profile_reference_study import assess,digest
from source_wall_record_contract_study import ROOT_KEYS
import face_threshold118
def fixture():
 m=dict.fromkeys(ROOT_KEYS)
 m.update(schema='GENERAL125_WORLD_FRAME_STUDY',inputs=['20','25',2],accepted=False,release_allowed=False,ordered_macro=None,units=[{'id':'A'},{'id':'B'}],program={'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin']},openings=[],wall_hosts={
 'left':['0','0','.25','5'],'core.wall':['1','0','1.2','5'],'A.unit_shared_wing':['2','0','2.2','5'],'A.unit_boundary':['3','0','3.2','5'],'A.bath.wall':['4','0','4.2','5'],'B.kitchen.wall':['5','0','5.2','5'],'A.bed1.wall':['6','0','6.2','5'],'other':['7','0','7.2','5'],'skin':['8','0','8.04','5'],'horizontal':['0','6','5','6.2']})
 face_threshold118.attach(m)
 return m
class Finish(unittest.TestCase):
 def good(self,m):return assess(m,digest(m))
 def bad(self,m):self.assertEqual(self.good(m)['state'],'INVALID_FINISH_RECORD')
 def test_source_pin_and_import(self):
  p=ENGINE/'face_threshold118.py';b=p.read_bytes()
  self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'831854a591ab9a3a32716b98b161b3efcd43f2b4')
  self.assertEqual(pathlib.Path(inspect.getsourcefile(face_threshold118.attach)).resolve(),p.resolve())
 def test_source_built_profiles_on_ten_synthetic_hosts(self):
  m=fixture();before=digest(m);o=self.good(m)
  self.assertEqual(o['state'],'CONCEPT_PROFILE_GEOMETRY_BOUND_ONLY');self.assertEqual(len(o['bindings']),10)
  for k in ('accepted','qualified','origin_verified','technical_system_verified','whole_schema_verified'):self.assertIs(o[k],False)
  self.assertEqual(before,digest(m))
 def test_missing_extra_profile_and_unknown_field(self):
  for mode in range(3):
   m=fixture()
   if mode==0:del m['wall_finish_profile']['left']
   elif mode==1:m['wall_finish_profile']['extra']=copy.deepcopy(m['wall_finish_profile']['left'])
   else:m['wall_finish_profile']['left']['mystery']=1
   self.bad(m)
 def test_host_axis_face_and_offset(self):
  for key in ('axis','faces','offsets'):
   m=fixture();p=m['wall_finish_profile']['left'];p[key]['coordinate' if key=='axis' else 'minus']='9';self.bad(m)
 def test_layer_thickness_chain_and_order(self):
  for key,value in (('thickness_m','0'),('inner_interface_coordinate','9'),('outer_interface_coordinate','9'),('order_from_axis',True),('order_from_axis',2.0)):
   m=fixture();m['wall_finish_profile']['left']['layers'][0][key]=value;self.bad(m)
 def test_missing_duplicate_and_side_layer(self):
  for mode in range(3):
   m=fixture();ls=m['wall_finish_profile']['left']['layers']
   if mode==0:ls.pop()
   elif mode==1:ls.append(copy.deepcopy(ls[0]))
   else:ls[0]['side']='foreign'
   self.bad(m)
 def test_role_sequence_and_type(self):
  for key,value in (('layer_role','dry_finish'),('layer_type','membrane'),('status','VERIFIED')):
   m=fixture();m['wall_finish_profile']['left']['layers'][0][key]=value;self.bad(m)
 def test_unknown_not_zero_and_technical_flags(self):
  for key,value in (('construction_tolerance','0'),('system_verification','VERIFIED'),('claims_symmetric_construction',0)):
   m=fixture();m['wall_finish_profile']['left'][key]=value;self.bad(m)
  m=fixture();m['wall_finish_profile']['left']['unmodeled_components']['waterproofing_system']['numeric_zero_claimed']=0;self.bad(m)
 def test_type_and_digest_identity(self):
  m=fixture();d=digest(m);m['wall_finish_profile']['left']['faces']['minus']=0
  self.bad(m);self.assertEqual(assess(fixture(),'f'*64)['state'],'INVALID_FINISH_RECORD')
 def test_consistent_sum_with_changed_concept_allowance_rejected(self):
  m=fixture();ls=m['wall_finish_profile']['left']['layers']
  ls[0]['thickness_m']='.111';ls[0]['outer_interface_coordinate']='.014'
  ls[1]['thickness_m']='.014';ls[1]['inner_interface_coordinate']='.014'
  self.bad(m)
 def test_source_thin_wet_conflict_remains_unknown(self):
  m=fixture();m['wall_hosts']['A.bath.skin']=['9','0','9.04','5'];face_threshold118.attach(m)
  o=self.good(m);self.assertEqual(o['state'],'CONCEPT_PROFILE_GEOMETRY_BOUND_WITH_SOURCE_CONFLICT')
  self.assertEqual(o['source_semantic_conflicts'][0]['code'],'SOURCE_PROFILE_SEMANTIC_CONFLICT')
  self.assertEqual(o['source_semantic_conflicts'][0]['state'],'UNKNOWN');self.assertIs(o['profile_semantics_verified'],False)
 def test_narrative_is_not_authentication(self):
  m=fixture();m['wall_finish_profile']['left']['composition_authority']='untrusted synthetic narrative'
  o=self.good(m);self.assertEqual(o['state'],'CONCEPT_PROFILE_GEOMETRY_BOUND_ONLY');self.assertIs(o['origin_verified'],False)
if __name__=='__main__':unittest.main()
