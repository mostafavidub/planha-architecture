import json,unittest,tempfile,subprocess,sys
from pathlib import Path
from unittest.mock import patch
import repair_saved_run as gateway
class RepairGateway(unittest.TestCase):
    def test_bad_shape(self):
        for body in (b'{}',b'[]',b'{"run_id":1,"candidate_id":2,"extra":3}',b'{"run_id":"x","run_id":"y","candidate_id":"z"}',b'{"run_id":NaN,"candidate_id":"z"}'):
            with patch.object(gateway,'execute') as execute:
                status,result=gateway.repair(body);self.assertEqual(status,422);execute.assert_not_called();self.assertFalse(result['delivery_allowed'])
    def test_invalid_saved_source(self):
        with patch.object(gateway,'load_source',side_effect=ValueError('bad')),patch.object(gateway,'execute')as execute:
            self.assertEqual(gateway.repair(b'{"run_id":"x","candidate_id":"y"}')[0],422);execute.assert_not_called()
    def test_exact_body_preserved(self):
        with patch.object(gateway,'load_source',return_value=(b' exact bytes ',{},{})),patch.object(gateway,'execute',return_value=(200,{}))as execute:
            gateway.repair(b'{"run_id":"x","candidate_id":"y"}');execute.assert_called_once_with('x','y',b' exact bytes ',None)
    def test_real_owned_child_cancelled_and_reaped(self):
        real=subprocess.Popen
        def child(*a,**kw):return real([sys.executable,'-c','import time;time.sleep(30)'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        with tempfile.TemporaryDirectory()as temp,patch.object(gateway,'BASE',Path(temp)),patch.object(gateway.subprocess,'Popen',side_effect=child):
            status,r=gateway.execute('x','y',b'{"W":25,"L":25,"n":2,"requested_count":1}',lambda:True);self.assertEqual(status,499);self.assertEqual(r['outcome'],'CANCELLED');life=json.loads((Path(temp)/r['run_id']/'lifecycle.json').read_text());self.assertTrue(life['wait_completed']);self.assertEqual(life['returncode'],-9)
    def test_nonzero_worker_fails_closed(self):
        real=subprocess.Popen
        def child(*a,**kw):return real([sys.executable,'-c','raise SystemExit(1)'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        with tempfile.TemporaryDirectory()as temp,patch.object(gateway,'BASE',Path(temp)),patch.object(gateway.subprocess,'Popen',side_effect=child):
            status,r=gateway.execute('x','y',b'{"W":25,"L":25,"n":2,"requested_count":1}');self.assertEqual(status,500);self.assertFalse(r['accepted'])
if __name__=='__main__':unittest.main()
