import unittest
import bedroom_grouping358 as b
class Tests(unittest.TestCase):
 def test_boundary_source_scaled(self):
  self.assertTrue(b.elongated([['0','0','5','4.4']],[['0','0','.6','2']])['trigger'])
  self.assertFalse(b.elongated([['0','0','5','4.5']],[['0','0','.6','2']])['trigger'])
 def test_no_geometry_not_na(self):
  with self.assertRaises(ValueError):b.elongated([['0','0','5','4']],[])
 def test_noncompensatory(self):
  x=b.compare({'a':'1','b':'10'},{'a':'2','b':'9'});self.assertTrue(x['tradeoff']);self.assertFalse(x['dominates_on_these_routes_only'])
 def test_missing_target(self):
  with self.assertRaises(ValueError):b.compare({'a':'1'},{'b':'1'})
 def test_no_route_not_zero(self):
  with self.assertRaises(ValueError):b.compare({'a':None},{'a':'1'})
if __name__=='__main__':unittest.main()
