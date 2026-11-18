import unittest,json,copy
from pathlib import Path
from private_role_joint367 import evaluate,source_port_cross_sections
from modules_spatial import rect
from wall_origin_joint367 import base,hall,ROOT
from common import digest
class Private(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());c.v=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());c.o=evaluate(c.r,c.v)
 def test_current_intrinsic_closed_not_necessity(self):
  self.assertEqual(self.o['status'],'PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE');self.assertFalse(self.o['parent_complete']);self.assertTrue(self.o['necessity_comparison'].startswith('NOT_ASSESSED'))
  for u in self.o['units']:self.assertEqual(u['source_connector_margin_proof']['remaining_m2'],'0');self.assertEqual(u['untargeted_terminal_extensions'],[])
 def test_actual_source_origin(self):
  b,bs=base(self.r);h,hs=hall(self.r);self.assertEqual(len(b['walls']),22);self.assertEqual(len(h['walls']),8);self.assertIn('attempt2',bs['file']);self.assertIn('attempt2',hs['file'])
 def test_ambiguous_source_axis_stops(self):
  p={'source_port_region':['0','0','1','1']}
  with self.assertRaises(ValueError):source_port_cross_sections([rect(['0','0','1','1'])],[p],'.7')
 def test_no_longitudinal_laundering(self):
  p={'source_port_region':['2','0','4','.85'],'source_port_digest':'s','actual_port_digest':'a','source_module_digest':'m'};a,j=source_port_cross_sections([rect(['0','0','10','1'])],[p],'.7');self.assertEqual(a,[rect(['2','0','4','1'])])
 def test_stale_review_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review365_service_source_validation/result.json').read_text()))
 def test_changed_wall_rejected(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['walls']['A.private_branch146.branch_end']=['0','0','1','1']
  with self.assertRaises(ValueError):evaluate(r,self.v)
if __name__=='__main__':unittest.main()
