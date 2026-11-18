import sys,json,copy,unittest,hashlib
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'semantic_rules357'))
import q04_runner365 as runner
R=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());F=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text())
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.actual=runner.evaluate(R,F)
 def test_actual(self):
  self.assertEqual(self.actual['verdict'],'PASS_SCOPED_FINITE_Q04_SOURCE_BALANCED365');self.assertEqual(self.actual['remaining'],[]);self.assertFalse(self.actual['accepted'])
 def test_manifest_rejected(self):
  with patch.object(runner,'MANIFEST_SHA','bad'),self.assertRaises(ValueError):runner.evaluate(R,F)
 def test_caller_forged_record_rejected(self):
  r=copy.deepcopy(R);r['accepted']=True
  fake=type('Done',(),{'stdout':json.dumps(self.actual)})()
  with patch.object(runner.subprocess,'run',return_value=fake),self.assertRaises(ValueError):runner.evaluate(r,F)
 def test_caller_forged_review_rejected(self):
  f=copy.deepcopy(F);f['accepted']=True
  fake=type('Done',(),{'stdout':json.dumps(self.actual)})()
  with patch.object(runner.subprocess,'run',return_value=fake),self.assertRaises(ValueError):runner.evaluate(R,f)
 def test_common_current_binding(self):
  c=self.actual['current_common_role'];self.assertEqual(c['model_hash'],self.actual['model_digest']);self.assertEqual(c['raw_review_digest'],self.actual['fresh_result_digest'])
 def test_source_corruption_rejected_before_subprocess(self):
  real=Path.read_bytes
  def bad(p):
   b=real(p)
   return b+b'\n# corruption'if str(p).endswith('/common_role_closure365.py')else b
  with patch.object(Path,'read_bytes',bad),patch.object(runner.subprocess,'run')as run,self.assertRaises(ValueError):runner.evaluate(R,F)
  run.assert_not_called()
 def test_service_alternative_retained(self):
  member=next(x for x in self.actual['alternatives']if x['id']=='service_anchor365');self.assertTrue(member['not_deleted']);self.assertEqual(member['eligibility']['verdict'],'PASS');self.assertEqual(member['comparison']['dominance'],'FALSE')
 def test_all_common_tasks_present(self):
  self.assertEqual(set(self.actual['current_common_task_bindings']),{'lift_A','lift_B','stair_A','stair_B'})
  self.assertEqual(len([k for k in self.actual['all_objectives']if k.startswith('COMMON/')and k.endswith(('/length','/turns'))]),8)
if __name__=='__main__':unittest.main()
