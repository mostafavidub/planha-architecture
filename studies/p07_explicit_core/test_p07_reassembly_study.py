from dataclasses import replace
from io import BytesIO
import copy
import json
from pathlib import Path
import unittest
from zipfile import ZipFile
import p07_reassembly_study as s


def wire(x):
    return json.dumps(x, ensure_ascii=False).encode()


def zipfile(payload, member="evidence/checkpoint.json"):
    stream = BytesIO()
    with ZipFile(stream, "w") as z:
        z.writestr("synthetic.txt", b"SYNTHETIC_FIXTURE_ONLY")
        z.writestr(member, payload)
    return stream.getvalue()


class Proof(unittest.TestCase):
    def setUp(self):
        self.rev = s.canonical_sha
        self.engine = {k: ("synthetic:" + k).encode() for k in s.ENGINE_PREFIX}
        self.roles = {k: ("synthetic:" + k).encode() for k in s.SOURCE_ROLES}
        self.hashes = {k:s.sha(v) for k,v in self.engine.items()}
        self.choice = "FRONT_REAR_FULL_BAND114"
        raw = {"W":"0011.2500","L":"17","n":2,"requested_count":1}
        inputs = ["11.25","17",2]
        self.model = {"inputs": inputs, "units":[{"id":"A"},{"id":"B"}],
                      "accepted":False, "release_allowed":False}
        self.core = {"symbolic_shape":"FULL_BAND"}
        ps = {u:{"status":"PROPOSAL_ONLY","symbolic_assignment":u,
                 "bedrooms":2,"sleep_roles":["double","twin"]} for u in ("A","B")}
        hs = {u:self.rev(p) for u,p in ps.items()}
        self.trace = {"schema":"CONSTRUCTION_TRACE127_PAIR_V1", "family":"FRONT_REAR",
                      "source_revision":self.rev(self.hashes), "raw":raw,
                      "proposals":ps,"unit_proposal_hashes":hs,
                      "model_hash":self.rev(self.model), "local_model_hash":self.rev(self.model),
                      "core_hash":self.rev(self.core)}
        self.checkpoint = {
            "choice":self.choice, "raw":raw, "proposals":ps, "core":self.core,
            "ctx":{"operation":"generate_from_dimensions",
                   "existing_plan_id":None, "baseline_model_hash":None,
                   "inputs":inputs,"source_files":self.hashes,"construction_trace":self.trace},
            "packet":{"family":"FRONT_REAR","core":self.core,"local_model":self.model,
                      "world_model":self.model,"admission_claim":False,"unit_proposal_hashes":hs},
        }
        self.tagged = {"schema":s.SCHEMA,"explicit_core_choice":self.choice,
                       "assignments":[{"unit":u,"position":i,"proposal":copy.deepcopy(ps[u])}
                                      for i,u in enumerate(("A","B"))]}
        self.repack()

    def repack(self):
        raw = wire(self.checkpoint)
        self.archive = zipfile(raw)
        self.pins = s.TrustedPins(
            self.choice, s.sha(self.archive), "evidence/checkpoint.json", s.sha(raw),
            s.sha(wire(self.trace)), self.rev(self.trace), self.rev(self.model),
            self.rev(self.core), self.rev(self.hashes), s.sha(Path(s.__file__).read_bytes()),
            {k:s.sha(v) for k,v in self.roles.items()})

    def call(self, **patch):
        args = dict(pins=self.pins, archive=self.archive, tagged_wire=wire(self.tagged),
                    engine_before=self.engine, roles_before=self.roles,
                    engine_after=self.engine, roles_after=self.roles,
                    supplied_model_wire=wire(self.model), supplied_core_wire=wire(self.core))
        args.update(patch)
        return s.seal(**args)

    def reject(self, code, **patch):
        with self.assertRaisesRegex(s.EvidenceError, "^"+code+"$"):
            self.call(**patch)

    def test_positive_receipt_claims_no_authority(self):
        r = self.call()
        self.assertEqual(r["status"], "SUPPLIED_OBJECTS_MATCH_PINNED_ARCHIVE_ONLY")
        self.assertEqual([a["unit"] for a in r["ordered_assignments"]], ["A","B"])
        self.assertEqual(r["model_sha256"], self.pins.model_sha256)
        for k in (*s.AUTHORITY, "runtime_execution_attested", "legacy_verdict_recomputed",
                  "physical_evaluated"):
            self.assertIs(r[k], False)
        self.assertNotIn("symbolic_assignment", repr(r))
        self.assertNotIn("0011.2500", repr(r))

    def test_prepare_returns_archived_order(self):
        items = s.prepare(self.pins,self.archive,wire(self.tagged),self.engine,self.roles)
        self.assertEqual(list(items["ordered_proposals"][0][1]), list(self.trace["proposals"]["A"]))

    def test_other_recognized_choice_mismatch(self):
        self.tagged["explicit_core_choice"]="FRONT_REAR_COMPACT118"
        self.reject("CHOICE_ORIGIN")

    def test_unknown_or_missing_choice(self):
        self.tagged["explicit_core_choice"]=[]
        self.reject("EXPLICIT_CORE_CHOICE")
        del self.tagged["explicit_core_choice"]
        self.reject("EXPLICIT_CORE_CHOICE")

    def test_compact_is_also_valid_with_independent_own_anchor(self):
        self.choice = self.tagged["explicit_core_choice"] = self.checkpoint["choice"] = "FRONT_REAR_COMPACT118"
        self.core["symbolic_shape"] = "COMPACT"
        self.trace["core_hash"] = self.rev(self.core)
        self.repack()
        self.assertEqual(self.call()["explicit_core_choice"],self.choice)

    def test_tagged_swap_and_bool_position(self):
        t = self.tagged["assignments"]
        t.reverse()
        self.reject("ASSIGNMENT_ORDER")
        t.reverse()
        t[0]["position"]=False
        self.reject("ASSIGNMENT_ORDER")

    def test_payload_swap_and_mutation(self):
        a,b = self.tagged["assignments"]
        a["proposal"],b["proposal"]=b["proposal"],a["proposal"]
        self.reject("ASSIGNMENT_BYTES")
        a["proposal"],b["proposal"]=b["proposal"],a["proposal"]
        a["proposal"]["extra"]="changed"
        self.reject("ASSIGNMENT_BYTES")

    def test_fail_closed_duplicate_or_nonfinite(self):
        self.reject("DUPLICATE_JSON_KEY", tagged_wire=b'{"x":{"x":0,"x":1}}')
        for v in (b'NaN',b'1e400',b'Infinity'):
            self.reject("NONFINITE_JSON", tagged_wire=b'{"x":'+v+b'}')

    def test_fail_closed_unicode_and_non_object(self):
        self.reject("INVALID_JSON_WIRE", tagged_wire=b'{"x":"\\ud800"}')
        self.reject("INVALID_JSON_WIRE", tagged_wire=b'\xff')
        self.reject("JSON_OBJECT_REQUIRED", tagged_wire=b'[]')
        self.reject("INVALID_JSON_WIRE", tagged_wire=b'{} trailing')

    def test_archive_repack_does_not_replace_trusted_pin(self):
        self.reject("ARCHIVE_BYTES", archive=zipfile(wire({"copy": 1})))

    def test_duplicate_zip_and_bad_crc(self):
        import warnings
        buf = BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with ZipFile(buf, "w") as z:
                z.writestr(self.pins.checkpoint_member, b"{}")
                z.writestr(self.pins.checkpoint_member, b"{}")
        data=buf.getvalue()
        self.reject("ARCHIVE_MEMBER_INVENTORY", archive=data,
                    pins=replace(self.pins,archive_sha256=s.sha(data)))
        orig = wire(self.checkpoint)
        at = self.archive.index(orig)
        data = self.archive[:at]+b"."+self.archive[at+1:]
        self.reject("ARCHIVE_READ", archive=data,
                    pins=replace(self.pins,archive_sha256=s.sha(data)))

    def test_trace_whitespace_with_archive_and_member_rehash(self):
        cp = wire(self.checkpoint).replace(wire(self.trace), wire(self.trace).replace(b'": ', b'":  ', 1))
        changed=zipfile(cp)
        self.reject("ORIGINAL_TRACE_BYTES", archive=changed, pins=replace(
            self.pins,archive_sha256=s.sha(changed),checkpoint_sha256=s.sha(cp)))

    def test_trace_engine_claim_and_extra_v1_field(self):
        self.trace["source_revision"]="0"*64
        self.repack()
        self.reject("LEGACY_SOURCE_REVISION")
        self.trace["source_revision"]=self.pins.engine_revision
        self.trace["core_choice"]=self.choice
        self.repack()
        self.reject("LEGACY_TRACE_SCHEMA")

    def test_engine_and_role_bytes_before_after(self):
        changed = {**self.engine,"constructor127.py":b"different"}
        for stage in ("engine_before","engine_after"):
            self.reject("ENGINE_SOURCE_REVISION", **{stage:changed})
        changed = {**self.roles,"stock":b"different"}
        for stage in ("roles_before","roles_after"):
            self.reject("ADAPTER_SOURCE_BYTES", **{stage:changed})
        self.reject("ADAPTER_BYTES", pins=replace(self.pins,adapter_sha256="0"*64))

    def test_context_source_lie_and_canonical_dimension(self):
        self.checkpoint["ctx"]["source_files"] = {**self.hashes, "constructor127.py":"0"*64}
        self.repack()
        self.reject("LEGACY_CONTEXT_SOURCE")
        self.checkpoint["ctx"]["source_files"] = self.hashes
        self.trace["raw"]["W"] = "1e1"
        self.repack()
        self.reject("DIMENSION_WIRE")
        self.trace["raw"]["W"] = "25.0001"
        self.repack()
        self.reject("DIMENSION_DOMAIN")
        self.trace["raw"]["W"] = "12"
        self.repack()
        self.reject("CANONICAL_DIMENSION_BINDING")

    def test_supplied_model_and_core_wrong(self):
        for wrong in ('"2"', "2.0"):
            mutated = wire(self.model).replace(b'"17", 2',b'"17", '+wrong.encode())
            self.reject("MODEL_DIGEST", supplied_model_wire=mutated)
        self.reject("SUPPLIED_CORE_DIGEST", supplied_core_wire=b'{"symbolic_shape":"COMPACT"}')

    def test_bad_archived_model_unit_order_or_authority(self):
        self.model["units"].reverse()
        self.trace["model_hash"]=self.trace["local_model_hash"]=self.rev(self.model)
        self.repack()
        self.reject("WORLD_UNIT_ORDER")
        self.model["units"].reverse()
        self.model["accepted"]=0
        self.trace["model_hash"]=self.trace["local_model_hash"]=self.rev(self.model)
        self.repack()
        self.reject("WORLD_AUTHORITY")


if __name__ == "__main__":
    unittest.main()
