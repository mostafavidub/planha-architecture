import unittest,json
from pathlib import Path
from fractions import Fraction as F
from support_review import evaluate
from modules_spatial import rect,union_area,intersection
class SupportReview(unittest.TestCase):
 def test_actual_disjoint_bound_reservations(self):
  r=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0]
  o=evaluate(*[r[k]for k in('central_envelope','central_fresh_review','source_groups285')])
  self.assertEqual(o['status'],'MEASURED_CURRENT_SOURCE_SUPPORT_NOT_FINAL_ROLE_APPROVAL');self.assertFalse(o['parent_complete']);self.assertFalse(o['admission_allowed'])
  for row in o['rows']:
   self.assertEqual(F(row['pre_reservation_unresolved_area_m2']),F('0.0448'));self.assertEqual(F(row['unresolved_area_m2']),0)
   fragments=[]
   for claim in row['reservation_purpose_ledger']:
    self.assertEqual(claim['source_door_operation_row_digest'],o['source_function_rows']['door_operation']);self.assertTrue(claim['source_door_method'])
    fragments.extend(map(rect,claim['claimed_fragments']))
    self.assertEqual(union_area(list(map(rect,claim['claimed_fragments']))),F(claim['claimed_area_m2']))
   self.assertEqual(union_area(fragments),F(row['reservation_claimed_union_area_m2']))
   self.assertEqual(union_area(fragments),F('0.0448'))
   self.assertTrue(all(intersection(a,b)is None for i,a in enumerate(fragments)for b in fragments[i+1:]))
   self.assertFalse(row['region_role_complete'])
if __name__=='__main__':unittest.main()
