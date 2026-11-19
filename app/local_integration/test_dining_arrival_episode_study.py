import copy,sys,unittest
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[1]/'reconstruction357/planha_general150_runtime_work')]
from dining_arrival_episode_study import seat_binding,scenario_fixture_obstacles,strict_json,check_units
from same_version_front_rear_contract import digest
from dining_module118 import build
def fixture():
 m=build('4','4');p={'module':m,'module_hash':digest(m),'id_map':{k:k for k in m['fixtures']},'transform':{'matrix':[[1,0],[0,1]],'translation':['0','0']}}
 u={'fixtures':copy.deepcopy(m['fixtures']),'fixture_metadata':{k:{} for k in m['fixtures']},'dining_module_placement':p,'activities':{}}
 ops=[]
 for s in m['seating']['instances']:
  r=s['rise_transfer'];a=r['pulled_occupied_body'];b=r['standing_body']
  from fractions import Fraction as F
  centre=lambda q:[str((F(q[0])+F(q[2]))/2),str((F(q[1])+F(q[3]))/2)]
  u['activities']['dining_'+s['id'][5:]]=b
  ops.append({'fixture_id':s['fixture_id'],'source_module_hash':digest(m),'closed_rect':s['closed_rect'],'open_rect':s['pulled_rect'],'occupied_body':s['occupied_body'],'translation':s['translation'],'egress_route':[centre(a),centre(b)]})
 return u,m['seating']['instances'][0],ops
class Episode(unittest.TestCase):
 def test_source_module_endpoint_only_not_whole_model(self):
  u,s,ops=fixture();fid,aid,end,op=seat_binding(u,s,ops);self.assertEqual(fid,s['fixture_id']);self.assertEqual(end,op['egress_route'][-1])
 def test_own_pulled_replaces_closed_and_no_own_occupied(self):
  u,s,ops=fixture();obs=scenario_fixture_obstacles(u,ops,s['fixture_id'])
  self.assertNotIn(s['closed_rect'],obs);self.assertIn(s['pulled_rect'],obs);self.assertNotIn(s['occupied_body'],obs)
  for o in ops[1:]:self.assertIn(o['closed_rect'],obs);self.assertIn(o['occupied_body'],obs)
 def test_standing_mutation(self):
  u,s,ops=fixture();u['activities']['dining_west']=['0','0','1','1']
  with self.assertRaisesRegex(ValueError,'STANDING_ACTIVITY'):seat_binding(u,s,ops)
 def test_egress_mutation(self):
  u,s,ops=fixture();ops[0]['egress_route'][-1]=['0','0']
  with self.assertRaisesRegex(ValueError,'EGRESS_STANDING'):seat_binding(u,s,ops)
 def test_duplicate_operation(self):
  u,s,ops=fixture();ops[1]=copy.deepcopy(ops[0])
  with self.assertRaisesRegex(ValueError,'FOUR_UNIQUE'):scenario_fixture_obstacles(u,ops,s['fixture_id'])
 def test_false_profile_approval(self):
  u,s,ops=fixture();s['rise_transfer']['human_transfer_and_support_profile_validated']=True
  u['dining_module_placement']['module_hash']=digest(u['dining_module_placement']['module'])
  with self.assertRaisesRegex(ValueError,'UNEXPECTED_APPROVAL'):seat_binding(u,s,ops)
 def test_tuple_not_normalized(self):
  with self.assertRaisesRegex(ValueError,'NON_JSON_TYPE'):strict_json({'point':(0,1)})
 def test_duplicate_unit_ids(self):
  with self.assertRaisesRegex(ValueError,'UNIT_IDENTITY'):check_units({'units':[{'id':'A'},{'id':'A'}],'profile':{'body_m':'.7'}})
 def test_fake_width(self):
  with self.assertRaisesRegex(ValueError,'BODY_PROFILE'):check_units({'units':[{'id':'A'},{'id':'B'}],'profile':{'body_m':'.6'}})
if __name__=='__main__':unittest.main()
