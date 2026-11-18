import unittest,json,sys,copy
from pathlib import Path
from request_contract368 import parse_json,verify,normalize,digest
from model_binding368 import bind
ROOT=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 def test_form_types(self):
  e=parse_json('{"W":"26","L":"28","n":"2","requested_count":"2"}');self.assertEqual(e['received_types']['n'],'str');self.assertIs(type(e['normalized_raw']['n']),int);self.assertEqual(verify(e)['raw_digest'],e['raw_digest'])
 def test_long_exact_decimal(self):
  self.assertEqual(normalize({'W':'26.'+'0'*40,'L':'28.'+'0'*40,'n':2,'requested_count':2})['normalized_raw']['W'],'26')
  for key,v in [('W','26.0000000000000000000000000001'),('W','25.9999999999999999999999999999'),('L','28.0000000000000000000000000001')]:
   d={'W':'26','L':'28','n':2,'requested_count':2};d[key]=v
   with self.assertRaises(ValueError):normalize(d)
 def test_api_types(self):self.assertEqual(parse_json('{"W":26,"L":28,"n":2,"requested_count":2}')['normalized_raw'],{'W':'26','L':'28','n':2,'requested_count':2})
 def test_count_strict(self):
  for x in ('2.0','02',' 2 ','2e0',True,2.0,None):
   with self.subTest(x=x),self.assertRaises(ValueError):normalize({'W':'26','L':'28','n':x,'requested_count':2})
 def test_json_float_bool_nan_duplicate_extra_missing(self):
  for body in ('{"W":26.0,"L":28,"n":2,"requested_count":2}','{"W":NaN,"L":28,"n":2,"requested_count":2}','{"W":true,"L":28,"n":2,"requested_count":2}','{"W":26,"W":26,"L":28,"n":2,"requested_count":2}','{"W":26,"L":28,"n":2,"requested_count":2,"proof":true}','{"W":26,"L":28,"n":2}'):
   with self.subTest(body=body),self.assertRaises(ValueError):parse_json(body)
 def test_lexical_boundaries(self):
  for text in ('026.000',' 26 ', '26.'+'0'*61):self.assertEqual(normalize({'W':text,'L':'28','n':2,'requested_count':2})['normalized_raw']['W'],'26')
  for text in ('2.6e1','26.'+'0'*62):
   with self.assertRaises(ValueError):normalize({'W':text,'L':'28','n':2,'requested_count':2})
 def test_scope(self):
  for k,v in [('W','25'),('L','45'),('n',1),('requested_count',1)]:
   d={'W':'26','L':'28','n':2,'requested_count':2};d[k]=v
   with self.assertRaises(ValueError):normalize(d)
 def test_typed_envelope_tamper(self):
  e=normalize({'W':'26','L':'28','n':2,'requested_count':2});e['normalized_raw']['n']=2.0
  with self.assertRaises(ValueError):verify(e)
 def test_real_fixed_record_bindings(self):
  e=normalize({'W':'26','L':'28','n':2,'requested_count':2})
  for kind,name in [('balanced','staging365_balanced_portals/actual365.json'),('joint','review367_joint_attempt2/actual367.json')]:
   r=json.loads((ROOT/name).read_text());b=bind(e,r,kind,'TEST_ONLY');self.assertEqual(b['unit_ids'],['A','B']);self.assertEqual(len({x['qualified_id']for x in b['entity_ids']}),len(b['entity_ids']))
   q=copy.deepcopy(r);q['candidate']['request']['n']=True
   with self.assertRaises(ValueError):bind(e,q,kind,'TEST_ONLY')
 def test_duplicate_id(self):
  r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());r['candidate']['model']['units'][1]['id']='A';e=normalize({'W':'26','L':'28','n':2,'requested_count':2})
  with self.assertRaises(ValueError):bind(e,r,'joint','TEST_ONLY')
if __name__=='__main__':unittest.main()
