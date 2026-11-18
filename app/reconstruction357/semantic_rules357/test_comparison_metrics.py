import unittest
from comparison_metrics import *
class Tests(unittest.TestCase):
 def test_union(self):self.assertEqual(rectangle_union_area([['0','0','2','2'],['1','0','3','2']]),6)
 def test_empty(self):self.assertEqual(rectangle_union_area([]),0)
 def test_float(self):
  with self.assertRaises(ValueError):rational(.7)
 def test_bool(self):
  with self.assertRaises(ValueError):rational(True)
 def test_route(self):self.assertEqual(route_metrics([['0','0'],['2','0'],['2','3']]),{'length':'5','direction_changes':1})
 def test_diagonal(self):
  with self.assertRaises(ValueError):route_metrics([['0','0'],['2','3']])
 def test_protection(self):self.assertFalse(compare_vectors({'a':2},{'a':1},{'p':1},{'p':2})['strictly_dominates'])
 def test_no_admission(self):self.assertFalse(compare_vectors({'a':2},{'a':1},{'p':1},{'p':1})['rule_acceptance'])
if __name__=='__main__':unittest.main()
