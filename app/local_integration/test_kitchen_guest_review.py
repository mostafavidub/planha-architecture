import unittest,json,copy
from pathlib import Path
from kitchen_guest_review import assess
class KitchenGuest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.models=[c['model']for c in json.loads((Path(__file__).parent/'evidence/requests/c1dd58b3-97ce-4d1c-9934-ea6a5a6a64b3/result.json').read_text())['candidates']]
 def test_actual_models_remain_unqualified(self):
  for m in self.models:
   r=assess(m);self.assertEqual(r['state'],'PASS_SCOPED_SEPARATION');self.assertFalse(r['display_allowed']);self.assertFalse(r['accepted']);self.assertEqual(len(r['units']),2)
 def test_crossing_rejected(self):
  m=copy.deepcopy(self.models[0]);u=m['units'][0];q=u['rooms']['kitchen'][0];u['entry_point']=[q[0],q[1]];u['scenario_routes']['guest_living']=[u['entry_point'],[q[2],q[1]]];u['scenario_routes']['guest_dining']=u['scenario_routes']['guest_living'];self.assertEqual(assess(m)['state'],'FAIL_INTERSECTION')
 def test_missing_kitchen_is_unknown(self):
  m=copy.deepcopy(self.models[0]);del m['units'][0]['rooms']['kitchen'];self.assertEqual(assess(m)['state'],'UNKNOWN')
 def test_missing_route_is_unknown(self):
  m=copy.deepcopy(self.models[0]);m['units'][0]['scenario_routes']['guest_dining']=[];self.assertEqual(assess(m)['state'],'UNKNOWN')
 def test_missing_motion_is_unknown(self):
  m=copy.deepcopy(self.models[0]);m['operations']['kitchen'][0]['motion_envelopes']=[];self.assertEqual(assess(m)['state'],'UNKNOWN')
 def test_body_width_not_centerline(self):
  m=copy.deepcopy(self.models[0]);u=m['units'][0];q=u['rooms']['kitchen'][0];from fractions import Fraction as F
  y=str(F(q[1])-F('.1'));u['entry_point']=[q[0],y];u['scenario_routes']['guest_living']=[u['entry_point'],[q[2],y]];u['scenario_routes']['guest_dining']=u['scenario_routes']['guest_living'];self.assertEqual(assess(m)['state'],'FAIL_INTERSECTION')
if __name__=='__main__':unittest.main()
