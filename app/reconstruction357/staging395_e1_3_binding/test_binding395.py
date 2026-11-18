import copy
import json
import unittest
from pathlib import Path

from binding395 import compare, digest


ROOT = Path(__file__).resolve().parents[2]
RUN = "1cdc4934-9ad0-4849-882f-95df163e622e"
BASE = ROOT / "review394_e1_2_actual_v1" / "runs" / RUN
REQUEST = json.loads((BASE / "request.json").read_text())


def fixture(kind):
    record = json.loads((BASE / kind / "record.json").read_text())
    receipt = json.loads((BASE / kind / "construct_worker_receipt.json").read_text())
    candidate = record["candidate"]
    trace = record["trace"]
    payload = {"operation": "actual-interface", "inputs": copy.deepcopy(candidate["model"]["inputs"]), "construction_trace": {"schema": trace["schema"], "raw": copy.deepcopy(candidate["request"]), "family": "FRONT_REAR", "model_hash": digest(candidate["model"])}, "frame_core125": copy.deepcopy(candidate["packet"]["core"]), "frame_local129": copy.deepcopy(candidate["packet"]["local_model"])}
    proof = {"verified": True, "input_record_digest": digest(record), "outer_trace_digest": digest(trace), "candidate_digest": digest(candidate), "model_hash": digest(candidate["model"]), "packet_digest": digest(candidate["packet"]), "raw": copy.deepcopy(candidate["request"])}
    if kind == "balanced":
        proof.update(run_id=RUN, candidate_id=record["candidate_id"])
    return record, receipt, payload, proof


class BindingTests(unittest.TestCase):
    def test_positive_both_real_schemas(self):
        for kind in ("balanced", "joint"):
            record, receipt, payload, proof = fixture(kind)
            self.assertTrue(compare(kind, REQUEST, record, receipt, payload, proof, RUN)["all_fields_match"])

    def test_dimension_mutation_rejected(self):
        record, receipt, payload, proof = fixture("joint")
        payload["inputs"][0] = "25"
        with self.assertRaisesRegex(ValueError, "ACTUAL_REVIEWER_PAYLOAD_BINDING|UNEXPLAINED_FIELD_MISMATCH"):
            compare("joint", REQUEST, record, receipt, payload, proof, RUN)

    def test_program_mutation_rejected(self):
        record, receipt, payload, proof = fixture("balanced")
        payload["frame_local129"]["program"]["units"] = 3
        with self.assertRaisesRegex(ValueError, "ACTUAL_REVIEWER_PAYLOAD_BINDING|UNEXPLAINED_FIELD_MISMATCH"):
            compare("balanced", REQUEST, record, receipt, payload, proof, RUN)

    def test_requested_count_mutation_rejected(self):
        record, receipt, payload, proof = fixture("joint")
        payload["construction_trace"]["raw"]["requested_count"] = 1
        with self.assertRaisesRegex(ValueError, "REVIEWER_TRACE_BINDING|UNEXPLAINED_FIELD_MISMATCH"):
            compare("joint", REQUEST, record, receipt, payload, proof, RUN)

    def test_ownership_mutation_rejected(self):
        record, receipt, payload, proof = fixture("balanced")
        payload["frame_local129"]["units"][0]["ownership"] = []
        with self.assertRaisesRegex(ValueError, "ACTUAL_REVIEWER_PAYLOAD_BINDING|UNEXPLAINED_FIELD_MISMATCH"):
            compare("balanced", REQUEST, record, receipt, payload, proof, RUN)

    def test_model_digest_mutation_rejected(self):
        record, receipt, payload, proof = fixture("joint")
        proof["model_hash"] = "bad"
        with self.assertRaisesRegex(ValueError, "ACTUAL_REVIEWER_PROOF_BINDING"):
            compare("joint", REQUEST, record, receipt, payload, proof, RUN)

    def test_balanced_candidate_id_mutation_rejected(self):
        record, receipt, payload, proof = fixture("balanced")
        record["candidate_id"] = "bad"
        receipt["record_digest"] = digest(record)
        proof["input_record_digest"] = digest(record)
        with self.assertRaisesRegex(ValueError, "BALANCED_IDENTITY_OR_RUN_BINDING"):
            compare("balanced", REQUEST, record, receipt, payload, proof, RUN)

    def test_joint_synthetic_candidate_id_rejected(self):
        record, receipt, payload, proof = fixture("joint")
        record["candidate_id"] = "invented"
        receipt["record_digest"] = digest(record)
        proof["input_record_digest"] = digest(record)
        with self.assertRaisesRegex(ValueError, "JOINT_SYNTHETIC_CANDIDATE_ID_FORBIDDEN"):
            compare("joint", REQUEST, record, receipt, payload, proof, RUN)

    def test_wrong_run_rejected(self):
        record, receipt, payload, proof = fixture("joint")
        with self.assertRaisesRegex(ValueError, "CURRENT_CONSTRUCTION_RECEIPT"):
            compare("joint", REQUEST, record, receipt, payload, proof, "950a1caa-2a37-4c5b-8615-dba18370167f")


if __name__ == "__main__":
    unittest.main()
