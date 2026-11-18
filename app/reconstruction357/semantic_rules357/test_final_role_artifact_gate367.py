import json,copy,unittest
from pathlib import Path
import final_role_artifact_gate367 as g
R=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((R/'review367_joint_attempt2/actual367.json').read_text());cls.f=json.loads((R/'review367_joint_source_validation_attempt2/result.json').read_text());cls.o=g.evaluate(cls.r,cls.f);cls.s,cls.d=g._load_seal_and_dag()
 def test_own(self):self.assertEqual(self.o['parent_evidence']['DISTINCTNESS_AND_FAIRNESS']['verdict'],'UNKNOWN')
 def mutation(self,fn):
  o=copy.deepcopy(self.o);fn(o)
  with self.assertRaises((ValueError,KeyError)):g._validate(o,self.r,self.f,self.s,self.d)
 def test_partial(self):self.mutation(lambda o:o['parent_evidence'].pop('SERVICE_COMPACTNESS'))
 def test_stale(self):self.mutation(lambda o:o.update(review_digest='stale'))
 def test_node(self):self.mutation(lambda o:o['nodes']['Q12_PER_UNIT'].update(status='UNKNOWN'))
 def test_receipt(self):self.mutation(lambda o:o['service_compactness_evidence']['invocation_receipts']['cost'].update(model_digest='fake'))
 def test_q12(self):self.mutation(lambda o:o['internal_per_unit_review']['units'][0].update(exact_pending=['missing']))
 def test_foreign(self):
  r=copy.deepcopy(self.r);r['candidate']['request']['W']='25'
  with self.assertRaises(ValueError):g.evaluate(r,self.f)
if __name__=='__main__':unittest.main()
