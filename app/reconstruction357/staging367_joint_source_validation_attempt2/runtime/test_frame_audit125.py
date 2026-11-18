import unittest,json,copy
from pathlib import Path
from frame_audit125 import evaluate_core
class Tests(unittest.TestCase):
 def setUp(self):self.c=json.loads((Path(__file__).parent/'evidence125/local_core39x7.07.json').read_text())
 def test_actual(self):
  r=evaluate_core(self.c);self.assertFalse(r['errors'],r);self.assertFalse(r['eligible_for_draft_export'])
 def test_nonrigid(self):
  self.c['world_from_local']['matrix'][0][1]=2;self.assertTrue(evaluate_core(self.c)['errors'])
 def test_port(self):
  self.c['entry_centers']['A'][0]='4.5';self.assertIn('ENTRY_PORT:A',evaluate_core(self.c)['errors'])
 def test_ownership(self):
  self.c['unit_ownership']['A']=self.c['unit_ownership']['B'];self.assertIn('OWNERSHIP:A',evaluate_core(self.c)['errors'])
 def test_core_resize(self):
  self.c['stair'][2]='3';self.assertIn('CORE_RECT:stair',evaluate_core(self.c)['errors'])
 def test_world_claim(self):
  self.c['accepted']=True;self.assertFalse(evaluate_core(self.c)['accepted'])
if __name__=='__main__':unittest.main()
