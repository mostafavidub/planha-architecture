import json,unittest,copy
from pathlib import Path
from group_readsets365 import build
R=Path(__file__).resolve().parents[1]
class Group365(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.r=json.loads((R/'staging365_balanced_portals/actual365.json').read_text());c.v=json.loads((R/'review365_balanced_source_validation/result.json').read_text())
 def test_current_eight_rows_and_explicit_unsupported_old_network(self):
  o=build(self.r,self.v);self.assertEqual(sum(x['verdict']=='SCOPED_PASS'for x in o['groups']['rows']),8);self.assertEqual(o['network']['reason'],'NETWORK288_UNVERIFIED:NETWORK288_SOURCE_ENTRY_INSTALLATION');self.assertFalse(o['live_authority'])
 def test_old_fresh_blocked(self):
  with self.assertRaises(ValueError):build(self.r,json.loads((R/'review362_source_validation/result.json').read_text()))
 def test_tampered_raw_blocked(self):
  v=copy.deepcopy(self.v);v['raw_report']['errors']=['fake']
  with self.assertRaises(ValueError):build(self.r,v)
 def test_cross_profile_blocked(self):
  with self.assertRaises(ValueError):build(self.r,self.v,source_profile='SOURCE362')
if __name__=='__main__':unittest.main()
