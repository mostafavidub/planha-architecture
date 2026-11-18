import unittest,json,copy
from pathlib import Path
from public_program_audit118 import examine_dining_module,examine
P=Path(__file__).parent
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads((P/'evidence/dining118_3.1x3.5.json').read_text())
 def test_actual_pull_not_capacity_pass(self):
  r=examine_dining_module(self.m);self.assertFalse(r['errors']);self.assertEqual(r['evidence']['actual_distinct_chairs'],4);self.assertTrue(r['pending'])
 def test_delete_chair(self):
  m=copy.deepcopy(self.m);del m['fixtures']['chair_west'];self.assertTrue(examine_dining_module(m)['errors'])
 def test_source_size(self):
  m=copy.deepcopy(self.m);m['fixtures']['chair_west'][2]='1.14';self.assertTrue(examine_dining_module(m)['errors'])
 def test_fake_pull(self):
  m=copy.deepcopy(self.m);m['seating']['instances'][0]['pulled_rect'][0]='0.1';self.assertTrue(examine_dining_module(m)['errors'])
 def test_route_through_table(self):
  u={'id':'A','ownership':[[0,0,10,10]],'rooms':{'living':[[0,0,10,10]]},'fixtures':{'dining_table':[4,4,5,6]},'activities':{},'entry_point':[1,5],'scenario_routes':{'guest_living':[[1,5],[8,5]]}}
  r=examine({'walls':{},'units':[u]});self.assertTrue(any(x['code']=='PUBLIC_ROUTE_FORBIDDEN_INTERSECTION'for x in r['errors']));self.assertTrue(any('guest_dining'in x for x in r['pending']))
if __name__=='__main__':unittest.main()
