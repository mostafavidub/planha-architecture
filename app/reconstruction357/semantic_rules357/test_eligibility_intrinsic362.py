import unittest,copy
import eligibility_intrinsic362 as e
class Tests(unittest.TestCase):
 def test_missing_each_blocks(self):
  rows=[{'id':k,'verdict':'PASS'}for k,_,_ in e.REGISTRY]
  for i in range(18):
   x=copy.deepcopy(rows);x[i]['verdict']='UNKNOWN';self.assertEqual(e._reduce(x),'UNKNOWN');self.assertEqual(e._reduce(rows[:i]+rows[i+1:]),'UNKNOWN')
 def test_duplicate(self):
  rows=[{'id':k,'verdict':'PASS'}for k,_,_ in e.REGISTRY];rows[-1]=rows[0];self.assertEqual(e._reduce(rows),'UNKNOWN')
 def test_counterproof(self):
  rows=[{'id':k,'verdict':'PASS'}for k,_,_ in e.REGISTRY];rows[5]['verdict']='FAIL';self.assertEqual(e._reduce(rows),'FAIL')
 def test_unregistered_profiles(self):
  for p in ('SOURCE351','SOURCE_IDENTITY357','UNKNOWN'):
   x=e.evaluate({}, {}, source_profile=p);self.assertFalse(x['eligible']);self.assertEqual(x['verdict'],'UNKNOWN')
 def test_no_comparative_cycle(self):
  deps=' '.join(k for _,_,k in e.REGISTRY)
  for x in ('q11_functional_boundary','long_corridor_necessity','geometric_diversity','worst_unit_function'):self.assertNotIn(x,deps)
class GateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import json
  from pathlib import Path
  p=Path(__file__).resolve().parents[1];cls.record=json.loads((p/'staging362_core_notch/actual362.json').read_text());cls.result=json.loads((p/'review362_source_validation/result.json').read_text());cls.other=json.loads((p/'review357_source_identity/result.json').read_text())
 def test_stale_model(self):
  r=copy.deepcopy(self.record);r['candidate']['model']['program']['bedrooms_per_unit']=2
  x=e.evaluate(r,self.result);self.assertFalse(x['eligible']);self.assertFalse(x['live_authority']);self.assertEqual(x['verdict'],'UNKNOWN')
 def test_cross_result(self):self.assertFalse(e.evaluate(self.record,self.other)['eligible'])
 def test_fake_proof(self):self.assertFalse(e.evaluate({'proof':True},{'PASS':True})['eligible'])
if __name__=='__main__':unittest.main()

