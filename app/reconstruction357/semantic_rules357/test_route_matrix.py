import unittest
from fractions import Fraction as F
from route_matrix import graph,distance
class Routes(unittest.TestCase):
 def test_crossing(self):
  g=graph([[[0,1],[2,1]],[[1,0],[1,2]]]);self.assertEqual(distance(g,(F(0),F(1)),(F(1),F(2))),2)
 def test_collinear(self):
  g=graph([[[0,0],[2,0]],[[1,0],[3,0]]]);self.assertEqual(distance(g,(F(0),F(0)),(F(3),F(0))),3)
 def test_disconnected(self):
  g=graph([[[0,0],[1,0]],[[2,0],[3,0]]]);self.assertIsNone(distance(g,(F(0),F(0)),(F(3),F(0))))
 def test_diagonal(self):
  with self.assertRaisesRegex(ValueError,'ORTHOGONAL'):graph([[[0,0],[1,1]]])
if __name__=='__main__':unittest.main()
