"""Protocol aliases and isolated DB only, not generated-plan evidence."""
import unittest,tempfile
from pathlib import Path
from service118 import Service
class Protocol121(unittest.TestCase):
 def test_aliases_preserve_binding_and_failclosed(self):
  with tempfile.TemporaryDirectory() as t:
   calls=[]
   def run(raw,**kw):
    calls.append(raw);return dict(status='NO_ADMITTED_LAYOUT',requested_count=6,admitted_count=0,distinct_count=0,shortfall=6,candidates=[])
   s=Service(str(Path(t)/'121.sqlite'),run,lambda c,r:c,lambda:'test',{})
   r=dict(operation_id='b'*32,W='26.04',L='13.29',n=2,requested_count=6)
   p=s.handle('/generate-hybrid121',r)
   self.assertEqual(len(calls),1)
   self.assertEqual(p,s.handle('/reopen-hybrid121',{'operation_id':r['operation_id']}))
   self.assertEqual(p,s.handle('/reopen-hybrid118',{'operation_id':r['operation_id']}))
   self.assertEqual(s.handle('/generate-hybrid121',dict(r,W='27'))['reason'],'OPERATION_INPUT_CONFLICT')
   a=s.handle('/hybrid121-artifact',dict(operation_id=r['operation_id'],payload_hash=p['result']['payload_hash'],candidate_id='invented',artifact_type='svg'))
   self.assertEqual(a['reason'],'ARTIFACT_SELECTION_BINDING')
 def test_ui_no_method_selector_and_new_routes(self):
  s=(Path(__file__).parent/'reference118/index.html').read_text()
  self.assertNotIn('<select',s)
  for path in ['/generate-hybrid121','/reopen-hybrid121','/hybrid121-artifact']:self.assertIn(path,s)
  self.assertIn('selection:p.selection_evidence',s)
if __name__=='__main__':unittest.main()
