"""Pure conjunction and strict unknown tests. No source/fresh/semantic run."""
import unittest,copy,json
from joint_composition390 import extension_condition,compose,RULES,role_extension_predicates,ROOT,rank0_mapping_check,execution_complete
class ConjunctionTests(unittest.TestCase):
 def setUp(self):
  self.old={'verdict':'PASS_SCOPED_FINITE_Q04_SOURCE_JOINT367','remaining':[],'domain':{'domain_closed':True}}
  c={'dominance':'FALSE','strict_worse_witnesses':[{'current':'1','alternative':'3/2','alternative_increase':'1/2'}]}
  self.rows=[{'id':'finite_rank1','eligible':True,'comparison':copy.deepcopy(c)},{'id':'finite_rank2','eligible':True,'comparison':copy.deepcopy(c)}]
 def test_exact_conjunction(self):self.assertTrue(extension_condition(self.old,self.rows))
 def test_unknown_not_dominance_refutation(self):
  self.rows[0]['comparison']['dominance']='UNKNOWN';self.assertFalse(extension_condition(self.old,self.rows))
 def test_ineligible_not_deleted(self):
  self.rows[1]['eligible']=False;self.assertFalse(extension_condition(self.old,self.rows))
 def test_missing_member(self):self.assertFalse(extension_condition(self.old,self.rows[:1]))
 def test_duplicate_member(self):self.rows[1]['id']='finite_rank1';self.assertFalse(extension_condition(self.old,self.rows))
 def test_empty_witness_not_accepted(self):self.rows[0]['comparison']['strict_worse_witnesses']=[];self.assertFalse(extension_condition(self.old,self.rows))
 def test_nonworse_witness_not_accepted(self):
  self.rows[0]['comparison']['strict_worse_witnesses'][0].update(alternative='1',alternative_increase='0');self.assertFalse(extension_condition(self.old,self.rows))
 def test_witness_delta_binding(self):
  self.rows[0]['comparison']['strict_worse_witnesses'][0]['alternative_increase']='99';self.assertFalse(extension_condition(self.old,self.rows))
 def test_old_domain_must_still_be_closed(self):
  self.old['domain']['domain_closed']=False;self.assertFalse(extension_condition(self.old,self.rows))
 def test_old_unknown_not_upgraded(self):
  self.old['remaining']=['UNRESOLVED'];self.assertFalse(extension_condition(self.old,self.rows))
 def test_no_source_or_proof_inputs_means_unknown(self):
  # Sources may be present, but unbound records never qualify. No expensive runner.
  out=compose({}, {}, {}, {}, {}, {}, {})
  self.assertFalse(out['qualification']['qualified']);self.assertFalse(out['cohort_closed']);self.assertEqual(set(out['qualification']['parent_verdicts11']),set(RULES));self.assertTrue(out['missing']);self.assertFalse(out['old_same_invocation_receipts_reissued'])
class RolePredicateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());cls.f=json.loads((ROOT/'review367_joint_source_validation_attempt2/result.json').read_text());cls.role=json.loads((ROOT/'final_role367_v4_supervised/actual.json').read_text());cls.extension={'verdict':'PASS_SCOPED_EXTENDED_FINITE_Q04_CONJUNCTION'}
 def test_original_join_predicates_rechecked_purely(self):
  p=role_extension_predicates(self.role,self.r,self.f,self.extension);self.assertEqual(len(p['exact_eight_hall_rows']),8);self.assertTrue(p['old_service_receipts_unchanged'])
 def test_removed_hall_row_blocks(self):
  r=copy.deepcopy(self.role);r['nodes']['WALL_PURPOSE']['evidence']['closed_hall_dependency_rows'].pop()
  with self.assertRaises(ValueError):role_extension_predicates(r,self.r,self.f,self.extension)
 def test_unresolved_unit_blocks(self):
  r=copy.deepcopy(self.role);r['nodes']['Q12_PER_UNIT']['evidence'][0]['exact_pending']=['UNRESOLVED']
  with self.assertRaises(ValueError):role_extension_predicates(r,self.r,self.f,self.extension)
 def test_changed_service_receipt_blocks(self):
  r=copy.deepcopy(self.role);r['service_compactness_evidence']['invocation_receipts']['cost']['units'][0]['against359']['current_room_excess_m2']='1'
  with self.assertRaises(ValueError):role_extension_predicates(r,self.r,self.f,self.extension)
class Rank0AndAuthorityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.coverage=json.loads((ROOT.parent/'review384_actual_v1/result.json').read_text())['evidence']['cohort']['rank0_source_coverage']
  cls.members=json.loads((ROOT/'final_role367_v4_supervised/actual.json').read_text())['service_compactness_evidence']['invocation_receipts']['necessity']['cohort']['members']
  cls.base=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text())
 def test_rank0_full_mapping(self):self.assertTrue(rank0_mapping_check(self.coverage,self.members,self.base)['verdict'].startswith('PASS_'))
 def test_each_missing_readset_predicate_blocks(self):
  for k in self.coverage['checks']:
   c=copy.deepcopy(self.coverage);c['checks'][k]=False
   with self.assertRaises(ValueError):rank0_mapping_check(c,self.members,self.base)
 def test_wrong_baseline_model_blocks(self):
  c=copy.deepcopy(self.coverage);c['baseline_model_digest']='forged'
  with self.assertRaises(ValueError):rank0_mapping_check(c,self.members,self.base)
 def test_missing_old_baseline_blocks(self):
  with self.assertRaises(ValueError):rank0_mapping_check(self.coverage,[r for r in self.members if r['id']!='balanced365'],self.base)
 def test_wrong_proposal_readset_blocks(self):
  c=copy.deepcopy(self.coverage);c['full_proposal_digest']='forged'
  with self.assertRaises(ValueError):rank0_mapping_check(c,self.members,self.base)
 def test_execution_completion_failclosed(self):
  sup={'reason':'COMPLETED','worker_returncode':0,'worker_reaped':True,'cleanup_verified':True,'unresolved':[]};state={'state':'COMPLETED','cleanup_verified':True};unchanged={'verified':True}
  self.assertTrue(execution_complete(sup,state,unchanged))
  for k,v in [('reason','TIMEOUT'),('worker_returncode',1),('worker_reaped',False),('cleanup_verified',False),('unresolved',[1])]:self.assertFalse(execution_complete(dict(sup,**{k:v}),state,unchanged))
  self.assertFalse(execution_complete(sup,{'state':'RUNNING','cleanup_verified':False},unchanged));self.assertFalse(execution_complete(sup,state,{'verified':False}))
if __name__=='__main__':unittest.main()
