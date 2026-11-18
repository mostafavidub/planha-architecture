import json,copy,unittest
from pathlib import Path
from public_program_audit118 import examine,digest
class Tests(unittest.TestCase):
 def setUp(self):
  self.m=json.loads((Path(__file__).parent/'evidence/capacity118_whole18x24_metadata_bound.json').read_text());self.m=self.m.get('model',self.m)
 def test_saved(self):self.assertEqual(examine(self.m)['errors'],[])
 def test_hash(self):
  self.m['units'][0]['dining_module_placement']['module_hash']='fake';self.assertTrue(examine(self.m)['errors'])
 def test_transform(self):
  self.m['units'][0]['dining_module_placement']['transform']['translation'][0]='100';self.assertTrue(examine(self.m)['errors'])
 def test_activity(self):
  self.m['units'][0]['activities']['dining_east']=['1','1','1.7','1.7'];self.assertTrue(examine(self.m)['errors'])
 def test_source_motion(self):
  p=self.m['units'][0]['dining_module_placement'];p['module']['seating']['instances'][0]['rise_transfer']['segments'][1]['actor_end'][0]='9';p['module_hash']=digest(p['module']);self.assertTrue(examine(self.m)['errors'])
if __name__=='__main__':unittest.main()
