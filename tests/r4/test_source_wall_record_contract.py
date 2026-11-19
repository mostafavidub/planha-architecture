"""Synthetic source-shaped wall graph tests; no producer or private model."""
import copy,hashlib,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'app/local_integration'))
from source_wall_record_contract_study import ROOT_KEYS,MAPS,SCHEMA,assess,digest,wall_graph,same_union,rectangle
def fixture():
 w={'A.shared':['0','0','2','1'],'B.shared':['1','0','3','1']}
 n={'schema':'EXACT_SOURCE_WALL_UNION118','source_wall_hash':digest(w),'solids':{'physical_wall_0':['0','0','1','1'],'physical_wall_1':['1','0','2','1'],'physical_wall_2':['2','0','3','1']},'source_aliases':{'A.shared':['physical_wall_0','physical_wall_1'],'B.shared':['physical_wall_1','physical_wall_2']},'source_walls_preserved':True,'method':'synthetic exact union','faces':'synthetic source-shaped study','finish_profile_status':'NOT_EVALUATED','accepted':False}
 m=dict.fromkeys(ROOT_KEYS);m.update(schema='GENERAL125_WORLD_FRAME_STUDY',inputs=['20','25',2],accepted=False,release_allowed=False,units=[{'id':'A'},{'id':'B'}],program={'units':2,'bedrooms_per_unit':2,'sleep_roles':['double','twin']},walls=w,wall_hosts=copy.deepcopy(w),source_wall_hosts=copy.deepcopy(w),physical_wall_network=n)
 return m
class WallRecords(unittest.TestCase):
 def test_source_pins(self):
  for name,pin in [('wall_union118.py','0b87dbbe20a86179493ff844035cbb681f44de59'),('assemble114.py','6e19b12c62820e015055765e0fe56d6339cd4312'),('world_transform125.py','b7e02236a057316998ae3c7d14cb0ddf94bd4879')]:
   b=(ROOT/'app/reconstruction357/planha_general150_runtime_work'/name).read_bytes();self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),pin)
 def test_overlapping_source_walls_exact_material_aliases(self):
  m=fixture();out=assess(m,digest(m));self.assertEqual(out['state'],'WALL_RECORD_REFERENCE_AND_MATERIAL_UNION_VALID_ONLY')
  self.assertTrue(out['wall_graph']['material_union_equal']);self.assertEqual(out['wall_graph']['physical_solid_count'],3)
  self.assertEqual(len(out['projection']['records']),6)
  for k in ('origin_verified','source_inventory_completeness_verified','whole_schema_verified','physical_verified','accepted','qualified','display_allowed','delivery_allowed'):self.assertIs(out[k],False)
 def reject(self,mutate):
  m=fixture();mutate(m);out=assess(m,digest(m));self.assertEqual(out['state'],'INVALID_WALL_RECORD_CONTRACT');return out
 def test_unknown_missing_root_and_network_fields(self):
  for f in (lambda m:m.update(unknown=[]),lambda m:m.pop('wall_hosts'),lambda m:m['physical_wall_network'].update(unknown=0),lambda m:m['physical_wall_network'].pop('faces')):self.reject(f)
 def test_duplicate_units_and_typed_program(self):
  for f in (lambda m:m['units'][1].update(id='A'),lambda m:m['program'].update(bedrooms_per_unit=2.0),lambda m:m['program'].update(units=True),lambda m:m['inputs'].__setitem__(2,2.0)):self.reject(f)
 def test_missing_extra_and_dangling_aliases(self):
  for f in (lambda m:m['physical_wall_network']['source_aliases'].pop('A.shared'),lambda m:m['physical_wall_network']['source_aliases'].update(extra=[]),lambda m:m['physical_wall_network']['source_aliases']['A.shared'].append('missing'),lambda m:m['physical_wall_network']['source_aliases']['A.shared'].append('physical_wall_0')):self.reject(f)
 def test_alias_wrong_material_and_missing_intersection(self):
  self.reject(lambda m:m['physical_wall_network']['source_aliases'].__setitem__('A.shared',['physical_wall_0','physical_wall_2']))
  self.reject(lambda m:m['physical_wall_network']['source_aliases'].__setitem__('A.shared',['physical_wall_0']))
 def test_material_gap_overlap_and_excess(self):
  for q in (['0','0','0.9','1'],['0','0','1.1','1'],['-1','0','1','1']):
   self.reject(lambda m:m['physical_wall_network']['solids'].__setitem__('physical_wall_0',q))
 def test_hash_identity_and_sourcewall_hash(self):
  m=fixture();out=assess(m,'0'*64);self.assertEqual(out['error'],'MODEL_DIGEST_MISMATCH')
  self.reject(lambda m:m['physical_wall_network'].update(source_wall_hash='0'*64))
 def test_coordinate_and_authority_types(self):
  for f in (lambda m:m['wall_hosts']['A.shared'].__setitem__(0,0),lambda m:m['wall_hosts']['A.shared'].__setitem__(0,False),lambda m:m['physical_wall_network'].update(accepted=0),lambda m:m.update(accepted=0)):self.reject(f)
 def test_union_spatial_not_just_area(self):
  self.assertFalse(same_union([rectangle(['0','0','1','1'])],[rectangle(['2','0','3','1'])]))
 def test_alias_order_not_geometric_meaning(self):
  m=fixture();m['physical_wall_network']['source_aliases']['A.shared'].reverse()
  self.assertEqual(assess(m,digest(m))['state'],'WALL_RECORD_REFERENCE_AND_MATERIAL_UNION_VALID_ONLY')
 def test_bound_projection_retains_namespace_and_decimal_value(self):
  m=fixture();m['wall_hosts']['A.shared'][0]='0.000';out=assess(m,digest(m))
  row=next(r for r in out['projection']['records'] if r['source_path']==['wall_hosts','A.shared'])
  self.assertEqual(row['namespace_hint_by_source_id'],'A');self.assertIs(row['ownership_attribution_verified'],False);self.assertEqual(row['canonical_rectangle'][0],'0');self.assertEqual(row['source_value_digest'],digest(m['wall_hosts']['A.shared']))
if __name__=='__main__':unittest.main()
