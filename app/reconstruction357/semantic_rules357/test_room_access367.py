import unittest,json,copy
from unittest.mock import patch
from pathlib import Path
from intrinsic_access367 import evaluate as access
from closure_room_program367 import evaluate,bundle_inventory
from common import digest
BASE=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((BASE/'review367_joint_attempt2/actual367.json').read_text());cls.r=json.loads((BASE/'review367_joint_source_validation_attempt2/result.json').read_text());cls.m=cls.c['candidate']['model'];cls.raw=cls.r['raw_report']
 def test_real_access(self):
  v=access(self.m,self.raw);self.assertEqual(v['verdict'],'PASS_SCOPED_INTRINSIC_ACCESS');self.assertFalse(v['parent_complete'])
 def test_room_no_parent_reentry(self):
  with patch('engine.evaluate',side_effect=AssertionError('NO_PARENT_REENTRY')):
   v=evaluate(self.c,self.r)
  self.assertTrue(v['proofscopecomplete']);self.assertFalse(v['parent_complete']);self.assertFalse(v['fresh_executed'])
 def test_wrong_profile(self):self.assertEqual(access(self.m,self.raw,'SOURCE_IDENTITY357')['verdict'],'UNKNOWN')
 def test_stale_panel(self):
  m=copy.deepcopy(self.m);m['operations']['doors'][0]['open_panel'][0]='0';self.assertEqual(access(m,self.raw)['verdict'],'UNKNOWN')
 def test_modified_trace(self):
  c=copy.deepcopy(self.c);c['trace']['parent_record_digest']='tampered';self.assertFalse(evaluate(c,self.r)['proofscopecomplete'])
 def test_extra_bedfixture(self):
  m=copy.deepcopy(self.m);m['units'][0]['fixtures']['bed1.fake']=['0','0','1','1'];rs={x['requirement_id']:copy.deepcopy(x)for x in self.raw['rule_contract_evidence']['requirements']}
  # Isolated helper seam only; public source-profile binding is not changed.
  rs['fixture_inventory_use']['evidence']['witness']['capacity']['evidence']['model_hash']=digest(m)
  self.assertRaises(ValueError,bundle_inventory,m,rs)
if __name__=='__main__':unittest.main()
