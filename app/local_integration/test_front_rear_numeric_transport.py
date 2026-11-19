"""Synthetic numeric boundary checks, not fresh geometry acceptance."""
import unittest,copy,numpy as np
from front_rear_runtime_adapter import proposal_transport,digest
NAMES=['bed1','bed2','bath','kitchen','dining','sofa1_use','sofa2_use','chair1_use','chair2_use','entry_apron']
def proposal():
 return {'rectangles':{n:[np.float64(.25),np.float64(-0.0),np.float64(5.5),np.float64(4.5)] for n in NAMES},
 'network_paths':{n:[[np.float64(.25),np.float64(1.5)] for _ in range(5)] for n in (set(NAMES)-{'entry_apron','dining'})|{'dining_front','dining_back','dining_west','dining_east'}},'bedrooms':2,'accepted':False}
class NumericBoundary(unittest.TestCase):
 def test_exact_binary64_coordinates(self):
  p=proposal();q,r=proposal_transport(p)
  self.assertEqual(digest(p),digest(q));self.assertEqual(len(r['coordinate_conversions']),160)
  self.assertIs(type(q['rectangles']['bed1'][0]),float);self.assertEqual(q['rectangles']['bed1'][1].hex(),'-0x0.0p+0')
  self.assertIs(type(p['rectangles']['bed1'][0]),np.float64)
 def test_nonfinite(self):
  for x in (np.float64('nan'),np.float64('inf')):
   p=proposal();p['rectangles']['bed1'][0]=x
   with self.assertRaises(ValueError):proposal_transport(p)
 def test_metadata_not_coerced(self):
  for key in ('bedrooms','accepted','solver_seconds','unknown'):
   p=proposal();p[key]=np.float64(2)
   with self.assertRaises(ValueError):proposal_transport(p)
 def test_missing_route_rejected(self):
  p=proposal();del p['network_paths']['dining_front']
  with self.assertRaises(ValueError):proposal_transport(p)
 def test_nested_metadata_rejected(self):
  p=proposal();p['metadata']={'hidden':np.float64(0)}
  with self.assertRaises(ValueError):proposal_transport(p)
 def test_other_numpy_types_rejected(self):
  for x in (np.float32(.25),np.int64(1),np.bool_(False)):
   p=proposal();p['rectangles']['bed1'][0]=x
   with self.assertRaises(ValueError):proposal_transport(p)
 def test_unknown_roles_and_shapes(self):
  for field in ('rectangles','network_paths'):
   p=proposal();p[field]['mystery']=p[field].get('bed1')
   with self.assertRaises(ValueError):proposal_transport(p)
  p=proposal();p['rectangles']['bed1'].append(1)
  with self.assertRaises(ValueError):proposal_transport(p)
 def test_native_scalar_types_unchanged(self):
  p=proposal();p['rectangles']['bed1']=[1,1.0,False,0]
  q,r=proposal_transport(p)
  self.assertEqual([type(x) for x in q['rectangles']['bed1']],[int,float,bool,int])
  # This boundary is not geometric schema acceptance; original proposal_check follows.
if __name__=='__main__':unittest.main()
