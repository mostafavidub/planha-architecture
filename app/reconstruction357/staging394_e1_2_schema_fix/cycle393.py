"""e1-2 only: invoke both registered constructors once; no review or semantic phase."""
import json
import sys
import time
from pathlib import Path

from guard390 import guard

P = Path(sys.argv[1])
rid = sys.argv[2]
expected = sys.argv[3]
HERE = Path(__file__).resolve().parent
guard(expected)
from contract390 import ROOT, clean, digest, verify

sys.path.insert(0, str(ROOT / "staging368_final_pipeline"))
from supervisor import supervise

start = time.monotonic()
deadline = start + 530
request = json.loads((P / "request.json").read_text())
verify(request)
members = []
for kind in ("balanced", "joint"):
    folder = P / kind
    folder.mkdir()
    cap = 45 if kind == "balanced" else 90
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise ValueError("SHARED530_DEADLINE")
    evidence = folder / "construct_supervision_evidence"
    evidence.mkdir()
    with (P / "events.jsonl").open("a") as stream:
        stream.write(json.dumps({"transport_run_id": rid, "kind": kind, "phase": "construct", "status": "STARTED", "budget": min(cap, remaining)}) + "\n")
    supervision = supervise([sys.executable, "-B", str(HERE / "phase390.py"), "construct", str(folder), str(min(cap, remaining)), rid, expected, kind], min(cap, remaining), evidence_directory=evidence)
    (folder / "construct_supervision.json").write_text(json.dumps(supervision, indent=2))
    guard(expected)
    if not clean(supervision):
        raise ValueError("CONSTRUCT_PHASE_FAILED:" + kind)
    record = json.loads((folder / "record.json").read_text())
    receipt = json.loads((folder / "construct_worker_receipt.json").read_text())
    if receipt.get("run_id") != rid or receipt.get("kind") != kind or receipt.get("phase") != "construct" or receipt.get("record_digest") != digest(record):
        raise ValueError("CONSTRUCT_RECEIPT_BINDING:" + kind)
    candidate = record["candidate"]
    if candidate["request"] != request["normalized_raw"] or candidate["request_digest"] != request["raw_digest"]:
        raise ValueError("CONSTRUCT_REQUEST_BINDING:" + kind)
    model = candidate["model"]
    if candidate["model_digest"] != digest(model) or record["trace"]["model_digest"] != digest(model):
        raise ValueError("CONSTRUCT_MODEL_BINDING:" + kind)
    members.append({
        "kind": kind,
        "model": model,
        "binding": {
            "run_id": rid,
            "candidate_id": record["candidate_id"],
            "record_digest": digest(record),
            "model_digest": digest(model),
            "raw_digest": request["raw_digest"],
            "canonical_request_digest": request["canonical_request_digest"],
            "received_digest": request["received_digest"],
            "transport_body_sha256": request["transport_body_sha256"],
        },
        "physical_review_status": "NOT_RUN_E1_2",
        "qualification": {"qualified": False, "missing": ["E1_3_FRESH_REVIEW_NOT_RUN"]},
    })
    with (P / "events.jsonl").open("a") as stream:
        stream.write(json.dumps({"transport_run_id": rid, "kind": kind, "phase": "construct", "status": "COMPLETED"}) + "\n")

result = {
    "state": "COMPLETED_E1_2_FRESH_REGISTERED_CONSTRUCTION",
    "transport_run_id": rid,
    "test_only": False,
    "experimental": True,
    "requested_count": 2,
    "tested_branch_count": 2,
    "request_fulfilled": False,
    "accepted": False,
    "delivery_allowed": False,
    "qualified_selected_set": False,
    "semantic_state": "NOT_RUN_E1_2",
    "repair_attempted": False,
    "members": members,
    "binding": {"run_id": rid, "transport_body_sha256": request["transport_body_sha256"], "canonical_request_digest": request["canonical_request_digest"]},
    "scope": "E1_2_FRESH_CONSTRUCTION_ONLY",
    "technical_accepted": False,
}
(P / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
(P / "cycle_timing.json").write_text(json.dumps({"seconds": time.monotonic() - start, "shared_budget": 530, "phases": ["balanced.construct", "joint.construct"]}, indent=2))
guard(expected)
