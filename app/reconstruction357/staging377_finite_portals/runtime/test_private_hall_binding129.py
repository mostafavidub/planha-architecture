import unittest,json,copy
from pathlib import Path
from private_hall_binding129 import examine,digest
P=Path(__file__).parent/'evidence129/case4_first_assembly.json'
class T(unittest.TestCase):
 def setUp(self):
  p=json.loads(P.read_text())['packet'];self.w=p['world_model'];self.l=p['local_model'];self.c=p['core']
 def result(self):return examine(self.w,self.l,self.c)
 def bad(self):self.assertTrue(self.result()['errors']or self.result()['pending']);self.assertEqual(self.result()['boundary_wall_ids'],[])
 def test_actual(self):r=self.result();self.assertEqual(r['errors'],[]);self.assertEqual(r['pending'],[]);self.assertEqual(len(r['boundary_wall_ids']),8)
 def test_extra_wall(self):self.w['walls']['A.private_hall.fake']=['1','1','2','2'];self.bad()
 def test_moved_hall(self):self.w['walls']['A.private_hall.back_left'][0]='0';self.bad()
 def test_renamed_hall(self):self.w['walls']['A.private_hall.fake']=self.w['walls'].pop('A.private_hall.left_return');self.bad()
 def test_bad_domain(self):self.w['private_domains'][0]['parts'][0]=['0','0','1','1'];self.bad()
 def test_bad_path(self):self.w['private_domains'][0]['paths']['A.bed1'][-1]=['0','0'];self.bad()
 def test_wrong_source(self):self.l['module_placements'][0]['module_hash']='bad';self.w['frame_binding125']['local_model_hash']=digest(self.l);self.bad()
 def test_fake_public_use(self):self.w['units'][0]['scenario_routes']['guest_dining']=copy.deepcopy(self.w['private_domains'][0]['paths']['A.bed1']);self.bad()
 def test_wrong_frame(self):self.w['frame_binding125']['world_from_local']['matrix']=[[1,0],[0,1]];self.bad()
 def test_moved_local_hall_rehashed(self):
  self.l['walls']['A.private_hall.back_left'][0]='0';self.w['frame_binding125']['local_model_hash']=digest(self.l);self.bad()
if __name__=='__main__':unittest.main()
