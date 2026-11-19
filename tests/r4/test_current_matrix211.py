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
  from producer_provenance import snapshot
  r['schema']=m.SCHEMAS['source_guest_route_evaluator'];r['current_domain_policy']='CURRENT_ENTRY_DOMAIN_X03_V1'
  r['source_snapshot']=snapshot(m.ROOT,m.SOURCES['source_guest_route_evaluator'])
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

 def test_nonjson_preserves_prior_reports(self):
  prior={'physical':{'status':'FAIL'}};before=m.digest(prior)
  for value in ({'units':()}, {'number':float('nan')}):
   capture,ok=m.capture_returned(value);self.assertFalse(ok);self.assertEqual(capture['state'],'EVALUATOR_ERROR')
  self.assertEqual(m.digest(prior),before)
 def test_returned_json_exact_types(self):
  for value in ({'n':2.0},{'n':2},{'n':True}):
   captured,ok=m.capture_returned(value);self.assertTrue(ok);self.assertEqual(type(captured['n']),type(value['n']))
 def test_summary_recomputed_from_full_reports(self):
  b,rr=self.report()
  reports={'physical':b['reports']['physical'],'original_replay':rr['replay']}
  reports.update({'current_'+k:copy.deepcopy(rr)for k in m.CURRENT})
  # Programme has its distinct nested report schema.
  pr=reports['current_current_programme_evaluator'];pr['findings']=[];pr['historical_physical_report']=copy.deepcopy(reports['physical']);pr['historical_physical_digest']=m.digest(reports['physical']);pr['reports']={'replay':copy.deepcopy(rr['replay'])};pr['report_digests']={'replay':m.digest(rr['replay'])}
  r={'state':'FULL_REPORTS_RETAINED_NOT_QUALIFIED','completed':True,'model_digest':b['model_digest'],'physical_status':'FAIL','physical_error_counts':m.code_counts(reports['physical']['errors']),'physical_pending_counts':{},'report_digests':{k:m.digest(v)for k,v in reports.items()},'current_assessments':{k:{'state':'UNKNOWN','integrity_verified':True}for k in m.CURRENT}}
  from producer_provenance import snapshot
  for name in m.CURRENT:
   reports['current_'+name]['source_snapshot']=snapshot(m.ROOT,m.SOURCES[name]);reports['current_'+name]['schema']=m.SCHEMAS[name]
  r['report_digests']={k:m.digest(v)for k,v in reports.items()}
  m.recheck_reports(r,reports)
  r['current_assessments'][m.CURRENT[0]]['state']='PASS'
  with self.assertRaises(ValueError):m.recheck_reports(r,reports)

if __name__=='__main__':unittest.main()
