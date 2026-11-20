import copy,json,sys,unittest
from pathlib import Path
from fractions import Fraction as F
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'app/local_integration'))
import single_model_p15 as p
from single_access_p15 import assess
class Contract(unittest.TestCase):
 def test_n1_ready_exact(self):
  r=p.preflight(b'{"W":"18","L":"20","n":1}');self.assertTrue(r['execution_ready']);self.assertEqual(r['raw'],p.RAW)
 def test_persian_exact(self):
  r=p.preflight('{"W":"۱۸٫۰۰","L":"۲۰","n":"1"}'.encode());self.assertTrue(r['execution_ready'])
 def test_n2_valid_unsupported(self):
  r=p.preflight(b'{"W":"18","L":"20","n":2}');self.assertTrue(r['input_valid']);self.assertFalse(r['execution_ready'])
 def test_other_dimensions_unsupported(self):
  self.assertFalse(p.preflight(b'{"W":"18.1","L":"20","n":1}')['execution_ready'])
 def test_invalid_before_producer(self):
  import search114
  with patch.object(search114,'propose',side_effect=AssertionError('NO_SOLVER'))as spy:
   for body in (b'{"W":"4.999","L":"20","n":1}',b'{"W":"18","L":"25.001","n":1}',b'{"W":"18","L":"20","n":3}',b'{"W":"18","L":"20","n":1,"requested_count":6}'):
    with self.assertRaises(ValueError):p.preflight(body)
   spy.assert_not_called()
 def test_core_built_one(self):
  c=p.core(p.RAW);self.assertEqual(set(c['units']),{'A'});self.assertEqual(set(c['entry_centers']),{'A'});self.assertEqual(set(c['unit_ownership']),{'A'})
 def test_core_exact_source_dimensions(self):
  c=p.core(p.RAW)
  for k,size in [('stair',(F('4.55'),F('2.45'))),('lift',(F('1.65'),F('1.65')))]:
   a,b,C,d=map(F,c[k]);self.assertEqual((C-a,d-b),size)
 def test_core_no_ownership_overlap(self):
  from checker114 import rect,intersects
  c=p.core(p.RAW);u=rect(c['units']['A'])
  self.assertTrue(all(not intersects(u,rect(q))for q in [c['stair'],c['lift'],*c['lobby']]))
 def test_no_implicit_pair_core(self):
  with self.assertRaises(ValueError):p.core({'W':'18','L':'20','n':2})
 def test_typed_digest(self):
  self.assertNotEqual(p.digest(1),p.digest(True));self.assertNotEqual(p.digest(1),p.digest(1.0))
  with self.assertRaises(ValueError):p.digest(float('nan'))
 def test_missing_or_pair_model_rejected(self):
  for m in ({},{'schema':p.FAMILY,'contract_version':'p15-single-v1','inputs':['18','20',2]},
            {'schema':p.FAMILY,'contract_version':'p15-single-v1','inputs':['18','20',1],'program':{'units':2}}):
   self.assertEqual(assess(m)['state'],'FAIL')
 def test_assembler_not_pair_then_filter(self):
  import single_assembler_p15 as a,inspect
  text=inspect.getsource(a.assemble)
  self.assertNotIn("('A','B')",text);self.assertNotIn('unit_proposals',text)
  self.assertNotIn("units'][:1]",text);self.assertNotIn("units'].pop",text)
if __name__=='__main__':unittest.main(verbosity=2)
