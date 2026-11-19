"""Synthetic exact geometry/transport tests, not generated model witnesses."""
import copy,hashlib,itertools,math,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import numpy as np
from left_right_two_source_binding import swap_point,swap_rect,isometry,transport,inventory,exact,digest,raw_check
from study_frame125_two_nonsquare import transport_boundary
class ExactGeometry(unittest.TestCase):
 def test_source_pins(self):
  pins={'left_right_two_source_binding.py':'9b4c6fa08ba53051cb4f7ffda683d7561a509514','study_frame125_two_nonsquare.py':'aeb2d85893dd960f36be2102b60c7058a56ffb47'}
  for name,pin in pins.items():
   b=(ROOT/'app/local_integration'/name).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin)
 def test_decimal_nonsquare_point_rectangle_involution(self):
  q=['0.125','1.375'];r=['0.125','1.375','12.625','20.875']
  self.assertEqual(swap_point(q),['1.375','0.125'])
  self.assertEqual(swap_rect(r),['1.375','0.125','20.875','12.625'])
  self.assertTrue(exact(swap_point(swap_point(q)),q))
  self.assertTrue(exact(swap_rect(swap_rect(r)),r))
  raw_check({'W':'12.5','L':'20.25','n':2,'requested_count':1})
 def test_all_eight_d4_compositions_roundtrip(self):
  count=0
  for swap in (False,True):
   for a,b in itertools.product((-1,1),repeat=2):
    m=[[0,a],[b,0]] if swap else [[a,0],[0,b]]
    t={'matrix':m,'translation':['0.125','-2.375']}
    for mode in ('placement','canonical'):
     self.assertTrue(exact(isometry(isometry(t,mode),mode),t))
    count+=1
  self.assertEqual(count,8)
 def test_invalid_signed_permutation_types_and_rank(self):
  for m in ([[1,1],[0,0]],[[1,0],[1,0]],[[.5,.5],[.5,.5]],[[True,0],[0,1]],[[1.0,0],[0,1]],[[2,0],[0,1]]):
   with self.subTest(matrix=m):
    with self.assertRaises(ValueError):isometry({'matrix':m,'translation':['0','0']},'placement')
 def test_explicit_field_roundtrip_not_whole_model(self):
  obj={'rect':['.1','.2','1.3','2.4'],'path':[['.1','.2'],['1.3','2.4']],'normal':['0','1'],'canonical_isometry':{'matrix':[[0,-1],[1,0]],'translation':['.25','1.5']},'module':{'immutable':['.1','.2']}}
  # Canonical decimal lexical representation is expected from source coordinates.
  canonical={'rect':['0.1','0.2','1.3','2.4'],'path':[['0.1','0.2'],['1.3','2.4']],'normal':['0','1'],'canonical_isometry':{'matrix':[[0,-1],[1,0]],'translation':['.25','1.5']},'module':{'immutable':['.1','.2']}}
  frozen=digest(obj);self.assertTrue(exact(transport(transport(obj)),canonical));self.assertEqual(digest(obj),frozen)
 def test_duplicate_unit_identity_rejected(self):
  for units in ([{'id':'A'},{'id':'A'}],[{'id':'B'},{'id':'A'}],[{'id':'A'}]):
   with self.assertRaisesRegex(ValueError,'UNIT_ORDER'):inventory({'units':units})
 def test_shared_fixture_names_are_unit_local(self):
  names='WC_iranian shower_floor basin fridge sink prep cooker sofa1 sofa2 armchair1 armchair2 dining_table dining_chair_front dining_chair_back dining_chair_west dining_chair_east bed1.bed bed1.closet bed2.bedA bed2.bedB bed2.closet'.split()
  # Synthetic inventory shape only; no geometry or distinct seat-instance proof.
  unit={'fixtures':dict.fromkeys(names),'fixture_metadata':dict.fromkeys(names),'rooms':dict.fromkeys(['bed1','bed2','bath','kitchen','dining','living','entry_circulation']),'dining_module_placement':{'module':{'seating':{'instances':[None]*4}}}}
  local={'units':[dict(copy.deepcopy(unit),id=u) for u in ('A','B')],'program':{'bedrooms_per_unit':2,'sleep_roles':['double','twin']},'walls':{},'physical_wall_network':{'source_aliases':{}}}
  inventory(local)
 def test_exact_json_identity_and_digest(self):
  for a,b in ((False,0),(2,2.0),('2',2),([1,2],(1,2))):
   self.assertFalse(exact(a,b))
  self.assertNotEqual(digest(False),digest(0));self.assertNotEqual(digest(2),digest(2.0))
 def test_float64_allowed_role_binaryratio_and_signedzero(self):
  for v in (np.float64(.1),np.float64(-0.0),np.float64(0.0),np.float64(12.625)):
   p={'local_model':{'proposal_network_paths':{'bed1':[[v,0]]}}}
   before=digest(p);out,ctx,receipt=transport_boundary(p,{})
   got=out['local_model']['proposal_network_paths']['bed1'][0][0]
   self.assertIs(type(got),float);self.assertEqual(got.as_integer_ratio(),v.as_integer_ratio())
   self.assertEqual(math.copysign(1,got),math.copysign(1,float(v)))
   self.assertEqual(receipt['digest_before'],receipt['digest_after']);self.assertEqual(digest(p),before)
 def test_numeric_boundary_rejects_wrong_role_type_and_nonfinite(self):
  cases=[{'unknown':np.float64(.1)},{'local_model':{'proposal_network_paths':{'bed1':[[np.float32(.1),0]]}}},{'local_model':{'proposal_network_paths':{'bed1':[[np.float64('nan'),0]]}}},{'local_model':{'proposal_network_paths':{'bed1':[[np.float64('inf'),0]]}}}]
  for p in cases:
   with self.assertRaises((AssertionError,ValueError,TypeError)):transport_boundary(p,{})
if __name__=='__main__':unittest.main()
