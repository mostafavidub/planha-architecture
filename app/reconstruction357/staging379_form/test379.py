"""Pure parser/binding on stored actual378 evidence and mocked owner tests.
These are not a new source run, fresh review or browser submission.
"""
import unittest,json,copy,ast,sys
from pathlib import Path
from contract379 import parse_json,bind,partial,W,HERE,digest
class Parser(unittest.TestCase):
 def test_persian(self):
  r=parse_json('{"W":"۲۶","L":"۲۸","n":"۲","requested_count":"۲"}')
  self.assertEqual(r['normalized_raw'],{'W':'26','L':'28','n':2,'requested_count':2})
 def test_injected_fields(self):
  for k in ('model','review','proof','fixture'):
   with self.assertRaises(ValueError):parse_json(json.dumps({'W':26,'L':28,'n':2,'requested_count':2,k:{}}))
 def test_duplicates(self):
  with self.assertRaises(ValueError):parse_json('{"W":26,"W":26,"L":28,"n":2,"requested_count":2}')
 def test_floats(self):
  with self.assertRaises(ValueError):parse_json('{"W":26.0,"L":28,"n":2,"requested_count":2}')
 def test_scope(self):
  with self.assertRaises(ValueError):parse_json('{"W":27,"L":28,"n":2,"requested_count":2}')
class Binding(unittest.TestCase):
 def setUp(self):
  p=W/'independent378actual/evidence/review378_actual_v1';self.r=json.loads((p/'record.json').read_text());self.f=json.loads((p/'fresh.json').read_text());self.e=parse_json('{"W":"۲۶","L":"۲۸","n":"۲","requested_count":"۲"}');self.run=self.r['trace']['run_id']
 def call(self):return bind(self.e,self.r,self.f,self.run)
 def test_original_source_id_retained(self):
  b=self.call();self.assertEqual(b['candidate_id'],self.r['candidate_id']);self.assertEqual(b['review_id'],self.f['review_id']);self.assertEqual(b['dispatch']['reason'],'NO_CURRENT_REJECTION_SCOPED_PHYSICAL_ONLY')
 def test_uuid_tamper(self):
  self.run='bad'
  with self.assertRaises(ValueError):self.call()
 def test_identity_tamper(self):
  self.r['candidate_id']='wrong'
  with self.assertRaises(ValueError):self.call()
 def test_raw_provenance_tamper(self):
  self.f['provenance']['raw']['W']='27'
  with self.assertRaises(ValueError):self.call()
 def test_raw_report_model_tamper(self):
  self.f['raw_report']['model_hash']='wrong'
  with self.assertRaises(ValueError):self.call()
 def test_model_tamper(self):
  self.r['candidate']['model']['program']['units']=3
  with self.assertRaises(ValueError):self.call()
 def test_envelope_tamper(self):
  self.e['received_digest']='wrong'
  with self.assertRaises(ValueError):self.call()
 def test_registry_tamper(self):
  self.f['expected_method_registry']['methods']={}
  with self.assertRaises(ValueError):self.call()
 def test_review_uuid(self):
  self.f['review_id']='bad'
  with self.assertRaises(ValueError):self.call()
 def test_rank_tamper(self):
  self.r['trace']['selection_rank']=0
  with self.assertRaises(ValueError):self.call()
class Scope(unittest.TestCase):
 def test_partial(self):
  x=partial('COMPLETED_PENDING_SEMANTICS','run');self.assertFalse(x['test_only']);self.assertTrue(x['experimental']);self.assertFalse(x['accepted']);self.assertFalse(x['request_fulfilled']);self.assertEqual(x['semantic_state'],'UNKNOWN_PENDING_VALIDATION')
 def test_sources_parse_and_no_owner_kill(self):
  for p in HERE.glob('*.py'):ast.parse(p.read_text())
  t=ast.parse((HERE/'browser379.py').read_text());self.assertFalse(any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in('kill','terminate')for n in ast.walk(t)))
 def test_ui_only_four_fields_one_post(self):
  s=(HERE/'index.html').read_text();self.assertEqual(s.count('<input '),4);self.assertEqual(s.count("method:'POST'"),1);self.assertNotIn('TEST_ONLY',s)
class OwnerSafety(unittest.TestCase):
 def execute_owner(self,broken):
  import tempfile,threading,sys
  from unittest.mock import Mock
  node=next(n for n in ast.parse((HERE/'server379.py').read_text()).body if isinstance(n,ast.FunctionDef)and n.name=='work')
  clean={'cleanup_verified':True,'worker_reaped':True,'unresolved':[],'reason':'COMPLETED','worker_returncode':0}
  sup=Mock(side_effect=RuntimeError('TEST_SUPERVISOR_EXCEPTION'))if broken else Mock(return_value=clean)
  ns={'json':json,'sys':sys,'HERE':HERE,'expected':'TEST','supervise':sup,'guard':Mock(),'partial':partial,'jobs':{},'active':True,'unsafe':False,'lock':threading.Lock()}
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<EXACT_WORK_SAFETY_TEST>','exec'),ns)
  with tempfile.TemporaryDirectory()as temp:
   folder=Path(temp)
   if not broken:(folder/'result.json').write_text(json.dumps(partial('COMPLETED_PENDING_SEMANTICS','run')))
   ns['work']('run',folder)
  return ns
 def test_supervisor_exception_remains_unsafe(self):
  ns=self.execute_owner(True);self.assertTrue(ns['unsafe']);self.assertFalse(ns['active']);self.assertEqual(ns['jobs']['run']['semantic_state'],'UNKNOWN_OWNER_FAILURE')
 def test_clean_receipt_allows_idle_shutdown(self):
  ns=self.execute_owner(False);self.assertFalse(ns['unsafe']);self.assertFalse(ns['active']);self.assertEqual(ns['jobs']['run']['state'],'COMPLETED_PENDING_SEMANTICS')
if __name__=='__main__':unittest.main()
