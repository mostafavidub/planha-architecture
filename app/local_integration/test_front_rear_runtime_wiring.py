"""Task2.3 smoke only: never invoke runtime.run or solver."""
import ast,unittest
from pathlib import Path
import front_rear_runtime_adapter as a
class WiringSmoke(unittest.TestCase):
 def test_compile_and_selected_chain(self):
  tree=ast.parse(Path(a.__file__).read_text())
  calls={ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call)}
  for name in ('verify_public','bind_request','constructor127.frame','search114.propose','constructor127.build','constructor127.context','construction_replay127.verify','evaluate_pair127.evaluate','functional_review.assess'):
   self.assertIn(name,calls)
  self.assertNotIn('constructor129.build',calls)
 def test_basic_tuple_boundary(self):
  value={'a':(1,'1',2.0,False,None)}
  out,r=a.transport(value)
  self.assertEqual(r['tuple_paths'],[['a']]);self.assertEqual(r['before_digest'],r['after_digest'])
  self.assertIs(type(out['a'][0]),int);self.assertIs(type(out['a'][2]),float);self.assertIs(type(out['a'][3]),bool)
 def test_reports_stable(self):
  reports={'physical':{'errors':['x'],'pending':['y'],'original_pending':['z'],'not_evaluated':['q'],'out_of_scope':[{'a':1}]}}
  pins={k:a.digest(v) for k,v in reports.items()}
  a.verify_reports(reports,pins)
  self.assertEqual(reports['physical']['errors'],['x'])
 def test_no_module_top_level_live_call(self):
  tree=ast.parse(Path(a.__file__).read_text())
  for n in tree.body:
   if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):
    self.assertNotIn(ast.unparse(n.value.func),('run','search114.propose','constructor127.build'))
if __name__=='__main__':unittest.main()
