import copy,unittest,tempfile
from pathlib import Path
import actual_descriptor301 as a
class Projection(unittest.TestCase):
 def fixture(self):
  return {'input':['18','20',2],'programme':{'units':2},'profile':{'body_m':'.7'},'frame':'PROJECTION_UNIT_FIXTURE',
   'model_digest':'0'*64,'source_witness_digest':'1'*64,'units':[
    {'unit':'A','access':[['kitchen','public']],'regions':{'kitchen':[['1','1','3','4']],'bedroom':[['7','1','10','4']],'common_stair':[['0','7','3','9']]}},
    {'unit':'B','access':[['bedroom','public']],'regions':{'kitchen':[['1','11','3','14']],'bedroom':[['7','16','10','19']],'common_stair':[['0','7','3','9']]}}]}
 def test_joint_unit_permutation(self):
  p=self.fixture();q=copy.deepcopy(p);q['units'].reverse()
  self.assertEqual(a.descriptor(p)['signature'],a.descriptor(q)['signature'])
 def test_independent_access_permutation_is_not_allowed(self):
  p=self.fixture();q=copy.deepcopy(p)
  q['units'][0]['access'],q['units'][1]['access']=q['units'][1]['access'],q['units'][0]['access']
  self.assertNotEqual(a.descriptor(p)['signature'],a.descriptor(q)['signature'])
 def test_global_d4(self):
  p=self.fixture()
  for M in a.c.D4:
   q=copy.deepcopy(p)
   for u in q['units']:u['regions']={k:[a.c.transform(r,{'matrix':M,'translation':['0','0']})for r in rs]for k,rs in u['regions'].items()}
   self.assertEqual(a.descriptor(p)['signature'],a.descriptor(q)['signature'])
 def test_comparability_contract(self):
  p=self.fixture()
  for k,v in [('input',['19','20',2]),('programme',{'units':1}),('profile',{'body_m':'.8'}),('frame','other')]:
   q=copy.deepcopy(p);q[k]=v
   self.assertEqual(a.compare_projections(p,q)['state'],'NOT_COMPARABLE')
 def test_native_finite_float_transport_identity(self):
  p={'coordinate':1.25,'count':2};self.assertEqual(a.digest(p),a.hashlib.sha256(a.json.dumps(p,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest())
  self.assertNotEqual(a.digest(2),a.digest(2.0));self.assertNotEqual(a.digest(1),a.digest(True))
 def test_nonfinite_and_tuple_rejected(self):
  for v in(float('nan'),float('inf'),float('-inf')):
   with self.assertRaisesRegex(ValueError,'NONFINITE_JSON'):a.digest(v)
  with self.assertRaisesRegex(ValueError,'EXACT_JSON_TYPES'):a.digest((1,2))
 def test_result_sets_fail_closed(self):
  good={'projection_checks':{k:True for k in('opaque_unit_and_order_projection_only','global_mirror_projection_only','synthetic_organization_difference_only')},
   'actual_negatives':[{'kind':k,'descriptor_binding_rejected':True}for k in('fixture_geometry','opening_reference','module_inventory')]}
  a.check_results(good)
  for key in good['projection_checks']:
   q=copy.deepcopy(good);q['projection_checks'][key]=False
   with self.assertRaisesRegex(ValueError,'PROJECTION_CHECK_SET'):a.check_results(q)
  q=copy.deepcopy(good);q['actual_negatives'][0]['descriptor_binding_rejected']=False
  with self.assertRaisesRegex(ValueError,'ACTUAL_NEGATIVE_SET'):a.check_results(q)
 def test_failure_receipt_real_file_safe_and_nonce_bound(self):
  with tempfile.TemporaryDirectory()as tmp:
   folder=Path(tmp);a.write_failure(folder,'nonce',ValueError('private detail must never be copied'))
   r=a.read_failure(folder,'nonce')
   self.assertEqual(r['code'],'UNCLASSIFIED_STAGE_FAILURE');self.assertFalse(r['receipt_verified'])
   self.assertNotIn('private detail',(folder/'failure.json').read_text())
   with self.assertRaisesRegex(ValueError,'FAILURE_NONCE_OR_REQUEST'):a.read_failure(folder,'stale-nonce')
 def test_failure_receipt_unknown_stage_rejected(self):
  with tempfile.TemporaryDirectory()as tmp:
   folder=Path(tmp);a.write_failure(folder,'nonce',ValueError('RUNTIME_INTEGRITY'))
   r=a.json.loads((folder/'failure.json').read_text());r['stage']='made-up'
   a.write(folder/'failure.json',r)
   with self.assertRaisesRegex(ValueError,'FAILURE_ENUM_AUTHORITY'):a.read_failure(folder,'nonce')
   for bad in([],{}):
    r['stage']=bad;a.write(folder/'failure.json',r)
    with self.assertRaisesRegex(ValueError,'FAILURE_ENUM_TYPES'):a.read_failure(folder,'nonce')
 def test_current_integrity_and_physical_binding(self):
  ph={'status':'FAIL','model_hash':'model'};bundle={'model_digest':'model','reports':{'physical':ph},'report_digests':{'physical':a.digest(ph)}}
  r={'integrity_verified':True,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'model_digest':'model','state':'UNKNOWN',
   'original_physical_digest':a.digest(ph),'original_physical_report':ph,'replay':{'verified':True,'model_hash':'model'}}
  a.current_report_binding('source_guest_route_evaluator',r,bundle)
  for key,value in [('integrity_verified',False),('missing',['error']),('original_physical_digest','bad'),('qualified',True)]:
   q=copy.deepcopy(r);q[key]=value
   with self.assertRaises(ValueError):a.current_report_binding('source_guest_route_evaluator',q,bundle)
if __name__=='__main__':unittest.main()
