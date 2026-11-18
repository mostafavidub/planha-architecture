"""Pure parser/identity/dispatch tests; no server/constructor/reviewer launch."""
import unittest,json,copy,ast
from pathlib import Path
from contract375 import parse_json,bind,decision,partial,W,HERE,digest
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
  p=W/'review372_actual_v1';self.r=json.loads((p/'repaired_record.json').read_text());self.f=json.loads((p/'fresh.json').read_text());self.l=json.loads((p/'reviewed_lineage.json').read_text());self.e=parse_json('{"W":26,"L":28,"n":2,"requested_count":2}');self.run=self.l['run_id']
 def call(self):return bind(self.e,self.r,self.f,self.run,self.l)
 def test_child_id_retained(self):self.assertEqual(self.call()['candidate_id'],self.l['candidate_id'])
 def test_child_lineage_tamper(self):
  self.l['record_digest']='wrong'
  with self.assertRaises(ValueError):self.call()
 def test_lineage_run_tamper(self):
  self.l['run_id']='wrong'
  with self.assertRaises(ValueError):self.call()
 def test_raw_provenance_tamper(self):
  self.f['provenance']['raw']['W']='27'
  with self.assertRaises(ValueError):self.call()
 def test_raw_report_model_tamper(self):
  self.f['raw_report']['model_hash']='wrong'
  with self.assertRaises(ValueError):self.call()
 def test_uuid(self):
  self.run='bad'
  with self.assertRaises(ValueError):self.call()
 def test_empty_review(self):
  self.f['review_id']=''
  with self.assertRaises(ValueError):self.call()
 def test_model_tamper(self):
  self.r['candidate']['model']['program']['units']=3
  with self.assertRaises(ValueError):self.call()
class Dispatch(unittest.TestCase):
 def test_pass_no_repair(self):self.assertEqual(decision({'status':'PASS_CONCEPT_SCOPED_REVIEW','errors':[],'pending':[]}),'NO_REPAIR_CURRENT_PASS')
 def test_unknown_no_repair(self):self.assertEqual(decision({'status':'UNKNOWN','errors':[],'pending':[]}),'STOP_NOT_UNAMBIGUOUS_FAIL')
 def test_fail_unsupported(self):self.assertEqual(decision({'status':'FAIL','errors':[{'code':'OTHER'}],'pending':[]}),'STOP_NO_SUPPORTED_WITNESS')
 def test_fail_only_routes_to_strict_gate(self):self.assertEqual(decision({'status':'FAIL','errors':[{'code':'FIXTURE_COLLISION'}],'pending':[]}),'REQUIRES_BOUND_OPERATOR_GATE')
 def test_partial_flags(self):
  x=partial('QUALITY_UNRESOLVED','run');self.assertEqual(x['requested_count'],2);self.assertEqual(x['tested_branch_count'],1);self.assertFalse(x['request_fulfilled']);self.assertFalse(x['accepted'])
 def test_sources_parse_and_browser_no_owner_kill(self):
  for p in HERE.glob('*.py'):ast.parse(p.read_text())
  t=ast.parse((HERE/'browser375.py').read_text());self.assertFalse(any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ('kill','terminate')for n in ast.walk(t)))
class OwnerSafety(unittest.TestCase):
 def execute_owner(self,broken):
  import tempfile,threading,sys
  from unittest.mock import Mock
  node=next(n for n in ast.parse((HERE/'server375.py').read_text()).body if isinstance(n,ast.FunctionDef)and n.name=='work')
  clean={'cleanup_verified':True,'worker_reaped':True,'unresolved':[],'reason':'COMPLETED','worker_returncode':0}
  sup=Mock(side_effect=RuntimeError('TEST_SUPERVISOR_EXCEPTION'))if broken else Mock(return_value=clean)
  ns={'json':json,'sys':sys,'HERE':HERE,'expected':'TEST','supervise':sup,'guard':Mock(),'partial':partial,'jobs':{},'active':True,'unsafe':False,'lock':threading.Lock()}
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<EXACT_WORK_SAFETY_TEST>','exec'),ns)
  with tempfile.TemporaryDirectory()as temp:
   folder=Path(temp)
   if not broken:(folder/'result.json').write_text(json.dumps(partial('QUALITY_UNRESOLVED','run')))
   ns['work']('run',folder)
  return ns
 def test_supervisor_exception_remains_unsafe(self):
  ns=self.execute_owner(True);self.assertTrue(ns['unsafe']);self.assertFalse(ns['active']);self.assertEqual(ns['jobs']['run']['semantic_state'],'UNKNOWN_OWNER_FAILURE')
 def test_clean_receipt_allows_idle_shutdown(self):
  ns=self.execute_owner(False);self.assertFalse(ns['unsafe']);self.assertFalse(ns['active']);self.assertEqual(ns['jobs']['run']['state'],'QUALITY_UNRESOLVED')
if __name__=='__main__':unittest.main()
