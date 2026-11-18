import unittest,time
from fractions import Fraction as F
import bedroom_route_witness358 as w
class Tests(unittest.TestCase):
 def test_join_no_new_edge(self):
  a=[['0','0'],['1','0']];b=[['0','0'],['0','2']];self.assertEqual(w.via_entry(a,b),[['1','0'],['0','0'],['0','2']])
 def test_wrong_root(self):
  with self.assertRaises(ValueError):w.via_entry([['0','0'],['1','0']],[['1','0'],['1','1']])
 def test_obstacle_not_dropped(self):
  x=w.check_leg([['1','1'],['3','1']],F('.7'),[(F(0),F(0),F(4),F(4))],[('otherbed',(F(2),F(0),F(3),F(2)))],time.monotonic()+1)
  self.assertEqual(x['verdict'],'UNKNOWN_STORED_PATH_BLOCKED_NOT_INFEASIBLE');self.assertTrue(x['collisions'])
 def test_floor_gap(self):
  x=w.check_leg([['1','1'],['3','1']],F('.7'),[(F(0),F(0),F(2),F(4))],[],time.monotonic()+1);self.assertTrue(x['uncovered'])
 def test_clear_path(self):
  x=w.check_leg([['1','1'],['3','1']],F('.7'),[(F(0),F(0),F(4),F(4))],[],time.monotonic()+1);self.assertEqual(x['verdict'],'PASS_SCOPED_TASK_PATH')
if __name__=='__main__':unittest.main()
