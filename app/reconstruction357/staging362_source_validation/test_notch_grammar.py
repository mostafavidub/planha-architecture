import sys,json,copy,time,unittest
from pathlib import Path
P=Path(__file__).resolve().parent;B=P.parent;sys.path.insert(0,str(P/'runtime'))
from notch_grammar362 import allowed_walls,checked_integrity
from source_registry362 import CurrentContext,_TOKEN
from contract114 import digest
class Tests(unittest.TestCase):
 def setUp(self):
  c=json.loads((B/'staging362_core_notch/actual362.json').read_text())['candidate'];self.m=c['model'];self.core=c['packet']['core']
 def test_actual_geometry(self):self.assertEqual(allowed_walls(self.m,self.core),{'core.notch362.A_separator'})
 def test_wrong_host(self):
  self.m['wall_hosts']['core.notch362.A_separator'][0]='0';self.assertRaises(ValueError,allowed_walls,self.m,self.core)
 def test_wrong_junction(self):
  self.m['walls']['core.lobby.outer_right'][1]='12.625';self.assertRaises(ValueError,allowed_walls,self.m,self.core)
 def test_core_tamper(self):
  self.core['lift'][0]='0';self.assertRaises(ValueError,allowed_walls,self.m,self.core)
 def test_fake_context(self):self.assertRaises(ValueError,checked_integrity,self.m,{'verified':True},lambda *a,**k:None)
 def test_stale_context(self):
  c=CurrentContext(_TOKEN,{}, {'model_hash':digest(self.m)},0);self.assertRaises(ValueError,checked_integrity,self.m,c,lambda *a,**k:None)
if __name__=='__main__':unittest.main()
