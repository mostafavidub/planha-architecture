"""Synthetic preservation/cause predicates and real source constraint extraction, no solver."""
import copy,sys,unittest
from pathlib import Path
from fractions import Fraction as F
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import cause_directed_contract108 as c
import cause_directed_candidate108 as candidate
from contract114 import core_first
from same_version_front_rear_contract import digest
from protected_repair_contract import protected
class CauseTests(unittest.TestCase):
 def proposal(self):
  dims={'bed1':('5.45','3.6'),'bed2':('5.45','4.5'),'bath':('3.15','2.25'),'kitchen':('2.35','3.05'),'dining':('3.1','3.5'),
   'sofa1_use':('2.2','1.6'),'sofa2_use':('2.2','1.6'),'chair1_use':('.8','1.5'),'chair2_use':('.8','1.5'),'entry_apron':('2.65','.9')}
  return {'rectangles':{k:['0','0',*v]for k,v in dims.items()},'bed_door_sides':{'bed1':'right','bed2':'left'}}
 def packet(self):
  return {'core':{'scope':'synthetic'},'world_model':{'inputs':['18','22',2],'program':{'units':2},'profile':{'body_m':'.7'},'accepted':False,'release_allowed':False,
   'units':[{'id':u,'fixtures':{'bed':['0','0','2','2']},'fixture_metadata':{'bed':{'kind':'bed','source_size_m':['2','2']}}}for u in('A','B')]}}
 def contract(self):
  p=self.proposal();packet=self.packet()
  return {'schema':'CAUSE_DIRECTED_FIXED_SIZE_CONTRACT108_V1','enabled_causes':['BATH_APRON_DINING'],'rectangle_dimensions':c.dimensions(p),'bed_door_sides':p['bed_door_sides'],
   'protected':protected(packet),'parent_model_digest':digest(packet['world_model']),'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
 def test_direct_bath_geometry_requires_overlap_and_outside(self):
  apron=[['0','0','1','1']];dining=[['.5','0','1.5','1']]
  self.assertTrue(c.bath_geometry(apron,dining,[['0','0','.5','1']])['direct_geometry_failure'])
  self.assertFalse(c.bath_geometry(apron,dining,apron)['direct_geometry_failure'])
  self.assertFalse(c.bath_geometry(apron,[['2','2','3','3']],[])['direct_geometry_failure'])
 def test_actual_source_bath_pieces_geometry_not_receipt(self):
  import bathroom_module117
  module=bathroom_module117.build('3.15','2.25');a=module['unit']['rooms']['public_access']
  self.assertTrue(c.bath_geometry(a,a,[])['direct_geometry_failure'])
  self.assertFalse(c.bath_geometry(a,a,a)['direct_geometry_failure'])
 def test_unknown_current_state_and_authority_fail_closed(self):
  base={'state':'UNKNOWN','model_digest':'hash','accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
  c.validate_current_report(base,'hash')
  for state in (None,'NEW_STATE','EVALUATOR_ERROR'):
   bad=copy.deepcopy(base);bad['state']=state
   with self.assertRaisesRegex(ValueError,'CURRENT_STATE_NOT_ALLOWED'):c.validate_current_report(bad,'hash')
  bad=copy.deepcopy(base);bad['qualified']=True
  with self.assertRaisesRegex(ValueError,'CURRENT_REPORT_AUTHORITY'):c.validate_current_report(bad,'hash')
 def test_error_code_requires_same_unit_and_room(self):
  errors=[{'code':'MODULE_APRON_NOT_REAL_PUBLIC_FLOOR','unit':'B','room':'bath'},{'code':'MODULE_APRON_NOT_REAL_PUBLIC_FLOOR','unit':'A','room':'bed1'}]
  self.assertEqual(c.target_error_count(errors,'A'),0);self.assertEqual(c.target_error_count(errors,'B'),1)
 def test_no_supported_cause_fails_closed(self):
  v=self.contract();v['enabled_causes']=[]
  with self.assertRaisesRegex(ValueError,'SUPPORTED_CAUSE_REQUIRED'):c.validate_parent_contract(v,[])
 def test_cause_switch_mismatch_rejected(self):
  with self.assertRaisesRegex(ValueError,'ENABLED_CAUSE_BINDING'):c.validate_parent_contract(self.contract(),['KITCHEN_GUEST_MOTION'])
 def test_rehashed_contract_changes_rejected_by_parent_comparison(self):
  expected=self.contract();changed=copy.deepcopy(expected);changed['rectangle_dimensions']['bed1']['width']='6'
  self.assertNotEqual(digest(changed),digest(expected))
  with patch.object(c,'freeze',return_value=expected):
   with self.assertRaisesRegex(ValueError,'PARENT_CONTRACT_BINDING'):c.bind_parent(changed,None,None,None,None,None,None,None,None)
 def test_synthetic_position_move_preserves_exact_dimensions(self):
  p=self.packet();v=self.contract();p['world_model']['units'][0]['fixtures']['bed']=['1','0','3','2']
  self.assertTrue(c.check_child(v,p,{'A':self.proposal(),'B':self.proposal()})['protected_verified'])
 def test_actual_dimension_and_typed_program_mutations_rejected(self):
  for field in('fixture','program','core','profile'):
   p=self.packet();v=self.contract()
   if field=='fixture':p['world_model']['units'][0]['fixtures']['bed'][2]='3'
   elif field=='program':p['world_model']['program']['units']=True
   elif field=='core':p['core']['scope']='changed'
   else:p['world_model']['profile']['body_m']='.6'
   with self.assertRaisesRegex(ValueError,'CHILD_PROTECTED_STATE_CHANGED'):c.check_child(v,p,{'A':self.proposal(),'B':self.proposal()})
 def test_door_side_and_room_dimension_changes_rejected(self):
  packet=self.packet();packet['world_model']['units'][0]['fixtures']['bed']=['1','0','3','2']
  for mode in ('door','dimension'):
   p=self.proposal()
   if mode=='door':p['bed_door_sides']['bed1']='left'
   else:p['rectangles']['bed1'][2]='6'
   with self.assertRaises(ValueError):c.check_child(self.contract(),packet,{'A':p,'B':self.proposal()})
 def test_resolution_missing_path_never_counts_as_fixed(self):
  parent={'model_digest':'parent','selected_causes':['KITCHEN_GUEST_MOTION'],'rows':[{'unit':'A','cause':'KITCHEN_GUEST_MOTION','route':'guest_dining','established':True}]}
  child={'model_digest':'child','selected_causes':[],'rows':[{'unit':'A','cause':'KITCHEN_GUEST_MOTION','route':'guest_dining','established':False,'state':'NO_STORED_ACTUAL_PATH_NO_CAUSE_CLAIM'}]}
  self.assertFalse(c.resolution(parent,child)['all_target_causes_resolved'])
  child['rows'][0]['state']='ACTUAL_STORED_PATH_CLEAR';self.assertTrue(c.resolution(parent,child)['all_target_causes_resolved'])
 def test_real_constraint_switches_and_locked_dimensions_without_solver(self):
  counts={}
  for causes in (['BATH_APRON_DINING'],['KITCHEN_GUEST_MOTION'],['BATH_APRON_DINING','KITCHEN_GUEST_MOTION']):
   v=self.contract();v['enabled_causes']=causes
   with patch.object(candidate,'milp',side_effect=AssertionError('NO_SOLVER'))as solver:
    actual=candidate.propose(core_first(F(18),F(22)),2,sleep_roles=['double','twin'],parent_contract=v,enabled_causes=causes,
     diagnostic_capture=lambda d:d)
   solver.assert_not_called();self.assertIn('matrix',actual)
   rows=actual['matrix'].toarray();lo=actual['lower'];hi=actual['upper'];groups=[r['group']for r in actual['row_metadata']]
   for i,spec in enumerate(actual['specs']):
    for axis,key in ((2,'width'),(3,'height')):
     val=float(F(v['rectangle_dimensions'][spec[0]][key])/F('.005'))
     self.assertTrue(any(row[4*i+axis]==1 and sum(x!=0 for x in row)==1 and a==b==val for row,a,b in zip(rows,lo,hi)))
   counts[tuple(causes)]=len(rows)
   if 'BATH_APRON_DINING'not in causes:self.assertNotIn('source_actual_bath_apron_dining_role',groups)
  self.assertGreater(counts[('BATH_APRON_DINING','KITCHEN_GUEST_MOTION')],counts[('BATH_APRON_DINING',)])
  self.assertGreater(counts[('BATH_APRON_DINING','KITCHEN_GUEST_MOTION')],counts[('KITCHEN_GUEST_MOTION',)])
if __name__=='__main__':unittest.main()
