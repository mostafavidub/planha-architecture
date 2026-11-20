import sys,unittest
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'studies'))
import p08_presolve_11x19 as p
class P08PreSolve(unittest.TestCase):
 def test_exact_bed_threshold_both_axes_and_contact(self):
  a,b=Q('11.05'),Q('8.25')
  self.assertTrue(p.prove_bed_pair(Q('10.5'),Q('7.725'),a,b)['contradiction'])
  self.assertFalse(p.prove_bed_pair(a,Q('7.725'),a,b)['contradiction'])
  self.assertFalse(p.prove_bed_pair(Q('10.5'),b,a,b)['contradiction'])
 def test_exact_shared_threshold_both_branches_and_contact(self):
  pair,bath=Q('5.65'),Q('3.15')
  self.assertTrue(p.prove_shared_apron(Q('5.225'),Q('2.325'),pair,bath)['contradiction'])
  self.assertFalse(p.prove_shared_apron(pair,Q('2.325'),pair,bath)['contradiction'])
  self.assertFalse(p.prove_shared_apron(Q('5.225'),bath,pair,bath)['contradiction'])
 def test_no_solver_pinned_actual_constraints_each_historical_branch(self):
  d=p.execute()
  self.assertEqual(d['reconstructed_attempt_rows'],12);self.assertEqual(d['proof_rows'],9);self.assertEqual(d['unresolved_rows'],3)
  self.assertEqual(d['current_solver_calls'],0);self.assertIs(d['global_infeasibility_proven'],False);self.assertIs(d['iis_extracted'],False)
  for i,r in enumerate(d['rows']):
   top,variant=p.ORDER[i//2];self.assertEqual(r['topology'],top);self.assertEqual(r['variant'],variant)
   self.assertEqual(Q(r['box_width_m']),Q('10.5'));self.assertEqual(Q(r['box_depth_m']),Q('7.725'))
   if i%2==0:
    self.assertEqual(r['named_violation'],'BED_PAIR_RECTANGULAR_SEPARATION_IMPOSSIBLE_IN_SOURCE_BOX')
    self.assertEqual((Q(r['x_deficit_m']),Q(r['y_deficit_m'])),(Q('.55'),Q('.525')))
   elif top=='KITCHEN_BATH_SHARED_SIDE':
    self.assertEqual(r['named_violation'],'SHARED_SERVICE_PAIR_CANNOT_CLEAR_FIXED_ENTRY_APRON')
    self.assertEqual((Q(r['left_deficit_m']),Q(r['right_deficit_m'])),(Q('.425'),Q('.825')))
   else:self.assertEqual(r['named_violation'],'UNKNOWN')
if __name__=='__main__':unittest.main()
