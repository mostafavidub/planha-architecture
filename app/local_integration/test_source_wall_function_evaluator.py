import unittest,sys
from fractions import Fraction as F
from front_rear_runtime_adapter import ENGINE
sys.path.insert(0,str(ENGINE))
from source_wall_counterfactual import interval_difference,exact_closure_change
from current_programme_evaluator import placed
from geometry114 import cells
class WallTests(unittest.TestCase):
 def test_split_intervals(self):
  self.assertEqual(interval_difference([(0,10)],[(2,4),(6,8)]),[(F(0),F(2)),(F(4),F(6)),(F(8),F(10))])
 def test_overlap_and_outside(self):
  self.assertEqual(interval_difference([(0,10)],[(-1,3),(2,7),(9,12)]),[(F(7),F(9))])
 def test_existing_gap_grows(self):
  region=[tuple(map(F,[0,0,2,2]))]
  old=[tuple(map(F,[-1,0,0,1]))];new=[]
  rows=exact_closure_change(region,old,new,[])
  r=next(z for z in rows if z['edge'][0]=='0' and z['edge'][1]=='False')
  self.assertEqual(r['before_missing'],[['1','2']]);self.assertEqual(r['newly_missing'],[['0','1']])
 def test_aperture_retained(self):
  region=[tuple(map(F,[0,0,2,2]))];wall=[tuple(map(F,[-1,0,0,2]))]
  r=exact_closure_change(region,wall,[],[tuple(map(F,[-1,0,1,2]))])
  self.assertFalse(any(z['newly_missing'] for z in r))
 def test_duplicate_source_no_material(self):
  q=['0','0','2','1'];self.assertEqual(cells([q,q],[q]),[])
 def test_partial_alias_unique_material(self):
  self.assertEqual(sum((F(q[2])-F(q[0]))*(F(q[3])-F(q[1])) for q in cells([[0,0,2,1],[1,0,3,1]],[[1,0,3,1]])),F(1))
 def test_nonrigid_rejected(self):
  with self.assertRaises(ValueError):placed([0,0,1,1],{'matrix':[[.5,.5],[.5,.5]],'translation':[0,0]})
 def test_boolean_rotation_rejected(self):
  with self.assertRaises(ValueError):placed([0,0,1,1],{'matrix':[[True,0],[0,1]],'translation':[0,0]})
 def test_reflection_exact(self):
  self.assertEqual(placed([0,0,1,2],{'matrix':[[-1,0],[0,1]],'translation':[3,4]}),list(map(F,[2,4,3,6])))
if __name__=='__main__':unittest.main()
