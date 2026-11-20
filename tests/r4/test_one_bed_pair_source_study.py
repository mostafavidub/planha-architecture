import copy,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
from one_bed_pair_source_study import normalize_proposal,program_bind,code_counts,stop_process,RECTS,TERMINALS,digest
def proposal():
 return {'bedrooms':1,'sleep_roles':['double'],'rectangles':{k:[0.,0.,1.,1.]for k in RECTS},'network_paths':{k:[[0.,0.]for _ in range(5)]for k in TERMINALS},'bed_door_sides':{'bed1':'left'}}
class OneBed(unittest.TestCase):
 def test_exact_one_bed_roles_and_no_mutation(self):
  p=proposal();h=digest(p);q,r=normalize_proposal(p);self.assertEqual(digest(q),h);self.assertEqual(digest(p),h)
 def test_no_bed2_hidden_fallback(self):
  p=proposal();p['rectangles']['bed2']=[0.,0.,1.,1.]
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_program_types_and_roles(self):
  for value in (True,1.0,2):
   p=proposal();p['bedrooms']=value
   with self.assertRaises(ValueError):normalize_proposal(p)
  p=proposal();p['sleep_roles']=['twin']
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_terminal_missing_and_wrong_dining_alias(self):
  p=proposal();p['network_paths']['dining']=p['network_paths'].pop('dining_west')
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_binary64_lossless_and_wrong_role(self):
  import numpy as np
  p=proposal();p['rectangles']['bed1'][0]=np.float64(-0.0)
  q,r=normalize_proposal(p);self.assertEqual(r['conversions'],1);self.assertEqual(q['rectangles']['bed1'][0].hex(),'-0x0.0p+0')
  p=proposal();p['metadata']=np.float64(1)
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_bad_scalar_and_path(self):
  for value in (False,float('nan'),float('inf'),'1'):
   p=proposal();p['rectangles']['bed1'][0]=value
   with self.assertRaises(ValueError):normalize_proposal(p)
  p=proposal();p['network_paths']['bed1'].pop()
  with self.assertRaises(ValueError):normalize_proposal(p)
 def test_registry_and_model_count_not_population(self):
  p={'id':'PROGRAM_1BED_V1','approval':{'status':'APPROVED_DESIGN_PROGRAM'},'bedrooms_per_unit':1,'design_persons_per_unit':2,'sleep_roles':['double'],'capacity_means_actual_population':False}
  m={'program':{'units':2,'bedrooms_per_unit':1,'sleep_roles':['double'],'design_occupants_per_unit':2,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True},'units':[{'id':'A'},{'id':'B'}],'accepted':False,'release_allowed':False}
  program_bind(m,p);m['program']['design_occupants_per_unit']=4
  with self.assertRaises(ValueError):program_bind(m,p)
 def test_timeout_exit_race_still_waits(self):
  from unittest.mock import Mock,patch
  proc=Mock();proc.pid=12345
  with patch('one_bed_pair_source_study.os.killpg',side_effect=ProcessLookupError):stop_process(proc)
  proc.wait.assert_called_once_with()
 def test_timeout_normal_group_kill_and_wait(self):
  from unittest.mock import Mock,patch
  import signal
  proc=Mock();proc.pid=12345
  with patch('one_bed_pair_source_study.os.killpg')as kill:stop_process(proc);kill.assert_called_once_with(12345,signal.SIGKILL)
  proc.wait.assert_called_once_with()
 def test_error_code_counts_do_not_publish_details(self):
  self.assertEqual(code_counts([{'code':'MISSING_ROUTE','detail':'private text'},'RULE_NOT_EVALUATED:private identifier','bad secret'] ),
   {'MISSING_ROUTE':1,'RULE_NOT_EVALUATED':1,'UNCLASSIFIED':1})
 def test_side_keys_and_type(self):
  p=proposal();p['bed_door_sides']['bed2']='left'
  with self.assertRaises(ValueError):normalize_proposal(p)
