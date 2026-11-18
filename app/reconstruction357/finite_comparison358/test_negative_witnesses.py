import unittest,json
from pathlib import Path
from comparison_metrics import route_metrics
from fractions import Fraction as F
class ActualTests(unittest.TestCase):
 def test_all_six_exact_negative_witnesses(self):
  x=json.loads(Path(__file__).with_name('negative_dominance_actual358.json').read_text());self.assertEqual(len(x['pairs']),6)
  for p in x['pairs']:
   w=p['witness'];key='length'if w['metric']=='path_length_m'else'direction_changes'
   self.assertEqual(route_metrics(w['baseline_path'])[key],w['baseline_value']);self.assertEqual(route_metrics(w['alternative_path'])[key],w['alternative_value']);self.assertGreater(F(w['alternative_value']),F(w['baseline_value']));self.assertEqual(w['logic']['dominance'],'FALSE');self.assertTrue(w['logic']['unknown_dimensions']);self.assertFalse(w['logic']['rule_acceptance'])
 def test_not_parent_acceptance(self):
  x=json.loads(Path(__file__).with_name('negative_dominance_actual358.json').read_text());self.assertFalse(x['whole_Q04_acceptance']);self.assertFalse(x['finite_branch_coverage_proven']);self.assertFalse(x['component_purpose_proven'])
