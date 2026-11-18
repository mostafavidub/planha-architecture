import unittest,json,copy,sys,subprocess,tempfile,time,os
from pathlib import Path
from unittest.mock import patch
import service_criterion367_v4 as s
import service_runner367_v4 as r
ROOT=r.ROOT
R=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());V=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());D=json.loads((ROOT/'finite_comparison367/service_receipts_capture367.json').read_text())['nested']
class Tests(unittest.TestCase):
 def output(self):
  with patch.object(s,'costs',return_value=copy.deepcopy(D['cost']))as c,patch.object(s,'necessity',return_value=copy.deepcopy(D['q04']))as q,patch('service_role_inventory_joint367.evaluate',return_value=copy.deepcopy(D['partition']))as p:
   x=s.evaluate(R,V);c.assert_called_once();q.assert_called_once();p.assert_called_once();return x
 def test_once_and_exact_receipts(self):self.assertTrue(r.verify_receipts(self.output()))
 def test_changed_receipt_fails(self):
  x=self.output();x['invocation_receipts']['necessity']['accepted']=True
  with self.assertRaises(ValueError):r.verify_receipts(x)
 def test_wrong_nested_model(self):
  x=self.output();x['invocation_receipts']['cost']['model_digest']='bad';x['cost_receipt_digest']=r.digest(x['invocation_receipts']['cost'])
  with self.assertRaises(ValueError):r.verify_receipts(x)
 def test_contained_success(self):self.assertEqual(r.contained_run([sys.executable,'-c','print("ok")'],2).strip(),'ok')
 def test_timeout_descendant_killed(self):
  with tempfile.TemporaryDirectory()as d:
   pidfile=Path(d)/'pid';code='import subprocess,sys,time; p=subprocess.Popen([sys.executable,"-c","import time;time.sleep(30)"]);open(sys.argv[1],"w").write(str(p.pid));time.sleep(30)'
   with self.assertRaises(subprocess.TimeoutExpired):r.contained_run([sys.executable,'-c',code,str(pidfile)],.3)
   pid=int(pidfile.read_text());time.sleep(.05)
   stat=Path('/proc')/str(pid)/'stat'
   if stat.exists():self.assertEqual(stat.read_text().split()[2],'Z')
 def test_exception_exit_cleanup(self):
  with self.assertRaises(subprocess.CalledProcessError):r.contained_run([sys.executable,'-c','raise SystemExit(3)'],2)
if __name__=='__main__':unittest.main()
