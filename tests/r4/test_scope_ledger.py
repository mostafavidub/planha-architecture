"""Structural checks only; does not evaluate architecture or establish complete PRD coverage."""
import hashlib,json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
class Scope(unittest.TestCase):
 def test_reference_and_scope(self):
  s=json.loads((ROOT/'specs/R4_SAMPLE_RULE_SCOPE_LEDGER_V1.json').read_text())
  self.assertEqual(s['status'],'PREPARED_DEPENDENCY_BLOCKED_NOT_EXECUTED')
  for r in s['source_files']:
   b=(ROOT/r['path']).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),r['blob'])
  self.assertEqual(len(s['registry_crosswalk']),89);self.assertEqual(len(s['named_requirements']),38)
  self.assertEqual(len({r['id'] for r in s['registry_crosswalk']}),89)
  self.assertEqual(len({r['id'] for r in s['named_requirements']}),38)
  self.assertEqual(len(s['current_criteria']),4)
  for c in s['current_criteria']:
   self.assertEqual(c['baseline_evidence_state'],'NOT_RUN_BASELINE_BINDING_PENDING')
   self.assertTrue(c['sources']);self.assertTrue(c['required_data'])
   if c['id']!='CURRENT_PROGRAM_SUITABILITY':self.assertEqual(c['missing_rule'],[])
  self.assertEqual(s['post_mvp']['state'],'NOT_EVALUATED_NOT_BLOCKING_MVP')
  self.assertEqual(s['post_mvp']['counterexamples'][0]['state'],'NECESSARY_MVP_EVIDENCE_REQUIRED')
  self.assertTrue(s['unmapped']['registry_without_named_subconditions'])
  self.assertIsNone(s['product_stage']['up_to_six']['minimum_required_count'])
  self.assertEqual(s['product_stage']['up_to_six']['max_qualified_count'],6)
  for key in ('accepted','qualified','display_allowed','delivery_allowed'):self.assertIs(s[key],False)
if __name__=='__main__':unittest.main()
