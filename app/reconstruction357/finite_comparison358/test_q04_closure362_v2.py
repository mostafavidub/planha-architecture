import unittest,copy,json
from pathlib import Path
from unittest.mock import patch
import q04_closure362_v2 as q
import run_q04_362_v2 as runner
R=json.loads((q.ROOT/'staging362_core_notch/actual362.json').read_text())
class Tests(unittest.TestCase):
 def test_current_fullband(self):
  out=q.full_band_current(R);self.assertEqual(out['rows'][0]['loss_exact_m2'],'621/25');self.assertTrue(out['pure_primitive_reexecuted'])
 def test_wrong_raw_rejected(self):
  r=copy.deepcopy(R);r['trace']['raw']['W']='25'
  with self.assertRaises(ValueError):q.full_band_current(r)
 def test_missing_counterexample_rejected(self):
  r=copy.deepcopy(R);r['candidate']['model']['units'][0]['ownership']=[['0','0','1','1']]
  with self.assertRaises(ValueError):q.full_band_current(r)
 def test_bad_parent_rejected(self):
  r=copy.deepcopy(R);r['trace']['parent_record_digest']='bad'
  with self.assertRaises(ValueError):q.bind_cohort(r)
 def test_cohort(self):self.assertEqual(len(q.bind_cohort(R)),4)
 def test_manifest_tamper(self):
  with self.assertRaises(ValueError):runner.verify('bad')
if __name__=='__main__':unittest.main()
