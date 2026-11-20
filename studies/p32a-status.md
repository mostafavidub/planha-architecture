# P32-A: status-only same-request observation
Input/source baseline: 9032ebaea0e4c685b9306cbdfe7815f459bcd9c9.
Only public_wln.js changes product behavior. No server, generator, evaluator,
budget, gate, frozen source, preview, download, or delivery changes.
The exact POST byte string is SHA256 compared with X04 request_digest; transport
is the matching fetch plus local document generation. This is consistency, not
a cryptographic signature or proof against a coherent forged server response.
X04 receipt_verified/evidence_usable remain false. Inner P17/X07 binding is
reported separately and permits qualified wording about observed physical FAIL
and simultaneous quality UNKNOWN, never delivery. No lost physical code is guessed.
P17 row model/runtime hashes and exact criterion set are checked; pair X07 schema
and same-request digest are distinct. Reused response IDs/nonces are rejected
within this document only. No durable replay protection is claimed.
Error-set 409 unsupported representation is separate from valid unsupported case.
Network, invalid receipt, timeout, and evaluation failures are not geometric infeasibility.
Six absent stage counters remain NOT_REPORTED.
Tests: real parser/preflight/HTTP/X04/projection plus a controlled synthetic writer;
browser desktop/mobile; intercepted negative responses explicitly labeled.
No genuine geometry, no evaluator rerun, no private payload, no raw model,
no screenshot upload, no positive P25 fixture. Page lifecycle events are synthetic;
they test local stale suppression, not BFCache certification.
Done scope: STATUS_ONLY_REQUEST_CONSISTENCY_AND_BROWSER_STATES_VERIFIED.
Whole P32 remains incomplete: same-version preview and actual P25 admission unavailable.
P29 repair cycle is untouched. Existing source-inventory staleness is not repaired here.
