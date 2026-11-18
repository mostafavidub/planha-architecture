import unittest,copy
from review_cycle import decide,digest
class ReceiptTests(unittest.TestCase):
 def setUp(self):
  model={'test':'synthetic'};h=digest(model);self.c={'model':model,'model_digest':h,'candidate_id':'c','accepted':False,'delivery_allowed':False,'qualified':False,'physical_review':{'model_hash':h,'status':'PASS_CONCEPT_SCOPED_REVIEW','errors':[],'pending':[],'hierarchical_provenance129':{'verified':True,'model_hash':h,'source_revision':'s','errors':[],'pending':[]}}};self.r={'schema':'MAC_PARAMETRIC_REPAIR_RECEIPT_V1','source_revision':'s','accepted':False,'delivery_allowed':False,'mechanics_success':True,'child_model_digest':h,'parent_model_digest':'old','repair_attempted':True,'operator_invoked':True,'state':'REPAIRED_PHYSICAL_SEMANTIC_UNKNOWN'}
 def test_bound_repair_receipt(self):
  d=decide(self.c,'req','s',self.r);self.assertTrue(d['repair_attempted']);self.assertFalse(d['accepted']);self.assertEqual(d['repair_receipt_digest'],digest(self.r))
 def test_receipt_wrong_model(self):
  self.r['child_model_digest']='wrong'
  with self.assertRaises(ValueError):decide(self.c,'req','s',self.r)
 def test_receipt_false_authority(self):
  self.r['accepted']=True
  with self.assertRaises(ValueError):decide(self.c,'req','s',self.r)
 def test_receipt_wrong_source(self):
  self.r['source_revision']='other'
  with self.assertRaises(ValueError):decide(self.c,'req','s',self.r)
