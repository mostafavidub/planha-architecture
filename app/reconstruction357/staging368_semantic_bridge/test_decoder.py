"""Synthetic decoder content tests, never evidence of a new checker run."""
import unittest,json,copy
from pathlib import Path
from current_run import _references,decode_current_review
class Decoder(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.reg,cls.cap=_references();p=cls.reg['members']['joint']['paths'];cls.r=json.loads(cls.cap[p['record']]);cls.f=json.loads(cls.cap[p['fresh']])
 def run_decode(self,f):return decode_current_review(self.r,f,'joint',self.reg,self.cap)
 def fail(self):
  f=copy.deepcopy(self.f);row=f['raw_report']['rule_contract_evidence']['requirements'][0];row['status']='FAIL';row['evidence']={'status':'FAIL','witness':{'synthetic':'counterexample'}};f['raw_report'].update(status='FAIL',errors=[{'code':'RULE_FAILED','requirement_id':row['requirement_id'],'witness':row['evidence']['witness']}]);return f
 def test_reference_content_not_newrun(self):self.assertEqual(self.run_decode(self.f)['status'],'PHYSICAL_SCOPED_REVIEW_COMPLETE')
 def test_bound_synthetic_fail(self):self.assertEqual(self.run_decode(self.fail())['status'],'REJECTED_UNSUPPORTED_REDESIGN')
 def test_missing_witness(self):
  f=self.fail();f['raw_report']['errors'][0]['witness']={}
  with self.assertRaises(ValueError):self.run_decode(f)
 def test_tampered_method(self):
  f=self.fail();f['raw_report']['rule_contract_evidence']['requirements'][0]['method']['name']='fake'
  with self.assertRaises(ValueError):self.run_decode(f)
 def test_empty_fail(self):
  f=self.fail();f['raw_report']['errors']=[]
  with self.assertRaises(ValueError):self.run_decode(f)
 def test_not_evaluated(self):
  f=copy.deepcopy(self.f);f['raw_report']['status']='NOT_EVALUATED';self.assertEqual(self.run_decode(f)['status'],'UNKNOWN')
 def test_registry_not_prebuilt(self):
  f=self.fail();f['expected_method_registry']['built_before_evaluate']=False
  with self.assertRaises(ValueError):self.run_decode(f)
 def test_unrecognized_status(self):
  f=copy.deepcopy(self.f);f['raw_report']['status']='SUCCESS'
  with self.assertRaises(ValueError):self.run_decode(f)
if __name__=='__main__':unittest.main()
