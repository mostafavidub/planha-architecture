import unittest,json,copy
from pathlib import Path
from constructor126 import context
from construction_replay126 import verify,digest
ROOT=Path(__file__).parent
class Tests(unittest.TestCase):
 def setUp(self):
  self.p=json.loads((ROOT/'evidence126/ab_actual_smoke.json').read_text());a=json.loads((ROOT/'evidence125/fresh_world125_composed_gate.json').read_text())['context']['construction_trace'];b=json.loads((ROOT/'evidence126/alternate_smoke.json').read_text())['proposal'];self.c=context(a['raw'],self.p,{'A':a['proposal'],'B':b});self.m=self.p['world_model']
 def test_actual_ab(self):self.assertTrue(verify(self.m,self.c)['verified'])
 def test_source(self):self.c['source_files']['assemble114.py']='fake';self.assertFalse(verify(self.m,self.c)['verified'])
 def test_program(self):self.c['construction_trace']['proposals']['B']['sleep_roles']=['twin'];self.assertFalse(verify(self.m,self.c)['verified'])
 def test_B_replaced_and_rehashed(self):
  t=self.c['construction_trace'];t['proposals']['B']=copy.deepcopy(t['proposals']['A']);t['unit_proposal_hashes']['B']=digest(t['proposals']['B']);self.assertFalse(verify(self.m,self.c)['verified'])
 def test_false_receipt_rehashed(self):
  self.m['accepted']=True;self.c['construction_trace']['model_hash']=digest(self.m);self.assertFalse(verify(self.m,self.c)['verified'])
 def test_revision_as_new(self):self.c['existing_plan_id']='previous';self.assertFalse(verify(self.m,self.c)['verified'])
 def test_input(self):self.c['construction_trace']['raw']['W']='38';self.assertFalse(verify(self.m,self.c)['verified'])
if __name__=='__main__':unittest.main()
