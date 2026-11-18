"""Synthetic receipt content tests only, not evidence of any new checker run."""
import unittest,json,copy,sys
from pathlib import Path
from current_run import validate_execution,seal_current_dag,verify_current_seals,ROOT
from equivalence import compare,attest_proofs,digest
sys.path.insert(0,str(ROOT/'staging368_final_pipeline'))
from request_contract368 import normalize
from model_binding368 import bind
class Content(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());c.f=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());c.q=json.loads((ROOT/'review_engine367_v4/actual.json').read_text());c.registry=json.loads((ROOT/'staging368_semantic_bridge/reference_registry.json').read_text());c.groups=json.loads((ROOT/'staging368_semantic_bridge/dry_reference_predicates.json').read_text())['joint']['predicate_result']
 def setUp(self):
  self.run='00000000-0000-4000-8000-000000000001';self.e=normalize(self.r['candidate']['request']);self.b=bind(self.e,self.r,'joint',self.run)
  common=dict(generation_run_id=self.run,binding=self.b,run_specific_receipt=True,source_unchanged=True,source_record_digest=digest(self.r),**{k:self.e[k]for k in ('canonical_request_digest','raw_digest','received_digest')})
  self.c={**common,'phase':'reconstructed_and_replayed','actual_construct_executed':True,'actual_replay_executed':True,'cached_model_returned':False}
  self.v={**common,'phase':'review_completed','checker_executed':True,'fresh_result_digest':digest(self.f),'expected_registry_digest':digest(self.f['expected_method_registry']),'review_id':'00000000-0000-4000-8000-000000000002'}
  self.s={k:dict(reason='COMPLETED',worker_returncode=0,cleanup_verified=True,worker_reaped=True,unresolved=[])for k in('construct','review')}
  self.p=dict(schema='FINAL_PIPELINE368_RUN',status='REVIEWED_NOT_QUALIFIED',generation_run_id=self.run,members=[dict(kind='joint',construct=self.c,review=self.v)],**{k:self.e[k]for k in ('canonical_request_digest','raw_digest','received_digest')})
 def check(self):return validate_execution(self.run,'joint',self.e,self.r,self.f,self.b,self.c,self.v,self.s,self.p)
 def test_content_valid_not_new_execution(self):self.assertEqual(self.check()['run_id'],self.run)
 def test_stale_run_receipt(self):self.v['generation_run_id']='00000000-0000-4000-8000-000000000099';self.assertRaises(ValueError,self.check)
 def test_checker_false(self):self.v['checker_executed']=False;self.assertRaises(ValueError,self.check)
 def test_cached_model(self):self.c['cached_model_returned']=True;self.assertRaises(ValueError,self.check)
 def test_unreaped_worker(self):self.s['review']['cleanup_verified']=False;self.assertRaises(ValueError,self.check)
 def test_unknown_extra_current_groups(self):
  rb=self.check();eq=compare(self.r,self.f,self.r,self.f);g=copy.deepcopy(self.groups);g['rows'].append({'verdict':'UNKNOWN'})
  self.assertRaises(ValueError,attest_proofs,self.q['quality'],self.registry['members']['joint']['proof_maps'],eq,g,rb,self.registry['source_contract_cohort_policy_digest'])
 def test_policy_mismatch(self):
  rb=self.check();eq=compare(self.r,self.f,self.r,self.f);self.assertRaises(ValueError,attest_proofs,self.q['quality'],self.registry['members']['joint']['proof_maps'],eq,self.groups,rb,'0'*64)
 def test_current_groups_stale(self):
  rb=self.check();eq=compare(self.r,self.f,self.r,self.f);g=copy.deepcopy(self.groups);g['current_fresh_digest']='0'*64;self.assertRaises(ValueError,attest_proofs,self.q['quality'],self.registry['members']['joint']['proof_maps'],eq,g,rb,self.registry['source_contract_cohort_policy_digest'])
 def test_current_dag_seals(self):
  rb=self.check();eq=compare(self.r,self.f,self.r,self.f);proofs=attest_proofs(self.q['quality'],self.registry['members']['joint']['proof_maps'],eq,self.groups,rb,self.registry['source_contract_cohort_policy_digest']);d=seal_current_dag(self.q['source_closures']['final_role'],rb,eq,self.groups,proofs);self.assertTrue(verify_current_seals(d['nodes'],d['topological_order']));self.assertEqual(d['stage'],'PRE_SELECTION_MEMBER_PREREQUISITES');d['nodes']['COMMON_ROLE']['tampered']=True;self.assertRaises(ValueError,verify_current_seals,d['nodes'],d['topological_order'])
if __name__=='__main__':unittest.main()
