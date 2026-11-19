import copy,unittest,sys
from pathlib import Path
import semantic_descriptor301 as d
class Descriptor(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.s=d.fixture()
 def test_source_built_positive(self):
  x=d.describe(self.s);self.assertEqual(len(self.s['records']),4)
  self.assertFalse(x['qualified']);self.assertFalse(x['whole_model_validated'])
 def test_presentation_and_json_order(self):
  s=copy.deepcopy(self.s)
  for r in s['records']:r['display_name']='نام نمایشی';r['color']='blue'
  s['records'].reverse()
  self.assertEqual(d.compare(self.s,s)['state'],'EXACT_DESCRIPTOR_EQUIVALENT')
 def test_opaque_reference_bijection(self):
  s=copy.deepcopy(self.s)
  for r in s['records']:
   old=r['reference'];new='opaque-'+old;r['reference']=new
   r['links']={k:(new if v==old else v)for k,v in r['links'].items()}
   for o in r['openings']:o['connects']=[new if x==old else x for x in o['connects']]
  self.assertEqual(d.compare(self.s,s)['state'],'EXACT_DESCRIPTOR_EQUIVALENT')
 def test_orphan_reference(self):
  s=copy.deepcopy(self.s);s['records'][0]['reference']='orphan'
  with self.assertRaisesRegex(ValueError,'SOURCE_REFERENCE_OR_GEOMETRY'):d.describe(s)
 def test_duplicate_reference(self):
  s=copy.deepcopy(self.s);s['records'][1]['reference']=s['records'][0]['reference']
  with self.assertRaisesRegex(ValueError,'DUPLICATE_REFERENCE'):d.describe(s)
 def test_moved_fixture_without_source(self):
  s=copy.deepcopy(self.s);k=next(iter(s['records'][0]['fixtures']));s['records'][0]['fixtures'][k][0]='100'
  with self.assertRaisesRegex(ValueError,'SOURCE_REFERENCE_OR_GEOMETRY'):d.describe(s)
 def test_unknown_schema(self):
  s=copy.deepcopy(self.s);s['records'][0]['source']['schema']='FAKE'
  with self.assertRaisesRegex(ValueError,'SOURCE_SCHEMA'):d.describe(s)
 def test_rehashed_source_mutation(self):
  s=copy.deepcopy(self.s);r=s['records'][0];r['source']['unit']['fixtures']['fridge'][0]='.1';r['source_digest']=d.digest(r['source'])
  with self.assertRaisesRegex(ValueError,'SOURCE_REBUILD_BINDING'):d.describe(s)
 def test_unit_permutation(self):
  s=copy.deepcopy(self.s)
  for r in s['records']:
   u='B'if r['unit']=='A'else'A';old=r['unit']+'.public';r['unit']=u
   r['links']={k:(u+'.public'if v==old else v)for k,v in r['links'].items()}
   for o in r['openings']:o['connects']=[u+'.public'if x==old else x for x in o['connects']]
  self.assertEqual(d.compare(self.s,s)['state'],'EXACT_DESCRIPTOR_EQUIVALENT')
 def test_mirror_source_transforms(self):
  s=copy.deepcopy(self.s);M=[[-1,0],[0,1]];t={'matrix':M,'translation':['18','0']}
  for i,r in enumerate(s['records']):
   old=r['transform']['translation'];new={'matrix':M,'translation':[str(18-d.F(old[0])),old[1]]}
   s['records'][i]=d.placed(r['source'],r['unit'],r['reference'],new)
  s['core']={k:d.transform(v,t)for k,v in s['core'].items()}
  self.assertEqual(d.compare(self.s,s)['state'],'EXACT_DESCRIPTOR_EQUIVALENT')
 def test_real_component_organisation_change(self):
  s=copy.deepcopy(self.s)
  for i,r in enumerate(s['records']):
   if r['source']['schema']=='KITCHEN_MODULE117':
    t=copy.deepcopy(r['transform']);t['translation'][0]='14'
    s['records'][i]=d.placed(r['source'],r['unit'],r['reference'],t)
  x=d.compare(self.s,s);self.assertEqual(x['state'],'COMPONENT_ORGANIZATION_DESCRIPTOR_DIFFERENCE');self.assertFalse(x['architectural_diversity_verified'])
 def test_identity_is_not_descriptor_equivalence(self):
  s=copy.deepcopy(self.s);s['records'][0]['display_name']='other'
  self.assertNotEqual(d.digest(self.s),d.digest(s));self.assertTrue(d.compare(self.s,s)['same_descriptor'])
 def test_incomparable_input_programme_frame(self):
  for field,val in [('input',{'W':'19','L':'20','n':2}),('programme','OTHER_COMPONENT_SET'),('frame','OTHER_FRAME')]:
   s=copy.deepcopy(self.s);s[field]=val
   self.assertEqual(d.compare(self.s,s)['state'],'NOT_COMPARABLE')
 def test_exact_types_and_nonrigid(self):
  s=copy.deepcopy(self.s);s['input']['n']=True
  with self.assertRaisesRegex(ValueError,'INPUT_SCOPE'):d.describe(s)
  s=copy.deepcopy(self.s);s['records'][0]['transform']['matrix']=[[2,0],[0,1]]
  with self.assertRaisesRegex(ValueError,'D4_MATRIX'):d.describe(s)
 def test_unknown_transform_field(self):
  s=copy.deepcopy(self.s);s['records'][0]['transform']['scale']='2'
  with self.assertRaisesRegex(ValueError,'TRANSFORM_FIELDS'):d.describe(s)
 def test_incomparable_does_not_validate_inputs(self):
  s=copy.deepcopy(self.s);s['frame']='other'
  self.assertFalse(d.compare(self.s,s)['input_validation_performed'])
 def test_distance_change_without_relation_is_not_new_descriptor(self):
  s=copy.deepcopy(self.s)
  for i,r in enumerate(s['records']):
   if r['source']['schema']=='KITCHEN_MODULE117':
    t=copy.deepcopy(r['transform']);t['translation'][0]='2.1'
    s['records'][i]=d.placed(r['source'],r['unit'],r['reference'],t)
  self.assertEqual(d.compare(self.s,s)['state'],'EXACT_DESCRIPTOR_EQUIVALENT')
 def test_float_not_integer(self):
  s=copy.deepcopy(self.s);s['input']['n']=2.0
  with self.assertRaisesRegex(ValueError,'EXACT_JSON_TYPES'):d.describe(s)
 def test_legacy_helper_name_sensitivity_not_whole_model_validity(self):
  # Legacy helper only; NO describe_candidate, fabricated gate, or whole checker.
  sys.path.insert(0,str(d.ENGINE));import diversity_multidim126 as old
  shell={'module_placements':[],'units':[],'common_spaces':copy.deepcopy(self.s['core'])}
  for uid in('A','B'):
   rs=[r for r in self.s['records']if r['unit']==uid]
   shell['module_placements'] += [{'unit_id':uid,'room_id':d.ROLES[r['source']['schema']][2],'module':r['source']}for r in rs]
   shell['units'].append({'id':uid,'rooms':{d.ROLES[r['source']['schema']][2]:r['room_parts']for r in rs},
    'dining_module_placement':{'module':{'fixtures':{'anchor':['0','0','1','1']}},'transform':{'matrix':[[1,0],[0,1]],'translation':['0','0']}}})
  renamed=copy.deepcopy(shell)
  for p in renamed['module_placements']:
   if p['room_id']=='kitchen':p['room_id']='opaque_k'
  for u in renamed['units']:u['rooms']['opaque_k']=u['rooms'].pop('kitchen')
  a={'program_key':'same-component-helper-only','access_signature':'same-not-validated','spatial':old.spatial_variants(shell)}
  b={**a,'spatial':old.spatial_variants(renamed)}
  result=old.compare(a,b)
  self.assertEqual(result['status'],'UNRESOLVED_ROLE_INVENTORY');self.assertFalse(result['distinct'])
if __name__=='__main__':unittest.main()
