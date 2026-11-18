import json,copy,unittest
from operation_check114 import source_nonleaf117
class TypedNonleaf(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with open('evidence/correction120/prefreeze_typed_kitchen_case5_assembly_only.json')as f:cls.m=json.load(f)['model']
 def opening(self,m):return next(o for o in m['openings']if o['id']=='A.kitchen.entry')
 def test_actual(self):self.assertTrue(source_nonleaf117(self.m,self.opening(self.m)))
 def test_legacy_two_roles(self):
  with open('evidence/correction120/fresh_case5_automatic120.json')as f:m=json.load(f)['result']['internal_proposals'][1]['model']
  self.assertTrue(source_nonleaf117(m,self.opening(m)))
  m['logical_regions']['A.public_access']['source_roles'].append('dining')
  self.assertFalse(source_nonleaf117(m,self.opening(m)))
 def test_negatives(self):
  for field,value in [('connects',['A.kitchen','A.bed1']),('kind','sliding_study'),('hardware',{'leaf':True}),('host_wall_id','front'),('rect',['0','0','1','.15'])]:
   m=copy.deepcopy(self.m);o=self.opening(m);o[field]=value;self.assertFalse(source_nonleaf117(m,o),field)
  m=copy.deepcopy(self.m);next(p for p in m['module_placements']if p['unit_id']=='A'and p['room_id']=='kitchen')['module_hash']='fake';self.assertFalse(source_nonleaf117(m,self.opening(m)))
 def test_private_door_not_arch(self):
  m=copy.deepcopy(self.m);o=next(o for o in m['openings']if o['id']=='A.bed1.entry');o['kind']='permanent_open_arch';o['hardware']=None;self.assertFalse(source_nonleaf117(m,o))
if __name__=='__main__':unittest.main()
