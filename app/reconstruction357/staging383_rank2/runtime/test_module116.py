import json,copy,unittest
from pathlib import Path
from checker114 import check_module
class ModuleMutation(unittest.TestCase):
 def setUp(self):
  self.m=json.loads(Path('evidence/module116_6x4.2.json').read_text())
 def codes(self,m):return {e['code']for e in check_module(m)['errors']}
 def test_no_whole_admission(self):
  r=check_module(self.m);self.assertFalse(r['whole_model_pass']);self.assertFalse(r['eligible_for_draft_export'])
 def test_fixture_resize(self):
  m=copy.deepcopy(self.m);m['unit']['fixtures']['bed1.bed'][2]='5.99';self.assertIn('MODULE_FIXTURE_RIGID_SIZE',self.codes(m))
 def test_missing_closet(self):
  m=copy.deepcopy(self.m);del m['unit']['fixtures']['bed1.closet'];self.assertIn('MODULE_PRIVATE_FIXTURE_INVENTORY',self.codes(m))
 def test_port_fake(self):
  m=copy.deepcopy(self.m);m['external_ports'][0]['opening_id']='fake';self.assertIn('MODULE_PORT_APERTURE_BINDING',self.codes(m))
 def test_diagonal_route(self):
  m=copy.deepcopy(self.m);key=next(iter(m['unit']['routes']));m['unit']['routes'][key]=[[0,0],[1,1]];self.assertIn('MODULE_SCHEMA_OR_GEOMETRY_ERROR',self.codes(m))
 def test_producer_source_binding(self):
  m=copy.deepcopy(self.m);m['source_binding']['producer_sha256']='0'*64;self.assertIn('MODULE_PRODUCER_SOURCE_CHANGED',self.codes(m))
 def test_body_contract_binding(self):
  m=copy.deepcopy(self.m);m['input_program']['body_m']='.6';self.assertIn('MODULE_PROGRAM_BODY_BINDING',self.codes(m))
if __name__=='__main__':unittest.main()
