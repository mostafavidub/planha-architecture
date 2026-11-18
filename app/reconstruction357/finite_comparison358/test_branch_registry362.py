import unittest,copy
from unittest.mock import patch
import branch_registry362 as b
class Tests(unittest.TestCase):
 def test_actual_domain(self):
  r=b.build();self.assertEqual(r['active_dispatch_count'],12);self.assertTrue(r['branch_enumeration_closed']);self.assertFalse(r['q04_comparison_closed']);self.assertFalse(r['parent_acceptance'])
 def test_historical_unknown_preserved(self):
  n=b.notch_lineage();self.assertEqual(n['historical_attempt']['raw_status'],'NOT_EVALUATED');self.assertTrue(n['historical_attempt']['retained']);self.assertEqual(n['current_attempt']['state'],'FRESH_EVALUATED_INTRINSIC_ELIGIBILITY_PENDING')
 def test_wrong_parent_rejected(self):
  original=b.artifact
  def bad(p):
   a,h=original(p)
   if p=='staging362_core_notch/actual362.json':a=copy.deepcopy(a);a['trace']['parent_model_digest']='not_same_branch'
   return a,h
  with patch.object(b,'artifact',bad),self.assertRaises(AssertionError):b.notch_lineage()
 def test_unknown_search_not_hidden(self):
  r=b.build_active_registry();r['branches'][0]['status']='NOT_ATTEMPTED_BUDGET_CHECKPOINT'
  with patch.object(b,'build_active_registry',return_value=r):
   out=b.build();self.assertFalse(out['branch_enumeration_closed']);self.assertIn(r['branches'][0]['id'],out['unresolved_active_dispatch_ids'])
if __name__=='__main__':unittest.main()
