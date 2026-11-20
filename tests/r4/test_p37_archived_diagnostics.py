"""Only synthetic location/renderer consistency fixtures. No model/evaluator."""
import copy,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'studies'))
import p37_archived_diagnostics as p
def h(x):return p.digest(['P37_FIXTURE_ONLY',x])
def world(c):
 return {'schema':'P37_FRONT_REAR_WORLD_FRAME_V1','unit':'metre','axes':['WORLD_X_RIGHT','WORLD_Y_UP'],
   'origin':['0','0'],'model_digest':c['model_digest'],'context_digest':h('construction context')}
def pointer(i):
 return {'namespace':'errors','ordinal':0,'child_index':i,'source_record_sha256':h('parent raw'),'child_record_sha256':h('child '+str(i))}
def ledger(original):
 names={k:[]for k in p.NAMESPACES}
 names['errors']=[{'ordinal':0,'code':'MISSING_REQUIRED_ACTIVITY_ROUTES','rule_id':None,'source_record_sha256':h('parent raw'),
   'child_occurrences':[{'unit':uid,'child_index':i,'child_record_sha256':h('child '+str(i))}for i,uid in enumerate(('A','B'))]}]
 for k in ('original_pending','not_evaluated'):
  names[k]=[{'ordinal':0,'code':'SYNTHETIC_DOUBLE_SCOPE','rule_id':None,'source_record_sha256':h('same evidence, separate namespaces'),'child_occurrences':[]}]
 return {'schema':'P37_ORIGINAL_LEDGER_V1','original_report_digest':original,'namespaces':names}
def sample():
 original=h('original')
 l=ledger(original)
 ctx={'schema':'P37_ARCHIVE_CONTEXT_V1','model_digest':h('model'),'frame_digest':h('frame'),'source_digest':h('source'),
      'original_report_digest':original,'request_digest':h('request'),'original_ledger_digest':p.digest(l)}
 ctx['frame_digest']=p.digest(world(ctx))
 common={k:ctx[k]for k in ('model_digest','frame_digest','source_digest','original_report_digest')}
 def finding(fid,code,scope,detail,variant=None,boxes=None):
  return {'schema':'P37_TYPED_FINDING_V1','finding_id':fid,'code':code,'scope':scope,'unit':'A',
   'evidence_digest':h(fid),**common,'variant_digest':variant,
   'layers':{k:next(iter(v))for k,v in p.LAYER_CODES[scope].items()}if scope in p.LAYER_CODES else dict.fromkeys(p.LAYERS,'NOT_OBSERVED'),
   'geometry':None if boxes is None else {'model_digest':ctx['model_digest'],'frame_digest':ctx['frame_digest'],'variant_digest':variant,'boxes':boxes},
   'detail':detail}
 def geo(labels):
  return [{'kind':k,'rect':['1','2','8/5','3']if k=='detached_aperture'else['1','2','3','4'],'unit':'A',
    'element_ref':'kitchen_motion:4'if k=='kitchen_motion_overlap'else'A.entry',
    'element_binding':'SOURCE_ROLE_INDEX_ONLY'if k=='kitchen_motion_overlap'else'SOURCE_OPENING_ID',
    'segment_index':None if k=='detached_aperture'else i,'area_m2':'3/5'if k=='detached_aperture'else'4'}
    for i,k in enumerate(labels)]
 facts=[finding('missing','MISSING_REQUIRED_ACTIVITY_ROUTES',p.ACTUAL,{'route':'guest_dining','reason':'NO_CONNECTED_BODY_ROUTE','profile':p.PROFILE,'original_pointer':pointer(0)}),
   finding('proposed','PLANNED_ENTRY_PANEL_AND_KITCHEN_MOTION',p.PLANNED,{'route':'guest_dining','profile':p.PROFILE,'body_m':'7/10'},boxes=geo(['entry_panel_overlap','kitchen_motion_overlap'])),
   finding('detached','NO_BODY_CROSSING_BETWEEN_DECLARED_REGIONS',p.DETACHED,{'opening_id':'A.entry','host_id':'A.unit_boundary',
     'original_width_m':'13/10','detached_width_m':'3/5','body_m':'7/10','width_deficit_m':'1/10','operation_mode':'SOURCE_LINEAR_SLIDE_NO_HINGE','aperture_axis':'WORLD_X','opening_before_digest':h('before'),
     'opening_after_digest':h('after'),'operation_after_digest':h('motion')},
     variant=h('variant'),boxes=geo(['detached_aperture'])),finding('unmapped','UNKNOWN_FIXTURE_CODE','UNSUPPORTED',None)]
 other=copy.deepcopy(facts[0]);other.update(unit='B',finding_id='missing-b');other['detail']['original_pointer']=pointer(1)
 facts.append(other)
 return ctx,facts,l
