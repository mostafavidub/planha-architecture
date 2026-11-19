"""Synthetic projection contract tests. No private models or producer execution."""
import ast,copy,hashlib,itertools,pathlib,sys,unittest
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'app/local_integration'))
from declared_geometry_projection_study import SCHEMA,FIELD_ROLES,CONTRACT,POINT_FIELDS,VECTOR_FIELDS,RECT_FIELDS,PATH_FIELDS,check,validate,transform,inverse,digest,compose
def fixture():
 def r(id,field,value,unit='A'):return {'unit_id':unit,'id':id,'source_field':field,'value':value}
 return {'schema':SCHEMA,'units':['A','B'],'records':[
  r('wall','walls',['0.125','1.375','12.625','20.875']),
  r('opening','openings.rect',['0.125','1.375','0.275','2.075']),
  r('hand','operations.hand_point',['1.125','2.375']),
  r('direction','operations.normal',['0','1']),
  r('walk','units.routes',[['0.125','1.375'],['3.625','1.375'],['3.625','4.875']]),
  r('module','module_placements.transform',{'matrix':[[0,-1],[1,0]],'translation':['1.125','2.375']}),
  r('canonical','operations.canonical_isometry',{'matrix':[[1,0],[0,-1]],'translation':['0.125','-1.375']}),
  r('wall','walls',['1','2','3','4'],'B')]}
class Projection(unittest.TestCase):
 def test_declared_field_categories_match_pinned_source(self):
  b=(ROOT/'app/reconstruction357/planha_general150_runtime_work/world_transform125.py').read_bytes()
  self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'b7e02236a057316998ae3c7d14cb0ddf94bd4879')
  wanted={'POINT_KEYS':set(POINT_FIELDS),'VECTOR_KEYS':set(VECTOR_FIELDS),'RECT_KEYS':set(RECT_FIELDS),'PATH_KEYS':set(PATH_FIELDS)}
  found={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(b).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in wanted}
  self.assertEqual(found,wanted)
 def test_complete_synthetic_fixture_and_authority(self):
  v=fixture();out=check(v);self.assertEqual(out['state'],'DECLARED_PROJECTION_VALID_ONLY')
  self.assertEqual(out['projection_digest'],digest(v))
  for k in ('source_completeness_verified','physical_verified','accepted','qualified','delivery_allowed'):self.assertIs(out[k],False)
 def test_eight_d4_nonzero_translation_inverse_all_roles(self):
  v=fixture();frozen=digest(v)
  for swap in (False,True):
   for a,b in itertools.product((-1,1),repeat=2):
    t={'matrix':[[0,a],[b,0]] if swap else [[a,0],[0,b]],'translation':['12.125','-3.375']}
    out=transform(v,t);back=transform(out,inverse(t))
    self.assertEqual(digest(back),frozen);self.assertEqual(digest(v),frozen)
 def test_translation_point_not_vector(self):
  out=transform(fixture(),{'matrix':[[1,0],[0,1]],'translation':['10','20']})
  r={x['id']:x for x in out['records']}
  self.assertEqual(r['hand']['value'],['11.125','22.375']);self.assertEqual(r['direction']['value'],['0','1'])
 def test_placement_and_canonical_composition(self):
  t={'matrix':[[0,1],[1,0]],'translation':['10','20']};p=fixture();out=transform(p,t)
  self.assertEqual(out['records'][5]['value'],{'matrix':[[1,0],[0,-1]],'translation':['12.375','21.125']})
  self.assertEqual(out['records'][6]['value'],{'matrix':[[0,1],[-1,0]],'translation':['-19.875','8.625']})
 def test_coordinate_frame_invariants_on_independent_point(self):
  def apply(t,p):
   return [sum(F(t['matrix'][i][j])*p[j] for j in range(2))+F(t['translation'][i]) for i in range(2)]
  v=fixture();t={'matrix':[[0,-1],[1,0]],'translation':['12.125','-3.375']};out=transform(v,t);q=[F('1.625'),F('-0.375')]
  self.assertEqual(apply(out['records'][6]['value'],apply(t,q)),apply(v['records'][6]['value'],q))
  self.assertEqual(apply(out['records'][5]['value'],q),apply(t,apply(v['records'][5]['value'],q)))
 def test_unknown_fields_and_roles_fail_closed(self):
  for mutate in (lambda v:v.update(extra=1),lambda v:v['records'][0].update(extra=1),lambda v:v['records'][5]['value'].update(extra=1),lambda v:v['records'][0].update(source_field='operations.unregistered')):
   v=fixture();mutate(v);self.assertEqual(check(v)['state'],'INVALID_DECLARED_PROJECTION')
 def test_duplicate_namespace_and_reference(self):
  for mutate in (lambda v:v['units'].__setitem__(1,'A'),lambda v:v['records'].append(copy.deepcopy(v['records'][0])),lambda v:v['records'][0].update(unit_id='C'),lambda v:v['records'][0].update(unit_id=True)):
   v=fixture();mutate(v);self.assertEqual(check(v)['state'],'INVALID_DECLARED_PROJECTION')
 def test_typed_numeric_and_tuple_rejection(self):
  for bad in (1,1.0,True,'nan','1e0','01','1.0','-0'):
   v=fixture();v['records'][2]['value'][0]=bad;self.assertEqual(check(v)['state'],'INVALID_DECLARED_PROJECTION')
  v=fixture();v['records'][2]['value']=tuple(v['records'][2]['value']);self.assertEqual(check(v)['state'],'INVALID_DECLARED_PROJECTION')
 def test_bad_matrix_and_degenerate_rect(self):
  for m in ([[1,1],[0,0]],[[True,0],[0,1]],[[1.0,0],[0,1]],[[.5,.5],[.5,.5]]):
   v=fixture();v['records'][5]['value']['matrix']=m;self.assertEqual(check(v)['state'],'INVALID_DECLARED_PROJECTION')
  v=fixture();v['records'][0]['value'][2]=v['records'][0]['value'][0];self.assertEqual(check(v)['state'],'INVALID_DECLARED_PROJECTION')
 def test_missing_required_role_is_not_complete_fixture(self):
  v=fixture();v['records']=[r for r in v['records'] if FIELD_ROLES[r['source_field']]!='vector']
  self.assertEqual(check(v)['state'],'INVALID_DECLARED_PROJECTION')
 def test_mutation_changes_bound_digest(self):
  v=fixture();before=check(v)['projection_digest'];v['records'][2]['value'][0]='1.25'
  self.assertNotEqual(check(v)['projection_digest'],before)
if __name__=='__main__':unittest.main()
