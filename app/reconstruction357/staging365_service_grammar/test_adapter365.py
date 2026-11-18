"""Pure guard/control-flow tests only; reconstruction seam mocked, no solve/build."""
import unittest,copy
from unittest.mock import patch
import adapter365 as a
class Tests(unittest.TestCase):
 def test_exact_request(self):
  self.assertTrue(a.validate_raw({'W':'26','L':'28','n':2,'requested_count':2}))
 def test_raw_matrix(self):
  raw={'W':'26','L':'28','n':2,'requested_count':2}
  for k,values in {'W':[26,'26.0','27',None], 'L':[28,'28.0','29',None], 'n':[True,2.0,'2',1], 'requested_count':[True,2.0,'2',1]}.items():
   for v in values:
    r=dict(raw);r[k]=v
    with self.subTest(k=k,v=v),self.assertRaises(ValueError):a.validate_raw(r)
  for r in [None,[],{},dict(raw,extra=1)]:
   with self.assertRaises(ValueError):a.validate_raw(r)
 def fixture(self):
  c={'model_digest':'model'}
  t={'schema':a.SCHEMA,'source_inventory':{'x':'sha'},'raw':{'W':'26','L':'28','n':2,'requested_count':2},'proposal':{},'candidate_digest':a.digest(c),'model_digest':'model','anchor_contract':{'bath':{'x':'1'}}}
  return t,{'candidate':c,'trace':copy.deepcopy(t)}
 def test_fulltrace_control_positive(self):
  t,o=self.fixture()
  with patch.object(a,'inventory',return_value={'x':'sha'}),patch.object(a,'construct',return_value=o):self.assertEqual(a.replay(t),o)
 def test_anchor_extra_and_type_tamper(self):
  for kind in ('anchor','extra','type'):
   t,o=self.fixture()
   if kind=='anchor':t['anchor_contract']['bath']['x']='2'
   elif kind=='extra':t['unregistered_claim']=True
   else:t['raw']['n']=2.0
   with patch.object(a,'inventory',return_value={'x':'sha'}),patch.object(a,'construct',return_value=o),self.assertRaises(ValueError):a.replay(t)
 def test_source_drift(self):
  t,o=self.fixture()
  with patch.object(a,'inventory',return_value={'x':'new'}),patch.object(a,'construct')as c,self.assertRaises(ValueError):a.replay(t)
  c.assert_not_called()
if __name__=='__main__':unittest.main()
