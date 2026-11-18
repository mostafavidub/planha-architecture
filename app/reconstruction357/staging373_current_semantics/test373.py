"""Pure input/tamper/transform checks only; no semantic kernels run."""
import unittest,copy,json,ast
from gate373 import load_inputs,validate,D,HERE,ROOT
class Gate(unittest.TestCase):
 def setUp(self):self.i=load_inputs()
 def check(self):return validate(self.i['record'],self.i['fresh'],self.i['lineage'])
 def test_actual_current_gate(self):self.assertTrue(self.check()['test_only'])
 def test_model_tamper(self):
  self.i['record']['candidate']['model']['program']['units']=3
  with self.assertRaises(ValueError):self.check()
 def test_fresh_reuse_tamper(self):
  self.i['fresh']['review_id']='other'
  with self.assertRaises(ValueError):self.check()
 def test_lineage_tamper(self):
  self.i['lineage']['parent_review_id']='other'
  with self.assertRaises(ValueError):self.check()
 def test_pending_tamper(self):
  self.i['fresh']['raw_report']['pending']=['UNKNOWN']
  with self.assertRaises(ValueError):self.check()
 def test_provenance_tamper(self):
  self.i['fresh']['provenance']['verified']=False
  with self.assertRaises(ValueError):self.check()
 def test_method_registry_tamper(self):
  self.i['fresh']['expected_method_registry']['methods']={}
  with self.assertRaises(ValueError):self.check()
 def test_source_registry_tamper(self):
  from gate373 import verify_sources
  reg=copy.deepcopy(self.i['fresh']['expected_method_registry']);key=next(iter(reg['sources']['baseline368']));reg['sources']['baseline368'][key]='0'*64
  with self.assertRaisesRegex(ValueError,'CURRENT_REGISTRY_SOURCE_CHANGED'):verify_sources(reg)
 def test_kernel_transforms_import_only(self):
  for name in ('living_closure','guest_closure','kitchen_closure'):
   old=(ROOT/'semantic_rules357'/(name+'365.py')).read_text()
   expected=old.replace('from network365 import evaluate','from network373 import evaluate').replace('from living_closure365 import','from living_closure373 import').replace('from guest_closure365 import','from guest_closure373 import')
   self.assertEqual((HERE/(name+'373.py')).read_text(),expected)
 def test_all_sources_parse(self):
  for p in HERE.glob('*.py'):ast.parse(p.read_text())
if __name__=='__main__':unittest.main()
