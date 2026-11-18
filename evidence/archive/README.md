# Selected V25 evidence archive

This private-repository directory preserves generated engineering evidence, not a product release or architectural approval.

- `V25_SELECTED_EVIDENCE_INDEX.json` lists source Actions run IDs, archive SHA-256, and every member's uncompressed SHA-256 and size.
- `V25_run_<run_id>.tar.gz` contains the explicitly selected run's generated JSON, loopback-browser trace/screenshot, and known worker stderr only.
- Original Actions artifacts have a 30-day retention period. Repository archives do not depend on that retention period, but remain subject to normal repository availability and deletion.
- A successful archival workflow is insufficient by itself: check its evidence commit and verify that the index and each referenced blob exist.

## Verification and reproduction

1. Read the corresponding `manifests/V25_*.json` report for the exact tested commit, run, job, scope and original artifact digest.
2. Verify the repository archive's SHA-256 against this index before extracting. Then verify each extracted file against its listed uncompressed SHA-256. Archive and original Actions ZIP digests intentionally differ.
3. Re-run the named workflow on the exact recorded source commit, preserving Python/dependency versions, fixture profile, input request and evaluation gates. Workflows record their bounded budgets. Do not treat a successful diagnostic workflow as an architectural pass.
4. MILP searches with wall-clock limits may return a different incumbent on another runner. Re-running the same input is therefore **not** guaranteed to reproduce the exact original model.
5. To reproduce an archived model, use its saved raw request, ownership family and complete proposal with the original deterministic constructor. Require identical model digest, unchanged historical guard/source revision, and a newly executed compatible review. Never copy an old PASS or FAIL as a fresh result.
6. Two-bedroom studies are explicit separate experiments, not silent fallback from the active three-bedroom adapter. Counterfactual copies are diagnostic interventions, not approved construction records.
7. Full programme suitability, required functional closure, production natural rejection/redesign, and architectural qualification remain separate obligations. No archive grants display, export, release or acceptance.

If a required archive is absent, preserve the exact Actions artifact before its 30-day expiry or record that the evidence was not durably retained. Do not claim permanent preservation based only on a manifest hash.
