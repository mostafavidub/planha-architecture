import json,unittest,copy
from pathlib import Path
from paired_private_zone118 import examine
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.m=json.loads((Path(__file__).parent/'evidence/q11_whole118_case1.json').read_text())['model']
 def test_actual_enclosure_but_missing_guest(self):
  zones=examine(self.m)['zones'];self.assertEqual(len(zones),2);self.assertTrue(all(z['geometric_enclosure_proven']for z in zones));self.assertTrue(all(z['status']=='NOT_EVALUATED_APPROACH_USE'for z in zones))
 def test_cannot_bypass_with_label(self):
  m=copy.deepcopy(self.m);m['private_grouping']='PASS';self.assertTrue(all(z['status']=='NOT_EVALUATED_APPROACH_USE'for z in examine(m)['zones']))
 def test_body_obstruction(self):
  m=copy.deepcopy(self.m);z=examine(m)['zones'][0];x,y,X,Y=z['zone'];m['walls']['bad']=[x,y,X,Y];self.assertTrue(any('ZONE_PHYSICAL_OBSTRUCTION'in q['errors']for q in examine(m)['zones']))
 def test_side_wall_gap(self):
  m=copy.deepcopy(self.m);m['walls']={k:v for k,v in m['walls'].items()if k!='A.bed1.left.upper'}
  # Mutation points at the actual side solid used by this source model.
  z=examine(m)['zones'];self.assertTrue(any(q['errors']for q in z))
if __name__=='__main__':unittest.main()
