"""Pure lexical portability checks; no model or semantic evaluation."""
import unittest,json,os,hashlib,ast
from pathlib import Path
W=Path(__file__).resolve().parent.parent
class Portable(unittest.TestCase):
 def test_old_freeze_unchanged(self):
  p=W/'review385_preaudit/source_freeze.json';self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),'7fe5d83472a806ca9f8811fe267158a77c04ba674e188fa8b0dcd5ed64a650c0')
  for n,h in json.loads(p.read_text())['files'].items():self.assertEqual(hashlib.sha256((W/n).read_bytes()).hexdigest(),h,n)
 def test_actual_historical_lexical_readset(self):
  rows=json.loads((W/'review387_preaudit/lexical_reads.json').read_text());f=json.loads((W/'review387_preaudit/source_freeze.json').read_text())['files'];self.assertEqual(len(rows),22)
  for r in rows:self.assertIn(r['path'],f);self.assertEqual(f[r['path']],r['sha256']);self.assertEqual(hashlib.sha256((W/r['path']).read_bytes()).hexdigest(),r['sha256'])
 def test_missing_file_is_bound_to_prior_intrinsic(self):
  d=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
  r=json.loads((W/'reconstruction357/review357_source_identity/result.json').read_text());e=json.loads((W/'reconstruction357/semantic_rules357/eligibility_intrinsic_actual357_finalpin.json').read_text());self.assertEqual(d(r),e['evidence']['new_result_digest'])
 def test_new_kernel_pin_matches_unchanged_original(self):
  p=W/'reconstruction357/staging387_current_semantics/balanced_access387.py';t=ast.parse(p.read_text());pins=ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='PINS'for x in n.targets)))
  for n,h in pins.items():self.assertEqual(hashlib.sha256((W/'reconstruction357'/n).read_bytes()).hexdigest(),h)
if __name__=='__main__':unittest.main()
