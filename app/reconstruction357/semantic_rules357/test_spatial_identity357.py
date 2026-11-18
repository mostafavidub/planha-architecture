import unittest,json,copy
from pathlib import Path
from fractions import Fraction as F
from reassess_spatial_identity357 import evaluate,ROOT
from common import digest
class IdentitySpatial(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record=json.loads((ROOT/'staging357_comparative/attached_service_final357.json').read_text());cls.review=json.loads((ROOT/'review357_source_identity/result.json').read_text());cls.out=evaluate(cls.record,cls.review)
 def test_new_model_exact_binding(self):self.assertEqual(self.out['model_hash'],digest(self.record['candidate']['model']));self.assertEqual(self.out['wall_purpose']['source_origin_record_digest'],digest(self.record))
 def test_no_parent_admission_or_new_fresh(self):
  for k in ('new_fresh_execution','live_authority','parent_complete','admission_allowed'):self.assertFalse(self.out[k])
 def test_new_extent_not_inherited_zero(self):
  for r in self.out['support']['rows']:self.assertEqual(F(r['unresolved_area_m2']),F('6.595'));self.assertEqual(F(r['reservation_claimed_union_area_m2']),F('.0448'))
 def test_sidecar_not_old_hall_pass(self):
  w=self.out['wall_purpose'];self.assertEqual(len(w['rows']),115);self.assertEqual(len(w['unjoined_host_ids']),0);self.assertEqual(sum(r['verdict'].startswith('UNKNOWN')for r in w['rows']),14)
 def test_stale_or_tampered_record_rejected(self):
  record=copy.deepcopy(self.record);record['candidate']['model']['walls']['left'][0]='.01'
  with self.assertRaises(ValueError):evaluate(record,self.review)
if __name__=='__main__':unittest.main()
