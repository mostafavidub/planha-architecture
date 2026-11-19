import unittest,copy,numpy as np
from bounded_repair_chain import candidate_transport,operator_transport,digest,bind_result
def proposal():
 return {'status':'PROPOSAL_ONLY','independent_shared_group_study':{'schema':'V25_FOUR_SEAT_ENVELOPE_PROPOSAL_ONLY','accepted':False,'historical_shared_gate_marker':False,'seat_uses':['sofa1_use','sofa2_use','chair1_use','chair2_use'],'envelope':[np.float64(0),np.float64(-0.0),np.float64(2),np.float64(2)],'body_witness':[np.float64(.1),np.float64(.1),np.float64(.8),np.float64(.8)],'source_body_m':'7/10','network_paths':{n:[[np.float64(i),np.float64(i)] for i in range(4)] for n in ['sofa1_use','sofa2_use','chair1_use','chair2_use']}}}
def nochild():
 op={'parent_model_digest':'parent','child':None};op['receipt_digest']=digest(op)
 r={'nonce':'nonce','completed':True,'source_integrity_verified':True,'state':'BOUNDED_SEARCH_NO_CHILD_NOT_INFEASIBLE','operator_result_digest':digest(op),'parent_model_digest':'parent','generated_count':0,'verified_generated_count':0,'fresh_child_binding_verified':False,'child_observed':False,**{k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')}}
 return r,op
def withchild():
 r,op=nochild();m={'synthetic':True};mh=digest(m)
 reports={'physical':{'model_hash':mh,'status':'FAIL'},'replay':{'verified':True}}
 pins={k:digest(v) for k,v in reports.items()}
 b={'packet':{'world_model':m},'model_digest':mh,'reports':reports,'report_digests':pins,**{k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')}}
 d={'model_digest':mh,'physical_digest':pins['physical'],'integrity_verified':True,'decision':{'state':'BLOCKED'},**{k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')}}
 op.pop('receipt_digest');op['child']={'model_digest':mh};op['receipt_digest']=digest(op)
 r.update(state='FRESH_CHILD_ALL_GATES_RECORDED_NOT_QUALIFIED',generated_count=1,verified_generated_count=1,child_observed=True,fresh_child_binding_verified=True,operator_result_digest=digest(op),child_model_digest=mh,child_runtime_digest=digest(b),reports=reports,report_digests=pins,current_decision_digest=digest(d),current_decision=d['decision'])
 return r,op,b,d
class Tests(unittest.TestCase):
 def test_synthetic_child_receipt_binding_only(self):
  r,o,b,d=withchild();self.assertTrue(bind_result(r,'nonce',o,b,d))
 def test_child_model_mutation(self):
  r,o,b,d=withchild();b['packet']['world_model']['extra']=1
  with self.assertRaises(ValueError):bind_result(r,'nonce',o,b,d)
 def test_child_decision_mutation(self):
  r,o,b,d=withchild();d['integrity_verified']=False
  with self.assertRaises(ValueError):bind_result(r,'nonce',o,b,d)
 def test_child_boolean_count(self):
  r,o,b,d=withchild();r['generated_count']=True
  with self.assertRaises(ValueError):bind_result(r,'nonce',o,b,d)

 def test_parent_receipt_nochild(self):
  r,o=nochild();self.assertTrue(bind_result(r,'nonce',o))
 def test_unknown_receipt_state(self):
  r,o=nochild();r['state']='unexpected'
  with self.assertRaises(ValueError):bind_result(r,'nonce',o)
 def test_nochild_falsecount(self):
  r,o=nochild();r['generated_count']=1
  with self.assertRaises(ValueError):bind_result(r,'nonce',o)
 def test_nochild_spurious_decision(self):
  r,o=nochild();r['current_decision']={}
  with self.assertRaises(ValueError):bind_result(r,'nonce',o)
 def test_wrong_nonce(self):
  r,o=nochild()
  with self.assertRaises(ValueError):bind_result(r,'wrong',o)
 def test_wrong_operator_digest(self):
  r,o=nochild();o['unlisted']=0
  with self.assertRaises(ValueError):bind_result(r,'nonce',o)
 def test_child_state_missing_files(self):
  r,o=nochild();r.update(state='FRESH_CHILD_ALL_GATES_RECORDED_NOT_QUALIFIED',generated_count=1,verified_generated_count=1,child_observed=True,fresh_child_binding_verified=True)
  with self.assertRaises(ValueError):bind_result(r,'nonce',o)

 def test_exact_group_transport(self):
  p=proposal();q,r=candidate_transport(p);self.assertEqual(digest(p),digest(q));self.assertTrue(r['group_coordinate_conversions']);self.assertIs(type(q['independent_shared_group_study']['envelope'][0]),float)
 def test_no_mutation(self):
  p=proposal();h=digest(p);candidate_transport(p);self.assertEqual(digest(p),h)
 def test_nonfinite(self):
  p=proposal();p['independent_shared_group_study']['envelope'][0]=np.float64(float('inf'))
  with self.assertRaises((ValueError,OverflowError)):candidate_transport(p)
 def test_metadata_numpy_rejected(self):
  p=proposal();p['bedrooms']=np.float64(2)
  with self.assertRaises(ValueError):candidate_transport(p)
 def test_bad_group_marker(self):
  p=proposal();p['independent_shared_group_study']['historical_shared_gate_marker']=True
  with self.assertRaises(ValueError):candidate_transport(p)
 def test_bad_seat_set(self):
  p=proposal();p['independent_shared_group_study']['seat_uses'][0]='unknown'
  with self.assertRaises(ValueError):candidate_transport(p)
 def test_bad_route_shape(self):
  p=proposal();p['independent_shared_group_study']['network_paths']['sofa1_use'].pop()
  with self.assertRaises(ValueError):candidate_transport(p)
 def test_unknown_nested_numpy(self):
  p=proposal();p['independent_shared_group_study']['unexpected']=np.float64(1)
  with self.assertRaises(ValueError):candidate_transport(p)
 def test_operator_digest(self):
  p={'attempts':[{'proposal':proposal()}],'child':None};q,r=operator_transport(p);self.assertEqual(digest(p),digest(q))
 def test_no_child_explicit(self):
  p={'attempts':[],'child':None};q,_=operator_transport(p);self.assertIsNone(q['child'])
if __name__=='__main__':unittest.main()
