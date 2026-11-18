import json,copy,unittest
from pathlib import Path
from core_comparison_audit118 import compare,applicability
from circulation_named_audit118 import private_grouping
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads((Path(__file__).parent/'evidence/compact118_reassembled_actual.json').read_text())['model']
 def test_actual_bounded(self):self.assertEqual(compare(self.m)['status'],'PASS_LIMITED')
 def test_no_other_input_transfer(self):
  m=copy.deepcopy(self.m);m['inputs'][0]='19';self.assertEqual(compare(m)['status'],'NOT_EVALUATED')
 def test_core_resize(self):
  m=copy.deepcopy(self.m);m['common_spaces']['lift'][2]='14';self.assertEqual(compare(m)['status'],'FAIL')
 def test_actual_pair(self):self.assertEqual(private_grouping(self.m)['status'],'PASS_LIMITED')
 def test_nonbed_through_pair(self):
  m=copy.deepcopy(self.m);m['units'][0]['routes']['WC_front']=[['11.4','1'],['11.4','3']];self.assertEqual(private_grouping(m)['status'],'NOT_EVALUATED')
 def test_conditional_applies(self):self.assertTrue(applicability(self.m)['witness']['applies'])
if __name__=='__main__':unittest.main()
