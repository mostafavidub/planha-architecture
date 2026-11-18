import unittest,json,copy
from pathlib import Path
from primitive_review_service365 import evaluate
P=Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  v=json.loads((P/'group_readsets_service_actual365.json').read_text());c.m=v['envelope']['packet']['world_model'];c.r=v['result']['raw_fresh_report'];c.ctx={k:v[k]for k in ('envelope','result','groups')};c.ctx['seconds']=10
 def test_foreign_profile(self):
  with self.assertRaises(ValueError):evaluate(self.m,self.r,source_profile='SOURCE_BALANCED365',post_fresh=self.ctx)
 def test_raw_mutation(self):
  r=copy.deepcopy(self.r);r['model_hash']='fake'
  with self.assertRaises(ValueError):evaluate(self.m,r,source_profile='SOURCE_SERVICE365',post_fresh=self.ctx)
 def test_foreign_context(self):
  c=copy.deepcopy(self.ctx);c['result']['raw_fresh_report']['errors']=['fake']
  with self.assertRaises(ValueError):evaluate(self.m,self.r,source_profile='SOURCE_SERVICE365',post_fresh=c)
 def test_stored_actual_limits(self):
  a=json.loads((P/'primitive_review_service_actual365.json').read_text());self.assertFalse(a['parent_dispatch_executed']);self.assertFalse(a['fresh_executed']);self.assertFalse(a['delivery_allowed'])
  for v in a['source_closures'].values():self.assertTrue(v['verdict'].startswith('PASS_SCOPED'));self.assertTrue(v['missing'])
if __name__=='__main__':unittest.main()
