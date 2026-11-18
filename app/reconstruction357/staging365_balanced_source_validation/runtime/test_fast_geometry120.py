"""Exact equivalence against frozen pre-optimization algorithm, not plan admission."""
import unittest,types,random
from pathlib import Path
from fast_cells120 import cells
from fast_route120 import route
p=Path(__file__).parent/'references/geometry_reference119.py.txt'
old=types.ModuleType('geometry_reference119');exec(compile(p.read_text(),str(p),'exec'),old.__dict__)
class ExactGeometry(unittest.TestCase):
 def test_210_seeded_and_boundary_equalities(self):
  rng=random.Random(120);count=0
  for _ in range(120):
   rects=[]
   for j in range(12):
    x=rng.randrange(-10,40)/10;y=rng.randrange(-10,40)/10;w=rng.randrange(1,20)/10;h=rng.randrange(1,20)/10;rects.append([str(x),str(y),str(x+w),str(y+h)])
   g=rects[:3];sub=rects[3:];assert old.cells(g,sub)==cells(g,sub);count+=1
  for _ in range(80):
   obstacles=[]
   for j in range(4):
    x=rng.randrange(1,35)/10;y=rng.randrange(1,35)/10;obstacles.append([str(x),str(y),str(x+.3),str(y+.4)])
   args=(['.5','.5'],['3.5','3.5'],['0','0','4','4'],obstacles)
   assert old.route(*args)==route(*args);count+=1
  # Precision beyond floats, boundary contacts, blocked endpoint, zero obstacle, node budget
  for obs in [[],[['1/3','0','2/3','4']],[['1','1','1','2']],[['.1','.1','.9','.9']], [['1.0000000000000000000001','1','2','2']]]:
   args=(['.5','.5'],['3.5','3.5'],['0','0','4','4'],obs)
   for budget in [1,18000]:assert old.route(*args,max_nodes=budget)==route(*args,max_nodes=budget);count+=1
  self.assertEqual(count,210)
