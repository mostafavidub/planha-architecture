import unittest
from translated_validator import translated,verify,F
class Tests(unittest.TestCase):
 def test_exact_translation(self):self.assertEqual(translated(['0','0','2','3'],['1/3','1/7'],'A','28'),[F('1/3'),F('1/7'),F('7/3'),F('22/7')])
 def test_reflection(self):self.assertEqual(translated(['0','0','2','3'],['1','2'],'B','28'),[F(1),F(23),F(3),F(26)])
 def test_missing_not_pass(self):self.assertEqual(verify({},{} )['status'],'FAIL_BINDING')
 def test_forged_legacy_schema(self):self.assertEqual(verify({}, {'schema':'TRANSLATED_PRIVATE354_SOURCE_TRACE_V1'})['status'],'FAIL_BINDING')
if __name__=='__main__':unittest.main()
