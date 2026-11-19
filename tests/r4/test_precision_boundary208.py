"""Synthetic/source input tests; no MILP or private model artifacts."""
import copy,json,sys,unittest
from pathlib import Path
from fractions import Fraction as F
from unittest.mock import Mock,patch
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
from precision_boundary208 import prepare,gated_propose,roundtrip,coordinate_receipt
from front_rear_runtime_adapter import proposal_transport,transport
from dimension_contract import InputError
from same_version_front_rear_contract import digest
class PrecisionTests(unittest.TestCase):
 def body(self,w='18.1',l='22.2',n=2):return json.dumps({'W':w,'L':l,'n':n}).encode()
 def proposal(self):
  names=['bed1','bed2','bath','kitchen','dining','sofa1_use','sofa2_use','chair1_use','chair2_use','entry_apron']
  net=set(names)-{'entry_apron','dining'}|{'dining_front','dining_back','dining_west','dining_east'}
  return {'rectangles':{n:[np.float64('.1'),np.float64('-0.0'),np.float64('1.2'),np.float64('2.3')]for n in names},
   'network_paths':{n:[[np.float64('.1'),np.float64('.2')]for _ in range(5)]for n in sorted(net)},'count':2,'metadata':{'scope':'synthetic-only'}}
 def test_exact_input_ratios_and_engine_raw(self):
  p=prepare(self.body());self.assertEqual(p['ratios'],{'W':['181','10'],'L':['111','5']})
  self.assertEqual(p['raw'],{'W':'18.1','L':'22.2','n':2,'requested_count':1})
 def test_each_axis_inclusive_bounds_not_readiness(self):
  for axis in ('W','L'):
   for edge in ('5','25'):
    d={'W':'18','L':'22','n':2};d[axis]=edge;p=prepare(json.dumps(d).encode())
    self.assertEqual(p['ratios'][axis],[edge,'1'])
 def test_invalid_never_dispatches_exact_live_wrapper(self):
  invalid=[self.body('25.001'),self.body(l='25.001'),self.body(True),self.body(l=False),self.body(n=True),
   b'{"W":NaN,"L":"22","n":2}',b'{"W":"18","L":Infinity,"n":2}',b'{"W":-Infinity,"L":"22","n":2}',
   b'{"W":"18","W":"19","L":"22","n":2}',self.body(n=3)]
  for body in invalid:
   with self.subTest(body_hash=digest(list(body))):
    producer=Mock()
    with self.assertRaises(InputError):gated_propose(body,producer)
    producer.assert_not_called()
 def test_json_numeric_decimal_remains_explicit_unsupported(self):
  producer=Mock()
  with self.assertRaises(InputError)as cm:gated_propose(b'{"W":18.1,"L":"22.2","n":2}',producer)
  self.assertEqual(cm.exception.code,'UNSUPPORTED_JSON_DECIMAL_REPRESENTATION');producer.assert_not_called()
 def test_valid_lower_width_no_core_not_parser_error_no_solver(self):
  producer=Mock();p,c,result=gated_propose(self.body('5'),producer)
  self.assertEqual(p['ratios']['W'],['5','1']);self.assertIsNone(c)
  self.assertEqual(result['status'],'STUDY_CORE_NO_FIT_NOT_INFEASIBLE');producer.assert_not_called()
 def test_valid_lower_length_actual_bound_conflict_without_milp(self):
  import source_fit_candidate207 as candidate
  with patch.object(candidate,'milp',side_effect=AssertionError('MILP_MUST_NOT_RUN'))as solver:
   p,c,result=gated_propose(self.body('18','5'),candidate.propose)
  self.assertEqual(p['ratios']['L'],['5','1']);self.assertIsNotNone(c)
  self.assertEqual(result['status'],'NO_PROPOSAL_IN_THIS_PROGRAM')
  self.assertEqual(result['reason'],'ROOM_OR_CORE_BOUND_CONFLICT')
  solver.assert_not_called()
 def test_valid_decimal_dispatch_exact_raw_core(self):
  producer=Mock(return_value={'status':'NO_PROPOSAL_IN_THIS_TOPOLOGY'})
  p,c,result=gated_propose(self.body(),producer)
  producer.assert_called_once();self.assertEqual(F(c['units']['A'][2]),F('17.85'))
  self.assertEqual(producer.call_args.kwargs['sleep_roles'],['double','twin'])
 def test_coordinate_binary_ratio_distinct_decimal_exact_json(self):
  p=self.proposal();pin=digest(p);norm,r=proposal_transport(p);proof=coordinate_receipt(p,norm,r)
  self.assertEqual(proof['conversion_count'],160);self.assertEqual(digest(p),pin)
  row=proof['records'][0];self.assertEqual(row['decimal_ratio'],['1','10']);self.assertNotEqual(row['binary_ratio'],row['decimal_ratio'])
  reread,rt=roundtrip(norm);self.assertEqual(rt['before_digest'],rt['after_digest']);self.assertEqual(digest(reread),pin)
 def test_signed_zero_preserved(self):
  reread,proof=roundtrip({'v':[-0.0,0.0]})
  self.assertEqual([v.hex()for v in reread['v']],['-0x0.0p+0','0x0.0p+0'])
  self.assertNotEqual(proof['binary64_records'][0]['hex'],proof['binary64_records'][1]['hex'])
 def test_numpy_outside_roles_rejected(self):
  for field in ('count','metadata'):
   p=self.proposal();p[field]=np.float64(2)
   with self.assertRaisesRegex(ValueError,'TRANSPORT_TYPE'):proposal_transport(p)
  with self.assertRaisesRegex(ValueError,'TRANSPORT_TYPE'):transport({'report':np.float64(.1)})
 def test_nonfinite_coordinate_rejected(self):
  for bad in (np.float64('nan'),np.float64('inf'),np.float64('-inf')):
   p=self.proposal();p['rectangles']['bed1'][0]=bad
   with self.assertRaisesRegex(ValueError,'PROPOSAL_SCALAR_NOT_EXACT'):proposal_transport(p)
 def test_nonfinite_report_rejected(self):
  for bad in (float('nan'),float('inf'),float('-inf')):
   with self.assertRaisesRegex(ValueError,'TRANSPORT_NONFINITE'):roundtrip({'v':bad})
 def test_receipt_ratio_mutation_rejected(self):
  p=self.proposal();norm,r=proposal_transport(p);r['coordinate_conversions'][0]['binary_ratio']=['0','1']
  with self.assertRaisesRegex(ValueError,'COORDINATE_BINARY_RATIO'):coordinate_receipt(p,norm,r)
 def test_coordinate_receipt_missing_duplicate_paths_rejected(self):
  for mode in ('empty','duplicate'):
   p=self.proposal();norm,r=proposal_transport(p)
   if mode=='empty':r['coordinate_conversions']=[]
   else:r['coordinate_conversions'][1]=copy.deepcopy(r['coordinate_conversions'][0])
   with self.assertRaisesRegex(ValueError,'COORDINATE_RECEIPT_COVERAGE'):coordinate_receipt(p,norm,r)
if __name__=='__main__':unittest.main()
