import unittest
from checker114 import rect,F
from operation_check114 import continuous_hit,segment_check
class ExactMotion(unittest.TestCase):
 def test_between_endpoints_collision(self):
  a=rect([0,0,.7,.7]);b=rect([2,0,2.7,.7]);o=rect([1,0,1.1,.7]);self.assertTrue(continuous_hit(a,b,o,o))
 def test_tangency_allowed(self):
  a=rect([0,0,.7,.7]);b=rect([2,0,2.7,.7]);o=rect([1,.7,1.1,1]);self.assertFalse(continuous_hit(a,b,o,o))
 def test_two_moving_cross(self):
  self.assertTrue(continuous_hit(rect([0,0,1,1]),rect([2,0,3,1]),rect([2,0,3,1]),rect([0,0,1,1])))
 def test_hole_reject(self):
  seg={'actor_start':[0,0,.7,.7],'actor_end':[2,0,2.7,.7],'t0':0,'t1':1,'hand_start':[0,1],'hand_end':[2,1]}
  out=segment_check(seg,rect([0,1,1,1.1]),(F(2),F(0)),[rect([0,0,1,2]),rect([2,0,3,2])],[])
  self.assertIn('CONTINUOUS_ACTOR_OUTSIDE_FLOOR',out)
 def test_real_continuous_grip(self):
  seg={'actor_start':[0,0,.7,.7],'actor_end':[1,0,1.7,.7],'t0':0,'t1':1,'hand_start':[.5,1],'hand_end':[1.5,1]}
  self.assertEqual(segment_check(seg,rect([0,1,1,1.1]),(F(1),F(0)),[rect([0,0,3,2])],[]),[])
 def test_actor_collision_between_safe_states(self):
  seg={'actor_start':[0,0,.7,.7],'actor_end':[2,0,2.7,.7],'t0':0,'t1':1,'hand_start':[.5,1],'hand_end':[2.5,1]}
  r=segment_check(seg,rect([0,1,1,1.1]),(F(2),F(0)),[rect([0,0,3,2])],[rect([1,0,1.1,.7])])
  self.assertIn('CONTINUOUS_ACTOR_OBSTACLE_COLLISION',r)
 def test_fake_grip_rejected(self):
  seg={'actor_start':[0,0,.7,.7],'actor_end':[1,0,1.7,.7],'t0':0,'t1':1,'hand_start':[.5,1],'hand_end':[1.6,1]}
  r=segment_check(seg,rect([0,1,1,1.1]),(F(1),F(0)),[rect([0,0,3,2])],[])
  self.assertIn('HANDLE_NOT_RIGIDLY_BOUND_TO_PANEL',r)
if __name__=='__main__':unittest.main()
