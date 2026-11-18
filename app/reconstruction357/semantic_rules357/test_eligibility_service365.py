import unittest,json,copy
from pathlib import Path
from eligibility_intrinsic_service365 import evaluate,_reduce,REGISTRY
P=Path(__file__).resolve().parent;R=P.parent
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((R/'staging365_service_grammar/candidate365.json').read_text());c.v=json.loads((R/'review365_service_source_validation/result.json').read_text())
 def test_record_tamper(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['inputs'][0]='27';self.assertFalse(evaluate(r,self.v)['eligible'])
 def test_foreign_profile(self):self.assertFalse(evaluate(self.r,self.v,source_profile='SOURCE_BALANCED365')['eligible'])
 def test_foreign_result(self):self.assertFalse(evaluate(self.r,json.loads((R/'review365_balanced_source_validation/result.json').read_text()))['eligible'])
 def test_missing_each(self):
  base=[{'id':x[0],'verdict':'PASS'}for x in REGISTRY]
  for i in range(18):
   r=copy.deepcopy(base);r[i]['verdict']='UNKNOWN';self.assertEqual(_reduce(r),'UNKNOWN');self.assertEqual(_reduce(base[:i]+base[i+1:]),'UNKNOWN')
 def test_duplicate(self):
  r=[{'id':x[0],'verdict':'PASS'}for x in REGISTRY];r[-1]=r[0];self.assertEqual(_reduce(r),'UNKNOWN')
 def test_stored_actual_scope(self):
  r=json.loads((P/'eligibility_intrinsic_service_actual365.json').read_text());self.assertEqual(r['verdict'],'PASS');self.assertEqual(len(r['rows']),18)
  for k in ('live_authority','repair_authority','delivery_allowed','parent_complete','new_fresh_execution'):self.assertFalse(r[k])
if __name__=='__main__':unittest.main()
