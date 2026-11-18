"""One bounded e1-3 binding audit over the already-built 394 records."""
import json
import subprocess
import sys
from pathlib import Path

from guard395 import guard
from binding395 import compare

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
if len(sys.argv) != 3:
    raise SystemExit("usage: run395.py NEW_EVIDENCE_DIRECTORY EXPECTED_FREEZE_SHA256")
OUT = Path(sys.argv[1]).resolve()
expected = sys.argv[2]
if OUT.exists():
    raise ValueError("EVIDENCE_PATH_MUST_NOT_EXIST")
count = guard(expected)
OUT.mkdir(parents=True)
run_id = "1cdc4934-9ad0-4849-882f-95df163e622e"
source = ROOT / "review394_e1_2_actual_v1" / "runs" / run_id
request = json.loads((source / "request.json").read_text())
reports = []
for kind in ("balanced", "joint"):
    record_path = source / kind / "record.json"
    receipt_path = source / kind / "construct_worker_receipt.json"
    payload_path = OUT / (kind + "_actual_reviewer_input.json")
    process = subprocess.run([sys.executable, "-B", str(HERE / "payload_worker395.py"), kind, str(record_path), str(payload_path)], capture_output=True, text=True, timeout=65)
    (OUT / (kind + "_payload_worker_receipt.json")).write_text(json.dumps({"returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr, "checker_executed": False}, indent=2))
    if process.returncode != 0:
        raise ValueError("REVIEWER_INPUT_ADAPTER_FAILED:" + kind)
    built = json.loads(payload_path.read_text())
    report = compare(kind, request, json.loads(record_path.read_text()), json.loads(receipt_path.read_text()), built["payload"], built["proof"], run_id)
    (OUT / (kind + "_field_report.json")).write_text(json.dumps(report, ensure_ascii=False, indent=2))
    reports.append(report)
    guard(expected)
result = {"schema": "E1_3_BINDING395_RESULT_V1", "run_id": run_id, "reports": [{"kind": r["kind"], "record_digest": r["record_digest"], "model_digest": r["model_digest"], "reviewer_payload_digest": r["reviewer_payload_digest"], "all_fields_match": r["all_fields_match"], "identity": r["identity"]} for r in reports], "reviewer_inputs_built_from_actual_records": True, "checker_executed": False, "reviewer_verdict_produced": False, "repair_executed": False, "e1_4_started": False, "accepted": False, "delivery_allowed": False, "technical_acceptance": False, "source_pin_count": count}
(OUT / "RESULT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
guard(expected)
