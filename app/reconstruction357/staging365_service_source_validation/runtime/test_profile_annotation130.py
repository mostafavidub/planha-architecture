"""Light record-profile tests only; no rebuild, gate or geometry admission."""
import unittest,json
from pathlib import Path
R=Path(__file__).parent
class T(unittest.TestCase):
 def setUp(self):self.records=json.loads((R/'world_record_schema129.json').read_text())['records']['root']
 def test_onebed_profile(self):
  root=next(set(k)for k in self.records if 'private_domains'not in k and 'ordered_macro_coordinate_frame'not in k)
  self.assertIn(sorted(root),self.records)
  self.assertNotIn(sorted(root|{'ordered_macro_coordinate_frame'}),self.records)
 def test_threebed_profile(self):
  root=next(set(k)for k in self.records if 'private_domains'in k and 'ordered_macro_coordinate_frame'not in k)
  self.assertIn(sorted(root|{'ordered_macro_coordinate_frame'}),self.records)
  self.assertNotIn(sorted(root|{'unknown_geometry'}),self.records)
 def test_fixed_producer_is_conditional(self):
  import ast
  tree=ast.parse((R/'world_transform125.py').read_text())
  matches=[n for n in ast.walk(tree)if isinstance(n,ast.If)and any(isinstance(x,ast.Assign)and any(isinstance(t,ast.Subscript)and isinstance(t.slice,ast.Constant)and t.slice.value=='ordered_macro_coordinate_frame'for t in x.targets)for x in n.body)]
  self.assertEqual(len(matches),1);self.assertEqual(ast.unparse(matches[0].test),"local.get('ordered_macro')")
if __name__=='__main__':unittest.main()