def anchor(ctx,facts):
 return {'schema':'P37_EXTERNAL_ARCHIVE_MANIFEST_V1','context_digest':p.digest(ctx),'finding_digests':{x['finding_id']:p.digest(x)for x in facts}}
def show(ctx,facts,l,anchor_fixture=None,expected=None):
 a=anchor(ctx,facts)if anchor_fixture is None else anchor_fixture
 return p.report(ctx,world(ctx),facts,l,trusted_manifest=a,expected_manifest_digest=p.digest(a)if expected is None else expected)
class P37DiagnosticTests(unittest.TestCase):
 def test_separate_original_missing_plan_and_detached(self):
  ctx,fs,l=sample();before=p.digest([ctx,fs,l]);out=show(ctx,fs,l)
  self.assertEqual([x['location_status']for x in out['findings']],['NOT_LOCALIZABLE','LOCATED_PLANNED_WITNESS','LOCATED_DETACHED_CONTROL','UNSUPPORTED_CODE','NOT_LOCALIZABLE'])
  self.assertEqual(out['findings'][0]['reason'],'MISSING_EVIDENCE');self.assertIsNone(out['findings'][0]['geometry_digest'])
  self.assertIn('علت یکتا اثبات نشده است',out['persian_report']);self.assertIn('۰٫۱ متر کم است',out['persian_report'])
  self.assertEqual(p.digest([ctx,fs,l]),before);self.assertTrue(all(not out[k]for k in p.AUTH))
 def test_namespaces_keep_exact_duplicate_distinct(self):
  c,fs,l=sample();o=show(c,fs,l)['original_report_namespaces']
  self.assertEqual(o['original_pending'],o['not_evaluated']);self.assertEqual(len(o['pending']),0)
  self.assertIn('out_of_scope',o)
  moved=copy.deepcopy(l);moved['namespaces']['not_evaluated'].clear()
  with self.assertRaisesRegex(ValueError,'P37_ORIGINAL_LEDGER_BINDING'):show(c,fs,moved)
 def test_independent_manifest_digest_not_forged_by_rehash(self):
  c,fs,l=sample();a=anchor(c,fs);prior=p.digest(a)
  fs[1]['geometry']['boxes'][0]['rect'][2]='4'
  with self.assertRaisesRegex(ValueError,'P37_FINDING_UNPINNED'):show(c,fs,l,a,prior)
  with self.assertRaisesRegex(ValueError,'P37_INDEPENDENT_MANIFEST'):show(c,fs,l,anchor(c,fs),prior)
 def test_model_frame_source_report_binding_are_independent_even_rehashed(self):
  for field in ('model_digest','frame_digest','source_digest','original_report_digest'):
   c,f,l=sample();f[0][field]=h('other')
   with self.assertRaisesRegex(ValueError,'P37_FINDING_BASIS'):show(c,f,l)
 def test_original_missing_and_unsupported_cannot_get_geometry(self):
  c,f,l=sample();f[0]['geometry']=f[1]['geometry']
  with self.assertRaisesRegex(ValueError,'P37_MISSING_EVIDENCE_MUST_NOT_LOCALIZE'):show(c,f,l)
  c,f,l=sample();f[3]['geometry']=f[1]['geometry']
  with self.assertRaisesRegex(ValueError,'P37_UNSUPPORTED_MUST_NOT_LOCALIZE'):show(c,f,l)
 def test_detached_explicit_different_variant_and_bound_widths(self):
  c,f,l=sample();f[2]['variant_digest']=c['model_digest']
  with self.assertRaisesRegex(ValueError,'P37_DETACHED_VARIANT'):show(c,f,l)
  c,f,l=sample();f[2]['detail']['detached_width_m']='0.8'
  with self.assertRaisesRegex(ValueError,'P37_DETACHED_WIDTHS'):show(c,f,l)
 def test_planned_body_size_is_source_contract(self):
  c,f,l=sample();f[1]['detail']['body_m']='1'
  with self.assertRaisesRegex(ValueError,'P37_PLANNED_METHOD_DETAIL'):show(c,f,l)
 def test_overlay_geometry_frame_and_kind_exact(self):
  c,f,l=sample();f[1]['geometry']['frame_digest']=h('other frame')
  with self.assertRaisesRegex(ValueError,'P37_GEOMETRY_BASIS'):show(c,f,l)
  c,f,l=sample();f[1]['geometry']['boxes'][0]['kind']='not_allowed'
  with self.assertRaisesRegex(ValueError,'P37_GEOMETRY_KIND'):show(c,f,l)
 def test_zero_or_inverted_or_nonfinite_geometry_rejected(self):
  for v,code in (('1/0','P37_RATIONAL_COORDINATE'),('0','P37_BOX_POSITIVE'),('inf','P37_RATIONAL_COORDINATE')):
   c,f,l=sample();f[1]['geometry']['boxes'][0]['rect'][2]=v
   with self.assertRaisesRegex(ValueError,code):show(c,f,l)
 def test_witness_minimal_svg_only_and_old_missing_has_no_overlay(self):
  c,f,l=sample();a=anchor(c,f);z=p.overlay(c,world(c),f[1],trusted_manifest=a,expected_manifest_digest=p.digest(a))
  tree=ET.fromstring(z['svg']);self.assertEqual(len(tree),3);self.assertEqual(z['finding_id'],'proposed')
  self.assertTrue(all('svg' in o.tag for o in tree));self.assertNotIn('href',z['svg']);self.assertFalse(z['whole_model_embedded'])
  for y in (f[0],f[3]):
   with self.assertRaisesRegex(ValueError,'P37_OVERLAY_NO_VERIFIED_LOCATION'):
    p.overlay(c,world(c),y,trusted_manifest=a,expected_manifest_digest=p.digest(a))
 def test_occurrence_pin_and_unit_uniqueness(self):
  c,f,l=sample();f[0]['detail']['original_pointer']['child_record_sha256']=h('foreign raw')
  with self.assertRaisesRegex(ValueError,'P37_ORIGINAL_RAW_RECORD_BINDING'):show(c,f,l)
  c,f,l=sample();f[-1]['detail']['original_pointer']=copy.deepcopy(f[0]['detail']['original_pointer'])
  with self.assertRaisesRegex(ValueError,'P37_ORIGINAL_POINTER_UNIQUE'):show(c,f,l)
 def test_own_unit_element_and_detached_width_and_world_affine(self):
  c,f,l=sample();f[1]['geometry']['boxes'][0]['element_ref']='B.entry'
  with self.assertRaisesRegex(ValueError,'P37_ELEMENT_ID_OR_ROLE'):show(c,f,l)
  c,f,l=sample();b=f[2]['geometry']['boxes'][0];b['rect'][2]='2';b['area_m2']='1'
  with self.assertRaisesRegex(ValueError,'P37_DETACHED_APERTURE_RECT_WIDTH'):show(c,f,l)
  c,f,l=sample();a=anchor(c,f);o=p.overlay(c,world(c),f[1],trusted_manifest=a,expected_manifest_digest=p.digest(a))
  self.assertEqual(o['world_bbox_m'],['1','2','3','4'])
  self.assertEqual(o['world_from_local'],{'matrix':[[1,0],[0,-1]],'translation_m':['1','4']})
  r=show(c,f,l)['findings'][1];self.assertEqual(r['geometry'],f[1]['geometry'])
  wf=world(c);wf['origin']=['1','0']
  with self.assertRaisesRegex(ValueError,'P37_FRAME_DATUM'):p.overlay(c,wf,f[1],trusted_manifest=a,expected_manifest_digest=p.digest(a))
 def test_exact_inventory_cannot_hide_pending_registered_finding(self):
  c,f,l=sample();a=anchor(c,f)
  with self.assertRaisesRegex(ValueError,'P37_FINDING_SET'):show(c,f[:-1],l,a)
if __name__=='__main__':unittest.main()
