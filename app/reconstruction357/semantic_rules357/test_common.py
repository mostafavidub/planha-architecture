import copy,json,unittest
from pathlib import Path
import common
P=Path(__file__).resolve().parents[1]/'actual_run/actual_response.json'
class Binding(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  x=json.loads(P.read_text());cls.m=x['selected'][0]['model'];cls.r=x['central_fresh_reviews'][0]['central_fresh_review']['raw_fresh_report']
 def test_real_recovered_identity(self):self.assertEqual(len(common.rows(self.m,self.r)),38)
 def test_stale(self):
  r=copy.deepcopy(self.r);r['model_hash']='wrong'
  with self.assertRaisesRegex(ValueError,'RAW_MODEL_BINDING'):common.rows(self.m,r)
 def test_duplicate(self):
  r=copy.deepcopy(self.r);rs=r['rule_contract_evidence']['requirements'];rs.append(rs[0])
  with self.assertRaisesRegex(ValueError,'DUPLICATE'):common.rows(self.m,r)
 def test_method_tamper(self):
  r=copy.deepcopy(self.r);r['rule_contract_evidence']['requirements'][0]['method']['code_sha256']='fake'
  with self.assertRaisesRegex(ValueError,'METHOD_BINDING'):common.rows(self.m,r)
 def test_missing(self):
  r=copy.deepcopy(self.r);r['rule_contract_evidence']['requirements'].pop()
  with self.assertRaisesRegex(ValueError,'INVENTORY'):common.rows(self.m,r)
 def test_wrong_contract(self):
  r=copy.deepcopy(self.r);r['rule_contract_evidence']['contract_hash']='fake'
  with self.assertRaisesRegex(ValueError,'CONTRACT_MODEL_BINDING'):common.rows(self.m,r)
if __name__=='__main__':unittest.main()
