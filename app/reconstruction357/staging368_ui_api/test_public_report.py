import unittest,copy,json
from public_report import public_result
from test_qualified_binding import fixture
class Tests(unittest.TestCase):
 def test_internal_receipts_not_disclosed(self):
  x,e,r=fixture();x['semantic_receipt']={'source_path':'/private/internal/path'};x['members'][0]['quality'][0]['source_closure']={'source_path':'/private/internal/path'};old=copy.deepcopy(x)
  out=public_result(x);self.assertNotIn('/private',json.dumps(out));self.assertEqual(x,old);self.assertEqual(len(out['members'][0]['quality']),12)
 def test_rejection_keeps_codes_not_internal_witness(self):
  x={'state':'REJECTED_UNSUPPORTED_REDESIGN','current_rejection':{'kind':'joint','binding':{'candidate_id':'c'},'status':'REJECTED_UNSUPPORTED_REDESIGN','reasons':[{'code':'TEST_ONLY','witness':{'path':'/private'}}],'pending':[]}}
  out=public_result(x);self.assertEqual(out['current_rejection']['reasons'],[{'code':'TEST_ONLY'}]);self.assertNotIn('/private',json.dumps(out))
if __name__=='__main__':unittest.main()
