import unittest,json,copy
from pathlib import Path
from equivalence import compare,digest
ROOT=Path(__file__).resolve().parents[1]
class ExactReadset(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());c.f=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text())
 def setUp(self):self.r2=copy.deepcopy(self.r);self.f2=copy.deepcopy(self.f)
 def runcheck(self):return compare(self.r,self.f,self.r2,self.f2)
 def test_reference_dry_comparison_not_execution(self):o=self.runcheck();self.assertTrue(o['evidence_equivalent']);self.assertFalse(o['execution_authority']);self.assertEqual(o['raw_timing_allowlist'],[])
 def test_outer_seconds_only(self):self.f2['seconds']+=1;self.assertTrue(self.runcheck()['evidence_equivalent']);self.assertNotEqual(digest(self.f),digest(self.f2))
 def test_method_change(self):self.f2['raw_report']['rule_contract_evidence']['requirements'][0]['method']={'changed':True};self.assertRaises(ValueError,self.runcheck)
 def test_status_change(self):self.f2['raw_report']['rule_contract_evidence']['requirements'][0]['status']='UNKNOWN';self.assertRaises(ValueError,self.runcheck)
 def test_evidence_change(self):self.f2['raw_report']['rule_contract_evidence']['requirements'][0]['evidence']={};self.assertRaises(ValueError,self.runcheck)
 def test_raw_extra_even_named_time(self):self.f2['raw_report']['elapsed_seconds']=0;self.assertRaises(ValueError,self.runcheck)
 def test_outer_extra(self):self.f2['unknown_extra']=True;self.assertRaises(ValueError,self.runcheck)
 def test_registry_extra(self):self.f2['expected_method_registry']['unknown_extra']=True;self.assertRaises(ValueError,self.runcheck)
 def test_checker_not_executed(self):self.f2['fresh_checker_executed']=False;self.assertRaises(ValueError,self.runcheck)
 def test_record_policy_change(self):self.r2['trace']['policy_changed']=True;self.assertRaises(ValueError,self.runcheck)
 def test_missing_vs_null(self):
  row=next(r for r in self.f2['raw_report']['rule_contract_evidence']['requirements']if'method'not in r);row['method']=None;self.assertRaises(ValueError,self.runcheck)
 def test_no_contract_time_waiver(self):self.f2['raw_report']['rule_contract_evidence']['rows'][0]['source']['modified_time']='changed';self.assertRaises(ValueError,self.runcheck)
if __name__=='__main__':unittest.main()
