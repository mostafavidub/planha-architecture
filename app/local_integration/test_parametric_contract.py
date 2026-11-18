import json,unittest
from parametric_worker import prepare
from dimension_contract import InputError

class ParametricContractTests(unittest.TestCase):
 def body(self,**kw):
  raw={'W':'24.000000000000000001','L':'25','n':2,'requested_count':6};raw.update(kw);return json.dumps(raw).encode()
 def test_exact_request_not_fixed_template(self):
  e,raw=prepare(self.body());self.assertEqual(raw,{'W':'24.000000000000000001','L':'25','n':2,'requested_count':6})
 def test_one_unit_explicitly_unsupported(self):
  with self.assertRaisesRegex(InputError,'UNSUPPORTED_UNIT_COUNT'):prepare(self.body(n=1))
 def test_program_not_silently_replaced(self):
  for p in [{'bedrooms_per_unit':2},{'bedrooms_per_unit':3,'capacity':8},None]:
   with self.assertRaisesRegex(InputError,'UNSUPPORTED_CUSTOM_PROGRAM'):prepare(self.body(program=p))
 def test_explicit_matching_profile(self):
  e,raw=prepare(self.body(program={'bedrooms_per_unit':3}));self.assertEqual(e['received_input']['program'],{'bedrooms_per_unit':3});self.assertEqual(raw['requested_count'],6)
 def test_option_count_not_clamped(self):
  with self.assertRaisesRegex(InputError,'UNSUPPORTED_OPTION_COUNT'):prepare(self.body(requested_count=13))

if __name__=='__main__':unittest.main()
