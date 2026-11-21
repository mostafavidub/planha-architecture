"""Pure evidence adapter for explicit FRONT_REAR selected-core reassembly.

No stock imports or execution, dispatch, filesystem writes or admission.
TrustedPins must come from an independently reviewed origin, not the submitted
archive or runner. SourceSnapshots are bytes supplied by the caller: this
module cannot attest that a process loaded, executed, or retained those bytes.
The stock caller must independently guard actual paths/imports, runtime source
closure before/after, deadline and the no-solver condition.
"""
from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
import json
from math import isfinite
from pathlib import Path
import re
from zipfile import BadZipFile, ZipFile

SCHEMA = "P07_EXPLICIT_CORE_PURE_EVIDENCE_V2"
CHOICES = frozenset(("FRONT_REAR_COMPACT118", "FRONT_REAR_FULL_BAND114"))
SOURCE_ROLES = frozenset(("stock", "transport", "archive_wrapper"))
ENGINE_PREFIX = frozenset((
    "construction_replay127.py", "constructor127.py", "assemble114.py",
    "contract114.py", "frame_contract125.py", "common_core125.py",
    "world_transform125.py",
))
TRACE_KEYS = frozenset((
    "schema", "source_revision", "family", "raw", "model_hash",
    "local_model_hash", "core_hash", "proposals", "unit_proposal_hashes",
))
MAX_MEMBER = 16 * 1024 * 1024
MAX_ARCHIVE = 64 * 1024 * 1024
AUTHORITY = ("accepted", "qualified", "display_allowed", "delivery_allowed",
             "download_allowed", "release_allowed", "production_supported")


class EvidenceError(ValueError):
    """A fixed diagnostic code. No input data are incorporated."""


def check(ok, code):
    if not ok:
        raise EvidenceError(code)


def sha(payload):
    return sha256(payload).hexdigest()


