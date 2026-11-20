"""P17 source derivation/binding tests; no synthetic fixture is a physical PASS."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import single_model_p15 as p
import single_evaluation_p17 as e
class Binding(unittest.TestCase):
 def setUp(self):
  self.model={'schema':p.FAMILY,'contract_version':'p15-single-v1','inputs':['18','20',1],'units':[{'id':'A'}],**{k:False for k in p.AUTH}}
  self.context=e.context(p.RAW,{'not_a_real_proposal':True})
 def test_current_source_audit(self):self.assertIn('single_runtime_p17.py',e.source_audit()['p17'])
 def test_context_mutations_pre_replay(self):
  for change in [lambda c:c['raw'].update(n=2),lambda c:c['core']['stair'].__setitem__(0,'.5'),lambda c:c.update(schema='OLD_CONTEXT')]:
   ctx=copy.deepcopy(self.context);change(ctx)
   with self.assertRaises(ValueError):e.verify(self.model,ctx)
 def test_typed_model_before_replay(self):
  for value in (True,1.0,2):
   m=copy.deepcopy(self.model);m['inputs'][2]=value
   with self.assertRaisesRegex(ValueError,'P17_MODEL_INPUT_TYPED'):e.verify(m,self.context)
 def test_pair_model_rejected(self):
  self.model['units'].append({'id':'B'})
  with self.assertRaises(ValueError):e.verify(self.model,self.context)
 def test_old_bundle_rejected(self):
  with self.assertRaisesRegex(ValueError,'P17_BUNDLE_SCHEMA'):e.bind_bundle({'schema':'OLD_PAIR_BUNDLE'})
 def test_numeric_digest_exact(self):
  self.assertNotEqual(p.digest(1),p.digest(1.0));self.assertNotEqual(p.digest(1),p.digest(True))
 def test_exact_four_derivatives(self):
  specs=json.loads((ROOT/'studies/p17_evaluator_derivatives.json').read_text())
  self.assertEqual(len(specs),4)
  for path,spec in specs.items():
   data=(ROOT/spec['source']).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest(),spec['source_blob'])
   code=data.decode().replace('\nAUTH=','\nfrom single_evaluation_p17 import source_audit\nAUTH=')
   for old,new in spec['edits']:
    self.assertIn(old,code);code=code.replace(old,new)
   code=code.replace("'schema':'"+spec['schema_from']+"'","'schema':'"+spec['schema_to']+"'")
   if spec['inventory_from_p15']:
    a=code.index('def inventory(');b=code.index('def proven_capacity_violation')
    code=code[:a]+'from single_access_p15 import inventory\n'+code[b:]
   tail=" return out\n"
   self.assertTrue(code.endswith(tail))
   code=code[:-len(tail)]+" out['retained_historical_physical_report']=copy.deepcopy(bundle['reports']['historical_physical'])\n out['retained_historical_physical_digest']=bundle['report_digests']['historical_physical']\n return out\n"
   self.assertEqual((ROOT/path).read_text(),code,path)
if __name__=='__main__':unittest.main(verbosity=2)
