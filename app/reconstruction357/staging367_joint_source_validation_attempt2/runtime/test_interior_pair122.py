import unittest,copy
from paired_private_zone118 import examine

def fixture():
 return {'inputs':['8','10',2],'profile':{'body_m':'.7'},'wall_hosts':{'service.back':['1','1','5','1.15'],'l':['2','1','2.15','5'],'r':['3.15','1','3.3','5']},'walls':{'service.back':['1','1','5','1.15'],'l.low':['2','1','2.15','2'],'l.high':['2','3','2.15','5'],'r.low':['3.15','1','3.3','2'],'r.high':['3.15','3','3.3','5']},'openings':[{'id':'A.bed1.entry','rect':['2','2','2.15','3'],'host_wall_id':'l','connects':['A.bed1','A.public_access']},{'id':'A.bed2.entry','rect':['3.15','2','3.3','3'],'host_wall_id':'r','connects':['A.bed2','A.public_access']}],'units':[{'id':'A','rooms':{'bed1':[['.2','1.15','2','5']],'bed2':[['3.3','1.15','5','5']],'entry_circulation':[['2.15','1.15','3.15','6']]},'fixtures':{},'routes':{},'scenario_routes':{k:[['6','6'],['7','6']]for k in ('guest_living','guest_dining','kitchen_to_dining_floor')}}]}
class Interior(unittest.TestCase):
 def passed(self,m):return [z for z in examine(m)['zones']if z['status']=='PASS_TWO_BEDROOM_PRIVATE_APPROACH_TOPOLOGY']
 def test_actual_interior_closed_host(self):
  z=self.passed(fixture());self.assertEqual(len(z),1);self.assertEqual(z[0]['closed_end_host_id'],'service.back');self.assertEqual(z[0]['zone'][1],'23/20')
 def test_island_host_only_not_wall(self):
  m=fixture();del m['walls']['service.back'];self.assertFalse(self.passed(m))
 def test_cap_gap(self):
  m=fixture();m['walls']['service.back']=['1','1','2.5','1.15'];self.assertFalse(self.passed(m))
 def test_added_opening_even_with_fake_solid(self):
  m=fixture();m['openings'].append({'id':'fake','rect':['2.5','1','2.8','1.15'],'connects':['x','y']});self.assertFalse(self.passed(m))
 def test_guest_through_domain(self):
  m=fixture();m['units'][0]['scenario_routes']['guest_living']=[['2.65','2'],['2.65','6']];self.assertFalse(self.passed(m))
 def test_body_obstacle(self):
  m=fixture();m['units'][0]['fixtures']['table']=['2.2','2','3','3'];self.assertFalse(self.passed(m))
 def test_side_extra_opening(self):
  m=fixture();m['openings'].append({'id':'other','rect':['2','4','2.15','4.5'],'connects':['x','y']});self.assertFalse(self.passed(m))
if __name__=='__main__':unittest.main()
