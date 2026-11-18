import ast,unittest,json,sys,runpy
from pathlib import Path
H=Path(__file__).resolve().parent;W=H.parents[1]
class Tests(unittest.TestCase):
 def test_all_eight_pure_bindings(self):
  x=json.loads((W/'review382_preaudit/historical_bindings.json').read_text());self.assertTrue(x['all_pass']);self.assertEqual(len(x['rows']),8);self.assertFalse(x['comparison_executed'])
 def test_only_matching_old_receipt_selected(self):
  s=(H/'cohort382.py').read_text();self.assertIn("'review357_source_identity/result.json','eligibility_intrinsic_actual357_finalpin.json'",s);self.assertNotIn("'review357_source_validation/result.json','eligibility_intrinsic_actual357_finalpin.json'",s)
 def test_raw381_unchanged(self):
  import hashlib
  p=W/'review381_actual_v1/manifest.json';f=json.loads(p.read_text())['files']
  self.assertTrue(all(hashlib.sha256((W/n).read_bytes()).hexdigest()==h for n,h in f.items()))
 def test_comparison_kernels_identical(self):
  a=ast.parse((H.parent/'staging381_role_semantics/cohort381.py').read_text());b=ast.parse((H/'cohort382.py').read_text())
  for name in('read','kernels'):
   x=next(n for n in a.body if isinstance(n,ast.FunctionDef)and n.name==name);y=next(n for n in b.body if isinstance(n,ast.FunctionDef)and n.name==name);self.assertEqual(ast.dump(x),ast.dump(y))
 def test_unassessed_scope_not_waived(self):
  s=(H/'cohort382.py').read_text();self.assertIn('UNASSESSED_NO_MODEL_NO_FRESH_NO_DOMINANCE_PROOF',s);self.assertIn("'full_q04_closed':False",s);self.assertIn('NOT_RERUN382',s)
if __name__=='__main__':unittest.main()
