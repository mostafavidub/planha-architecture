import unittest,sys,json,copy
from pathlib import Path
from fractions import Fraction as F
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'planha_general150_runtime_work'))
from core_variant364 import core
from entry364 import install
class Tests(unittest.TestCase):
 def setUp(self):self.record=json.loads((B/'staging362_core_notch/actual362.json').read_text());self.old=self.record['candidate']['packet']['core'];self.new=core(F(26),F(28))
 def test_assets_ownership_unchanged(self):
  for k in('stair','lift','lobby','unit_ownership','units','core_extent_x','notch362'):self.assertEqual(self.old[k],self.new[k])
 def test_derived_parameters(self):
  p=self.new['balanced_portals364'];self.assertEqual(p['portal_y'],{'stair':'13.875','lift':'14.125'});self.assertEqual(self.new['entry_centers']['A'][0],'14.075');self.assertEqual(self.new['entry_centers']['B'],self.old['entry_centers']['B'])
 def fixture(self):
  m=copy.deepcopy(self.record['candidate']['model']);m['openings']=[o for o in m['openings']if o['id']in('A.entry','B.entry')];m['operations']={}
  for o in m['openings']:
   if o['id']=='A.entry':o['rect'][0]='13.425';o['rect'][2]='14.725'
  return m
 def test_reverse_rigid_and_actor(self):
  m=self.fixture();install(m,{'A':-1,'B':1});op=m['operations']['doors'][0];self.assertEqual(op['translation'],['-1.3','0']);self.assertEqual(op['rail_envelope'][0],'12.125');self.assertEqual(op['rail_envelope'][2],'14.725')
  for s in op['states']:
   r=list(map(F,s['actor_rect']));self.assertGreaterEqual(r[0],F('13.125'));self.assertLessEqual(r[2],F('15.775'))
   closed=list(map(F,op['closed_panel']));delta=list(map(F,op['translation']));self.assertEqual(list(map(F,s['panel_rect'])),[closed[i]+F(s['fraction'])*delta[i%2]for i in range(4)])
 def test_missing_direction(self):self.assertRaises(ValueError,install,self.fixture(),{'A':-1})
 def test_boolean_direction(self):self.assertRaises(ValueError,install,self.fixture(),{'A':True,'B':1})
 def test_positive_shift_has_rail_conflict(self):
  m=self.fixture();install(m,{'A':1,'B':1});self.assertGreater(F(m['operations']['doors'][0]['rail_envelope'][2]),F(m['wall_hosts']['A.unit_boundary'][2]))
 def test_explicit_tradeoff(self):
  p=self.new['balanced_portals364'];self.assertEqual(p['metric_policy'],'INDEPENDENT_CANDIDATE_EXPLICIT_TRADEOFF_NOT_PARETO_REPAIR');self.assertFalse(p['accepted'])
if __name__=='__main__':unittest.main()
