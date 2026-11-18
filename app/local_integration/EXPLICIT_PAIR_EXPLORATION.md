# Explicit two-bedroom exploration

This is an experimental API path, not a qualified plan-delivery product.

- Generate with explicit `"program":{"bedrooms_per_unit":2}`, `n:2`, exact W/L within 5..25. Omission still means the existing three-bedroom programme. There is no silent fallback.
- Main UI does not yet expose a programme selector.
- `POST /redesign-explicit-two` accepts only `{"run_id":"...","candidate_id":"..."}` for an initial, currently source-bound, explicitly two-bedroom historical record.
- It reconstructs the exact constructor127 parent and obtains a fresh review. Only the narrowly classified two-unit guest-dining route failure permits the bounded exploratory search. Unknown-only or unrelated failures do not.
- Parent pending rules are retained. A child is independently constructed and freshly reviewed with the same request, programme, fixture IDs/types/source sizes, source body profile and core.
- The worker is terminated and reaped on cancellation or the 150-second gateway limit. Search tries at most three variants with an internal elapsed budget.
- `/repair` remains separate and does not accept constructor127. No constructor129 precondition is weakened.
- A retained parent is not a new model: generated_count=0, reviewed_candidate_count=1, reused_parent=true. A genuinely new child counts as one.
- All results remain accepted=false, qualified=false, display_allowed=false and delivery_allowed=false. History is historical only; export/download remain denied.

## Verified and not yet verified

Callable replay of a real archived natural failure succeeded in run44406994713: exact parent reconstruction, fresh rejection, a different fresh physical-pass child and six rejected invalid preconditions.

The first live HTTP sample in run44407576996 produced six fresh physical-pass/semantic-unknown parents and no eligible failure. Therefore the successful continuation endpoint branch was **not exercised** in that sample; a green workflow is not a successful live cycle.

Current source hashes are required for saved continuation. Historical results whose producer sources changed are preserved as historical evidence but are not silently treated as current parents.

Four functional requirements, automatic appropriate-programme choice, one-unit support, broader coverage and production-cycle closure remain incomplete. No claim of original version588 recovery or all historical changes is made.
