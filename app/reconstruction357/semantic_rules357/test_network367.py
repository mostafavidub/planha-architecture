import unittest,json,copy
from pathlib import Path
from group_readsets367 import build
from network367 import evaluate
B=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  c=json.loads((B/'review367_joint_attempt2/actual367.json').read_text());r=json.loads((B/'review367_joint_source_validation_attempt2/result.json').read_text());v=build(c,r);cls.e=v['envelope'];cls.r=v['result'];cls.p=v['groups']['rows'][:8]
 def test_cross_record_and_raw(self):
  c=json.loads((B/'review367_joint_attempt2/actual367.json').read_text());r=json.loads((B/'review367_joint_source_validation_attempt2/result.json').read_text())
  for target in ('request','trace','packet','raw'):
   cc=copy.deepcopy(c);rr=copy.deepcopy(r)
   if target=='request':cc['candidate']['request']['W']='25'
   elif target=='trace':cc['trace']['schema']='SOURCE_SERVICE_ANCHOR365_TRACE_V1'
   elif target=='packet':cc['candidate']['packet']['core']['entry_centers']['A'][0]='14'
   else:rr['raw_report']['model_hash']='fake'
   with self.assertRaises(ValueError):build(cc,rr)
  other=json.loads((B/'review365_service_source_validation/result.json').read_text())
  with self.assertRaises(ValueError):build(c,other)
 def test_actual_network(self):
  x=evaluate(self.e,self.r,self.p,2);self.assertEqual(x['verdict'],'SCOPED_PASS',x);self.assertEqual(len(x['rows']),2);self.assertFalse(x['new_fresh_execution'])
 def test_wrong_root(self):
  e=copy.deepcopy(self.e);e['packet']['core']['entry_centers']['B'][0]=e['packet']['core']['entry_centers']['A'][0];self.assertEqual(evaluate(e,self.r,self.p,2)['verdict'],'UNKNOWN')
 def test_wrong_direction(self):
  e=copy.deepcopy(self.e);e['packet']['core']['service_balanced367']['slide_direction']['A']=1;self.assertEqual(evaluate(e,self.r,self.p,2)['verdict'],'UNKNOWN')
 def test_missing_operation_field(self):
  e=copy.deepcopy(self.e);e['packet']['world_model']['operations']['doors'][0].pop('mount');self.assertEqual(evaluate(e,self.r,self.p,2)['verdict'],'UNKNOWN')
 def test_fabricated_prerequisite(self):
  p=copy.deepcopy(self.p);p[0]['verdict']='FAIL';self.assertEqual(evaluate(self.e,self.r,p,2)['verdict'],'UNKNOWN')
 def test_profile(self):
  e=copy.deepcopy(self.e);e['schema']='REGISTERED_SOURCE358_VIEW';self.assertEqual(evaluate(e,self.r,self.p,2)['verdict'],'UNKNOWN')
 def test_living_own_source_no_old_network_call(self):
  import types,builtins
  from unittest.mock import patch
  p=B/'semantic_rules357';cm=types.ModuleType('_common367');cm.__file__=str(p/'common.py');exec(compile((p/'common.py').read_bytes(),cm.__file__,'exec'),cm.__dict__);cm.REGISTRY_NAME='method_registry_source367.json'
  lm=types.ModuleType('_living367');lm.__file__=str(p/'living_closure367.py')
  def imp(name,*args,**kwargs):return cm if name=='common'else builtins.__import__(name,*args,**kwargs)
  lm.__dict__['__builtins__']={**vars(builtins),'__import__':imp};exec(compile((p/'living_closure367.py').read_bytes(),lm.__file__,'exec'),lm.__dict__)
  from common import digest
  g={'model_hash':digest(self.e['packet']['world_model']),'fresh_result_digest':digest(self.r),'rows':self.p}
  x=lm.evaluate(self.e,self.r,g,6);self.assertEqual(x['verdict'],'PASS_SCOPED_INTRINSIC_LIVING',x);self.assertFalse(x['parent_complete'])
if __name__=='__main__':unittest.main()
