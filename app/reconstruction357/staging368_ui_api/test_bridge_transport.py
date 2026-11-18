import unittest,copy
import test_derived_report
from derived_report import derive,unwrap_bridge
from state_machine import digest
class Tests(unittest.TestCase):
 def fixture(self):
  raw,s,e,r=test_derived_report.Tests().objects();sup={'reason':'COMPLETED','worker_returncode':0,'worker_reaped':True,'cleanup_verified':True,'unresolved':[]}
  rec={'generation_run_id':r,'raw_pipeline_digest':digest(raw),'request_digest':digest({'run_id':r,'envelope':e}),'source_unchanged':True,'bridge_result':s}
  f={'schema':'DERIVED_FINAL_REPORT368','generation_run_id':r,'raw_pipeline_digest':digest(raw),'bridge_receipt_digest':digest(rec),'supervision_digest':digest(sup),'qualified_set':s}
  return f,rec,sup,raw,e,r
 def test_exact(self):
  f,rec,sup,raw,e,r=self.fixture();self.assertEqual(unwrap_bridge(f,rec,sup,raw,e,r),rec['bridge_result'])
 def test_changed_receipt(self):
  f,rec,sup,raw,e,r=self.fixture();rec['source_unchanged']=False
  with self.assertRaises(ValueError):unwrap_bridge(f,rec,sup,raw,e,r)
 def test_timeout_resealed_not_qualified(self):
  f,rec,sup,raw,e,r=self.fixture();sup['reason']='TIMEOUT';f['supervision_digest']=digest(sup)
  with self.assertRaises(ValueError):unwrap_bridge(f,rec,sup,raw,e,r)
 def test_wrong_request_even_resealed(self):
  f,rec,sup,raw,e,r=self.fixture();rec['request_digest']='old';f['bridge_receipt_digest']=digest(rec)
  with self.assertRaises(ValueError):unwrap_bridge(f,rec,sup,raw,e,r)
 def test_actual_rejection_projection(self):
  raw,s,e,r=test_derived_report.Tests().objects();b=s['members'][0]['binding'];raw['members']=[{'kind':'balanced','review':{'binding':b,'review_id':b['review_id'],'fresh_result_digest':b['fresh_digest']}}]
  rej={'kind':'balanced','binding':b,'status':'REJECTED_UNSUPPORTED_REDESIGN','reasons':[{'code':'TEST_ONLY_STRUCTURED_ERROR'}],'pending':[{'test_only':True}],'supported_repair_operators':[],'model_digest':b['model_digest'],'fresh_digest':b['fresh_digest']}
  s={'generation_run_id':r,'status':rej['status'],'current_rejection':rej,'supported_repair_operators':[]}
  out=derive(raw,s,e,r);self.assertEqual(out['state'],rej['status']);self.assertEqual(out['current_rejection']['pending'],rej['pending']);self.assertFalse(out['repair_attempted'])
  rej['binding']=dict(b,review_id='stale')
  with self.assertRaises(ValueError):derive(raw,s,e,r)
if __name__=='__main__':unittest.main()
