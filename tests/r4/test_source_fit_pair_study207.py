"""Synthetic source-module and added-constraint tests; not a whole-plan witness."""
import copy,sys,unittest
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/local_integration/candidate'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import source_fit_profile207 as fit
import source_fit_candidate207 as candidate
from contract114 import core_first,digest
class FitTests(unittest.TestCase):
 def test_source_pins_and_actual_pieces(self):
  p=fit.profiles();self.assertGreater(len(p['bath_apron']),0);self.assertEqual(len(p['kitchen_motions']),6)
  import bathroom_module117
  for w,h in [('3.15','2.25'),('3.575','2.675'),('4.3','3.1')]:
   m=bathroom_module117.build(w,h);self.assertEqual(digest(m['unit']['rooms']['public_access']),digest(p['bath_apron']))
 def test_previous_motion_helper_exact_reuse(self):
  from four_seat_group_candidate import source_kitchen_motion
  import kitchen_module117
  for w,h in [('2.35','3.05'),('3.175','3.625'),('3.6','4.2')]:
   prior,_=source_kitchen_motion(w,h)
   self.assertEqual([[str(F(v))for v in r]for r in fit.motion_rectangles(kitchen_module117.build(w,h))],[[str(v)for v in r]for r in prior])
 def fixture(self):
  paths={n:[['1','1'],['2','1'],['2','2'],['3','2'],['3','3']]for n in ('sofa1_use','dining_east')}
  return [tuple(map(F,['4','4','5','5']))],tuple(map(F,['6','6','7','7'])),[tuple(map(F,['8','8','9','9']))],paths,[tuple(map(F,['0','0','10','10']))]
 def test_clear_synthetic_reservations(self):
  self.assertEqual(fit.reservation_errors(*self.fixture()),([],[]))
 def test_dining_intrudes_actual_apron(self):
  a,d,m,p,o=self.fixture();n,c=fit.reservation_errors(a,a[0],m,p,o);self.assertIn('BATH_APRON_IN_DINING_EXCLUDED_PUBLIC_ROLE',n)
 def test_apron_outside_owner(self):
  a,d,m,p,o=self.fixture();a=[tuple(map(F,['-1','4','1','5']))];n,c=fit.reservation_errors(a,d,m,p,o);self.assertIn('BATH_APRON_OUTSIDE_OWNERSHIP',n)
 def test_motion_intrudes_guest_band(self):
  a,d,m,p,o=self.fixture();m=[tuple(map(F,['1','1','2','2']))];n,c=fit.reservation_errors(a,d,m,p,o);self.assertIn('GUEST_BODY_SOURCE_MOTION_INTRUSION',c);self.assertEqual(n,[])
 def test_source_built_six_motion_route_predicate_without_solver(self):
  # Source-built obstacles and synthetic paths/domain, not a whole-plan scene.
  import inspect,kitchen_module117
  from source_guest_route_evaluator import route_check
  fit.source_check()
  self.assertEqual(Path(inspect.getsourcefile(route_check)).resolve(),ROOT/'app/local_integration/source_guest_route_evaluator.py')
  module=kitchen_module117.build('2.35','3.05');pin=digest(module)
  motions=fit.motion_rectangles(module);self.assertEqual(len(motions),6)
  body=F(module['operations']['kitchen'][0]['assumptions']['body_m'])
  self.assertEqual(body,F('.7'))
  rects=[tuple(map(F,r))for r in motions]
  xmin=min(r[0]for r in rects);ymin=min(r[1]for r in rects)
  xmax=max(r[2]for r in rects);ymax=max(r[3]for r in rects)
  domain=[[str(xmin-3),str(ymin-3),str(xmax+3),str(ymax+3)]]
  clear=[[str(xmin-1),str(ymin-1)],[str(xmax+1),str(ymin-1)]]
  self.assertGreater(route_check(clear,clear[0],clear[-1],body,domain,motions),0)
  for i,(x,y,xx,yy)in enumerate(rects):
   with self.subTest(motion_index=i):
    cy=(y+yy)/2
    path=[[str(x-1),str(cy)],[str(xx+1),str(cy)]]
    self.assertGreater(route_check(path,path[0],path[-1],body,domain,[]),0)
    self.assertTrue(any(fit.hit(b,rects[i])for b in fit.sweep(path,body)))
    # Isolate each source envelope so another obstacle cannot explain rejection.
    with self.assertRaisesRegex(ValueError,'^ROUTE_OBSTACLE_COLLISION$'):
     route_check(path,path[0],path[-1],body,domain,[motions[i]])
  self.assertEqual(digest(module),pin)
  fit.source_check()
 def test_wrong_actor_scope_rejected(self):
  a,d,m,p,o=self.fixture();p['kitchen']=p.pop('dining_east')
  with self.assertRaisesRegex(ValueError,'DECLARED_GUEST_TERMINALS'):fit.reservation_errors(a,d,m,p,o)
 def test_diagonal_rejected(self):
  a,d,m,p,o=self.fixture();p['dining_east'][1]=['2','2']
  with self.assertRaisesRegex(ValueError,'GUEST_PATH_ORTHOGONAL'):fit.reservation_errors(a,d,m,p,o)
 def test_wrong_human_profile_rejected(self):
  import kitchen_module117
  m=kitchen_module117.build('2.35','3.05');m['operations']['kitchen'][0]['assumptions']['body_m']='.6'
  with self.assertRaisesRegex(ValueError,'SOURCE_BODY'):fit.motion_rectangles(m)
 def test_master_source_constraints_present_without_solver(self):
  import search114
  core=core_first(F(20),F(18))
  def collect(p):
   return {r['group']for r in p['row_metadata']}
  old=search114.propose(core,2,sleep_roles=['double','twin'],diagnostic_capture=collect)
  new=candidate.propose(core,2,sleep_roles=['double','twin'],diagnostic_capture=collect)
  self.assertTrue(old<=new);self.assertIn('source_actual_bath_apron_dining_role',new)
 def test_actual_installers_subset_positive_and_detached_negatives(self):
  props={uid:{'rectangles':{'bath':['6','5','9.15','7.25'],'kitchen':['1','1','3.35','4.05']}}for uid in ('A','B')}
  expected=fit.installation_expectations(props,F(18));pin=digest(expected)
  self.assertEqual(fit.verify_installed_subset(expected,expected)['state'],'PASS_SOURCE_SUBSET_ONLY')
  result=fit.installation_negatives(expected,expected);self.assertTrue(result['all_detected']);self.assertEqual(len(result['rows']),4);self.assertEqual(digest(expected),pin)
 def test_missing_downstream_motion_enrichment_rejected(self):
  props={uid:{'rectangles':{'bath':['6','5','9.15','7.25'],'kitchen':['1','1','3.35','4.05']}}for uid in ('A','B')}
  expected=fit.installation_expectations(props,F(18));observed=copy.deepcopy(expected)
  del observed['operations']['kitchen'][0]['motion_envelopes']
  self.assertEqual(fit.verify_installed_subset(observed,expected)['state'],'FAIL_SOURCE_BINDING')
 def test_source_installed_wrong_door_side_direct_geometry(self):
  props={uid:{'rectangles':{'bath':['6','5','9.15','7.25'],'kitchen':['1','1','3.35','4.05']}}for uid in ('A','B')}
  shell=fit.installation_expectations(props,F(18))
  for u in shell['units']:u['ownership']=[['0','0','20','18']]
  result=fit.door_side_negative(shell)
  self.assertEqual([r['state']for r in result['rows']],['DETECTED_DIRECT_GEOMETRY']*2)
 def test_scope_no_one_bed_fallback(self):
  with self.assertRaisesRegex(ValueError,'SOURCE_FIT207_SCOPE'):candidate.propose(core_first(F(20),F(18)),1,sleep_roles=['double'])
 def test_profile_copy_isolation(self):
  p=fit.profiles();d=digest(p);p['bath_apron'].clear();self.assertEqual(digest(fit.profiles()),d)
if __name__=='__main__':unittest.main()
