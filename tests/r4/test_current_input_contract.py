"""R4-1.02 focused current V3 HTTP contract tests, no geometry dispatch."""
import hashlib,http.client,json,pathlib,threading,unittest
from unittest.mock import patch
import public_wln_server as server
from public_wln_contract import parse_public,SCHEMA,DOMAIN_POLICY_VERSION,verify_public
from live_program_scheduler import preflight
from dimension_contract import InputError
ROOT=pathlib.Path(__file__).resolve().parents[2]
class Boundaries(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=server.server(0);cls.port=cls.s.server_address[1]
  cls.t=threading.Thread(target=cls.s.serve_forever,daemon=True);cls.t.start()
 @classmethod
 def tearDownClass(cls):cls.s.shutdown();cls.s.server_close();cls.t.join()
 def request(self,body):
  c=http.client.HTTPConnection('127.0.0.1',self.port,timeout=5)
  c.request('POST','/api/public/plan',body=body,headers={'Content-Type':'application/json'})
  r=c.getresponse();status=r.status;out=json.loads(r.read());c.close();return status,out
 def rejected(self,data,status,code,field=None):
  body=json.dumps(data).encode()
  with self.assertRaises(InputError) as ex:parse_public(body)
  self.assertEqual((ex.exception.status,ex.exception.code),(status,code))
  with patch('public_wln_server.run_live',side_effect=AssertionError('UNEXPECTED_DISPATCH')) as dispatch:
   actual,out=self.request(body);self.assertEqual(actual,status);self.assertEqual(out['code'],code)
   if field is not None:self.assertEqual(out['field'],field)
   for k in server.AUTH:self.assertIs(out[k],False)
   dispatch.assert_not_called()
 def test_both_axis_exact_outside_bounds(self):
  for axis in ('W','L'):
   for value in ('4.999','25.001'):
    with self.subTest(axis=axis,value=value):
     raw={'W':'18','L':'20','n':2};raw[axis]=value
     self.rejected(raw,422,'DIMENSION_OUT_OF_OWNER_RANGE',axis)
 def test_closed_boundaries_valid_but_not_ready(self):
  for axis in ('W','L'):
   for value in ('5','25'):
    raw={'W':'18','L':'20','n':2};raw[axis]=value;body=json.dumps(raw).encode()
    envelope=parse_public(body);self.assertEqual(verify_public(body,envelope),envelope)
    self.assertEqual(envelope['canonical_request']['dimensions_m'][axis],{'numerator':value,'denominator':'1'})
    with patch('public_wln_server.run_live',side_effect=AssertionError('UNEXPECTED_DISPATCH')) as dispatch:
     status,out=self.request(body);self.assertEqual(status,409);self.assertIs(out['input_valid'],True)
     self.assertEqual(out['actual_live_attempts'],0);dispatch.assert_not_called()
 def test_invalid_unit_domain(self):
  for n in (3,4,'3','4'):
   self.rejected({'W':'18','L':'20','n':n},422,'INVALID_BRIEF','n')
 def test_fraction_string_and_empty_unit(self):
  self.rejected({'W':'18','L':'20','n':'1.5'},422,'INVALID_BRIEF','n')
  self.rejected({'W':'18','L':'20','n':''},422,'INPUT_REQUIRED','n')
 def test_unit_decimal_token_is_invalid_brief_no_rounding(self):
  self.rejected({'W':'18','L':'20','n':1.5},422,'INVALID_BRIEF','n')
 def test_missing_null_blank_unit_required(self):
  for value in (None,'',' ','\t'):
   self.rejected({'W':'18','L':'20','n':value},422,'INPUT_REQUIRED','n')
  self.rejected({'W':'18','L':'20'},422,'INPUT_REQUIRED','n')
 def test_other_invalid_unit_values(self):
  for n in (0,-1,True,False,'abc',[],{},'2.0','2e0'):
   self.rejected({'W':'18','L':'20','n':n},422,'INVALID_BRIEF','n')
 def test_dimension_wire_policy_unmodified(self):
  self.rejected({'W':18.5,'L':'20','n':2},409,'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION')
 def test_unit_decimal_tokens_rejected_even_integral_value(self):
  for token in ('1.0','1e0','2.0','2e0','1e'+'9'*70):
   body=('{"W":"18","L":"20","n":'+token+'}').encode()
   with self.assertRaises(InputError) as ex:parse_public(body)
   self.assertEqual((ex.exception.code,ex.exception.status),('INVALID_BRIEF',422))
   with patch('public_wln_server.run_live',side_effect=AssertionError('UNEXPECTED_DISPATCH')) as dispatch:
    status,out=self.request(body);self.assertEqual((status,out['code']),(422,'INVALID_BRIEF'));dispatch.assert_not_called()
 def test_hidden_fields(self):
  for name,value in (('bedrooms',2),('requested_count',6),('program',{'bedrooms_per_unit':2})):
   self.rejected({'W':'18','L':'20','n':2,name:value},422,'UNEXPECTED_PUBLIC_FIELD',name)
 def test_n1_valid_unsupported_n2_selected_without_execution(self):
  one=preflight(b'{"W":"18","L":"20","n":1}')
  self.assertIs(one['input_valid'],True);self.assertIs(one['execution_ready'],False)
  with patch('public_wln_server.run_live',side_effect=AssertionError('UNEXPECTED_DISPATCH')) as dispatch:
   status,out=self.request(b'{"W":"18","L":"20","n":1}');self.assertEqual(status,409)
   self.assertIs(out['input_valid'],True);dispatch.assert_not_called()
  two=preflight(b'{"W":"18","L":"20","n":2}');self.assertIs(two['execution_ready'],True)
 def test_versions_and_current_static_ui_domain(self):
  self.assertEqual(SCHEMA,'V25_PUBLIC_WLN_CONTRACT_V3');self.assertEqual(DOMAIN_POLICY_VERSION,'MVP_UNIT_DOMAIN_PRD_V3')
  html=(ROOT/'app/local_integration/public_wln.html').read_text()
  js=(ROOT/'app/local_integration/public_wln.js').read_text()
  self.assertIn('min="1" max="2" step="1"',html);self.assertEqual(html.count('<input '),3)
  self.assertIn('(n!==1&&n!==2)',js)
  self.assertNotIn('requested_count',html);self.assertNotIn('name="bedrooms"',html)
if __name__=='__main__':unittest.main()
