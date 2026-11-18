import unittest,json,sys,copy
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent
sys.path.insert(0,str(B/'staging365_balanced_portals'));sys.path.insert(0,str(B/'planha_general150_runtime_work'));sys.path.insert(0,str(P))
from protected365 import check
class Tests(unittest.TestCase):
 def setUp(self):
  self.old=json.loads((B/'staging362_core_notch/actual362.json').read_text())['candidate'];self.new=json.loads((B/'staging365_balanced_portals/actual365.json').read_text())['candidate']
 def test_actual(self):self.assertEqual(check(self.old,self.new)['rows'][0]['added_area'],'0')
 def test_core_tamper(self):
  self.new['packet']['core']['lift'][0]='0';self.assertRaises(ValueError,check,self.old,self.new)
 def test_model_owner_tamper(self):
  self.new['model']['units'][0]['ownership'].pop();self.assertRaises(ValueError,check,self.old,self.new)
 def test_floor_outside(self):
  self.new['model']['units'][0]['rooms']['fake']=[['100','100','101','101']];self.assertRaises(ValueError,check,self.old,self.new)
if __name__=='__main__':unittest.main()
