import tempfile,unittest
from pathlib import Path
from producer_provenance import snapshot,require_unchanged,receipt
from review_cycle import digest
class ProducerTests(unittest.TestCase):
 def test_changed_sources_fail_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'p.py';p.write_text('a=1')
   before=snapshot(d,['p.py']);require_unchanged(d,before)
   p.write_text('a=2')
   with self.assertRaisesRegex(ValueError,'SOURCE_CHANGED'):require_unchanged(d,before)
 def test_no_sources_is_not_provenance(self):
  with self.assertRaisesRegex(ValueError,'SOURCES_REQUIRED'):snapshot('.',[])
 def test_bound_receipt_never_qualifies(self):
  model={'x':1};h=digest(model)
  r=receipt(sources={'p.py':'a'*64},request_digest='request',raw={},proposal={},packet={'world_model':model},context={'construction_trace':{'raw':{},'proposal':{},'model_hash':h}},review={'model_hash':h},engine_revision='e')
  self.assertFalse(r['accepted']);self.assertFalse(r['delivery_allowed']);self.assertFalse(r['qualified'])
  claimed=r.pop('receipt_digest');self.assertEqual(claimed,digest(r))
 def test_foreign_review_rejected(self):
  with self.assertRaisesRegex(ValueError,'MODEL_BINDING'):
   receipt(sources={'p.py':'a'*64},request_digest='r',raw={},proposal={},packet={'world_model':{}},context={'construction_trace':{'raw':{},'proposal':{},'model_hash':digest({})}},review={'model_hash':'wrong'},engine_revision='e')
if __name__=='__main__':unittest.main()
