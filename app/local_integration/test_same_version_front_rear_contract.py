import copy,json,unittest
from public_wln_contract import parse_public
import same_version_front_rear_contract as c
class ContractTests(unittest.TestCase):
 def setUp(self):
  self.body=b'{"W":"18","L":"20","n":2}'
  self.e=parse_public(self.body)
 def test_request_lineage(self):
  r=c.bind_request(self.body,self.e,'PROGRAM_2BED_V1')
  self.assertEqual(r['raw'],{'W':'18','L':'20','n':2,'requested_count':1})
  self.assertEqual(r['program_registry_digest'],c.digest(r['program_registry']))
  self.assertEqual(r['contract_digest'],c.digest(c.contract()))
 def test_program_no_fallback(self):
  for p in (None,2,True,'PROGRAM_1BED_V1','PROGRAM_3BED_V1','unknown'):
   with self.assertRaises(ValueError):c.bind_request(self.body,self.e,p)
 def test_transport_required(self):
  for e in (dict(self.e,transport_body_sha256='0'*64),dict(self.e,qualified=True)):
   with self.assertRaises(ValueError):c.bind_request(self.body,e,'PROGRAM_2BED_V1')
 def test_other_case_rejected(self):
  for raw in ({'W':'20','L':'18','n':2},{'W':'18','L':'20','n':1}):
   b=json.dumps(raw).encode()
   with self.assertRaises(ValueError):c.bind_request(b,parse_public(b),'PROGRAM_2BED_V1')
 def test_copy_isolation(self):
  a=c.contract();a['api_parameters']['search114.propose'].append('fake')
  self.assertNotIn('fake',c.contract()['api_parameters']['search114.propose'])
  r=c.bind_request(self.body,self.e,'PROGRAM_2BED_V1');r['envelope']['received_input']['W']='5'
  self.assertEqual(self.e['received_input']['W'],'18')
 def test_authority(self):
  for obj in (c.contract(),c.bind_request(self.body,self.e,'PROGRAM_2BED_V1')):
   for k in ('accepted','qualified','display_allowed','delivery_allowed'):self.assertIs(obj[k],False)
 def test_scope(self):
  x=c.contract()
  self.assertFalse(x['fresh_model_executed'])
  self.assertEqual(x['quality'],'PROFILE_NOT_READY')
  self.assertFalse(x['technical_profile_is_program_approval'])
  self.assertFalse(x['search']['no_witness_is_global_infeasibility'])
  self.assertEqual(x['search']['requested_count'],1)
 def test_explicit_program(self):
  x=c.contract()
  self.assertEqual(x['bedrooms_per_unit'],2);self.assertEqual(x['sleep_roles'],['double','twin'])
  self.assertEqual(x['api_parameters']['functional_review.assess'],['model','physical_review','source_revision'])
 def test_exact_digest_types(self):
  self.assertNotEqual(c.digest(2),c.digest(2.0))
  self.assertNotEqual(c.digest(0),c.digest(False))
if __name__=='__main__':unittest.main()
