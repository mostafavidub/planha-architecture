"""Synthetic contract fixtures; not an auth/storage/server test. NOT_RUN."""
import copy,unittest
from project_snapshot_contract import validate,digest,read_intent,compare_retry
def record():
    return {"schema":"R4_PROJECT_SNAPSHOT_METADATA_DRAFT_V1","project_id":"p1","snapshot_id":"s1","owner_subject":"ownerA","revision":1,"parent_metadata_digest":None,"snapshot_content_digest":"d"*64,"profile_digest":"e"*64,"source_snapshot_digest":"f"*64,"units_digest":"1"*64,"geometry_mapping_digest":"2"*64,"request_digest":"a"*64,"model_digest":"b"*64,"rule_version":"rules_v1","report_digest":"c"*64,"state":"UNKNOWN","artifact":None,"legacy_run_id":None}
class Contract(unittest.TestCase):
    def test_metadata_match_never_authenticates(self):
        r=validate(record());self.assertTrue(r["metadata_valid"]);self.assertFalse(r["owner_authenticated"]);self.assertFalse(r["storage_committed"])
    def test_read_never_authorizes_or_regenerates(self):
        m=record();r=read_intent("ownerA",m,digest(m),"download_same_snapshot")
        self.assertFalse(r["operation_allowed"]);self.assertFalse(r["regeneration_allowed"]);self.assertEqual(r["artifact_bytes"],0)
    def test_contract_owner_reference_mismatch(self):
        m=record()
        with self.assertRaisesRegex(ValueError,"OWNER_MISMATCH"):read_intent("ownerB",m,digest(m),"read_metadata")
    def test_stale_digest_denied(self):
        with self.assertRaisesRegex(ValueError,"METADATA_DIGEST_MISMATCH"):read_intent("ownerA",record(),"d"*64,"read_metadata")
    def test_legacy_auto_adoption_denied(self):
        m=record();m["legacy_run_id"]="old_uuid"
        with self.assertRaisesRegex(ValueError,"LEGACY_OWNER_ADOPTION"):validate(m)
    def test_claimed_owner_extra_field_denied(self):
        m=record();m["authenticated"]=True
        with self.assertRaisesRegex(ValueError,"SNAPSHOT_FIELDS"):validate(m)
    def test_path_locator_forbidden(self):
        m=record();m["snapshot_id"]="../private"
        with self.assertRaisesRegex(ValueError,"IDENTIFIER"):validate(m)
    def test_metadata_only_cannot_issue_artifact(self):
        m=record();m["artifact"]={"path":"plan.dxf"}
        with self.assertRaisesRegex(ValueError,"ARTIFACT_ISSUANCE"):validate(m)
    def test_retry_same_metadata_not_storage_proof(self):
        r=compare_retry(record(),copy.deepcopy(record()));self.assertTrue(r["same_metadata"]);self.assertFalse(r["operation_allowed"])
    def test_retry_immutable_conflict(self):
        a=record();b=copy.deepcopy(a);b["state"]="REJECTED"
        with self.assertRaisesRegex(ValueError,"IMMUTABLE"):compare_retry(a,b)
    def test_bool_revision_rejected(self):
        m=record();m["revision"]=True
        with self.assertRaisesRegex(ValueError,"REVISION"):validate(m)
    def test_qualified_state_not_implemented(self):
        m=record();m["state"]="QUALIFIED"
        with self.assertRaisesRegex(ValueError,"STATE_NOT_SUPPORTED"):validate(m)
    def test_preconstruction_missing_model_is_outside_scope(self):
        m=record();m["model_digest"]=None
        with self.assertRaisesRegex(ValueError,"DIGEST:model_digest"):validate(m)
    def test_git_commit_is_not_source_snapshot_digest(self):
        m=record();m["source_snapshot_digest"]="a"*40
        with self.assertRaisesRegex(ValueError,"DIGEST:source_snapshot_digest"):validate(m)
    def test_no_source_authenticity_from_self_consistency(self):
        m=record();m["model_digest"]="d"*64;r=validate(m)
        self.assertTrue(r["metadata_valid"]);self.assertFalse(r["source_content_verified"])
if __name__=="__main__":unittest.main()
