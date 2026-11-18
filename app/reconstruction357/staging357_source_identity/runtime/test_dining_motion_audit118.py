import unittest,json,copy
from pathlib import Path
from dining_motion_audit118 import examine
class Test(unittest.TestCase):
 def setUp(self):self.m=json.loads((Path(__file__).parent/'evidence/dining118_3.1x3.5_body_study.json').read_text())
 def test_saved(self):
  r=examine(self.m);self.assertEqual(r['errors'],[]);self.assertEqual(len(r['evidence']['continuous_witnesses']),8);self.assertEqual(r['evidence']['minimum_envelope_dimensions'],['3','17/5']);self.assertFalse(r['evidence']['accepted']);self.assertTrue(r['pending'])
 def test_other_occupied(self):
  self.m['seating']['instances'][1]['occupied_body']=['.1','1.4','.8','2.1'];self.assertTrue(any(x['code']=='DINING_CONTINUOUS_COLLISION'for x in examine(self.m)['errors']))
 def test_table(self):
  self.m['fixtures']['table']=['.7','1.15','1.5','2.35'];self.assertTrue(any(x['code']=='DINING_CONTINUOUS_COLLISION'for x in examine(self.m)['errors']))
 def test_shrink(self):
  self.m['width']='2.9';self.assertTrue(any(x['code']=='DINING_CONTINUOUS_OUTSIDE'for x in examine(self.m)['errors']))
 def test_body(self):
  self.m['seating']['instances'][0]['rise_transfer']['segments'][0]['actor_end'][2]='.7';self.assertTrue(examine(self.m)['errors'])
 def test_discontinuity(self):
  self.m['seating']['instances'][0]['rise_transfer']['segments'][1]['actor_start'][0]='.06';self.assertTrue(examine(self.m)['errors'])
if __name__=='__main__':unittest.main()
