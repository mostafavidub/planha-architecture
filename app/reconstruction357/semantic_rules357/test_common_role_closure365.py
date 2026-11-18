import unittest,json,copy
from common_role_closure365 import evaluate,intrinsic,ROOT
from common import digest
class CommonRole362(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());cls.v=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());cls.req={x['requirement_id']:x for x in cls.v['raw_report']['rule_contract_evidence']['requirements']};cls.o=evaluate(cls.r,cls.v)
 def test_actual_use_not_minrect_only(self):
  self.assertEqual(len(self.o['actual_required_transfers']),4);self.assertEqual(len(self.o['actual_entry_operation_use']),2);self.assertEqual(self.o['whole_junction_area_m2'],'583/80');self.assertFalse(self.o['admission_allowed'])
 def test_missing_fresh_operation(self):
  q=copy.deepcopy(self.req);q['door_operation']['status']='UNKNOWN'
  with self.assertRaisesRegex(ValueError,'CURRENT_FRESH'):intrinsic(self.r,q)
 def test_missing_actual_continuous_actor(self):
  r=copy.deepcopy(self.r)
  for op in r['candidate']['model']['operations']['doors']:
   if op['opening_id']=='A.entry':op['continuous_actor_segments']=[]
  m=r['candidate']['model'];r['candidate']['model_digest']=digest(m);q=copy.deepcopy(self.req)
  for x in q.values():
   if 'model_hash'in x:x['model_hash']=digest(m)
  with self.assertRaisesRegex(ValueError,'CONTINUOUS_USE_MISSING'):intrinsic(r,q)
 def test_missing_actual_required_route(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['common_routes'].pop('lift_B');m=r['candidate']['model'];r['candidate']['model_digest']=digest(m);q=copy.deepcopy(self.req)
  for x in q.values():
   if 'model_hash'in x:x['model_hash']=digest(m)
  with self.assertRaisesRegex(ValueError,'REQUIRED_TRANSFER_INVENTORY'):intrinsic(r,q)
 def test_stale_review(self):
  v=json.loads((ROOT/'review359_source_validation/result.json').read_text())
  with self.assertRaises(ValueError):evaluate(self.r,v)
 def test_bound_alone_no_wholeclaim(self):
  self.assertEqual(self.o['fixed_portal_family_bound']['parent_complete'],False);self.assertIn('WHOLE_JUNCTION_ROLE_SCOPE_REVIEW',self.o['fixed_portal_family_bound']['missing']);self.assertIn('Q04_COMPARATIVE_NECESSITY',self.o['not_claimed'])
 def test_extra_lobby_extent_unsupported(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['common_spaces']['lobby'].append(['15.775','12.625','17.575','13.425']);r['candidate']['model_digest']=digest(r['candidate']['model'])
  with self.assertRaisesRegex(ValueError,'SOURCE_FIXED_PORTAL'):intrinsic(r,self.req)
 def test_obstacle_island_rejected(self):
  from common_role_closure365 import interior_clearance
  from modules_spatial import rect
  m=copy.deepcopy(self.r['candidate']['model']);m['walls']['island']=['14.8','13.6','15','13.8']
  with self.assertRaisesRegex(ValueError,'INTERIOR_OBSTACLE'):interior_clearance(m,rect(self.o['whole_junction_region']))
 def test_open_panel_intrusion_rejected(self):
  from common_role_closure365 import interior_clearance
  from modules_spatial import rect
  m=copy.deepcopy(self.r['candidate']['model']);m['operations']['doors'][0]['open_panel']=['14.8','13.6','15','13.8']
  with self.assertRaisesRegex(ValueError,'INTERIOR_OBSTACLE'):interior_clearance(m,rect(self.o['whole_junction_region']))
 def test_unknown_blocked_inventory_rejected(self):
  from common_role_closure365 import interior_clearance
  from modules_spatial import rect
  m=copy.deepcopy(self.r['candidate']['model']);m['operations']['new_kind']=[]
  with self.assertRaisesRegex(ValueError,'UNSUPPORTED_OPERATION'):interior_clearance(m,rect(self.o['whole_junction_region']))
 def test_actual_clear_interior_witness(self):
  w=self.o['connected_source_domain_witness'];self.assertEqual(w['positive_interior_intersections'],[]);self.assertGreater(w['blocked_inventory_count'],100)
 def test_closet_endpoints_outside_middle_crosses(self):
  from common_role_closure365 import interior_clearance
  from modules_spatial import rect,intersection
  m=copy.deepcopy(self.r['candidate']['model']);q=rect(self.o['whole_junction_region']);panel=m['operations']['closets'][0]['panels'][0];panel['closed_panel']=['12','13.6','12.1','13.8'];panel['open_panel']=['16','13.6','16.1','13.8'];panel['rail_envelope']=panel['closed_panel']
  self.assertIsNone(intersection(rect(panel['closed_panel']),q));self.assertIsNone(intersection(rect(panel['open_panel']),q))
  with self.assertRaisesRegex(ValueError,'INTERIOR_OBSTACLE.*linear_motion'):interior_clearance(m,q)
if __name__=='__main__':unittest.main()
