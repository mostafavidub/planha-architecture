import unittest,copy
from unittest.mock import patch
import checker114 as c
class Compare(unittest.TestCase):
 def test_no_waive(self):
  for pending,errors,status in [(['RULE_NOT_EVALUATED:long_corridor_necessity'],[],'PASS_NONCIRCULAR_PHYSICAL_SCOPED'),(['RULE_NOT_EVALUATED:long_corridor_necessity','Q11_MISSING'],[],'NOT_EVALUATED'),(['RULE_NOT_EVALUATED:long_corridor_necessity'],[{'code':'COLLISION'}],'FAIL')]:
   original={'pending':pending,'errors':errors,'status':'NOT_EVALUATED','model_hash':'m'}
   with patch.object(c,'_evaluate_impl',return_value=copy.deepcopy(original))as impl:r=c.evaluate_for_circulation_comparison({})
   self.assertEqual(r['status'],status);self.assertEqual(r['pending'],pending);self.assertEqual(r['errors'],errors);self.assertFalse(r['eligible_for_draft_export']);self.assertTrue(impl.call_args.kwargs['comparison_only'])
if __name__=='__main__':unittest.main()
