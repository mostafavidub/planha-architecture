import unittest,subprocess,signal,json
from unittest.mock import patch,MagicMock
import final_role_joint367_launcher_v3 as m
class Containment(unittest.TestCase):
 def worker(self):
  p=MagicMock();p.pid=987654321;p.returncode=0;p.communicate.return_value=('{}','');return p
 def test_fixed_modes(self):
  with self.assertRaises(ValueError):m.run('arbitrary')
 def test_fixed_source_preimport_script(self):
  for s in m.SCRIPTS.values():self.assertLess(s.index("for n,h in m['files']"),s.index('sys.path.insert'));self.assertIn('assert hashlib.sha256',s)
 def test_success_group_finally_killed(self):
  p=self.worker()
  with patch.object(m.subprocess,'Popen',return_value=p)as pop,patch.object(m.os,'killpg')as kill:
   m.run('tests');self.assertTrue(pop.call_args.kwargs['start_new_session']);self.assertEqual(p.communicate.call_args_list[0].kwargs,{'timeout':180});kill.assert_called_once_with(p.pid,signal.SIGKILL)
 def test_timeout_group_finally_killed(self):
  p=self.worker();p.communicate.side_effect=[subprocess.TimeoutExpired('fixed',180),('','')]
  with patch.object(m.subprocess,'Popen',return_value=p),patch.object(m.os,'killpg')as kill:
   with self.assertRaises(subprocess.TimeoutExpired):m.run('actual')
   kill.assert_called_once_with(p.pid,signal.SIGKILL);self.assertEqual(p.communicate.call_count,2)
 def test_failure_group_finally_killed(self):
  p=self.worker();p.returncode=1
  with patch.object(m.subprocess,'Popen',return_value=p),patch.object(m.os,'killpg')as kill:
   with self.assertRaises(ValueError):m.run('tests')
   kill.assert_called_once()
if __name__=='__main__':unittest.main()
