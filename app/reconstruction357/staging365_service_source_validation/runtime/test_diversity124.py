"""Bounded classifier tests; transformed fixture receipts are NOT plan approvals."""
import copy,json,unittest
from pathlib import Path
from diversity124 import audit_batch,describe_model,compare,digest,transform
class Diversity(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.candidate=json.loads((Path(__file__).parent/'evidence124/service_shared_case1_current_gate.json').read_text());c.model=c.candidate['model'];c.description=describe_model(c.model)
 def unchanged(self,m):self.assertFalse(compare(self.description,describe_model(m))['distinct'])
 def test_singular_fractional_transform_rejected(self):
  for mat in [[[".5",".5"],[".5",".5"]],[[1,1],[0,1]],[[2,0],[0,".5"]],[[".6","-.8"],[".8",".6"]]]:
   with self.assertRaisesRegex(ValueError,'NONRIGID_SOURCE_TRANSFORM'):
    transform({'transform':{'matrix':mat,'translation':['0','0']}})
 def test_all_eight_exact_d4_transforms(self):
  from fractions import Fraction as F
  for swapped in (False,True):
   for a in (-1,1):
    for b in (-1,1):
     mat=[[0,a],[b,0]]if swapped else[[a,0],[0,b]]
     fn=transform({'transform':{'matrix':mat,'translation':['1/3','2/7']}});r=fn([0,0,2,1]);self.assertEqual((r[2]-r[0])*(r[3]-r[1]),F(2));self.assertEqual(sorted([r[2]-r[0],r[3]-r[1]]),[F(1),F(2)])
 def test_actual_singleton(self):
  r=audit_batch([self.candidate]);self.assertEqual(r['distinct_count'],1);self.assertEqual(r['shortfall'],5);self.assertFalse(r['verified_architectural_diversity']);self.assertFalse(r['errors'])
 def test_actual_duplicate(self):
  r=audit_batch([self.candidate,copy.deepcopy(self.candidate)]);self.assertEqual(r['distinct_count'],1)
 def test_json_order_unit_order(self):
  m=json.loads(json.dumps(self.model,sort_keys=True));m['units'].reverse();m['openings'].reverse();m['module_placements'].reverse();self.unchanged(m)
 def test_unit_id_rename(self):
  def name(s):return 'Z'+s[1:]if s=='A'or s.startswith('A.')else s
  def rename(v,key=None):
   if key=='module':return copy.deepcopy(v)
   if isinstance(v,dict):return {(k if key=='id_map'else name(k)):rename(x,k)for k,x in v.items()}
   if isinstance(v,list):return [rename(x)for x in v]
   return name(v)if isinstance(v,str)else v
  self.unchanged(rename(self.model))
 def test_topology_hash_seed_no_effect(self):
  m=copy.deepcopy(self.model);m['topology']='FAKE_NEW';m['source_revision']='new';m['random_seed']=999;self.unchanged(m)
 def test_light_window_absent(self):
  m=copy.deepcopy(self.model);m.pop('concept_windows',None);m.pop('openedge_assumptions',None);self.unchanged(m)
 def test_cell_subdivision(self):
  m=copy.deepcopy(self.model);r=m['units'][0]['rooms']['bed1'].pop();from fractions import Fraction as F
  x,y,X,Y=map(F,r);mid=(x+X)/2;m['units'][0]['rooms']['bed1'] += [list(map(str,[x,y,mid,Y])),list(map(str,[mid,y,X,Y]))];self.unchanged(m)
 def test_route_waypoint_is_not_diversity(self):
  m=copy.deepcopy(self.model);u=m['units'][0];k=next(iter(u['routes']));u['routes'][k].insert(1,u['routes'][k][0]);self.unchanged(m)
 def test_private_fake_alias_not_counted(self):
  m=copy.deepcopy(self.model);m['logical_regions']['FAKE_PRIVATE']={'kind':'private_approach','parts':[]}
  with self.assertRaises(ValueError):describe_model(m)
 def test_fixture_only_moved_rejected(self):
  m=copy.deepcopy(self.model);r=m['units'][0]['fixtures']['bed1.bed'];r[0]=str(float(r[0])+.1);r[2]=str(float(r[2])+.1)
  with self.assertRaises(ValueError):describe_model(m)
 def test_correlated_opening_metadata_rejected(self):
  m=copy.deepcopy(self.model);o=next(o for o in m['openings']if o['id']=='A.bed1.entry');o['connects']=['A.bath','A.bed1']
  with self.assertRaises(ValueError):describe_model(m)
 def test_receipt_binding(self):
  c=copy.deepcopy(self.candidate);c['gate']['model_hash']='fake';r=audit_batch([c]);self.assertEqual(r['distinct_count'],0);self.assertIn('GATE_MODEL_BINDING',r['errors'][0]['reason'])
 def test_no_false_program_aggregation(self):
  # Descriptor-level unit test only, not a generated/admitted alternative.
  a=copy.deepcopy(self.description);a['program_key']+='different';r=compare(self.description,a);self.assertEqual(r['status'],'INCOMPARABLE_PROGRAM');self.assertFalse(r['distinct'])
 def test_contact_only_change_unresolved(self):
  a=copy.deepcopy(self.description);a['units'][0]['physical_floor_contacts']=[];self.assertFalse(compare(self.description,a)['distinct'])
if __name__=='__main__':unittest.main()
