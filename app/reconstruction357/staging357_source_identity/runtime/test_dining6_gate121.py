import copy,json,unittest
from pathlib import Path
from public_program_audit118 import examine_dining_module,digest
from dining_motion_audit118 import examine
from dining_inventory119 import counts
class Six(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads(Path('../planha_program6_study/evidence/module6_5.4x4.4.json').read_text())
 def test_local(self):self.assertEqual(examine(self.m)['errors'],[]);self.assertEqual(examine_dining_module(self.m)['errors'],[])
 def unit(self):
  m=copy.deepcopy(self.m);ids={k:k for k in m['fixtures']};md={k:{'kind':'dining_table6'if k=='table'else'dining_chair_front'if k in('chair_front_left','chair_front_right','chair_left')else'dining_chair_back'}for k in ids}
  return {'dining_module_placement':{'module':m,'module_hash':digest(m),'id_map':ids,'transform':{'matrix':[[1,0],[0,1]],'translation':['0','0']}},'fixtures':copy.deepcopy(m['fixtures']),'fixture_metadata':md}
 def test_source_inventory(self):self.assertEqual(dict(counts(self.unit())),{'dining_table6':1,'dining_chair_front':3,'dining_chair_back':3})
 def test_negatives(self):
  u=self.unit();u['fixtures'].pop('chair_left')
  with self.assertRaises((KeyError,ValueError)):counts(u)
  for mutate in [lambda m:m['fixtures']['table'].__setitem__(2,'9'),lambda m:m['seating']['instances'].pop(),lambda m:m['source_binding'].update(metadata_sha256='fake'),lambda m:m['seating']['instances'][0]['occupied_body'].__setitem__(2,'9')]:
   m=copy.deepcopy(self.m);mutate(m);self.assertTrue(examine(m)['errors'])
if __name__=='__main__':unittest.main()
