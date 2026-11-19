import json,unittest,threading,http.client
from unittest.mock import patch
import public_input_errors403 as D
import public_wln_contract as V
from dimension_contract import InputError
import public_wln_server as P
import request_trace_server109 as T
class Diagnostics(unittest.TestCase):
 def err(self,body):
  try:D.parse_public_errors(body)
  except InputError as e:return e
  self.fail('expected invalid')
 def test_valid_envelope_identical(self):
  for x in ({'W':'۵٫۵','L':'۲۵','n':'۱'},{'W':5,'L':25,'n':2},{'W':'18','L':'20','n':'2'}):
   b=json.dumps(x).encode();self.assertEqual(D.parse_public_errors(b),V.parse_public(b))
 def test_three_independent_semantic_errors(self):
  b=b'{"W":"4.999","L":"25.001","n":3}';e=self.err(b)
  self.assertEqual([x['field']for x in e.errors],['W','L','n'])
  self.assertEqual([x['code']for x in e.errors],['DIMENSION_OUT_OF_OWNER_RANGE']*2+['INVALID_BRIEF'])
 def test_primary_missing_n_preserved(self):
  e=self.err(b'{}');self.assertEqual((e.code,e.field,e.status),('INPUT_REQUIRED','n',422))
  self.assertEqual([x['field']for x in e.errors],['W','L','n'])
 def test_mixed_status_preserved(self):
  for w,l in [('1'*65,'26'),('4','1'*65)]:
   b=json.dumps({'W':w,'L':l,'n':3}).encode();e=self.err(b)
   try:V.parse_public(b)
   except InputError as original:self.assertEqual(D.row(e),D.row(original))
   self.assertEqual([x['status']for x in e.errors],[409,422,422]if len(w)>64 else[422,409,422])
 def test_structural_failfast(self):
  cases=[b'{"W":5.5,"L":26,"n":3}',b'{"W":5,"W":6,"L":26,"n":3}',b'{"W":NaN,"L":26,"n":3}',b'{"W":Infinity}',b'[]',b'{',b'{"W":4,"L":26,"n":3,"extra":true}',b'{"W":'+b'1'*65+b',"L":26,"n":3}']
  for b in cases:
   e=self.err(b);self.assertEqual(e.scope,'STRUCTURAL_FAIL_FAST');self.assertEqual(e.errors,[D.row(e)])
 def test_unit_decimal_not_rounded(self):
  for token in ('2.0','2e0','1.5'):
   e=self.err(('{"W":"4","L":"26","n":'+token+'}').encode())
   self.assertEqual(e.errors[-1],{'code':'INVALID_BRIEF','field':'n','status':422})
 def test_blank_null_bool_types(self):
  for n in ('',None,False):
   e=self.err(json.dumps({'W':None,'L':False,'n':n}).encode())
   self.assertEqual(len(e.errors),3);self.assertEqual(e.errors[-1]['code'],'INVALID_BRIEF'if n is False else'INPUT_REQUIRED')
 def test_source_pins(self):self.assertEqual(len(D.guard()),2)
class HTTP(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.servers=[]
  for module in (P,T):
   s=module.server(0);t=threading.Thread(target=s.serve_forever,daemon=True);t.start();cls.servers.append((module,s,t))
 @classmethod
 def tearDownClass(cls):
  for m,s,t in cls.servers:s.shutdown();s.server_close();t.join()
 def post(self,s,b):
  c=http.client.HTTPConnection('127.0.0.1',s.server_port,timeout=5);c.request('POST','/api/public/plan',b,{'Content-Type':'application/json'});r=c.getresponse();status=r.status;out=json.loads(r.read());c.close();return status,out
 def test_actual_both_http_no_dispatch(self):
  with patch.object(P,'run_live',side_effect=AssertionError('NO_DISPATCH'))as p,patch.object(T,'run',side_effect=AssertionError('NO_DISPATCH'))as t:
   for m,s,thread in self.servers:
    for b in (b'{}',b'{"W":"4","L":"26","n":3}',json.dumps({'W':'1'*65,'L':'26','n':3}).encode(),b'{"W":5.5,"L":26,"n":3}'):
     e=D.parse_public_errors
     try:e(b)
     except InputError as expected:
      status,out=self.post(s,b);self.assertEqual(status,expected.status);self.assertEqual(out,D.response(expected))
   p.assert_not_called();t.assert_not_called()
 def test_validation_fault_closed_before_dispatch(self):
  for m,s,thread in self.servers:
   with patch.object(m,'parse_public',side_effect=ValueError('SOURCE_PRIVATE_DETAIL')),patch.object(m,'run_live'if m is P else'run',side_effect=AssertionError('NO_DISPATCH'))as dispatch:
    status,out=self.post(s,b'{"W":"18","L":"20","n":2}')
    self.assertEqual(status,500);self.assertEqual(out['code'],'INPUT_VALIDATION_FAILED_CLOSED')
    self.assertFalse(out['generation_started']);self.assertNotIn('SOURCE_PRIVATE_DETAIL',json.dumps(out));dispatch.assert_not_called()
 def test_valid_unsupported_no_worker(self):
  import request_trace109 as trace
  with patch.object(P,'run_live',side_effect=AssertionError('NO_WORKER'))as p,patch.object(trace,'make_request',side_effect=AssertionError('NO_WORKER'))as t:
   for m,s,thread in self.servers:
    status,out=self.post(s,b'{"W":"5","L":"5","n":"1"}');self.assertEqual(status,409);self.assertNotEqual(out.get('schema'),D.SCHEMA)
    self.assertTrue(out.get('input_valid'));self.assertEqual(out.get('scope'),'VALID_UNSUPPORTED_CAPABILITY')if m is T else None
   p.assert_not_called();t.assert_not_called()
if __name__=='__main__':unittest.main()
