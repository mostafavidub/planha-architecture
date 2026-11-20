"""P25 scoped, offline n2 evidence verifier. No runtime or delivery authority.

The caller supplies a manifest and its expected digest from a separately verified
archive/execution channel. Never mint the expected digest from incoming evidence.
This checks consistency with that external anchor, not signatures or producer
authenticity. All original report bytes are retained by the caller, not rewritten.
FRONT_REAR/18x20 expects its reviewed historical c5ee source root, not the
current LR source root: stage these exact published verifier bytes under that
unchanged checkout’s studies directory for private archival verification only.
"""
import hashlib
import inspect
import json
import math
import re
from pathlib import Path

import construction_replay127
import current_entry_boundary_x03 as domain
import current_four_decision as v1
import front_rear_runtime_adapter as runtime
import rule_contract118 as rules
import same_version_front_rear_contract as pairing

ROOT = Path(__file__).resolve().parents[1]
LOCAL = "app/local_integration/"
ENGINE = "app/reconstruction357/planha_general150_runtime_work/"
ENGINE_PIN = "faada6a8a1106adfe8a24a5f18dfdf6b550f20a6ecc93d81ce07d47a20d6a279"
SCHEMA = "P25_N2_SCOPED_BOUND_EVIDENCE_V1"
PIN_SCHEMA = "P25_INDEPENDENT_ARCHIVE_ANCHORS_V1"
AUTH = ("accepted", "qualified", "display_allowed", "delivery_allowed")
RELEASE = AUTH + ("release", "release_allowed", "technical_accepted", "public_release")
CASES = {"FRONT_REAR": ["18", "20", 2], "LEFT_RIGHT": ["20", "25", 2]}
POLICIES = {
    "FRONT_REAR": "8383c54d4f6bfd3d94580ede2ab20276b917f414",
    "LEFT_RIGHT": "a0a3b751ebe3d452b10eff8fa65f9c23ff30ad1c",
}
PHYSICAL_GROUPS = {
    "dict": ("counts", "privacy_evidence", "placement_evidence", "q11_evidence",
             "rule_contract_evidence", "multiproposal_provenance127"),
    "list": ("errors", "pending", "original_pending", "not_evaluated", "out_of_scope"),
}
SOURCES = {
    "app/local_integration/current_four_decision.py": "55e503d1459fb8005607997f3e09df983bc6d041",
    "app/local_integration/front_rear_runtime_adapter.py": "92ce916b71bb05f0087e2527a51dd8de4d40a676",
    "app/local_integration/same_version_front_rear_contract.py": "0c182a3e26ba48ef6a42df2bf40c2a2ab67c055c",
    "app/local_integration/current_programme_evaluator.py": "99ada55f405e0c205d1a431469d1faae55a149dd",
    "app/local_integration/program_profile_registry.py": "af549f86f39e2e57554cd48e0ffdea54d5444262",
    "app/local_integration/source_guest_route_evaluator.py": "17fb50e08d153aee4aa2ecd4fa4d13928f522a4e",
    "app/local_integration/kitchen_guest_review.py": "27e021ca5eec451dd40a8f8e203763dd2500a052",
    "app/local_integration/guest_four_route_diagnostic.py": "6814519f90f3a5c15ddb1275af268542112c9878",
    "app/local_integration/source_living_evaluator.py": "2f368ae2a1d5db32d7163076f90eb5a7e991f76f",
    "app/local_integration/living_connectivity_diagnostic.py": "afe01e361a72f1436d589dd499c82f5b41c6b0c2",
    "app/local_integration/fixed_route_clearance_diagnostic.py": "463999cf077f42194bdba3c1b331176aedb8aabb",
    "app/local_integration/source_wall_function_evaluator.py": "84233b6bba2c4835af5e59c203ecf51a6765b8e0",
    "app/local_integration/source_wall_counterfactual.py": "2cf702e94564197fc3229da715f4939bac1f51ed",
    "app/local_integration/public_wln_contract.py": "80fd2b2710342735dc35e484c9b0da790995d830",
    "app/local_integration/dimension_contract.py": "058502cd97b5131908b82fdbdba34c62d3376ea3",
    "specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json": "df289f3a072083afc26247970e0804ee69331ede",
    "app/reconstruction357/planha_general150_runtime_work/rule_contract118.py": "97bf97b3fe90d14314f0633357e6e66856597f8b",
    "app/reconstruction357/planha_general150_runtime_work/rule_contract118.json": "4fe2359fbbc40cddc0d1a1fb01b63bfb294cae49",
    "app/reconstruction357/planha_general150_runtime_work/construction_replay127.py": "16b44b228d8dce909b3f45181d0c0d722c1a188f",
}

def need(ok, code):
    if not ok:
        raise ValueError(code)

