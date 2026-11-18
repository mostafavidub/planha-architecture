import unittest,json,copy
from fractions import Fraction as F
from branch_margin_service365_v2 import evaluate,transverse_port_support,ROOT
from modules_spatial import rect,union_area
class BranchMargin(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.r=json.loads((ROOT/'staging365_service_grammar/candidate365.json').read_text());c.v=json.loads((ROOT/'review365_service_source_validation/result.json').read_text());c.o=evaluate(c.r,c.v)
 def test_own_partial_extent(self):
  for u in self.o['units']:self.assertEqual(u['remaining_m2'],'27/20');self.assertEqual(u['remaining_protected_domain_intersections'],[]);self.assertFalse(u['whole_role_complete'])
 def test_no_uselessness_claim(self):
  self.assertFalse(self.o['admission_allowed']);self.assertTrue(all('NOT_PROVEN_USELESS'in u['remaining_status']for u in self.o['units']))
 def test_source_pin_rejected(self):
  r=copy.deepcopy(self.r);r['trace']['source_inventory']['planha_general150_runtime_work/private_branch_hall146.py']='0'*64
  with self.assertRaises(ValueError):evaluate(r,self.v)
 def test_cross_section_not_longitudinal(self):
  p={'source_port_region':['2','0','4','.85'],'opening_id':'a','source_port_digest':'s','actual_port_digest':'a'}
  allowed,_=transverse_port_support([rect(['0','0','10','1'])],[p],'.7');self.assertEqual(allowed,[rect(['2','0','4','1'])])
 def test_no_wide_empty_room_laundering(self):
  p={'source_port_region':['2','0','4','.85'],'opening_id':'a','source_port_digest':'s','actual_port_digest':'a'}
  self.assertEqual(transverse_port_support([rect(['0','0','10','5'])],[p],'.7')[0],[])
if __name__=='__main__':unittest.main()
