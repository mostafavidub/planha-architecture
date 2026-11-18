import hashlib
import json
import unittest

from construction_identity394 import summarize


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


RUN = "950a1caa-2a37-4c5b-8615-dba18370167f"
REQUEST = {"normalized_raw": {"W": "26", "L": "28", "n": 2, "requested_count": 2}}
REQUEST["raw_digest"] = digest(REQUEST["normalized_raw"])


def fixture(kind):
    model = {"schema": "MODEL", "inputs": REQUEST["normalized_raw"]}
    candidate = {"request": REQUEST["normalized_raw"], "request_digest": REQUEST["raw_digest"], "model": model, "model_digest": digest(model)}
    record = {"candidate": candidate, "trace": {"model_digest": digest(model)}}
    if kind == "balanced":
        record["candidate_id"] = "balanced-real-id"
    receipt = {"run_id": RUN, "kind": kind, "phase": "construct", "record_digest": digest(record), "source_guard_before_after": True, "seconds": 1.25}
    return record, receipt


class IdentityTests(unittest.TestCase):
    def test_balanced_primary_id(self):
        record, receipt = fixture("balanced")
        out = summarize(record, REQUEST, receipt, RUN, "balanced", digest)
        self.assertTrue(out["candidate_id_present"])
        self.assertEqual(out["candidate_id"], "balanced-real-id")

    def test_joint_absent_primary_id_is_explicit(self):
        record, receipt = fixture("joint")
        out = summarize(record, REQUEST, receipt, RUN, "joint", digest)
        self.assertFalse(out["candidate_id_present"])
        self.assertIsNone(out["candidate_id"])
        self.assertEqual(out["candidate_digest"], digest(record["candidate"]))

    def test_missing_required_model_rejected(self):
        record, receipt = fixture("joint")
        del record["candidate"]["model"]
        with self.assertRaisesRegex(ValueError, "CONSTRUCTION_MODEL_MISSING"):
            summarize(record, REQUEST, receipt, RUN, "joint", digest)

    def test_wrong_receipt_run_rejected(self):
        record, receipt = fixture("joint")
        receipt["run_id"] = "c2ed65c7-fb29-4348-ad3c-6169cfead624"
        with self.assertRaisesRegex(ValueError, "CONSTRUCT_RECEIPT_BINDING"):
            summarize(record, REQUEST, receipt, RUN, "joint", digest)

    def test_joint_fake_primary_id_rejected(self):
        record, receipt = fixture("joint")
        record["candidate_id"] = "invented"
        receipt["record_digest"] = digest(record)
        with self.assertRaisesRegex(ValueError, "JOINT_SCHEMA_UNEXPECTED"):
            summarize(record, REQUEST, receipt, RUN, "joint", digest)


if __name__ == "__main__":
    unittest.main()
