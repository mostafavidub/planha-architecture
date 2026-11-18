import copy,unittest
from review_cycle import decide,digest
class PairReviewTests(unittest.TestCase):
 def candidate(self):
  m={'inputs':['15','25',2]};h=digest(m);p={'bedrooms':2,'sleep_roles':['double','twin']}
  return {'model':m,'model_digest':h,'candidate_id':'c','accepted':False,'delivery_allowed':False,'qualified':False,'generation_context':{'construction_trace':{'schema':'CONSTRUCTION_TRACE127_PAIR_V1','model_hash':h,'source_revision':'s','proposals':{'A':p,'B':copy.deepcopy(p)}}},'physical_review':{'model_hash':h,'status':'PASS_CONCEPT_SCOPED_REVIEW','errors':[],'pending':[],'multiproposal_provenance127':{'model_hash':h,'source_revision':'s','verified':True,'errors':[],'pending':[]}}}
 def test_pair_scoped_pass_is_not_qualification(self):
  d=decide(self.candidate(),'r','s');self.assertEqual(d['state'],'PHYSICAL_PASS_SEMANTIC_UNKNOWN');self.assertFalse(d['accepted']);self.assertFalse(d['delivery_allowed'])
 def test_trace_required(self):
  c=self.candidate();c.pop('generation_context')
  with self.assertRaisesRegex(ValueError,'PAIR_TRACE_REQUIRED'):decide(c,'r','s')
 def test_program_cannot_change(self):
  c=self.candidate();c['generation_context']['construction_trace']['proposals']['A']['bedrooms']=3
  with self.assertRaisesRegex(ValueError,'TWO_BEDROOM_SOURCE_REQUIRED'):decide(c,'r','s')
 def test_ambiguous_origin_rejected(self):
  c=self.candidate();c['physical_review']['hierarchical_provenance129']={}
  with self.assertRaisesRegex(ValueError,'AMBIGUOUS'):decide(c,'r','s')
 def test_unverified_origin_rejected(self):
  c=self.candidate();c['physical_review']['multiproposal_provenance127']['verified']=False
  with self.assertRaisesRegex(ValueError,'RECONSTRUCTION_PROOF_REQUIRED'):decide(c,'r','s')
 def test_rejection_with_pending_does_not_authorize_repair(self):
  c=self.candidate();c['physical_review'].update(status='FAIL',errors=['route'],pending=['unknown'])
  d=decide(c,'r','s');self.assertEqual(d['state'],'REJECTED_PHYSICAL');self.assertFalse(d['operator_invoked'])
if __name__=='__main__':unittest.main()
