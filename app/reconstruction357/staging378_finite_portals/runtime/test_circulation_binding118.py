import unittest,json
import named_checks118 as named
import core_circulation_scope118 as core
class Binding(unittest.TestCase):
 def test_registration(self):
  self.assertIs(named.ADAPTERS['long_corridor_necessity'],core.evaluate)
  self.assertIs(named.APPLICABILITY_ADAPTERS['long_corridor_necessity'],core.applicability)
  self.assertIs(named.adapters_for_workflow(None)['long_corridor_necessity'],core.evaluate)
 def test_pending_preserved(self):
  with open('evidence/finish_threshold118_saved_geometry.json')as f:m=json.load(f)['model']
  self.assertIs(core.applicability(m)['witness']['applies'],True)
  r=named.ADAPTERS['long_corridor_necessity'](m)
  self.assertNotEqual(r['status'],'PASS_LIMITED')
  self.assertIn('INTERNAL_CIRCULATION_COMPARATIVE_NECESSITY_NOT_ESTABLISHED',r['witness']['pending'])
if __name__=='__main__':unittest.main()
