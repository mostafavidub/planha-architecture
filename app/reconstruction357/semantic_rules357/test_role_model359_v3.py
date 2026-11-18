import unittest,json,copy
from pathlib import Path
from role_registry_model359_v3 import evaluate,ROOT
from wall_origin359 import hall
from common import digest
class Actual359(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text());cls.v=json.loads((ROOT/'review359_source_validation/result.json').read_text());cls.o=evaluate(cls.r,cls.v);Path(__file__).with_name('role_registry_on359_v3.json').write_text(json.dumps(cls.o,indent=2))
 def test_exact359(self):self.assertEqual(self.o['model_hash'],digest(self.r['candidate']['model']));self.assertEqual(self.o['source_profile'],'SOURCE359')
 def test_new_source_hall_recomputed(self):self.assertEqual(len(hall(self.r)[0]['walls']),8)
 def test_old_review_rejected(self):
  old=json.loads((ROOT/'review358_source_validation/result.json').read_text())
  with self.assertRaises(ValueError):evaluate(self.r,old)
 def test_clamp_tamper_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['source_hall_clamp359'][0]['proof']['hall'][0]='0'
  with self.assertRaises(ValueError):evaluate(r,self.v)
 def test_release_not_automatic_parentpass(self):
  self.assertFalse(self.o['whole_parent_complete']);self.assertFalse(self.o['admission_allowed']);n=self.o['nodes'];self.assertTrue(n['Q11_WHOLE_ROLE']['status'].startswith('UNKNOWN'));self.assertTrue(all(not r['untargeted_terminal_extensions']for r in n['PRIVATE_CIRCULATION']['evidence'].values()))
 def test_whole_room_roles_zero_public_gap(self):
  n=self.o['nodes'];self.assertEqual(len(n['SOURCE_ROOM_USE']['evidence']),12);self.assertTrue(all(r['unresolved_area_m2']=='0'for r in n['PUBLIC_SUPPORT']['evidence']['rows']))
 def test_service_source_bound(self):
  n=self.o['nodes']['SERVICE_CIRCULATION'];self.assertTrue(n['status'].startswith('PASS_SCOPED_SOURCE117'));self.assertEqual(n['evidence']['current_record_digest'],digest(self.r));self.assertEqual(n['evidence']['current_fresh_result_digest'],digest(self.v));self.assertEqual(n['evidence']['evidence'][1]['model_digest'],self.o['model_hash'])
 def test_pending_exact_no_service(self):
  for r in self.o['nodes']['Q12_PER_UNIT']['evidence']:
   self.assertEqual(set(r['exact_pending']),{'Q04_CLOSED_FINITE_ELIGIBLE_COMPARISON','WHOLE_COMMON_LOBBY_ROLE','HALL_WALL_PURPOSE_Q04_DEPENDENCY'})
 def test_no_q11_parent_promotion(self):
  self.assertEqual(set(self.o['nodes']['Q11_WHOLE_ROLE']['blocking_dependencies']),{'COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON'})
 def test_transitive_service_manifest(self):
  import hashlib
  from service_runner359_v2 import MANIFEST_SHA
  p=ROOT/'finite_comparison358/service_closure359_manifest_v2.json'
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),MANIFEST_SHA)
  files=json.loads(p.read_text())['files']
  for name in ('wall_purpose.py','unsupported_extent_causes357.py','living_closure.py'):
   key='semantic_rules357/'+name
   self.assertEqual(files[key],hashlib.sha256((ROOT/key).read_bytes()).hexdigest())
  self.assertEqual(self.o['nodes']['SERVICE_CIRCULATION']['evidence']['invocation_source_manifest_sha256'],MANIFEST_SHA)
if __name__=='__main__':unittest.main()
