import copy,json,unittest
from pathlib import Path
from frame_circulation125 import examine,grammar
from frame_audit125 import digest
P=Path(__file__).parent/'evidence125/world125_transfer_bound39x7.07.json'
class Tests(unittest.TestCase):
 def setUp(self):
  p=json.loads(P.read_text());self.m=p['world_model'];self.c=p['core']
 def bad(self):self.assertTrue(grammar(self.m,self.c))
 def test_actual(self):self.assertEqual(grammar(self.m,self.c),[])
 def test_context_missing(self):self.assertTrue(grammar(self.m))
 def test_extra_wall(self):self.m['walls']['fake']=['1','1','2','2'];self.bad()
 def test_moved_wall(self):self.m['walls']['left']=['.01','0','.26','7.07'];self.bad()
 def test_forged_hash(self):self.c['physical_core_hash']='0'*64;self.bad()
 def test_forged_core_rehashed(self):
  self.c['physical_core_model']['units']['B']=copy.deepcopy(self.c['physical_core_model']['units']['A']);self.c['physical_core_hash']=digest(self.c['physical_core_model']);self.m['frame_binding125']['core_contract_hash']=digest(self.c);self.bad()
 def test_ownership(self):self.m['units'][1]['ownership']=copy.deepcopy(self.m['units'][0]['ownership']);self.bad()
 def test_portal(self):self.m['openings'][0]['rect'][0]='17';self.bad()
 def test_route(self):self.m['common_routes']['stair_A'][1]=['1','1'];self.bad()
 def test_input(self):self.m['inputs'][0]='38';self.bad()
 def test_module_hiding_wall(self):
  p=self.m['module_placements'][0];k=next(iter(p['module']['walls']));p['id_map'][k]='left';self.bad()
 def test_renamed_corridor(self):self.m['units'][0]['rooms']['hidden_hall']=self.m['units'][0]['rooms'].pop('entry_circulation');self.bad()
 def test_wrong_portal_roles(self):
  self.m['openings'][0]['connects']=['A.bath','B.bed1']
  self.assertIn('COMMON_PORTAL_ENDPOINT_ROLES:A.entry',examine(self.m,self.c)['errors'])
 def test_other_unit_role(self):self.m['openings'][0]['connects']=['lobby','B.public_access'];self.bad()
 def test_fake_role(self):self.m['openings'][0]['connects']=['lobby','A.fake'];self.bad()
 def test_public_role_private_alias(self):self.m['logical_regions']['A.public_access']['source_roles']=['bed1'];self.bad()
 def test_public_role_override_parts(self):self.m['logical_regions']['A.public_access']['parts']=[['0','0','1','1']];self.bad()
 def test_forged_source_roles_rehashed(self):
  self.c['physical_core_model']['openings'][0]['connects']=['A.bath','B.bed1'];self.c['physical_core_hash']=digest(self.c['physical_core_model']);self.m['frame_binding125']['core_contract_hash']=digest(self.c);self.bad()
 def test_reversed_role_order(self):
  self.m['openings'][0]['connects'].reverse();self.assertEqual(grammar(self.m,self.c),[])
 def test_singular(self):self.c['world_from_local']['matrix']=[[.5,.5],[.5,.5]];self.bad()
if __name__=='__main__':unittest.main()
