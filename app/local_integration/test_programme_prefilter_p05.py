import copy,json,unittest
from fractions import Fraction as Q
from unittest.mock import patch
import programme_prefilter_p05 as p
from dimension_contract import InputError
def body(w='18',l='20',units=2):return json.dumps({'W':w,'L':l,'n':units}).encode()
def core(w='13',l='6'):
 return p.prepare_core(p.CORE_ENTRY,body(w,l))['core']
class NetCapacityP05(unittest.TestCase):
 def test_named_historical_stops_actual_source_preflight_only(self):
  with patch('subprocess.Popen',side_effect=AssertionError('no spawn')) as spawn:
   for w,l,old,gross in (('13','6','15.3125','19.735'),('18','5','12.6875','24.36'),('10','5','6.8875','6.96')):
    with self.subTest(w=w,l=l):
     r=p.inspect_request(body(w,l));self.assertEqual(r['state'],'MEASURED_SCOPED_NO_FIT_CLAIM',r.get('reason'))
     self.assertEqual(r['historical_module_bound']['bound'],0)
     self.assertEqual(r['historical_module_bound']['state'],'CURRENT_MODULE_PROGRAM_BOUND_EMPTY_NOT_GLOBAL_INFEASIBILITY')
     self.assertEqual(r['historical']['bedroom_choices'],[1,2,3,4])
     for unit in r['per_unit'].values():
      self.assertEqual(Q(unit['historical_source_box_m2']),Q(old))
      self.assertEqual(Q(unit['owned_union_m2']),Q(gross))
      self.assertEqual(Q(unit['fixed_union_overlap_m2']),0)
      self.assertEqual(Q(unit['geometric_area_after_known_fixed_deductions_m2']),Q(gross))
      self.assertEqual(unit['geometric_double_bedroom_area_quotient_not_count'],int(Q(gross)/Q('19.62')))
      self.assertEqual(unit['geometric_area_comparison'],'BELOW_SOURCE_MODULE_AREA_BOUND')
     self.assertIs(r['fit_verified'],False);self.assertIs(r['global_infeasibility_proven'],False)
   spawn.assert_not_called()
 def test_exact_union_duplicate_and_overlap(self):
  a,b=p.rectangle(['0','0','2','2']),p.rectangle(['1','0','3','2'])
  self.assertEqual(p.union_area([a,b,a]),Q(6))
  self.assertEqual(p.overlap_area([a,a],[b,b]),Q(2))
  c=core();r,_=p.ownership_metrics(c,Q(13),Q(6))
  c['unit_ownership']['A'].append(copy.deepcopy(c['unit_ownership']['A'][0]))
  self.assertEqual(p.ownership_metrics(c,Q(13),Q(6))[0],r)
 def test_fixed_common_and_walls_subtracted_once_only(self):
  c=core();c['unit_ownership']['A'].append(['2.2','1.475','3','2'])
  r,keys=p.ownership_metrics(c,Q(13),Q(6));a=r['A']
  self.assertIn('stair.bottom',keys);self.assertIn('A.boundary.left',keys)
  self.assertEqual(Q(a['fixed_core_overlap_m2']),Q('.18'))
  self.assertEqual(Q(a['fixed_wall_overlap_m2']),Q('.24'))
  self.assertEqual(Q(a['fixed_union_overlap_m2']),Q('.42'))
  self.assertEqual(Q(a['geometric_area_after_known_fixed_deductions_m2']),Q('19.735'))
 def test_cross_unit_overlap_fails_closed(self):
  c=core();c['unit_ownership']['A'].append(c['units']['B'])
  with self.assertRaisesRegex(p.MissingEvidence,'CROSS_UNIT_OWNERSHIP_OVERLAP'):p.ownership_metrics(c,Q(13),Q(6))
 def test_missing_known_evidence_is_profile_not_ready(self):
  for field in ('unit_ownership','outside_band_unit_separator_y','lobby'):
   with self.subTest(field=field):
    original=p.prepare_core(p.CORE_ENTRY,body())
    del original['core'][field]
    with patch.object(p,'prepare_core',return_value=original),patch.object(p,'source_guard',return_value={}):
     r=p.inspect_request(body());self.assertEqual(r['state'],'PROFILE_NOT_READY');self.assertNotIn('per_unit',r)
  self.assertEqual(p.inspect_request(body('5','5'))['reason'],'CURRENT_CORE_METHOD_NO_FIT_NOT_INFEASIBLE')
 def test_sufficient_area_is_not_dimension_fit(self):
  r=p.inspect_request(body('25','10'));self.assertEqual(r['state'],'MEASURED_SCOPED_NO_FIT_CLAIM',r.get('reason'))
  self.assertEqual(Q(r['necessary_disjoint_module_area_m2']),Q('69.25'))
  for u in r['per_unit'].values():
   self.assertEqual(u['geometric_area_comparison'],'AREA_NOT_BELOW_BOUND_NOT_FIT')
   self.assertEqual(u['source_box_comparison'],'AREA_NOT_BELOW_BOUND_NOT_FIT')
   self.assertIn('twin',u['modules_not_fitting_source_box_dimensions'])
  self.assertTrue(all(r[k] is False for k in ('accepted','qualified','delivery_allowed','display_allowed','fit_verified','dispatch_authorized')))
 def test_programmes_not_inferred_or_replaced(self):
  one=p.inspect_request(body(),'PROGRAM_1BED_V1')
  self.assertEqual(Q(one['necessary_disjoint_module_area_m2']),Q('44.725'))
  self.assertEqual(p.inspect_request(body(),'PROGRAM_3BED_V1')['reason'],'PROGRAMME_PROFILE_NOT_READY')
  self.assertEqual(p.inspect_request(body(units=1))['reason'],'ONLY_COMPACT_FRONT_REAR_N2_DIAGNOSTIC')
  with self.assertRaises(InputError):p.inspect_request(body(units=3))
  with self.assertRaises(InputError):p.inspect_request(body(18.1,'22.2'))
 def test_source_changed_or_shadowed_stays_unknown(self):
  snap=p.source_guard();self.assertIn('app/reconstruction357/planha_general150_runtime_work/assemble114.py',snap)
  with patch.object(p,'source_guard',side_effect=[snap,{}]):
   r=p.inspect_request(body());self.assertEqual(r['reason'],'SOURCE_CHANGED_DURING_OBSERVATION')
  with patch.object(p,'prepare_core',lambda *_:None):
   r=p.inspect_request(body());self.assertEqual(r['reason'],'ACTUAL_SOURCE_PATH')
 def test_decimal_wire_keeps_ratios_and_original_digest(self):
  a=p.inspect_request(body('18.1','22.2'));b=p.inspect_request(body('۱۸٫۱۰','22.20'))
  self.assertEqual(a['state'],'MEASURED_SCOPED_NO_FIT_CLAIM',a.get('reason'))
  self.assertEqual(a['core_digest'],b['core_digest']);self.assertEqual(a['request_digest'],b['request_digest'])
  self.assertNotEqual(a['transport_body_sha256'],b['transport_body_sha256'])
if __name__=='__main__':unittest.main()
