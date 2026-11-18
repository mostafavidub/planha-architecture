import json,copy,unittest
from pathlib import Path
from row_adapter358 import validate,inventory
class Tests(unittest.TestCase):
 def setUp(self):
  x=json.loads(Path(__file__).with_name('row_candidate358.json').read_text());self.r=x['trace']['raw'];self.p=x['trace']['proposal']
 def test_actual(self):self.assertIsNotNone(validate(self.r,self.p))
 def test_asset_tamper(self):
  p=copy.deepcopy(self.p);p['rectangles']['bath'][2]='30'
  with self.assertRaises(ValueError):validate(self.r,p)
 def test_macro_tamper(self):
  p=copy.deepcopy(self.p);p['ordered_macro']['rectangles']['bed1'][0]='0'
  with self.assertRaises(ValueError):validate(self.r,p)
 def test_seat_overlap(self):
  p=copy.deepcopy(self.p);p['rectangles']['chair1_use']=p['rectangles']['chair2_use']
  with self.assertRaises(ValueError):validate(self.r,p)
 def test_inventory(self):
  s=inventory();self.assertTrue(any('/references/'in k for k in s));self.assertTrue(any(k.endswith('.json')for k in s));self.assertTrue(any(k.endswith('row_body358.py')for k in s))
if __name__=='__main__':unittest.main()
