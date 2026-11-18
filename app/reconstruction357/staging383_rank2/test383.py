"""Pure preaudit. Mocked assembly/replay tests are NOT actual fresh evidence."""
import unittest,copy,json,sys,uuid,importlib.util
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parent/'staging378_finite_portals'))
import family378 as f
import source383 as s
from core378 import core
from fractions import Fraction as F
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.parent=f.load_parent();cls.choices=f.enumerate_family(cls.parent)
 def test_three_interior_ranks(self):
  cs=self.choices;lo,hi=map(F,cs[0]['selected_interval']);self.assertEqual([p['finite_rank378']for p in cs],[0,1,2]);self.assertEqual(F(cs[0]['entry_x']['A']),(lo+hi)/2)
  self.assertEqual(F(cs[1]['entry_x']['A']),lo+(hi-lo)/4);self.assertTrue(all(lo<F(p['entry_x']['A'])<hi for p in cs))
 def test_input_types_and_scope(self):
  raw=self.parent['candidate']['request']
  for k,v in [('W',26.0),('n',True),('requested_count',1),('L','29'),('proof',{})]:
   r=copy.deepcopy(raw);r[k]=v
   with self.assertRaises(ValueError):f.validate_request(r)
 def test_geometry_not_cached(self):
  r=copy.deepcopy(self.parent);r['candidate']['model']['walls']['A.bath.A.service_right'][2]='13.1'
  self.assertNotEqual(f.enumerate_family(r)[1]['entry_x'],self.choices[1]['entry_x'])
 def test_empty_domain(self):
  r=copy.deepcopy(self.parent);r['candidate']['model']['walls']['testblocking']=['13.1','12.35','14','12.46']
  with self.assertRaises(ValueError):f.enumerate_family(r)
 def test_core_tamper_rank_domain_parameter(self):
  for key,value in [('finite_rank378',99),('selected_interval',['0','99']),('entry_x',{'A':'0','B':'0'})]:
   c=copy.deepcopy(self.choices[1]);c[key]=value
   with self.assertRaises(ValueError):core(F(26),F(28),c)
 def test_core_protected(self):
  c=core(F(26),F(28),self.choices[1]);old=self.parent['candidate']['packet']['core']
  for k in ('stair','lift','lobby','unit_ownership','units','notch362'):self.assertEqual(c[k],old[k])
 def fake_record(self):
  packet=copy.deepcopy(self.parent['candidate']['packet']);rid='37800000-0000-4000-8000-000000000001'
  with patch.object(s,'inventory',return_value={'pure':'mock'}),patch.object(s,'build',return_value=packet),patch.object(s,'enumerate_family',return_value=self.choices):
   return s.construct(self.parent['candidate']['request'],rid)
 def test_rank2_source_registration(self):
  r=self.fake_record();self.assertEqual(r['trace']['selection_rank'],2)
  self.assertEqual(r['candidate']['generation_context']['selection'],self.choices[2])
  self.assertEqual(r['trace']['schema'],'FINITE_PORTALS383_SOURCE_TRACE_V1')
  self.assertNotEqual(r['candidate']['generation_context']['selection'],self.choices[1])
  c=core(F(26),F(28),self.choices[2]);self.assertEqual(c['entry_centers']['A'][0],self.choices[2]['entry_x']['A']);self.assertEqual(c['balanced_portals365']['finite_rank378'],2)
 def test_replay_exact_and_tamper(self):
  r=self.fake_record();packet=copy.deepcopy(self.parent['candidate']['packet'])
  with patch.object(s,'inventory',return_value={'pure':'mock'}),patch.object(s,'build',return_value=packet),patch.object(s,'enumerate_family',return_value=self.choices):
   self.assertEqual(s.replay(r),r)
   for area,key,value in [('trace','selection_rank',0),('trace','enumeration',[]),('candidate','model_digest','tampered'),('trace','run_id','invalid')]:
    bad=copy.deepcopy(r);bad[area][key]=value
    with self.assertRaises(ValueError):s.replay(bad)
 def test_self_consistent_forged_rank_still_rejected(self):
  r=self.fake_record();r['trace']['selection_rank']=0;r['candidate']['generation_context']['selection']=self.choices[0]
  r['trace']['candidate_digest']=s.digest(r['candidate'])
  r['candidate_id']=s.digest({'run_id':r['trace']['run_id'],'request_digest':s.digest(r['candidate']['request']),'model_digest':s.digest(r['candidate']['model']),'trace_digest':s.digest(r['trace'])})
  with patch.object(s,'inventory',return_value={'pure':'mock'}),patch.object(s,'build',return_value=self.parent['candidate']['packet']),patch.object(s,'enumerate_family',return_value=self.choices):
   with self.assertRaises(ValueError):s.replay(r)
 def test_identity_and_inventory_tamper(self):
  r=self.fake_record()
  with patch.object(s,'inventory',return_value={'pure':'other'}):
   with self.assertRaises(ValueError):s.replay(r)
  r['candidate_id']='forged'
  with patch.object(s,'inventory',return_value={'pure':'mock'}),patch.object(s,'build',return_value=self.parent['candidate']['packet']),patch.object(s,'enumerate_family',return_value=self.choices):
   with self.assertRaises(ValueError):s.replay(r)
 def test_dispatch_does_not_generalize_repair(self):
  import evaluate383 as e
  r=self.fake_record();c=r['candidate'];t=r['trace']
  proof={'verified':True,'schema':s.SCHEMA,'input_record_digest':s.digest(r),'outer_trace_digest':s.digest(t),'candidate_digest':s.digest(c),'model_hash':s.digest(c['model']),'packet_digest':s.digest(c['packet']),'raw':c['request'],'run_id':t['run_id'],'candidate_id':r['candidate_id'],'parent_record_digest':t['parent_record_digest']}
  fresh={'schema':'FINITE383_CURRENT_SOURCE_VALIDATION','review_id':'37800000-0000-4000-8000-000000000002','input_record_digest':s.digest(r),'outer_trace_digest':s.digest(t),'model_digest':s.digest(c['model']),'fresh_checker_executed':True,'source_unchanged':True,'prior_quality_certificates_reused':False,'provenance':proof,'expected_method_registry':{'pure':'mock'},'raw_report':{'model_hash':s.digest(c['model']),'errors':[{'code':'ROUTE_FAILED'}],'pending':[]}}
  with patch.object(e,'registry_for',return_value={'pure':'mock'}):
   self.assertEqual(s.repair_dispatch(r,fresh)['reason'],'UNSUPPORTED_REPAIR_REASON')
   for field in ('run_id','candidate_id','model_hash'):
    bad=copy.deepcopy(fresh);bad['provenance'][field]='forged'
    with self.assertRaises(ValueError):s.repair_dispatch(r,bad)
   bad=copy.deepcopy(fresh);bad['expected_method_registry']={}
   with self.assertRaises(ValueError):s.repair_dispatch(r,bad)
   bad=copy.deepcopy(fresh);bad['raw_report']['model_hash']='forged'
   with self.assertRaises(ValueError):s.repair_dispatch(r,bad)
   fresh['raw_report'].update(errors=[],pending=['UNPROVEN'])
   self.assertEqual(s.repair_dispatch(r,fresh)['reason'],'UNKNOWN_PENDING_REVIEW')
   fresh['raw_report'].update(pending=[],status='UNKNOWN')
   self.assertEqual(s.repair_dispatch(r,fresh)['reason'],'UNKNOWN_REVIEW_STATUS')
 def test_protected_assets(self):
  prior=self.parent['candidate']['model'];s.require_protected(self.parent,prior)
  for k in ('stair','lift'):
   bad=copy.deepcopy(prior);bad['common_spaces'][k]=[]
   with self.assertRaises(ValueError):s.require_protected(self.parent,bad)
  for k in ('fixtures','activities','ownership'):
   bad=copy.deepcopy(prior);bad['units'][0][k]={}
   with self.assertRaises(ValueError):s.require_protected(self.parent,bad)
  bad=copy.deepcopy(prior);key=next(k for k in bad['units'][0]['rooms']if k.startswith('bed'));bad['units'][0]['rooms'][key]=[]
  with self.assertRaises(ValueError):s.require_protected(self.parent,bad)
 def test_no_prior_fixture_dependency(self):
  for n in ('source383.py',):
   text=(HERE/n).read_text()
   for marker in ('review369','review371','review372','CONTROLLED_TEST_FIXTURE','operator372'):self.assertNotIn(marker,text)
 def test_current_module_origins(self):
  import evaluate383 as e
  rows=e.module_origin_audit();self.assertEqual(sum(r['relation']=='CURRENT383_RUNTIME'for r in rows),6)
  import types
  fake=types.SimpleNamespace(__file__=str(HERE.parent/'planha_general150_runtime_work/named_checks118.py'))
  with patch.dict(sys.modules,{'named_checks118':fake}):
   with self.assertRaises(ValueError):e.module_origin_audit()
 def test_notch_keeps_geometry_checks(self):
  spec=importlib.util.spec_from_file_location('notch378_test',HERE/'runtime/notch_grammar365.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  m=json.loads((HERE.parent/'staging365_balanced_portals/actual365.json').read_text())['candidate']['model'];c=core(F(26),F(28),self.choices[1])
  self.assertEqual(mod.allowed_walls(m,c),{'core.notch362.A_separator'})
  for key in ('finite_rank378','portal_y'):
   bad=copy.deepcopy(c);bad['balanced_portals365'][key]=99 if key=='finite_rank378'else{'stair':'0','lift':'0'}
   with self.assertRaises(ValueError):mod.allowed_walls(m,bad)
  bad=copy.deepcopy(m);bad['walls']['core.notch362.A_separator']=['0','0','1','1']
  with self.assertRaises(ValueError):mod.allowed_walls(bad,c)
class HarnessTests(unittest.TestCase):
 def test_cleanup_failclosed(self):
  from guard383 import clean
  good={'reason':'COMPLETED','worker_returncode':0,'cleanup_verified':True,'worker_reaped':True,'unresolved':[]}
  self.assertTrue(clean(good))
  for k,v in [('reason','TIMEOUT'),('worker_returncode',1),('cleanup_verified',False),('worker_reaped',False),('unresolved',[123])]:
   self.assertFalse(clean(dict(good,**{k:v})))
  self.assertFalse(clean({}))
 def test_launch_missing_cycle_or_failure_never_success(self):
  from guard383 import launch_complete
  good={'reason':'COMPLETED','worker_returncode':0,'cleanup_verified':True,'worker_reaped':True,'unresolved':[]}
  for c in (None,{}, {'status':'INTEGRATION_STOPPED_NOT_A_CANDIDATE_VERDICT'}):self.assertFalse(launch_complete(good,{'verified':True},c))
  self.assertTrue(launch_complete(good,{'verified':True},{'status':'UNKNOWN_PENDING_REVIEW'}))
  self.assertFalse(launch_complete(good,{'verified':False},{'status':'UNKNOWN_PENDING_REVIEW'}))
 def cycle_mock(self,receipt):
  import tempfile,runpy,types
  import guard383
  with tempfile.TemporaryDirectory()as temp:
   p=Path(temp);(p/'dispatch.json').write_text(json.dumps({'reason':'UNKNOWN_PENDING_REVIEW','errors':[],'pending':['UNPROVEN']}))
   calls=[]
   def supervise(*args,**kwargs):calls.append(args);return copy.deepcopy(receipt)
   with patch.object(guard383,'guard',return_value=1),patch.dict(sys.modules,{'supervisor':types.SimpleNamespace(supervise=supervise)}),patch.object(sys,'argv',['cycle383.py',temp,'pure_mock_freeze']):
    try:runpy.run_path(str(HERE/'cycle383.py'),run_name='__main__')
    except SystemExit:pass
   return json.loads((p/'cycle_result.json').read_text()),calls
 def test_mock_cycle_retains_unknown(self):
  r,calls=self.cycle_mock({'reason':'COMPLETED','worker_returncode':0,'cleanup_verified':True,'worker_reaped':True,'unresolved':[]})
  self.assertEqual(r['status'],'UNKNOWN_PENDING_REVIEW');self.assertEqual(len(calls),3);self.assertFalse(r['accepted']);self.assertFalse(r['browser_executed'])
 def test_mock_cycle_stops_first_bad_cleanup(self):
  r,calls=self.cycle_mock({'reason':'COMPLETED','worker_returncode':0,'cleanup_verified':False,'worker_reaped':True,'unresolved':[123]})
  self.assertEqual(len(calls),1);self.assertEqual(r['status'],'INTEGRATION_STOPPED_NOT_A_CANDIDATE_VERDICT')
 def test_harness_caps_no_direct_kill(self):
  import ast
  for name in ('launch383.py','cycle383.py','worker383.py'):
   tree=ast.parse((HERE/name).read_text())
   self.assertFalse(any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in('kill','terminate')for n in ast.walk(tree)))
  self.assertIn("[('construct',45),('fresh',90),('audit',5)]",(HERE/'cycle383.py').read_text())
  self.assertIn('P.mkdir(exist_ok=False)',(HERE/'launch383.py').read_text())
if __name__=='__main__':unittest.main()
