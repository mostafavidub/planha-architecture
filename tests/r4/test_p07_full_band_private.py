"""No optimizer test. Fixtures exercise archival validation, not physical acceptance."""
import copy, tempfile, time, unittest
from pathlib import Path
from unittest.mock import patch
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'studies'))
import p07_full_band_private as p

def fixture():
 from program_profile_registry import lookup
 s=p.stock();c,_=s.selected_core(p.RAW,p.CHOICE)
 other,_=s.selected_core(p.RAW,'FRONT_REAR_COMPACT118')
 prof=lookup('PROGRAM_2BED_V1')
 cfg={'schema':'P07_PRIVATE_LAUNCH_V1','nonce':'a'*32,'choice':p.CHOICE,'start':1,'deadline':241,
       'source':{'engine_revision':'e'*64,'files':{str(f.relative_to(p.ROOT)):p.sha(f.read_bytes()) for f in (p.STOCK,p.LOCAL/'program_profile_registry.py',p.ENGINE/'assemble114.py',p.ENGINE/'contract114.py')}},
       'inputs':{'raw_digest':p.digest(p.RAW),'core_digest':p.digest(c),'profile_digest':p.digest(prof),'different_compact_core_digest':p.digest(other)}}
 props={k:{'bedrooms':2,'sleep_roles':['double','twin'],'status':'PROPOSAL_ONLY','variant':0}for k in ('A','B')}
 m={'inputs':['18','20',2],'program':{'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin'],
   'design_occupants_per_unit':4,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True},
   'units':[{'id':u,'ownership':c.get('unit_ownership',{}).get(u,[c['units'][u]])}for u in ('A','B')],
   'accepted':False,'release_allowed':False,
   'common_spaces':{k:c[k]for k in ('stair','lift','lobby')},
   'common_routes':{k:['1']for k in ('stair_A','stair_B','lift_A','lift_B')},
   'openings':[{'id':u+'.entry','connects':['lobby',u+'.public_access']}for u in ('A','B')],
   'logical_regions':{u+'.public_access':{'unit':u,'source_roles':['living','entry_circulation']} for u in ('A','B')}}
 h={k:p.digest(q)for k,q in props.items()}
 pkt={'family':'FRONT_REAR','admission_claim':False,'core':c,'world_model':m,'local_model':m,'unit_proposal_hashes':h}
 ctx={'inputs':m['inputs'],'construction_trace':{'family':'FRONT_REAR','schema':'CONSTRUCTION_TRACE127_PAIR_V1','core_hash':p.digest(c),
  'raw':p.RAW,'local_model_hash':p.digest(m),'model_hash':p.digest(m),'source_revision':cfg['source']['engine_revision'],
  'proposals':props,'unit_proposal_hashes':h}}
 snap=cfg['source']['files'];r=s.make_receipt(p.RAW,p.CHOICE,prof,c,props,m,snap,cfg['nonce'])
 v=p.retained_packet({'raw':copy.deepcopy(p.RAW),'profile':prof,'core':c,'proposals':props,'packet':pkt,'ctx':ctx,
  'receipt':r,'snap':snap,'tr':{'coordinate_conversions':[],'before_digest':h['A'],'after_digest':h['A']},'out':{'stage':'INDEPENDENT_REPLAY'}},cfg)
 return cfg,copy.deepcopy(v)
class P07Tests(unittest.TestCase):
 def setUp(self):
  self.cfg,self.v=fixture()
 def test_stock_import_actual_and_full_band_core_is_distinct(self):
  self.assertEqual(p.stock().CHOICES[p.CHOICE],'full_band_core_first')
  self.assertEqual(p.inputs(),self.cfg['inputs'])
  self.assertNotEqual(p.inputs()['core_digest'],p.inputs()['different_compact_core_digest'])
 def test_synthetic_packet_binding_only(self):
  b=p.encode(self.v);self.assertEqual(p.bind_packet(p.decode(b),self.cfg),p.digest(self.v['packet']['world_model']))
  self.assertEqual(b,p.encode(self.v))
 def test_missing_model_not_complete(self):
  self.v['packet'].pop('world_model')
  with self.assertRaises(KeyError):p.bind_packet(self.v,self.cfg)
 def test_fake_model_tamper_even_if_changes_both_pointers(self):
  self.v['packet']['world_model']['program']['bedrooms_per_unit']=1
  self.v['packet']['local_model']['program']['bedrooms_per_unit']=1
  with self.assertRaisesRegex(ValueError,'P07_PACKET_TRACE'):p.bind_packet(self.v,self.cfg)
 def test_nonce_and_source_independently(self):
  for k,bad in (('nonce','b'*32),('source_digest','c'*64)):
   with self.subTest(k=k):
    v=copy.deepcopy(self.v);v[k]=bad
    with self.assertRaisesRegex(ValueError,'P07_CAPTURE_IDENTITY'):p.bind_packet(v,self.cfg)
 def test_raw_number_type_not_equal_by_python_coercion(self):
  self.v['raw']['n']=2.0
  with self.assertRaisesRegex(ValueError,'P07_INPUT_CORE_PROFILE'):p.bind_packet(self.v,self.cfg)
 def test_malformed_route_rejected_directly_not_only_by_hash(self):
  from core_choice_pair_study import core_geometry
  m=self.v['packet']['world_model']
  m['common_routes']={k:[['1','1'],['1','2']]for k in m['common_routes']}
  a=core_geometry(m,self.v['core'])
  self.assertEqual(a['status'],'PASS_SOURCE_CORE_PARTITION_ONLY') # shape/partition only, not actual use
  m['common_routes']['stair_A']=[]
  b=core_geometry(m,self.v['core'])
  self.assertEqual(b['status'],'FAIL')
  self.assertIn('COMMON_ROUTE_TYPED_PATH_REQUIRED',b['errors'])
 def test_partial_wait_and_missing_stock_completion_are_not_success(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t)
   with self.assertRaisesRegex(ValueError,'P07_PROCESS_NOT_COMPLETED'):
    p.archive_report(d,self.cfg,{'exit':-9,'timeout':True,'reaped':True,'observed_terminal':241})
   with self.assertRaises(FileNotFoundError):
    p.archive_report(d,self.cfg,{'exit':0,'timeout':False,'reaped':True,'observed_terminal':25})
 def test_cutoff_withholds_even_probable_success_and_retains_partial(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t);(d/'partial-private.txt').write_bytes(b'synthetic partial')
   def bogus():
    while True:time.sleep(.010)
   o=p.final_result(d,time.monotonic()+.04,bogus)
   self.assertEqual(o['state'],'DEADLINE_EXPIRED_PRIVATE_PARTIAL_ONLY')
   self.assertFalse(o['accepted'])
   self.assertFalse((d/'receipt.json').exists())
   self.assertEqual((d/'partial-private.txt').read_bytes(),b'synthetic partial')
   self.assertEqual(p.decode((d/'terminal-unverified.json').read_bytes()),o)
 def test_native_checkpoint_order_and_private_write_preserved(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t);v={'sink':1,'prep':2}
   x=p.write(d/'private.json',v,native_order=True)
   b=p.read(d/'private.json')
   self.assertEqual(b,b'{"sink":1,"prep":2}');self.assertEqual(x,p.sha(b))
   with self.assertRaises(FileExistsError):p.write(d/'private.json',{'not':'overwriting'})
   self.assertEqual(p.read(d/'private.json'),b)
if __name__=='__main__':unittest.main()
