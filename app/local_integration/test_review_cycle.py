import copy, unittest
from review_cycle import decide,digest
class ReviewDecision(unittest.TestCase):
 def setUp(self):
  m={'example':'synthetic unit contract only'}; h=digest(m)
  self.c={'model':m,'model_digest':h,'candidate_id':'c','accepted':False,'delivery_allowed':False,'qualified':False,'physical_review':{'model_hash':h,'status':'PASS_CONCEPT_SCOPED_REVIEW','errors':[],'pending':[],'hierarchical_provenance129':{'model_hash':h,'verified':True,'source_revision':'s','errors':[],'pending':[]}}}
 def test_pass_not_qualified(self):
  r=decide(self.c,'r','s');self.assertEqual(r['state'],'PHYSICAL_PASS_SEMANTIC_UNKNOWN');self.assertFalse(r['qualified'])
 def test_synthetic_rejection_does_not_authorize_wrong_operator(self):
  self.c['physical_review'].update(status='FAIL',errors=[{'code':'FIXTURE_COLLISION'}]);r=decide(self.c,'r','s');self.assertEqual(r['state'],'REJECTED_PHYSICAL');self.assertFalse(r['operator_invoked'])
 def test_pending_is_unknown(self):
  self.c['physical_review'].update(status='NOT_EVALUATED',pending=['UNRESOLVED']);self.assertEqual(decide(self.c,'r','s')['state'],'UNKNOWN_REVIEW')
 def test_stale_model(self):
  self.c['model']['example']='changed'
  with self.assertRaises(ValueError):decide(self.c,'r','s')
 def test_stale_source(self):
  with self.assertRaises(ValueError):decide(self.c,'r','other')
 def test_contradiction(self):
  self.c['physical_review']['errors']=['FAIL']
  with self.assertRaises(ValueError):decide(self.c,'r','s')
 def test_no_mutation(self):
  old=copy.deepcopy(self.c);decide(self.c,'r','s');self.assertEqual(old,self.c)
 def test_no_boolean_acceptance(self):
  self.c['accepted']=True
  with self.assertRaises(ValueError):decide(self.c,'r','s')
if __name__=='__main__':unittest.main()
