import unittest,json,copy
from pathlib import Path
from constructor125 import context
from construction_replay125 import verify
class T(unittest.TestCase):
 def setUp(self):
  p=Path(__file__).parent/'evidence125';self.x=json.loads((p/'fresh_world125_composed_gate.json').read_text());self.p=self.x['packet'];t=self.x['context']['construction_trace'];self.c=context(t['raw'],t['proposal'],self.p)
 def check(self):self.assertFalse(verify(self.p['world_model'],self.c)['verified'])
 def test_false_new(self):self.c['existing_plan_id']='old';self.check()
 def test_source(self):self.c['source_files']['world_transform125.py']='fake';self.check()
 def test_worldhash(self):self.c['construction_trace']['model_hash']='fake';self.check()
 def test_old_revision(self):self.c['construction_trace']['source_revision']='fake';self.check()
 def test_old_model_input(self):self.c['construction_trace']['raw']['model']={};self.check()
if __name__=='__main__':unittest.main()
