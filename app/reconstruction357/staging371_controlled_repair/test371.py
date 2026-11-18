"""Pure gate tests against copies of pinned evidence; no constructor/fresh run."""
import copy,json,unittest
from pathlib import Path
from operator371 import validate_failure,propose,digest
A=Path(__file__).resolve().parents[2]/'review369_current_family_actual_v1'
class GateTests(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((A/'fixture_record.json').read_text());self.f=json.loads((A/'fresh_first.json').read_text());self.b=json.loads((A/'fixture_binding.json').read_text())
 def sync(self):self.b['fresh_digest']=digest(self.f)
 def test_bound_collateral_allows_proposal_only(self):
  plan=propose(self.r,self.f,self.b)
  self.assertEqual(plan['status'],'RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED')
  self.assertEqual(plan['before_raw_report'],self.f['raw_report']);self.assertFalse(plan['accepted']);self.assertFalse(plan['delivery_allowed'])
 def test_no_collision_denied(self):
  self.f['raw_report']['errors']=[e for e in self.f['raw_report']['errors']if e['code']!='FIXTURE_COLLISION'];self.sync()
  with self.assertRaisesRegex(ValueError,'DIRECT_COLLISION'):validate_failure(self.r,self.f,self.b)
 def test_pending_denied(self):
  self.f['raw_report']['pending']=['UNKNOWN'];self.sync()
  with self.assertRaisesRegex(ValueError,'UNAMBIGUOUS'):validate_failure(self.r,self.f,self.b)
 def test_unknown_provenance_denied(self):
  self.f['provenance']['verified']=False;self.sync()
  with self.assertRaisesRegex(ValueError,'PROVENANCE'):validate_failure(self.r,self.f,self.b)
 def test_stale_provenance_denied(self):
  self.f['provenance']['model_hash']='stale';self.sync()
  with self.assertRaisesRegex(ValueError,'PROVENANCE_BINDING'):validate_failure(self.r,self.f,self.b)
 def test_stale_review_denied(self):
  self.b['review_id']='other'
  with self.assertRaisesRegex(ValueError,'PROVENANCE_BINDING'):validate_failure(self.r,self.f,self.b)
 def test_extra_collision_denied(self):
  self.f['raw_report']['errors'].append({'code':'FIXTURE_COLLISION','fixtures':['sofa1','sofa2']});self.sync()
  with self.assertRaisesRegex(ValueError,'SAME_PAIR'):validate_failure(self.r,self.f,self.b)
 def test_missing_witness_denied(self):
  self.f['raw_report']['errors'].pop(0);self.sync()
  with self.assertRaisesRegex(ValueError,'WITNESS_COUNT'):validate_failure(self.r,self.f,self.b)
 def test_prior_raw_unknown_retained(self):
  plan=propose(self.r,self.f,self.b)
  self.assertEqual(plan['before_raw_report']['original_pending'],['VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED'])
class ComparisonTests(unittest.TestCase):
 def test_error_removal_permitted(self):
  from verify371 import witness_delta
  self.assertFalse(any(witness_delta({'errors':[{'code':'X'}]},{'errors':[]}).values()))
 def test_changed_nested_witness_conservative_block(self):
  from verify371 import witness_delta
  self.assertTrue(witness_delta({'errors':[{'code':'X','witness':1}]},{'errors':[{'code':'X','witness':2}]})['errors'])
 def test_duplicate_error_regression_block(self):
  from verify371 import witness_delta
  e={'code':'X'}
  self.assertTrue(witness_delta({'errors':[e]},{'errors':[e,e]})['errors'])
 def test_new_unknown_block(self):
  from verify371 import witness_delta
  self.assertTrue(witness_delta({'original_pending':[]},{'original_pending':['UNKNOWN']})['original_pending'])
if __name__=='__main__':unittest.main()
