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
class CapacityHTTP(unittest.TestCase):
 def setUp(self):
  import threading,public_wln_server as server
  self.server=server
  self.socket=server.server(0)
  self.thread=threading.Thread(target=self.socket.serve_forever,daemon=True);self.thread.start()
  self.spawn=patch('subprocess.Popen',side_effect=AssertionError('P05_NO_SOLVER'))
  self.spy=self.spawn.start();self.addCleanup(self.spawn.stop)
 def tearDown(self):
  self.socket.shutdown();self.socket.server_close();self.thread.join(timeout=5)
  self.spy.assert_not_called();self.assertFalse(self.server.LOCK.locked())
 def post(self,raw):
  import http.client
  c=http.client.HTTPConnection('127.0.0.1',self.socket.server_port,timeout=15)
  try:
   c.request('POST','/api/public/plan',raw,{'Content-Type':'application/json'})
   r=c.getresponse();return r.status,json.loads(r.read())
  finally:c.close()
 def assert_bound(self,raw,row):
  import hashlib
  self.assertEqual(row['request_digest'],hashlib.sha256(raw).hexdigest())
  self.assertEqual(p.freeze_http({k:v for k,v in row.items() if k!='observation_digest'})[1],row['observation_digest'])
  self.assertIs(row['fit_verified'],False);self.assertIs(row['dispatch_authorized'],False)
 def test_named_cases_real_http_unchanged_unsupported_no_worker(self):
  with patch.object(self.server,'run_bound',side_effect=AssertionError('unexpected worker')) as work:
   for w,l,gross,quotient in (('13','6','19.735',1),('18','5','24.36',1),('10','5','6.96',0)):
    raw=body(w,l);status,out=self.post(raw)
    self.assertEqual(status,409);self.assertEqual(out['status'],'UNSUPPORTED_SELECTED_SAME_VERSION_CASE')
    self.assertIs(out['input_valid'],True);self.assertEqual(out['actual_live_attempts'],0)
    row=out['capacity_observation'];self.assert_bound(raw,row)
    self.assertEqual(row['state'],'MEASURED_SCOPED_NO_FIT_CLAIM')
    self.assertEqual(row['historical_module_area_bound'],0)
    self.assertEqual(Q(row['per_unit']['A']['owned_union_m2']),Q(gross))
    self.assertEqual(row['per_unit']['A']['geometric_double_bedroom_area_quotient_not_count'],quotient)
    self.assertNotIn('sources',row);self.assertNotIn('model',row)
   raw=body('25','10');status,out=self.post(raw)
   self.assertEqual(status,409)
   row=out['capacity_observation'];self.assert_bound(raw,row)
   self.assertEqual(row['per_unit']['A']['geometric_area_comparison'],'AREA_NOT_BELOW_BOUND_NOT_FIT')
   self.assertIn('twin',row['per_unit']['A']['modules_not_fitting_source_box_dimensions'])
   work.assert_not_called()
 def test_invalid_and_n1_skip_observation_and_producer(self):
  with patch.object(p,'capture_http',side_effect=AssertionError('must not observe')) as cap,patch.object(self.server,'run_bound',side_effect=AssertionError('no dispatch')) as run:
   for raw,expected in [(body('4.999','20'),422),(body('18','20',3),422),(body(18.1,'22.2'),409),(body('17','20',1),409)]:
    status,out=self.post(raw)
    self.assertEqual(status,expected);self.assertNotIn('capacity_observation',out)
   cap.assert_not_called();run.assert_not_called()
 def controlled(self,raw,runtime,*,deadline):
  pf=self.server.preflight(raw)
  return {'state':'CONTROLLED_NO_MODEL','preflight':pf,'source_integrity_verified':True,'attempts':[],**p.AUTH}
 def test_ready_n2_observed_and_n1_not_observed_without_changing_receipt(self):
  for n in (2,1):
   raw=body(units=n)
   with patch.object(self.server,'run_bound',side_effect=self.controlled) as run:
    status,out=self.post(raw);self.assertEqual(status,200);run.assert_called_once()
   self.assertEqual(out['status'],'CONTROLLED_NO_MODEL')
   self.assertEqual(out['decision']['state'],'NO_VERIFIED_DECISION');self.assertEqual(out['plan_count_available'],0)
   if n==2:self.assert_bound(raw,out['capacity_observation'])
   else:self.assertNotIn('capacity_observation',out)
 def test_observer_exception_does_not_deny_ready_dispatch(self):
  raw=body()
  with patch.object(p,'capture_http',side_effect=RuntimeError('PRIVATE_DIAGNOSTIC')),patch.object(self.server,'run_bound',side_effect=self.controlled) as run:
   status,out=self.post(raw)
   self.assertEqual(status,200);run.assert_called_once()
  row=out['capacity_observation'];self.assert_bound(raw,row)
  self.assertEqual(row['state'],'PROFILE_NOT_READY');self.assertNotIn('PRIVATE_DIAGNOSTIC',json.dumps(out))
 def test_frozen_no_alias_binding_and_rehashed_private_metadata_rejected(self):
  raw=body('13','6')
  env=p.parse_public(raw)
  report=p.inspect_request(raw)
  with patch.object(p,'inspect_request',return_value=report):snapshot=p.capture_http(raw,env)
  report['per_unit']['A']['owned_union_m2']='0'
  out=p.attach_http({'status':'ORIGINAL','qualified':True},raw,snapshot)
  self.assertEqual(Q(out['capacity_observation']['per_unit']['A']['owned_union_m2']),Q('19.735'))
  self.assertIs(out['qualified'],True)
  for wire,frozen in ((body('10','5'),snapshot),(raw,(snapshot[0]+b' ',snapshot[1]))):
   self.assertEqual(p.attach_http({},wire,frozen)['capacity_observation']['state'],'PROFILE_NOT_READY')
  forged=json.loads(snapshot[0]);forged['per_unit']['A']['private']='PRIVATE_PAYLOAD'
  r=p.attach_http({},raw,p.freeze_http(forged))['capacity_observation']
  self.assertEqual(r['state'],'PROFILE_NOT_READY');self.assertNotIn('PRIVATE_PAYLOAD',json.dumps(r))
  with patch.object(p,'source_guard',return_value={}):
   self.assertEqual(p.attach_http({},raw,snapshot)['capacity_observation']['state'],'PROFILE_NOT_READY')
if __name__=='__main__':unittest.main()
