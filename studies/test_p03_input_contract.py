"""P03 current input-contract proof, not generation/product qualification.
Real HTTP factories/parser/preflight; sentinels only at execution boundaries.
"""
import copy,hashlib,http.client,importlib,inspect,json,sys,threading,unittest
from contextlib import ExitStack
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ENGINE),str(ROOT/'frontend')]
import public_wln_contract as v3
import public_input_errors403 as diagnostic
import current_entry_boundary_x03 as boundary
import current_entry_launch_x03 as launch
from dimension_contract import InputError
BASE='dc07a92502c77bcc438b91c75c8a3d8d1da4ac89'
PINS={"app/local_integration/public_wln_contract.py":"80fd2b2710342735dc35e484c9b0da790995d830","app/local_integration/dimension_contract.py":"058502cd97b5131908b82fdbdba34c62d3376ea3","app/local_integration/public_input_errors403.py":"4dba239c1484c6eda7985cde0b590680ec9ed3f3","app/local_integration/public_wln_server.py":"da45aa429bf055ec021e3e4110024b05a85ae49c","app/local_integration/request_trace_server109.py":"fbe215097b43c576ff3c97d44e741cea3d0de834","app/local_integration/current_entry_launch_x03.py":"771efe4180d03eb420e926b7c070f22937e31685","app/local_integration/current_entry_boundary_x03.py":"8383c54d4f6bfd3d94580ede2ab20276b917f414","app/local_integration/live_program_scheduler.py":"1b671b6632d01c1012fcb39b2c33e731fb619fbc","app/local_integration/request_trace109.py":"a992bc89c70f2e2a3ee7a5c361d87830ed8e0f52","app/local_integration/automatic_program_search.py":"686e29e65384a8b6990cbb65b63050ca6aef4208","app/local_integration/public_wln.js":"6d49500c2f253bbd3b167a50de0598705f1a9484","app/local_integration/public_wln.html":"3315b1837bb3a6328db2e4908ef0686ef624b4bc","app/reconstruction357/planha_general150_runtime_work/contract114.py":"a2631c6a38a43b8d423edf82ad8d526ced1b8196"}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
HTTP_OBSERVATIONS=[]
def snapshot():
 result={}
 for name,pin in PINS.items():
  p=ROOT/name;b=p.read_bytes()
  if p.is_symlink()or hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()!=pin:raise AssertionError('P03_SOURCE_CHANGED:'+name)
  result[name]=hashlib.sha256(b).hexdigest()
 return result
def body(**changes):
 raw={'W':'18','L':'20','n':2};raw.update(changes)
 return json.dumps(raw,ensure_ascii=False,allow_nan=False).encode()
def raw_token(field,token):
 raw={'W':'"18"','L':'"20"','n':'2'};raw[field]=token
 return ('{'+','.join('"'+k+'":'+v for k,v in raw.items())+'}').encode()
def matrix():
 cases=[]
 def add(name,b,status,code=None,kind='INVALID_INPUT'):
  cases.append((name,b,status,code,kind))
 for axis in ('W','L'):
  for value in ('5','25'):
   add(axis+'_boundary_string_'+value,body(**{axis:value}),409,None,'VALID_UNSUPPORTED')
   add(axis+'_boundary_integer_'+value,body(**{axis:int(value)}),409,None,'VALID_UNSUPPORTED')
  for value in ('4.999','25.001','25.0000000000000001'):
   add(axis+'_outside_string_'+value,body(**{axis:value}),422,'DIMENSION_OUT_OF_OWNER_RANGE')
   add(axis+'_outside_numeric_'+value,raw_token(axis,value),409,'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION','UNSUPPORTED_WIRE_REPRESENTATION')
  for value in ('18.125','۱۸٫۱','١٢٫٥','5.000000000000000001'):
   add(axis+'_exact_string_'+value,body(**{axis:value}),409,None,'VALID_UNSUPPORTED')
  for value in ('18.125','18e0','1e400'):
   add(axis+'_numeric_wire_'+value,raw_token(axis,value),409,'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION','UNSUPPORTED_WIRE_REPRESENTATION')
  for value,code in (('', 'EXACT_DECIMAL_REQUIRED'),(None,'INVALID_FIELD_TYPE'),(True,'INVALID_FIELD_TYPE'),([], 'INVALID_FIELD_TYPE'),({},'INVALID_FIELD_TYPE'),('NaN','EXACT_DECIMAL_REQUIRED'),('Infinity','EXACT_DECIMAL_REQUIRED'),('1e1','EXACT_DECIMAL_REQUIRED')):
   add(axis+'_invalid_'+str(value),body(**{axis:value}),422,code)
  for value in ('NaN','Infinity','-Infinity'):
   add(axis+'_nonfinite_'+value,raw_token(axis,value),422,'NONFINITE_NUMBER')
  raw={'W':'18','L':'20','n':2};del raw[axis]
  add(axis+'_missing',json.dumps(raw).encode(),422,'FIELD_REQUIRED')
 for n in (1,'1','۱'):
  add('n1_'+str(n),body(n=n),409,None,'VALID_UNSUPPORTED')
 for n in (3,4,'3','4','1.5',True,[],{}):
  add('n_invalid_'+str(n),body(n=n),422,'INVALID_BRIEF')
 for token in ('1.5','2.0','2e0'):
  add('n_numeric_'+token,raw_token('n',token),422,'INVALID_BRIEF')
 for n in ('',' ',None):
  add('n_empty_'+str(n),body(n=n),422,'INPUT_REQUIRED')
 add('n_missing',b'{"W":"18","L":"20"}',422,'INPUT_REQUIRED')
 for extra in ('requested_count','program','bedrooms','capability','accepted','mode'):
  add('extra_'+extra,body(**{extra:1}),422,'UNEXPECTED_PUBLIC_FIELD')
 add('duplicate',b'{"W":18,"W":19,"L":20,"n":2}',422,'DUPLICATE_FIELD')
 add('escaped_duplicate',b'{"W":18,"\\u0057":19,"L":20,"n":2}',422,'DUPLICATE_FIELD')
 add('nonobject',b'[]',422,'OBJECT_REQUIRED')
 add('malformed',b'{',422,'JSON_SYNTAX_INVALID')
 return cases
