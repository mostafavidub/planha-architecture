import copy,hashlib,unittest
from programme_evidence_comparison import *
def fixture():
 base={'inputs':{'W':'18','L':'20','n':2},'program':{'bedrooms':2,'design_persons':4},'profile':{'body_m':'.7'},'fixture_catalog_hash':'test','units':[{'id':'A','fixtures':{'seat':['0','0','1','1']}}]}
 a=copy.deepcopy(base);b=copy.deepcopy(base);b['layout_test_only']='alternative'
 paths=['source_living_evaluator.py','source_guest_route_evaluator.py','living_connectivity_diagnostic.py','fixed_route_clearance_diagnostic.py','kitchen_guest_review.py']
 snap={'app/local_integration/'+p:hashlib.sha256((ROOT/'app/local_integration'/p).read_bytes()).hexdigest() for p in paths}
 def report(m,length):
  mh=digest(m);p={'model_hash':mh,'status':'FAIL','errors':[{'code':'SYNTHETIC_PHYSICAL_FAIL'}],'pending':[]}
  return {'schema':'CURRENT_LIVING_SOURCE_EVIDENCE_V1','state':'UNKNOWN','model_digest':mh,'integrity_verified':True,'source_snapshot':snap,'profile':m['profile'],
   'replay':{'verified':True,'model_hash':mh,'source_revision':ENGINE_REVISION},'original_physical_report':p,'original_physical_digest':digest(p),
   'units':[{'unit':'A','actual_seat_endpoints':[{'fixture_id':'seat','activity_id':'seat_use'}],'area_accounting':{DENOMINATORS[0]:'10',DENOMINATORS[1]:'9','verified_useful_living_area_m2':None},
    'studies':[{'domain':'AUTHORIZED_LIVING_AND_CIRCULATION_ACCESS','anchor_fixture_id':'anchor','target_fixture_ids':['seat'],'routes':[{'target_fixture':'seat','body_m':'7/10','state':'PASS_ACCESS_WITNESS_ONLY','path':[['0','0'],['1','0']],'length_m':length,'direction_changes_including_reversal':0}]}]}],**{k:False for k in AUTH}}
 return a,b,copy.deepcopy(report(a,'2')),copy.deepcopy(report(b,'1'))
def run(args):
 a,b,l,r=args;return compare(a,b,l,r,{'models':[digest(a),digest(b)],'reports':[digest(l),digest(r)]})
class Comparison(unittest.TestCase):
 def test_metric_better_never_quality_winner(self):
  o=run(fixture());self.assertEqual(o['status'],'COMPARABLE_SCOPED_EVIDENCE_NOT_QUALITY_RANKING');self.assertIsNone(o['winner']);self.assertEqual(o['physical_failure_preserved'],[True,True])
 def test_duplicate_model(self):
  a,b,l,r=fixture();self.assertIn('DUPLICATE_MODEL_NOT_ALTERNATIVE',run((a,a,l,l))['reasons'])
 def test_program_mismatch(self):
  a,b,l,r=fixture();b['program']['bedrooms']=1;self.assertEqual(run((a,b,l,r))['status'],'NOT_COMPARABLE')
 def test_profile_mismatch(self):
  a,b,l,r=fixture();b['profile']['body_m']='.8';self.assertEqual(run((a,b,l,r))['status'],'NOT_COMPARABLE')
 def test_target_mismatch(self):
  a,b,l,r=fixture();r['units'][0]['studies'][0]['target_fixture_ids']=['other'];self.assertEqual(run((a,b,l,r))['status'],'NOT_COMPARABLE')
 def test_denominator_missing(self):
  a,b,l,r=fixture();del r['units'][0]['area_accounting'][DENOMINATORS[1]];self.assertEqual(run((a,b,l,r))['status'],'NOT_COMPARABLE')
 def test_wrong_evaluator_version(self):
  a,b,l,r=fixture();r['schema']='OTHER';self.assertEqual(run((a,b,l,r))['status'],'NOT_COMPARABLE')
 def test_missing_report(self):
  a,b,l,r=fixture();self.assertEqual(run((a,b,l,{}))['status'],'NOT_COMPARABLE')
 def test_wrong_report_receipt(self):
  a,b,l,r=fixture();o=compare(a,b,l,r,{'models':[digest(a),digest(b)],'reports':['0'*64,digest(r)]});self.assertIn('REPORT_RECEIPTS',o['reasons'])
 def test_no_witness_not_infinite(self):
  a,b,l,r=fixture();x=r['units'][0]['studies'][0]['routes'][0];x.update(state='NO_WITNESS_THIS_DOMAIN',path=None);o=run((a,b,l,r));self.assertEqual(o['comparisons'][0]['comparison'],'MISSING_WITNESS_NOT_NUMERIC_SUPERIORITY')
 def test_timeout_not_quality_failure(self):
  a,b,l,r=fixture();r['units'][0]['studies'][0]['routes'][0]['state']='TIMED_OUT';o=run((a,b,l,r));self.assertEqual(o['status'],'NOT_COMPARABLE');self.assertIsNone(o['winner'])
 def test_weights_not_accepted(self):
  with self.assertRaises(TypeError):compare(*fixture(),{},weights={'length':1})
 def test_source_omission(self):
  a,b,l,r=fixture();r['source_snapshot'].pop('app/local_integration/source_living_evaluator.py');self.assertEqual(run((a,b,l,r))['status'],'NOT_COMPARABLE')
 def test_typed_program_difference(self):
  a,b,l,r=fixture();b['program']['design_persons']=4.0;self.assertEqual(run((a,b,l,r))['status'],'NOT_COMPARABLE')
if __name__=='__main__':unittest.main()
