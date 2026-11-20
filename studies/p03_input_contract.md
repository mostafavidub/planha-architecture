# P03 — current input contract and executable boundary proof

Baseline reviewed: `dc07a92502c77bcc438b91c75c8a3d8d1da4ac89`. This change adds evidence tests and documentation only. It does not change parser, server, scheduler, engine, historical deadline, runtime budget, capability or any source pin.

## Current executable surface (explicit registry, not every Python import)
| Entry / caller | Validation path | Capability disposition |
|---|---|---|
| `current_entry_launch_x03.server("PUBLIC_WLN_18X20")` -> `public_wln_server.Handler.do_POST`, `/api/public/plan` | errors403 -> public V3 parse + verify original bytes -> live scheduler preflight | n=1 valid but unsupported; n=2 only 18x20 has scoped preflight readiness; all other valid combinations unsupported |
| `current_entry_launch_x03.server("REQUEST_TRACE_18X22")` -> `request_trace_server109.Handler.do_POST`, same POST path | same errors403 / V3 -> trace preflight | n=1 valid unsupported; only 18x22 matches historical study preflight, but make_request deadline 2026-11-19T15:59:09Z is expired and is NOT reset |
| `automatic_program_search.run_live` / `live_program_scheduler.run_live` | same V3 parse/verify/engine_raw before dispatch | same single 18x20/n2 scope; not variable-input readiness |
| `request_trace109.run/make_request` | same V3 preflight before allocation/spawn | historical deadline still enforced |
| `current_entry_boundary_x03.propose_current/construct_current` | registered identifier -> original public bytes -> verified envelope -> server-owned program/core | only registered n2/P2 FRONT_REAR study; valid input may have no core fit |
| Four current assessors + `current_four_decision.assemble` | direct `check_model_domain` before transport/evaluation | model inputs must be in domain; no report/physical PASS bypass |
| Direct raw repair helpers | `check_raw_domain`, separate internal four-field diagnostic schema | not public input; never advertise requested_count/program as form fields |

Declared registry is exactly two launcher services and two producer/constructor entries. This is not an all-repository call graph or Python sandbox. Source pins and actual callable paths are checked. Old X03/X05 inventories have known stale snapshots; this task does not refresh, disable, or pretend to pass those historical aggregate inventories.

## Exact wire policy (existing V3, unchanged)
- Public body is one JSON object with only W, L, n. Extra program/count/authority/capability fields are rejected.
- Each W/L independently accepts JSON integer or an exact decimal **string**, inclusive 5..25 m. Persian/Arabic digits and decimal separator in strings use the existing translation; no float conversion, rounding, scaling or clamping.
- Decimal strings are preserved in received_input and converted through Decimal/Fraction to an exact numerator/denominator and engine string. Existing 64-character numeric limit is retained.
- Raw JSON decimal/exponent tokens for W/L (including 4.999, 25.001, 18.125, 18e0) are explicitly 409 `UNSUPPORTED_JSON_DECIMAL_REPRESENTATION`. This is unsupported representation, NOT successful dimension validation, NOT valid-unsupported generator capability, and NOT proof the dimension is infeasible.
- String "4.999"/"25.001" instead reaches semantic validation and is 422 `DIMENSION_OUT_OF_OWNER_RANGE`.
- n accepts only integer-token 1 or 2 (integer or permitted digit string). 3/4/fractional/boolean/container values are invalid. Missing, null and blank n are required-input errors. Numeric n:2.0/2e0 is 422 INVALID_BRIEF, never rounded.
- Structural duplicate keys, malformed JSON, nonfinite constants and extra fields fail before generation. Existing resource limits remain separate unsupported-input guards.
- Form uses three text fields and sends their strings unchanged. DOM/source assertions are not pixel review or a new browser behavior claim.

## Six subprocess mappings
1. **1.01 enter W/L/n:** actual three-field form and HTTP body; no requested_count/program UI.
2. **1.02 empty/type checks:** matrix covers missing/empty/null/bool/list/object, malformed/duplicate/nonfinite and extras. Parser is real; dispatch sentinels cannot supply a valid parser result.
3. **1.03 independent 5..25 bounds:** each axis and both endpoints accepted by input contract; outside string endpoints rejected without clamping. Actual HTTP 409 for a valid endpoint means valid but unsupported study case, not invalid or successful generation.
4. **1.04 n=1/2:** input validity is separate from n1 generation capability. P15/P17 work is not completed by this proof.
5. **1.05 exact decimals:** original bytes/envelope binding and exact rational roundtrip on both axes, localized digits, long finite decimal strings and typed tamper tests. Numeric JSON decimal/exponent support remains deliberately absent; no all-representation support claim.
6. **1.06 capability:** real preflight is exercised without generator execution. 18x20 n2 scoped ready is not qualification; historical trace's static 18x22 match is not current executable readiness. P04/P17/P19/P34 remain outside this task.

## Verification and limits
- New test executes both real loopback launcher factories, HTTP server, V3 parser, error collector and preflight. Only run_live, request allocation and subprocess creation are forbidden sentinels for invalid/unsupported cases. No evaluator, MILP or fresh geometry run is required.
- Readiness test uses current real clock and confirms the old trace deadline rejects allocation. No clock patch, deadline reopening or hidden fallback.
- Existing targeted regressions cover source-pinned launcher behavior, direct report guards and real producer/constructor paths stopped at MILP/assembly sentinels. Full geometry/quality is not tested.
- Source bytes are pinned before/after. All input fixtures are synthetic and nonpersonal. No raw model/report or artifact upload.
- Historical `contract114.parse` still permits 5..45 and direct scripts can be manually invoked. The test explicitly proves 26 is historical-parser-valid and current-boundary-invalid. `validation_server` (four-field diagnostic) and frontend/backend/engine/current/latest aliases are excluded from current launch registry; their files are not rewritten. Packaging isolation remains absent.
- Success means the scoped current P03 input/HTTP contract is verified, not that every historical callable is protected or that all valid inputs can produce qualified plans.
