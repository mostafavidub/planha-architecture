"""R4-2.01 preflight/source tests only, no solver; currently NOT_RUN."""
import hashlib,json,pathlib,unittest
from live_program_scheduler import preflight
from dimension_contract import InputError
ROOT=pathlib.Path(__file__).resolve().parents[2]
class Coverage(unittest.TestCase):
 def test_expected_preflight(self):
  s=json.loads((ROOT/'specs/R4_CURRENT_TARGET_COVERAGE_V1.json').read_text())
  for row in s['expected_preflight_cases']:
   with self.subTest(case=row['id']):
    body=json.dumps(row['body']).encode()
    if not row['input_valid']:
     with self.assertRaises(InputError) as ex:preflight(body)
     self.assertEqual(ex.exception.code,row['expected'])
    else:
     got=preflight(body);self.assertEqual(got['state'],row['expected'])
     self.assertIs(got['input_valid'],True);self.assertIs(got['execution_ready'],row['execution_ready'])
     for key in ('accepted','qualified','display_allowed','delivery_allowed'):self.assertIs(got[key],False)
 def test_exact_source_and_no_readiness_inference(self):
  s=json.loads((ROOT/'specs/R4_CURRENT_TARGET_COVERAGE_V1.json').read_text())
  for f in s['source_files']:
   b=(ROOT/f['path']).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),f['blob'])
  self.assertEqual(s['status'],'SOURCE_INSPECTION_NOT_EXECUTED')
  self.assertTrue(all(x['production_supported'] is False for x in s['families']))
  self.assertTrue(all(x['public_execution_supported'] is False for x in s['programmes']))
if __name__=='__main__':unittest.main()
