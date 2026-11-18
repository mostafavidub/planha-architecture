import unittest,json,copy
from pathlib import Path
from unittest.mock import patch
import bedroom_grouping_service365 as g
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((g.ROOT/'staging365_service_grammar/candidate365.json').read_text());c.v=json.loads((g.ROOT/'review365_service_source_validation/result.json').read_text())
 def test_foreign_record(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['inputs'][0]='27';self.assertFalse(g.evaluate(r,self.v)['proofscopecomplete'])
 def test_foreign_result(self):self.assertFalse(g.evaluate(self.r,json.loads((g.ROOT/'review365_balanced_source_validation/result.json').read_text()))['proofscopecomplete'])
 def test_archive_tamper(self):
  orig=Path.read_bytes
  def bad(p):return orig(p)+b' 'if p.name=='bedroom_route_witness_actual358.json'else orig(p)
  with patch.object(Path,'read_bytes',bad):self.assertFalse(g.evaluate(self.r,self.v)['proofscopecomplete'])
 def test_probe_tamper(self):
  orig=Path.read_bytes
  def bad(p):return orig(p)+b' 'if p.name=='result.json'and p.parent.name=='local_closet_counterfactual_service365'else orig(p)
  with patch.object(Path,'read_bytes',bad):self.assertFalse(g.evaluate(self.r,self.v)['proofscopecomplete'])
 def test_actual_tradeoff_not_dominance(self):
  o=json.loads((g.P/'bedroom_grouping_service_actual365.json').read_text());self.assertTrue(o['proofscopecomplete']);self.assertFalse(o['parent_initial']);self.assertFalse(o['delivery_allowed'])
  for u in o['evidence']['per_unit_tradeoffs']:
   a=u['alternatives']['row358'];self.assertTrue(a['shorter']);self.assertTrue(a['longer']);self.assertEqual(len(a['area_loss_disclosed']),3);self.assertFalse(a['is_nonshrink_repair'])
if __name__=='__main__':unittest.main()
