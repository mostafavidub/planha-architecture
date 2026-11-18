import unittest,json,copy
from pathlib import Path
from group_readsets_service365 import build
R=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.r=json.loads((R/'staging365_service_grammar/candidate365.json').read_text());c.v=json.loads((R/'review365_service_source_validation/result.json').read_text())
 def test_one_actual_reassessment(self):
  o=build(self.r,self.v);(R/'semantic_rules357/group_readsets_service_actual365.json').write_text(json.dumps(o,default=str))
  self.assertEqual(len(o['groups']['rows']),9);self.assertFalse(o['live_authority']);self.assertFalse(o['groups']['parent_complete'])
 def test_foreign_result(self):
  with self.assertRaises(ValueError):build(self.r,json.loads((R/'review365_balanced_source_validation/result.json').read_text()))
 def test_raw_tamper(self):
  v=copy.deepcopy(self.v);v['raw_report']['errors']=['forged']
  with self.assertRaises(ValueError):build(self.r,v)
 def test_record_tamper(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['inputs'][0]='27'
  with self.assertRaises(ValueError):build(r,self.v)
 def test_cross_profile(self):
  with self.assertRaises(ValueError):build(self.r,self.v,source_profile='SOURCE_BALANCED365')
 def test_invalid_budget(self):
  for n in (0,-1,11,True,float('nan')):
   with self.assertRaises(ValueError):build(self.r,self.v,seconds=n)
if __name__=='__main__':unittest.main()
