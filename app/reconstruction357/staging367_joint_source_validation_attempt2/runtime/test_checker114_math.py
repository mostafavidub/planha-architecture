import unittest
from checker114 import rect,covered,sweeps,intersects
class Geometry(unittest.TestCase):
 def test_hole(self):
  h=list(map(rect,[[0,0,3,1],[0,2,3,3],[0,1,1,2],[2,1,3,2]]))
  self.assertFalse(covered(rect([0,0,3,3]),h))
  self.assertTrue(covered(rect([0,0,1,3]),h))
 def test_partition(self):
  self.assertTrue(covered(rect([0,0,2,2]),list(map(rect,[[0,0,1,2],[1,0,2,2]]))))
 def test_corner(self):
  ss=sweeps([[0,0],[1,0],[1,1]])
  self.assertTrue(any(intersects(q,rect([1.1,-.3,1.2,-.2])) for q in ss))
 def test_tangent(self):
  self.assertFalse(intersects(rect([0,0,1,1]),rect([1,0,2,1])))
 def test_diagonal(self):
  with self.assertRaises(ValueError):sweeps([[0,0],[1,1]])
if __name__=='__main__':unittest.main()
