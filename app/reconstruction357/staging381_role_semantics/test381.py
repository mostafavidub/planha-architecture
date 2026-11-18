import unittest,sys,copy,ast,types
from unittest.mock import patch
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;sys.path[:0]=[str(H),str(R/'semantic_rules357'),str(R/'staging378_finite_portals')]
import gate381 as g
class Tests(unittest.TestCase):
 def setUp(self):self.i=g.load_inputs()
 def test_current379_binding(self):self.assertEqual(g.validate(**self.i)['run_id'],'02dc5f92-93b6-4466-be6c-5114e96bc636')
 def test_prior378_rejected(self):
  import json
  old=Path('independent378actual/evidence/review378_actual_v1')
  with self.assertRaises(ValueError):g.validate(json.loads((old/'record.json').read_text()),json.loads((old/'fresh.json').read_text()))
 def test_model_tamper(self):
  self.i['record']['candidate']['model']['inputs'][0]='27'
  with self.assertRaises(ValueError):g.validate(**self.i)
 def test_exact_rank1_selection(self):
  from entry_separation381 import require_registered_selection
  p=self.i['record']['candidate']['packet']['core']['balanced_portals365'];lo,hi,x=require_registered_selection(p);self.assertTrue(lo<x<hi);self.assertNotEqual(x,(lo+hi)/2)
  for field,value in [('finite_rank378',0),('entry_x',{'A':'15.05','B':'13.825'}),('slide_direction',{'A':1,'B':1})]:
   q=copy.deepcopy(p);q[field]=value
   with self.assertRaises(ValueError):require_registered_selection(q)
 def test_midpoint_policy_rejected(self):
  from entry_separation381 import require_registered_selection
  p=copy.deepcopy(self.i['record']['candidate']['packet']['core']['balanced_portals365']);p['selection']='MIDPOINT_MAXIMIZES_MIN_COORDINATE_SLACK_WITHIN_WIDEST_FEASIBLE_COMPONENT'
  with self.assertRaises(ValueError):require_registered_selection(p)
 def test_unequal_balance_not_pass(self):
  import balanced_access381 as b
  sys.path.insert(0,str(R/'balance363'));import assessor
  def mockroute(m,k):return {'route_id':k,'length_m':'1'if k.endswith('_A')else'2','turns':1,'fully_open_entry_passage_square_capacity':{'max_axis_aligned_square_width_m':'.7'},'unassessed':[]}
  required={k:{'status':'PASS_LIMITED'}for k in('core_concept','door_operation','opening_hosts','wall_network','partition_ledger')}
  with patch.object(b,'build',return_value={}),patch.object(b,'rows',return_value=required),patch.object(assessor,'model_route',side_effect=mockroute):
   out=b.evaluate(self.i['record'],self.i['fresh']);self.assertEqual(out['verdict'],'UNKNOWN_BALANCE_NOT_ESTABLISHED');self.assertFalse(any(x['equal_fixed_source_metrics']for x in out['comparisons']))
 def test_no_candidate_optimization(self):
  for p in H.glob('*.py'):
   if p.name.startswith('test'):continue
   for node in ast.walk(ast.parse(p.read_text())):
    if isinstance(node,ast.ImportFrom):self.assertNotIn(node.module,('source378','evaluate378','checker114','constructor378'))
 def test_rank2_not_silently_excluded(self):self.assertIn('UNASSESSED_NO_MODEL_NO_FRESH_NO_DOMINANCE_PROOF',(H/'cohort381.py').read_text())
 def test_origin_reject(self):
  from adapters381 import load
  with patch.dict(sys.modules,{'groups381':types.SimpleNamespace(__file__='/tmp/forged.py')}):
   with self.assertRaisesRegex(ValueError,'SEMANTIC_MODULE_ORIGIN'):load('group_readsets365_v2')
if __name__=='__main__':unittest.main()
