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
class P10BathAlignmentTests(unittest.TestCase):
 """Actual module builder+installer, detached synthetic room scene; no whole model or solver."""
 def setUp(self):
  from contextlib import ExitStack
  from unittest.mock import patch
  import subprocess
  import scipy.optimize
  import search114
  self.stack=ExitStack();self.addCleanup(self.stack.close)
  for module,key in ((subprocess,'Popen'),(scipy.optimize,'milp'),(candidate,'milp'),(search114,'milp')):
   self.stack.enter_context(patch.object(module,key,side_effect=AssertionError('NO_SOLVER_OR_WORKER')))
  import parametric_pair_p04 as p04
  self.p04=p04
  self.rect=[6.125,5.125,9.275,7.375]
  self.proposal={'rectangles':{'bath':self.rect},'network_paths':{'bath':[[7.65,3.0],[7.65,3.0],[7.65,4.0],[7.65,4.0],[7.65,4.625]]}}
  import bathroom_module117,place_bathroom117
  base=bathroom_module117.build()
  self.model={'inputs':['18.1','22.2',2],'units':[],'walls':{},'wall_hosts':{},'source_wall_hosts':{},'openings':[]}
  for uid in ('A','B'):
   u={'id':uid,'rooms':{},'fixtures':{},'activities':{},'fixture_metadata':{},'routes':{},'route_targets':{}}
   self.model['units'].append(u)
   place_bathroom117.install(base,self.model,u,uid,self.rect,F('22.2'))
   u['rooms'].update(living=copy.deepcopy(self.model['module_aprons'][uid+'.bath']),
                     entry_circulation=[['0','0','1','1']],dining=[['1','1','2','2']])
   self.model['logical_regions'][uid+'.public_access']={'unit':uid,'source_roles':['living','entry_circulation']}
   for key,rect in u['activities'].items():
    a,b,c,d=map(F,rect);target=[str((a+c)/2),str((b+d)/2)]
    # Endpoint-only stored witness for this fixture, not physical path proof.
    u['routes'][key]=[target];u['route_targets'][key]=target
  self.fit={'proposal_digest':digest(self.proposal),'source_module_hashes':{'bath':digest(base)},
            'state':'PASS_LIMITED_CONSTRAINTS','core_digest':digest({})}
 def receipt(self):
  self.fit['proposal_digest']=digest(self.proposal)
  phys={'status':'FAIL','errors':[{'code':'SYNTHETIC_UNRELATED_PHYSICAL_FAIL'}],'model_hash':digest(self.model)}
  pin=digest(phys)
  r=self.p04.bath_alignment(self.proposal,self.model,self.fit,phys)
  self.assertEqual(digest(phys),pin);self.assertEqual(r['physical_digest'],pin)
  self.assertTrue(all(r[k] is False for k in self.p04.AUTHORITY))
  return r,phys
 def test_emitted_terminal_rows_match_source_module_offsets(self):
  import inspect,bathroom_module117
  from contract114 import GRID
  lines,line0=inspect.getsourcelines(candidate.propose)
  line=line0+next(i for i,s in enumerate(lines) if 'const(1.525 if name' in s)
  src=bathroom_module117.build()['external_ports'][0]
  result=candidate.propose(core_first(F(20),F(18)),2,sleep_roles=['double','twin'],diagnostic_capture=lambda data:data)
  bath=4*next(i for i,s in enumerate(result['specs']) if s[0]=='bath')
  indices=[i for i,r in enumerate(result['row_metadata']) if r['source_line']==line]
  found=[]
  for axis,offset in enumerate(src['center']):
   for ix in indices:
    row=result['matrix'].getrow(ix);coeff=dict(zip(row.indices,row.data))
    if coeff.get(bath+axis)==-1 and len(coeff)==2 and sorted(coeff.values())==[-1,1]:
     self.assertEqual(F(str(result['lower'][ix])),F(offset)/GRID)
     self.assertEqual(result['lower'][ix],result['upper'][ix]);found.append(axis)
  self.assertEqual(found,[0,1])
 def test_actual_public_launcher_reads_current_p10_pins_without_dispatch(self):
  from current_entry_launch_x03 import server
  with server('PUBLIC_WLN_18X20',0) as s:
   self.assertEqual(s.server_address[0],'127.0.0.1')
   self.assertGreater(s.server_port,0)
 def test_a_b_exact_decimal_and_source_no_binary_claim(self):
  r,_=self.receipt();rows=r['units']
  self.assertEqual([s['orientation'] for s in rows],['TRANSLATION','Y_REFLECTION'])
  for row in rows:
   self.assertEqual(row['state'],'ALIGNED_SOURCE_SUBSET_ONLY')
   self.assertTrue(row['decimal_terminal_matches_source'])
   self.assertFalse(row['binary64_terminal_equals_world_port_exact'])
   self.assertEqual(row['stored_activity_destinations_matched'],4)
 def test_one_emitted_decimal_quantum_is_not_a_tolerance(self):
  self.proposal['network_paths']['bath'][-1][0]=7.650001
  rows=self.receipt()[0]['units']
  self.assertTrue(all(row['codes']==['P10_PROPOSAL_DECIMAL_TERMINAL_MISMATCH'] for row in rows))
 def test_bad_port_identity_reflection_and_wrong_activity(self):
  self.model['module_ports'][1]['opening_id']='A.bath'
  self.model['module_placements'][1]['transform']['matrix'][1][1]=1
  self.model['units'][1]['route_targets']['basin_front']=['0','0']
  rows=self.receipt()[0]['units']
  self.assertEqual(rows[0]['codes'],[])
  self.assertEqual(rows[1]['codes'],['P10_INSTALLED_PLACEMENT_MISMATCH','P10_INSTALLED_PORT_MISMATCH',
                                    'P10_STORED_ACTIVITY_DESTINATION_MISMATCH'])
 def test_dining_not_typed_floor_and_missing_route_not_success(self):
  u=self.model['units'][0];u['rooms']['dining']=copy.deepcopy(u['rooms']['living'])
  u['rooms']['living']=[['0','0','1','1']]
  self.model['units'][1]['routes'].pop('WC_use')
  rows=self.receipt()[0]['units']
  self.assertEqual(rows[0]['codes'],['P10_APRON_DINING_INTRUSION','P10_APRON_NOT_ON_TYPED_PUBLIC_FLOOR',
                                    'P10_PORT_BODY_NOT_ON_TYPED_PUBLIC_FLOOR'])
  self.assertEqual(rows[1]['state'],'UNKNOWN_UNEVALUATED_GEOMETRY')
  self.assertEqual(rows[1]['stored_activity_routes_missing'],1)
 def test_noncontract_token_not_rounded(self):
  self.proposal['network_paths']['bath'][-1][0]=7.6500001
  self.fit['proposal_digest']=digest(self.proposal)
  phys={'model_hash':digest(self.model)}
  with self.assertRaisesRegex(ValueError,'^P10_NOT_PRODUCER_DECIMAL_TOKEN$'):
   self.p04.bath_alignment(self.proposal,self.model,self.fit,phys)
  self.assertEqual(self.p04.observe_bath_alignment(self.proposal,self.model,self.fit,phys)['state'],'UNKNOWN_UNVERIFIED_SOURCE_OR_INPUT')
 def test_completed_real_receipt_readback_with_rehashed_tamper(self):
  from unittest.mock import patch
  a,phys=self.receipt();mh=digest(self.model)
  reports={'physical':phys,'replay':{},'functional':{},'preconstruction_fit':self.fit,'bath_alignment_p10':a}
  bundle={'binding':{'source_core_digest':digest({}),'raw':{}},'packet':{'core':{},'world_model':self.model},'context':{},
          'proposal':self.proposal,'engine_revision':self.p04.ENGINE_REVISION,'model_digest':mh,
          'source_snapshot':{},'object_integrity_verified':True,'reports':reports,
          'report_digests':{key:digest(value) for key,value in reports.items()}}
  # Stub unrelated whole-packet/repo identity; actual P10 reconstruction and digest validation run.
  with patch.object(self.p04,'guard',return_value={}),patch.object(self.p04,'packet_binding',return_value=mh):
   self.assertTrue(self.p04.verify_completed(bundle))
   bundle['reports']['bath_alignment_p10']['units'][0]['apron_piece_count']+=1
   bundle['report_digests']['bath_alignment_p10']=digest(bundle['reports']['bath_alignment_p10'])
   with self.assertRaisesRegex(ValueError,'^P10_REPORT_READBACK$'):
    self.p04.verify_completed(bundle)
  self.assertEqual(bundle['reports']['physical'],phys)
if __name__=='__main__':unittest.main()
