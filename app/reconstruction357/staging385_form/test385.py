"""Pure existing-evidence binding/mocked lifecycle tests; no live model review."""
import ast,copy,json,sys,unittest,tempfile,threading,uuid
from pathlib import Path
from unittest.mock import Mock,patch
from contract385 import *
class Parser(unittest.TestCase):
 def test_fourfields(self):self.assertEqual(parse_json('{"W":"۲۶","L":"۲۸","n":"۲","requested_count":"۲"}')['normalized_raw'],{'W':'26','L':'28','n':2,'requested_count':2})
 def test_injections(self):
  for k in('model','proof','review','fixture'):
   with self.assertRaises(ValueError):parse_json(json.dumps({'W':26,'L':28,'n':2,'requested_count':2,k:{}}))
 def test_badfields(self):
  for body in ('{"W":26,"W":26,"L":28,"n":2,"requested_count":2}','{"W":26.0,"L":28,"n":2,"requested_count":2}','{"W":27,"L":28,"n":2,"requested_count":2}'):
   with self.assertRaises(ValueError):parse_json(body)
class Bindings(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.env=parse_json('{"W":"۲۶","L":"۲۸","n":"۲","requested_count":"۲"}')
  p=W/'independent378actual/evidence/review378_actual_v1';cls.br=json.loads((p/'record.json').read_text());cls.bf=json.loads((p/'fresh.json').read_text());cls.rid=cls.br['trace']['run_id']
  cls.jr=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());cls.jf=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text())
 def test_both_bind_same_run_program(self):
  a=bind_member(self.env,self.br,self.bf,self.rid,'balanced',self.bf['review_id']);b=bind_member(self.env,self.jr,self.jf,self.rid,'joint','38500000-0000-4000-8000-000000000001')
  for k in('run_id','raw_digest','program_digest','profile_digest','input_digest'):self.assertEqual(a[k],b[k])
  self.assertNotEqual(a['candidate_id'],b['candidate_id']);self.assertNotEqual(a['review_id'],b['review_id'])
 def test_joint_raw_and_registry_tamper(self):
  for target in('model','registry','raw'):
   f=copy.deepcopy(self.jf)
   if target=='model':f['model_digest']='forged'
   if target=='registry':f['expected_method_registry']['methods']={}
   if target=='raw':f['provenance']['raw']['W']='27'
   with self.assertRaises(ValueError):bind_member(self.env,self.jr,f,self.rid,'joint','38500000-0000-4000-8000-000000000001')
 def test_balanced_candidate_and_run_tamper(self):
  r=copy.deepcopy(self.br);r['candidate_id']='bad'
  with self.assertRaises(ValueError):bind_member(self.env,r,self.bf,self.rid,'balanced',self.bf['review_id'])
  with self.assertRaises(ValueError):bind_member(self.env,self.br,self.bf,str(uuid.uuid4()),'balanced',self.bf['review_id'])
 def test_binding_changed(self):
  a=bind_member(self.env,self.br,self.bf,self.rid,'balanced',self.bf['review_id']);a['review_id']=str(uuid.uuid4())
  with self.assertRaises(ValueError):validate_member(self.env,self.br,self.bf,a,self.rid)
class Seal(unittest.TestCase):
 def test_no_boolean_only_qualification(self):
  tree=ast.parse((HERE/'seal385.py').read_text());ns={}
  nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='qualifies'or isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='PARENTS'for t in n.targets)]
  exec(compile(ast.Module(body=nodes,type_ignores=[]),'<PURE_QUALIFICATION_PREDICATE>','exec'),ns)
  self.assertFalse(ns['qualifies']({'qualified':True}));q={'qualified':True,'cohort_closed':True,'q12_verdict':'PASS','parent_verdicts':{k:'PASS'for k in ns['PARENTS']},'missing':[]};self.assertTrue(ns['qualifies'](q))
  q['parent_verdicts']['SPACE_ACCOUNTING']='UNKNOWN';self.assertFalse(ns['qualifies'](q))
 def test_ui_and_no_kill(self):
  html=(HERE/'index.html').read_text();self.assertEqual(html.count('<input '),4);self.assertEqual(html.count("method:'POST'"),1);self.assertIn('member.model.units',html)
  for p in HERE.glob('*.py'):ast.parse(p.read_text())
  for n in('browser385.py','server385.py'):
   tree=ast.parse((HERE/n).read_text());self.assertFalse(any(isinstance(x,ast.Call)and isinstance(x.func,ast.Attribute)and x.func.attr in('kill','terminate')for x in ast.walk(tree)))
class Owner(unittest.TestCase):
 def call(self,broken):
  node=next(n for n in ast.parse((HERE/'server385.py').read_text()).body if isinstance(n,ast.FunctionDef)and n.name=='work')
  s=Mock(side_effect=RuntimeError('MOCK'))if broken else Mock(return_value={'cleanup_verified':True,'worker_reaped':True,'unresolved':[],'reason':'COMPLETED','worker_returncode':0})
  ns={'json':json,'sys':sys,'HERE':HERE,'expected':'TEST','supervise':s,'guard':Mock(),'partial':partial,'jobs':{},'active':True,'unsafe':False,'lock':threading.Lock()};exec(compile(ast.Module(body=[node],type_ignores=[]),'<PURE_OWNER>','exec'),ns)
  with tempfile.TemporaryDirectory()as temp:
   p=Path(temp)
   if not broken:(p/'result.json').write_text(json.dumps(partial('COMPLETE','run')))
   ns['work']('run',p)
  return ns
 def test_unsafe_exception(self):
  n=self.call(True);self.assertTrue(n['unsafe']);self.assertFalse(n['active'])
 def test_clean_owner(self):
  n=self.call(False);self.assertFalse(n['unsafe']);self.assertFalse(n['active'])
if __name__=='__main__':unittest.main()
