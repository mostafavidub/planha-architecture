"""Pure mocked-authority gate tests, not same-run semantic execution evidence."""
import unittest,json,copy,sys,tempfile,types,hashlib,ast
from pathlib import Path
from unittest.mock import patch
H=Path(__file__).resolve().parent;W=H.parents[1];sys.path.insert(0,str(H))
import gate385 as g
class GateTests(unittest.TestCase):
 def setUp(self):
  old=W/'independent379actual/evidence/review379_actual_v1/runs/02dc5f92-93b6-4466-be6c-5114e96bc636'
  self.data={k:json.loads((old/(k+'.json')).read_text())for k in('record','fresh','binding','request')}
  self.tmp=tempfile.TemporaryDirectory(dir=W);self.folder=Path(self.tmp.name)/'balanced';self.folder.mkdir()
  for k,v in self.data.items():
   p=self.folder.parent/'request.json'if k=='request'else self.folder/(k+'.json');p.write_text(json.dumps(v))
  g._STATE=None
  self.contract=types.SimpleNamespace(validate_member_folder=lambda *a,**k:copy.deepcopy(self.data),validate_member=lambda env,r,f,b,rid,kind:copy.deepcopy(b))
  self.p=patch.object(g,'_contract',return_value=self.contract);self.p.start()
 def tearDown(self):self.p.stop();g._STATE=None;self.tmp.cleanup()
 def test_no_unconfigured_authority(self):
  with self.assertRaises(ValueError):g.load_inputs()
 def test_mock_current_gate_binding(self):
  b=g.configure(self.folder,'MOCK_FREEZE');self.assertEqual(b['model_digest'],self.data['fresh']['model_digest']);self.assertEqual(b['authority'],'SAME_RUN_SUPERVISED385_MEMBER')
 def test_configure_once(self):
  g.configure(self.folder,'MOCK_FREEZE')
  with self.assertRaises(ValueError):g.configure(self.folder,'MOCK_FREEZE')
 def test_input_tamper(self):
  g.configure(self.folder,'MOCK_FREEZE');r=copy.deepcopy(self.data['record']);r['candidate']['model']['inputs'][0]='27'
  with self.assertRaises(ValueError):g.validate(r,self.data['fresh'])
 def test_file_tamper_after_configuration(self):
  g.configure(self.folder,'MOCK_FREEZE');(self.folder/'fresh.json').write_text('{}')
  with self.assertRaises(ValueError):g.load_inputs()
 def test_physical_pending_rejected(self):
  self.data['fresh']['raw_report']['pending']=['UNKNOWN'];(self.folder/'fresh.json').write_text(json.dumps(self.data['fresh']))
  with self.assertRaises(ValueError):g.configure(self.folder,'MOCK_FREEZE')
 def test_parent_authority_failure_rejected(self):
  self.contract.validate_member_folder=lambda *a,**k:(_ for _ in()).throw(ValueError('RECEIPT_NOT_CLEAN'))
  with self.assertRaises(ValueError):g.configure(self.folder,'MOCK_FREEZE')
 def test_transported_snapshot_diff_rejected(self):
  (self.folder/'binding.json').write_text('{}')
  with self.assertRaises(ValueError):g.configure(self.folder,'MOCK_FREEZE')
 def test_views_bound_to_current_inputs(self):
  g.configure(self.folder,'MOCK_FREEZE');env,res,b=g.views(self.data['record'],self.data['fresh']);g.validate_views(env,res);env['packet']['world_model']['inputs'][0]='27'
  with self.assertRaises(ValueError):g.validate_views(env,res)
 def test_wrong_member_kind_folder(self):
  with self.assertRaises(ValueError):g.configure(self.folder.parent,'MOCK_FREEZE')
class SourceTests(unittest.TestCase):
 def test_no_constructor_or_checker_execution_imports(self):
  for p in H.glob('*.py'):
   if p.name.startswith('test'):continue
   for n in ast.walk(ast.parse(p.read_text())):
    if isinstance(n,ast.ImportFrom):self.assertNotIn(n.module,('source378','evaluate378','checker114','constructor378','source383','evaluate383'))
 def test_no_pinned_prior_input_loader(self):
  s=(H/'gate385.py').read_text();self.assertNotIn('inputs.json',s);self.assertIn('validate_member_folder',s)
