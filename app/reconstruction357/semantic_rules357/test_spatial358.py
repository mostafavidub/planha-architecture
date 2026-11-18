import unittest,json,copy
from fractions import Fraction as F
from reassess_spatial358 import evaluate,ROOT
from common import digest
class Spatial358(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text());cls.review=json.loads((ROOT/'review358_source_validation/result.json').read_text());cls.out=evaluate(cls.record,cls.review)
 def test_same_new_model(self):
  o=self.out;self.assertEqual(o['model_hash'],digest(self.record['candidate']['model']));self.assertEqual(o['wall_purpose']['model_hash'],o['model_hash']);self.assertEqual(o['support']['model_hash'],o['model_hash'])
 def test_zero_now_source_bound_not_transferred(self):
  self.assertTrue(self.out['role_proof_scope']['complete_source_sitting_prerequisite_recomputed'])
  for r in self.out['support']['rows']:self.assertEqual(F(r['unresolved_area_m2']),0);self.assertEqual(F(r['public_domain_area_m2']),F(r['body_plus_source_function_coverage_m2']));self.assertTrue(r['reservation_purpose_ledger'])
 def test_all_wall_origins_but_q04_pending(self):
  w=self.out['wall_purpose'];self.assertEqual(len(w['rows']),109);self.assertEqual(w['unjoined_host_ids'],[]);self.assertEqual(w['counts']['UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY'],8);self.assertFalse(w['parent_complete'])
 def test_357_raw_cannot_be_used(self):
  old=json.loads((ROOT/'review357_source_identity/result.json').read_text())
  with self.assertRaises(ValueError):evaluate(self.record,old)
 def test_new_model_tampering_rejected(self):
  r=copy.deepcopy(self.record);r['candidate']['model']['walls']['left'][0]='.01'
  with self.assertRaises(ValueError):evaluate(r,self.review)
 def test_no_parent_promotion_or_fresh(self):
  for k in ('new_fresh_execution','live_authority','parent_complete','admission_allowed'):self.assertFalse(self.out[k])
if __name__=='__main__':unittest.main()
