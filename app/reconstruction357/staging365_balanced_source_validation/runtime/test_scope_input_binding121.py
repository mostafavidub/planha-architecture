import unittest,copy,ast
from pathlib import Path
from unittest.mock import patch
import claim_audit118 as claim
import project_input_audit118 as inputs
class ScopeInput(unittest.TestCase):
 def model(self):
  tree=ast.parse(Path('assemble114.py').read_text())
  # Actual producer declaration, not a duplicate of checker EXPECTED.
  for n in ast.walk(tree):
   if isinstance(n,ast.Dict):
    for k,v in zip(n.keys,n.values):
     if isinstance(k,ast.Constant) and k.value=='scope_declaration':
      return {'scope_declaration':ast.literal_eval(v),'accepted':False,'release_allowed':False}
  self.fail('producer declaration missing')
 def test_actual_scope_without_old_light_keys(self):
  m=self.model();self.assertNotIn('daylight_sufficiency',m['scope_declaration']);self.assertEqual(claim.claim_boundary(m)['status'],'PASS_LIMITED')
 def test_approval_and_contradiction(self):
  for k in ('technical_approval','legal_approval','execution_ready','daylight_sufficiency','ventilation_sufficiency'):
   m=self.model();m['scope_declaration'][k]=True;self.assertEqual(claim.claim_boundary(m)['status'],'FAIL',k)
 def test_actual_input_protocol(self):
  r=inputs.no_hidden_project_inputs({'inputs':{'W':'18','L':'24','n':2}});self.assertEqual(r['status'],'PASS_LIMITED',r);self.assertEqual(len(r['witness']['negative_api_checks']),8)
 def test_source_change_not_transferred(self):
  with patch.dict(inputs.PINS,{'service118.py':'wrong'}):self.assertEqual(inputs.no_hidden_project_inputs({})['status'],'NOT_EVALUATED')
if __name__=='__main__':unittest.main()
