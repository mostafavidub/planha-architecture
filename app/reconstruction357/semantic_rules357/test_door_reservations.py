import unittest,copy,json
from pathlib import Path
from door_reservations import derive
class Reservation(unittest.TestCase):
 def model(self):return {'wall_hosts':{'h':['0','1','4','1.15']},'operations':{'doors':[{'opening_id':'entry','kind':'sliding_linear','mount':{'kind':'surface','host_wall_id':'h','face':'min','offset_m':'.02','panel_thickness_m':'.1'},'closed_panel':['1','.88','2','.98'],'open_panel':['2','.88','3','.98'],'rail_envelope':['1','.88','3','.98'],'states':[{'unit':'A'}]}]}}
 def test_exact_source_offset(self):self.assertEqual(derive(self.model(),'A')[0]['region'],['1','49/50','3','1'])
 def test_wrong_offset(self):
  m=self.model();m['operations']['doors'][0]['mount']['offset_m']='.03'
  with self.assertRaises(ValueError):derive(m,'A')
 def test_rail_fabrication(self):
  m=self.model();m['operations']['doors'][0]['rail_envelope'][2]='3.5'
  with self.assertRaises(ValueError):derive(m,'A')
 def test_not_other_unit(self):self.assertEqual(derive(self.model(),'B'),[])
 def test_actual(self):
  root=Path(__file__).resolve().parents[1];m=json.loads((root/'actual_run/actual_response.json').read_text())['central_fresh_reviews'][0]['central_envelope']['packet']['world_model'];r=derive(m,'A');self.assertEqual(len(r),7);self.assertEqual(sum(x['kind']=='SOURCE113_EXISTING_POCKET_RESERVATION'for x in r),3)
if __name__=='__main__':unittest.main()
