import unittest,copy
from final_route_ledger120 import evaluate
class Ledger(unittest.TestCase):
 def setUp(self):
  self.m={'profile':{'body_m':'.7'},'walls':{},'units':[{'id':'A','ownership':[['0','0','3','2']],'rooms':{'entry_circulation':[['0','0','3','.7']],'living':[['0','.7','3','2']]},'routes':{'access':[['.35','.35'],['2.65','.35']]},'scenario_routes':{}}]}
 def test_exact(self):self.assertEqual(evaluate(self.m)['status'],'PASS_LIMITED')
 def test_stale_reroute(self):
  self.m['units'][0]['routes']['access']=[['.35','1.65'],['2.65','1.65']];self.assertEqual(evaluate(self.m)['status'],'FAIL')
 def test_relabel_only(self):
  u=self.m['units'][0];u['rooms']['living']+=u['rooms']['entry_circulation'];u['rooms']['entry_circulation']=[];self.assertEqual(evaluate(self.m)['status'],'FAIL')
 def test_missing_coverage(self):
  self.m['units'][0]['rooms']['living']=[];self.assertEqual(evaluate(self.m)['status'],'FAIL')
 def test_scenario_added(self):
  self.m['units'][0]['scenario_routes']['guest']=[['.35','1.65'],['2.65','1.65']];self.assertEqual(evaluate(self.m)['status'],'FAIL')
 def test_partition_equivalent(self):
  self.m['units'][0]['rooms']['entry_circulation']=[['0','0','1','.7'],['1','0','3','.7']];self.assertEqual(evaluate(self.m)['status'],'PASS_LIMITED')
if __name__=='__main__':unittest.main()