def canonical_sha(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8"))


def _dict(pairs):
    out = {}
    for k, v in pairs:
        check(k not in out, "DUPLICATE_JSON_KEY")
        out[k] = v
    return out


def _nonfinite(_):
    raise EvidenceError("NONFINITE_JSON")


def _float(s):
    x = float(s)
    check(isfinite(x), "NONFINITE_JSON")
    return x


_DECODER = json.JSONDecoder(object_pairs_hook=_dict, parse_constant=_nonfinite,
                            parse_float=_float)


def parse(payload):
    check(type(payload) is bytes and 0 < len(payload) <= MAX_MEMBER, "JSON_SIZE_OR_TYPE")
    try:
        obj = _DECODER.decode(payload.decode("utf-8"))
        # Re-encoding catches unpaired surrogate escapes and keeps the native
        # JSON hash type-sensitive (e.g. true, 1 and 1.0 do not compare equal).
        canonical_sha(obj)
    except EvidenceError:
        raise
    except (UnicodeError, ValueError, RecursionError, OverflowError):
        raise EvidenceError("INVALID_JSON_WIRE") from None
    check(type(obj) is dict, "JSON_OBJECT_REQUIRED")
    return obj


def _member_span(payload, *keys):
    """Return exact wire bytes for one nested member, after strict full parse."""
    s = payload.decode("utf-8")
    def blank(i):
        while i < len(s) and s[i] in " \t\r\n":
            i += 1
        return i

    i = 0
    for want in keys:
        i = blank(i)
        check(i < len(s) and s[i] == "{", "TRACE_MEMBER_PATH")
        i += 1
        while True:
            i = blank(i)
            check(i < len(s) and s[i] != "}", "TRACE_MEMBER_PATH")
            key, j = _DECODER.raw_decode(s, i)
            i = blank(j)
            check(i < len(s) and s[i] == ":", "TRACE_MEMBER_PATH")
            i = blank(i + 1)
            if key == want:
                break
            _, j = _DECODER.raw_decode(s, i)
            i = blank(j)
            check(i < len(s) and s[i] == ",", "TRACE_MEMBER_PATH")
            i += 1
    _, end = _DECODER.raw_decode(s, i)
    return s[i:end].encode("utf-8")


def _hex(value):
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _relative(value):
    return (type(value) is str and 0 < len(value) <= 512
            and all(re.fullmatch(r"[A-Za-z0-9_.-]+", p) and p not in (".", "..")
                    for p in value.split("/")))


@dataclass(frozen=True)
class TrustedPins:
    core_choice: str
    archive_sha256: str
    checkpoint_member: str
    checkpoint_sha256: str
    trace_bytes_sha256: str
    trace_sha256: str
    model_sha256: str
    core_sha256: str
    engine_revision: str
    adapter_sha256: str
    source_sha256: dict


def _pins(p):
    check(type(p) is TrustedPins, "INDEPENDENT_PINS_REQUIRED")
    check(type(p.core_choice) is str and p.core_choice in CHOICES, "TRUSTED_CHOICE")
    check(_relative(p.checkpoint_member), "CHECKPOINT_MEMBER_NAME")
    check(all(_hex(getattr(p, k)) for k in (
        "archive_sha256", "checkpoint_sha256", "trace_bytes_sha256",
        "trace_sha256", "model_sha256", "core_sha256", "engine_revision",
        "adapter_sha256")), "PROVENANCE_PIN_SHAPE")
    check(type(p.source_sha256) is dict and set(p.source_sha256) == SOURCE_ROLES
          and all(_hex(x) for x in p.source_sha256.values()), "SOURCE_ROLE_PINS")
    check(sha(Path(__file__).read_bytes()) == p.adapter_sha256, "ADAPTER_BYTES")


def _archive(p, archive):
    check(type(archive) is bytes and 0 < len(archive) <= MAX_ARCHIVE, "ARCHIVE_SIZE_OR_TYPE")
    check(sha(archive) == p.archive_sha256, "ARCHIVE_BYTES")
    try:
        with ZipFile(BytesIO(archive)) as z:
            iv = z.infolist()
            names = [i.filename for i in iv]
            check(0 < len(names) <= 1024 and len(set(names)) == len(names)
                  and names.count(p.checkpoint_member) == 1, "ARCHIVE_MEMBER_INVENTORY")
            entry = z.getinfo(p.checkpoint_member)
            check(not entry.is_dir() and 0 < entry.file_size <= MAX_MEMBER,
                  "CHECKPOINT_MEMBER_SIZE")
            wire = z.read(entry)  # checks member CRC, never writes or extracts.
    except (BadZipFile, RuntimeError, NotImplementedError, OSError, EOFError):
        raise EvidenceError("ARCHIVE_READ") from None
    check(sha(wire) == p.checkpoint_sha256, "CHECKPOINT_BYTES")
    return wire


def _source(p, engine, roles, context_files):
    check(type(engine) is dict and ENGINE_PREFIX <= set(engine)
          and all(_relative(k) and type(v) is bytes for k, v in engine.items()),
          "ENGINE_SOURCE_SNAPSHOT")
    digests = {k: sha(v) for k, v in engine.items()}
    check(canonical_sha(digests) == p.engine_revision, "ENGINE_SOURCE_REVISION")
    check(type(context_files) is dict and (ENGINE_PREFIX-{"construction_replay127.py"}) <= set(context_files)
          and all(_hex(v) and digests.get(k) == v for k, v in context_files.items()),
          "LEGACY_CONTEXT_SOURCE")
    check(type(roles) is dict and set(roles) == SOURCE_ROLES
          and all(type(v) is bytes for v in roles.values()), "ADAPTER_SOURCE_SNAPSHOT")
    check({k: sha(v) for k, v in roles.items()} == p.source_sha256, "ADAPTER_SOURCE_BYTES")


def _decimal_dimension(x):
    # Mirrors the wire subset of stock selected_core; validates only this
    # archival adapter, not the product parser or geometry/capability.
    check(type(x) is str and 0 < len(x) <= 1024
          and re.fullmatch(r"[0-9]+(?:[.][0-9]+)?", x) is not None, "DIMENSION_WIRE")
    integer, _, fractional = x.partition(".")
    integer = integer.lstrip("0") or "0"
    fractional = fractional.rstrip("0")
    check(len(integer) <= 2 and 5 <= int(integer) <= 25
          and (int(integer) != 25 or not fractional), "DIMENSION_DOMAIN")
    return integer + ("." + fractional if fractional else "")


def _model(model, inputs, pin):
    check(type(model) is dict and canonical_sha(model) == pin, "MODEL_DIGEST")
    units = model.get("units")
    check(type(units) is list and len(units) == 2 and all(
        type(x) is dict and x.get("id") == u for x, u in zip(units, ("A","B"))),
        "WORLD_UNIT_ORDER")
    check(canonical_sha(model.get("inputs")) == canonical_sha(inputs), "MODEL_INPUT_BINDING")
    check(model.get("accepted") is False and model.get("release_allowed") is False,
          "WORLD_AUTHORITY")


def prepare(pins, archive, tagged_wire, engine, roles):
    """Return validated ingress for an external stock runner, not an execution claim.

    Preserve the archived proposals' object-key order for the stock reader.
    The separately tagged wire checks slot identity/order but is not the source
    of the payload handed back to that runner.
    """
    _pins(pins)
    checkpoint = _archive(pins, archive)
    c = parse(checkpoint)
    ctx, packet = c.get("ctx"), c.get("packet")
    check(type(ctx) is dict and type(packet) is dict, "CHECKPOINT_OBJECTS")
    t = ctx.get("construction_trace")
    check(type(t) is dict and set(t) == TRACE_KEYS
          and t["schema"] == "CONSTRUCTION_TRACE127_PAIR_V1"
          and t["family"] == packet.get("family") == "FRONT_REAR", "LEGACY_TRACE_SCHEMA")
    check(ctx.get("operation") == "generate_from_dimensions"
          and "baseline_model_hash" in ctx and ctx["baseline_model_hash"] is None
          and "existing_plan_id" in ctx and ctx["existing_plan_id"] is None, "LEGACY_CONTEXT")
    check(sha(_member_span(checkpoint,"ctx","construction_trace")) == pins.trace_bytes_sha256,
          "ORIGINAL_TRACE_BYTES")
    check(canonical_sha(t) == pins.trace_sha256, "ORIGINAL_TRACE_HASH")
    check(t["source_revision"] == pins.engine_revision, "LEGACY_SOURCE_REVISION")
    _source(pins, engine, roles, ctx.get("source_files"))
    tagged = parse(tagged_wire)
    check(set(tagged) == {"schema","explicit_core_choice","assignments"}
          and tagged["schema"] == SCHEMA and type(tagged["explicit_core_choice"]) is str
          and tagged["explicit_core_choice"] in CHOICES, "EXPLICIT_CORE_CHOICE")
    check(tagged["explicit_core_choice"] == c.get("choice") == pins.core_choice, "CHOICE_ORIGIN")
    raw, inputs = t["raw"], ctx.get("inputs")
    check(type(raw) is dict and set(raw) == {"W","L","n","requested_count"}
          and type(raw["n"]) is int and raw["n"] == 2
          and type(raw["requested_count"]) is int and raw["requested_count"] == 1
          and type(inputs) is list and len(inputs) == 3
          and all(type(inputs[i]) is str for i in (0,1))
          and type(inputs[2]) is int and inputs[2] == raw["n"]
          and canonical_sha(c.get("raw")) == canonical_sha(raw), "RAW_CASE_BINDING")
    check(inputs[:2] == [_decimal_dimension(raw[k]) for k in ("W","L")],
          "CANONICAL_DIMENSION_BINDING")
    seq, ps = tagged["assignments"], t["proposals"]
    check(type(ps) is dict and set(ps) == {"A","B"} and type(seq) is list and len(seq) == 2,
          "ASSIGNMENT_INVENTORY")
    hashes = {}
    for i,u in enumerate(("A","B")):
        row, p = seq[i], ps[u]
        check(type(row) is dict and set(row) == {"unit","position","proposal"}
              and row["unit"] == u and type(row["position"]) is int and row["position"] == i,
              "ASSIGNMENT_ORDER")
        check(type(p) is dict and p.get("status") == "PROPOSAL_ONLY"
              and type(p.get("bedrooms")) is int and p["bedrooms"] == 2
              and p.get("sleep_roles") == ["double","twin"], "PROPOSAL_PROGRAM")
        hashes[u] = canonical_sha(p)
        check(canonical_sha(row["proposal"]) == hashes[u], "ASSIGNMENT_BYTES")
    check(t["unit_proposal_hashes"] == packet.get("unit_proposal_hashes") == hashes
          and canonical_sha(c.get("proposals")) == canonical_sha(ps), "PROPOSAL_BINDING")
    check(packet.get("admission_claim") is False and t["model_hash"] == pins.model_sha256
          and t["local_model_hash"] == pins.model_sha256
          and t["core_hash"] == pins.core_sha256, "ARCHIVED_PACKET_BINDING")
    _model(packet.get("world_model"), inputs, pins.model_sha256)
    _model(packet.get("local_model"), inputs, pins.model_sha256)
    check(type(packet.get("core")) is dict
          and canonical_sha(packet["core"]) == canonical_sha(c.get("core")) == pins.core_sha256,
          "ARCHIVED_CORE_BINDING")
    return {"raw": c["raw"], "inputs": inputs, "choice": pins.core_choice,
            "ordered_proposals": [(u,c["proposals"][u]) for u in ("A","B")],
            "assignment_sha256": [hashes[u] for u in ("A","B")]}


def seal(pins, archive, tagged_wire, engine_before, roles_before,
         engine_after, roles_after, supplied_model_wire, supplied_core_wire):
    """Reverify both observations and independently hash the supplied objects."""
    ready = prepare(pins, archive, tagged_wire, engine_before, roles_before)
    _source(pins, engine_after, roles_after, parse(_archive(pins, archive))["ctx"]["source_files"])
    model, core = parse(supplied_model_wire), parse(supplied_core_wire)
    _model(model, ready["inputs"], pins.model_sha256)
    check(canonical_sha(core) == pins.core_sha256, "SUPPLIED_CORE_DIGEST")
    check(sha(Path(__file__).read_bytes()) == pins.adapter_sha256, "ADAPTER_BYTES")
    return {
        "schema": SCHEMA,
        "status": "SUPPLIED_OBJECTS_MATCH_PINNED_ARCHIVE_ONLY",
        "explicit_core_choice": ready["choice"],
        "ordered_assignments": [{"unit": u, "position": i, "proposal_sha256": h}
                                for i,(u,h) in enumerate(zip(("A","B"),ready["assignment_sha256"]))],
        "archive_sha256": pins.archive_sha256,
        "checkpoint_sha256": pins.checkpoint_sha256,
        "legacy_trace_bytes_sha256": pins.trace_bytes_sha256,
        "legacy_trace_sha256": pins.trace_sha256,
        "model_sha256": pins.model_sha256, "core_sha256": pins.core_sha256,
        "engine_revision": pins.engine_revision, "adapter_sha256": pins.adapter_sha256,
        "source_snapshot_roles": dict(pins.source_sha256),
        "runtime_execution_attested": False, "legacy_verdict_recomputed": False,
        "physical_evaluated": False, **dict.fromkeys(AUTHORITY, False),
    }
