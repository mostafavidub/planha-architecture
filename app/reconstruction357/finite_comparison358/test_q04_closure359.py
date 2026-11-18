import unittest,json,copy
from q04_closure359 import *
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text());cls.f=json.loads((ROOT/'review359_source_validation/result.json').read_text());cls.actual=json.loads((HERE/'q04_closure_actual359.json').read_text())
 def test_current_actual(self):
  x=evaluate(self.r,self.f);self.assertEqual(x['verdict'],'UNKNOWN');self.assertIn('CORE_NOTCH360_FIXED_LINEAGE',x['unknown_reasons']);self.assertEqual(x['current_gate']['verdict'],'PASS');self.assertFalse(x['all12_accepted'])
 def test_tail_missing_role_is_not_pass(self):
  p=copy.deepcopy(self.actual['purpose']);p['units'][0]['untargeted_terminal_extensions']=[{'synthetic_tail':True}];self.assertFalse(purpose_complete(p))
 def test_unproved_margin_not_pass(self):
  p=copy.deepcopy(self.actual['purpose']);p['units'][0]['source_connector_margin_proof']['all_residual_cells_source_bound']=False;self.assertFalse(purpose_complete(p))
 def test_tie_not_strict(self):self.assertEqual(negative(self.r['candidate']['model'],self.r['candidate']['model'])['dominance'],'UNKNOWN')
 def test_tamper_gate_fails_closed(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['inputs']=['5','5',2];x=evaluate(r,self.f);self.assertEqual(x['verdict'],'UNKNOWN')
if __name__=='__main__':unittest.main()
