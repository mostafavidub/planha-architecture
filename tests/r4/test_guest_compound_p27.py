"""Synthetic inputs; actual operators captured before MILP. No archived model."""
import copy,sys,unittest
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch
import numpy as np
import scipy.optimize as opt
import scipy.optimize._milp as scipy_milp
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'studies'),str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import cause_directed_candidate108 as old
import guest_compound_candidate_p27 as new
import guest_master_p11 as p11
import planned_witness_contract108 as contract
import planned_witness_support108 as support
from core_choice_pair_study import selected_core
from same_version_front_rear_contract import digest
import test_planned_witness108 as prior

def verify_capture(base,guest):
 scope=guest['p27_scope']
 m,n=base['matrix'].shape
 assert scope['old_row_count']==m and scope['old_var_end']==n+1,'P27_LEGACY_SHAPE'
 sj,gj=scope['serving_junction'],scope['guest_junction']
 assert 0<=sj<gj<n,'P27_JUNCTION_LAYOUT'
 spans=scope['guest_spans']
 assert set(spans)==set(p11.GUESTS),'P27_GUEST_SPAN_SET'
 routes=scope['route_junctions']
 assert set(p11.GUESTS)<set(routes) and all(j==(gj if k in p11.GUESTS else sj)for k,j in routes.items()),'P27_ROUTE_JUNCTION'
 guest_rows={i for lo,hi in spans.values()for i in range(lo,hi)}
 assert guest_rows and all(base['row_metadata'][i]['group']=='rooted_body_network'for i in guest_rows),'P27_GUEST_ROW_SOURCE'
 for name in ('objective','integrality'):
  assert np.array_equal(np.delete(guest[name][:n+1],gj),base[name]),'P27_LEGACY_VECTOR'
 for name in ('lb','ub'):
  assert np.array_equal(np.delete(getattr(guest['bounds'],name)[:n+1],gj),getattr(base['bounds'],name)),'P27_LEGACY_VAR_BOUNDS'
 for name in ('lower','upper'):
  assert np.array_equal(guest[name][:m],base[name]),'P27_LEGACY_ROW_BOUNDS'
 a,b=base['matrix'],guest['matrix']
 touched=0
 for i in range(m):
  x,y=a.indptr[i:i+2];u,v=b.indptr[i:i+2]
  expected={}
  for j,val in zip(a.indices[x:y],a.data[x:y]):
   k=gj if i in guest_rows and j==sj else j+(j>=gj)
   if k==gj:touched+=1
   expected[k]=val
  assert dict(zip(b.indices[u:v],b.data[u:v]))==expected,'P27_LEGACY_CSR'
  assert base['row_metadata'][i]['group']==guest['row_metadata'][i]['group'],'P27_LEGACY_ROW_ROLE'
 assert touched>0 and base['specs']==guest['specs'],'P27_GUEST_REMAP_AND_SPECS'
 groups=Counter(x['group'] for x in guest['row_metadata'][m:])
 assert groups['p27_guest_root_retained_motion']==30,'P27_GUEST_SIX_MOTIONS'
 blocks=scope['panel_blocks']
 assert Counter(k for k,_ in blocks)=={'common_guest_root':1,'dining_east':3,'sofa1_use':3},'P27_PANEL_EXACT_SEGMENTS'
 assert [i for _,i in blocks]==list(range(b.shape[0]-35,b.shape[0],5)),'P27_PANEL_APPEND'
 assert sum(n for k,n in groups.items()if k.startswith('p27_guest_panel_'))==35,'P27_PANEL_ROW_COUNT'
 for route,i in blocks:
  assert all(x['group']=='p27_guest_panel_'+route for x in guest['row_metadata'][i:i+5]),'P27_PANEL_GROUP'
  u,v=b.indptr[i:i+2];bits=list(b.indices[u:v])
  assert len(bits)==4 and min(bits)>=scope['old_var_end'] and all(guest['integrality'][j]==1 for j in bits),'P27_PANEL_SWITCHES'
 return {'old_rows':m,'old_vars':n,'new_rows':b.shape[0],'new_vars':b.shape[1],
         'guest_junction_coefficients_remapped':touched,'panel_segments':len(blocks),'panel_rows':35,'optimizer_calls':0}

