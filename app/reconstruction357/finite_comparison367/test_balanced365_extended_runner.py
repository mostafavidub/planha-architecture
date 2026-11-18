import unittest,json,copy
from unittest.mock import patch
from types import SimpleNamespace
import balanced365_extended_runner as r
R=json.loads((r.ROOT/'staging365_balanced_portals/actual365.json').read_text());F=json.loads((r.ROOT/'review365_balanced_source_validation/result.json').read_text());A=json.loads((r.ROOT/'finite_comparison367/balanced365_extended_actual.json').read_text())
class Tests(unittest.TestCase):
 def test_current_actual(self):
  x=r.evaluate(R,F);self.assertEqual(x['verdict'],'PASS_SCOPED_FINITE_Q04_BALANCED365_EXPANDED367');self.assertEqual(x['new367_comparison']['dominance'],'FALSE');self.assertEqual(x['remaining'],[]);self.assertEqual(x['draft366_property']['status'],'UNASSESSED_NO_BUILD_NO_FRESH')
 def test_caller_fresh_not_receipt(self):
  f=copy.deepcopy(F);f['accepted']=True
  with patch.object(r.subprocess,'run',return_value=SimpleNamespace(stdout=json.dumps(A))):
   with self.assertRaises(ValueError):r.evaluate(R,f)
 def test_wrong_model_child(self):
  a=copy.deepcopy(A);a['model_digest']='other'
  with patch.object(r.subprocess,'run',return_value=SimpleNamespace(stdout=json.dumps(a))):
   with self.assertRaises(ValueError):r.evaluate(R,F)
 def test_manifest_drift_before_child(self):
  with patch.object(r,'MANIFEST_SHA','wrong'),patch.object(r.subprocess,'run') as child:
   with self.assertRaises(ValueError):r.evaluate(R,F)
   child.assert_not_called()
if __name__=='__main__':unittest.main()
