"""Pure negative/provenance tests only. No model generation or fresh checker."""
import copy,hashlib,sys,time,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'runtime'))
import source_registry365 as registry
import source_identity365 as identity

class Tests(unittest.TestCase):
 def test_serialized_context_no_authority(self):
  self.assertFalse(registry.verify_context({'a':1},{'verified':True})['verified'])
 def test_token_required(self):
  with self.assertRaises(ValueError):registry.CurrentContext(object(),{},{},time.monotonic()+10)
 def test_wrong_schema_rejected_before_replay_process(self):
  with self.assertRaisesRegex(ValueError,'UNREGISTERED'):
   registry.resolve({'trace':{'schema':'ROW_BALANCED_PORTALS365_SOURCE_TRACE_V1'}},time.monotonic()+10)
 def test_expired_deadline_rejected_before_replay_process(self):
  with self.assertRaisesRegex(ValueError,'DEADLINE'):
   registry.resolve({'trace':{'schema':'DERIVED_BALANCED_SOURCE369_TRACE_V1'}},time.monotonic()-1)
 def test_source_seams_exact(self):
  canonical=HERE.parent/'planha_general150_runtime_work'
  for n in ('named_checks118.py','q11_boundary118.py','circulation_frame148.py','core_circulation_scope118.py'):
   original=(canonical/n).read_bytes();current=(HERE/'runtime'/n).read_bytes()
   identity.check_one(n,original,current,hashlib.sha256(original).hexdigest())
 def test_geometry_checker_byte_identical(self):
  parent=HERE.parent/'staging365_balanced_source_validation/runtime'
  for n in ('checker114.py','operation_check114.py','geometry114.py'):
   self.assertEqual((parent/n).read_bytes(),(HERE/'runtime'/n).read_bytes())

if __name__=='__main__':unittest.main(verbosity=2)
