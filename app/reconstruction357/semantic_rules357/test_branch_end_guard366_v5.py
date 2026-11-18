import unittest,json,copy
from branch_end_guard366_v5 import *
from branch_end_guard366_v5 import _expected_branch_projection
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
  m=_expected_branch_projection(self.r,self.p)
  x=compare_constructed(self.r,self.p,m);self.assertTrue(x['fresh_required']);self.assertFalse(x['admission_allowed'])
  m['units'][0]['activities']['new_unregistered_task']=['16','6','18','7']
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,m)
 def test_auditor_ownership_loss(self):
  m=_expected_branch_projection(self.r,self.p);m['units'][0]['ownership']=[['0','0','1','1']]
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,m)
 def test_auditor_bedroom_floor_loss(self):
  m=_expected_branch_projection(self.r,self.p);m['units'][0]['rooms']['bed1']=[['0','0','1','1']]
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,m)
 def test_auditor_plot_width_change(self):
  m=_expected_branch_projection(self.r,self.p);m['inputs'][0]='25'
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,m)
 def test_common_or_new_model_key_changed(self):
  m=_expected_branch_projection(self.r,self.p);m['common_spaces']['lobby']=[]
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,m)
  m=_expected_branch_projection(self.r,self.p);m['unregistered']=True
  with self.assertRaises(ValueError):compare_constructed(self.r,self.p,m)
 def test_saved_actual_constructor_reassessment(self):
  m=json.loads((ROOT/'review367_joint_diagnostic/branch_model_built.json').read_text())['model'];o=compare_constructed(self.r,self.p,m);self.assertEqual(o['expected_projection_digest'],digest(m));self.assertTrue(o['fresh_required'])
 def test_actual_path_through_wall_rejected(self):
  m=json.loads((ROOT/'review367_joint_diagnostic/branch_model_built.json').read_text())['model'];m['units'][0]['routes']['WC_front']=[['0','0'],m['units'][0]['routes']['WC_front'][-1]]
  with self.assertRaises(ValueError):validate_current_paths(self.r,m)
 def test_changed_target_rejected(self):
  m=json.loads((ROOT/'review367_joint_diagnostic/branch_model_built.json').read_text())['model'];m['units'][0]['route_targets']['WC_front']=['0','0']
  with self.assertRaises(ValueError):validate_current_paths(self.r,m)
 def test_missing_required_task_rejected(self):
  m=json.loads((ROOT/'review367_joint_diagnostic/branch_model_built.json').read_text())['model'];del m['units'][0]['routes']['WC_front']
  with self.assertRaises(ValueError):validate_current_paths(self.r,m)
if __name__=='__main__':unittest.main()
