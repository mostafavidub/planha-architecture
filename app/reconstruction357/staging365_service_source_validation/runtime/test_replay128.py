import unittest,json,copy
from pathlib import Path
from constructor128 import context
from construction_replay128 import verify,digest
class T(unittest.TestCase):
 def setUp(self):
  j=json.loads((Path(__file__).parent/'evidence128/coarse_wallbound_whole.json').read_text());self.m=j['model'];self.p={'model':self.m,'core':j['core'],'admission_claim':False};self.c=context(j['raw'],j['proposal'],self.p)
 def test_actual(self):self.assertTrue(verify(self.m,self.c)['verified'])
 def test_source(self):self.c['source_files']['constructor128.py']='bad';self.assertFalse(verify(self.m,self.c)['verified'])
 def test_program(self):self.c['construction_trace']['proposal']['sleep_roles']=['double','twin'];self.assertFalse(verify(self.m,self.c)['verified'])
 def test_model_rehash(self):self.m['accepted']=True;self.c['construction_trace']['model_hash']=digest(self.m);self.assertFalse(verify(self.m,self.c)['verified'])
 def test_revision_as_new(self):self.c['baseline_model_hash']='old';self.assertFalse(verify(self.m,self.c)['verified'])
 def test_proposal_geometry(self):self.c['construction_trace']['proposal']['rectangles']['bed1'][0]='1.234';self.assertFalse(verify(self.m,self.c)['verified'])
if __name__=='__main__':unittest.main()
