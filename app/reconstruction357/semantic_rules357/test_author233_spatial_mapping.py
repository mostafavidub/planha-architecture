import unittest,json,copy
from pathlib import Path
from author233_spatial_mapping import evaluate
class Mapping(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  p=Path(__file__).resolve().parent;cls.e=json.loads((p.parent/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0]['central_envelope'];cls.l=json.loads((p/'living_actual357.json').read_text());cls.g=json.loads((p/'guest_actual357.json').read_text())
 def test_actual(self):
  o=evaluate(self.e,self.l,self.g);self.assertFalse(o['parent_promotion_performed']);self.assertTrue(all(r['audit_recommendation'].startswith('ELIGIBLE')for r in o['rules'].values()))
 def test_overlay_not_waived_at_trigger(self):
  e=copy.deepcopy(self.e);e['raw'].update(W='12.5',L='20');o=evaluate(e,self.l,self.g);self.assertEqual(o['rules']['Q02']['r_liv']['status'],'UNKNOWN');self.assertTrue(o['rules']['Q02']['audit_recommendation'].startswith('UNKNOWN'))
 def test_rotated_overlay_not_waived(self):
  e=copy.deepcopy(self.e);e['raw'].update(W='20',L='12.5');self.assertEqual(evaluate(e,self.l,self.g)['rules']['Q02']['r_liv']['status'],'UNKNOWN')
 def test_missing_relation(self):
  g=copy.deepcopy(self.g);g['evidence']['relations'].pop();self.assertTrue(evaluate(self.e,self.l,g)['rules']['Q06']['audit_recommendation'].startswith('UNKNOWN'))
 def test_disconnected_target(self):
  l=copy.deepcopy(self.l);l['evidence']['network']['rows'][0]['unconnected_stored_targets']=['sofa1'];self.assertTrue(evaluate(self.e,l,self.g)['rules']['Q02']['audit_recommendation'].startswith('UNKNOWN'))
if __name__=='__main__':unittest.main()
