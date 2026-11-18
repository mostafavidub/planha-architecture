import json,copy,unittest
from pathlib import Path
from actual_opening_geometry121 import evaluate
from rule_contract118 import evaluate_rule_contract
from scope117 import EXCLUDED
class OwnerScope(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads(Path('evidence/program6/deterministic_macro_assembly121.json').read_text())['model']
 def test_absent_windows_not_required(self):
  m=copy.deepcopy(self.m);m['concept_windows']=[];r=evaluate(m);self.assertEqual(r['status'],'PASS_LIMITED')
 def test_no_light_role_or_edge_check(self):
  m=copy.deepcopy(self.m)
  for w in m['concept_windows']:w['room']='NO_LIGHT_ROOM_REQUIREMENT';w['destination']={'edge':'UNKNOWN'}
  self.assertEqual(evaluate(m)['status'],'PASS_LIMITED')
 def test_physical_host_still_fails(self):
  m=copy.deepcopy(self.m);m['concept_windows'][0]['plan_rect']=['-1','-1','1','1'];self.assertEqual(evaluate(m)['status'],'FAIL')
 def test_lighting_callback_never_runs(self):
  def forbidden(m):raise AssertionError('LIGHT_CHECK_EXECUTED')
  r=evaluate_rule_contract(self.m,trusted_evaluators={'window_opportunities':forbidden,'actual_opening_geometry':evaluate},context={'stage':'concept_internal','batch_models':[self.m]})
  row=next(x for x in r['requirements']if x['requirement_id']=='window_opportunities');self.assertEqual(row['status'],'EXCLUDED_BY_OWNER_SCOPE');self.assertNotIn('RULE_NOT_EVALUATED:window_opportunities',r['pending']);self.assertFalse(any(x.get('requirement_id')=='window_opportunities'for x in r['review_findings']))
 def test_no_lighting_remaining_unknowns(self):self.assertNotIn('SERVICE_VENTILATION_NOT_EVALUATED',EXCLUDED);self.assertNotIn('FIXTURE_HEIGHT_WINDOW_CLEARANCE_NOT_EVALUATED',EXCLUDED)
if __name__=='__main__':unittest.main()
