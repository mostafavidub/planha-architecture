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
  return {'schema':'PLANNED_WITNESS_FIXED_SIZE_CONTRACT108_V2','enabled_causes':['PLANNED_GUEST_DINING_MOTION'],
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
if __name__=='__main__':unittest.main()