class P14N2OneBedroomStudy(unittest.TestCase):
 BODY=b'{"W":"18","L":"20","n":2}'
 def setUp(self):
  from contextlib import ExitStack
  from unittest.mock import patch
  import scipy.optimize,search114,subprocess
  self.g=ExitStack();self.addCleanup(self.g.close)
  for mod,name in ((scipy.optimize,'milp'),(search114,'milp'),(subprocess,'Popen')):
   self.g.enter_context(patch.object(mod,name,side_effect=AssertionError('NO_SOLVER_OR_WORKER')))
  import one_bed_pair_p14 as p14
  self.p=p14
 def p1_model(self):
  return {'inputs':['18','20',2],
    'program':{'units':2,'bedrooms_per_unit':1,'sleep_roles':['double'],'design_occupants_per_unit':2,'capacity_profile':'LEGACY_SOURCE_PROGRAM','provisional':True},
    'units':[{'id':uid} for uid in ('A','B')],'accepted':False,'release_allowed':False}
 def test_explicit_preflight_only_n2_p1_no_public_program_field(self):
  p=self.p.prepare(self.BODY);self.assertEqual(p['raw'],self.p.RAW)
  self.assertEqual(p['programme']['id'],'PROGRAM_1BED_V1');self.assertEqual(p['programme']['design_persons_per_unit'],2)
  for body in (b'{"W":"18","L":"20","n":1}',b'{"W":"18","L":"22","n":2}',b'{"W":"18","L":"20","n":2.0}',
               b'{"W":"18","L":"20","n":2,"programme":"PROGRAM_1BED_V1"}'):
   with self.assertRaises(ValueError):self.p.prepare(body)
 def test_real_source_components_one_bed_four_seats_not_capacity_upgrade(self):
  import json
  from fractions import Fraction as F
  from contract114 import S
  from bedroom_module116 import build as bed
  from bathroom_module117 import build as bath
  from kitchen_module117 import build as kit
  from dining_module118 import build as din
  p=self.p;model=self.p1_model();model['module_placements']=[]
  cat=json.loads((p.ENGINE/'fixture_catalog114.json').read_bytes());model['fixture_catalog_hash']=digest(cat)
  modules={'bed1':bed('5.45','3.6'),'bath':bath(),'kitchen':kit('2.35','3.05')}
  for u in model['units']:
   uid=u['id'];u.update(fixtures={},fixture_metadata={},activities={},rooms={'bed1':[['1','1','2','2']]},
                         public_program={'capacity':{'residents':2}})
   for i,(room,module)in enumerate(modules.items()):
    t={'matrix':[[1,0],[0,1 if uid=='A'else -1]],'translation':[str(i*4+1),'5'if uid=='A'else'15']}
    ids={k:k for field in ('fixtures','activities') for k in module['unit'][field]}
    for field in ('fixtures','activities'):
     u[field].update({k:list(map(S,p.placed(q,t))) for k,q in module['unit'][field].items()})
    u['fixture_metadata'].update(copy.deepcopy(module['unit']['fixture_metadata']))
    model['module_placements'].append({'unit_id':uid,'room_id':room,'module':module,'module_hash':digest(module),'id_map':ids,'transform':t})
   dm=din();ids={k:'dining_'+k for k in dm['fixtures']}
   u['dining_module_placement']={'module':dm,'module_hash':digest(dm),'id_map':ids,'transform':t}
   for key,q in dm['fixtures'].items():
    fid=ids[key];u['fixtures'][fid]=list(map(S,p.placed(q,t)))
    u['fixture_metadata'][fid]={'kind':'dining_table' if key=='table' else 'dining_chair_front' if key in ('chair_front','chair_west')else'dining_chair_back'}
   for seat in dm['seating']['instances']:
    u['activities']['dining_'+seat['id'][5:]]=list(map(S,p.placed(seat['rise_transfer']['standing_body'],t)))
   for fid in ('sofa1','sofa2','armchair1','armchair2'):
    d=cat['types'][fid];u['fixtures'][fid]=['0','0',d['width_m'],d['depth_m']]
    u['fixture_metadata'][fid]={'kind':fid};u['activities'][fid+'_front']=['0','0','1','1']
  profile=p.prepare(self.BODY)['programme'];pins=digest(model)
  out=p.inventory(model,profile,cat)
  for row in out:
   self.assertEqual((row['design_persons'],row['fixtures'],row['registered_dining_places'],row['closet_instances']),(2,18,4,1))
   self.assertEqual(row['clothing_volume'],'NOT_VERIFIED')
  bad=copy.deepcopy(model);bad['units'][1]['fixtures']['bed1.bed'][2]='999'
  with self.assertRaisesRegex(ValueError,'^P14_SOURCE_INSTANCE_BINDING$'):p.inventory(bad,profile,cat)
  self.assertEqual(digest(model),pins)
 def bundle(self):
  p=self.p;req=p.prepare(self.BODY);m=self.p1_model();pr=proposal();pr.update(status='PROPOSAL_ONLY')
  from constructor127 import frame
  mh=digest(m);hashes={u:digest(pr) for u in ('A','B')};core,_=frame(req['raw'],'FRONT_REAR')
  t={'raw':req['raw'],'model_hash':mh,'local_model_hash':mh,'core_hash':digest(core),'unit_proposal_hashes':hashes,
      'family':'FRONT_REAR','source_revision':p.ENGINE_REVISION,'proposals':{'A':pr,'B':pr}}
  c={'construction_trace':t,'operation':'generate_from_dimensions','baseline_model_hash':None,'existing_plan_id':None,'inputs':m['inputs']}
  re={'verified':True,'model_hash':mh,'source_revision':p.ENGINE_REVISION,'trace_hash':digest(t),'errors':[],'pending':[]}
  ph={'model_hash':mh,'status':'FAIL','errors':[{'code':'SYNTHETIC_RETAINED_PHYSICAL_ERROR'}],'pending':['SYNTHETIC_PENDING'],
      'accepted':False,'release':False,'multiproposal_provenance127':re}
  rs={'replay':re,'physical':ph}
  return {'schema':'P14_P1_N2_ORIGINAL_RUNTIME_BUNDLE_V1','request':req,'request_body_hex':self.BODY.hex(),'model_digest':mh,
      'packet':{'family':'FRONT_REAR','local_model':m,'world_model':m,'core':core,'admission_claim':False,'unit_proposal_hashes':hashes},
      'proposal':pr,'context':c,'engine_revision':p.ENGINE_REVISION,'reports':rs,'report_digests':{k:digest(v)for k,v in rs.items()},
      'source_snapshot':p.snapshot(p.ROOT,sorted(p.PATHS)),**p.ALWAYS_FALSE}
 def test_readback_negative_p1_request_report_and_assignment(self):
  p=self.p;b=self.bundle();p.binding(b)
  for name in ('raw-bytes','typed-count','cross-program','report','proposal','source','core'):
   with self.subTest(name=name),self.assertRaises(ValueError):
    t=copy.deepcopy(b)
    if name=='raw-bytes':t['request_body_hex']=b'{ "W":"18","L":"20","n":2 }'.hex()
    if name=='typed-count':t['request']['raw']['n']=2.0
    if name=='cross-program':t['packet']['world_model']['program']['bedrooms_per_unit']=2
    if name=='report':
     t['reports']['physical']['multiproposal_provenance127']={'verified':True};t['report_digests']['physical']=digest(t['reports']['physical'])
    if name=='proposal':t['context']['construction_trace']['proposals']['B']=dict(proposal(),sleep_roles=['twin'])
    if name=='source':del t['source_snapshot']['app/local_integration/one_bed_pair_p14.py']
    if name=='core':
     t['packet']['core']={'kind':'REHASHED_FAKE_CORE'}
     trace=t['context']['construction_trace'];trace['core_hash']=digest(t['packet']['core'])
     t['reports']['replay']['trace_hash']=digest(trace)
     t['report_digests']={k:digest(v)for k,v in t['reports'].items()}
    p.binding(t)
 def test_decision_witnesses_reuse_exact_scoped_verdict_no_pass_promotion(self):
  p=self.p;b=self.bundle();mh=b['model_digest'];ph=b['reports']['physical'];re=b['reports']['replay']
  rows={}
  for key,schema in p.four.SCHEMAS.items():
   row={'schema':schema,'criterion':key,'model_digest':mh,'current_domain_policy':'CURRENT_ENTRY_DOMAIN_X03_V1',
        'integrity_verified':True,'state':'UNKNOWN',**p.ALWAYS_FALSE}
   if key==p.CID:
    cap={'errors':[],'evidence':{'model_hash':mh,'units':[{'unit':uid,'residents_study':2,'actual_places':{'sleeping_places':2}} for uid in ('A','B')]}};rr={'replay':re,'capacity':cap}
    row.update(schema=p.P1_SCHEMA,programme_id=p.PROGRAMME,profile_digest=b['request']['programme_digest'],
       historical_physical_report=ph,historical_physical_digest=digest(ph),reports=rr,report_digests={k:digest(v)for k,v in rr.items()},
       source_snapshot=p.snapshot(p.ROOT,sorted(p.SOURCES[key])))
   else:
    row.update(replay=re,original_physical_report=ph,original_physical_digest=digest(ph),
        source_snapshot=p.snapshot(p.ROOT,sorted(p.four.REQUIRED_SOURCES[key])))
    if key=='CONTINUOUS_USEFUL_LIVING':row['state']='NOT_EVALUATED'
    if key=='NONFUNCTIONAL_WALL_EXCLUSION':row['missing']=['SYNTHETIC_EVALUATOR_ERROR']
   rows[key]=row
  before=digest(b);bind=lambda rr:{k:digest(v)for k,v in rr.items()}
  res=p.decision(b,rows,bind(rows));self.assertEqual(res['decision']['state'],'BLOCKED')
  self.assertEqual([x['effective_state']for x in res['criteria']],['NOT_EVALUATED','UNKNOWN','UNKNOWN','EVALUATOR_ERROR'])
  self.assertTrue({'PHYSICAL_FAIL','CURRENT_UNKNOWN','CURRENT_NOT_EVALUATED','EVALUATOR_ERROR'}<=set(res['decision']['blockers']))
  bad=copy.deepcopy(rows);bad[p.CID]['state']='PASS'
  with self.assertRaisesRegex(ValueError,'^P14_CAPACITY_STATE_BINDING$'):p.decision(b,bad,bind(bad))
  bad=copy.deepcopy(rows);bad[p.CID]['historical_physical_report']['errors']=[]
  with self.assertRaisesRegex(ValueError,'^P14_ASSESSMENT_PHYSICAL$'):p.decision(b,bad,bind(bad))
  self.assertEqual(digest(b),before)
 def test_actual_source_front_end_single_controlled_zero_witness(self):
  from types import SimpleNamespace
  from unittest.mock import patch
  import tempfile,search114
  p=self.p
  with tempfile.TemporaryDirectory() as td,patch.object(search114,'milp',return_value=SimpleNamespace(x=None,status=1,message='CONTROLLED_NO_WITNESS'))as f:
   root=pathlib.Path(td);r=p.run(self.BODY,root)
   self.assertEqual(r['state'],'NO_WITNESS_WITHIN_SINGLE_ATTEMPT',r);f.assert_called_once()
   self.assertEqual({x.name for x in root.iterdir()},{'request.json','attempt-open.json','proposal-observed.json','evidence-index.json'})
 def test_private_file_is_exclusive_and_narrow(self):
  import tempfile
  with tempfile.TemporaryDirectory()as t:
   p=pathlib.Path(t)
   self.p.retain_private(p,'fixture.json',{'only':'synthetic'})
   self.assertEqual((p/'fixture.json').stat().st_mode&0o777,0o600)
   with self.assertRaises(FileExistsError):self.p.retain_private(p,'fixture.json',{})
   with self.assertRaisesRegex(ValueError,'^P14_LOCAL_FILENAME$'):self.p.retain_private(p,'../outside.json',{})
if __name__=='__main__':unittest.main()
