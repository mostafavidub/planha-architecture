"""Pure POST-MODEL/POST-REPORT draft metadata contract; NO auth/storage/delivery.
Preconstruction failures require a separate lifecycle record, not fake digests.
Inputs to read_intent are untrusted comparison values, never authenticated users.
"""
import hashlib,json,re
FIELDS={"schema","project_id","snapshot_id","owner_subject","revision","parent_snapshot_digest","snapshot_content_digest","profile_digest","source_snapshot_digest","units_digest","geometry_mapping_digest","request_digest","model_digest","rule_version","report_digest","state","artifact","legacy_run_id"}
STATES={"REJECTED","UNKNOWN","EVALUATOR_ERROR","PARTIAL"}
def need(ok,code):
    if not ok:raise ValueError(code)
def strict(v):
    if type(v)is dict:
        need(all(type(k)is str for k in v),"JSON_KEYS")
        for x in v.values():strict(x)
    elif type(v)is list:
        for x in v:strict(x)
    else:need(type(v)in(str,int,bool,type(None)),"JSON_TYPE")
def digest(v):
    strict(v)
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def identifier(v):
    return type(v)is str and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}",v)is not None
def hash_ok(v):
    return type(v)is str and re.fullmatch(r"[0-9a-f]{64}",v)is not None
def validate(record):
    strict(record)
    need(type(record)is dict and set(record)==FIELDS,"SNAPSHOT_FIELDS")
    need(record["schema"]=="R4_PROJECT_SNAPSHOT_METADATA_DRAFT_V1","SCHEMA")
    for k in ("project_id","snapshot_id","owner_subject"):need(identifier(record[k]),"IDENTIFIER:"+k)
    need(type(record["revision"])is int and record["revision"]>=1,"REVISION")
    need(record["parent_snapshot_digest"] is None if record["revision"]==1 else hash_ok(record["parent_snapshot_digest"]),"PARENT_LINEAGE")
    for k in ("snapshot_content_digest","profile_digest","source_snapshot_digest","units_digest","geometry_mapping_digest","request_digest","model_digest","report_digest"):need(hash_ok(record[k]),"DIGEST:"+k)
    need(identifier(record["rule_version"]),"RULE_VERSION")
    need(type(record["state"])is str and record["state"]in STATES,"STATE_NOT_SUPPORTED")
    need(record["legacy_run_id"] is None,"LEGACY_OWNER_ADOPTION_FORBIDDEN")
    need(record["artifact"] is None,"ARTIFACT_ISSUANCE_NOT_IMPLEMENTED")
    return {"metadata_valid":True,"metadata_digest":digest(record),"source_content_verified":False,"owner_authenticated":False,"storage_committed":False,"qualified":False,"delivery_allowed":False}
def compare_retry(existing,proposed):
    validate(existing);validate(proposed)
    need(existing["owner_subject"]==proposed["owner_subject"] and existing["project_id"]==proposed["project_id"],"OWNER_PROJECT_MISMATCH")
    need(existing["snapshot_id"]==proposed["snapshot_id"],"SNAPSHOT_ID_MISMATCH")
    need(digest(existing)==digest(proposed),"IMMUTABLE_SNAPSHOT_CONFLICT")
    return {"same_metadata":True,"idempotent_storage_verified":False,"operation_allowed":False,"blocker":"AUTH_STORAGE_ADAPTER_REQUIRED"}
def read_intent(claimed_principal,record,expected_digest,operation):
    """Only deny mismatches and describe obligations; match NEVER authorizes."""
    validate(record)
    need(identifier(claimed_principal),"PRINCIPAL_COMPARISON_VALUE")
    need(claimed_principal==record["owner_subject"],"OWNER_MISMATCH")
    need(hash_ok(expected_digest) and digest(record)==expected_digest,"METADATA_DIGEST_MISMATCH")
    need(operation in ("read_metadata","download_same_snapshot"),"READ_OPERATION")
    return {"owner_reference_state":"OWNER_REFERENCE_MATCH_NOT_AUTHENTICATED","operation":operation,"operation_allowed":False,"blocker":"AUTH_STORAGE_ADAPTER_REQUIRED","owner_authenticated":False,"regeneration_allowed":False,"artifact_bytes":0,"qualified":False,"delivery_allowed":False}
