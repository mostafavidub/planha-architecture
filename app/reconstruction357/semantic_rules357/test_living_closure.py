import json,copy,unittest
from pathlib import Path
from living_closure import evaluate,digest
class Living(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0]
 def args(self):return [copy.deepcopy(self.r[k])for k in('central_envelope','central_fresh_review','source_groups285')]
 def test_actual_intrinsic(self):
  a=self.args();h=digest(a);o=evaluate(*a);self.assertEqual(o['verdict'],'PASS_SCOPED_INTRINSIC_LIVING',o);self.assertFalse(o['parent_complete']);self.assertEqual(digest(a),h)
 def test_candidate_tamper(self):
  a=self.args();a[0]['candidate_id']='TEST_ONLY_CHANGED';self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_group_tamper(self):
  a=self.args();a[2]['rows'][0]['row_hash']='0'*64;self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_unproven(self):
  a=self.args();a[2]['rows'][0]['verdict']='UNKNOWN';self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_budget(self):self.assertEqual(evaluate(*self.args(),seconds=0)['verdict'],'UNKNOWN')
if __name__=='__main__':unittest.main()
