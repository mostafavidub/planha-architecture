import unittest,json,copy
from pathlib import Path
from private_binding121 import examine
from core_wall_audit118 import opening_hosts
from core_circulation_scope118 import grammar
from circulation_named_audit118 import private_grouping
class T(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.m=json.loads(Path('evidence/program6/deterministic_macro_assembly121.json').read_text())['model']
 def test_actual(self):
  self.assertFalse(examine(self.m)['errors']);self.assertFalse(grammar(self.m));self.assertEqual(opening_hosts(self.m)['status'],'PASS_LIMITED');self.assertEqual(private_grouping(self.m)['status'],'PASS_LIMITED')
 def test_ownership_alias(self):
  m=copy.deepcopy(self.m);m['logical_regions']['A.private_access']['parts']=m['units'][0]['ownership'];self.assertTrue(examine(m)['errors'])
 def test_rename(self):
  m=copy.deepcopy(self.m);m['logical_regions']['A.private_access']['kind']='bath';self.assertTrue(examine(m)['errors'])
 def test_portrole(self):
  m=copy.deepcopy(self.m);next(o for o in m['openings']if o['id']=='A.bed3.entry')['connects'][0]='A.public_access';self.assertTrue(examine(m)['errors'])
 def test_remove_wall(self):
  m=copy.deepcopy(self.m);del m['walls']['A.private_hall.back_left'];self.assertTrue(examine(m)['errors'])
if __name__=='__main__':unittest.main()
