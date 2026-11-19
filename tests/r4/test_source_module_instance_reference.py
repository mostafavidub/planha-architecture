"""Actual module installer fixture from floor tests, not whole generated plans."""
import copy,unittest
from test_source_module_floor_reference import build_fixture
from source_module_instance_reference_study import assess,digest
class Instances(unittest.TestCase):
 def good(self,m):return assess(m,digest(m),'PRE_WORLD_INSTALLER')
 def bad(self,m):self.assertEqual(self.good(m)['state'],'INVALID_MODULE_INSTANCE_SUBSET')
 def test_eight_source_built_installed_module_subsets(self):
  m=build_fixture();o=self.good(m);self.assertEqual(o['state'],'MODULE_INSTANCE_REFERENCE_SUBSET_BOUND_ONLY')
  self.assertEqual(len(o['bindings']),8)
  for cat,field in (('fixtures','fixture_binding_count'),('activities','activity_binding_count')):
   self.assertEqual(o[field],sum(len(p['module']['unit'][cat]) for p in m['module_placements']))
  self.assertIs(o['origin_verified'],False);self.assertIs(o['whole_inventory_verified'],False)
 def test_xy_world_source_policy_and_unchanged_metadata_negative(self):
  import world_transform125 as w
  from test_source_module_floor_reference import ENGINE
  import hashlib,inspect,pathlib
  p=ENGINE/'world_transform125.py';b=p.read_bytes()
  self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'b7e02236a057316998ae3c7d14cb0ddf94bd4879')
  self.assertEqual(pathlib.Path(inspect.getsourcefile(w.placement)).resolve(),p.resolve())
  m=build_fixture()
  for unit in m['units']:
   unit['rooms']={k:[w.rect(q)for q in qs]for k,qs in unit['rooms'].items()}
   for category in ('fixtures','activities'):unit[category]={k:w.rect(q)for k,q in unit[category].items()}
  m['module_aprons']={k:[w.rect(q)for q in qs]for k,qs in m['module_aprons'].items()}
  for p in m['module_placements']:p['transform']=w.placement(p['transform'])
  self.assertEqual(assess(m,digest(m),'XY_SWAPPED_WORLD')['state'],'INVALID_MODULE_INSTANCE_SUBSET')
  for unit in m['units']:
   for md in unit['fixture_metadata'].values():md['rotation_deg']=(90-md.get('rotation_deg',0))%180
  o=assess(m,digest(m),'XY_SWAPPED_WORLD')
  self.assertEqual(o['state'],'MODULE_INSTANCE_REFERENCE_SUBSET_BOUND_ONLY');self.assertIs(o['frame_provenance_verified'],False)
  self.assertIs(o['display_allowed'],False);self.assertIs(o['delivery_allowed'],False)
 def test_explicit_frame_mode_required(self):
  m=build_fixture();self.assertEqual(assess(m,digest(m),'GUESS')['state'],'INVALID_MODULE_INSTANCE_SUBSET')
 def test_geometry_mutation_and_wrong_type(self):
  for value in ('999',False,1.0):
   m=build_fixture();u=m['units'][0];fid=next(iter(u['fixtures']));u['fixtures'][fid][0]=value;self.bad(m)
 def test_missing_and_dangling_reference(self):
  for mode in range(2):
   m=build_fixture();p=m['module_placements'][0];key=next(iter(p['module']['unit']['fixtures']))
   if mode==0:del p['id_map'][key]
   else:p['id_map'][key]='not_present'
   self.bad(m)
 def test_empty_source_instance_map(self):
  m=build_fixture();p=m['module_placements'][0];p['module']['unit']['fixtures']={};p['module_hash']=digest(p['module']);self.bad(m)
 def test_metadata_exact_json_types(self):
  m=build_fixture();p=m['module_placements'][0];key=next(iter(p['module']['unit']['fixtures']));target=p['id_map'][key]
  p['module']['unit']['fixture_metadata'][key]['synthetic_probe']=0;p['module_hash']=digest(p['module'])
  m['units'][0]['fixture_metadata'][target]['synthetic_probe']=False
  self.bad(m)
 def test_metadata_missing_and_one_sided_edit(self):
  for mode in range(2):
   m=build_fixture();u=m['units'][0];key=next(iter(u['fixture_metadata']))
   if mode==0:del u['fixture_metadata'][key]
   else:u['fixture_metadata'][key]['unknown_probe']='edit'
   self.bad(m)
 def test_activity_geometry_and_absence(self):
  for mode in range(2):
   m=build_fixture();u=m['units'][0];key=next(iter(u['activities']))
   if mode==0:del u['activities'][key]
   else:u['activities'][key][2]='999'
   self.bad(m)
 def test_duplicate_target_within_unit_rejected(self):
  m=build_fixture();p=m['module_placements'][0];src=p['module']['unit'];key=next(iter(src['fixtures']))
  src['fixtures']['synthetic_duplicate']=copy.deepcopy(src['fixtures'][key]);src['fixture_metadata']['synthetic_duplicate']=copy.deepcopy(src['fixture_metadata'][key])
  p['id_map']['synthetic_duplicate']=p['id_map'][key];p['module_hash']=digest(p['module']);self.bad(m)
 def test_digest_identity_and_no_input_mutation(self):
  m=build_fixture();d=digest(m);self.good(m);self.assertEqual(digest(m),d)
  self.assertEqual(assess(m,'f'*64,'PRE_WORLD_INSTALLER')['state'],'INVALID_MODULE_INSTANCE_SUBSET')
 def test_same_id_between_units_is_permitted(self):
  m=build_fixture();o=self.good(m);self.assertEqual(o['state'],'MODULE_INSTANCE_REFERENCE_SUBSET_BOUND_ONLY')
  self.assertTrue(set(m['units'][0]['fixtures'])&set(m['units'][1]['fixtures']))
 def test_extra_instances_not_claimed_verified(self):
  m=build_fixture();m['units'][0]['fixtures']['unverified_extra']=['0','0','1','1']
  o=self.good(m);self.assertEqual(o['state'],'MODULE_INSTANCE_REFERENCE_SUBSET_BOUND_ONLY')
  self.assertIs(o['whole_inventory_verified'],False)
 def test_consistent_untrusted_metadata_does_not_authenticate_source(self):
  m=build_fixture();p=m['module_placements'][0];key=next(iter(p['module']['unit']['fixtures']));target=p['id_map'][key]
  p['module']['unit']['fixture_metadata'][key]['synthetic_probe']='untrusted';p['module_hash']=digest(p['module'])
  m['units'][0]['fixture_metadata'][target]['synthetic_probe']='untrusted'
  o=self.good(m);self.assertEqual(o['state'],'MODULE_INSTANCE_REFERENCE_SUBSET_BOUND_ONLY');self.assertIs(o['origin_verified'],False)
if __name__=='__main__':unittest.main()
