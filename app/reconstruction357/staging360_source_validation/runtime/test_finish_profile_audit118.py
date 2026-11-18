import copy,unittest
from finish_profile_audit118 import examine
class Tests(unittest.TestCase):
 def fixture(self):return {'wall_hosts':{'test':['1','0','1.15','2']},'wall_finish_profile':{'test':{'role':'dry_partition','profile_kind':'CONCEPT_SENSITIVITY_NOT_TECHNICAL','source_reference':'Blueprint B02 conceptual15/25; asymmetric test fixture only','axis':{'orientation':'vertical','coordinate':'1.05'},'offsets':{'minus':'.05','plus':'.10'},'faces':{'minus':'1','plus':'1.15'},'system_verification':'NOT_VERIFIED','construction_tolerance':'UNKNOWN_NOT_ZERO','layer_composition_status':'DECLARED_LAYER_HYPOTHESIS_NOT_TECHNICALLY_VERIFIED','layer_profile_source':'Synthetic arithmetic test fixture, not a project material profile','finish_by_side':{'minus':'EXPLICITLY_ABSENT_WITH_BASIS','plus':'EXPLICITLY_ABSENT_WITH_BASIS'},'finish_absence_basis':{'minus':'Synthetic no-finish fixture only','plus':'Synthetic no-finish fixture only'},'layers':[{'id':'minus_assumption','order_from_axis':1,'inner_interface_coordinate':'1.05','outer_interface_coordinate':'1','side':'minus','layer_type':'core','material_model_or_concept_type':'Synthetic core part for arithmetic test','thickness_basis':'Explicit synthetic test geometry, no project authority','thickness_m':'.05','existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION'},{'id':'plus_assumption','order_from_axis':1,'inner_interface_coordinate':'1.05','outer_interface_coordinate':'1.15','side':'plus','layer_type':'core','material_model_or_concept_type':'Synthetic core part for arithmetic test','thickness_basis':'Explicit synthetic test geometry, no project authority','thickness_m':'.1','existence':'ASSUMED_PRESENT','status':'CONCEPT_ASSUMPTION'}]}}}
 def test_asymmetric_actual_faces(self):self.assertEqual(examine(self.fixture())['status'],'PASS_CONCEPT_FACE_LAYER_GEOMETRY')
 def test_aggregate_half_is_not_composition(self):
  m=self.fixture();m['wall_finish_profile']['test']['layers'][0]['meaning']='Aggregate modeled finished-envelope half; not material';self.assertEqual(examine(m)['status'],'NOT_EVALUATED')
 def test_unknown_finish_is_not_absent(self):
  m=self.fixture();m['wall_finish_profile']['test']['finish_by_side']['minus']='UNKNOWN';self.assertEqual(examine(m)['status'],'NOT_EVALUATED')
 def test_generic_role_not_profile(self):
  m=self.fixture();m['wall_finish_profile']['test']['role']='source_bound_module_host';self.assertEqual(examine(m)['status'],'NOT_EVALUATED')
 def test_order_tamper(self):
  m=self.fixture();m['wall_finish_profile']['test']['layers'][0]['order_from_axis']=2;self.assertEqual(examine(m)['status'],'FAIL')
 def test_interface_tamper(self):
  m=self.fixture();m['wall_finish_profile']['test']['layers'][0]['outer_interface_coordinate']='1.01';self.assertEqual(examine(m)['status'],'FAIL')
 def test_unknown_geometry_not_performance(self):
  m=self.fixture();m['wall_finish_profile']['test']['unmodeled_components']={'membrane':{'modeled_state':'NOT_SPECIFIED','performance':'NOT_VERIFIED'}};self.assertEqual(examine(m)['status'],'NOT_EVALUATED')
 def test_axis_wrong(self):
  m=self.fixture();m['wall_finish_profile']['test']['axis']['coordinate']='1.075';self.assertEqual(examine(m)['status'],'FAIL')
 def test_sum_wrong(self):
  m=self.fixture();m['wall_finish_profile']['test']['layers'][0]['thickness_m']='.04';self.assertEqual(examine(m)['status'],'FAIL')
 def test_unknown_not_zero(self):
  m=self.fixture();m['wall_finish_profile']['test']['layers'][0]['thickness_m']=None;self.assertEqual(examine(m)['status'],'NOT_EVALUATED')
 def test_unknown_disguised_zero(self):
  m=self.fixture();m['wall_finish_profile']['test']['layers'][0]['thickness_m']='0';self.assertEqual(examine(m)['status'],'FAIL')
 def test_faces_wrong(self):
  m=self.fixture();m['wall_finish_profile']['test']['faces']['plus']='1.14';self.assertEqual(examine(m)['status'],'FAIL')
 def test_technical_claim_rejected(self):
  m=self.fixture();m['wall_finish_profile']['test']['system_verification']='APPROVED';self.assertEqual(examine(m)['status'],'FAIL')
 def test_symmetry_not_inferred(self):
  m=self.fixture();m['wall_finish_profile']['test']['claims_symmetric_construction']=True;self.assertEqual(examine(m)['status'],'FAIL')
if __name__=='__main__':unittest.main()
