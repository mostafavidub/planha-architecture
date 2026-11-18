import json,unittest
from pathlib import Path
from program_capacity_audit118 import examine
class Test(unittest.TestCase):
 def setUp(self):
  self.m=json.loads((Path(__file__).parent/'evidence/capacity118_whole18x24_metadata_bound.json').read_text());self.m=self.m.get('model',self.m)
 def test_positive(self):
  r=examine(self.m);self.assertEqual(r['errors'],[]);self.assertEqual(r['pending'],[]);self.assertEqual(r['evidence']['worst_unit_margin'],0)
 def test_double_count(self):
  self.m['units'][0]['public_program']['capacity']['living_seats'][0]['places']=3;self.assertTrue(examine(self.m)['errors'])
 def test_duplicate(self):
  seats=self.m['units'][0]['public_program']['capacity']['living_seats'];seats[1]=seats[0].copy();self.assertTrue(examine(self.m)['errors'])
 def test_other_occupied(self):
  seats=self.m['units'][0]['public_program']['capacity']['living_seats'];seats[1]['occupied_body']=seats[0]['occupied_body'];self.assertTrue(examine(self.m)['errors'])
 def test_block_access(self):
  self.m['walls']['block']=['6.4','5.1','6.9','5.8'];self.assertTrue(examine(self.m)['errors'])
 def test_sleep_route_missing(self):
  del self.m['units'][0]['routes']['bed2.bedB_back'];self.assertTrue(examine(self.m)['pending'])
if __name__=='__main__':unittest.main()