class P03(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.before=snapshot()
 @classmethod
 def tearDownClass(cls):
  if snapshot()!=cls.before:raise AssertionError('P03_FINAL_SOURCE_CHANGED')
 def test_exact_decimal_roundtrip_both_axes(self):
  values=['5','25','12.5','5.000000000000000001','24.'+'1'*61,'۱۸٫۱','١٢٫٥']
  for axis in ('W','L'):
   for text in values:
    b=body(**{axis:text});e=v3.parse_public(b);original=copy.deepcopy(e)
    self.assertEqual(v3.verify_public(b,e),original)
    converted=v3.engine_raw(e);normalized=text.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩٫','01234567890123456789.'))
    expected=Fraction(normalized)
    self.assertEqual(Fraction(converted[axis]),expected)
    self.assertEqual(e['canonical_request']['dimensions_m'][axis],{'numerator':str(expected.numerator),'denominator':str(expected.denominator)})
    self.assertEqual(e,original);self.assertEqual(e['received_input'][axis],text)
    self.assertEqual(v3.verify_public(b,e),e)
  with self.assertRaises(InputError)as ex:v3.parse_public(body(W='24.'+'1'*62))
  self.assertEqual((ex.exception.status,ex.exception.code),(409,'UNSUPPORTED_NUMERIC_LENGTH'))
 def test_units_separate_validity_from_capability(self):
  for n in (1,2,'1','2','۱','۲'):
   e=v3.parse_public(body(n=n));self.assertIn(e['canonical_request']['unit_count'],(1,2))
   if e['canonical_request']['unit_count']==1:
    with self.assertRaises(InputError)as ex:v3.engine_raw(e)
    self.assertEqual((ex.exception.status,ex.exception.code),(409,'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT'))
   else:self.assertEqual(v3.engine_raw(e)['n'],2)
 def test_contract_matrix_primary_preserved(self):
  for name,b,status,code,kind in matrix():
   with self.subTest(case=name):
    if kind=='VALID_UNSUPPORTED':
     e=v3.parse_public(b);self.assertEqual(diagnostic.parse_public_errors(b),e)
    else:
     with self.assertRaises(InputError)as original:v3.parse_public(b)
     with self.assertRaises(InputError)as enriched:diagnostic.parse_public_errors(b)
     self.assertEqual((original.exception.status,original.exception.code),(status,code))
     self.assertEqual((enriched.exception.status,enriched.exception.code),(status,code))
     self.assertIs(diagnostic.response(enriched.exception)['generation_started'],False)
 def test_original_bytes_and_typed_envelope_binding(self):
  b=body(W='18.125');e=v3.parse_public(b)
  with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):v3.verify_public(b+b' ',e)
  for key,value in [('accepted',0),('qualified',True),('schema','FORGED')]:
   q=copy.deepcopy(e);q[key]=value
   with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):v3.verify_public(b,q)
  q=copy.deepcopy(e);q['canonical_request']['unit_count']=True
  with self.assertRaisesRegex(InputError,'ENVELOPE_BINDING_CHANGED'):v3.engine_raw(q)
 def test_real_http_both_registered_services_zero_dispatch(self):
  import public_wln_server as public
  import request_trace109 as trace
  services=(('PUBLIC_WLN_18X20',public),('REQUEST_TRACE_18X22',importlib.import_module('request_trace_server109')))
  for service,module in services:
   s=launch.server(service);t=threading.Thread(target=s.serve_forever,daemon=True);t.start()
   errors=[];s.handle_error=lambda *args:errors.append('HANDLER_EXCEPTION')
   try:
    with ExitStack()as stack:
     live=stack.enter_context(patch.object(public,'run_live',side_effect=AssertionError('P03_DISPATCH_FORBIDDEN')))
     request=stack.enter_context(patch.object(trace,'make_request',side_effect=AssertionError('P03_REQUEST_FORBIDDEN')))
     spawn=stack.enter_context(patch('subprocess.Popen',side_effect=AssertionError('P03_SUBPROCESS_FORBIDDEN')))
     for name,b,status,code,kind in matrix():
      with self.subTest(service=service,case=name):
       c=http.client.HTTPConnection('127.0.0.1',s.server_port,timeout=10)
       try:
        c.request('POST','/api/public/plan',body=b,headers={'Content-Type':'application/json'})
        response=c.getresponse();data=response.read();payload=json.loads(data)
       finally:c.close()
       self.assertEqual(response.status,status)
       for k in AUTH:self.assertIs(payload[k],False)
       if kind=='VALID_UNSUPPORTED':
        e=v3.parse_public(b);self.assertIn(e['canonical_request']['unit_count'],(1,2))
        self.assertNotEqual(payload.get('schema'),diagnostic.SCHEMA)
        state=payload.get('status')or payload.get('code')
        self.assertIn(state,('UNSUPPORTED_SELECTED_SAME_VERSION_CASE','UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT','BLOCKED'))
        if state=='BLOCKED':self.assertEqual(payload['study_result']['state'],'UNSUPPORTED_TRACE_STUDY_CONTRACT')
        if service=='PUBLIC_WLN_18X20':self.assertIs(payload['input_valid'],True)
        elif payload.get('study_result'):self.assertIs(payload['study_result']['input_valid'],True)
        else:self.assertIs(payload['input_valid'],True)
       else:
        self.assertEqual(payload['code'],code);self.assertEqual(payload['primary_status'],status)
        self.assertEqual(payload['acceptance_contract'],v3.SCHEMA)
        self.assertIs(payload['generation_started'],False)
       HTTP_OBSERVATIONS.append({'service':service,'case':name,'kind':kind,'http_status':response.status,'code':payload.get('code'),'state':payload.get('status'),'response_digest':hashlib.sha256(data).hexdigest()})
     live.assert_not_called();request.assert_not_called();spawn.assert_not_called()
   finally:s.shutdown();s.server_close();t.join(timeout=5)
   self.assertFalse(t.is_alive());self.assertEqual(errors,[]);self.assertFalse(module.LOCK.locked())
 def test_current_direct_dispatch_invalid_before_producer_import(self):
  for name,b,status,code,kind in matrix():
   if kind=='VALID_UNSUPPORTED':continue
   for call in (lambda:boundary.propose_current(b),lambda:boundary.construct_current(b,{})):
    with self.subTest(case=name),patch.object(boundary.importlib,'import_module',side_effect=AssertionError('PRODUCER_IMPORT_FORBIDDEN'))as imported:
     with self.assertRaises(InputError)as ex:call()
     self.assertEqual((ex.exception.status,ex.exception.code),(status,code));imported.assert_not_called()
 def test_direct_valid_n1_no_producer(self):
  with patch.object(boundary.importlib,'import_module',side_effect=AssertionError('PRODUCER_IMPORT_FORBIDDEN'))as imported:
   for call in (lambda:boundary.propose_current(body(n=1)),lambda:boundary.construct_current(body(n=1),{})):
    with self.assertRaises(InputError)as ex:call()
    self.assertEqual((ex.exception.status,ex.exception.code),(409,'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT'))
   imported.assert_not_called()
 def test_model_raw_and_prepared_bindings(self):
  for axis in ('W','L'):
   for value in ('5','25','18.125'):
    raw={'W':'18','L':'22','n':2,'requested_count':1};raw[axis]=value
    self.assertTrue(boundary.check_model_domain({'inputs':[raw['W'],raw['L'],2]})['input_valid'])
    self.assertEqual(boundary.check_raw_domain(raw)['canonical_request']['dimensions_m'][axis],v3.parse_public(body(**{axis:value}))['canonical_request']['dimensions_m'][axis])
   for value in ('4.999','25.001',True,None):
    raw={'W':'18','L':'22','n':2,'requested_count':1};raw[axis]=value
    with self.assertRaises(InputError):boundary.check_raw_domain(raw)
    with self.assertRaises(InputError):boundary.check_model_domain({'inputs':[raw['W'],raw['L'],2]})
  b=body(L='22');p=boundary.prepare('SOURCE_FIT207_COMPACT_PAIR',b)
  self.assertEqual(boundary.validate_prepared(p,b),p)
  q=copy.deepcopy(p);q['raw']['W']='26'
  with self.assertRaisesRegex(ValueError,'CURRENT_REQUEST_BINDING'):boundary.validate_prepared(q,b)
 def test_preflight_readiness_is_not_generation(self):
  import live_program_scheduler as scheduler
  import request_trace109 as trace
  with patch('subprocess.Popen',side_effect=AssertionError('P03_SUBPROCESS_FORBIDDEN'))as spawn:
   self.assertTrue(scheduler.preflight(body())['execution_ready'])
   self.assertFalse(scheduler.preflight(body(n=1))['execution_ready'])
   self.assertFalse(scheduler.preflight(body(W='18.125'))['execution_ready'])
   self.assertTrue(trace.preflight(body(L='22'))['execution_ready'])
   # Actual historical deadline remains in force; no synthetic clock reactivation.
   with self.assertRaisesRegex(ValueError,'TASK_TIMEBOX_EXPIRED'):trace.make_request(body(L='22'))
   spawn.assert_not_called()
 def test_current_surface_registry_and_legacy_exclusion(self):
  self.assertEqual(set(launch.SERVICES),{'PUBLIC_WLN_18X20','REQUEST_TRACE_18X22'})
  self.assertEqual(set(boundary.REGISTRY),{'SOURCE_FIT207_COMPACT_PAIR','CONSTRUCTOR127_COMPACT_PAIR'})
  for name in ('validation_server','frontend','backend','current','latest','engine','contract114','unknown'):
   with patch.object(launch.importlib,'import_module',side_effect=AssertionError('IMPORT_FORBIDDEN'))as imported:
    with self.assertRaisesRegex(ValueError,'HISTORICAL_SERVICE_CURRENT_DISABLED'):launch.server(name)
    imported.assert_not_called()
 def test_legacy_parser_not_current_acceptance(self):
  from contract114 import parse
  self.assertEqual(parse({'W':'26','L':'20','n':2})[0],26)
  with self.assertRaisesRegex(InputError,'DIMENSION_OUT_OF_OWNER_RANGE'):v3.parse_public(body(W='26'))
  with self.assertRaises(InputError):boundary.check_model_domain({'inputs':['26','20',2]})
 def test_form_preserves_strings_and_three_fields(self):
  from html.parser import HTMLParser
  class Fields(HTMLParser):
   def __init__(self):super().__init__();self.fields=[]
   def handle_starttag(self,tag,attrs):
    if tag=='input':self.fields.append(dict(attrs))
  parser=Fields();parser.feed((ROOT/'app/local_integration/public_wln.html').read_text())
  self.assertEqual([x['name']for x in parser.fields],['W','L','n'])
  self.assertTrue(all(x['type']=='text'for x in parser.fields))
  js=(ROOT/'app/local_integration/public_wln.js').read_text()
  self.assertIn('W:form.elements.W.value,L:form.elements.L.value,n:form.elements.n.value',js)
  self.assertNotIn('parseFloat(',js);self.assertNotIn('Number(',js)
 def test_source_and_actual_callable_paths(self):
  self.assertEqual(snapshot(),self.before)
  for fn,path in ((v3.parse_public,'public_wln_contract.py'),(v3.engine_raw,'public_wln_contract.py'),(diagnostic.parse_public_errors,'public_input_errors403.py'),(boundary.public_request,'current_entry_boundary_x03.py'),(launch.server,'current_entry_launch_x03.py')):
   self.assertEqual(Path(inspect.getsourcefile(fn)).resolve(),ROOT/'app/local_integration'/path)
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(P03))
 print(json.dumps({'task':'P03','base_commit':BASE,'tests_run':result.testsRun,'successful':result.wasSuccessful(),
 'http_observations':HTTP_OBSERVATIONS,'http_cases':len(HTTP_OBSERVATIONS),'matrix_cases_per_service':len(matrix()),
 'source_snapshot':snapshot(),'product_code_changed':False,'geometry_executed':False,'qualification_established':False,
 'scope':'CURRENT_V3_INPUT_CONTRACT_AND_REAL_LOOPBACK_HTTP; NO_LEGACY_ISOLATION_OR_PARAMETRIC_READINESS_CLAIM'},sort_keys=True),flush=True)
 raise SystemExit(0 if result.wasSuccessful()else 1)
