import copy,json,unittest
from typed_public_access120 import parts
class Typed(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with open('evidence/correction120/fresh_case5_automatic120.json')as f:m=json.load(f)['result']['internal_proposals'][1]['model']
  cls.m=m;cls.uid='A';role='A.kitchen_public_access';rec=next(p for p in m['module_placements']if p['unit_id']=='A'and p['room_id']=='kitchen');old=rec['id_map']['K.public_access'];rec['id_map']['K.public_access']=role
  ids={rec['id_map'][o['id']]for o in rec['module']['openings']}
  for o in m['openings']:
   if o['id']in ids:o['connects']=[role if x==old else x for x in o['connects']]
  m['logical_regions'][role]={'unit':'A','source_roles':['living','entry_circulation','dining']}
 def check(self,m,role='A.kitchen_public_access',opening_id=None):return parts(m,m['units'][0],role,opening_id)
 def test_positive_union(self):self.assertTrue(self.check(self.m))
 def test_unknown(self):
  with self.assertRaises(ValueError):self.check(self.m,'A.any_public')
 def test_private_in_union(self):
  m=copy.deepcopy(self.m);m['logical_regions']['A.kitchen_public_access']['source_roles'].append('bed1')
  with self.assertRaises(ValueError):self.check(m)
 def test_bed_opening_use(self):
  with self.assertRaises(ValueError):self.check(self.m,opening_id='A.bed1.entry')
 def test_rename_dining(self):
  m=copy.deepcopy(self.m);m['units'][0]['rooms']['fake']=m['units'][0]['rooms'].pop('dining')
  with self.assertRaises(ValueError):self.check(m)
 def test_plain_public_not_broadened(self):
  m=copy.deepcopy(self.m);m['logical_regions']['A.public_access']['source_roles'].append('dining')
  with self.assertRaises(ValueError):self.check(m,'A.public_access')
if __name__=='__main__':unittest.main()
