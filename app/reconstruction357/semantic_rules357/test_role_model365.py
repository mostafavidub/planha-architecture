import unittest,json,copy
from pathlib import Path
from role_registry_model365 import evaluate,ROOT
from wall_origin365 import hall
from common import digest
class Actual359(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());cls.v=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());cls.o=evaluate(cls.r,cls.v)
 def test_exact359(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(self.o['source_profile'],'SOURCE_BALANCED365')
 def test_new_source_hall_recomputed(self):self.assertEqual(len(hall(self.r)[0]['walls']),8)
 def test_old_review_rejected(self):
  old=json.loads((ROOT/'review359_source_validation/result.json').read_text())
  with self.assertRaises(ValueError):evaluate(self.r,old)
 def test_clamp_tamper_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['source_hall_clamp359'][0]['proof']['hall'][0]='0'
  with self.assertRaises(ValueError):evaluate(r,self.v)
 def test_release_not_automatic_parentpass(self):
  self.assertFalse(self.o['whole_parent_complete']);self.assertFalse(self.o['admission_allowed']);n=self.o['nodes'];self.assertTrue(n['Q11_WHOLE_ROLE']['status'].startswith('UNKNOWN'));self.assertTrue(all(not r['untargeted_terminal_extensions']for r in n['PRIVATE_CIRCULATION']['evidence'].values()))
 def test_whole_room_roles_zero_public_gap(self):
  n=self.o['nodes'];self.assertEqual(len(n['SOURCE_ROOM_USE']['evidence']),12);self.assertEqual({r['unit']:r['unresolved_area_m2']for r in n['PUBLIC_SUPPORT']['evidence']['rows']},{'A':'3/1000','B':'0'})
 def test_notch_source_predicate(self):
  from wall_origin365 import base
  b,e=base(self.r);self.assertIn('notch_frame_source_sha256',e)
  self.assertEqual(b['wall_hosts']['core.lobby.outer_right'],self.r['candidate']['model']['wall_hosts']['core.lobby.outer_right'])
 def test_notch_host_tamper(self):
  from wall_origin365 import base
  r=copy.deepcopy(self.r);r['candidate']['model']['wall_hosts']['core.lobby.outer_right'][1]='12.625';r['candidate']['model_digest']=digest(r['candidate']['model']);r['trace']['model_digest']=r['candidate']['model_digest'];r['trace']['candidate_digest']=digest(r['candidate'])
  with self.assertRaisesRegex(ValueError,'NOTCH_FRAME_EXACT'):base(r)
 def test_all_wall_origins_joined(self):
  w=self.o['nodes']['WALL_PURPOSE']['evidence'];self.assertEqual(w['status'],'MEASURED_CONSTRUCTIVE_SUBCLAIMS_NOT_FULL_Q11_OR_Q05');self.assertEqual(w['unjoined_host_ids'],[]);self.assertEqual(w['counts'].get('UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY'),8)
 def test_common_helper_not_invoked_or_closed(self):
  self.assertEqual(self.o['nodes']['COMMON_ROLE']['status'],'PASS_SCOPED_CONCEPTUAL_COMMON_TRANSFER_JUNCTION_ROLE');self.assertEqual(self.o['nodes']['COMMON_ROLE']['evidence']['model_hash'],digest(self.r['candidate']['model']))
 def test_service359_not_transferred(self):
  self.assertEqual(self.o['nodes']['SERVICE_CIRCULATION']['status'],'UNKNOWN_EXCLUSIVE_SERVICE_ROLE_ACCOUNTING')
 def test_new_public_gap_not_hidden(self):
  n=self.o['nodes'];self.assertEqual(n['PUBLIC_SUPPORT']['status'],'UNKNOWN');a=next(u for u in n['Q12_PER_UNIT']['evidence']if u['unit']=='A');self.assertIn('PUBLIC_FUNCTIONAL_EXTENT_GAP',a['exact_pending'])
 def test_own_entry_operations_rebound(self):
  e=self.o['nodes']['COMMON_ROLE']['evidence'];self.assertEqual(e['record_digest'],digest(self.r));self.assertEqual(e['raw_review_digest'],digest(self.v));self.assertEqual(len(e['actual_entry_operation_use']),2)
if __name__=='__main__':unittest.main()
