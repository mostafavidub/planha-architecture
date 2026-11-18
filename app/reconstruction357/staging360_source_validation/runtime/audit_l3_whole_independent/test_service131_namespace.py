import sys,tempfile,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from service131 import Service
from engine131 import select_scoped
from engine125 import validate_raw
class Tests(unittest.TestCase):
 def test_protocol(self):
  with tempfile.TemporaryDirectory()as d:
   calls=[]
   def run(raw,**kw):
    validate_raw(raw);calls.append(raw);n=raw['requested_count'];proof=select_scoped([],n)[1]
    return dict(status='NO_ADMITTED_LAYOUT',requested_count=n,distinct_count=0,shortfall=n,candidates=[],admitted_pool=[],admitted_count=0,internal_proposals=[],pool_diversity_diagnostics=proof,organization_count=0,organization_shortfall=n,scoped_diversity=proof,verified_architectural_diversity=False)
   s=Service(str(Path(d)/'db'),run,lambda c,r:c,lambda:'fixed',{})
   raw={'operation_id':'a'*32,'W':'35','L':'30.72','n':2,'requested_count':6}
   for fld in ('program','proposal','candidate','city','north','baseline_model_hash','existing_plan_id'):
    self.assertEqual(s.handle('/generate-hybrid131',dict(raw,**{fld:1}))['reason'],'REQUEST_FIELDS')
   self.assertEqual(calls,[])
   p=s.handle('/generate-hybrid131',raw);self.assertIn('result',p);self.assertEqual(p['result']['service_schema'],'GENERAL131');self.assertEqual(len(calls),1)
   self.assertEqual(s.handle('/reopen-hybrid131',{'operation_id':'a'*32}),p)
   self.assertEqual(s.handle('/generate-hybrid131',raw),p);self.assertEqual(len(calls),1)
   for path in ('/generate-hybrid130','/reopen-hybrid130','/hybrid130-artifact'):
    self.assertEqual(s.handle(path,{'operation_id':'a'*32})['reason'],'UNKNOWN_PATH')
 def test_hot_source(self):
  with tempfile.TemporaryDirectory()as d:
   rev=['a'];s=Service(str(Path(d)/'db'),lambda *a,**k:self.fail('dispatched'),None,lambda:rev[0],{});rev[0]='b'
   self.assertEqual(s.handle('/generate-hybrid131',{'operation_id':'a'*32})['reason'],'SOURCE_REVISION_CHANGED')
if __name__=='__main__':unittest.main()
