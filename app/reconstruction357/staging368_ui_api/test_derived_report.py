import unittest,copy
from test_qualified_binding import fixture
from derived_report import derive
class Tests(unittest.TestCase):
 def objects(self):
  final,e,r=fixture();raw={'generation_run_id':r,'status':'REVIEWED_NOT_QUALIFIED',**{k:e[k]for k in ('canonical_request_digest','raw_digest','received_digest')}}
  semantic={k:v for k,v in final.items()if k!='state'};semantic.update(status='QUALIFIED_FIXED_CURRENT_RUN',received_digest=e['received_digest'])
  return raw,semantic,e,r
 def test_projection_preserves_inputs(self):
  raw,s,e,r=self.objects();before=copy.deepcopy((raw,s));out=derive(raw,s,e,r);self.assertEqual(out['state'],'QUALIFIED_CONCEPTUAL_SET');self.assertEqual((raw,s),before);self.assertFalse(out['accepted'])
 def test_other_run_rejected(self):
  raw,s,e,r=self.objects();s['generation_run_id']='other'
  with self.assertRaises(ValueError):derive(raw,s,e,r)
 def test_unknown_remains_unknown(self):
  raw,s,e,r=self.objects();s={'status':'UNKNOWN','generation_run_id':r,'missing':['TEST_ONLY']};out=derive(raw,s,e,r);self.assertEqual(out['state'],'UNKNOWN');self.assertFalse(out['repair_attempted'])
 def test_unregistered_status(self):
  raw,s,e,r=self.objects();s['status']='PASS'
  with self.assertRaises(ValueError):derive(raw,s,e,r)
if __name__=='__main__':unittest.main()
