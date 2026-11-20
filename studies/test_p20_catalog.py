"""P20 actual inventory/primitive/decision tests, synthetic data, no generator."""
import copy,json,sys,unittest
from unittest.mock import patch
from fractions import Fraction as F
from pathlib import Path
from p20_catalog_audit import CATALOG,ROOT,validate
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
from current_programme_evaluator import proven_capacity_violation
from source_guest_route_evaluator import route_check
from source_living_evaluator import union_area
from source_wall_counterfactual import exact_closure_change
from geometry114 import cells
from current_four_decision import decide,SCHEMAS
class CatalogTests(unittest.TestCase):
 def setUp(self):
  self.data=json.loads(CATALOG.read_text())
  self.spawn=patch('subprocess.Popen',side_effect=AssertionError('NO_PROCESS_ALLOWED')).start()
  self.milp=patch('scipy.optimize.milp',side_effect=AssertionError('NO_SOLVER_ALLOWED')).start()
  self.addCleanup(patch.stopall)
 def tearDown(self):
  self.spawn.assert_not_called();self.milp.assert_not_called()
 def test_current_inventory(self):
  self.assertEqual(validate(self.data),{'conditions':23,'criteria':4,'bound_evaluator_files':8,'geometry_executed':False,'qualified':False})
 def test_missing_source_rejected(self):
  self.data['criteria'][0]['conditions'][0]['source_refs']=[]
  with self.assertRaisesRegex(ValueError,'UNSOURCED_CONDITION'):validate(self.data)
 def test_invented_source_rejected(self):
  self.data['criteria'][0]['conditions'][0]['source_refs']=['UNAPPROVED_RULE']
  with self.assertRaisesRegex(ValueError,'UNSOURCED_CONDITION'):validate(self.data)
 def test_arbitrary_threshold_rejected(self):
  self.data['criteria'][2]['conditions'][0]['numeric_thresholds_added']=[.45]
  with self.assertRaisesRegex(ValueError,'UNAUTHORIZED_THRESHOLD'):validate(self.data)
 def test_condition_cannot_grant_pass(self):
  self.data['criteria'][3]['conditions'][-1]['aggregate_effect']='PASS'
  with self.assertRaisesRegex(ValueError,'CONDITION_PROMOTION'):validate(self.data)
 def test_out_of_scope_not_pass_policy(self):
  self.data['aggregate_policy']['out_of_scope_is_not_pass']=False
  with self.assertRaisesRegex(ValueError,'AGGREGATE_POLICY'):validate(self.data)
 def test_unknown_not_stored_assessment_pass(self):
  self.data['criteria'][0]['current_state']='PASS'
  with self.assertRaisesRegex(ValueError,'CATALOG_IS_NOT_ASSESSMENT'):validate(self.data)
 def test_missing_condition_rejected(self):
  self.data['criteria'][1]['conditions'].pop()
  with self.assertRaisesRegex(ValueError,'CONDITION_SET'):validate(self.data)
 def test_changed_implementation_pin_rejected(self):
  self.data['criteria'][0]['implementation_bindings'][0]['git_blob']='0'*40
  with self.assertRaisesRegex(ValueError,'IMPLEMENTATION_CHANGED'):validate(self.data)
 def test_wrong_entrypoint_rejected(self):
  self.data['criteria'][0]['implementation_bindings'][0]['entry']='invented'
  with self.assertRaisesRegex(ValueError,'ENTRYPOINT'):validate(self.data)
 def test_no_private_locator_added(self):
  self.data['private']='https://docs.google.com/document/private'
  with self.assertRaisesRegex(ValueError,'PRIVATE_LOCATOR'):validate(self.data)
 def test_open_decision_missing_rejected(self):
  self.data['open_decisions'].pop()
  with self.assertRaisesRegex(ValueError,'OPEN_DECISION_SET'):validate(self.data)
 def test_open_calibration_not_falsely_completed(self):
  self.data['open_decisions'][0]['implemented_by_this_task']=True
  with self.assertRaisesRegex(ValueError,'OPEN_DECISION_CLAIM'):validate(self.data)
 def test_not_applicable_not_dropped(self):
  self.data['condition_result_vocabulary'].pop('NOT_APPLICABLE')
  with self.assertRaisesRegex(ValueError,'CONDITION_RESULT_VOCABULARY'):validate(self.data)
 def states(self,state='UNKNOWN'):return {k:state for k in SCHEMAS}
 def physical(self):return {'status':'PASS_CONCEPT_SCOPED_REVIEW','errors':[],'pending':[]}
 def test_actual_capacity_violation_and_fail_decision(self):
  cap={'errors':[{'code':'ACTUAL_CAPACITY_SHORTFALL'}],'evidence':{'units':[]}}
  self.assertTrue(proven_capacity_violation(cap))
  states=self.states();states['CURRENT_PROGRAM_SUITABILITY']='FAIL'
  out=decide(self.physical(),states)
  self.assertIn('CURRENT_NECESSARY_FAIL',out['blockers']);self.assertIn('CURRENT_UNKNOWN',out['blockers'])
  self.assertFalse(out['qualified']);self.assertEqual(out['state'],'BLOCKED')
 def test_missing_capacity_evidence_not_proven_fail_or_pass(self):
  self.assertFalse(proven_capacity_violation({'errors':[],'evidence':{'units':[]}}))
  out=decide(self.physical(),self.states())
  self.assertIn('CURRENT_UNKNOWN',out['blockers']);self.assertFalse(out['current_four_conditions_complete'])
 def test_out_of_scope_actual_decision_not_pass(self):
  states=self.states('PASS');states['NONFUNCTIONAL_WALL_EXCLUSION']='NOT_EVALUATED'
  out=decide(self.physical(),states)
  self.assertIn('CURRENT_NOT_EVALUATED',out['blockers']);self.assertFalse(out['current_four_conditions_complete'])
 def test_even_four_pass_not_product_qualification(self):
  out=decide(self.physical(),self.states('PASS'))
  self.assertEqual(out['state'],'FOUR_CURRENT_CHECKS_COMPLETE_NOT_PRODUCT_QUALIFIED')
  for k in ('qualified','accepted','display_allowed','delivery_allowed'):self.assertIs(out[k],False)
 def test_actual_body_collision_rejects_witness(self):
  with self.assertRaisesRegex(ValueError,'ROUTE_OBSTACLE_COLLISION'):
   route_check([['1','1'],['3','1']],['1','1'],['3','1'],F('.7'),[['0','0','4','2']],[['1.5','1.1','2','1.3']])
  # A rejected supplied path does not prove absence of every possible path.
  self.assertEqual(decide(self.physical(),self.states())['state'],'BLOCKED')
 def test_actual_clear_path_only_scoped_witness(self):
  self.assertEqual(route_check([['1','1'],['3','1']],['1','1'],['3','1'],F('.7'),[['0','0','4','2']],[]),1)
  self.assertFalse(decide(self.physical(),self.states())['current_four_conditions_complete'])
 def test_living_area_not_connectivity_or_useful_area(self):
  self.assertEqual(union_area([['0','0','1','1'],['2','0','3','1']]),F(2))
  with self.assertRaisesRegex(ValueError,'ROUTE_DOMAIN_COVERAGE'):
   route_check([['.5','.5'],['2.5','.5']],['.5','.5'],['2.5','.5'],F('.7'),[['0','0','1','1'],['2','0','3','1']],[])
 def test_wall_alias_no_material_benefit(self):
  q=['0','0','2','1'];self.assertEqual(cells([q,q],[q]),[])
  row=next(r for r in self.data['criteria'] if r['id']=='NONFUNCTIONAL_WALL_EXCLUSION')
  self.assertTrue(any(r['id']=='P20_WALL_ALIAS_MATERIAL' for r in row['conditions']))
 def test_boundary_dependency_not_necessity_pass(self):
  region=[tuple(map(F,[0,0,2,2]))];wall=[tuple(map(F,[-1,0,0,2]))]
  rows=exact_closure_change(region,wall,[],[])
  self.assertTrue(any(r['newly_missing'] for r in rows))
  self.assertFalse(decide(self.physical(),self.states())['qualified'])
if __name__=='__main__':unittest.main()
