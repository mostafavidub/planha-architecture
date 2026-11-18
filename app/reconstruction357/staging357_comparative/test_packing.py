import unittest,json,copy
from pathlib import Path
from packing_validator import verify
class Tests(unittest.TestCase):
 def setUp(self):
  x=json.loads(Path(__file__).with_name('attached_service_candidate357.json').read_text());self.r=x['trace']['raw'];self.p=x['trace']['proposal']
 def test_actual(self):self.assertEqual(verify(self.r,self.p)['errors'],[])
 def test_size(self):
  p=copy.deepcopy(self.p);p['rectangles']['bath'][2]='20';self.assertTrue(verify(self.r,p)['errors'])
 def test_claim_not_authority(self):
  p=copy.deepcopy(self.p);p['accepted']=True;p['rectangles']['chair1_use']=p['rectangles']['chair2_use'];self.assertTrue(verify(self.r,p)['errors'])
 def test_missing_inventory(self):
  p=copy.deepcopy(self.p);p['rectangles'].pop('dining');self.assertTrue(verify(self.r,p)['errors'])
 def test_approach(self):
  p=copy.deepcopy(self.p);p['source_approach_reservations']={};self.assertTrue(verify(self.r,p)['errors'])
if __name__=='__main__':unittest.main()
