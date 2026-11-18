"""Storage/binding tests only; synthetic negative responses are not layout evidence."""
import unittest,tempfile,json,sqlite3
from pathlib import Path
from service118 import Service
class Protocol(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.db=str(Path(self.tmp.name)/'test.sqlite');self.rev='test-revision';self.op='a'*32
  def run(raw,**kw):return dict(status='NO_ADMITTED_LAYOUT',requested_count=6,admitted_count=0,distinct_count=0,shortfall=6,candidates=[],rejections=[{'reason':'TEST_NEGATIVE_ONLY'}])
  self.s=Service(self.db,run,lambda c,r:c,lambda:self.rev,{'svg':lambda c:b'never'},15)
  self.raw=dict(operation_id=self.op,W='15',L='20',n='2',requested_count=6)
 def test_project_brief_has_only_three_fields(self):
  for key,val in [('program',{'bedrooms_per_unit':2}),('bedrooms_per_unit',2),('city','x'),('north','top'),('typology','x')]:
   r=self.s.handle('/generate-hybrid118',dict(self.raw,**{key:val}));self.assertEqual(r['reason'],'REQUEST_FIELDS',key)
 def test_new_generation_rejected_after_source_change(self):
  self.rev='changed-before-new-request';p=self.s.handle('/generate-hybrid118',self.raw);self.assertEqual(p['reason'],'SOURCE_REVISION_CHANGED')
 def tearDown(self):self.tmp.cleanup()
 def test_reopen_exact(self):
  p=self.s.handle('/generate-hybrid118',self.raw);self.assertEqual(p,self.s.handle('/reopen-hybrid118',{'operation_id':self.op}))
 def test_no_artifact_for_rejected(self):
  p=self.s.handle('/generate-hybrid118',self.raw)['result'];r=self.s.handle('/hybrid118-artifact',dict(operation_id=self.op,payload_hash=p['payload_hash'],candidate_id='invented',artifact_type='svg'));self.assertEqual(r['reason'],'ARTIFACT_SELECTION_BINDING')
 def test_operation_binding(self):
  self.s.handle('/generate-hybrid118',self.raw);r=self.s.handle('/generate-hybrid118',dict(self.raw,W='16'));self.assertEqual(r['reason'],'OPERATION_INPUT_CONFLICT')
 def test_revision_binding(self):
  self.s.handle('/generate-hybrid118',self.raw);self.rev='changed';r=self.s.handle('/reopen-hybrid118',{'operation_id':self.op});self.assertEqual(r['reason'],'SOURCE_REVISION_CHANGED')
 def test_storage_tamper(self):
  self.s.handle('/generate-hybrid118',self.raw)
  with sqlite3.connect(self.db)as db:
   x=json.loads(db.execute('SELECT payload FROM drafts118').fetchone()[0]);x['status']='FAKE';db.execute('UPDATE drafts118 SET payload=?',(json.dumps(x),))
  self.assertEqual(self.s.handle('/reopen-hybrid118',{'operation_id':self.op})['reason'],'SAVED_PAYLOAD_HASH')
if __name__=='__main__':unittest.main()
