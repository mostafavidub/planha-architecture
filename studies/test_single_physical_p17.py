"""P17 physical adapter: no solver, schema/typed binding and derivative retention.
Minimal identity fixtures do NOT constitute a valid complete model or physics PASS.
The real n1 physical path is verified by the separately authorized HTTP live run.
"""
import copy,inspect,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import single_model_p15 as p
import single_physical_p17 as a
import checker114
class PhysicalContract(unittest.TestCase):
 def setUp(self):
  self.raw=copy.deepcopy(p.RAW);self.proposal={'bedrooms':2,'sleep_roles':['double','twin']}
  c=p.core(self.raw)
  self.model={'schema':p.FAMILY,'contract_version':'p15-single-v1','inputs':['18','20',1],
   'units':[{'id':'A','ownership':copy.deepcopy(c['unit_ownership']['A'])}],'program':{'units':1},
   'common_spaces':{k:copy.deepcopy(c[k])for k in('stair','lift','lobby')},
   'construction_identity':{'family':p.FAMILY,'raw_digest':p.digest(self.raw),'core_digest':p.digest(c),
    'proposal_digest':p.digest(self.proposal),'programme_digest':p.digest(p.lookup('PROGRAM_2BED_V1')),
    'unit_assignment':{'A':p.digest(self.proposal)},'pair_built_then_filtered':False},**{k:False for k in p.AUTH}}
 def test_identity_only_not_physics(self):
  a.validate_identity(self.model,self.raw,self.proposal)
 def test_pair_rejected(self):
  self.model['units'].append({'id':'B'})
  with self.assertRaisesRegex(ValueError,'SINGLE_UNIT_INVENTORY'):a.validate_identity(self.model,self.raw,self.proposal)
 def test_request_n2_rejected(self):
  self.raw['n']=2
  with self.assertRaisesRegex(ValueError,'SINGLE_RAW_BINDING'):a.validate_identity(self.model,self.raw,self.proposal)
 def test_float_unit_count(self):
  self.model['inputs'][2]=1.0
  with self.assertRaisesRegex(ValueError,'SINGLE_TYPED_INPUT'):a.validate_identity(self.model,self.raw,self.proposal)
 def test_bool_program_count(self):
  self.model['program']['units']=True
  with self.assertRaisesRegex(ValueError,'SINGLE_PROGRAM_UNIT_COUNT'):a.validate_identity(self.model,self.raw,self.proposal)
 def test_core_change_even_rehashed_identity(self):
  self.model['common_spaces']['stair'][0]='.5'
  with self.assertRaisesRegex(ValueError,'SINGLE_CORE_BINDING'):a.validate_identity(self.model,self.raw,self.proposal)
 def test_old_contract(self):
  self.model['contract_version']='114-provisional-v1'
  with self.assertRaisesRegex(ValueError,'SINGLE_MODEL_SCHEMA'):a.validate_identity(self.model,self.raw,self.proposal)
 def test_hidden_owner(self):
  self.model['units'][0]['ownership'].append(['1','1','2','2'])
  with self.assertRaisesRegex(ValueError,'SINGLE_OWNERSHIP'):a.validate_identity(self.model,self.raw,self.proposal)
 def test_context_old_schema(self):
  with self.assertRaisesRegex(ValueError,'SINGLE_CONTEXT_SCHEMA'):a.verify_context(self.model,{'schema':'CONSTRUCTION_TRACE127_PAIR_V1'})
 def test_no_fake_legacy_prefix(self):
  self.assertFalse(a.VERSION.startswith(('GENERAL117_','GENERAL118_')))
  with self.assertRaises(ValueError):a.reduce_scope117({'checker_version':checker114.VERSION,'errors':[],'pending':[]})
 def test_scope_keeps_fail_and_unknown(self):
  r={'checker_version':a.VERSION,'errors':[{'code':'ORIGINAL_FAIL'}],'pending':['UNKNOWN_EVIDENCE','VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED'],'status':'FAIL'}
  result=a.reduce_scope117(r)
  self.assertEqual(result['errors'],r['errors']);self.assertIn('UNKNOWN_EVIDENCE',result['pending'])
  self.assertIn('VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED',result['not_evaluated'])
  self.assertEqual(result['status'],'FAIL')
 def test_source_guard_actual(self):
  self.assertIn('physical_adapter',a.source_guard())
 def test_exact_physical_derivative(self):
  source=inspect.getsource(checker114._evaluate_impl)
  changes=[
   ('not 5<=W<=45 or not 5<=L<=45 or n!=2','not 5<=W<=25 or not 5<=L<=25 or n!=1'),
   ("model.get('contract_version')not in ('114-provisional-v1','115-provisional-v1')","model.get('contract_version')!='p15-single-v1'"),
   ('len(units)!=2','len(units)!=1'),
   ("Path(__file__).with_name('fixture_catalog114.json')","(ENGINE/'fixture_catalog114.json')"),
   ('Path(__file__).parent','ENGINE'),
   ('from scope117 import reduce_scope117',''),
   ('from q11_boundary118 import examine as examine_q11',''),
   ('from rule_contract118 import attach_rule_contract',''),
   ('from named_checks118 import adapters_for_workflow,APPLICABILITY_ADAPTERS',''),
   ('adapters=adapters_for_workflow(workflow_context)','adapters=adapters_for_single_workflow(workflow_context)'),
   ('applicability_evaluators=APPLICABILITY_ADAPTERS',"applicability_evaluators={'long_corridor_necessity':single_applicability}")]
  for old,new in changes:
   self.assertIn(old,source);source=source.replace(old,new)
  self.assertEqual(inspect.getsource(a._evaluate_impl).strip(),source.strip())
if __name__=='__main__':unittest.main()
