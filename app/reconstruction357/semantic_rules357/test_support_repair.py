import unittest
from source_support_repair import diagnose
class Repair(unittest.TestCase):
 def model(self):return {'profile':{'body_m':'.7'},'walls':{'w':['0','0','4','.2']},'units':[{'id':'A','fixtures':{'sofa1':['1','.5','3','1.4']},'activities':{'sofa1_front':['1','1.4','3','2.1']},'routes':{},'scenario_routes':{}}]}
 def test_positive(self):self.assertEqual(diagnose(self.model())[0]['gap_m'],'3/10')
 def test_zero(self):
  m=self.model();m['walls']['w'][3]='.5';self.assertEqual(diagnose(m),[])
 def test_body_passable(self):
  m=self.model();m['walls']['w']=['0','-1','4','-.2'];self.assertEqual(diagnose(m),[])
 def test_partial_wall(self):
  m=self.model();m['walls']['w'][2]='2';self.assertEqual(diagnose(m),[])
 def test_activity(self):
  m=self.model();m['units'][0]['activities']['real']=['1','.2','2','.5'];self.assertEqual(diagnose(m)[0]['verdict'],'INELIGIBLE_DECLARED_USE_IN_GAP')
 def test_door_actor(self):
  m=self.model();m['operations']={'doors':[{'states':[{'unit':'A','actor_rect':['1','.2','2','.5']}]}]};self.assertEqual(diagnose(m)[0]['verdict'],'INELIGIBLE_DECLARED_USE_IN_GAP')
if __name__=='__main__':unittest.main()
