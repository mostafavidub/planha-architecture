"""Early rejection tests never replay the assembler or invoke search."""
import unittest
from construction_replay118 import verify,source_revision,digest
from q11_boundary118 import verify_new_workflow
class Trace(unittest.TestCase):
 def test_missing_not_assumed_new(self):self.assertFalse(verify({}, {})['verified'])
 def test_old_source_rejected_before_replay(self):
  m={'inputs':['18','24',2]};r=verify(m,{'construction_trace':{'schema':'CONSTRUCTION_TRACE118_V1','source_revision':'old','model_hash':digest(m),'raw':{'width':'18','length':'24','units':2}}});self.assertTrue(r['errors']);self.assertFalse(r['verified'])
 def test_model_edit_rejected_before_replay(self):
  m={'inputs':['18','24',2]};r=verify(m,{'construction_trace':{'schema':'CONSTRUCTION_TRACE118_V1','source_revision':source_revision(),'model_hash':'wrong','raw':{'width':'18','length':'24','units':2}}});self.assertTrue(r['errors']);self.assertFalse(r['verified'])
 def test_revision_cannot_relabel_new(self):
  m={'inputs':['18','24',2]};r=verify_new_workflow(m,{'operation':'generate_from_dimensions','baseline_model_hash':'prior','inputs':m['inputs']});self.assertIn('Q11_REVISION_MISLABELED_NEW_CONSTRUCTION',[x['code']for x in r['errors']]);self.assertFalse(r['verified'])
if __name__=='__main__':unittest.main()
