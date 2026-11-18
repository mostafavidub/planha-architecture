import json,copy,unittest
from pathlib import Path
from bedroom_approach_audit123 import examine
from typed_public_access120 import parts
class Typed(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  p=Path(__file__).resolve().parents[1]/'planha_hybrid_independent/baseline122_verify73_clean_20261114/random_1/response.json';c.old=json.loads(p.read_text())['result']['internal_proposals'][0]['model']
 def mapped(self):
  m=copy.deepcopy(self.old)
  for u in m['units']:
   uid=u['id'];role=uid+'.bedroom_public_access';m['logical_regions'][role]={'unit':uid,'kind':'BEDROOM_PUBLIC_APPROACH123','source_roles':['living','entry_circulation','dining']}
   for p in m['module_placements']:
    if p['unit_id']==uid and p['room_id'].startswith('bed'):p['id_map']['M.public_access']=role
   for o in m['openings']:
    if o['id']==uid+'.bed1.entry':o['connects']=[role if x==uid+'.public_access'else x for x in o['connects']]
   for p in m['module_ports']:
    if p['opening_id']==uid+'.bed1.entry':p['role_id']=role
   for d in m['operations']['doors']:
    if d['opening_id']==uid+'.bed1.entry':
     for z in d['continuous_actor_segments']+d['states']:
      if z['side']=='outside':z['role_id']=role
  return m
 def test_old_overlap_not_renamed_pass(self):
  m=self.mapped();r=examine(m,m['units'][0],'A.bedroom_public_access');self.assertTrue(any('CONSERVATIVE_RESERVATION_COLLISION'in e and ':actor:'in e for e in r['errors']),r)
 def test_private_union_rejected(self):
  m=self.mapped();m['logical_regions']['A.bedroom_public_access']['source_roles'].append('bed1');self.assertIn('BEDROOM_TYPED_ROLE_CONTRACT',examine(m,m['units'][0],'A.bedroom_public_access')['errors'])
 def test_crossuse_rejected(self):
  m=self.mapped();r=examine(m,m['units'][0],'A.bedroom_public_access','A.bath.entry');self.assertIn('BEDROOM_TYPED_OTHER_OPENING',r['errors'])
 def test_source_hash_rejected(self):
  m=self.mapped();p=next(p for p in m['module_placements']if p['unit_id']=='A'and p['room_id']=='bed1');p['module_hash']='fake';self.assertIn('BEDROOM_MODULE_HASH',examine(m,m['units'][0],'A.bedroom_public_access')['errors'])
if __name__=='__main__':unittest.main()
