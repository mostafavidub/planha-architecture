import unittest,json,copy
from unittest.mock import patch
from types import SimpleNamespace
import q04_runner367_v2 as r
R=json.loads((r.ROOT/'review367_joint_attempt2/actual367.json').read_text());F=json.loads((r.ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());A=json.loads((r.ROOT/'finite_comparison367/q04_actual367_v2.json').read_text())
class Tests(unittest.TestCase):
 def test_current_actual(self):
  x=r.evaluate(R,F);self.assertEqual(x['verdict'],'UNKNOWN');self.assertEqual(len(x['cohort']['members']),8);self.assertIn('BALANCED_ONLY366_CONSTRUCTIBLE_DRAFT_NOT_YET_PROPERTY_REFUTED',x['remaining'])
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
