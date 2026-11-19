"""Source-profile geometry and explicit planned-cause adapter; no solver or private data."""
import copy,sys,unittest
from pathlib import Path
from fractions import Fraction as F
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import planned_witness_contract108 as c
import planned_witness_support108 as support
import cause_directed_candidate108 as candidate
from core_choice_pair_study import selected_core
from same_version_front_rear_contract import digest
from protected_repair_contract import protected
class PlannedTests(unittest.TestCase):
 def scene(self):
  return {'body':'.7','parts':[['0','0','6','6']],'owner':[['0','0','6','6']],
   'obstacles':[['2','1.8','3','2.2']],'labels':['kitchen_motion:0']}
 def path(self):return [['1','2'],['4','2']]
 def contract(self):
  dims={'bed1':('5.45','3.6'),'bed2':('5.45','4.5'),'bath':('3.15','2.25'),'kitchen':('2.35','3.05'),'dining':('3.1','3.5'),
   'sofa1_use':('2.2','1.6'),'sofa2_use':('2.2','1.6'),'chair1_use':('.8','1.5'),'chair2_use':('.8','1.5'),'entry_apron':('2.65','.9')}
  return {'schema':'COMPOUND_PLANNED_FIXED_SIZE_CONTRACT108_V3','enabled_causes':['PLANNED_GUEST_DINING_MOTION'],
   'rectangle_dimensions':{k:{'width':v[0],'height':v[1]}for k,v in dims.items()},'bed_door_sides':{'bed1':'right','bed2':'left'},
   'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
 def test_source_pins(self):self.assertTrue(support.source_guard())
 def test_world_transform_exact_same_proposal(self):
  p={'network_paths':{'dining_east':[[1.25,2.5],[3,2.5]]}}
  before=digest(p)
  self.assertEqual(c.world_path(p,'A','20'),[['5/4','5/2'],['3','5/2']])
  self.assertEqual(c.world_path(p,'B','20'),[['5/4','35/2'],['3','35/2']])
  self.assertEqual(digest(p),before)
 def test_no_invented_path_or_boolean_coordinate(self):
  for p in ({},{'network_paths':{'dining_east':[[True,2],[3,2]]}}):
   with self.assertRaises(ValueError):c.world_path(p,'A','20')
 def test_missing_original_code_same_unit_route(self):
  report={'errors':[{'code':'MISSING_REQUIRED_ACTIVITY_ROUTES','failures':[{'unit':'A','route':'guest_dining'},{'unit':'B','route':'guest_living'}]}]}
  self.assertEqual(c.missing_count(report,'A'),1);self.assertEqual(c.missing_count(report,'B'),0)
  report['errors'][0]['code']='OTHER';self.assertEqual(c.missing_count(report,'A'),0)
 def test_exact_exclusive_motion(self):
  p=self.path();self.assertEqual(c.isolated_motion(p,p[0],p[-1],self.scene()),['kitchen_motion:0'])
 def test_nonmotion_collision_never_cause(self):
  s=self.scene();s['obstacles'].append(['2','1','3','3']);s['labels'].append('whole_kitchen:0')
  with self.assertRaisesRegex(ValueError,'ROUTE_OBSTACLE_COLLISION'):c.isolated_motion(self.path(),['1','2'],['4','2'],s)
 def test_endpoint_cannot_be_repaired_by_connector(self):
  with self.assertRaisesRegex(ValueError,'ROUTE_ENDPOINT'):c.isolated_motion(self.path(),['1.1','2'],['4','2'],self.scene())
 def test_domain_and_owner_rejection(self):
  for key in ('parts','owner'):
   s=self.scene();s[key]=[['0','0','1.5','6']]
   with self.assertRaises(ValueError):c.isolated_motion(self.path(),['1','2'],['4','2'],s)
 def test_motion_absent_is_not_cause(self):
  s=self.scene();s['obstacles']=[];s['labels']=[]
  with self.assertRaisesRegex(ValueError,'PLANNED_NOT_EXCLUSIVE_MOTION'):c.isolated_motion(self.path(),['1','2'],['4','2'],s)
 def test_original_profile_contains_whole_kitchen_bath_not_living_occupancy(self):
  u={'id':'A','ownership':[['0','0','8','8']],'rooms':{'bath':[['0','0','1','1']],'kitchen':[['4','4','6','6']]},'fixtures':{},
   'public_program':{'capacity':{'living_seats':[{'occupied_body':['1','1','2','2']}]}}}
  m={'walls':{},'profile':{'body_m':'.7'},'operations':{'doors':[],'dining_chairs':[],'kitchen':[{'unit':'A','motion_envelopes':[['3','3','4','4']]}]}}
  s=c.original_guest_scene(m,u)
  self.assertEqual(s['labels'],['private:bath:0','whole_kitchen:0','kitchen_motion:0'])
  self.assertEqual(len(s['obstacles']),3)
 def test_operator_mapping_is_explicit_and_nonmutating(self):
  x=self.contract();before=digest(x);op=c.candidate_contract(x)
  self.assertEqual(x['enabled_causes'],['PLANNED_GUEST_DINING_MOTION'])
  self.assertEqual(op['enabled_causes'],['KITCHEN_GUEST_MOTION'])
  self.assertEqual(op['operator_adapter']['source_contract_digest'],before);self.assertEqual(digest(x),before)
 def test_old_stored_contract_not_silently_accepted(self):
  v=self.contract();v['schema']='CAUSE_DIRECTED_FIXED_SIZE_CONTRACT108_V1'
  with self.assertRaisesRegex(ValueError,'PARENT_CONTRACT_SCHEMA'):c.candidate_contract(v)
 def test_actual_operator_constraints_capture_without_solver(self):
  v=c.candidate_contract(self.contract())
  core,_=selected_core({'W':'18','L':'20','n':2,'requested_count':1},'FRONT_REAR_COMPACT118')
  with patch.object(candidate,'milp',side_effect=AssertionError('NO_SOLVER'))as solver:
   out=candidate.propose(core,2,variant=0,sleep_roles=['double','twin'],topology='SIDE_ROOTED_SERVICES',
    parent_contract=v,enabled_causes=v['enabled_causes'],diagnostic_capture=lambda d:d)
  solver.assert_not_called();self.assertIn('matrix',out)
  self.assertNotIn('source_actual_bath_apron_dining_role',[r['group']for r in out['row_metadata']])
 def test_resolution_requires_actual_route_and_original_missing_gone(self):
  p={'model_digest':'parent','selected_causes':['PLANNED_GUEST_DINING_MOTION'],'rows':[{'unit':'A','cause':'PLANNED_GUEST_DINING_MOTION','route':'guest_dining','established':True}]}
  row={'unit':'A','cause':'PLANNED_GUEST_DINING_MOTION','route':'guest_dining','established':False,'original_missing_route_count':0}
  ch={'model_digest':'child','selected_causes':[],'rows':[row]}
  for state in ('NOT_ESTABLISHED','ACTUAL_STORED_PATH_CLEAR','PLANNED_PATH_CLEAR'):
   row['state']=state;self.assertFalse(c.resolution(p,ch)['all_target_causes_resolved'])
  row['state']='ACTUAL_STORED_PATH_CLEAR_ORIGINAL_PROFILE';self.assertTrue(c.resolution(p,ch)['all_target_causes_resolved'])
  row['original_missing_route_count']=1;self.assertFalse(c.resolution(p,ch)['all_target_causes_resolved'])
 def test_rehashed_contract_binding_uses_new_freeze(self):
  expected=self.contract();bad=copy.deepcopy(expected);bad['bed_door_sides']['bed1']='left'
  with patch.object(c,'freeze',return_value=expected):
   with self.assertRaisesRegex(ValueError,'PARENT_CONTRACT_BINDING'):c.bind_parent(bad,None,None,None,None,None,None,None,None)
 def test_context_wrong_family_schema_typed_count_and_units(self):
  proposals={'A':{},'B':{}};m={'units':[{'id':'A'},{'id':'B'}],'inputs':['18','20',2]}
  ctx={'construction_trace':{'schema':'CONSTRUCTION_TRACE127_PAIR_V1','family':'FRONT_REAR','raw':{'W':'18','L':'20','n':2},'model_hash':digest(m),'proposals':proposals}}
  c.bind_context(m,proposals,'20',ctx)
  for key,value in(('family','LEFT_RIGHT'),('schema','UNKNOWN')):
   bad=copy.deepcopy(ctx);bad['construction_trace'][key]=value
   with self.assertRaisesRegex(ValueError,'PLANNED_TRACE_FAMILY'):c.bind_context(m,proposals,'20',bad)
  bad=copy.deepcopy(ctx);bad['construction_trace']['raw']['n']=True
  with self.assertRaisesRegex(ValueError,'PLANNED_UNIT_COUNT'):c.bind_context(m,proposals,'20',bad)
  badm=copy.deepcopy(m);badm['units'][1]['id']='A'
  with self.assertRaisesRegex(ValueError,'PLANNED_PAIR_UNITS'):c.bind_context(badm,proposals,'20',ctx)
 def test_actual_source_standing_binding_for_existing_route(self):
  from dining_module118 import build
  module=build('3.1','3.5')
  idmap={k:'dining_'+k for k in module['fixtures']}
  seat=next(s for s in module['seating']['instances']if s['fixture_id']=='chair_east')
  u={'fixtures':{idmap[k]:v for k,v in module['fixtures'].items()},'activities':{'dining_east':seat['rise_transfer']['standing_body']},
   'public_program':{'destinations':{'guest_dining':{'activity_id':'dining_east','fixture_id':'dining_chair_east'}}},
   'scenario_routes':{'guest_dining':[['0','0'],['1','0']]},
   'dining_module_placement':{'module':module,'module_hash':digest(module),'transform':{'matrix':[[1,0],[0,1]],'translation':['0','0']},'id_map':idmap}}
  self.assertEqual(len(c.actual_destination(u)),2)
  for field in('activity','fixture','id'):
   bad=copy.deepcopy(u)
   if field=='activity':bad['activities']['dining_east']=['0','0','1','1']
   elif field=='fixture':bad['fixtures']['dining_chair_east']=['0','0','1','1']
   else:bad['public_program']['destinations']['guest_dining']['fixture_id']='dining_chair_west'
   with self.assertRaises(ValueError):c.actual_destination(bad)
 def test_solver_metadata_exact_types_and_nonfinite(self):
  p={'solver_status':2,'solver_seconds':.02,'budget_seconds':30}
  self.assertEqual(support.solver_observation(p),p)
  for key,value in(('solver_status',True),('solver_seconds',float('nan')),('budget_seconds',False)):
   bad=dict(p);bad[key]=value
   with self.assertRaisesRegex(ValueError,'SOLVER_OBSERVATION_TYPE'):support.solver_observation(bad)
 def test_source_bound_conflict_is_not_missing_solver_telemetry(self):
  p={'status':'NO_PROPOSAL_IN_THIS_PROGRAM','reason':'ROOM_OR_CORE_BOUND_CONFLICT'}
  self.assertIs(support.solver_observation(p)['solver_called'],False)
  bad=dict(p);bad['solver_status']=2
  with self.assertRaisesRegex(ValueError,'PRE_SOLVER_OBSERVATION_CONFLICT'):support.solver_observation(bad)
  with self.assertRaisesRegex(ValueError,'SOLVER_OBSERVATION_TYPE'):support.solver_observation({'status':'NO_PROPOSAL_IN_THIS_TOPOLOGY'})
 def compound_fixture(self):
  from entry117 import install
  core,_=selected_core({'W':'18','L':'20','n':2,'requested_count':1},'FRONT_REAR_COMPACT118')
  ex=F(core['entry_centers']['A'][0]);y,yt=F(core['band'][1]),F(core['band'][3])
  m={'openings':[{'id':uid+'.entry','rect':list(map(str,[ex-F('.65'),lo,ex+F('.65'),hi])),'host_wall_id':uid+'.unit_boundary'}for uid,lo,hi in(('A',y-F('.15'),y),('B',yt,yt+F('.15')))],'operations':{}}
  install(m)
  root=[str(ex),str(F(core['units']['A'][3])-F('.4'))]
  p={'network_paths':{'dining_east':[root,[str(ex+1),root[1]]]}}
  proposals={'A':copy.deepcopy(p),'B':copy.deepcopy(p)}
  v=self.contract();v['enabled_causes']=['PLANNED_ENTRY_PANEL_AND_KITCHEN_MOTION'];v['core_digest']=digest(core)
  v['entry_source_binding']=c.entry_binding(m,proposals,'20')
  return core,m,proposals,v
 def test_actual_entry_source_both_roots_and_mirror(self):
  core,m,ps,v=self.compound_fixture()
  binding=v['entry_source_binding']
  self.assertTrue(all(x['root_body_clear']for x in binding['units']))
  self.assertEqual(len(binding['local_panel']),4)
  bad=copy.deepcopy(m);bad['operations']['doors'][0]['open_panel'][0]='0'
  with self.assertRaisesRegex(ValueError,'ENTRY_OPERATION_SOURCE_REBUILD'):c.entry_binding(bad,ps,'20')
  badps=copy.deepcopy(ps);badps['A']['network_paths']['dining_east'][0][0]=binding['local_panel'][0]
  with self.assertRaisesRegex(ValueError,'ENTRY_ROOT_BODY_COLLISION'):c.entry_binding(m,badps,'20')
 def test_compound_requires_both_and_no_other_obstacle(self):
  p=[['1','2'],['5','2']];s=self.scene()
  s['obstacles']=[['2','1.8','2.5','2.2'],['4','1.8','4.5','2.2']];s['labels']=['open_panel:A.entry','kitchen_motion:4']
  self.assertEqual(c.compound_motion(p,p[0],p[-1],s,'open_panel:A.entry'),['kitchen_motion:4','open_panel:A.entry'])
  for index in(0,1):
   bad=copy.deepcopy(s);bad['obstacles'].pop(index);bad['labels'].pop(index)
   with self.assertRaisesRegex(ValueError,'COMPOUND_CAUSE_SET'):c.compound_motion(p,p[0],p[-1],bad,'open_panel:A.entry')
  s['obstacles'].append(['3','1','3.5','3']);s['labels'].append('wall:synthetic')
  with self.assertRaisesRegex(ValueError,'ROUTE_OBSTACLE_COLLISION'):c.compound_motion(p,p[0],p[-1],s,'open_panel:A.entry')
 def test_actual_matrix_old_prefix_exact_new_panel_rows(self):
  import compound_panel_candidate108 as new
  core,m,ps,v=self.compound_fixture();op=c.candidate_contract(v)
  opts={'sleep_roles':['double','twin'],'parent_contract':op,'enabled_causes':op['enabled_causes'],'diagnostic_capture':lambda d:d}
  with patch.object(candidate,'milp',side_effect=AssertionError('NO_SOLVER'))as oldsolver,patch.object(new,'milp',side_effect=AssertionError('NO_SOLVER'))as newsolver:
   a=candidate.propose(core,2,**opts);b=new.propose(core,2,**opts)
  oldsolver.assert_not_called();newsolver.assert_not_called()
  result=support.compare_panel_capture(a,b);self.assertTrue(result['verified']);self.assertGreater(result['reserved_body_segments'],1)
  bad=copy.deepcopy(b);bad['matrix'].data[0]+=1
  with self.assertRaisesRegex(ValueError,'PANEL_OLD_CSR_CHANGED'):support.compare_panel_capture(a,bad)
  bad=copy.deepcopy(b);bad['objective'][0]+=1
  with self.assertRaisesRegex(ValueError,'PANEL_OLD_VECTOR_CHANGED'):support.compare_panel_capture(a,bad)
 def test_reservation_wrong_core_or_rootproof_rejected(self):
  core,m,ps,v=self.compound_fixture();op=c.candidate_contract(v)
  self.assertEqual(c.panel_reservation(op,core),v['entry_source_binding']['local_panel'])
  bad=copy.deepcopy(core);bad['extra']='not_same'
  with self.assertRaisesRegex(ValueError,'ENTRY_RESERVATION_CORE'):c.panel_reservation(op,bad)
  op['entry_panel_reservation']['units'][0]['root_body_clear']=False
  with self.assertRaisesRegex(ValueError,'ENTRY_RESERVATION_ROOTS'):c.panel_reservation(op,core)
 def test_actual_appended_sharedroot_rows_reject_panel_overlap_allow_contact(self):
  import itertools,numpy as np
  import compound_panel_candidate108 as new
  core,m,ps,v=self.compound_fixture();op=c.candidate_contract(v)
  opts={'sleep_roles':['double','twin'],'parent_contract':op,'enabled_causes':op['enabled_causes'],'diagnostic_capture':lambda d:d}
  a=candidate.propose(core,2,**opts);b=new.propose(core,2,**opts);m0,n=a['matrix'].shape
  rows=b['matrix'][m0:m0+5].toarray();lo=b['lower'][m0:m0+5];hi=b['upper'][m0:m0+5]
  jhi=np.flatnonzero(rows[1,:n])[0];jlo=np.flatnonzero(rows[2,:n])[0]
  grid=F('.005');root=F(ps['A']['network_paths']['dining_east'][0][0]);panel=list(map(F,v['entry_source_binding']['local_panel']))
  def feasible(end):
   x=np.zeros(b['matrix'].shape[1]);x[jlo]=float(min(root,end)/grid);x[jhi]=float(max(root,end)/grid)
   for bits in itertools.product((0,1),repeat=4):
    x[n:n+4]=bits;value=rows@x
    if np.all(value>=lo-1e-8)and np.all(value<=hi+1e-8):return True
   return False
  self.assertTrue(feasible(root))
  self.assertTrue(feasible(panel[0]-F('.35')))
  self.assertFalse(feasible(panel[0]-F('.35')+grid))
  self.assertFalse(feasible(panel[2]))
if __name__=='__main__':unittest.main()

