import unittest,tempfile
from pathlib import Path
from service128 import Service
from engine128 import select_scoped
class Protocol(unittest.TestCase):
 def test_strict_and_reopen(self):
  with tempfile.TemporaryDirectory()as d:
   calls=[]
   def run(raw,**kw):
    calls.append(raw);proof=select_scoped([],raw['requested_count'])[1]
    return {'requested_count':raw['requested_count'],'admitted_count':0,'distinct_count':0,'shortfall':raw['requested_count'],'candidates':[],'internal_proposals':[],'admitted_pool':[],'organization_count':0,'organization_shortfall':raw['requested_count'],'pool_diversity_diagnostics':proof,'scoped_diversity':proof,'verified_architectural_diversity':False}
   s=Service(str(Path(d)/'db'),run,lambda c,r:c,lambda:'fixed',{})
   raw={'operation_id':'a'*32,'W':'35','L':'30.72','n':2,'requested_count':6}
   for key in ['program','proposal','candidate','baseline_model_hash','existing_plan_id']:
    self.assertEqual(s.handle('/generate-hybrid128',dict(raw,**{key:'x'}))['reason'],'REQUEST_FIELDS')
   p=s.handle('/generate-hybrid128',raw);self.assertIn('result',p)
   self.assertEqual(p,s.handle('/reopen-hybrid128',{'operation_id':'a'*32}));self.assertEqual(len(calls),1)
   self.assertEqual(s.handle('/generate-hybrid127',raw)['reason'],'UNKNOWN_PATH')
if __name__=='__main__':unittest.main()
