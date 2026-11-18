"""Schema-aware identity for e1-2 construction records; never invents a primary ID."""
import uuid


def summarize(record, request, receipt, run_id, kind, digest):
    if kind not in ("balanced", "joint"):
        raise ValueError("UNKNOWN_CONSTRUCTOR_KIND")
    if str(uuid.UUID(run_id)) != run_id:
        raise ValueError("INVALID_CURRENT_RUN_ID")
    if not isinstance(record, dict) or not isinstance(record.get("candidate"), dict) or not isinstance(record.get("trace"), dict):
        raise ValueError("CONSTRUCTION_RECORD_SCHEMA")
    candidate = record["candidate"]
    model = candidate.get("model")
    if not isinstance(model, dict):
        raise ValueError("CONSTRUCTION_MODEL_MISSING")
    model_digest = digest(model)
    if candidate.get("request") != request.get("normalized_raw") or candidate.get("request_digest") != request.get("raw_digest"):
        raise ValueError("CONSTRUCT_REQUEST_BINDING:" + kind)
    if candidate.get("model_digest") != model_digest or record["trace"].get("model_digest") != model_digest:
        raise ValueError("CONSTRUCT_MODEL_BINDING:" + kind)
    record_digest = digest(record)
    expected_receipt = {"run_id": run_id, "kind": kind, "phase": "construct", "record_digest": record_digest, "source_guard_before_after": True}
    if any(receipt.get(key) != value for key, value in expected_receipt.items()):
        raise ValueError("CONSTRUCT_RECEIPT_BINDING:" + kind)
    candidate_digest = digest(candidate)
    candidate_id_present = "candidate_id" in record
    candidate_id = record.get("candidate_id")
    if candidate_id_present and (not isinstance(candidate_id, str) or not candidate_id):
        raise ValueError("INVALID_TOP_LEVEL_CANDIDATE_ID:" + kind)
    if kind == "balanced" and not candidate_id_present:
        raise ValueError("BALANCED_CANDIDATE_ID_MISSING")
    if kind == "joint" and candidate_id_present:
        raise ValueError("JOINT_SCHEMA_UNEXPECTED_TOP_LEVEL_CANDIDATE_ID")
    return {"candidate_id_present": candidate_id_present, "candidate_id": candidate_id, "candidate_digest": candidate_digest, "record_digest": record_digest, "model_digest": model_digest, "receipt_run_id": receipt["run_id"], "receipt_seconds": receipt.get("seconds"), "identity_note": "PRIMARY_CANDIDATE_ID_PRESENT" if candidate_id_present else "NO_PRIMARY_CANDIDATE_ID_IN_JOINT_SCHEMA_USE_CANDIDATE_DIGEST_AND_RECEIPT"}
