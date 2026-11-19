import copy,json,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
import structural_pair302 as m
class Structural(unittest.TestCase):
 def projection(self,model='a'*64,x='2'):
  return {'input':['18','20',2],'programme':{'bedrooms':2},'profile':{'body_m':'.7'},'frame':'ACTUAL_FRONT_REAR_WORLD_XY','model_digest':model,
   'units':[{'unit':u,'access':[['living','bedroom']],'regions':{'bedroom':[['0','0','1','1']],'kitchen':[[x,'0',str(float(x)+1),'1']],'common_lobby':[['0','2','1','3']]}}for u in('A','B')],
   'source_witness_digest':'synthetic_projection_only'}
 def retained(self,d,projections):
  a=m.descriptor_import();rows=[]
  for case,p in zip(('V0','V2'),projections):
   folder=Path(d)/case;folder.mkdir();(folder/'projection.json').write_text(json.dumps(p))
   desc=a.descriptor(p);rows.append({'case':case,**{k:'f'*64 for k in('raw_digest','core_digest','profile_digest','program_digest','source_digest')},'completed':True,'integrity_verified':True,'descriptor_state':'ACTUAL_MODEL_BOUND_DESCRIPTOR','projection_digest':m.digest(p),'model_digest':p['model_digest'],'descriptor_digest':m.digest(desc),'descriptor_signature':desc['signature']})
  return rows
 def test_source_constraints_equal_objectives_differ_no_solver(self):
  import numpy as np
  import source_fit_candidate207 as producer
  m.dependency_guard()
  p=m.prepare(b'{"W":"18","L":"20","n":2}');core,_=m.selected_core(p['raw'],'FRONT_REAR_COMPACT118')
  with patch.object(producer,'milp',side_effect=AssertionError('NO_SOLVER')):
   a,b=[producer.propose(core,2,time_limit=1,variant=v,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES',diagnostic_capture=lambda r:r)for v in(0,2)]
  self.assertEqual(m.capture_equivalence(a,b)['state'],'SAME_HARD_CONSTRAINTS_DIFFERENT_DECLARED_OBJECTIVE')
  broken=copy.deepcopy(b);broken['matrix'].data[0]+=1
  with self.assertRaises(ValueError):m.capture_equivalence(a,broken)
  broken=copy.deepcopy(b);broken['bounds'].ub[0]+=1
  with self.assertRaises(ValueError):m.capture_equivalence(a,broken)
  broken=copy.deepcopy(b);broken['objective']=a['objective'].copy()
  with self.assertRaises(ValueError):m.capture_equivalence(a,broken)
  for key in('lower','upper','integrality'):self.assertTrue(np.array_equal(a[key],b[key]),key)
  self.assertTrue(np.array_equal(a['bounds'].lb,b['bounds'].lb));self.assertTrue(np.array_equal(a['bounds'].ub,b['bounds'].ub))
  self.assertEqual(a['matrix'].shape,b['matrix'].shape);self.assertEqual((a['matrix']!=b['matrix']).nnz,0)
  self.assertEqual(a['specs'],b['specs']);self.assertEqual(a['row_metadata'],b['row_metadata'])
  names=[r[0]for r in a['specs']];expected=sorted([4*names.index('kitchen')+1,4*names.index('dining')])
  self.assertEqual(np.flatnonzero(a['objective']!=b['objective']).tolist(),expected)
 def test_registered_variants_only(self):
  self.assertEqual(m.VARIANTS,{'V0':0,'V2':2});self.assertEqual(set(m.CASES.values()),{('18','20')})
 def test_missing_descriptor_not_distinct(self):
  self.assertEqual(m.pair_readback([],Path('.'))['state'],'NOT_COMPARABLE_MISSING_BOUND_DESCRIPTOR')
 def test_projection_duplicate_not_padding(self):
  p=self.projection()
  with tempfile.TemporaryDirectory()as d:
   rows=self.retained(d,[p,copy.deepcopy(p)]);r=m.pair_readback(rows,Path(d))
  self.assertTrue(r['same_model']);self.assertEqual(r['state'],'EXACT_DESCRIPTOR_EQUIVALENT');self.assertFalse(r['qualified'])
 def test_projection_different_organisation_not_quality(self):
  p,q=self.projection(),self.projection('b'*64,'0')
  with tempfile.TemporaryDirectory()as d:
   rows=self.retained(d,[p,q]);r=m.pair_readback(rows,Path(d))
  self.assertEqual(r['state'],'DESCRIPTOR_DIFFERENCE_NOT_QUALITY');self.assertFalse(r['architectural_diversity_verified'])
 def test_projection_program_mismatch_not_distinct(self):
  p,q=self.projection(),self.projection('b'*64);q['programme']['bedrooms']=1
  with tempfile.TemporaryDirectory()as d:
   rows=self.retained(d,[p,q]);r=m.pair_readback(rows,Path(d))
  self.assertEqual(r['state'],'NOT_COMPARABLE')
 def test_projection_cross_model_rejected(self):
  with tempfile.TemporaryDirectory()as d:
   rows=self.retained(d,[self.projection(),self.projection('b'*64)]);rows[0]['model_digest']='c'*64
   with self.assertRaises(ValueError):m.pair_readback(rows,Path(d))
 def test_projection_rehashed_content_not_old_descriptor(self):
  with tempfile.TemporaryDirectory()as d:
   rows=self.retained(d,[self.projection(),self.projection('b'*64)])
   path=Path(d)/'V0/projection.json';p=json.loads(path.read_text());p['units'][0]['regions']['kitchen']=[['0','0','1','1']];path.write_text(json.dumps(p));rows[0]['projection_digest']=m.digest(p)
   with self.assertRaises(ValueError):m.pair_readback(rows,Path(d))
 def test_shared_budget_no_fallback(self):
  self.assertEqual(m.slot(249),0);self.assertEqual(m.slot(250),240)
 def test_unknown_cli_no_solver(self):
  with patch.object(sys,'argv',['structural_pair302.py','--retry']),patch.object(m,'run',side_effect=AssertionError('NO_RUN')):
   with self.assertRaises(ValueError):m.main()
if __name__=='__main__':unittest.main()
