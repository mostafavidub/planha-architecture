import unittest,json,copy
from role_registry_service365 import evaluate,ROOT
from wall_origin_service365 import base,hall
from common import digest
class ServiceRoles365(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());cls.v=json.loads((ROOT/'review365_service_source_validation/result.json').read_text());cls.o=evaluate(cls.r,cls.v)
 def test_own_model_profile(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(self.o['source_profile'],'SOURCE_SERVICE365')
 def test_branch_hall_rebuilt_not_row(self):
  h,e=hall(self.r);self.assertEqual(len(h['walls']),8);self.assertTrue(all('private_branch146' in k for k in h['walls']))
 def test_all_wall_hosts_joined(self):
  w=self.o['nodes']['WALL_PURPOSE']['evidence'];self.assertEqual(w['unjoined_host_ids'],[]);self.assertEqual(len(w['rows']),109)
 def test_public_no_borrowed_margin(self):
  s=self.o['nodes']['PUBLIC_SUPPORT']['evidence'];self.assertEqual({u['unit']:u['unresolved_area_m2']for u in s['rows']},{'A':'0','B':'0'});self.assertNotIn('source_operational_reservation',s)
 def test_common_tail_not_singleton_pass(self):
  c=self.o['nodes']['COMMON_ROLE'];self.assertTrue(c['status'].startswith('UNKNOWN'));self.assertEqual(len(c['evidence']['regions']),2)
 def test_actual_balance_gap_retained(self):
  b=self.o['nodes']['Q12_PER_UNIT']['balanced_common_access'];self.assertEqual(b['verdict'],'UNKNOWN_BALANCE_NOT_ESTABLISHED');lift=next(c for c in b['comparisons']if c['origin']=='lift');self.assertEqual(lift['length_A_m'],'193/40');self.assertEqual(lift['length_B_m'],'161/40')
 def test_old_balanced_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text()))
 def test_changed_branch_origin_rejected(self):
  r=copy.deepcopy(self.r);r['trace']['proposal']['ordered_macro']['origin']=['0','0']
  with self.assertRaises(ValueError):evaluate(r,self.v)
 def test_not_second_qualified_option(self):self.assertFalse(self.o['admission_allowed']);self.assertTrue(self.o['nodes']['Q12_PER_UNIT']['status'].startswith('UNKNOWN'))
if __name__=='__main__':unittest.main()
