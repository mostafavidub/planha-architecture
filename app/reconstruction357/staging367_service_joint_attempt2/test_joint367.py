import unittest,copy
from joint367 import original,original_parameters,assert_notch_entry,protect
from core_notch367 import derive
class Tests(unittest.TestCase):
 def test_core_source_geometry(self):
  r=original();a=r['candidate']['packet']['core'];b=derive(a)
  self.assertEqual(a['stair'],b['stair']);self.assertEqual(a['lift'],b['lift']);self.assertEqual(len(b['lobby']),1);self.assertNotEqual(a['unit_ownership'],b['unit_ownership'])
 def test_initial366_incompatible(self):
  c=derive(original()['candidate']['packet']['core']);p={'entry_x':{'A':'15.225'},'slide_direction':{'A':1}}
  with self.assertRaisesRegex(ValueError,'RAIL'):assert_notch_entry(c,p)
 def test_preserve_input_and_ownership(self):
  m=original()['candidate']['model']
  for key in('inputs','ownership','bedfloor'):
   x=copy.deepcopy(m)
   if key=='inputs':x['inputs'][0]='25'
   elif key=='ownership':x['units'][0]['ownership']=[]
   else:x['units'][0]['rooms']['bed1']=[]
   with self.assertRaises(ValueError):protect(m,x,ownership_equal=True)
 def test_notch_source_mismatch(self):
  a=copy.deepcopy(original()['candidate']['packet']['core']);a['lobby'][1][0]='999'
  with self.assertRaises(ValueError):derive(a)
if __name__=='__main__':unittest.main()
