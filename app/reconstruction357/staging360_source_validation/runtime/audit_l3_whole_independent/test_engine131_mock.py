import sys,unittest,copy,hashlib,json
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P));import engine131 as e
RAW={'W':'37.45','L':'19.97','n':2,'requested_count':6}
GOOD={'status':'PASS_CONCEPT_SCOPED_REVIEW','gate_scope':'CONCEPT117_SOURCE_COMPAT_V1','errors':[],'pending':[],'eligible_for_draft_export':True}
class Clock:
 def __init__(self):self.t=0
 def __call__(self):return self.t
class Tests(unittest.TestCase):
 def flow(self,gate=None,budget=26,validation=0,solve=0,revision=None):
  calls=[];clock=Clock();fallback=[]
  def prop(kind,c,t):calls.append((kind,c,t));clock.t+=solve;return {'status':'PROPOSAL_ONLY','kind':kind}
  def build(raw,family,p):return {'world_model':{'kind':p['kind'],'family':family}}
  def evaluate(*a,**kw):clock.t+=validation;return copy.deepcopy(gate or GOOD)
  def lower(raw,**kw):fallback.append(kw['budget']);return {'attempts':[],'internal_proposals':[],'candidates':[],'search_seconds':0,'assembly_seconds':0,'validation_seconds':0,'full_gate_calls':0}
  with ExitStack()as s:
   for name,value in [('frame',lambda raw,f:(f,None)),('propose_l3',lambda c,t:prop('L3',c,t)),('propose',lambda c,t:prop('ROW',c,t)),('build',build),('context',lambda *a:{}),('evaluate_current',evaluate),('select_scoped',lambda cs,n:(cs[:n],{}))]:s.enter_context(patch.object(e,name,value))
   s.enter_context(patch.object(e,'revision',revision or(lambda:'fixed')));s.enter_context(patch.object(e.time,'monotonic',clock));s.enter_context(patch('engine127.run',lower));r=e.runtime(RAW,budget)
  return r,calls,fallback
 def test_dispatch(self):
  r,c,f=self.flow();self.assertEqual([(a,b)for a,b,_ in c],[('L3','LEFT_RIGHT'),('ROW','FRONT_REAR'),('ROW','LEFT_RIGHT')]);self.assertEqual(len(r['admitted_pool']),3);self.assertFalse(f);self.assertTrue(all(t==3 for _,_,t in c))
 def test_failed_gate_not_admitted(self):
  for bad in(dict(GOOD,errors=['x']),dict(GOOD,pending=['x']),dict(GOOD,status='FAIL'),dict(GOOD,eligible_for_draft_export=False)):
   r,c,f=self.flow(bad);self.assertEqual(r['admitted_pool'],[]);self.assertEqual(len(f),1)
 def test_validation_checkpoint(self):
  r,c,f=self.flow(validation=501);self.assertEqual(len(c),1);self.assertEqual([x['status']for x in r['attempts'][1:]],['NOT_ATTEMPTED_BUDGET_CHECKPOINT']*2)
 def test_search_checkpoint(self):
  r,c,f=self.flow(solve=3,budget=3);self.assertEqual(len(c),1)
 def test_zero_budget(self):
  r,c,f=self.flow(budget=0);self.assertEqual(c,[]);self.assertEqual(f,[])
 def test_total_checkpoint(self):
  # In-flight work may finish beyond checkpoint; no further starts.
  r,c,f=self.flow(validation=601);self.assertEqual(len(c),1)
 def test_revision_change(self):
  vals=iter(['a','b'])
  with self.assertRaisesRegex(ValueError,'SOURCE_CHANGED'):self.flow(revision=lambda:next(vals))
 def test_input_boundary(self):
  for raw in [dict(RAW,program=1),dict(RAW,n=1),dict(RAW,requested_count=0),dict(RAW,requested_count=13),dict(RAW,W='4.99'),dict(RAW,L='45.01')]:
   with patch.object(e,'frame',side_effect=AssertionError('must not dispatch')):
    with self.assertRaises(ValueError):e.runtime(raw)
  for v in ('5','45','5.001','44.999'):e.validate_raw(dict(RAW,W=v,L=v))
 def test_same_program_selection(self):
  import program_selection130 as s
  def candidate(kind,roles):return {'kind':kind,'model':{'units':[{'id':'A'}],'program':{'sleep_roles':roles,'bedrooms_per_unit':len(roles)}},'gate':GOOD}
  cs=[candidate('L3',['twin','twin','double']),candidate('ROW',['double','twin','twin']),candidate('LOW',['double'])]
  def describe(c):
   roles=sorted(c['model']['program']['sleep_roles']);return {'program_key':str(roles),'kind':c['kind'],'source_witness':{'source_rooms':[{'unit':'A','functional_label':'bedroom:'+r}for r in roles]}}
  with patch.object(s,'describe',describe),patch.object(s,'compare',lambda a,b:{'distinct':a['kind']!=b['kind']}),patch('quality_tradeoffs129.facts',lambda m:{}),patch('quality_tradeoffs129.rank',lambda m:0):
   r=s.select(cs,6);self.assertEqual(r['selected_indices'],[0,1]);self.assertEqual(r['selected_sleep_roles'],['double','twin','twin'])
   bad=copy.deepcopy(cs);bad[0]['gate']=dict(GOOD,pending=['x']);self.assertEqual(s.select(bad,6)['selected_indices'],[1])
if __name__=='__main__':unittest.main()
