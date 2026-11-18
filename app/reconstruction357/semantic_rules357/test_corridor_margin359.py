import unittest,json,copy
from pathlib import Path
from corridor_margin359 import prove
from common import rows
import common
ROOT=Path(__file__).resolve().parents[1]
class Margin(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text());v=json.loads((ROOT/'review359_source_validation/result.json').read_text());old=common.REGISTRY_NAME;common.REGISTRY_NAME='method_registry_source359.json';cls.req=rows(cls.r['candidate']['model'],v['raw_report']);common.REGISTRY_NAME=old;cls.c=json.loads(Path(__file__).with_name('circulation_role_actual359.json').read_text())
 def test_actual_cells_exact_source_bound(self):
  for u,c in zip(self.r['candidate']['model']['units'],self.c['units']):self.assertTrue(prove(self.r,u,c['private_circulation_components'],self.req)['all_residual_cells_source_bound'])
 def test_outside_cell_not_supporting_margin(self):
  rows=copy.deepcopy(self.c['units'][0]['private_circulation_components']);rows[0]['unsupported_margin_regions'].append(['3','5.2','4','6.2']);o=prove(self.r,self.r['candidate']['model']['units'][0],rows,self.req);self.assertFalse(o['all_residual_cells_source_bound'])
 def test_missing_required_traversal(self):
  r=copy.deepcopy(self.r);r['candidate']['model']['private_domains'][0]['paths']={}
  with self.assertRaises(ValueError):prove(r,r['candidate']['model']['units'][0],self.c['units'][0]['private_circulation_components'],self.req)
 def test_unchecked_operation_not_accepted(self):
  req=copy.deepcopy(self.req);req['door_operation']['status']='NOT_EVALUATED'
  with self.assertRaises(ValueError):prove(self.r,self.r['candidate']['model']['units'][0],self.c['units'][0]['private_circulation_components'],req)
if __name__=='__main__':unittest.main()
