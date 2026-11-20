"""Synthetic guard/matrix/archival controls only. Never call an optimizer."""
import copy,tempfile,time,unittest
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import Bounds,LinearConstraint
from scipy.sparse import csr_matrix
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'studies'))
import p28_private_one_child as p

def matrix():
 A=csr_matrix([[0.,1.5],[-4.,0.],[3.,5.]])
 args={'c':np.array([-.0,1.271]),'integrality':np.array([1,0]),'bounds':Bounds([0.,1.],[10.,11.]),
       'constraints':LinearConstraint(A,[0.,-1.,-4.],[4.,5.,float('inf')])}
 z={'data':A.data.copy(),'indices':A.indices.copy(),'indptr':A.indptr.copy(),'matrix_shape':np.array([3,2]),
    'objective':args['c'].copy(),'variable_integrality':args['integrality'].copy(),
    'variable_lower':args['bounds'].lb.copy(),'variable_upper':args['bounds'].ub.copy(),
    'row_lower':args['constraints'].lb.copy(),'row_upper':args['constraints'].ub.copy()}
 return z,args
def routes():
 return {'units':[{'id':uid,'scenario_routes':{'guest_dining':[['0','0'],['0','1']]}}for uid in ('A','B')]}
def observations():
 return {'selected_causes':[],'rows':[
    {'unit':x,'cause':p.CAUSE,'route':'guest_dining','state':'ACTUAL_STORED_PATH_CLEAR_ORIGINAL_PROFILE','original_missing_route_count':0}
    for x in ('A','B')]}
def telemetry(j,i):
 v={'operator':1,'milp':1,'highs':1}
 return {'starts':v,'returns':dict(v),'matrix':{'match':True},'solver_status':j,'incumbent':i}
