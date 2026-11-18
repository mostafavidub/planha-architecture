"""Active entrypoint checks only; frozen historical CLI is not range25-compliant."""
import json,subprocess,sys,unittest
from pathlib import Path
from dimension_contract import InputError
from repair_saved_worker import validated_source_raw
class EntryTests(unittest.TestCase):
 def body(self,**kw):
  raw={'W':'25','L':'25','n':2,'requested_count':1};raw.update(kw);return json.dumps(raw).encode()
 def candidate(self,**kw):
  raw={'W':'25','L':'25','n':2,'requested_count':1};raw.update(kw)
  return {'generation_context':{'construction_trace':{'raw':raw}}}
 def test_real_generation_cli_rejects_before_engine(self):
  for axis in ['W','L']:
   for value in ['25.000000000000000001','26','45','4.999']:
    with self.subTest(axis=axis,value=value):
     p=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('parametric_worker.py'))],input=self.body(**{axis:value}),capture_output=True,timeout=10)
     self.assertEqual(p.returncode,0,p.stderr.decode())
     r=json.loads(p.stdout);self.assertEqual(r['outcome'],'INVALID_INPUT');self.assertEqual(r['code'],'DIMENSION_OUT_OF_OWNER_RANGE');self.assertFalse(r['accepted']);self.assertFalse(r['delivery_allowed'])
 def test_saved_repair_out_of_range_cannot_reach_trace(self):
  for axis in ['W','L']:
   for value in ['25.000000000000000001','45','4.99']:
    with self.assertRaisesRegex(InputError,'DIMENSION_OUT_OF_OWNER_RANGE'):
     validated_source_raw(self.body(**{axis:value}),{})
 def test_saved_repair_trace_cannot_substitute_historical_dimensions(self):
  for axis in ['W','L']:
   with self.assertRaisesRegex(ValueError,'SAVED_TRACE_REQUEST_BINDING_MISMATCH'):
    validated_source_raw(self.body(),self.candidate(**{axis:'28'}))
 def test_saved_repair_exact_valid_binding(self):
  for v in ['5','25','24.000000000000000001']:
   raw=validated_source_raw(self.body(W=v),self.candidate(W=v));self.assertEqual(raw['W'],v)
if __name__=='__main__':unittest.main()
