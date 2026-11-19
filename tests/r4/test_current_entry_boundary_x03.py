import copy,importlib,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ENGINE),str(ROOT/'frontend')]
import current_entry_boundary_x03 as boundary
from dimension_contract import InputError
def body(W='18',L='22',**extra):return json.dumps(dict(W=W,L=L,n=2,**extra),allow_nan=False).encode()
class Reached(RuntimeError):pass
class BoundaryTests(unittest.TestCase):
 def test_each_axis_bounds_and_exact_types(self):
  for axis in ('W','L'):
   for v in ('5','25','18.125'):
    x={'W':'18','L':'22','n':2};x[axis]=v
    self.assertTrue(boundary.check_model_domain({'inputs':[x['W'],x['L'],x['n']]})['input_valid'])
   for v in ('4.999','25.001',True,None,25.001,'NaN','Infinity'):
    x={'W':'18','L':'22','n':2};x[axis]=v
    with self.assertRaises((ValueError,InputError)):boundary.check_model_domain({'inputs':[x['W'],x['L'],x['n']]})
 def test_invalid_new_dispatch_zero_import_and_solver(self):
  bad=[body(W='25.001'),body(L='25.001'),body(W='4.999'),body(L='4.999'),body(W=True),
       b'{"W":18,"W":19,"L":22,"n":2}',b'{"W":NaN,"L":22,"n":2}',b'{"W":18,"L":Infinity,"n":2}',
       b'{"W":18,"L":22,"n":true}',body(capability=True),body(source='forged')]
  for b in bad:
   for run in (lambda:boundary.propose_current(b),lambda:boundary.construct_current(b,{})):
    with patch.object(boundary.importlib,'import_module',side_effect=Reached)as called:
     with self.assertRaises((ValueError,InputError)):run()
     called.assert_not_called()
 def test_valid_unsupported_not_invalid(self):
  with self.assertRaises(InputError)as c:boundary.propose_current(b'{"W":18,"L":22,"n":1}')
  self.assertEqual(c.exception.status,409)
  with self.assertRaisesRegex(ValueError,'CURRENT_CORE_METHOD_NO_FIT'):boundary.propose_current(body(W='5'))
 def test_unknown_entry_and_capability_disabled(self):
  for value in ('contract114.parse','search114.propose','unknown',{'method':'source_fit_candidate207.propose'},True):
   with self.assertRaisesRegex(ValueError,'UNREGISTERED_CURRENT_ENTRY_DISABLED'):boundary.entry(value)
  with self.assertRaises(InputError):boundary.propose_current(body(mode='HISTORICAL'))
 def test_prepared_rebuild_not_self_digest(self):
  b=body();p=boundary.prepare('SOURCE_FIT207_COMPACT_PAIR',b)
  self.assertEqual(boundary.validate_prepared(p,b),p)
  for key,value in [('raw',{'W':'26','L':'22','n':2,'requested_count':1}),('core',{}),('profile',{}),('sources',{}),('rule',{'mode':'CURRENT_PRODUCT'})]:
   q=copy.deepcopy(p);q[key]=value
   with self.assertRaisesRegex(ValueError,'CURRENT_REQUEST_BINDING'):boundary.validate_prepared(q,b)
  q=copy.deepcopy(p);q['capability']=True
  with self.assertRaisesRegex(ValueError,'CURRENT_REQUEST_BINDING'):boundary.validate_prepared(q,b)
 def test_valid_producer_real_path_stops_before_milp(self):
  import source_fit_candidate207 as fit
  with patch.object(fit,'milp',side_effect=Reached('MILP_SENTINEL'))as call:
   with self.assertRaisesRegex(Reached,'MILP_SENTINEL'):boundary.propose_current(body(),seconds=1)
   self.assertEqual(call.call_count,1)
 def test_valid_constructor_real_frame_stops_before_assembly(self):
  import constructor127
  p={'bedrooms':2,'sleep_roles':['double','twin']}
  with patch.object(constructor127,'assemble',side_effect=Reached('ASSEMBLY_SENTINEL'))as call:
   with self.assertRaisesRegex(Reached,'ASSEMBLY_SENTINEL'):boundary.construct_current(body(),{'A':p,'B':p})
   self.assertEqual(call.call_count,1)
 def test_direct_guard_parser_actual_import_path(self):
  import public_wln_contract
  with patch.object(public_wln_contract,'parse_public',lambda b: {}):
   with self.assertRaisesRegex(ValueError,'CURRENT_BOUNDARY_IMPORT_PATH'):
    boundary.check_model_domain({'inputs':['18','22',2]})
 def test_source_changed_blocks_before_producer(self):
  path=next(iter(boundary.SOURCE_PINS))
  with patch.dict(boundary.SOURCE_PINS,{path:'0'*40}):
   with self.assertRaisesRegex(ValueError,'CURRENT_BOUNDARY_SOURCE_CHANGED'):boundary.propose_current(body())
 def test_frozen_26_remains_historical_not_current(self):
  from contract114 import parse
  raw={'W':'26','L':'22','n':2,'requested_count':1}
  self.assertEqual(parse(raw)[0],26)
  m={'inputs':['26','22',2]};r={'status':'PASS_CONCEPT_SCOPED_REVIEW','model_hash':boundary.digest(m),'errors':[],'pending':[]}
  with self.assertRaises(InputError):boundary.bind_current_evidence(body(),m,r,boundary.digest(m),boundary.digest(r))
 def test_report_same_source_different_request_rejected(self):
  m={'inputs':['18','22',2]};r={'status':'PASS_CONCEPT_SCOPED_REVIEW','model_hash':boundary.digest(m)}
  out=boundary.bind_current_evidence(body(),m,r,boundary.digest(m),boundary.digest(r))
  self.assertFalse(out['qualified']);self.assertFalse(out['authenticity_verified'])
  with self.assertRaisesRegex(ValueError,'CURRENT_MODEL_REQUEST_MISMATCH'):
   boundary.bind_current_evidence(body(W='19'),m,r,boundary.digest(m),boundary.digest(r))
  with self.assertRaisesRegex(ValueError,'CURRENT_REPORT_MODEL_BINDING'):
   q=dict(r,model_hash='0'*64);boundary.bind_current_evidence(body(),m,q,boundary.digest(m),boundary.digest(q))
 def test_all_four_direct_assess_and_decision_enforce_before_transport(self):
  names=('current_programme_evaluator','source_guest_route_evaluator','source_living_evaluator','source_wall_function_evaluator','current_four_decision')
  for name in names:
   mod=importlib.import_module(name)
   def call(bundle):
    return mod.assemble(bundle,{}, {})if name=='current_four_decision'else mod.assess(bundle)
   for axis in (0,1):
    for value in ('4.999','25.001',True,'NaN'):
     inp=['18','22',2];inp[axis]=value
     with patch.object(mod,'transport',side_effect=Reached)as transport:
      with self.assertRaises((ValueError,InputError)):call({'packet':{'world_model':{'inputs':inp}}})
      transport.assert_not_called()
    for value in ('5','25'):
     inp=['18','22',2];inp[axis]=value
     with patch.object(mod,'transport',side_effect=Reached)as transport:
      with self.assertRaises(Reached):call({'packet':{'world_model':{'inputs':inp}}})
      self.assertEqual(transport.call_count,1)
 def test_raw_direct_repair_rejects_before_constructor(self):
  import parametric_repair,parametric_route_repair,parametric_repair_flow
  for axis in ('W','L'):
   for value in ('4.999','25.001',True):
    raw={'W':'18','L':'22','n':2,'requested_count':1};raw[axis]=value
    calls=[lambda:parametric_repair.propose(raw,None,None,None,None,None,None),
      lambda:parametric_repair.verify_child(raw,None,None,None,None,None),
      lambda:parametric_route_repair.propose_route(raw,None,None,None,None,None,None),
      lambda:parametric_repair_flow.attempt(raw,None,None,None,None,None,None)]
    for call in calls:
     with self.assertRaises((ValueError,InputError)):call()
 def test_inventory_is_static_and_pinned(self):
  from current_entry_inventory_x03 import scan
  result=scan();self.assertGreater(len(result['rows']),200)
  self.assertEqual(result['literal_legacy_import_isolation'],'NOT_IMPLEMENTED')
if __name__=='__main__':unittest.main()
