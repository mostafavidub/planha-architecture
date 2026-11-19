import copy,json,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import current_matrix211 as m
class Matrix(unittest.TestCase):
 def report(self):
  p={'model_hash':'a'*64,'status':'FAIL','errors':[{'code':'ORIGINAL_FAIL'}]}
  b={'model_digest':'a'*64,'reports':{'physical':p},'report_digests':{'physical':m.digest(p)}}
  r={'integrity_verified':True,'model_digest':'a'*64,'state':'UNKNOWN','original_physical_report':copy.deepcopy(p),'original_physical_digest':m.digest(p),'replay':{'verified':True,'model_hash':'a'*64},'units':[],**{k:False for k in m.AUTH}}
  return b,r
 def test_n1_valid_unsupported_no_core(self):
  with patch('core_choice_pair_study.selected_core',side_effect=AssertionError('NO_CORE')),patch.object(m,'prepare',side_effect=AssertionError('NO_PREPARE')):
   r=m.eligibility(b'{"W":"18.1","L":"22.2","n":1}')
  self.assertFalse(r['dispatch']);self.assertEqual(r['state'],'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT')
 def test_exact_three_registered_rows(self):
  self.assertEqual(m.CASES,{'D':('18.1','22.2'),'B':('25','25')})
 def test_invalid_before_dispatch(self):
  for body in (b'{"W":"25.001","L":"22.2","n":2}',b'{"W":true,"L":"22.2","n":2}',b'{"W":"18","W":"19","L":"20","n":2}'):
   with self.assertRaises(Exception):m.eligibility(body)
 def test_shared_slot_no_reallocation(self):
  self.assertEqual(m.slot(600),240);self.assertEqual(m.slot(250),240);self.assertEqual(m.slot(249.99),0)
 def test_unknown_with_physical_fail_retained(self):
  b,r=self.report();before=m.digest(r);m.current_report_binding('source_guest_route_evaluator',r,b);self.assertEqual(m.digest(r),before)
 def test_model_mismatch(self):
  b,r=self.report();r['model_digest']='b'*64
  with self.assertRaises(ValueError):m.current_report_binding('source_guest_route_evaluator',r,b)
 def test_integrity_and_authority_rejected(self):
  for field,value in [('integrity_verified',False),('qualified',True),('state','ERROR')]:
   b,r=self.report();r[field]=value
   with self.assertRaises(ValueError):m.current_report_binding('source_guest_route_evaluator',r,b)
 def test_original_report_not_summary(self):
  b,r=self.report();r['original_physical_report']['errors']=[]
  with self.assertRaises(ValueError):m.current_report_binding('source_guest_route_evaluator',r,b)
 def test_nested_execution_error(self):
  b,r=self.report();r['units']=[{'routes':[{'state':'UNKNOWN_EVALUATOR_OR_BINDING_ERROR'}]}]
  with self.assertRaises(ValueError):m.current_report_binding('source_guest_route_evaluator',r,b)
 def test_timeout_invalidates(self):
  r=m.invalidate({'completed':True,'independent_origin_verified':True,'integrity_verified':True},'TIMEOUT')
  self.assertFalse(r['completed']);self.assertFalse(r['independent_origin_verified']);self.assertFalse(r['evidence_usable'])
 def test_summary_nonce_and_partial_current(self):
  r={'case':'D','run_nonce':'n','state':'FULL_REPORTS_RETAINED_NOT_QUALIFIED','completed':True,'independent_origin_verified':True,'integrity_verified':True,'current_assessments':{},**{k:False for k in m.AUTH}}
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'summary.json';p.write_text(json.dumps(r))
   with self.assertRaises(ValueError):m.read_summary(p,'D','wrong')
   with self.assertRaises(ValueError):m.read_summary(p,'D','n')
 def test_unknown_cli_no_batch(self):
  with patch.object(sys,'argv',['current_matrix211.py','--unknown']),patch.object(m,'run',side_effect=AssertionError('NO_RUN')):
   with self.assertRaises(ValueError):m.main()
if __name__=='__main__':unittest.main()
