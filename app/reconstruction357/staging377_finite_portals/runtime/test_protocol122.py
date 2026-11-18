"""Protocol aliases and isolated DB only, not generated-plan evidence."""
import unittest,tempfile
from pathlib import Path
from service118 import Service
class Protocol122(unittest.TestCase):
 def test_aliases_preserve_binding_and_failclosed(self):
  with tempfile.TemporaryDirectory() as t:
   calls=[]
   def run(raw,**kw):
    calls.append(raw);return dict(status='NO_ADMITTED_LAYOUT',requested_count=6,admitted_count=0,distinct_count=0,shortfall=6,candidates=[])
   s=Service(str(Path(t)/'122.sqlite'),run,lambda c,r:c,lambda:'test',{})
   r=dict(operation_id='b'*32,W='26.04',L='13.29',n=2,requested_count=6)
   p=s.handle('/generate-hybrid122',r)
   self.assertEqual(len(calls),1)
   self.assertEqual(p,s.handle('/reopen-hybrid122',{'operation_id':r['operation_id']}))
   self.assertEqual(p,s.handle('/reopen-hybrid118',{'operation_id':r['operation_id']}))
   self.assertEqual(s.handle('/generate-hybrid122',dict(r,W='27'))['reason'],'OPERATION_INPUT_CONFLICT')
   a=s.handle('/hybrid122-artifact',dict(operation_id=r['operation_id'],payload_hash=p['result']['payload_hash'],candidate_id='invented',artifact_type='svg'))
   self.assertEqual(a['reason'],'ARTIFACT_SELECTION_BINDING')
 def test_ui_no_method_selector_and_new_routes(self):
  s=(Path(__file__).parent/'reference118/index.html').read_text()
  self.assertNotIn('<select',s)
  for path in ['/generate-hybrid122','/reopen-hybrid122','/hybrid122-artifact']:self.assertIn(path,s)
  self.assertIn('selection:p.selection_evidence',s)
if __name__=='__main__':unittest.main()
