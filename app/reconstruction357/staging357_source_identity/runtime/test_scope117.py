"""Synthetic reducer tests only, never evidence that a physical plan passes."""
import unittest
from scope117 import reduce_scope117,EXCLUDED
class Scope(unittest.TestCase):
 def report(self,**kw):return dict(checker_version='GENERAL117_TEST_ONLY',errors=[],pending=list(EXCLUDED),status='NOT_EVALUATED',**kw)
 def test_exact_three_retained_as_unknown(self):
  r=reduce_scope117(self.report());self.assertTrue(r['eligible_for_draft_export']);self.assertEqual(set(r['not_evaluated']),set(EXCLUDED));self.assertFalse(r['accepted'])
 def test_mandatory_pending_blocks(self):
  r=self.report();r['pending']+=['DOOR_OPERATION_NOT_EVALUATED:A.entry','PRIVACY_ACTUAL_OPEN_DOOR_STATE_MISSING'];self.assertFalse(reduce_scope117(r)['eligible_for_draft_export'])
 def test_physical_error_blocks(self):
  r=self.report();r['errors']=[{'code':'WINDOW_ADJACENT_FIXTURE_PROJECTION_BLOCKED'}];self.assertEqual(reduce_scope117(r)['status'],'FAIL')
 def test_no_prefix_wildcards(self):
  r=self.report();r['pending']+=['SERVICE_VENTILATION_NOT_EVALUATED:MANDATORY_CUSTOM'];self.assertFalse(reduce_scope117(r)['eligible_for_draft_export'])
 def test_old_report_rejected(self):
  r=self.report();r['checker_version']='GENERAL116_OLD'
  with self.assertRaises(ValueError):reduce_scope117(r)
if __name__=='__main__':unittest.main()
