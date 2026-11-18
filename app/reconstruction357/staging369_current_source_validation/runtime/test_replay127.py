import unittest,json,copy
from pathlib import Path
from constructor127 import context
from construction_replay127 import verify,digest
P=Path(__file__).parent/'evidence127'
class T(unittest.TestCase):
 def setUp(self):
  self.p=json.loads((P/'compact_packet.json').read_text());s=json.loads((P/'compact_smoke.json').read_text());self.c=context(s['raw'],self.p,{'A':s['proposal'],'B':copy.deepcopy(s['proposal'])});self.m=self.p['world_model']
 def test_actual(self):self.assertTrue(verify(self.m,self.c)['verified'])
 def test_B_geometry_rehash(self):
  t=self.c['construction_trace'];b=t['proposals']['B'];b['rectangles']['bed1'][0]=str(float(b['rectangles']['bed1'][0])+.1);t['unit_proposal_hashes']['B']=digest(b);self.assertFalse(verify(self.m,self.c)['verified'])
 def test_false_claim_rehash(self):
  self.m['accepted']=True;self.c['construction_trace']['model_hash']=digest(self.m);self.assertFalse(verify(self.m,self.c)['verified'])
 def test_program(self):self.c['construction_trace']['proposals']['B']['sleep_roles']=['double'];self.assertFalse(verify(self.m,self.c)['verified'])
 def test_source(self):self.c['source_files']['constructor127.py']='bad';self.assertFalse(verify(self.m,self.c)['verified'])
if __name__=='__main__':unittest.main()
