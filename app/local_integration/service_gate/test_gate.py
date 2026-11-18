import unittest,http.server,threading,http.client,json
from range25_wrapper import wrapped_handler,validate,is_generation
class Gate(unittest.TestCase):
 def test_boundaries(self):
  for axis in ('W','L'):
   for value in ('5','25','۵','۲۵','۲۵٫۰۰۰۰'):
    r={'W':25,'L':25};r[axis]=value;self.assertIsNone(validate(json.dumps(r).encode()))
   for value in ('25.0001','۲۵٫۰۰۰۱','45','4.999'):
    r={'W':25,'L':25};r[axis]=value;self.assertEqual(validate(json.dumps(r).encode()),('DIMENSION_OUT_OF_OWNER_RANGE',axis))
 def test_bad_exact_types(self):
  for v in (25.0,True,None,'1e1'):
   self.assertIsNotNone(validate(json.dumps({'W':v,'L':25}).encode()))
 def test_paths(self):
  for p in ('/generate','/generate-hybrid150','/generate-reference116','/generate-unified91','/review-concept'):self.assertTrue(is_generation(p))
  for p in ('/reopen','/reopen-hybrid150','/hybrid150-artifact','/save-concepts'):self.assertFalse(is_generation(p))
 def test_http_pass_through_auth_archive_and_banner(self):
  calls=[]
  class H(http.server.BaseHTTPRequestHandler):
   def log_message(self,*a):pass
   def do_POST(self):
    body=self.rfile.read(int(self.headers['Content-Length']));calls.append((self.path,body));self.send_response(200 if self.headers.get('X-Test')=='ok'else 403);self.end_headers();self.wfile.write(body)
   def do_GET(self):
    b=b'<html><h1>old</h1></html>';self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
  s=http.server.HTTPServer(('127.0.0.1',0),wrapped_handler(H));t=threading.Thread(target=s.serve_forever);t.start()
  try:
   def req(path,body,auth=True):
    c=http.client.HTTPConnection('127.0.0.1',s.server_port);c.request('POST',path,body,{'X-Test':'ok'if auth else'no'});r=c.getresponse();data=r.read();c.close();return r.status,data
   raw=b'{"W":"25.0001","L":25}'
   self.assertEqual(req('/generate',raw)[0],422);self.assertEqual(calls,[])
   self.assertEqual(req('/reopen',raw),(200,raw));self.assertEqual(calls[-1],('/reopen',raw))
   valid=b'{ "W":25, "L":5 }';self.assertEqual(req('/generate',valid),(200,valid));self.assertEqual(req('/generate',valid,False)[0],403)
   c=http.client.HTTPConnection('127.0.0.1',s.server_port);c.request('GET','/');r=c.getresponse();b=r.read();self.assertIn('۵ تا ۲۵'.encode(),b);self.assertIn(b'<h1>old</h1>',b);self.assertEqual(int(r.getheader('Content-Length')),len(b));c.close()
  finally:s.shutdown();t.join();s.server_close()
if __name__=='__main__':unittest.main()
