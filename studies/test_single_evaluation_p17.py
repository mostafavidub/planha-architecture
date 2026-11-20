"""P17 source derivation/binding tests; no synthetic fixture is a physical PASS."""
import copy,hashlib,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
import single_model_p15 as p
import single_evaluation_p17 as e
class Binding(unittest.TestCase):
 def setUp(self):
  self.model={'schema':p.FAMILY,'contract_version':'p15-single-v1','inputs':['18','20',1],'units':[{'id':'A'}],**{k:False for k in p.AUTH}}
  self.context=e.context(p.RAW,{'not_a_real_proposal':True})
 def test_current_source_audit(self):self.assertIn('single_runtime_p17.py',e.source_audit()['p17'])
 def test_context_mutations_pre_replay(self):
  for change in [lambda c:c['raw'].update(n=2),lambda c:c['core']['stair'].__setitem__(0,'.5'),lambda c:c.update(schema='OLD_CONTEXT')]:
   ctx=copy.deepcopy(self.context);change(ctx)
   with self.assertRaises(ValueError):e.verify(self.model,ctx)
 def test_typed_model_before_replay(self):
  for value in (True,1.0,2):
   m=copy.deepcopy(self.model);m['inputs'][2]=value
   with self.assertRaisesRegex(ValueError,'P17_MODEL_INPUT_TYPED'):e.verify(m,self.context)
 def test_pair_model_rejected(self):
  self.model['units'].append({'id':'B'})
  with self.assertRaises(ValueError):e.verify(self.model,self.context)
 def test_old_bundle_rejected(self):
  with self.assertRaisesRegex(ValueError,'P17_BUNDLE_SCHEMA'):e.bind_bundle({'schema':'OLD_PAIR_BUNDLE'})
 def test_numeric_digest_exact(self):
  self.assertNotEqual(p.digest(1),p.digest(1.0));self.assertNotEqual(p.digest(1),p.digest(True))
 def test_exact_four_derivatives(self):
  specs=json.loads((ROOT/'studies/p17_evaluator_derivatives.json').read_text())
  self.assertEqual(len(specs),4)
  for path,spec in specs.items():
   data=(ROOT/spec['source']).read_bytes()
   self.assertEqual(hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest(),spec['source_blob'])
   code=data.decode().replace('\nAUTH=','\nfrom single_evaluation_p17 import source_audit\nAUTH=')
   for old,new in spec['edits']:
    self.assertIn(old,code);code=code.replace(old,new)
   code=code.replace("'schema':'"+spec['schema_from']+"'","'schema':'"+spec['schema_to']+"'")
   if spec['inventory_from_p15']:
    a=code.index('def inventory(');b=code.index('def proven_capacity_violation')
    code=code[:a]+'from single_access_p15 import inventory\n'+code[b:]
   tail=" return out\n"
   self.assertTrue(code.endswith(tail))
   code=code[:-len(tail)]+" out['retained_historical_physical_report']=copy.deepcopy(bundle['reports']['historical_physical'])\n out['retained_historical_physical_digest']=bundle['report_digests']['historical_physical']\n return out\n"
   self.assertEqual((ROOT/path).read_text(),code,path)
 def test_false_current_integrity_even_with_rehash(self):
  import single_decision_p17 as d
  reports={cid:{'integrity_verified':True}for cid in d.SCHEMAS}
  reports[next(iter(reports))]['integrity_verified']=False
  rehashed={cid:p.digest(v)for cid,v in reports.items()}
  self.assertEqual(len(rehashed),4)
  with self.assertRaisesRegex(ValueError,'P17_CURRENT_INTEGRITY'):d.require_current_integrity(reports)
 def test_summary_rehashed_claims_rejected(self):
  import single_runtime_p17 as r
  bundle={'reports':{'physical':{'status':'FAIL','errors':[{'code':'ACTUAL'}],'pending':['UNKNOWN']},
                     'historical_physical':{'status':'FAIL','errors':[{'code':'PAIR'}]},'access':{'state':'FAIL'}}}
  current={'C':{'state':'UNKNOWN'}}
  decision={'criteria':[{'criterion':'C','state':'UNKNOWN'}]}
  negatives={k:True for k in r.NEGATIVES}
  summary={'state':'FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED',**{k:False for k in p.AUTH},'attempts':1,'source_integrity_verified':True,'within_budget':True,'negatives':copy.deepcopy(negatives),
           'physical_status':'FAIL','physical_errors':1,'physical_pending':1,'historical_status':'FAIL','historical_errors':1,
           'access_state':'FAIL','current_states':{'C':'UNKNOWN'},'current_digests':{'C':p.digest(current['C'])}}
  # A summary-only consistency fixture, not a physical/replay/integrity positive.
  r.check_summary(summary,bundle,current,decision,negatives)
  for key,value in [('attempts',True),('historical_errors',0),('access_state','PASS'),('physical_status','PASS'),('within_budget',False)]:
   altered=copy.deepcopy(summary);altered[key]=value;p.digest(altered)
   with self.assertRaises(ValueError):r.check_summary(altered,bundle,current,decision,negatives)
  altered=copy.deepcopy(negatives);altered['old_report']=False
  summary['negatives']=copy.deepcopy(altered)
  with self.assertRaisesRegex(ValueError,'P17_NEGATIVE_SET'):r.check_summary(summary,bundle,current,decision,altered)
 def test_late_and_source_failure_are_observed_only(self):
  from single_runtime_p17 import terminal
  for source,now in [(True,10),(True,11),(False,9)]:
   t=terminal(True,source,10,now,True,'FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED')
   self.assertFalse(t['usable']);self.assertFalse(t['fresh_model_executed']);self.assertTrue(t['observed_model_constructed'])
  self.assertTrue(terminal(True,True,10,9,True,'FULL')['fresh_model_executed'])
 def decision_fixture(self):
  # Binding/source replay are stubbed here; actual decision assembly and typed digest are not.
  import single_decision_p17 as d
  replay={'verified':True};physical={'status':'FAIL','errors':[{'code':'FIXTURE_PHYSICAL_FAIL'}],'pending':['FIXTURE_UNKNOWN']}
  historical={'status':'FAIL','errors':[{'code':'HISTORICAL_FIXTURE'}]}
  b={'model_digest':'a'*64,'reports':{'physical':physical,'historical_physical':historical,'access':{'state':'PASS_SCOPED_OWNERSHIP_ACCESS'}},'report_digests':{'historical_physical':p.digest(historical)}}
  reports={}
  for cid,schema in d.SCHEMAS.items():
   row={'schema':schema,'criterion':cid,'integrity_verified':True,'current_domain_policy':'SINGLE_CURRENT_DOMAIN_P17_V1','model_digest':b['model_digest'],
        'source_physical_report':copy.deepcopy(physical),'source_physical_digest':p.digest(physical),
        'retained_historical_physical_report':copy.deepcopy(historical),'retained_historical_physical_digest':p.digest(historical),
        'single_source_snapshot':{},'state':'UNKNOWN',**{k:False for k in p.AUTH}}
   if cid=='CURRENT_PROGRAM_SUITABILITY':row.update(reports={'replay':replay},report_digests={'replay':p.digest(replay)},report_mutations=[])
   else:row['replay']=replay
   reports[cid]=row
  return d,b,reports,replay
 def test_decision_json_roundtrip_does_not_change_receipt(self):
  from unittest.mock import patch
  d,b,reports,replay=self.decision_fixture();pins={k:p.digest(v)for k,v in reports.items()}
  with patch.object(d,'bind_bundle',return_value=replay),patch.object(d,'source_audit',return_value={}):
   original=d.assemble(b,reports,pins)
   roundtrip=d.assemble(json.loads(json.dumps(b,sort_keys=True)),json.loads(json.dumps(reports,sort_keys=True)),json.loads(json.dumps(pins,sort_keys=True)))
  self.assertEqual(p.digest(original),p.digest(roundtrip))
  self.assertEqual([r['criterion']for r in original['criteria']],sorted(d.SCHEMAS))
  self.assertIn('PHYSICAL_FAIL',original['decision']['blockers']);self.assertIn('CURRENT_UNKNOWN',original['decision']['blockers'])
  self.assertIn('P25_DELIVERY_NOT_IMPLEMENTED',original['decision']['blockers'])
 def test_decision_all_criterion_permutations_same_receipt(self):
  import itertools
  from unittest.mock import patch
  d,b,reports,replay=self.decision_fixture();pins={k:p.digest(v)for k,v in reports.items()}
  digests=set()
  with patch.object(d,'bind_bundle',return_value=replay),patch.object(d,'source_audit',return_value={}):
   for order in itertools.permutations(reports):
    digests.add(p.digest(d.assemble(b,{k:reports[k]for k in order},pins)))
  self.assertEqual(len(digests),1)
 def test_decision_content_mutation_still_rejected(self):
  from unittest.mock import patch
  d,b,reports,replay=self.decision_fixture();pins={k:p.digest(v)for k,v in reports.items()}
  reports[next(iter(reports))]['state']='PASS'
  with patch.object(d,'bind_bundle',return_value=replay),patch.object(d,'source_audit',return_value={}):
   with self.assertRaisesRegex(ValueError,'P17_CURRENT_DIGEST'):d.assemble(b,reports,pins)
if __name__=='__main__':unittest.main(verbosity=2)
