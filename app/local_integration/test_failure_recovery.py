"""Controlled operational failures. No damaged real dependency or geometry claim."""
import json,sys,tempfile,subprocess,unittest
from pathlib import Path
from unittest.mock import patch
import generation_gateway as generation
import repair_saved_run as repair
BODY=b'{"W":"25","L":"25","n":2,"requested_count":1}'
class FailureRecovery(unittest.TestCase):
 def test_real_missing_generation_executable(self):
  with tempfile.TemporaryDirectory()as t,patch.object(generation,'ROOT',Path(t)):
   status,r=generation.generate(BODY);self.assertEqual(status,503);p=Path(t)/'app/local_integration/evidence/requests'/r['run_id'];life=json.loads((p/'lifecycle.json').read_text());self.assertFalse(life['worker_started']);self.assertIsNone(life['pid']);self.assertTrue(life['wait_completed']);self.assertFalse(r['delivery_allowed'])
 def test_real_missing_repair_executable(self):
  with tempfile.TemporaryDirectory()as t,patch.object(repair,'BASE',Path(t)),patch.object(repair.sys,'executable',str(Path(t)/'nonexistent-python')):
   status,r=repair.execute('parent','candidate',BODY);self.assertEqual(status,503);self.assertFalse(json.loads((Path(t)/r['run_id']/'lifecycle.json').read_text())['worker_started'])
 def timeout_case(self,module,is_repair):
  real=subprocess.Popen;children=[]
  def child(*a,**kw):
   p=real([sys.executable,'-c','import time;time.sleep(30)'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);children.append(p);return p
  # Accelerated clock tests deadline branch, not a real150-second endurance test.
  clock=iter([0,151])
  with tempfile.TemporaryDirectory()as t,patch.object(module,'BASE' if is_repair else 'ROOT',Path(t)),patch.object(module.subprocess,'Popen',side_effect=child),patch.object(module.time,'monotonic',side_effect=lambda:next(clock)):
   status,r=module.execute('parent','candidate',BODY)if is_repair else module.generate(BODY)
   self.assertEqual(status,504);self.assertEqual(r['outcome'],'EXECUTION_TIMEOUT');self.assertEqual(children[0].returncode,-9);self.assertFalse(r['accepted'])
 def test_generation_deadline_branch(self):self.timeout_case(generation,False)
 def test_repair_deadline_branch(self):self.timeout_case(repair,True)
if __name__=='__main__':unittest.main()
