import unittest,json,copy
from unittest.mock import patch
from pathlib import Path
import service365_private_evidence_v2 as s
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((s.P.parent/'staging365_service_grammar/candidate365.json').read_text());c.v=json.loads((s.P.parent/'review365_service_source_validation/result.json').read_text())
 def test_guest_import_mutation(self):
  read=Path.read_bytes
  def changed(p):return read(p)+b'\n# tamper'if p.name=='guest_closure.py'else read(p)
  with patch.object(Path,'read_bytes',changed),self.assertRaisesRegex(ValueError,'SOURCE_CHANGED:guest_closure'):s.evaluate(self.r,self.v)
 def test_living_import_mutation(self):
  read=Path.read_bytes
  def changed(p):return read(p)+b'\n# tamper'if p.name=='living_closure.py'else read(p)
  with patch.object(Path,'read_bytes',changed),self.assertRaisesRegex(ValueError,'SOURCE_CHANGED:living_closure'):s.evaluate(self.r,self.v)
 def test_old_artifact_not_promoted(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['inputs'][0]='27'
  with self.assertRaises(ValueError):s.evaluate(r,self.v)
 def test_saved_exact_equivalence(self):
  old=json.loads((s.P/'service365_private_actual.json').read_text());new=json.loads((s.P/'service365_private_actual_v2.json').read_text());self.assertEqual(old['rows'],new['rows']);self.assertEqual(old['task_routes'],new['task_routes']);self.assertFalse(new['parent_complete'])
if __name__=='__main__':unittest.main()
