import unittest,copy,json
from pathlib import Path
import eligibility_intrinsic357 as e
ROOT=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 def test_every_subclaim_required(self):
  rows=[{'id':k,'verdict':'PASS'}for k,_,_ in e.REGISTRY]
  self.assertEqual(e._reduce(rows),'PASS')
  for i in range(18):
   x=copy.deepcopy(rows);x[i]['verdict']='UNKNOWN';self.assertEqual(e._reduce(x),'UNKNOWN')
   self.assertEqual(e._reduce(rows[:i]+rows[i+1:]),'UNKNOWN')
 def test_counterproof(self):
  rows=[{'id':k,'verdict':'PASS'}for k,_,_ in e.REGISTRY];rows[4]['verdict']='FAIL';self.assertEqual(e._reduce(rows),'FAIL')
 def test_duplicate_registry(self):
  rows=[{'id':k,'verdict':'PASS'}for k,_,_ in e.REGISTRY];rows[-1]=rows[0];self.assertEqual(e._reduce(rows),'UNKNOWN')
 def test_duplicate_inventory(self):
  with self.assertRaises(ValueError):e._inventory(['a','a'],lambda x:x)
 def test_comparison_not_dependency(self):
  dependencies=' '.join(k for _,_,k in e.REGISTRY)
  for x in ('long_corridor_necessity','q11_functional_boundary','geometric_diversity','worst_unit_function'):self.assertNotIn(x,dependencies)
 def test_stale_record_gate(self):
  r=json.loads((ROOT/'staging357_comparative/attached_service_final357.json').read_text());n=json.loads((ROOT/'review357_source_identity/result.json').read_text());r['trace']['accepted']=True
  x=e.evaluate(r,n);self.assertFalse(x['eligible']);self.assertFalse(x['live_authority']);self.assertEqual(x['verdict'],'UNKNOWN')
 def test_no_caller_bool(self):
  x=e.evaluate({'proof':True},{'accepted':True});self.assertFalse(x['eligible'])
if __name__=='__main__':unittest.main()
