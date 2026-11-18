import unittest,json,copy
from pathlib import Path
from dining_motion_audit118 import examine_whole
from public_program_audit118 import examine
class Test(unittest.TestCase):
 def setUp(self):
  self.m=json.loads((Path(__file__).parent/'evidence/capacity118_whole18x24_metadata_bound.json').read_text());self.m=self.m.get('model',self.m)
 def test_positive(self):
  r=examine_whole(self.m);self.assertEqual(r['errors'],[]);self.assertEqual(len(r['evidence']['seats']),8)
 def test_actual_wall(self):
  self.m['walls']['new_obstacle']=['1.01','1.66','1.1','1.8'];self.assertTrue(examine_whole(self.m)['errors'])
 def test_fixture(self):
  self.m['units'][0]['fixtures']['dining_chair_west'][0]='1.5';self.assertTrue(examine_whole(self.m)['errors'])
 def test_egress(self):
  self.m['operations']['dining_chairs'][0]['egress_route'][0]=['1','1'];self.assertTrue(examine_whole(self.m)['errors'])
 def test_public_walking_not_exception(self):
  u=self.m['units'][0];r=u['fixtures']['dining_chair_east'];u['scenario_routes']['guest_dining']=[[r[0],r[1]],[r[2],r[1]]];self.assertTrue(any(x['code']=='PUBLIC_ROUTE_FORBIDDEN_INTERSECTION'for x in examine(self.m)['errors']))
if __name__=='__main__':unittest.main()
