import unittest,json,copy
from service_closure359 import *
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.args=[json.loads((ROOT/p).read_text())for p in ['staging359_hall_clamp/actual359.json','review359_source_validation/result.json','staging358_comparative/row_candidate358.json','review358_source_validation/result.json']]
 def test_actual(self):
  x=assess(*self.args);self.assertEqual(x['verdict'],'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS');self.assertTrue(all(u['current_room_excess_m2']=='0'for u in x['units']));self.assertFalse(x['live_authority'])
 def test_service_only_outside_entry_not_ignored(self):
  self.assertFalse(reconcile_scope({'complete':True},{'unassigned_after_source_clearance_m2':'1/4'}))
 def test_raw_tamper_rejected(self):
  a=copy.deepcopy(self.args);a[1]['raw_report']['errors']=['tamper']
  with self.assertRaises(ValueError):assess(*a)
 def test_added_unswept_entry_tail_is_not_shared(self):
  m=copy.deepcopy(self.args[0]['candidate']['model']);u=m['units'][0];u['rooms']['entry_circulation'].append(['100','100','101','101']);r=measure(m)[0];p=next(p for p in m['module_placements']if p['unit_id']=='A'and p['room_id']=='bath');app=[transformed_rect(q,p['transform'])for q in p['module']['unit']['rooms']['public_access']];o=next(o for o in m['openings']if o['id']=='A.bath');x=domain_partition(m,u,r['service_target_ids'],app,rect(o['rect']));self.assertFalse(x['complete']);self.assertEqual(x['entry_uncovered_area_m2'],'1')
 def test_source_approach_tamper_rejected(self):
  m=copy.deepcopy(self.args[0]['candidate']['model']);m['module_aprons']['A.bath']=[]
  with self.assertRaises(ValueError):classify(m,measure(m))
if __name__=='__main__':unittest.main()
