import copy,hashlib,unittest
from current_four_decision import *
def fixture():
 model={'synthetic_test_only':True};mh=digest(model)
 physical={'model_hash':mh,'status':'FAIL','errors':[{'code':'SYNTHETIC_FAIL'}],'pending':['SYNTHETIC_PENDING'],'original_pending':['OLD'],'not_evaluated':['OLD'],'out_of_scope':[{'code':'OLD'}]}
 replay={'verified':True,'model_hash':mh,'source_revision':ENGINE_REVISION,'errors':[],'pending':[]}
 bundle={'packet':{'world_model':model},'model_digest':mh,'reports':{'physical':physical,'replay':replay},'report_digests':{'physical':digest(physical),'replay':digest(replay)}}
 path='app/local_integration/current_four_decision.py';snap={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}
 rows={}
 for cid,schema in SCHEMAS.items():
  r={'schema':schema,'criterion':cid,'state':'UNKNOWN','model_digest':mh,'integrity_verified':True,'source_snapshot':snap,**{k:False for k in AUTH}}
  if cid=='CURRENT_PROGRAM_SUITABILITY':r.update(reports={'replay':replay},historical_physical_report=physical,historical_physical_digest=digest(physical))
  else:r.update(replay=replay,original_physical_report=physical,original_physical_digest=digest(physical))
  rows[cid]=r
 rows=copy.deepcopy(rows)
 return bundle,rows,{k:digest(v) for k,v in rows.items()}
class Decisions(unittest.TestCase):
 def test_actual_state_no_authority_synthetic_fixture(self):
  b,r,p=fixture();out=assemble(b,r,p)
  self.assertIn('PHYSICAL_FAIL',out['decision']['blockers']);self.assertIn('CURRENT_UNKNOWN',out['decision']['blockers'])
  self.assertEqual(out['original_reports'],b['reports']);self.assertTrue(all(out[k] is False for k in AUTH))
 def test_mutation_without_receipt(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['state']='PASS'
  with self.assertRaisesRegex(ValueError,'ASSESSMENT_DIGEST'):assemble(b,r,p)
 def test_wrong_model_with_rehashed_report(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['model_digest']='0'*64;p={k:digest(v) for k,v in r.items()}
  with self.assertRaisesRegex(ValueError,'MODEL_SCHEMA'):assemble(b,r,p)
 def test_physical_report_changed(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['original_physical_report']['errors']=[];p={k:digest(v) for k,v in r.items()}
  with self.assertRaisesRegex(ValueError,'ASSESSMENT_PHYSICAL'):assemble(b,r,p)
 def test_fake_authority(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['accepted']=0;p={k:digest(v) for k,v in r.items()}
  with self.assertRaisesRegex(ValueError,'ASSESSMENT_AUTHORITY'):assemble(b,r,p)
 def test_missing_criterion(self):
  b,r,p=fixture();del r['CONTINUOUS_USEFUL_LIVING']
  with self.assertRaisesRegex(ValueError,'EXACT_FOUR'):assemble(b,r,p)
 def test_unknown_remains_distinct(self):
  s={k:'PASS' for k in SCHEMAS};s['CONTINUOUS_USEFUL_LIVING']='UNKNOWN'
  self.assertIn('CURRENT_UNKNOWN',decide({'status':'PASS_CONCEPT_SCOPED_REVIEW'},s)['blockers'])
 def test_fail_remains_distinct(self):
  s={k:'PASS' for k in SCHEMAS};s['CONTINUOUS_USEFUL_LIVING']='FAIL'
  self.assertIn('CURRENT_NECESSARY_FAIL',decide({'status':'PASS_CONCEPT_SCOPED_REVIEW'},s)['blockers'])
 def test_not_evaluated_distinct(self):
  s={k:'NOT_EVALUATED' for k in SCHEMAS};self.assertIn('CURRENT_NOT_EVALUATED',decide({'status':'PASS_CONCEPT_SCOPED_REVIEW'},s)['blockers'])
 def test_error_not_architectural_fail(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['integrity_verified']=False;p={k:digest(v) for k,v in r.items()}
  out=assemble(b,r,p);self.assertIn('EVALUATOR_ERROR',out['decision']['blockers']);self.assertNotIn('CURRENT_NECESSARY_FAIL',out['decision']['blockers'])
 def test_nested_error(self):
  self.assertTrue(error_markers({'integrity_verified':True,'units':[{'routes':[{'state':'UNKNOWN_EVALUATOR_OR_BINDING_ERROR'}]}]}))
 def test_all_four_pass_still_no_product_authority(self):
  d=decide({'status':'PASS_CONCEPT_SCOPED_REVIEW'},dict.fromkeys(SCHEMAS,'PASS'))
  self.assertTrue(d['current_four_conditions_complete']);self.assertFalse(d['all_PRD_requirements_verified']);self.assertFalse(d['qualified'])
 def test_source_hash_wrong(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['source_snapshot']={'app/local_integration/current_four_decision.py':'0'*64};p={k:digest(v) for k,v in r.items()}
  with self.assertRaisesRegex(ValueError,'SOURCE_SNAPSHOT_CHANGED'):assemble(b,r,p)
 def test_source_traversal(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['source_snapshot']={'app/local_integration/../x':'0'*64};p={k:digest(v) for k,v in r.items()}
  with self.assertRaisesRegex(ValueError,'SOURCE_PATH'):assemble(b,r,p)
 def test_replay_typed_boolean(self):
  b,r,p=fixture();r['CONTINUOUS_USEFUL_LIVING']['replay']['verified']=1;p={k:digest(v) for k,v in r.items()}
  with self.assertRaisesRegex(ValueError,'ASSESSMENT_REPLAY'):assemble(b,r,p)
if __name__=='__main__':unittest.main()
