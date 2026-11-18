import unittest,json,copy
from pathlib import Path
from circulation_integrity119 import evaluate
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.m=json.loads(Path('evidence/alternative119/case5_diningports_variant2_whole.json').read_text())['model']
 def test_actual(self):
  r=evaluate(self.m);self.assertEqual(r['status'],'PASS_LIMITED');self.assertTrue(r['witness']['common_unprogrammed_components'])
 def test_missing_target(self):
  m=copy.deepcopy(self.m);del m['units'][0]['routes']['dining_east'];self.assertNotEqual(evaluate(m)['status'],'PASS_LIMITED')
 def test_fake_dead_corridor(self):
  m=copy.deepcopy(self.m);m['units'][0]['rooms']['entry_circulation'].append(['.3','.3','.4','.4']);self.assertEqual(evaluate(m)['status'],'FAIL')
 def test_rename(self):
  m=copy.deepcopy(self.m);u=m['units'][0];u['rooms']['hidden_corridor']=u['rooms'].pop('entry_circulation');self.assertNotEqual(evaluate(m)['status'],'PASS_LIMITED')
 def test_route_collision(self):
  m=copy.deepcopy(self.m);m['units'][0]['routes']['dining_east']=[['0','0'],['1','0']];self.assertEqual(evaluate(m)['status'],'FAIL')
if __name__=='__main__':unittest.main()