def fixture():
 core,_=selected_core(new.RAW,'FRONT_REAR_COMPACT118')
 x=prior.PlannedTests().contract()
 src=p11.entry_source(core);a,b=map(F,src['root']);length=F(src['length'])
 x.update(raw=copy.deepcopy(new.RAW),core_digest=digest(core),enabled_causes=['PLANNED_ENTRY_PANEL_AND_KITCHEN_MOTION'],
  entry_source_binding={'schema':'ACTUAL_SOURCE_ENTRY_PANEL_BINDING108_V1','local_panel':src['local_panel'],
   'units':[{'unit':uid,'operation_digest':digest(op),'root_digest':digest([str(a),str(y)]),'root_body_clear':True}
     for uid,y,op in zip(('A','B'),(b,length-b),src['operations'])]})
 return core,contract.candidate_contract(x)

class GuestTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  assert support.source_guard()
  cls.core,cls.operator=fixture()
  with patch.object(old,'milp',side_effect=AssertionError('NO_MILP')) as a,patch.object(new,'milp',side_effect=AssertionError('NO_MILP'))as b,patch.object(opt,'milp',side_effect=AssertionError('NO_MILP'))as c,patch.object(scipy_milp,'milp',side_effect=AssertionError('NO_MILP'))as d:
   before=digest([cls.core,cls.operator])
   opts=dict(time_limit=30,variant=0,sleep_roles=['double','twin'],parent_contract=cls.operator,enabled_causes=cls.operator['enabled_causes'],diagnostic_capture=lambda x:x)
   cls.base=old.propose(cls.core,2,**opts);cls.guest=new.propose(cls.core,2,**opts)
   assert digest([cls.core,cls.operator])==before
   for fn in (a,b,c,d):fn.assert_not_called()
 def test_exact_preserved_matrix(self):self.assertEqual(verify_capture(self.base,self.guest)['panel_segments'],7)
 def test_serving_route_cannot_use_guest_junction(self):
  bad={**self.guest,'p27_scope':copy.deepcopy(self.guest['p27_scope'])};s=bad['p27_scope'];k=next(k for k in s['route_junctions']if k not in p11.GUESTS);s['route_junctions'][k]=s['guest_junction']
  with self.assertRaisesRegex(AssertionError,'P27_ROUTE_JUNCTION'):verify_capture(self.base,bad)
 def test_motion_row_cannot_be_dropped(self):
  bad={**self.guest,'row_metadata':copy.deepcopy(self.guest['row_metadata'])}
  next(r for r in bad['row_metadata']if r['group']=='p27_guest_root_retained_motion')['group']='OTHER'
  with self.assertRaisesRegex(AssertionError,'P27_GUEST_SIX_MOTIONS'):verify_capture(self.base,bad)
 def test_preserved_coefficient_cannot_be_rewritten(self):
  bad={**self.guest,'matrix':self.guest['matrix'].copy()};bad['matrix'].data[0]+=1
  with self.assertRaisesRegex(AssertionError,'P27_LEGACY_CSR'):verify_capture(self.base,bad)
 def test_entry_and_request_semantics_are_not_just_hash_scope(self):
  for field,err in (('core','ENTRY_RESERVATION_CORE'),('raw','P27_GUEST_EXACT_REQUEST'),('root','P27_GUEST_ENTRY_BINDING'),('operation','P27_GUEST_ENTRY_BINDING'),('panel','P27_GUEST_ENTRY_BINDING')):
   o=copy.deepcopy(self.operator)
   if field=='core':o['core_digest']='0'*64
   elif field=='raw':o['raw']['n']=2.0
   elif field in ('root','operation'):o['entry_panel_reservation']['units'][1][field+'_digest']='0'*64
   else:o['entry_panel_reservation']['local_panel'][0]='0'
   with self.assertRaisesRegex(ValueError,err):new.bound_entry(o,self.core)
 def test_guest_panel_block_cannot_be_relabelled_as_serving(self):
  bad={**self.guest,'row_metadata':copy.deepcopy(self.guest['row_metadata'])}
  next(r for r in bad['row_metadata']if r['group']=='p27_guest_panel_common_guest_root')['group']='p27_serving_panel'
  with self.assertRaisesRegex(AssertionError,'P27_PANEL_ROW_COUNT'):verify_capture(self.base,bad)

if __name__=='__main__':unittest.main()
