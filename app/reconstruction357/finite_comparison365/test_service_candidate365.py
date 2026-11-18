import unittest,json,copy
import service_candidate_criterion365 as s
from service_candidate_objectives365 import evaluate
R=json.loads((s.ROOT/'staging365_service_grammar/candidate365.json').read_text());V=json.loads((s.ROOT/'review365_service_source_validation/result.json').read_text())
class Tests(unittest.TestCase):
 def test_wrong_profile_fresh(self):
  f=json.loads((s.ROOT/'review365_balanced_source_validation/result.json').read_text())
  with self.assertRaises(ValueError):s.evaluate(R,f)
 def test_tampered_candidate(self):
  r=copy.deepcopy(R);r['candidate']['model']['profile']['body_m']='0.1'
  with self.assertRaises(ValueError):s.evaluate(r,V)
 def test_residual_blocks(self):self.assertFalse(s.reconcile_scope({'complete':True},{'unassigned_after_source_clearance_m2':'1911/200'}))
 def test_ownership_loss(self):self.assertFalse(s.ownership_nondecrease([[0,0,2,2]],[[0,0,1,2]]))
 def test_actual_criterion_unknown(self):
  x=s.evaluate(R,V);self.assertEqual(x['verdict'],'UNKNOWN');self.assertEqual(x['source_profile'],'SOURCE_SERVICE365')
  for u in x['against359']['evidence'][1]['units']:self.assertEqual(u['outside_entry_unassigned_m2'],'1911/200')
 def test_objective_no_promotion(self):
  x=evaluate(R,V);self.assertEqual(x['verdict'],'UNKNOWN');self.assertEqual(len(x['pairs']),6);self.assertEqual(len(x['common_bindings']),4);self.assertFalse(x['accepted'])
if __name__=='__main__':unittest.main()