def strict(o, depth=0):
    need(depth <= 96, "P25_DEPTH")
    t = type(o)
    need(t in (dict, list, str, int, float, bool, type(None)), "P25_TYPE")
    if t is dict:
        need(all(type(k) is str for k in o), "P25_KEY")
        for value in o.values():
            strict(value, depth + 1)
    elif t is list:
        for value in o:
            strict(value, depth + 1)
    elif t is float:
        need(math.isfinite(o), "P25_NONFINITE")

def digest(o):
    strict(o)
    return hashlib.sha256(json.dumps(o, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode()).hexdigest()

def expected_hash(s):
    return type(s) is str and re.fullmatch("[0-9a-f]{64}", s) is not None

def no_authority(record, mandatory):
    need(type(record) is dict, "P25_AUTHORITY_RECORD")
    need(all(record.get(k) is False for k in mandatory), "P25_AUTHORITY")
    need(all(record[k] is False for k in RELEASE if k in record), "P25_AUTHORITY")

def source_state(family):
    pins = {**SOURCES, LOCAL + "current_entry_boundary_x03.py": POLICIES[family]}
    out = {}
    for name, pin in pins.items():
        p = ROOT / name
        need(p.resolve() == p and p.is_relative_to(ROOT), "P25_SOURCE_PATH")
        b = p.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        need(blob == pin, "P25_UNREVIEWED_SOURCE")
        out[name] = hashlib.sha256(b).hexdigest()
    pairs = ((v1.assemble, LOCAL + "current_four_decision.py"),
             (v1.transport, LOCAL + "front_rear_runtime_adapter.py"),
             (v1.digest, LOCAL + "same_version_front_rear_contract.py"),
             (domain.check_model_domain, LOCAL + "current_entry_boundary_x03.py"),
             (construction_replay127.revision, ENGINE + "construction_replay127.py"),
             (rules.load_contract, ENGINE + "rule_contract118.py"))
    for fn, name in pairs:
        need(Path(inspect.getsourcefile(fn)).resolve() == ROOT / name, "P25_CALLABLE_SOURCE")
    need(v1.transport is runtime.transport and v1.digest is pairing.digest and
         construction_replay127.revision() == ENGINE_PIN == v1.ENGINE_REVISION,
         "P25_ENGINE_OR_ALIAS_SOURCE")
    self_path = ROOT / "studies/p25_bound_evidence.py"
    need(Path(__file__).resolve() == self_path, "P25_SOURCE_PATH")
    out["studies/p25_bound_evidence.py"] = hashlib.sha256(self_path.read_bytes()).hexdigest()
    return out

def _packet(bundle):
    p, c = bundle["packet"], bundle["context"]
    t = c["construction_trace"]
    family = p.get("family")
    need(type(family) is str and family in CASES and t.get("family") == family, "P25_FAMILY")
    vals = CASES[family]
    m, local, core = (p[k] for k in ("world_model", "local_model", "core"))
    mh = digest(m)
    need(mh == bundle["model_digest"] == t["model_hash"] and
         digest(local) == t["local_model_hash"] and digest(core) == t["core_hash"],
         "P25_PACKET_HASHES")
    need(bundle["engine_revision"] == t["source_revision"] == ENGINE_PIN and
         t["schema"] == "CONSTRUCTION_TRACE127_PAIR_V1", "P25_TRACE_SCHEMA_SOURCE")
    need(c["operation"] == "generate_from_dimensions" and c["baseline_model_hash"] is None
         and c["existing_plan_id"] is None and p["admission_claim"] is False, "P25_ORIGIN_SCOPE")
    raw = dict(zip(("W", "L", "n"), vals), requested_count=1)
    need(digest(t["raw"]) == digest(raw) and digest(m["inputs"]) == digest(c["inputs"]) == digest(vals),
         "P25_EXACT_REQUEST")
    if family == "FRONT_REAR":
        need(digest(local) == mh, "P25_FRONT_REAR_FRAME")
    else:
        swapped = [vals[1], vals[0], 2]
        frame = {"matrix": [[0, 1], [1, 0]], "translation": ["0", "0"]}
        f = m["frame_binding125"]
        need(digest(local["inputs"]) == digest(core["solver_inputs"]) == digest(swapped)
             and digest(core["physical_core_model"]["inputs"]) == digest(vals)
             and digest(core["world_from_local"]) == digest(f["world_from_local"]) == digest(frame)
             and f["local_model_hash"] == t["local_model_hash"] and f["core_contract_hash"] == t["core_hash"]
             and f["not_a_receipt_of_whole_acceptance"] is True, "P25_LEFT_RIGHT_FRAME")
    need(m["schema"] == ({"FRONT_REAR": "GENERAL117_HIERARCHICAL_STUDY",
                         "LEFT_RIGHT": "GENERAL125_WORLD_FRAME_STUDY"}[family]) and
         digest(m["profile"]) == digest({"body_m": ".7"}), "P25_MODEL_PROFILE")
    need([u["id"] for u in m["units"]] == ["A", "B"], "P25_UNITS")
    base_program = {"units": 2, "bedrooms_per_unit": 2, "sleep_roles": ["double", "twin"],
                    "design_occupants_per_unit": 4, "capacity_profile": "LEGACY_SOURCE_PROGRAM",
                    "provisional": True}
    need(all(digest(m["program"][k]) == digest(val) for k, val in base_program.items()),
         "P25_PROGRAM")
    props = t["proposals"]
    need(type(props) is dict and set(props) == {"A", "B"}, "P25_PROPOSAL_ASSIGNMENTS")
    prop_pins = {k: digest(v) for k, v in props.items()}
    need(p["unit_proposal_hashes"] == t["unit_proposal_hashes"] == prop_pins, "P25_PROPOSAL_HASHES")
    for v in props.values():
        need(v["status"] == "PROPOSAL_ONLY" and type(v["bedrooms"]) is int and v["bedrooms"] == 2
             and v["sleep_roles"] == ["double", "twin"] and v["capacity_profile"] == "LEGACY_SOURCE_PROGRAM",
             "P25_PROPOSAL_PROGRAM")
        if family == "LEFT_RIGHT":
            need(v["organization_topology"] == "FRAME125_SERVICE_SIDE", "P25_LEFT_RIGHT_TOPOLOGY")
    filenames = set(construction_replay127.REQUIRED_SOURCES)
    need(type(c["source_files"]) is dict and set(c["source_files"]) == filenames, "P25_TRACE_SOURCE_SET")
    for name, h in c["source_files"].items():
        need(hashlib.sha256((ROOT / ENGINE / name).read_bytes()).hexdigest() == h, "P25_TRACE_SOURCE")
    no_authority(bundle, AUTH)
    no_authority(m, ("accepted", "release_allowed"))
    return family, t, mh

def _reports(bundle, t, mh, family):
    reports, pins = bundle["reports"], bundle["report_digests"]
    need(type(reports) is dict and type(pins) is dict and
         {"replay", "physical"} <= set(reports) == set(pins), "P25_REQUIRED_ORIGINALS")
    need(all(digest(v) == pins[k] for k, v in reports.items()), "P25_ORIGINAL_REPORT_PIN")
    rr, ph = reports["replay"], reports["physical"]
    no_authority(rr, ("accepted",))
    need(rr["verified"] is True and rr["errors"] == rr["pending"] == [] and
         rr["source_revision"] == ENGINE_PIN and rr["model_hash"] == mh and
         rr["trace_hash"] == digest(t), "P25_REPLAY_TRACE")
    need(type(ph) is dict and all(type(ph.get(k)) is (dict if shape == "dict" else list)
         for shape, keys in PHYSICAL_GROUPS.items() for k in keys), "P25_FULL_PHYSICAL")
    need(ph["model_hash"] == mh and ph["checker_version"] == "GENERAL117_INDEPENDENT_CONCEPT_V1"
         and ph["status"] in ("PASS_CONCEPT_SCOPED_REVIEW", "FAIL", "NOT_EVALUATED")
         and digest(ph["multiproposal_provenance127"]) == digest(rr), "P25_PHYSICAL_PROVENANCE")
    need(type(ph.get("counts")) is dict and set(ph["counts"]) == {"units","fixtures","walls","windows"}
         and all(type(v) is int and v >= 0 for v in ph["counts"].values()) and ph["counts"]["units"] == 2,
         "P25_PHYSICAL_COUNTS")
    no_authority(ph["privacy_evidence"], ("accepted",))
    need(ph["privacy_evidence"]["whole_model_hash"] == mh
         and type(ph["privacy_evidence"]["targets"]) is list and ph["privacy_evidence"]["targets"]
         and type(ph["placement_evidence"]["evidence"]) is list and ph["placement_evidence"]["evidence"]
         and ph["q11_evidence"]["rule"] == "Q11 RESIDUAL_WASTE", "P25_PHYSICAL_SUBREPORTS")
    if family == "LEFT_RIGHT":
        need(type(ph.get("world_inventory125")) is dict and type(ph.get("common_frame125")) is dict
             and ph["world_inventory125"]["model_hash"] == mh
             and ph["world_inventory125"]["local_model_hash"] == t["local_model_hash"],
             "P25_LR_PHYSICAL_FRAME_REPORT")
        no_authority(ph["common_frame125"], ("accepted", "release_allowed"))
    no_authority(ph, ("accepted", "release", "technical_accepted", "public_release"))
    named = ph["rule_contract_evidence"]
    no_authority(named, ("accepted", "release"))
    contract = rules.load_contract()
    need(ph["all_rules_approved"] is False and named["all_rules_approved"] is False
         and named["contract_hash"] == rules.CONTRACT_SHA256 and named["contract_schema"] == contract["schema"]
         and named["stage"] == "concept_internal" and named["model_hash"] == mh, "P25_NAMED_RULE_SOURCE")
    for k in ("requirements", "rows", "pending", "errors"):
        need(type(named[k]) is list, "P25_NAMED_RULE_REPORT")
    need([r["requirement_id"] for r in named["requirements"]] == [r["id"] for r in contract["requirements"]]
         and [r["rule_id"] for r in named["rows"]] == [r["id"] for r in contract["registry"]],
         "P25_NAMED_RULE_INVENTORY")
    need(all(r["source_rule_ids"] == spec["source_rule_ids"] for r, spec in
             zip(named["requirements"], contract["requirements"])), "P25_NAMED_RULE_REFERENCES")
    need(all(r["full_rule_approved"] is False for r in named["rows"]), "P25_NAMED_RULE_AUTHORITY")
    return named

def verify(bundle, assessments, submitted_v1, independent_pins, expected_pin_digest):
    """No HTTP, no replay, no solver. Never a positive qualification decision."""
    need(expected_hash(expected_pin_digest) and digest(independent_pins) == expected_pin_digest,
         "P25_INDEPENDENT_PIN")
    need(type(independent_pins) is dict and set(independent_pins) ==
         {"schema", "bundle_digest", "assessment_digests", "v1_decision_digest"} and
         independent_pins["schema"] == PIN_SCHEMA, "P25_PIN_SCHEMA")
    ad = independent_pins["assessment_digests"]
    need(type(assessments) is dict and type(ad) is dict and
         set(assessments) == set(ad) == set(v1.SCHEMAS), "P25_EXACT_FOUR")
    need(all(expected_hash(x) for x in [independent_pins["bundle_digest"],
         independent_pins["v1_decision_digest"], *ad.values()]), "P25_HASH_SHAPE")
    need(digest(bundle) == independent_pins["bundle_digest"], "P25_BUNDLE_PIN")
    need(all(digest(v) == ad[k] for k, v in assessments.items()), "P25_ASSESSMENT_PIN")
    need(digest(submitted_v1) == independent_pins["v1_decision_digest"], "P25_V1_DECISION_PIN")
    try:
        family = bundle["packet"]["family"]
        need(type(family) is str and family in CASES, "P25_FAMILY")
        before = source_state(family)
        family, t, mh = _packet(bundle)
        named = _reports(bundle, t, mh, family)
    except KeyError as ex:
        raise ValueError("P25_REQUIRED_ORIGINAL_FIELDS") from ex
    ordered = {k: assessments[k] for k in v1.SCHEMAS}
    rebuilt = v1.assemble(bundle, ordered, ad)
    need(digest(rebuilt) == digest(submitted_v1), "P25_V1_REDERIVATION")
    need(rebuilt["integrity_verified"] is True, "P25_V1_INTEGRITY")
    old = rebuilt["decision"]
    blockers = list(old["blockers"])
    if named["errors"]:
        blockers.append("NAMED_PHYSICAL_RULE_FAILURE")
    if named["pending"]:
        blockers.append("NAMED_PHYSICAL_RULE_UNRESOLVED")
    # No positive delivery decision is available in this scoped verifier.
    blockers.append("PRODUCT_ADMISSION_AND_AUTHENTICITY_UNVERIFIED")
    need(digest(independent_pins) == expected_pin_digest and
         digest(bundle) == independent_pins["bundle_digest"] and
         all(digest(v) == ad[k] for k, v in assessments.items()) and
         digest(submitted_v1) == independent_pins["v1_decision_digest"] and
         source_state(family) == before, "P25_CHANGED_DURING_VERIFICATION")
    return {
        "schema": SCHEMA, "state": "BLOCKED", "family": family,
        "evidence_consistency_verified": True, "execution_authenticity_verified": False,
        "product_coverage_verified": False, "model_digest": mh, "trace_digest": digest(t),
        "physical_digest": bundle["report_digests"]["physical"],
        "v1_decision_digest": digest(rebuilt), "trusted_pin_digest": expected_pin_digest,
        "sources_digest": digest(before), "blockers": list(dict.fromkeys(blockers)),
        "criteria": [{"criterion": x["criterion"], "reported_state": x["reported_state"],
                      "effective_state": x["effective_state"],
                      "evaluator_error_count": len(x["evaluator_errors"]),
                      "assessment_digest": x["assessment_digest"]} for x in rebuilt["criteria"]],
        **{k: False for k in AUTH},
    }
