import copy,json,unittest
from pathlib import Path
from kitchen_closure import evaluate,digest
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0]
 def args(self):return [copy.deepcopy(self.r[k])for k in('central_envelope','central_fresh_review','source_groups285')]
 def test_actual(self):
  a=self.args();h=digest(a);r=evaluate(*a);self.assertEqual(r['verdict'],'PASS_SCOPED_ESSENTIAL_KITCHEN_RELATIONS',r);self.assertFalse(r['parent_complete']);self.assertEqual(len(r['evidence']['relations']),4);self.assertEqual(digest(a),h)
 def test_stale_model(self):
  a=self.args();a[0]['packet']['world_model']['status']='changed';self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_stale_candidate(self):
  a=self.args();a[0]['candidate_id']='changed';self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_source_unknown(self):
  a=self.args();rs=a[1]['raw_fresh_report']['rule_contract_evidence']['requirements'];next(r for r in rs if r['requirement_id']=='kitchen_essential_operation')['status']='UNKNOWN';self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_group_tamper(self):
  a=self.args();a[2]['rows'][0]['witness_hash']='0'*64;self.assertEqual(evaluate(*a)['verdict'],'UNKNOWN')
 def test_budget(self):self.assertEqual(evaluate(*self.args(),seconds=0)['verdict'],'UNKNOWN')
if __name__=='__main__':unittest.main()
