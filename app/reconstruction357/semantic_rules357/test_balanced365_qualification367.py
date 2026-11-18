"""Negative seam tests only. No synthetic fixture is admission evidence."""
import unittest,copy,ast
from pathlib import Path
from balanced365_qualification367_core import bind
from common import digest
class Tests(unittest.TestCase):
 def setup_data(self):
  r={'candidate':{'model':{'id':'TEST_ONLY'}}};f={'raw_report':{}};m=digest(r['candidate']['model']);rd=digest(r);fd=digest(f)
  old={'model_hash':m,'raw_report_hash':digest({}),'registered_artifact_verified':True}
  q={'schema':'BALANCED365_EXPANDED_COHORT367','verdict':'PASS_SCOPED_FINITE_Q04_BALANCED365_EXPANDED367','remaining':[],'model_digest':m,'record_digest':rd,'fresh_result_digest':fd,'new367_intrinsic':{'eligible':True},'new367_comparison':{'dominance':'FALSE'},'draft366_property':{'test_only':True}}
  roles={'schema':'ROLE_REGISTRY_BALANCED365_EXPANDED367_SOURCE_ROLES','model_hash':m,'record_digest':rd,'review_digest':fd,'nodes':{'Q04_COMPARISON':{'evidence':q}}};return r,f,old,roles
 def reject(self,change):
  r,f,o,x=self.setup_data();change(r,f,o,x)
  with self.assertRaises((ValueError,KeyError)):bind(r,f,o,x)
 def test_stale(self):self.reject(lambda r,f,o,x:x.update(review_digest='stale'))
 def test_forged_q04(self):self.reject(lambda r,f,o,x:x['nodes']['Q04_COMPARISON']['evidence'].update(model_digest='fake'))
 def test_cross_model(self):self.reject(lambda r,f,o,x:r['candidate']['model'].update(id='other'))
 def test_missing_q12(self):self.reject(lambda *args:None)
 def test_old_scope_only(self):self.reject(lambda r,f,o,x:x['nodes']['Q04_COMPARISON']['evidence'].update(schema='OLD365_ONLY'))
 def test_no_parent_reentry(self):
  p=Path(__file__).with_name('role_registry_balanced365_expanded367.py');tree=ast.parse(p.read_text());imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]
  self.assertIn('balanced365_extended_runner',imports);self.assertFalse(any(n and ('engine' in n or 'qualification' in n)for n in imports))
if __name__=='__main__':unittest.main()
