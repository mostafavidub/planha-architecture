"""Synthetic n2 evidence controls. No tests generate or evaluate a plan."""
import copy
import hashlib
import itertools
import json
import unittest
from unittest.mock import patch

import p25_bound_evidence as p25
import current_four_decision as old

GUEST = "KITCHEN_GUEST_PATH_SEPARATION"
PROGRAM = "CURRENT_PROGRAM_SUITABILITY"
F = {k: False for k in p25.AUTH}

def pins_for_synthetic(b, a, decision):
    # Fixture facility only. A real caller must not derive its own trust anchor.
    pins = {"schema": p25.PIN_SCHEMA, "bundle_digest": p25.digest(b),
            "assessment_digests": {k: p25.digest(v) for k, v in a.items()},
            "v1_decision_digest": p25.digest(decision)}
    return pins, p25.digest(pins)

def fixture():
    axis = ["20", "25", 2]
    frame = {"matrix": [[0, 1], [1, 0]], "translation": ["0", "0"]}
    core = {"solver_inputs": ["25", "20", 2], "physical_core_model": {"inputs": axis},
            "world_from_local": frame}
    # Deliberately non-plan fixture: no actual coordinates, spaces, walls or paths.
    loc = {"inputs": ["25", "20", 2]}
    m = {"inputs": axis, "units": [{"id": "A"}, {"id": "B"}], "accepted": False,
         "release_allowed": False, "schema": "GENERAL125_WORLD_FRAME_STUDY", "profile": {"body_m": ".7"},
         "frame_binding125": {
             "local_model_hash": p25.digest(loc), "core_contract_hash": p25.digest(core),
             "world_from_local": frame, "not_a_receipt_of_whole_acceptance": True},
         "program": {"units": 2, "bedrooms_per_unit": 2, "sleep_roles": ["double", "twin"],
                     "design_occupants_per_unit": 4, "provisional": True,
                     "capacity_profile": "LEGACY_SOURCE_PROGRAM"}}
    mh = p25.digest(m)
    prop = {"status": "PROPOSAL_ONLY", "bedrooms": 2, "sleep_roles": ["double", "twin"],
            "capacity_profile": "LEGACY_SOURCE_PROGRAM", "organization_topology": "FRAME125_SERVICE_SIDE"}
    pp = {x: p25.digest(prop) for x in "AB"}
    trace = {"schema": "CONSTRUCTION_TRACE127_PAIR_V1", "family": "LEFT_RIGHT",
             "raw": {"W": "20", "L": "25", "n": 2, "requested_count": 1},
             "model_hash": mh, "local_model_hash": p25.digest(loc), "core_hash": p25.digest(core),
             "source_revision": p25.ENGINE_PIN, "proposals": {"A": prop, "B": prop},
             "unit_proposal_hashes": pp}
    sources = {n: hashlib.sha256((p25.ROOT / p25.ENGINE / n).read_bytes()).hexdigest()
               for n in p25.construction_replay127.REQUIRED_SOURCES}
    ctx = {"construction_trace": trace, "source_files": sources, "inputs": axis,
           "operation": "generate_from_dimensions", "baseline_model_hash": None, "existing_plan_id": None}
    pkt = {"family": "LEFT_RIGHT", "world_model": m, "core": core, "local_model": loc,
           "admission_claim": False, "unit_proposal_hashes": pp}
    rr = {"model_hash": mh, "trace_hash": p25.digest(trace), "verified": True, "accepted": False,
          "source_revision": p25.ENGINE_PIN, "errors": [], "pending": []}
    contract = p25.rules.load_contract()
    named = {"accepted": False, "release": False, "all_rules_approved": False,
             "contract_schema": contract["schema"], "contract_hash": p25.rules.CONTRACT_SHA256,
             "model_hash": mh, "stage": "concept_internal", "errors": [], "pending": ["SYNTHETIC_NOT_RUN"],
             "requirements": [{"requirement_id": r["id"], "source_rule_ids": r["source_rule_ids"],
                               "status": "NOT_EVALUATED"} for r in contract["requirements"]],
             "rows": [{"rule_id": r["id"], "full_rule_approved": False} for r in contract["registry"]]}
    ph = {"model_hash": mh, "status": "FAIL", "errors": ["SYNTHETIC_FAIL"], "pending": ["SYNTHETIC_PENDING"],
          "checker_version": "GENERAL117_INDEPENDENT_CONCEPT_V1", "multiproposal_provenance127": rr,
          "accepted": False, "release": False, "all_rules_approved": False, "technical_accepted": False,
          "public_release": False, "original_pending": [], "not_evaluated": [], "out_of_scope": [],
          "counts": {"units": 2, "fixtures": 0, "walls": 0, "windows": 0},
          "privacy_evidence": {"accepted": False, "whole_model_hash": mh, "targets": [{"synthetic": True}]},
          "placement_evidence": {"evidence": [{"synthetic": True}]},
          "q11_evidence": {"rule": "Q11 RESIDUAL_WASTE"},
          "rule_contract_evidence": named, "world_inventory125": {
              "model_hash": mh, "local_model_hash": trace["local_model_hash"]},
          "common_frame125": {"accepted": False, "release_allowed": False}}
    reports = {"replay": rr, "physical": ph}
    b = {"packet": pkt, "context": ctx, "engine_revision": p25.ENGINE_PIN, "model_digest": mh,
         "reports": reports, "report_digests": {k: p25.digest(v) for k, v in reports.items()}, **F}
    a = {}
    for k, schema in old.SCHEMAS.items():
        r = {"schema": schema, "criterion": k, "model_digest": mh, "integrity_verified": True,
             "current_domain_policy": "CURRENT_ENTRY_DOMAIN_X03_V1", "state": "UNKNOWN",
             "source_snapshot": {n: hashlib.sha256((p25.ROOT / n).read_bytes()).hexdigest()
                                 for n in old.REQUIRED_SOURCES[k]}, **F}
        if k == PROGRAM:
            r.update(reports={"replay": rr}, historical_physical_report=ph,
                     historical_physical_digest=p25.digest(ph))
        else:
            r.update(replay=rr, original_physical_report=ph, original_physical_digest=p25.digest(ph))
        a[k] = r
    return b, a

