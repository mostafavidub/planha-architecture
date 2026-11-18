import copy,json,unittest
from pathlib import Path
from guest_closure import evaluate,transformed_rect,digest
class Guest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0]
 def args(self):return[copy.deepcopy(self.r[k])for k in('central_envelope','central_fresh_review','source_groups285')]
 def test_actual_four_per_unit(self):
  a=self.args();h=digest(a);o=evaluate(*a);self.assertEqual(o['verdict'],'PASS_SCOPED_FOUR_SOURCE_GUEST_RELATIONS',o);self.assertEqual(len(o['evidence']['relations']),8);self.assertFalse(o['parent_complete']);self.assertEqual(digest(a),h)
 def test_changed_candidate(self):
  a=self.args();a[0]['candidate_id']='TEST_CHANGED';self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_changed_witness(self):
  a=self.args();a[2]['rows'][0]['witness_hash']='0'*64;self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_unknown_source(self):
  a=self.args();a[2]['rows'][0]['verdict']='UNKNOWN';self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_zero_budget(self):self.assertEqual(evaluate(*self.args(),seconds=0)['verdict'],'UNKNOWN')
 def test_nonisometric_endpoint(self):
  with self.assertRaises(ValueError):transformed_rect([0,0,1,1],{'matrix':[[2,0],[0,1]],'translation':['0','0']})
if __name__=='__main__':unittest.main()