class TestP28(unittest.TestCase):
 def test_actual_scipy_constraint_structures_not_solve(self):
  arr,args=matrix()
  self.assertEqual(p.exact_matrix(arr,args),{'match':True,'shape':[3,2],'arrays':10})
 def test_one_csr_or_bound_or_objective_tamper_blocks(self):
  for k in ('data','indices','indptr','objective','variable_integrality','row_upper','variable_lower'):
   with self.subTest(k=k):
    ref,a=matrix();ref[k][0]+=1
    with self.assertRaisesRegex(ValueError,'P28_ACTUAL_SOLVER_MATRIX_MISMATCH'):p.exact_matrix(ref,a)
 def test_signed_float_zero_not_coerced(self):
  ref,a=matrix();ref['objective'][0]=0.0
  with self.assertRaisesRegex(ValueError,'P28_ACTUAL_SOLVER_MATRIX_MISMATCH'):p.exact_matrix(ref,a)
 def test_preserve_distinct_returned_dispositions(self):
  for j,i,status,wanted in ((1,True,'PROPOSAL_ONLY','WITNESS'),(1,False,'SEARCH_TIMEOUT_NO_WITNESS','SOLVER_TIMEOUT_NO_WITNESS'),
   (2,False,'NO_PROPOSAL_IN_THIS_TOPOLOGY','BOUNDED_NO_WITNESS'),(4,False,'NO_PROPOSAL_IN_THIS_TOPOLOGY','SOLVER_FAULT_NO_WITNESS'),
   (1,True,'ROUNDED_PROPOSAL_REJECTED','ROUNDED_WITNESS_REJECTED')):
   with self.subTest(j=j):
    self.assertEqual(p.classify_child({'solver_status':j,'status':status,'budget_seconds':30},telemetry(j,i)),wanted)
 def test_mismatched_incumbent_and_missing_or_double_call(self):
  x={'solver_status':1,'status':'PROPOSAL_ONLY','budget_seconds':30}
  with self.assertRaisesRegex(ValueError,'P28_WITNESS_STATUS'):p.classify_child(x,telemetry(1,False))
  z=telemetry(1,True);z['starts']['milp']=2
  with self.assertRaisesRegex(ValueError,'P28_WORKER_CALL_COUNTS'):p.classify_child(x,z)
 def test_matrix_check_required_even_for_time_limit(self):
  v=telemetry(1,False);v.pop('matrix')
  with self.assertRaisesRegex(ValueError,'P28_SOLVER_METADATA'):
   p.classify_child({'solver_status':1,'status':'SEARCH_TIMEOUT_NO_WITNESS','budget_seconds':30},v)
 def test_both_stored_actual_route_shapes_and_target_source_result(self):
  par={'selected_causes':[p.CAUSE]};m=routes();z=observations();good={'protected_verified':True}
  self.assertEqual(p.resolve(par,z,good,m)['state'],'BOTH_ACTUAL_STORED_GUEST_ROUTES_RESOLVED_NO_ADMISSION')
  for mutate in (lambda q:q['units'][1]['scenario_routes'].clear(),
                 lambda q:q['units'][1]['scenario_routes'].update(guest_dining=[]),
                 lambda q:q['units'].reverse()):
   bad=copy.deepcopy(m);mutate(bad)
   self.assertEqual(p.resolve(par,z,good,bad)['state'],'CHILD_NOT_PROVEN_TARGET_RESOLVED')
 def test_only_one_row_fake_clear_and_new_cause_rejected(self):
  par={'selected_causes':[p.CAUSE]}
  good={'protected_verified':True}
  for mutate in (lambda z:z['rows'].pop(),
                 lambda z:z['rows'][1].update(state='PLANNED_PATH_CLEAR'),
                 lambda z:z['rows'][1].update(original_missing_route_count=False),
                 lambda z:z['selected_causes'].append('NEW')):
   z=observations();mutate(z)
   self.assertEqual(p.resolve(par,z,good,routes())['state'],'CHILD_NOT_PROVEN_TARGET_RESOLVED')
  with self.assertRaisesRegex(ValueError,'P28_PROTECTED_CHILD'):p.resolve(par,observations(),{},routes())
 def test_child_cause_hash_bound_to_exact_model_and_physical(self):
  props={'A':{},'B':{}};m=routes();ph={'status':'FAIL'};ctx={'raw':{'n':2}}
  b={'model_digest':p.digest(m),'packet':{'world_model':m},'context':ctx,'reports':{'physical':ph},'report_digests':{'physical':p.digest(ph)}}
  d={'schema':'SOURCE_COMPOUND_PLANNED_CAUSE108_V3','model_digest':p.digest(m),'physical_digest':p.digest(ph),
     'context_digest':p.digest(ctx),'proposal_digest':p.digest(props)}
  p.bind_diagnostic(d,b,props)
  for key in ('model_digest','physical_digest','context_digest','proposal_digest'):
   wrong=dict(d,**{key:'a'*64})
   with self.assertRaisesRegex(ValueError,'P28_CHILD_DIAGNOSTIC_MODEL_PHYSICAL_BINDING'):
    p.bind_diagnostic(wrong,b,props)
 def test_manifest_requires_independent_expected_hash(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t); target=root/'input.json'
   key={'schema':'P28_EXTERNAL_PRIVATE_INPUTS_V1','files':{k:{'path':str(root/k),'sha256':'a'*64}for k in p.CONFIG_KEYS}}
   s=p.write(target,key)
   with self.assertRaisesRegex(ValueError,'P28_INDEPENDENT_EXTERNAL_MANIFEST'):p.config(target,'0'*64)
   self.assertEqual(p.config(target,s),key)
   for k in p.CONFIG_KEYS:p.write(root/k,{'wrong':'rehashed elsewhere'})
   with self.assertRaisesRegex(ValueError,'P28_EXTERNAL_BYTES'):p.all_inputs(key)
 def test_wrong_and_duplicate_json_do_not_promote(self):
  with self.assertRaisesRegex(ValueError,'P28_DUPLICATE_JSON'):p.decode(b'{"case":1,"case":2}')
  with self.assertRaisesRegex(ValueError,'P28_NONFINITE_JSON'):p.decode(b'{"case":1e1000}')
 def test_deadline_keeps_private_partial_only(self):
  with tempfile.TemporaryDirectory()as t:
   f=Path(t);p.write(f/'partial.json',{'unverified':'synthetic'})
   def late():
    while True:time.sleep(.01)
   v=p.stop_safe(f,time.monotonic()+.045,late)
   self.assertEqual(v['state'],'DEADLINE_PRIVATE_PARTIAL_ONLY')
   self.assertFalse((f/'receipt.json').exists());self.assertTrue((f/'partial.json').is_file())
   self.assertTrue((f/'terminal-unverified.json').is_file());self.assertFalse(v['qualified'])
 def test_staged_public_bytes_and_exact_p25_fr_domain(self):
  import p25_bound_evidence as q
  for rel,blob in p.PUBLIC_BLOBS.items():
   b=(p.BASE/rel).read_bytes()
   import hashlib
   self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest(),blob)
  got=q.source_state('FRONT_REAR')
  self.assertIn('app/local_integration/current_entry_boundary_x03.py',got)
if __name__=='__main__':unittest.main()
