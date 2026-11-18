"""Negative contracts using recorded natural parent; no new quality claims."""
import json,copy,unittest,sys
from pathlib import Path
from parametric_route_repair import propose_route
ROOT=next(x for x in Path(__file__).resolve().parents if(x/'manifests/WORKTREE_STATE.json').is_file());sys.path.insert(0,str(ROOT/'engine'))
class RouteContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.original=json.loads((ROOT/'app/local_integration/evidence/natural_route_repair/parent.json').read_text())
 def setUp(self):self.a=copy.deepcopy(self.original)
 def call(self,family='LEFT_RIGHT'):
  a=self.a;return propose_route(a['raw'],family,a['proposal'],a['packet'],a['context'],a['review'],a['context']['construction_trace']['source_revision'])
 def test_wrong_frame(self):
  with self.assertRaises(ValueError):self.call('UNKNOWN')
 def test_wrong_proposal_family(self):
  self.a['proposal']['generation_method']='CONTROLLED_FIXTURE'
  with self.assertRaises(ValueError):self.call()
 def test_changed_raw(self):
  self.a['raw']['W']='44'
  with self.assertRaises(ValueError):self.call()
 def test_changed_model(self):
  self.a['packet']['world_model']['inputs'][0]='44'
  with self.assertRaises(ValueError):self.call()
 def test_changed_core(self):
  self.a['packet']['core']['extra']='changed'
  with self.assertRaises(ValueError):self.call()
 def test_pending_unknown(self):
  self.a['review']['pending']=['UNKNOWN']
  with self.assertRaises(ValueError):self.call()
 def test_no_route_witness(self):
  self.a['review']['errors']=[{'code':'OTHER'}]
  with self.assertRaisesRegex(ValueError,'SINGLE_SEATING_ROUTE'):self.call()
 def test_pass_not_repaired(self):
  self.a['review']['status']='PASS_CONCEPT_SCOPED_REVIEW'
  with self.assertRaises(ValueError):self.call()
 def test_collision_different_operator(self):
  self.a['review']['errors'].append({'code':'FIXTURE_COLLISION'})
  with self.assertRaisesRegex(ValueError,'COLLISION_NOT_ROUTE'):self.call()
 def test_unknown_origin(self):
  self.a['review']['hierarchical_provenance129']['verified']=False
  with self.assertRaises(ValueError):self.call()
if __name__=='__main__':unittest.main()
