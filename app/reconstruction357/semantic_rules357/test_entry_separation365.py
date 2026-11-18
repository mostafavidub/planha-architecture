import unittest,json,copy
from entry_separation365 import evaluate,derive,ROOT
from common import digest
from modules_spatial import rect,difference,union_area
class Separation365(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());cls.v=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());cls.q={x['requirement_id']:x for x in cls.v['raw_report']['rule_contract_evidence']['requirements']};cls.o=evaluate(cls.r,cls.v)
 def test_source_exact_margin_not_usable(self):
  a=self.o['reservations'][0];self.assertEqual(a['area_m2'],'3/1000');self.assertEqual(a['source_panel_thickness_m'],'1/10');self.assertEqual(a['source_mount_offset_m'],'1/50');self.assertEqual(a['coordinate_slack_m'],'1/40');self.assertEqual(a['usable_floor_capacity_increment'],0)
 def test_covers_exact_existing_gap(self):
  s=json.loads((ROOT/'semantic_rules357/role_registry_on365.json').read_text());a=next(u for u in s['nodes']['PUBLIC_SUPPORT']['evidence']['rows']if u['unit']=='A');gap=list(map(rect,a['unresolved_regions']));rs=[rect(x['region'])for x in self.o['reservations']];self.assertEqual(difference(gap,rs),[]);self.assertEqual(difference(rs,gap),[])
 def test_does_not_cover_extra_cell(self):
  extra=rect(['13','12.355','13.075','12.475']);self.assertGreater(union_area(difference([extra],[rect(self.o['reservations'][0]['region'])])),0)
 def test_missing_fresh_door_rejected(self):
  q=copy.deepcopy(self.q);q['door_operation']['status']='UNKNOWN'
  with self.assertRaisesRegex(ValueError,'CURRENT_SEPARATION'):derive(self.r,q)
 def test_stale_profile_rejected(self):
  with self.assertRaises(ValueError):evaluate(self.r,json.loads((ROOT/'review362_source_validation/result.json').read_text()))
 def test_wrong_mount_rejected(self):
  r=copy.deepcopy(self.r);m=r['candidate']['model'];next(o for o in m['operations']['doors']if o['opening_id']=='A.entry')['mount']['offset_m']='.03';r['candidate']['model_digest']=digest(m);r['trace']['model_digest']=digest(m);r['trace']['candidate_digest']=digest(r['candidate']);q=copy.deepcopy(self.q)
  for x in q.values():
   if 'model_hash'in x:x['model_hash']=digest(m)
  with self.assertRaisesRegex(ValueError,'MOUNT_PROFILE'):derive(r,q)
if __name__=='__main__':unittest.main()
