import unittest,json,copy
from pathlib import Path
from privacy116 import examine_module
P=Path(__file__).parent
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads((P/'evidence/module116_6x4.2.json').read_text())
 def test_saved_actual_and_fragment(self):
  self.assertEqual(examine_module(self.m)['evidence']['status'],'PASS_SCOPED_MODULE_PRIVACY')
  q=copy.deepcopy(self.m);q['units']=[q['unit']];self.assertFalse(examine_module(q)['errors'])
 def test_weak_screen(self):
  q=copy.deepcopy(self.m);q['walls']['privacy_screen'][3]='1'
  r=examine_module(q);self.assertNotEqual(r['evidence']['status'],'PASS_SCOPED_MODULE_PRIVACY');self.assertTrue(any(x['code']=='PRIVATE_TARGET_VISIBLE'for x in r['errors']))
 def test_missing_changing(self):
  q=copy.deepcopy(self.m);del q['unit']['activities']['bed1.changing'];self.assertTrue(examine_module(q)['pending'])
 def test_closed_only(self):
  q=copy.deepcopy(self.m);q['operations']['doors']=[];self.assertTrue(examine_module(q)['pending'])
 def test_cabinet_not_screen(self):
  q=copy.deepcopy(self.m);del q['walls']['privacy_screen'];self.assertNotEqual(examine_module(q)['evidence']['status'],'PASS_SCOPED_MODULE_PRIVACY')
if __name__=='__main__':unittest.main()