class Controls(unittest.TestCase):
    def setUp(self):
        self.b, self.a = fixture()
        self.forbid = []
        for modname, fn in (("construction_replay127", "verify"), ("constructor127", "build"),
                            ("search114", "propose"), ("evaluate_pair127", "evaluate")):
            # Patch only importable modules without optional scipy/numpy in this stdlib CI.
            if modname not in ("construction_replay127", "evaluate_pair127"):
                continue
            p = patch(modname + "." + fn, side_effect=AssertionError("FORBIDDEN_EXECUTION"))
            self.forbid.append(p.start())
            self.addCleanup(p.stop)
        self.addCleanup(self.assert_zero)

    def assert_zero(self):
        for fn in self.forbid:
            fn.assert_not_called()

    def old(self):
        return old.assemble(self.b, self.a, {k: p25.digest(v) for k, v in self.a.items()})

    def run_bound(self, candidate=None, v1=None):
        d = self.old() if v1 is None else v1
        p, h = pins_for_synthetic(self.b, self.a, d)
        return p25.verify(self.b, self.a if candidate is None else candidate, d, p, h)

    def ph_update(self, change):
        ph = self.b["reports"]["physical"]
        change(ph)
        h = p25.digest(ph)
        self.b["report_digests"]["physical"] = h
        for cid, r in self.a.items():
            prefix = "historical" if cid == PROGRAM else "original"
            r[prefix + "_physical_report"] = ph
            r[prefix + "_physical_digest"] = h

    def test_all_orders_same_receipt_and_raw_unchanged(self):
        hp = p25.digest([self.b, self.a])
        d = self.old()
        p, h = pins_for_synthetic(self.b, self.a, d)
        first = p25.verify(self.b, self.a, d, p, h)
        for order in itertools.permutations(self.a):
            self.assertEqual(first, p25.verify(self.b, {k: self.a[k] for k in order}, d, p, h))
        self.assertEqual(first, p25.verify(self.b, json.loads(json.dumps(self.a, sort_keys=True)), d, p, h))
        self.assertEqual(hp, p25.digest([self.b, self.a]))
        self.assertEqual(first["state"], "BLOCKED")
        self.assertFalse(first["delivery_allowed"])
        self.assertFalse(first["execution_authenticity_verified"])
        self.assertIn("NAMED_PHYSICAL_RULE_UNRESOLVED", first["blockers"])

    def test_missing_external_anchor_and_mutation(self):
        d = self.old()
        p, h = pins_for_synthetic(self.b, self.a, d)
        for fake in (None, "", "f"*64):
            with self.assertRaisesRegex(ValueError, "^P25_INDEPENDENT_PIN$"):
                p25.verify(self.b, self.a, d, p, fake)
        aa = copy.deepcopy(self.a)
        aa[GUEST]["state"] = "PASS"
        with self.assertRaisesRegex(ValueError, "^P25_ASSESSMENT_PIN$"):
            p25.verify(self.b, aa, d, p, h)
        with self.assertRaisesRegex(ValueError, "^P25_EXACT_FOUR$"):
            p25.verify(self.b, {k:v for k,v in self.a.items() if k != GUEST}, d, p, h)

    def test_rehashed_summary_not_equal_rederivation(self):
        d = self.old()
        d["decision"]["blockers"] = []
        with self.assertRaisesRegex(ValueError, "^P25_V1_REDERIVATION$"):
            self.run_bound(v1=d)

    def test_context_family_and_unbound_replay_trace(self):
        d = self.old()
        tr = self.b["context"]["construction_trace"]
        tr["family"] = "FRONT_REAR"
        with self.assertRaisesRegex(ValueError, "^P25_FAMILY$"):
            self.run_bound(v1=d)
        tr["family"] = "LEFT_RIGHT"
        tr["raw"]["W"] = "21"
        with self.assertRaisesRegex(ValueError, "^P25_EXACT_REQUEST$"):
            self.run_bound(v1=d)
        tr["raw"]["W"] = "20"
        tr["added"] = "same model but stale replay"
        with self.assertRaisesRegex(ValueError, "^P25_REPLAY_TRACE$"):
            self.run_bound(v1=d)

    def test_wrong_model_and_source(self):
        d = self.old()
        self.b["model_digest"] = "c"*64
        with self.assertRaisesRegex(ValueError, "^P25_PACKET_HASHES$"):
            self.run_bound(v1=d)
        self.b["model_digest"] = self.b["reports"]["physical"]["model_hash"]
        substitute = dict(p25.SOURCES)
        substitute[p25.LOCAL + "current_four_decision.py"] = "0"*40
        with patch.object(p25, "SOURCES", substitute):
            with self.assertRaisesRegex(ValueError, "^P25_UNREVIEWED_SOURCE$"):
                self.run_bound(v1=d)

    def test_original_report_completeness(self):
        d = self.old()
        self.ph_update(lambda r:r.pop("rule_contract_evidence"))
        with self.assertRaisesRegex(ValueError, "^P25_FULL_PHYSICAL$"):
            self.run_bound(v1=d)
        del self.b["reports"]["physical"]
        del self.b["report_digests"]["physical"]
        with self.assertRaisesRegex(ValueError, "^P25_REQUIRED_ORIGINALS$"):
            self.run_bound(v1=d)

    def test_nested_authority_and_named_drop(self):
        d = self.old()
        self.ph_update(lambda r:r.update(release=True))
        with self.assertRaisesRegex(ValueError, "^P25_AUTHORITY$"):
            self.run_bound(v1=d)
        self.ph_update(lambda r:(r.update(release=False), r["rule_contract_evidence"]["requirements"].pop()))
        with self.assertRaisesRegex(ValueError, "^P25_NAMED_RULE_INVENTORY$"):
            self.run_bound(v1=d)

    def test_shape_placeholders_and_false_nested_frame_authority(self):
        d = self.old()
        self.ph_update(lambda r:r.update(counts={}))
        with self.assertRaisesRegex(ValueError, "^P25_PHYSICAL_COUNTS$"):
            self.run_bound(v1=d)
        self.ph_update(lambda r:r.update(counts={"units":2,"fixtures":0,"walls":0,"windows":0}))
        self.ph_update(lambda r:r["common_frame125"].update(release_allowed=0))
        with self.assertRaisesRegex(ValueError, "^P25_AUTHORITY$"):
            self.run_bound(v1=d)

    def test_wrong_version_and_forged_assessment(self):
        d = self.old()
        x = self.a[GUEST]
        policy = x["current_domain_policy"]
        x["current_domain_policy"] = "OUTDATED"
        with self.assertRaisesRegex(ValueError, "^CURRENT_DOMAIN_POLICY_REVISION$"):
            self.run_bound(v1=d)
        x["current_domain_policy"] = policy
        x["delivery_allowed"] = True
        with self.assertRaisesRegex(ValueError, "^ASSESSMENT_AUTHORITY$"):
            self.run_bound(v1=d)

    def test_current_fail_and_error_and_not_evaluated_retained(self):
        self.a[GUEST].update(state="FAIL", missing=["SYNTHETIC_EVALUATOR_FAILURE"])
        self.a[PROGRAM].update(state="NOT_EVALUATED")
        out = self.run_bound()
        self.assertTrue({"PHYSICAL_FAIL", "EVALUATOR_ERROR", "CURRENT_NECESSARY_FAIL",
                         "CURRENT_NOT_EVALUATED"} <= set(out["blockers"]))
        r = next(c for c in out["criteria"] if c["criterion"] == GUEST)
        self.assertEqual(r["reported_state"], "FAIL")
        self.assertEqual(r["evaluator_error_count"], 1)

    def test_unknown_or_type_drift_not_in_scope(self):
        d = self.old()
        self.b["context"]["construction_trace"]["raw"]["n"] = 2.0
        with self.assertRaisesRegex(ValueError, "^P25_EXACT_REQUEST$"):
            self.run_bound(v1=d)

    def test_all_reported_pass_never_qualifies_or_relabels(self):
        for r in self.a.values():
            r["state"] = "PASS"
        self.ph_update(lambda r:r.update(status="PASS_CONCEPT_SCOPED_REVIEW", errors=[], pending=[]))
        out = self.run_bound()
        self.assertEqual(out["state"], "BLOCKED")
        self.assertFalse(out["product_coverage_verified"])
        self.assertFalse(out["execution_authenticity_verified"])
        self.assertFalse(out["accepted"])
        self.assertFalse(out["qualified"])
        self.assertFalse(out["display_allowed"])
        self.assertFalse(out["delivery_allowed"])
        self.assertIn("NAMED_PHYSICAL_RULE_UNRESOLVED", out["blockers"])

if __name__ == "__main__":
    unittest.main()
