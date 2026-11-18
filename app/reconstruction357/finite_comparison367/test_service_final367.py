import json,copy,unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
import service_runner367 as runner
from service_criterion367_v3 import reduce_bound
ROOT=runner.ROOT
R=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());V=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text())
C=json.loads((ROOT/'finite_comparison367/cost_ledger_actual367.json').read_text());Q=json.loads((ROOT/'finite_comparison367/q04_actual367_v3.json').read_text());P=json.loads((ROOT/'semantic_rules357/service_role_inventory_joint_actual367.json').read_text());A=json.loads((ROOT/'finite_comparison367/service_actual367_v3.json').read_text())
class Tests(unittest.TestCase):
 def test_bound_reducer_actual_evidence(self):
  x=reduce_bound(R,V,C,Q,P);self.assertEqual(x['verdict'],'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS');self.assertEqual(x['remaining'],[]);self.assertTrue(all(u['scoped_exclusive_metric']['global_exclusive_function_m2']is None for u in x['units']))
 def test_partition_unknown(self):
  p=copy.deepcopy(P);p['verdict']='UNKNOWN';p['remaining']=['missingoperation'];self.assertEqual(reduce_bound(R,V,C,Q,p)['verdict'],'UNKNOWN')
 def test_unclassified_blocks(self):
  p=copy.deepcopy(P);p['units'][0]['unclassified_m2']='1/100'
  with self.assertRaises(ValueError):reduce_bound(R,V,C,Q,p)
 def test_wrong_partition_model(self):
  p=copy.deepcopy(P);p['model_digest']='bad'
  with self.assertRaises(ValueError):reduce_bound(R,V,C,Q,p)
 def test_no_necessity_promotion(self):
  q=copy.deepcopy(Q);q['remaining']=['domain'];q['verdict']='UNKNOWN';self.assertEqual(reduce_bound(R,V,C,q,P)['verdict'],'UNKNOWN')
 def test_global_exclusive_claim_rejected(self):
  p=copy.deepcopy(P);p['global_exclusive_function_m2']='0'
  with self.assertRaises(ValueError):reduce_bound(R,V,C,Q,p)
 def test_caller_fresh_false_receipt(self):
  v=copy.deepcopy(V);v['accepted']=True
  with patch.object(runner.subprocess,'run',return_value=SimpleNamespace(stdout=json.dumps(A))):
   with self.assertRaises(ValueError):runner.evaluate(R,v)
 def test_partition_unit_mismatch(self):
  p=copy.deepcopy(P);p['units'][0]['unit']='C'
  with self.assertRaises(ValueError):reduce_bound(R,V,C,Q,p)
 def test_partition_fresh_mismatch(self):
  p=copy.deepcopy(P);p['fresh_result_digest']='other'
  with self.assertRaises(ValueError):reduce_bound(R,V,C,Q,p)
 def test_manifest_tamper_preimport(self):
  with patch.object(runner,'MANIFEST_SHA','bad'),patch.object(runner.subprocess,'run')as child:
   with self.assertRaises(ValueError):runner.evaluate(R,V)
   child.assert_not_called()
if __name__=='__main__':unittest.main()
