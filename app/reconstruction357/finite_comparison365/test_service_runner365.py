import sys,json,copy,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'semantic_rules357'))
import service_runner365 as runner
R=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());F=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text())
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.actual=runner.evaluate(R,F)
 def test_actual(self):self.assertEqual(self.actual['verdict'],'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS')
 def test_manifest_bad(self):
  with patch.object(runner,'MANIFEST_SHA','bad'),self.assertRaises(ValueError):runner.evaluate(R,F)
 def test_caller_record_bad(self):
  r=copy.deepcopy(R);r['accepted']=True;fake=type('Done',(),{'stdout':json.dumps(self.actual)})()
  with patch.object(runner.subprocess,'run',return_value=fake),self.assertRaises(ValueError):runner.evaluate(r,F)
 def test_caller_review_bad(self):
  f=copy.deepcopy(F);f['accepted']=True;fake=type('Done',(),{'stdout':json.dumps(self.actual)})()
  with patch.object(runner.subprocess,'run',return_value=fake),self.assertRaises(ValueError):runner.evaluate(R,f)
 def test_source_bad(self):
  real=Path.read_bytes
  def bad(p):
   b=real(p);return b+b'bad'if str(p).endswith('/service_closure365.py')else b
  with patch.object(Path,'read_bytes',bad),patch.object(runner.subprocess,'run')as run,self.assertRaises(ValueError):runner.evaluate(R,F)
  run.assert_not_called()
if __name__=='__main__':unittest.main()
