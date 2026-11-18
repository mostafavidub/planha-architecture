import unittest,json,copy
from dining_inventory119 import counts
class Inventory(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with open('../planha_hybrid_independent/baseline118/random_5/response.json')as f:r=json.load(f)['result']
  cls.m=r['internal_proposals'][1]['model']
 def test_one_bed_four_source_chairs(self):
  self.assertEqual(self.m['program']['sleep_roles'],['double'])
  for u in self.m['units']:self.assertEqual(dict(counts(u)),{'dining_table':1,'dining_chair_front':2,'dining_chair_back':2})
 def test_mutations(self):
  u=self.m['units'][0]
  mutations=[lambda v:v['fixtures'].pop('dining_chair_west'),lambda v:v['fixtures']['dining_chair_west'].__setitem__(2,'999'),lambda v:v['dining_module_placement'].update(module_hash='fake'),lambda v:v['dining_module_placement']['id_map'].update(chair_west='dining_chair_east'),lambda v:v['fixture_metadata']['dining_chair_west'].update(kind='dining_chair_back'),lambda v:v['dining_module_placement']['transform'].update(matrix=[[1,1],[0,1]])]
  for i,fn in enumerate(mutations):
   v=copy.deepcopy(u);fn(v)
   with self.assertRaises((ValueError,KeyError),msg=str(i)):counts(v)
if __name__=='__main__':unittest.main()
