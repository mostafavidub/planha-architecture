import unittest
from clamp_geometry359 import clamp
class Tests(unittest.TestCase):
 def kwargs(self):return dict(hall=['0','4','10','5'],connector_regions=[['2','0','3','4'],['7','0','8','4']],interface=['4.5','4.65','5.5','5.35'],required_paths={'a':[['5','5'],['5','4.5'],['2.5','4.5'],['2.5','1']]},operation_envelopes={},body='.8')
 def test_generic_connector_preservation(self):
  x=clamp(**self.kwargs());self.assertEqual(x['hall'],['2','4','8','5']);self.assertFalse(x['accepted'])
 def test_operation_blocks_trim(self):
  k=self.kwargs();k['operation_envelopes']={'actual_actor':['0.5','4','1.5','5']};self.assertEqual(clamp(**k)['hall'][0],'1/2')
 def test_profile_not_hardcoded(self):
  k=self.kwargs();k['body']='2';self.assertEqual(clamp(**k)['hall'][0],'3/2')
 def test_missing_not_empty(self):
  k=self.kwargs();k['required_paths']={}
  with self.assertRaises(ValueError):clamp(**k)
 def test_no_diagonal(self):
  k=self.kwargs();k['required_paths']={'x':[['1','1'],['2','2']]}
  with self.assertRaises(ValueError):clamp(**k)
if __name__=='__main__':unittest.main()
