import json,unittest,copy
from pathlib import Path
from circulation_named_audit118 import private_grouping,long_corridor_facts,measures,area
from core_wall_audit118 import wall_network,q
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads((Path(__file__).parent/'evidence/capacity118_whole18x24_explicit2.json').read_text())['internal_proposals'][0]['model']
 def old_unproven(self):return json.loads((Path(__file__).parent/'evidence/q11_whole118_case1.json').read_text())['model']
 def test_saved_grouping_not_claimed(self):self.assertEqual(private_grouping(self.old_unproven())['status'],'NOT_EVALUATED')
 def test_no_label_bypass(self):
  m=copy.deepcopy(self.old_unproven());m['private_grouping']={'pass':True};m['long_corridor']=False
  self.assertEqual(private_grouping(m)['status'],'NOT_EVALUATED');self.assertEqual(long_corridor_facts(m)['status'],'NOT_EVALUATED')
 def test_exact_route_metrics(self):self.assertEqual(measures([['0','0'],['0','2'],['3','2']])['length_m'],'5')
 def test_union_not_double_count(self):self.assertEqual(area([q([0,0,2,2]),q([1,0,3,2])]),6)
 def test_new_union_not_finish(self):
  r=wall_network(self.m);self.assertEqual(r['status'],'NOT_EVALUATED');self.assertTrue(r['witness']['physical_union_verified']);self.assertEqual(len(r['witness']['host_components']),1)
 def test_union_alias_deleted(self):
  m=copy.deepcopy(self.m);k=next(iter(m['physical_wall_network']['source_aliases']));m['physical_wall_network']['source_aliases'][k]=[];self.assertEqual(wall_network(m)['status'],'FAIL')
 def test_union_phantom_solid(self):
  m=copy.deepcopy(self.m);m['physical_wall_network']['solids']['extra']=['6','6','7','7'];self.assertEqual(wall_network(m)['status'],'FAIL')
if __name__=='__main__':unittest.main()
