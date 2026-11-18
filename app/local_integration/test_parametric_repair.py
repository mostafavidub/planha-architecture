"""Contract negatives using saved controlled execution, not fresh checker tests."""
import copy,json,unittest
from pathlib import Path
from parametric_repair import propose,verify_child,digest,protected
ROOT=next(x for x in Path(__file__).resolve().parents if(x/'manifests/WORKTREE_STATE.json').is_file())
class RepairContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  e=ROOT/'app/local_integration/evidence/parametric_repair';cls.a0=json.loads((e/'parent.json').read_text());cls.b0=json.loads((e/'child.json').read_text())
 def setUp(self):self.a=copy.deepcopy(self.a0);self.b=copy.deepcopy(self.b0)
 def plan(self,**kw):
  a=self.a;return propose(a['raw'],kw.pop('family','FRONT_REAR'),a['proposal'],a['packet'],a['context'],a['review'],a['context']['construction_trace']['source_revision'],test_only=kw.pop('test_only',True),**kw)
 def verify(self,p):return verify_child(self.a['raw'],self.a['packet'],p,self.b['packet'],self.b['review'],self.b['context'])
 def test_controlled_proposal_and_rebuilt_child(self):
  p=self.plan();self.assertEqual(p['operator']['dy'],'-3/2');self.assertTrue(self.verify(p)['protected_unchanged'])
 def test_controlled_fixture_not_natural(self):
  with self.assertRaisesRegex(ValueError,'UNREGISTERED'):self.plan(test_only=False)
 def test_other_frame_denied(self):
  with self.assertRaisesRegex(ValueError,'FRAME'):self.plan(family='LEFT_RIGHT')
 def test_raw_change(self):
  self.a['raw']['W']='30'
  with self.assertRaises(ValueError):self.plan()
 def test_core_change(self):
  self.a['packet']['core']['tampered']=True
  with self.assertRaises(ValueError):self.plan()
 def test_model_change(self):
  self.a['packet']['world_model']['inputs'][0]='30'
  with self.assertRaises(ValueError):self.plan()
 def test_pending_not_permission(self):
  self.a['review']['pending']=['unknown']
  with self.assertRaises(ValueError):self.plan()
 def test_pass_not_repaired(self):
  self.a['review']['status']='PASS_CONCEPT_SCOPED_REVIEW'
  with self.assertRaises(ValueError):self.plan()
 def test_no_collision(self):
  self.a['review']['errors']=[{'code':'OTHER'}]
  with self.assertRaisesRegex(ValueError,'DIRECT_COLLISION'):self.plan()
 def test_unknown_origin(self):
  self.a['review']['hierarchical_provenance129']['verified']=False
  with self.assertRaises(ValueError):self.plan()
 def test_source_revision_changed(self):
  self.a['review']['hierarchical_provenance129']['source_revision']='other'
  with self.assertRaises(ValueError):self.plan()
 def test_no_mutation(self):
  before=digest(self.a);self.plan();self.assertEqual(before,digest(self.a))
 def test_plan_tamper(self):
  p=self.plan();p['operator']['dy']='0'
  with self.assertRaisesRegex(ValueError,'PLAN_CHANGED'):self.verify(p)
 def test_non_target_fixture_protected(self):
  p=self.plan();self.b['packet']['world_model']['units'][0]['fixtures']['armchair1'][0]='0'
  with self.assertRaises(ValueError):self.verify(p)
 def test_core_protected(self):
  p=self.plan();self.b['packet']['core']['x']='changed'
  with self.assertRaises(ValueError):self.verify(p)
 def test_source_plan_mismatch(self):
  p=self.plan();self.b['context']['construction_trace']['proposal']['bedrooms']=2
  with self.assertRaisesRegex(ValueError,'CHILD_SOURCE'):self.verify(p)
 def test_child_review_not_parent(self):
  p=self.plan();self.b['review']=self.a['review']
  with self.assertRaisesRegex(ValueError,'FRESH_CHILD'):self.verify(p)
if __name__=='__main__':unittest.main()
