"""Current V3 preflight coverage only. No solver, model, or qualification proof."""
import hashlib,pathlib,unittest,json
from unittest.mock import patch
from live_program_scheduler import preflight
from public_wln_contract import SCHEMA,DOMAIN_POLICY_VERSION
from dimension_contract import InputError
ROOT=pathlib.Path(__file__).resolve().parents[2]
PINS={
  "app/local_integration/public_wln_contract.py": "80fd2b2710342735dc35e484c9b0da790995d830",
  "app/local_integration/live_program_scheduler.py": "1b671b6632d01c1012fcb39b2c33e731fb619fbc",
  "app/local_integration/program_profile_registry.py": "af549f86f39e2e57554cd48e0ffdea54d5444262",
  "app/local_integration/same_version_front_rear_contract.py": "0c182a3e26ba48ef6a42df2bf40c2a2ab67c055c",
  "app/local_integration/front_rear_runtime_adapter.py": "92ce916b71bb05f0087e2527a51dd8de4d40a676",
  "app/reconstruction357/planha_general150_runtime_work/constructor127.py": "beb67bf4b08a65242305519a678eef94fef3fad6",
  "app/reconstruction357/planha_general150_runtime_work/contract114.py": "a2631c6a38a43b8d423edf82ad8d526ced1b8196",
  "app/reconstruction357/planha_general150_runtime_work/frame_contract125.py": "de9d4b2daa8024e1feac526649dafb6ac301706a",
  "app/reconstruction357/planha_general150_runtime_work/search114.py": "65e0f278c9f9ef480388d3ea8056161c0a938a36"
}
class CurrentCoverage(unittest.TestCase):
 def test_current_source_identity(self):
  for path,pin in PINS.items():
   b=(ROOT/path).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin,path)
  self.assertEqual(SCHEMA,'V25_PUBLIC_WLN_CONTRACT_V3')
  self.assertEqual(DOMAIN_POLICY_VERSION,'MVP_UNIT_DOMAIN_PRD_V3')
 def test_selected_and_valid_unsupported_cases(self):
  cases=[('18','20',2,True,'READY_SCOPED_CONTRACT_ONLY'),('18','20',1,False,'UNSUPPORTED_CURRENT_ENGINE_UNIT_COUNT')]
  cases += [(w,l,2,False,'UNSUPPORTED_SELECTED_SAME_VERSION_CASE') for w,l in [('5','5'),('25','25'),('5','25'),('25','5'),('20','18'),('12.5','20'),('18','18')]]
  with patch('subprocess.Popen',side_effect=AssertionError('UNEXPECTED_PROCESS')) as proc:
   for w,l,n,ready,state in cases:
    with self.subTest(w=w,l=l,n=n):
     r=preflight(json.dumps({'W':w,'L':l,'n':n}).encode())
     self.assertIs(r['input_valid'],True);self.assertIs(r['execution_ready'],ready);self.assertEqual(r['state'],state)
     for k in ('accepted','qualified','display_allowed','delivery_allowed'):self.assertIs(r[k],False)
     if ready:
      p=r['binding']['program_registry'];self.assertEqual(p['id'],'PROGRAM_2BED_V1');self.assertEqual(p['design_persons_per_unit'],4)
   proc.assert_not_called()
 def test_v3_required_invalid_and_wire_states(self):
  cases=[({'W':'18','L':'20'},'INPUT_REQUIRED'),({'W':'18','L':'20','n':None},'INPUT_REQUIRED')]
  cases += [({'W':'18','L':'20','n':n},'INVALID_BRIEF') for n in (3,4,0,-1,True,1.5,'abc','1.5')]
  cases += [({'W':18.5,'L':'20','n':2},'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION')]
  for raw,code in cases:
   with self.subTest(raw=raw):
    with self.assertRaises(InputError) as e:preflight(json.dumps(raw).encode())
    self.assertEqual(e.exception.code,code)
if __name__=='__main__':unittest.main()
