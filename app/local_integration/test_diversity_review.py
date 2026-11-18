import unittest,json,copy
from diversity_review import audit,ROOT
class Diversity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads((ROOT/'app/local_integration/evidence/requests/bce0971e-bac5-48fc-9a95-d32c47140168/result.json').read_text())
 def run_audit(self,c):return audit(c,self.r['envelope']['canonical_request_digest'],self.r['engine_source_revision'])
 def test_real_pair_not_family_label_proof(self):
  r=self.run_audit(self.r['candidates']);self.assertEqual(r['required_pairs'],1);self.assertEqual(len(r['pairs']),1);self.assertFalse(r['pairs'][0]['distinct']);self.assertEqual(r['qualified_count'],0)
 def test_six_copies_all_fifteen_pairs(self):
  r=self.run_audit([copy.deepcopy(self.r['candidates'][0])for _ in range(6)]);self.assertEqual(r['required_pairs'],15);self.assertEqual(len(r['pairs']),15);self.assertTrue(all(p['status']=='DUPLICATE_MODEL'for p in r['pairs']));self.assertEqual(r['qualified_count'],0)
 def test_tampered_review_fails_closed(self):
  c=copy.deepcopy(self.r['candidates']);c[0]['review_decision']['state']='FAKE';r=self.run_audit(c);self.assertTrue(r['descriptor_failures']);self.assertFalse(r['pairs'][0]['distinct'])
 def test_single_no_false_diversity(self):
  r=self.run_audit(self.r['candidates'][:1]);self.assertEqual(r['pairs'],[]);self.assertEqual(r['proven_distinct_pairs'],0)
if __name__=='__main__':unittest.main()
