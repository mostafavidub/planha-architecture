import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
import closure_openings as c
class Closure(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  x=json.loads((Path(__file__).resolve().parents[1]/'actual_run/actual_response.json').read_text());cls.m=x['selected'][0]['model'];cls.r=x['central_fresh_reviews'][0]['central_fresh_review']['raw_fresh_report']
 def test_bound_artifact_not_live_or_parent(self):
  x=c.evaluate(self.m,self.r);self.assertEqual(x['verdict'],'UNKNOWN');self.assertEqual(x['evidence']['inventory_join'],'BOUND_SCOPED');self.assertFalse(x['parent_initial']);self.assertFalse(x['fresh_execution_attested'])
 def test_stale_model(self):
  m=copy.deepcopy(self.m);m['openings'][0]['host_wall_id']='fake';self.assertEqual(c.evaluate(m,self.r)['codes'][0],'BINDING_OR_DATA_UNAVAILABLE')
 def test_inventory_omission(self):
  r=copy.deepcopy(self.r)
  row=next(x for x in r['rule_contract_evidence']['requirements'] if x['requirement_id']=='opening_hosts');row['evidence']['witness']['openings'].pop()
  self.assertIn('HOST_WITNESS_INVENTORY',c.evaluate(self.m,r)['codes'])
 def test_operation_omission(self):
  r=copy.deepcopy(self.r);row=next(x for x in r['rule_contract_evidence']['requirements'] if x['requirement_id']=='door_operation');row['evidence']['witness']['actual_operation_ids'].pop()
  self.assertIn('OPERATION_WITNESS_INVENTORY:doors',c.evaluate(self.m,r)['codes'])
 def test_bound_failure_preserved_not_ignored(self):
  r=copy.deepcopy(self.r);row=next(x for x in r['rule_contract_evidence']['requirements'] if x['requirement_id']=='door_operation');row['status']='FAIL';row['evidence']['witness']['errors']=['TEST_ONLY_COLLISION']
  # Synthetic consumer branch, NOT a real checker failure nor repair authority.
  x=c.evaluate(self.m,r);self.assertEqual(x['verdict'],'FAIL');self.assertFalse(x['delivery_allowed'])
 def test_pending_never_passes(self):
  r=copy.deepcopy(self.r);row=next(x for x in r['rule_contract_evidence']['requirements'] if x['requirement_id']=='door_operation');row['status']='NOT_EVALUATED';row['evidence']['witness']['pending']=['TEST_ONLY_MISSING_SCENARIO']
  self.assertEqual(c.evaluate(self.m,r)['verdict'],'UNKNOWN')
 def test_duplicate(self):
  r=copy.deepcopy(self.r);r['rule_contract_evidence']['requirements'].append(r['rule_contract_evidence']['requirements'][0]);self.assertEqual(c.evaluate(self.m,r)['verdict'],'UNKNOWN')
class ScenarioJoin(Closure):
 def test_full_source_profile_inventory(self):
  rs=c.rows(self.m,self.r);x=c._scenario_join(self.m,rs)
  self.assertEqual(x['missing'],[]);self.assertEqual(len(x['inventory']),len(self.m['openings']))
 def test_nonleaf_unsupported(self):
  m=copy.deepcopy(self.m);m['openings'][0]['kind']='unknown';m['operations']['doors']=[x for x in m['operations']['doors'] if x['opening_id']!=m['openings'][0]['id']]
  x=c._scenario_join(m,c.rows(self.m,self.r));self.assertTrue(any('NONLEAF_SOURCE_PROFILE_UNSUPPORTED' in y for y in x['missing']))
 def test_missing_operation(self):
  m=copy.deepcopy(self.m);m['operations']['doors'].pop()
  self.assertTrue(c._scenario_join(m,c.rows(self.m,self.r))['missing'])
 def test_duplicate_trajectory(self):
  m=copy.deepcopy(self.m);a=m['operations']['doors'][0]['continuous_actor_segments'];a.append(copy.deepcopy(a[0]))
  self.assertTrue(any('DUPLICATE_TRAJECTORY_RECORD' in y for y in c._scenario_join(m,c.rows(self.m,self.r))['missing']))
 def test_missing_both_side(self):
  m=copy.deepcopy(self.m);m['operations']['doors'][0]['continuous_actor_segments']=[]
  self.assertTrue(c._scenario_join(m,c.rows(self.m,self.r))['missing'])
if __name__=='__main__':unittest.main()
