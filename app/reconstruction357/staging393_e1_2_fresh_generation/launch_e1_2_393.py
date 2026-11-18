"""Bounded e1-2 entrypoint: one valid browser POST, fresh registered construction, full owner drain."""
import hashlib
import json
import sys
from pathlib import Path

from guard390 import guard

HERE = Path(__file__).resolve().parent
W = HERE.parent.parent
if len(sys.argv) != 3:
    raise SystemExit("usage: python -B launch_e1_2_393.py NEW_EVIDENCE_DIRECTORY EXPECTED_FREEZE_SHA256")
P = Path(sys.argv[1]).resolve()
expected = sys.argv[2]
if P.exists():
    raise SystemExit("EVIDENCE_PATH_MUST_NOT_EXIST")
if P.name in {"review390_actual_v1", "review391_e1_1_actual_v1", "review392_e1_1_actual_v1_entrypoint"}:
    raise SystemExit("HISTORICAL_EVIDENCE_PATH_FORBIDDEN")
count = guard(expected)
P.mkdir(parents=True)
(P / "preregistration.json").write_text(json.dumps({
    "operation": "e1-2",
    "freeze_sha256": expected,
    "outer_seconds": 660,
    "owner_seconds": 540,
    "cycle_shared_seconds": 530,
    "phase_caps": {"balanced": [45, 90, 5, 90], "joint": [90, 90, 5, 60], "seal": 25},
    "retry": False,
    "browser_valid_submissions": 1,
    "raw_values": {"W": "۲۶", "L": "۲۸", "n": "۲", "requested_count": "۲"},
    "registered_builders": {"balanced": "staging378_finite_portals/source378.construct", "joint": "staging367_service_joint_attempt2/joint367.construct"},
    "historical390_result_must_not_be_reused": True,
    "test_only": False,
    "experimental": True,
    "requested_count": 2,
    "source_file_count": count,
    "e1_3_or_later_authorized": False,
}, ensure_ascii=False, indent=2))
sys.path.insert(0, str(HERE.parent / "staging368_final_pipeline"))
from supervisor import supervise

supervision_evidence = P / "outer_supervision_evidence"
supervision_evidence.mkdir()
(P / "launch_state.json").write_text(json.dumps({"state": "RUNNING_UNVERIFIED", "cleanup_verified": False}))
try:
    supervision = supervise([sys.executable, "-B", str(HERE / "browser_e1_2_393.py"), str(P), expected], 660, evidence_directory=supervision_evidence)
except Exception as error:
    supervision = {"reason": "OUTER_SUPERVISOR_EXCEPTION", "cleanup_verified": False, "worker_reaped": False, "unresolved": ["UNKNOWN"], "error": type(error).__name__ + ":" + str(error)}
(P / "outer_supervision.json").write_text(json.dumps(supervision, indent=2))
clean = supervision.get("reason") == "COMPLETED" and supervision.get("worker_returncode") == 0 and supervision.get("cleanup_verified") is True and supervision.get("worker_reaped") is True and supervision.get("unresolved") == []
shutdown = P / "server_shutdown.json"
owner_clean = shutdown.exists() and json.loads(shutdown.read_text()).get("safe_idle") is True
source_ok = False
try:
    guard(expected)
    source_ok = True
    (P / "source_evidence_unchanged.json").write_text(json.dumps({"verified": True, "count": count}))
except Exception as error:
    (P / "source_evidence_unchanged.json").write_text(json.dumps({"verified": False, "error": str(error)}))
result = None
try:
    result = json.loads((P / "browser_result.json").read_text())
except Exception:
    pass
audit_ok = False
try:
    fresh = json.loads((P / "FRESH_GENERATION_AUDIT.json").read_text())
    audit_ok = fresh["fresh_generation_verified"] is True and fresh["historical_result_reused"] is False and json.loads((P / "listener_closed.json").read_text())["verified"] is True and json.loads((P / "server_identity_audit.json").read_text())["original_process_gone"] is True
except Exception:
    pass
success = clean and owner_clean and source_ok and isinstance(result, dict) and result.get("state") == "COMPLETED_E1_2_FRESH_REGISTERED_CONSTRUCTION" and audit_ok
(P / "containment_outcome.json").write_text(json.dumps({"outer_reason": supervision["reason"], "owner_clean_shutdown_observed": owner_clean, "emergency_outer_containment": not clean, "not_equivalent_to_owner_clean_shutdown": not clean or not owner_clean, "completed": success}, indent=2))
(P / "launch_state.json").write_text(json.dumps({"state": "COMPLETED" if success else "STOPPED_OR_UNRESOLVED", "cleanup_verified": clean and owner_clean}))
print(json.dumps(supervision))
if not success:
    raise SystemExit(1)
