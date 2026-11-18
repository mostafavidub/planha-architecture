import unittest,json,copy
from cohort367 import ROOT,inventory,MEMBERS
class Tests(unittest.TestCase):
 def setUp(self):self.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text())
 def test_all_eight_retained(self):
  x=inventory(self.r,'joint367');self.assertEqual(len(x['members']),8);self.assertFalse(x['domain_closed']);self.assertTrue(all(r['eligibility'].startswith('PENDING')for r in x['members']))
 def test_missing_current_id(self):
  with self.assertRaises(ValueError):inventory(self.r,'UNKNOWN')
 def test_forged_record(self):
  self.r['accepted']=True
  with self.assertRaises(ValueError):inventory(self.r,'joint367')
 def test_new_branch_explicit(self):self.assertIn('joint367',dict(MEMBERS))
if __name__=='__main__':unittest.main()