class QualificationTests(unittest.TestCase):
 def setUp(self):
  p=W/'independent379actual/evidence/review379_actual_v1/runs/02dc5f92-93b6-4466-be6c-5114e96bc636';self.r=json.loads((p/'record.json').read_text());self.f=json.loads((p/'fresh.json').read_text());self.roles=json.loads((W/'review381_actual_v1/result.json').read_text())
 def test_stored_primitives_not_member_admission(self):
  from qualification385 import qualify
  q=qualify(self.r,self.f,self.roles,None)
  self.assertFalse(q['qualified']);self.assertEqual(q['q12_verdict'],'UNKNOWN');self.assertFalse(q['cohort_closed'])
  for k in('OPENINGS_REAL','LIVING_USEFUL_CONTIGUITY','GUEST_ROUTE_INDEPENDENCE','KITCHEN_PROXIMITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS'):self.assertEqual(q['parent_verdicts'][k],'PASS')
 def test_evidence_digest_tamper_rejected(self):
  from qualification385 import qualify
  self.roles['evidence']['exact_balance']['verdict']='PASS_FAKE'
  with self.assertRaises(ValueError):qualify(self.r,self.f,self.roles,None)
 def test_join_wrong_identity_rejected(self):
  from qualification385 import qualify
  with self.assertRaises(ValueError):qualify(self.r,self.f,self.roles,{'binding':{'record_digest':'wrong'}})
class CanonicalSealTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  # Pure composition of immutable historical evidence. No current-run claim,
  # constructor, reviewer, intrinsic engine or geometric-role rerun occurs.
  import importlib.util
  R=H.parent;sys.path[:0]=[str(R/'semantic_rules357'),str(R/'staging381_role_semantics')]
  import common;common.REGISTRY_NAME='method_registry_source365.json'
  from gate381 import load_inputs,views
  i=load_inputs();cls.r=i['record'];cls.f=i['fresh'];cls.roles=json.loads((W/'review381_actual_v1/result.json').read_text());cls.cohort=json.loads((W/'review384_actual_v1/result.json').read_text())['evidence']['cohort']
  cls.roles=copy.deepcopy(cls.roles);cls.roles['evidence']['cohort']=cls.cohort;cls.roles['evidence_bindings']['cohort']={**cls.roles['binding'],'evidence_digest':g.D(cls.cohort)}
  def direct(path,name):
   spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
  cls.direct=staticmethod(direct)
  join=direct(R/'staging386_view_binding/final_join386.py','_pure_test_join386')
  cls.raw=join.join(cls.r,cls.f,cls.roles,cls.cohort,views(cls.r,cls.f))
 def contexts(self):
  import semantic_seal385 as sealing
  return sealing,patch.object(sealing,'bytes_for',side_effect=lambda p:Path(p).read_bytes()),patch.object(sealing,'module',side_effect=self.direct)
 def test_canonical_seal_and_all_unit_sources(self):
  sealing,a,b=self.contexts()
  with a,b:
   out=sealing.seal_current(self.r,self.f,self.roles,self.raw);sealing.dependency_tools().verify(out['nodes'],sealing.expected_dag())
   node=out['nodes']['Q12_PER_UNIT'];self.assertIn('Q04_COMPARISON',node['sealed_dependency_digests'])
   for u in node['evidence']:self.assertTrue(u['source_room_roles']);self.assertEqual(set(u['capacity_use_access_source_rows']),set(sealing.CAPACITY))
 def test_complete_qualified_only_with_exact_sealed_provenance(self):
  import frozen385
  from qualification385 import qualify
  sealing,a,b=self.contexts()
  with a,b,patch.object(frozen385,'module',return_value=sealing):
   out=sealing.seal_current(self.r,self.f,self.roles,self.raw)
   q=qualify(self.r,self.f,self.roles,out);self.assertTrue(q['qualified']);self.assertEqual(set(q['parent_verdicts'].values()),{'PASS'})
   for alteration in ('dependency','unit_source','balance'):
    bad=copy.deepcopy(out)
    if alteration=='dependency':bad['nodes']['Q12_PER_UNIT']['sealed_dependency_digests'].pop('Q04_COMPARISON')
    elif alteration=='unit_source':bad['nodes']['Q12_PER_UNIT']['evidence'][0]['capacity_use_access_source_rows']={}
    else:bad['nodes']['Q12_PER_UNIT']['evidence'][0]['balanced_access_digest']='forged'
    with self.assertRaises(ValueError):qualify(self.r,self.f,self.roles,bad)
if __name__=='__main__':unittest.main()
