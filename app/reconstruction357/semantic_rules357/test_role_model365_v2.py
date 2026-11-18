import unittest,json,copy
from role_registry_model365_v2 import evaluate,ROOT
from common import digest
class Role365V2(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());cls.v=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());cls.o=evaluate(cls.r,cls.v)
 def test_current_model_binding(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']))
 def test_nonusable_margin_not_capacity(self):
  us=self.o['nodes']['Q12_PER_UNIT']['evidence'];a=next(u for u in us if u['unit']=='A');self.assertEqual(a['nonusable_operational_reservation_m2'],'3/1000');self.assertEqual(a['usable_capacity_increment_from_reservation'],0);self.assertEqual(a['current_source_public_extent_unresolved_m2'],'0')
 def test_balance_current_not_old_gap(self):
  b=self.o['nodes']['Q12_PER_UNIT']['balanced_common_access'];self.assertEqual(b['verdict'],'PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS');self.assertEqual(b['model_hash'],self.o['model_hash'])
 def test_dependencies_remain(self):
  n=self.o['nodes'];self.assertTrue(n['Q11_WHOLE_ROLE']['status'].startswith('UNKNOWN'));self.assertEqual(set(n['Q11_WHOLE_ROLE']['blocking_dependencies']),{'SERVICE_CIRCULATION','WALL_PURPOSE','Q04_COMPARISON'})
 def test_selected_set_not_singleton(self):
  q=self.o['nodes']['Q14_SELECTION_SET'];self.assertTrue(q['status'].startswith('UNKNOWN'));self.assertEqual(q['evidence']['internal_pair_test']['status'],'NOT_APPLICABLE_INTERNAL_SINGLETON_REVIEW');self.assertEqual(q['evidence']['selected_output_set_fulfillment'],'NOT_PROVEN')
 def test_stale_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review362_source_validation/result.json').read_text()))
 def test_changed_reserved_slack_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['packet']['core']['balanced_portals365']['selected_interval']=['15','16']
  with self.assertRaises(ValueError):evaluate(r,self.v)
 def test_no_delivery(self):self.assertFalse(self.o['admission_allowed']);self.assertFalse(self.o['whole_parent_complete'])
if __name__=='__main__':unittest.main()
