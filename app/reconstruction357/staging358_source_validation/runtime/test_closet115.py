import unittest,copy
from checker114 import rect
from operation_check114 import check_closets
class ClosetProof(unittest.TestCase):
 def sample(self):
  ps=[]
  for x,y,d in [('.02','0','1.025'),('.08','1.025','-1.025')]:
   from fractions import Fraction as F
   x,y,d=map(F,(x,y,d));a=[x,y,x+F('.04'),y+F('1.025')];b=[a[0],a[1]+d,a[2],a[3]+d]
   ps.append({'closed_panel':list(map(str,a)),'open_panel':list(map(str,b)),'translation':['0',str(d)],'rail_envelope':[str(x),'0',str(x+F('.04')),'2.05'],'states':[],'continuous_actor_segments':[]})
  c={'unit':'A','fixture_id':'closet','front_axis':'x','front_side':'min','panels':ps,'assumption':'Unapproved hypothetical hardware','shell_rects':[]}
  m={'units':[{'id':'A','fixtures':{'closet':[0,0,.6,2.05]},'fixture_metadata':{'closet':{'kind':'closet'}}}],'operations':{'closets':[c]}}
  return m
 def test_two_halves_without_actor_not_pass(self):
  e,p=check_closets(self.sample(),{'A':[rect([-2,0,1,3])]}, {}, [('A','closet',rect([0,0,.6,2.05]))])
  self.assertEqual(e,[]);self.assertTrue(p)
 def test_panel_resize_reject(self):
  m=self.sample();m['operations']['closets'][0]['panels'][0]['closed_panel'][2]='.07'
  e,p=check_closets(m,{'A':[rect([-2,0,1,3])]}, {}, [('A','closet',rect([0,0,.6,2.05]))])
  self.assertIn('CLOSET_STUDY_PANEL_THICKNESS',[x['code']for x in e])
 def test_missing_half_reject(self):
  m=self.sample();m['operations']['closets'][0]['panels'].pop()
  e,p=check_closets(m,{}, {}, [('A','closet',rect([0,0,.6,2.05]))])
  self.assertIn('CLOSET_TWO_HALF_PANELS_REQUIRED',[x['code']for x in e])
if __name__=='__main__':unittest.main()
