import json,copy,unittest
from pathlib import Path
from core_circulation_scope118 import grammar
from circulation_integrity119 import evaluate
from core_wall_audit118 import wall_network
class T(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.m=json.loads(Path('../planha_hybrid_independent/baseline119/random_4/response.json').read_text())['result']['internal_proposals'][1]['model']
 def test_actual_single_source_and_routes(self):
  self.assertEqual(grammar(self.m),[]);self.assertEqual(evaluate(self.m)['status'],'PASS_LIMITED')
 def test_single_does_not_waive_bad_network(self):self.assertEqual(wall_network(self.m)['status'],'FAIL')
 def test_missing_source(self):
  m=copy.deepcopy(self.m);m['module_placements']=[p for p in m['module_placements']if not p['module']['schema'].startswith('PRIVATE_')];self.assertTrue(grammar(m))
 def test_fake_rename(self):
  m=copy.deepcopy(self.m);u=m['units'][0];u['rooms']['private_hall']=u['rooms'].pop('entry_circulation');self.assertTrue(grammar(m))
 def test_private_pair_still_required_for_two(self):
  m=copy.deepcopy(self.m);m['units'][0]['rooms']['bed2']=m['units'][0]['rooms']['bed1'];self.assertTrue(grammar(m))
if __name__=='__main__':unittest.main()
