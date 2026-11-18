import unittest,json,copy
from branch_end_guard366 import *
class Guard(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());c.p=propose(c.r)
 def test_actual_source_bound(self):
  for u in self.p['units']:self.assertEqual(u['derived_end'],'135/8');self.assertEqual(u['wall_thickness_m'],'3/20');self.assertTrue(any(x['source_id'].startswith('source_port:')for x in u['bound_witnesses']))
 def test_continuous_crossing_not_endpoint_only(self):
  sw=motion(['0','0','1','1'],['4','0','5','1'])
  with self.assertRaises(ValueError):assert_removed_clear(rect(['2','0','3','1']),[('continuous_actor',sw)])
 def test_actual_port_crossing_stops(self):
  with self.assertRaises(ValueError):assert_removed_clear(rect(['2','0','3','1']),[('source_port',rect(['1','0','4','1']))])
 def test_task_crossing_stops(self):
  with self.assertRaises(ValueError):assert_removed_clear(rect(['2','0','3','1']),[('actual_task',rect(['2','0','3','1']))])
 def test_unknown_motion_stops(self):
  with self.assertRaises(ValueError):motion(['0','0','1','1'],['2','2','3','3'])
 def test_constructor_unchanged_rejected(self):
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,self.r['candidate']['model'])
 def test_synthetic_predicted_geometry_not_fresh(self):
  m=copy.deepcopy(self.r['candidate']['model'])
  for row in self.p['units']:
   for k in ('walls','wall_hosts','source_wall_hosts'):m[k].update(row['wall_replacements'])
   u=next(u for u in m['units']if u['id']==row['unit']);u['rooms']['private_circulation']=[list(map(str,q))for q in difference(list(map(rect,u['rooms']['private_circulation'])),[rect(row['removed_floor_candidate'])])]
  x=compare_constructed(self.r,self.p,m);self.assertTrue(x['fresh_required']);self.assertFalse(x['admission_allowed'])
  m['units'][0]['activities']['new_unregistered_task']=['16','6','18','7']
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,m)
if __name__=='__main__':unittest.main()
