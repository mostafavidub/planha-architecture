"""Source component and detached receipt tests; not whole-plan fixtures."""
import copy,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'app/local_integration'))
import core_choice_pair_study as s
from program_profile_registry import lookup
RAW={'W':'18','L':'20','n':2,'requested_count':1}
class CoreStudyTests(unittest.TestCase):
 def model(self,choice):
  core,_=s.selected_core(RAW,choice)
  m={'common_spaces':{k:copy.deepcopy(core[k])for k in('stair','lift','lobby')},'inputs':['18','20',2],
   'units':[{'id':u,'ownership':copy.deepcopy(core.get('unit_ownership',{}).get(u,[core['units'][u]]))}for u in('A','B')],
   'logical_regions':{u+'.public_access':{'unit':u,'source_roles':['living','entry_circulation']}for u in('A','B')},
   'openings':[{'id':u+'.entry','rect':[str(s.F(core['entry_centers'][u][0])-s.F('.65')),str(s.F(core['entry_centers'][u][1])-s.F('.075')),str(s.F(core['entry_centers'][u][0])+s.F('.65')),str(s.F(core['entry_centers'][u][1])+s.F('.075'))],'host_wall_id':u+'.unit_boundary','connects':['lobby',u+'.entry_circulation']}for u in('A','B')]}
  from entry117 import install
  install(m)
  from contract114 import S
  m['common_routes']={}
  for uid in ('A','B'):
   box=list(map(s.F,core['units'][uid]));ex=s.F(core['entry_centers'][uid][0]);ey=box[3]-s.F('.4')if uid=='A'else box[1]+s.F('.4')
   for src in ('stair','lift'):
    a,b,c,d=map(s.F,core[src]);cy=(b+d)/2;sx=c-s.F('.4')if src=='stair'else a+s.F('.4')
    m['common_routes'][src+'_'+uid]=[[S(x),S(y)]for x,y in ((sx,cy),(ex,cy),(ex,ey))]
  return core,m
 def test_both_source_components(self):
  for choice in s.CHOICES:
   core,m=self.model(choice);self.assertEqual(s.core_geometry(m,core)['errors'],[])
 def test_different_core_and_ownership(self):
  a,m=self.model(next(iter(s.CHOICES)));b,n=self.model('FRONT_REAR_FULL_BAND114')
  self.assertNotEqual(s.digest(a),s.digest(b));self.assertEqual(len(n['units'][0]['ownership']),1);self.assertEqual(len(m['units'][0]['ownership']),3)
 def test_raw_exact_types_and_domain(self):
  for key,v in [('n',True),('n',2.0),('n',1),('W','4.999'),('L','25.001'),('W','18x0'),('requested_count',True)]:
   raw=copy.deepcopy(RAW);raw[key]=v
   with self.subTest(key=key,value=v),self.assertRaises(ValueError):s.selected_core(raw,'FRONT_REAR_FULL_BAND114')
 def test_unknown_choice_and_no_hidden_program(self):
  with self.assertRaises(ValueError):s.selected_core(RAW,'OTHER')
  raw={**RAW,'program':2}
  with self.assertRaises(ValueError):s.selected_core(raw,'FRONT_REAR_FULL_BAND114')
 def test_profile_exact(self):
  p=lookup('PROGRAM_2BED_V1');s.bind_profile(p)
  for k,v in [('design_persons_per_unit',4.0),('version',True),('sleep_roles',['double','double']),('capacity_means_actual_population',0)]:
   bad=copy.deepcopy(p);bad[k]=v
   with self.assertRaises(ValueError):s.bind_profile(bad)
 def test_missing_lift_and_two_stairs(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');del m['common_spaces']['lift'];m['common_spaces']['stair2']=core['stair']
  self.assertIn('CORE_COMPONENT_INVENTORY',s.core_geometry(m,core)['errors'])
 def test_stair_entry_not_independent_lobby(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['openings'][0]['connects'][0]='stair'
  self.assertIn('INDEPENDENT_LOBBY_ENTRY_REQUIRED',s.core_geometry(m,core)['errors'])
 def test_duplicate_or_missing_entry(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['openings'].append(copy.deepcopy(m['openings'][0]))
  self.assertIn('INDEPENDENT_LOBBY_ENTRY_REQUIRED',s.core_geometry(m,core)['errors'])
  m['openings']=[]
  self.assertIn('INDEPENDENT_LOBBY_ENTRY_REQUIRED',s.core_geometry(m,core)['errors'])
 def test_public_access_rename_is_not_source_binding(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['logical_regions']['A.public_access']['source_roles']=['stair']
  self.assertIn('PUBLIC_ACCESS_SOURCE_ROLE_BINDING',s.core_geometry(m,core)['errors'])
 def test_ownership_overlap(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['units'][1]['ownership']=copy.deepcopy(m['units'][0]['ownership'])
  self.assertIn('UNIT_OWNERSHIP_OVERLAP',s.core_geometry(m,core)['errors'])
 def test_resized_lift_or_disconnected_lobby(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['common_spaces']['lift'][2]='17.7'
  self.assertIn('SOURCE_CLEAR_SIZES_CHANGED',s.core_geometry(m,core)['errors'])
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['common_spaces']['lobby']=[['5.1','8.625','6','9.5'],['7','8.625','8','9.5']]
  self.assertIn('LOBBY_GRAPH_DISCONNECTED',s.core_geometry(m,core)['errors'])
 def test_empty_stationary_and_malformed_common_route(self):
  for path,code in (([],'COMMON_ROUTE_TYPED_PATH_REQUIRED'),([['1','1'],['1','1']],'COMMON_ROUTE_NO_MOVEMENT'),([[1,'1'],['2','1']],'COMMON_ROUTE_TYPED_PATH_REQUIRED'),([['1','1'],['2','2']],'COMMON_ROUTE_NOT_ORTHOGONAL')):
   core,m=self.model('FRONT_REAR_FULL_BAND114');m['common_routes']['stair_A']=path
   self.assertIn(code,s.core_geometry(m,core)['errors'])
  core,m=self.model('FRONT_REAR_FULL_BAND114');del m['common_routes']['lift_B']
  self.assertIn('COMMON_ROUTE_INVENTORY',s.core_geometry(m,core)['errors'])
 def test_detached_receipt_mutations(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');profile=lookup('PROGRAM_2BED_V1')
  args=[RAW,'FRONT_REAR_FULL_BAND114',profile,core,{'A':{'x':1},'B':{'x':1}},m,{'file':'a'*64},'1'*32]
  receipt=s.make_receipt(*args);s.bind_receipt(receipt,*args)
  for i in range(len(args)):
   changed=copy.deepcopy(args)
   if i==1:changed[i]='FRONT_REAR_COMPACT118'
   elif i==7:changed[i]='2'*32
   elif i==0:changed[i]['W']='19'
   elif i==2:changed[i]['version']=1.0
   elif i==3:changed[i]['entry_centers']['A'][0]='0'
   elif i==4:changed[i]['B']['x']=True
   elif i==5:changed[i]['inputs'][0]='19'
   else:changed[i]['file']='b'*64
   with self.subTest(index=i),self.assertRaises(ValueError):s.bind_receipt(receipt,*changed)
 def test_receipt_authority_cannot_flip(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');args=[RAW,'FRONT_REAR_FULL_BAND114',lookup('PROGRAM_2BED_V1'),core,{},m,{},'1'*32]
  receipt=s.make_receipt(*args);receipt['accepted']=True
  with self.assertRaises(ValueError):s.bind_receipt(receipt,*args)
class AssessmentOnlyTests(unittest.TestCase):
 def test_status_aggregation_never_hides_failure(self):
  rows={'core_partition':{'status':'PASS_SOURCE_CORE_PARTITION_ONLY','errors':[],'pending':[]},
   'core_concept':{'status':'PASS_LIMITED','witness':{'errors':[],'pending':[]}},
   'opening_hosts':{'status':'PASS_LIMITED','witness':{'errors':[],'pending':[]}}}
  self.assertTrue(s.predicates_verified(rows))
  for state in ('FAIL','UNKNOWN','NOT_EVALUATED','EVALUATOR_ERROR'):
   bad=copy.deepcopy(rows);bad['core_concept']['status']=state;self.assertFalse(s.predicates_verified(bad))
  for key in ('errors','pending'):
   bad=copy.deepcopy(rows);bad['opening_hosts']['witness'][key]=['SYNTHETIC_BLOCKER'];self.assertFalse(s.predicates_verified(bad))
  bad=copy.deepcopy(rows);del bad['opening_hosts'];self.assertFalse(s.predicates_verified(bad))
  for field in ('errors','pending'):
   bad=copy.deepcopy(rows);del bad['core_concept']['witness'][field];self.assertFalse(s.predicates_verified(bad))
   for malformed in (None,False,(),'',{}):
    bad=copy.deepcopy(rows);bad['core_concept']['witness'][field]=malformed;self.assertFalse(s.predicates_verified(bad))
 def test_core_adapter_fixed_scope_before_model_access(self):
  raw={**RAW,'W':'19'}
  with self.assertRaisesRegex(ValueError,'CORE_ASSESSMENT_DIMENSION_SCOPE'):
   s.core_assessment(raw,'FRONT_REAR_FULL_BAND114',{},None,{},None,{},'1'*32,{}, {},{})
 def test_predicate_exception_stays_error(self):
  result=s.core_predicates({}, {})
  self.assertEqual(result['core_partition']['status'],'EVALUATOR_ERROR')
  self.assertFalse(s.predicates_verified(result))
if __name__=='__main__':unittest.main()

