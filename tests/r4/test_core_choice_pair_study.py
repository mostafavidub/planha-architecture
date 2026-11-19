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
   'openings':[{'id':u+'.entry','connects':['lobby',u+'.entry_circulation']}for u in('A','B')]}
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
 def test_ownership_overlap(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['units'][1]['ownership']=copy.deepcopy(m['units'][0]['ownership'])
  self.assertIn('UNIT_OWNERSHIP_OVERLAP',s.core_geometry(m,core)['errors'])
 def test_resized_lift_or_disconnected_lobby(self):
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['common_spaces']['lift'][2]='17.7'
  self.assertIn('SOURCE_CLEAR_SIZES_CHANGED',s.core_geometry(m,core)['errors'])
  core,m=self.model('FRONT_REAR_FULL_BAND114');m['common_spaces']['lobby']=[['5.1','8.625','6','9.5'],['7','8.625','8','9.5']]
  self.assertIn('LOBBY_GRAPH_DISCONNECTED',s.core_geometry(m,core)['errors'])
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
if __name__=='__main__':unittest.main()
