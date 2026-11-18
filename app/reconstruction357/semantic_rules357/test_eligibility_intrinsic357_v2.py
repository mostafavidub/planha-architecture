import unittest,json,copy
from pathlib import Path
import eligibility_intrinsic357_v2 as e
P=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  x=json.loads((P/'actual_run/actual_response.json').read_text());cls.b=x['selected'][0];cls.br=x['central_fresh_reviews'][0];cls.n=json.loads((P/'staging357_comparative/attached_service_final357.json').read_text());cls.nr=json.loads((P/'review357_source_identity/result.json').read_text())
 def test_baseline_exact_gate(self):
  load,pins=e._loader('SOURCE351');x=e._view(self.b,self.br,'SOURCE351',load,pins);self.assertFalse(x['live_authority']);self.assertEqual(x['groups']['model_hash'],pins['baseline']['model_digest'])
 def test_baseline_stale(self):
  r=copy.deepcopy(self.br);r['central_fresh_review']['accepted']=True
  self.assertFalse(e.evaluate(self.b,r,source_profile='SOURCE351')['eligible'])
 def test_profile_not_interchangeable(self):
  self.assertFalse(e.evaluate(self.n,self.nr,source_profile='SOURCE351')['eligible']);self.assertFalse(e.evaluate(self.b,self.br,source_profile='SOURCE_IDENTITY357')['eligible'])
 def test_unregistered358(self):self.assertFalse(e.evaluate(self.n,self.nr,source_profile='SOURCE358')['eligible'])
 def test_missing_one_and_duplicates(self):
  rows=[{'id':k,'verdict':'PASS'}for k,_,_ in e.REGISTRY]
  for i in range(18):
   x=copy.deepcopy(rows);x[i]['verdict']='UNKNOWN';self.assertEqual(e._reduce(x),'UNKNOWN')
  rows[-1]=rows[0];self.assertEqual(e._reduce(rows),'UNKNOWN')
 def test_no_final_comparison_dependency(self):
  deps=' '.join(k for _,_,k in e.REGISTRY)
  self.assertNotIn('long_corridor_necessity',deps);self.assertNotIn('q11_functional_boundary',deps)
if __name__=='__main__':unittest.main()
