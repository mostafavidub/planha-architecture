"""Field-by-field fail-closed binding of request, model and actual reviewer input."""
import hashlib
import json
import uuid
from copy import deepcopy
from fractions import Fraction


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def required(label, value):
    if value is None:
        raise ValueError("REQUIRED_FIELD_MISSING:" + label)
    if isinstance(value, str) and not value:
        raise ValueError("REQUIRED_FIELD_EMPTY:" + label)
    if isinstance(value, (list, dict)) and not value:
        raise ValueError("REQUIRED_FIELD_EMPTY:" + label)
    return value


def ownership(label, value):
    required(label, value)
    if not isinstance(value, list):
        raise ValueError("OWNERSHIP_TYPE:" + label)
    for index, rectangle in enumerate(value):
        if not isinstance(rectangle, list) or len(rectangle) != 4 or any(item is None for item in rectangle):
            raise ValueError("OWNERSHIP_RECT_SHAPE:" + label + ":" + str(index))
        try:
            x1, y1, x2, y2 = map(Fraction, rectangle)
        except Exception as error:
            raise ValueError("OWNERSHIP_RECT_NUMBER:" + label + ":" + str(index)) from error
        if x2 <= x1 or y2 <= y1:
            raise ValueError("OWNERSHIP_RECT_NONPOSITIVE:" + label + ":" + str(index))
    return value


def same(label, request_value, model_value, reviewer_value, explanation=None):
    required(label + ".request", request_value)
    required(label + ".model", model_value)
    required(label + ".reviewer_payload", reviewer_value)
    if request_value != model_value or model_value != reviewer_value:
        raise ValueError("UNEXPLAINED_FIELD_MISMATCH:" + label)
    return {"field": label, "request": request_value, "model": model_value, "reviewer_payload": reviewer_value, "match": True, "allowed_difference": explanation}


