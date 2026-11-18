import unittest,copy,json
from pathlib import Path
import bedroom_grouping365 as b
P=Path(__file__).resolve().parents[1]
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((P/'staging365_balanced_portals/actual365.json').read_text());cls.f=json.loads((P/'review365_balanced_source_validation/result.json').read_text());cls.old=json.loads((P/'staging358_comparative/row_candidate358.json').read_text());cls.sections=json.loads((P/'semantic_rules357/bedroom_sections_actual358.json').read_text())['rows']
 def test_actual_equivalence(self):self.assertEqual(len(b.room_equivalence(self.r['candidate']['model'],self.old['candidate']['model'],self.sections)),6)
 def test_module_changed(self):
  m=copy.deepcopy(self.r['candidate']['model']);m['module_placements'][0]['module']['bounds']=['0','0','1','1']
  with self.assertRaises(ValueError):b.room_equivalence(m,self.old['candidate']['model'],self.sections)
 def test_interior_wall_changed(self):
  m=copy.deepcopy(self.r['candidate']['model']);room=m['units'][0]['rooms']['bed1'][0];m['walls']['TEST']=room
  with self.assertRaises(ValueError):b.room_equivalence(m,self.old['candidate']['model'],self.sections)
 def test_cross_model_fresh(self):
  f=json.loads((P/'review358_source_validation/result.json').read_text());x=b.evaluate(self.r,f);self.assertFalse(x['proofscopecomplete']);self.assertEqual(x['verdict'],'UNKNOWN')
 def test_stale_record(self):
  r=copy.deepcopy(self.r);r['accepted']=True;x=b.evaluate(r,self.f);self.assertFalse(x['proofscopecomplete'])
 def test_ownership_loss(self):
  old=json.loads((P/'staging359_hall_clamp/actual359.json').read_text())['candidate']['model'];m=copy.deepcopy(self.r['candidate']['model']);m['units'][0]['ownership']=[]
  with self.assertRaises(ValueError):b.ownership_protection(m,old)
 def test_current_ownership_nonshrink(self):
  old=json.loads((P/'staging359_hall_clamp/actual359.json').read_text())['candidate']['model'];x=b.ownership_protection(self.r['candidate']['model'],old);self.assertEqual([r['lost_area_m2']for r in x],['0','0']);self.assertEqual(x[0]['added_area_m2'],'627/400')
if __name__=='__main__':unittest.main()
