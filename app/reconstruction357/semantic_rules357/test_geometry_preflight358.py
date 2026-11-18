import unittest,json
from pathlib import Path
from common import digest
class PreflightArtifact(unittest.TestCase):
 def test_actual_bound_and_non_admitting(self):
  p=Path(__file__).resolve().parent;o=json.loads((p/'geometry_support_preflight_actual358.json').read_text());r=json.loads((p.parent/'staging358_comparative/row_candidate358.json').read_text());self.assertEqual(o['model_hash'],digest(r['candidate']['model']));self.assertEqual(o['status'],'GEOMETRY_MEASURED_NOT_ACCEPTED')
  for k in('source_use_verified','parent_complete','admission_allowed','fresh_execution'):self.assertFalse(o[k])
  self.assertEqual([r['unresolved_area_m2']for r in o['rows']],['0','0']);self.assertTrue(all(not r['components']for r in o['causes']['units']))
if __name__=='__main__':unittest.main()
