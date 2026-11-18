import http.client
import json
from pathlib import Path
import select
import signal
import socket
import subprocess
import sys
import unittest
from test_dimension_contract import body


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc=subprocess.Popen([sys.executable,'-B',str(Path(__file__).with_name('validation_server.py'))],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            if not select.select([cls.proc.stdout],[],[],5)[0]:raise RuntimeError('SERVER_START_TIMEOUT')
            cls.port=json.loads(cls.proc.stdout.readline())['port']
        except BaseException:
            cls.proc.terminate();cls.proc.communicate(timeout=5);raise

    @classmethod
    def tearDownClass(cls):
        cls.proc.send_signal(signal.SIGINT)
        out,err=cls.proc.communicate(timeout=5)
        assert cls.proc.returncode==0,err
        assert b'"listener_closed": true' in out,out
        with socket.socket() as sock:
            sock.settimeout(1)
            assert sock.connect_ex(('127.0.0.1',cls.port))!=0,'LISTENER_STILL_OPEN'

    def request(self, method, path, data=None, headers=None):
        conn=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5)
        try:
            conn.request(method,path,body=data,headers=headers or {})
            response=conn.getresponse();return response.status,json.loads(response.read())
        finally:conn.close()

    def test_real_post_preserves_request(self):
        for w,l in [('۵','۲۵'),('١٢٫٥','١٤'),('12','14'),('13','14'),('12','15')]:
            status,response=self.request('POST','/validate',body(W=w,L=l),{'Content-Type':'application/json'})
            self.assertEqual(status,409)
            self.assertEqual(response['envelope']['received_input']['W'],w)
            self.assertEqual(response['envelope']['received_input']['L'],l)
            self.assertFalse(response['accepted']);self.assertFalse(response['delivery_allowed'])
            self.assertEqual(response['envelope']['canonical_request']['requested_count'],6)

    def test_generation_rejects_unsupported_before_dispatch(self):
        status,result=self.request('POST','/generate',body(n=1),{'Content-Type':'application/json'})
        self.assertEqual(status,409);self.assertEqual(result['code'],'UNSUPPORTED_UNIT_COUNT_CURRENT_PARAMETRIC_FAMILY')

    def test_invalid_requests(self):
        for data in [b'{',body(W=4),body(L=None),b'{"W":5,"W":6}']:
            status,_=self.request('POST','/validate',data,{'Content-Type':'application/json'})
            self.assertEqual(status,422)

    def test_health_and_no_generation_route(self):
        status,result=self.request('GET','/health');self.assertEqual(status,200)
        self.assertTrue(result['generation_enabled']);self.assertEqual(result['mode'],'EXPERIMENTAL_PARAMETRIC')
        self.assertEqual(self.request('POST','/api/runs',body(),{'Content-Type':'application/json'})[0],404)

    def test_content_type_and_body_limit(self):
        self.assertEqual(self.request('POST','/validate',body(),{'Content-Type':'text/plain'})[0],415)
        self.assertEqual(self.request('POST','/validate',b' '*16385,{'Content-Type':'application/json'})[0],409)

    def test_actual_history_record_and_no_store(self):
        run='0d9f29cd-33ce-42be-9984-4a774bffd21e'
        status,result=self.request('GET','/history/'+run)
        self.assertEqual(status,200);self.assertTrue(result['historical_only'])
        self.assertFalse(result['live_model_restored']);self.assertEqual(result['run_id'],run)
        c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5)
        try:
            c.request('GET','/history');r=c.getresponse();self.assertEqual(r.getheader('Cache-Control'),'no-store');r.read()
        finally:c.close()

    def test_actual_output_paths_deny_and_path_escape(self):
        run='0d9f29cd-33ce-42be-9984-4a774bffd21e'
        for route in ('/export/','/download/'):
            status,result=self.request('GET',route+run)
            self.assertEqual(status,403);self.assertEqual(result['artifact_bytes_sent'],0)
        for route in ('/history/../x','/history/'+run+'?id=other','/download/../request.json'):
            self.assertEqual(self.request('GET',route)[0],404)


class DisconnectedResponseTests(unittest.TestCase):
    def test_browser_disconnect_does_not_raise_or_retry(self):
        from validation_server import Handler
        from unittest.mock import Mock
        handler=Handler.__new__(Handler)
        handler.send_response=Mock();handler.send_header=Mock();handler.end_headers=Mock()
        handler.wfile=Mock();handler.wfile.write.side_effect=BrokenPipeError()
        handler.respond(200,{'accepted':False})
        self.assertTrue(handler.close_connection)
        self.assertEqual(handler.wfile.write.call_count,1)

if __name__=='__main__':unittest.main()

