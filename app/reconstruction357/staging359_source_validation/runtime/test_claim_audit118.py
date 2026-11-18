import unittest,copy
from claim_audit118 import claim_boundary,EXPECTED
class Claim(unittest.TestCase):
 def model(self):return {'scope_declaration':dict(EXPECTED),'accepted':False,'release_allowed':False}
 def test_declaration_only(self):self.assertEqual(claim_boundary(self.model())['status'],'PASS_LIMITED')
 def test_each_unsupported_approval_rejected(self):
  for key,val in EXPECTED.items():
   m=self.model();m['scope_declaration'][key]=True if val is False else 'APPROVED';self.assertEqual(claim_boundary(m)['status'],'FAIL',key)
 def test_missing_not_pass(self):
  m=self.model();del m['scope_declaration'];self.assertEqual(claim_boundary(m)['status'],'NOT_EVALUATED')
 def test_truthy_integer_not_false(self):
  m=self.model();m['scope_declaration']['technical_approval']=0;self.assertEqual(claim_boundary(m)['status'],'FAIL')
if __name__=='__main__':unittest.main()
