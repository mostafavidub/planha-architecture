import unittest,json,copy
from pathlib import Path
from role_registry_model359 import evaluate,ROOT
from wall_origin359 import hall
from common import digest
class Actual359(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text());cls.v=json.loads((ROOT/'review359_source_validation/result.json').read_text());cls.o=evaluate(cls.r,cls.v);Path(__file__).with_name('role_registry_on359.json').write_text(json.dumps(cls.o,indent=2))
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
if __name__=='__main__':unittest.main()