def compare(kind, request, record, receipt, payload, proof, run_id):
    if kind not in ("balanced", "joint") or str(uuid.UUID(run_id)) != run_id:
        raise ValueError("KIND_OR_RUN")
    if receipt != {**receipt, "run_id": run_id, "kind": kind, "phase": "construct", "record_digest": digest(record), "source_guard_before_after": True}:
        raise ValueError("CURRENT_CONSTRUCTION_RECEIPT")
    if not isinstance(request, dict) or not isinstance(request.get("normalized_raw"), dict) or set(request["normalized_raw"]) != {"W", "L", "n", "requested_count"}:
        raise ValueError("REQUEST_REQUIRED_FIELDS")
    normalized = request["normalized_raw"]
    for name in ("W", "L", "n", "requested_count"):
        required("request.normalized_raw." + name, normalized.get(name))
    if request.get("raw_digest") != digest(normalized):
        raise ValueError("REQUEST_RAW_DIGEST")
    candidate = record.get("candidate")
    trace = record.get("trace")
    if not isinstance(candidate, dict) or not isinstance(trace, dict):
        raise ValueError("RECORD_SCHEMA")
    model = candidate.get("model")
    packet = candidate.get("packet")
    if not isinstance(model, dict) or not isinstance(packet, dict):
        raise ValueError("MODEL_OR_PACKET_MISSING")
    required("model.inputs", model.get("inputs")); required("model.program", model.get("program")); required("model.units", model.get("units"))
    if not isinstance(model["inputs"], list) or len(model["inputs"]) != 3 or not isinstance(model["program"], dict) or not isinstance(model["units"], list):
        raise ValueError("MODEL_REQUIRED_FIELD_TYPE")
    required("payload.inputs", payload.get("inputs")); required("payload.construction_trace", payload.get("construction_trace")); required("payload.frame_core125", payload.get("frame_core125")); required("payload.frame_local129", payload.get("frame_local129"))
    if not isinstance(payload["inputs"], list) or len(payload["inputs"]) != 3 or not isinstance(payload["construction_trace"], dict) or not isinstance(payload["frame_core125"], dict) or not isinstance(payload["frame_local129"], dict):
        raise ValueError("PAYLOAD_REQUIRED_FIELD_TYPE")
    required("payload.frame_local129.program", payload["frame_local129"].get("program")); required("payload.frame_local129.units", payload["frame_local129"].get("units"))
    if candidate.get("request") != request.get("normalized_raw") or candidate.get("request_digest") != request.get("raw_digest"):
        raise ValueError("REQUEST_RECORD_BINDING")
    if candidate.get("model_digest") != digest(model) or trace.get("model_digest") != digest(model):
        raise ValueError("MODEL_DIGEST_BINDING")
    expected_proof = {"input_record_digest": digest(record), "outer_trace_digest": digest(trace), "candidate_digest": digest(candidate), "model_hash": digest(model), "packet_digest": digest(packet), "raw": candidate["request"]}
    if proof.get("verified") is not True or any(proof.get(k) != v for k, v in expected_proof.items()):
        raise ValueError("ACTUAL_REVIEWER_PROOF_BINDING")
    if payload.get("inputs") != model.get("inputs") or payload.get("frame_core125") != packet.get("core") or payload.get("frame_local129") != packet.get("local_model"):
        raise ValueError("ACTUAL_REVIEWER_PAYLOAD_BINDING")
    if payload.get("construction_trace", {}).get("raw") != candidate["request"] or payload["construction_trace"].get("model_hash") != digest(model):
        raise ValueError("REVIEWER_TRACE_BINDING")
    if packet.get("world_model") != model or packet.get("local_model") != model:
        raise ValueError("WORLD_LOCAL_MODEL_BINDING")
    canonical = request["canonical_request"]
    width = str(Fraction(canonical["dimensions_m"]["W"]["numerator"], canonical["dimensions_m"]["W"]["denominator"]))
    length = str(Fraction(canonical["dimensions_m"]["L"]["numerator"], canonical["dimensions_m"]["L"]["denominator"]))
    rows = [
        same("dimensions.W", width, model["inputs"][0], payload["inputs"][0]),
        same("dimensions.L", length, model["inputs"][1], payload["inputs"][1]),
        same("unit_count", canonical["unit_count"], model["inputs"][2], payload["inputs"][2]),
        same("requested_count", canonical["requested_count"], candidate["request"]["requested_count"], payload["construction_trace"]["raw"]["requested_count"], "requested_count is a request/trace field, not a model geometry field"),
    ]
    if canonical.get("program_policy") != "FIXED_SOURCE_THREE_BEDROOM_DOUBLE_TWIN_TWIN_NOT_OWNER_CUSTOM_PROGRAM":
        raise ValueError("PROGRAM_POLICY")
    expected_program = {"bedrooms_per_unit": 3, "sleep_roles": ["double", "twin", "twin"], "capacity_profile": "SIX_PERSON_INTERNAL_PROGRAM121", "design_occupants_per_unit": 6, "units": 2, "provisional": True}
    for key, value in expected_program.items():
        model_value = model["program"].get(key)
        reviewer_value = payload["frame_local129"]["program"].get(key)
        rows.append(same("program." + key, value, model_value, reviewer_value))
    unit_ids = [unit["id"] for unit in model["units"]]
    payload_ids = [unit["id"] for unit in payload["frame_local129"]["units"]]
    if any(not isinstance(item, dict) or item.get("id") is None for item in model["units"] + payload["frame_local129"]["units"]):
        raise ValueError("UNIT_ID_MISSING")
    if len(set(unit_ids)) != len(unit_ids) or len(set(payload_ids)) != len(payload_ids):
        raise ValueError("UNIT_ID_DUPLICATE")
    rows.append(same("unit_ids", ["A", "B"], unit_ids, payload_ids))
    ownership_rows = []
    core_ownership = packet["core"].get("unit_ownership")
    if not isinstance(core_ownership, dict):
        raise ValueError("CORE_OWNERSHIP_MISSING")
    for unit in model["units"]:
        uid = unit["id"]
        reviewer_unit = next((item for item in payload["frame_local129"]["units"] if item.get("id") == uid), None)
        if reviewer_unit is None:
            raise ValueError("REVIEWER_UNIT_MISSING:" + uid)
        core_value = ownership("geometric_ownership." + uid + ".core", core_ownership.get(uid))
        model_value = ownership("geometric_ownership." + uid + ".model", unit.get("ownership"))
        reviewer_value = ownership("geometric_ownership." + uid + ".reviewer_payload", reviewer_unit.get("ownership"))
        ownership_rows.append(same("geometric_ownership." + uid, core_value, model_value, reviewer_value, "geometric rectangles; unrelated to account authentication"))
    balanced_id = record.get("candidate_id")
    if kind == "balanced":
        expected_id = digest({"run_id": run_id, "request_digest": digest(candidate["request"]), "model_digest": digest(model), "trace_digest": digest(trace)})
        if balanced_id != expected_id or trace.get("run_id") != run_id or proof.get("run_id") != run_id or proof.get("candidate_id") != balanced_id:
            raise ValueError("BALANCED_IDENTITY_OR_RUN_BINDING")
        identity = {"candidate_id_present": True, "candidate_id": balanced_id, "candidate_digest": digest(candidate), "run_source": "record.trace+proof+receipt"}
    else:
        if "candidate_id" in record:
            raise ValueError("JOINT_SYNTHETIC_CANDIDATE_ID_FORBIDDEN")
        if "run_id" in trace or "run_id" in proof:
            raise ValueError("JOINT_UNDECLARED_RUN_FIELD")
        identity = {"candidate_id_present": False, "candidate_id": None, "candidate_digest": digest(candidate), "run_source": "current construction receipt only"}
    return {"schema": "E1_3_REQUIRED_FIELD_BINDING396_V1", "kind": kind, "run_id": run_id, "request_digest": digest(request), "record_digest": digest(record), "model_digest": digest(model), "reviewer_payload_digest": digest(payload), "reviewer_proof_digest": digest(proof), "field_rows": rows, "ownership_rows": ownership_rows, "identity": identity, "all_required_fields_present": True, "all_fields_match": True, "unknown_or_missing": [], "accepted": False, "delivery_allowed": False, "technical_acceptance": False}
